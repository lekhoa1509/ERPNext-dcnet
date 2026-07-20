"""Bulk-pump orchestrator — fast SQL-INSERT path for Misa migration.

Replaces the doc-first ORM submit pass (submit_phase_4_drafts) with
direct bulk INSERT of all required tables. For PROOF-OF-CONCEPT scope
only Sales Invoice is implemented; PI/PE/JE/SE/Asset follow in later
commits.

Entry: ``run_bulk_pump_si_only(batch_name, company)`` — handles only
SI vouchers (BH prefix). Used to validate the approach before
extending to other doctypes.
"""
from __future__ import annotations

import json
import time
from typing import Any

import frappe

from vn_accounting.misa_migration.bulk_pump.bulk_executor import (
    bulk_insert, timed_bulk_insert,
)
from vn_accounting.misa_migration.bulk_pump.builders.sales_invoice import (
    build_si_dicts,
)
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    _ensure_placeholder_item,
)
from vn_accounting.misa_migration.importers._naming import (
    company_abbr as _naming_company_abbr,
)


def _name_prefix(company: str | None) -> str:
    """Doc-name prefix matching builders' migrated_doc_name() exactly."""
    return f"{_naming_company_abbr(company)}-" if company else ""


def _auto_promote_phase4_rows_to_ready(batch_name: str) -> int:
    """Promote Phase 4 NKC/BR/MV rows status 'New' → 'Ready' + populate
    voucher_no from raw_payload's `Số chứng từ`.

    bulk_pump builders filter rows by status='Ready' + voucher_no — if those
    aren't set, Phase 4 silently processes 0 vouchers. ORM phase_4_orchestrator
    sets these fields during its dispatch loop, but bulk SQL path skips ORM
    entirely, leaving rows untouched. Without this auto-step, users who click
    'Đăng chế độ nhanh (SQL)' get 0 vouchers and don't know why.

    Returns count of rows promoted. Idempotent — skips Ready rows + rows
    without a voucher_no in the raw payload.
    """
    rows = frappe.db.sql(
        """SELECT name, raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type IN ('NKC','Bang ke BR','Bang ke MV')
             AND status='New'""",
        (batch_name,), as_dict=True,
    )
    if not rows:
        return 0
    promoted = 0
    for r in rows:
        try:
            p = json.loads(r["raw_payload"] or "{}")
        except Exception:
            continue
        sct = str(p.get("Số chứng từ") or "").strip()
        if not sct:
            continue
        frappe.db.sql(
            "UPDATE `tabMisa Migration Row` SET voucher_no=%s, status='Ready' WHERE name=%s",
            (sct, r["name"]),
        )
        promoted += 1
    if promoted:
        frappe.db.commit()
    return promoted


def _company_abbr(company: str) -> str:
    return frappe.db.get_value("Company", company, "abbr") or ""


def _debit_to_account(company: str) -> str:
    """Default receivable account for SI.debit_to (TK 131 by VN convention)."""
    acc = (
        frappe.db.get_value("Company", company, "default_receivable_account")
        or frappe.db.get_value("Account", {
            "company": company, "account_type": "Receivable", "is_group": 0
        }, "name")
    )
    if not acc:
        frappe.throw(f"No receivable account found for {company}")
    return acc


def _load_misa_si_pairs(batch_name: str) -> list[tuple[dict, dict]]:
    """Load (voucher_dict, invoice_dict) pairs for SI bulk-pump.

    Uses the SAME parser stack as the doc-first orchestrator: nkc_parser +
    invoice_list_parser. NKC rows must be status='Ready' (only post pending
    work). BR rows are loaded regardless of status — we need their invoice
    metadata for matching even if the BR rows themselves have been processed.
    """
    from vn_accounting.misa_migration.parsers import (
        nkc_parser, invoice_list_parser,
    )
    from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
        _build_invoice_lookup,
    )

    # NKC: only Ready vouchers with BH prefix
    nkc_payloads = []
    for r in frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC' AND status='Ready'
           AND voucher_no LIKE 'BH%%'""",
        (batch_name,), as_dict=True,
    ):
        try:
            nkc_payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass

    # BR: all (regardless of status) — invoice metadata is needed for matching
    br_payloads = []
    for r in frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='Bang ke BR'""",
        (batch_name,), as_dict=True,
    ):
        try:
            br_payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass

    vouchers = nkc_parser.parse_nkc_rows(nkc_payloads)
    br_invoices = _build_invoice_lookup(
        invoice_list_parser.parse_invoice_list(br_payloads, kind="BR")
    )

    pairs = []
    for voucher in vouchers:
        vno = voucher.get("voucher_no")
        if not vno:
            continue
        invoice = br_invoices.find(vno, voucher.get("invoice_no"))
        if not invoice or not invoice.get("line_items"):
            continue
        pairs.append((voucher, invoice))
    return pairs


def _update_misa_rows_posted(batch_name: str, voucher_nos: list[str]) -> int:
    """Mark Misa Migration Row status=Posted for the given voucher_nos.

    target_name is the company-namespaced doc name ({abbr}-{voucher_no}),
    matching what the SI builder set as the actual doc name.
    """
    if not voucher_nos:
        return 0
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    prefix = _name_prefix(company)
    placeholders = ",".join(["%s"] * len(voucher_nos))
    return frappe.db.sql(
        f"""UPDATE `tabMisa Migration Row`
            SET status='Posted',
                target_doctype='Sales Invoice',
                target_name=CONCAT(%s, voucher_no)
            WHERE batch=%s AND voucher_no IN ({placeholders})""",
        (prefix, batch_name, *voucher_nos),
    )


def _update_ob_inventory_rows_posted(batch_name: str) -> int:
    """Mark all file_type='OB Inventory' rows status=Posted after the bulk
    Stock Entry insert succeeds. SE name format is OB-INV-{batch_name} (stable
    per-batch single SE grouping all item/warehouse pairs).

    Without this, 738+ OB Inventory rows stay Ready after bulk SQL post and
    pre-flight keeps reporting them as 'pending' — confusing the user since
    inventory WAS actually inserted (Bin + SLE created).
    """
    return frappe.db.sql(
        """UPDATE `tabMisa Migration Row`
           SET status='Posted',
               target_doctype='Stock Entry',
               target_name=%s
           WHERE batch=%s AND file_type='OB Inventory' AND status='Ready'""",
        (f"OB-INV-{batch_name}", batch_name),
    )


def _update_customer_outstanding(company: str, voucher_nos: list[str]) -> int:
    """Recompute Customer.outstanding from GL Entry (Dr Receivable - Cr Receivable)
    for each Customer that received a new SI. Idempotent."""
    if not voucher_nos:
        return 0
    # Find unique customers from inserted SI. Match by misa_voucher_no (the
    # raw Misa number) so this is independent of the company-namespaced doc
    # name ({abbr}-{voucher_no}).
    placeholders = ",".join(["%s"] * len(voucher_nos))
    customers = frappe.db.sql_list(
        f"SELECT DISTINCT customer FROM `tabSales Invoice` "
        f"WHERE company=%s AND misa_voucher_no IN ({placeholders})",
        (company, *voucher_nos),
    )
    if not customers:
        return 0
    # Sum Receivable balance per customer from GL
    cph = ",".join(["%s"] * len(customers))
    rows = frappe.db.sql(
        f"""SELECT party, SUM(debit) - SUM(credit) AS bal
            FROM `tabGL Entry`
            WHERE company=%s AND party_type='Customer' AND party IN ({cph})
            AND is_cancelled=0
            GROUP BY party""",
        (company, *customers), as_dict=True,
    )
    # No-op: Customer doctype doesn't have outstanding_amount field.
    # Outstanding is computed on-demand from GL by ERPNext reports.
    return len(rows)


def run_bulk_pump_masters(batch_name: str, company: str = None) -> dict[str, Any]:
    """Phase 1/3 master bulk-pump — CoA leaves + Employee + Bank Account.

    Companion to run_bulk_pump_full (Phase 0/4). Run BEFORE the transactional
    pump so PE.bank_account references resolve, Employee party_type works for
    salary vouchers, and CoA structure mirrors Misa source hierarchy.
    """
    from vn_accounting.misa_migration.bulk_pump.builders.masters import (
        build_employee_dicts, build_bank_account_dicts,
    )
    from vn_accounting.misa_migration.setup.coa_leaves import (
        ensure_coa_leaves_from_batch,
    )
    if not company:
        company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    out: dict[str, Any] = {"company": company, "batch": batch_name}
    t0 = time.time()

    # Source-driven CoA leaf bootstrap. Scans Misa Migration Rows for all
    # TKs referenced (NKC + OB + BR/MV) and creates them under longest-prefix
    # parent — preserves Misa hierarchy (e.g. 1121 as parent of 11215/11218,
    # 3331 as parent of 33311) so BCDTK parent rollups match source.
    coa_out = ensure_coa_leaves_from_batch(batch_name, company)
    out["coa_leaves"] = {
        "created": len(coa_out.get("created") or []),
        "skipped_existing": len(coa_out.get("skipped_existing") or []),
        "skipped_no_parent": len(coa_out.get("skipped_no_parent") or []),
        "source_tks": coa_out.get("source_tks", 0),
        "errors": coa_out.get("errors") or [],
    }

    # Employee
    emp_out = build_employee_dicts(batch_name, company)
    emp_rows = emp_out.get("Employee", [])
    if emp_rows:
        n, secs = timed_bulk_insert("Employee", emp_rows, batch_size=500)
        out["Employee"] = {"inserted": n, "elapsed_seconds": round(secs, 2)}
    else:
        out["Employee"] = {"inserted": 0}
    # Mark Misa rows posted
    for row_name, target in (emp_out.get("_row_to_name") or {}).items():
        frappe.db.sql(
            "UPDATE `tabMisa Migration Row` SET status='Posted', "
            "target_doctype='Employee', target_name=%s WHERE name=%s",
            (target, row_name),
        )

    # Bank + Bank Account
    ba_out = build_bank_account_dicts(batch_name, company)
    bank_rows = ba_out.get("Bank", [])
    if bank_rows:
        n, secs = timed_bulk_insert("Bank", bank_rows, batch_size=500)
        out["Bank"] = {"inserted": n, "elapsed_seconds": round(secs, 2)}
    bacc_rows = ba_out.get("Bank Account", [])
    if bacc_rows:
        n, secs = timed_bulk_insert("Bank Account", bacc_rows, batch_size=500)
        out["Bank Account"] = {"inserted": n, "elapsed_seconds": round(secs, 2)}
    else:
        out["Bank Account"] = {"inserted": 0}
    for row_name, target in (ba_out.get("_row_to_name") or {}).items():
        frappe.db.sql(
            "UPDATE `tabMisa Migration Row` SET status='Posted', "
            "target_doctype='Bank Account', target_name=%s WHERE name=%s",
            (target, row_name),
        )

    frappe.db.commit()
    out["elapsed_seconds"] = round(time.time() - t0, 2)
    return out


def run_bulk_pump_full(batch_name: str, company: str = None,
                       include_opening: bool = True) -> dict[str, Any]:
    """Bulk-pump ALL phases — SI + PI + PE + JE + SE + Asset.

    Order: JE → SE → SI → PI → PE (mirrors ORM submit order for consistency).
    Each phase runs independently; failures in one don't affect others.

    Returns timing breakdown per DocType + per table.
    """
    from vn_accounting.misa_migration.parsers import (
        nkc_parser, invoice_list_parser,
    )
    from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
        _build_invoice_lookup,
    )
    from vn_accounting.misa_migration.bulk_pump.builders.journal_entry import build_je_dicts
    from vn_accounting.misa_migration.bulk_pump.builders.purchase_invoice import build_pi_dicts
    from vn_accounting.misa_migration.bulk_pump.builders.payment_entry import build_pe_dicts
    from vn_accounting.misa_migration.bulk_pump.builders.stock_entry import build_se_dicts
    from vn_accounting.misa_migration.bulk_pump.builders.asset import build_asset_dicts
    from vn_accounting.misa_migration.bulk_pump.builders.opening_balance import build_opening_je
    from vn_accounting.misa_migration.bulk_pump.builders.opening_inventory import build_opening_inventory
    from vn_accounting.misa_migration.bulk_pump.post_derive import (
        rebuild_bin_for_company, rebuild_payment_ledger_entry_for_company,
        backfill_pe_references_for_company,
    )
    from vn_accounting.misa_migration.bulk_pump.validate_sample import validate_sample
    from vn_accounting.misa_migration.bulk_pump import account_resolver, warehouse_resolver
    from vn_accounting.misa_migration.parsers import sct_parser

    t0 = time.time()
    if not company:
        company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")

    # Auto-promote Phase 4 NKC/BR/MV rows to status='Ready' + populate
    # voucher_no from raw_payload. Required because builders filter by
    # status='Ready' — without this, bulk SQL silently processes 0 vouchers.
    _auto_promote_phase4_rows_to_ready(batch_name)

    co_doc = frappe.get_doc("Company", company)
    abbr = co_doc.abbr or ""
    debit_to = _debit_to_account(company)
    credit_to = co_doc.default_payable_account
    default_expense = co_doc.default_expense_account
    default_income = co_doc.default_income_account or "511 - Doanh thu bán hàng và cung cấp dịch vụ - DCT"
    stock_adj = co_doc.stock_adjustment_account or default_expense
    default_cash = co_doc.default_cash_account or debit_to
    # Default Cost Center — required by ERPNext's validate_cost_center.
    # Without it, every doc opens with "Trung tâm chi phí None không thuộc
    # về công ty X" popup (Frappe interpolates NULL as "None" in the
    # f-string error). Each builder should stamp this onto every row that
    # carries cost_center (SI/PI items + taxes, JE Account, PE/PE Deduction,
    # SE Detail, GL Entry, Asset).
    default_cc = co_doc.cost_center or frappe.db.get_value(
        "Cost Center",
        {"company": company, "is_group": 0},
        "name", order_by="creation",
    )
    # Pre-warm resolver caches for this company
    account_resolver.reset()
    account_resolver.warm_cache(company)
    warehouse_resolver.reset()
    warehouse_resolver.warm_cache(company)

    # Load NKC + BR all in one go (one batch query)
    nkc_payloads = []
    for r in frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC' AND status='Ready'""",
        (batch_name,), as_dict=True,
    ):
        try:
            nkc_payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass
    br_payloads = []
    for r in frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='Bang ke BR'""",
        (batch_name,), as_dict=True,
    ):
        try:
            br_payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass
    mv_payloads = []
    for r in frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='Bang ke MV'""",
        (batch_name,), as_dict=True,
    ):
        try:
            mv_payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass

    vouchers = nkc_parser.parse_nkc_rows(nkc_payloads)
    br_invoices = _build_invoice_lookup(invoice_list_parser.parse_invoice_list(br_payloads, kind="BR"))
    mv_invoices = _build_invoice_lookup(invoice_list_parser.parse_invoke_list(mv_payloads, kind="MV") if False else invoice_list_parser.parse_invoice_list(mv_payloads, kind="MV"))

    # SCT for SE item-line lookup (Misa Sổ chi tiết)
    sct_payloads = []
    for r in frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` WHERE batch=%s AND file_type='SCT'",
        (batch_name,), as_dict=True,
    ):
        try:
            sct_payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass
    # SCT raw_payload is already in parsed snake_case shape (parser ran at upload).
    # Skip re-parsing; group directly.
    sct_by_voucher = sct_parser.group_by_voucher(sct_payloads)

    placeholder = _ensure_placeholder_item(company)
    all_rows: dict[str, list[dict]] = {}
    posted_voucher_map: dict[str, str] = {}  # voucher_no → target_doctype
    # SLE state — accumulates across SE vouchers in posting_date order
    sle_state: dict[tuple, dict] = {}

    # === Phase 0 — Opening Balance JE ===
    ob_date = (
        frappe.db.get_value("Misa Migration Batch", batch_name, "ob_posting_date")
        or "2024-12-31"
    )

    # Helper: stamp default_cc on every accounting-shaped row from a builder
    # output that didn't set cost_center explicitly. Skips tables whose
    # schema doesn't have a cost_center column (e.g. Journal Entry parent
    # — only Journal Entry Account child carries cost_center) so the bulk
    # INSERT doesn't fail with "Unknown column 'cost_center' in 'INSERT INTO'".
    _CC_TABLE_CACHE: dict[str, bool] = {}
    def _table_has_cc(tbl: str) -> bool:
        if tbl not in _CC_TABLE_CACHE:
            _CC_TABLE_CACHE[tbl] = bool(frappe.db.has_column(tbl, "cost_center"))
        return _CC_TABLE_CACHE[tbl]

    def _stamp_cc(out_dict):
        if not default_cc or not out_dict:
            return
        for tbl, tbl_rows in out_dict.items():
            if not isinstance(tbl_rows, list):
                continue
            if not _table_has_cc(tbl):
                continue
            for row in tbl_rows:
                if isinstance(row, dict) and "cost_center" not in row:
                    if any(k in row for k in ("account", "debit", "credit", "item_code", "company")):
                        row["cost_center"] = default_cc

    if not include_opening:
        print("[bulk_pump_full] include_opening=False — skip Phase 0 "
              "(công ty đã có sổ từ đợt trước)", flush=True)
    ob_out = build_opening_je(batch_name, company, str(ob_date)) if include_opening else None
    print(f"[bulk_pump_full] Building Phase 0 OB JE for {ob_date}...", flush=True)
    if ob_out:
        _stamp_cc(ob_out)
        for k, v in ob_out.items():
            all_rows.setdefault(k, []).extend(v)
        print(f"  OB JE: {len(ob_out.get('Journal Entry Account', []))} accounts", flush=True)

    # === Phase 0 — Opening Inventory (Material Receipt SE) ===
    print(f"[bulk_pump_full] Building Phase 0 OB Inventory...", flush=True)
    oi_out = build_opening_inventory(batch_name, company, str(ob_date)) if include_opening else None
    if oi_out:
        _stamp_cc(oi_out)
        for k, v in oi_out.items():
            all_rows.setdefault(k, []).extend(v)
        print(f"  OB Inventory: {len(oi_out.get('Stock Entry Detail', []))} (item,warehouse) pairs",
              flush=True)

    # === Phase 0 — Opening Asset + CCDC ===
    print(f"[bulk_pump_full] Building Phase 0 Assets...", flush=True)
    seen_asset_codes: set[str] = set()  # dedupe — Misa may list same code in both FA + CCDC
    for ft, is_ccdc in (("OB Fixed Asset", False), ("OB CCDC", True)):
        for r in frappe.db.sql(
            "SELECT raw_payload FROM `tabMisa Migration Row` "
            "WHERE batch=%s AND file_type=%s AND status NOT IN ('Skipped','Failed','Invalid')",
            (batch_name, ft), as_dict=True,
        ):
            try:
                p = json.loads(r["raw_payload"] or "{}")
            except (TypeError, ValueError):
                continue
            # Normalize Misa raw keys → builder-expected snake_case
            asset_data = {
                "asset_code": p.get("Mã tài sản") or p.get("Mã CCDC"),
                "ccdc_code": p.get("Mã CCDC") or p.get("Mã tài sản"),
                "asset_name": p.get("Tên tài sản") or p.get("Tên CCDC"),
                "ccdc_name": p.get("Tên CCDC") or p.get("Tên tài sản"),
                "gross_amount": p.get("Nguyên giá") or p.get("Giá trị CCDC") or 0,
                "accumulated_depreciation": p.get("Hao mòn lũy kế") or 0,
                "useful_life_months": p.get("Thời gian SD (tháng)"),
                "total_periods": p.get("Số kỳ phân bổ"),
                "qty": p.get("Số lượng") or 1,
                "available_for_use_date": p.get("Ngày ghi tăng"),
                "recognition_date": p.get("Ngày ghi tăng"),
            }
            # Default Asset Category — first existing for this company
            asset_cat = frappe.db.get_value(
                "Asset Category", {}, "name", order_by="creation",
            ) or "Equipment"
            # Default Location — first existing
            location = frappe.db.get_value("Location", {}, "name") or None
            if not location:
                continue
            code = asset_data["asset_code"] or asset_data["ccdc_code"]
            if not code or code in seen_asset_codes:
                continue
            asset_out = build_asset_dicts(
                asset_data, company, asset_cat, location, is_ccdc=is_ccdc,
            )
            if asset_out:
                seen_asset_codes.add(code)
                _stamp_cc(asset_out)
                for k, v in asset_out.items():
                    all_rows.setdefault(k, []).extend(v)

    # Sort vouchers by posting_date so SLE state accumulates correctly
    vouchers.sort(key=lambda v: (str(v.get("posting_date") or "9999"), v.get("voucher_no") or ""))

    # Canonical Misa prefix → bulk_pump builder (aligned with ORM voucher_router).
    # Use EXACT match against voucher.prefix; fallback to leading-letters of vno
    # when voucher.prefix is empty. Unknown prefixes fall through to JE.
    SI_PREFIXES = {"BH"}
    PI_PREFIXES = {"MDV", "MH"}
    # PN is PI+PR in ORM (purchase_receipt module); not yet implemented in bulk_pump
    # — keep routing to SE as stop-gap until v1.1.
    SE_PREFIXES = {"PN", "PNHN", "PX", "PXHN", "PNN", "PXDNG", "PXK"}
    PE_PREFIXES = {"BC", "UNC", "PT", "PC"}
    JE_PREFIXES = {"CTNB", "NVK", "PBDT", "PBPTT", "PBCC", "KH", "CK"}

    import re as _re
    def _extract_prefix(v):
        p = (v.get("prefix") or "").upper()
        if p:
            return p
        m = _re.match(r"^([A-Z]+)", v.get("voucher_no") or "")
        return m.group(1).upper() if m else ""

    print(f"[bulk_pump_full] {len(vouchers)} vouchers to dispatch", flush=True)
    t_build = time.time()
    skip_count = 0
    for voucher in vouchers:
        vno = voucher.get("voucher_no")
        if not vno:
            skip_count += 1; continue
        prefix = _extract_prefix(voucher)
        out = None
        target_dt = None

        if prefix in SI_PREFIXES:
            invoice = br_invoices.find(vno, voucher.get("invoice_no"))
            if invoice and invoice.get("line_items"):
                out = build_si_dicts(voucher, invoice, company, abbr, placeholder, debit_to, default_income)
                target_dt = "Sales Invoice"
            if not out:
                # BH không có dòng bảng kê BR (Misa không đưa hóa đơn điều
                # chỉnh vào bảng kê bán ra — BH20252600/BH20252217 làm lệch
                # 131 −31,5M + 4212 +29,1M trên tập 2025) → fallback JE từ
                # chân NKC, mất phân hệ nhưng sổ cái đủ chân (như ORM router).
                out = build_je_dicts(voucher, company)
                target_dt = "Journal Entry"
        elif prefix in PI_PREFIXES:
            invoice = mv_invoices.find(vno, voucher.get("invoice_no")) or br_invoices.find(vno, voucher.get("invoice_no"))
            if invoice and invoice.get("line_items"):
                out = build_pi_dicts(voucher, invoice, company, placeholder, credit_to, default_expense)
                target_dt = "Purchase Invoice"
            else:
                out = build_je_dicts(voucher, company)
                target_dt = "Journal Entry"
        elif prefix in PE_PREFIXES:
            out = build_pe_dicts(voucher, company, default_cash, debit_to, credit_to)
            target_dt = "Payment Entry"
            if not out:
                out = build_je_dicts(voucher, company)
                target_dt = "Journal Entry"
        elif prefix in SE_PREFIXES:
            sct_voucher = sct_by_voucher.get(vno)
            sct_lines = (sct_voucher.get("lines") if sct_voucher else None) or []
            if sct_lines:
                out = build_se_dicts(voucher, company, stock_adj, sct_lines=sct_lines, sle_state=sle_state)
                target_dt = "Stock Entry"
            if not out:
                out = build_je_dicts(voucher, company)
                target_dt = "Journal Entry"
        else:  # JE_PREFIXES + unknown
            out = build_je_dicts(voucher, company)
            target_dt = "Journal Entry"

        if not out:
            skip_count += 1
            continue
        # Stamp default cost_center on every accounting-shaped row that didn't
        # set one — avoids "Trung tâm chi phí None" popup on doc open.
        _stamp_cc(out)
        for k, v in out.items():
            all_rows.setdefault(k, []).extend(v)
        posted_voucher_map[vno] = target_dt
    print(f"[bulk_pump_full] Built in {time.time()-t_build:.1f}s "
          f"({len(posted_voucher_map)} vouchers, {skip_count} skipped)", flush=True)
    for k, rs in all_rows.items():
        print(f"  {k}: {len(rs)}", flush=True)

    # Bulk INSERT — order matters: parents before children where FK applies
    insert_order = [
        "Sales Invoice", "Sales Invoice Item", "Sales Taxes and Charges",
        "Purchase Invoice", "Purchase Invoice Item", "Purchase Taxes and Charges",
        "Payment Entry",
        "Journal Entry", "Journal Entry Account",
        "Stock Entry", "Stock Entry Detail",
        "Asset", "Asset Finance Book", "Depreciation Schedule",
        "Payment Schedule",
        "GL Entry",
        "Stock Ledger Entry",
    ]
    counts = {}
    timings = {}
    for tbl in insert_order:
        rows = all_rows.get(tbl, [])
        if not rows:
            continue
        n, secs = timed_bulk_insert(tbl, rows, batch_size=500)
        counts[tbl] = n
        timings[tbl] = secs
        print(f"[bulk_pump_full] tab{tbl}: {n} in {secs:.2f}s ({n/secs:.0f}/s)" if secs > 0 else f"[bulk_pump_full] tab{tbl}: {n}", flush=True)
    frappe.db.commit()

    # Mark Misa rows
    by_dt: dict[str, list[str]] = {}
    for vno, dt in posted_voucher_map.items():
        by_dt.setdefault(dt, []).append(vno)
    _mark_prefix = _name_prefix(company)
    for dt, vnos in by_dt.items():
        if not vnos:
            continue
        placeholders = ",".join(["%s"] * len(vnos))
        frappe.db.sql(
            f"""UPDATE `tabMisa Migration Row`
                SET status='Posted', target_doctype=%s,
                    target_name=CONCAT(%s, voucher_no)
                WHERE batch=%s AND voucher_no IN ({placeholders})""",
            (dt, _mark_prefix, batch_name, *vnos),
        )
    frappe.db.commit()

    # === Post-derive: PE→SI/PI allocation, Bin, Payment Ledger Entry ===
    print(f"[bulk_pump_full] Backfilling PE→SI/PI references...", flush=True)
    n_refs, refs_summary = backfill_pe_references_for_company(company)
    print(f"  PE refs: {n_refs} rows | linked={refs_summary['linked']} "
          f"no_match={refs_summary['no_match']} "
          f"in {refs_summary['elapsed_seconds']:.1f}s", flush=True)
    print(f"[bulk_pump_full] Rebuilding Bin + PLE...", flush=True)
    n_bin, t_bin = rebuild_bin_for_company(company)
    print(f"  Bin: {n_bin} rows in {t_bin:.1f}s", flush=True)
    n_ple, t_ple = rebuild_payment_ledger_entry_for_company(company)
    print(f"  PLE: {n_ple} rows in {t_ple:.1f}s", flush=True)

    # === Safety net: ORM .validate() sample-pass on SI/PI/PE ===
    print(f"[bulk_pump_full] Running ORM validate() safety sample...", flush=True)
    try:
        vsample = validate_sample(company, sample_pct=0.5, fail_threshold_pct=5.0)
        print(f"  validate-sample: {vsample['total_sampled']} sampled, "
              f"{vsample['total_failed']} failed "
              f"({vsample['fail_pct']:.1f}%) in {vsample['elapsed_seconds']:.1f}s "
              f"— {'PASS' if vsample['passed_threshold'] else 'FAIL'}",
              flush=True)
    except Exception as exc:
        vsample = {"error": f"{type(exc).__name__}: {exc}", "passed_threshold": None}
        print(f"  validate-sample crashed: {vsample['error']}", flush=True)

    # === Audit-fix pass: year-end closing + reconcile + status cleanup ===
    print(f"[bulk_pump_full] Running audit-fix backfill pass...", flush=True)
    audit_summary: dict[str, Any] = {}
    try:
        from vn_accounting.misa_migration.bulk_pump import backfill_audit_fixes
        # P&L residual close DEFERRED: at this point GL is the raw bulk
        # output — the reconcile stage rewrites it from NKC legs right
        # after, which would invalidate any residual computed here (E2E
        # vòng 6: stale PL-CLOSE Cr 6321 5,85 tỷ). auto_pipeline runs the
        # close at the END of reconcile instead.
        audit_summary = backfill_audit_fixes.run_all(
            company=company, include_pl_residual_close=False)
        print(f"  audit-fix DONE in {audit_summary.get('total_elapsed_seconds', 0)}s",
              flush=True)
    except Exception as exc:
        audit_summary = {"error": f"{type(exc).__name__}: {exc}"}
        print(f"  audit-fix crashed: {audit_summary['error']}", flush=True)
        import traceback; traceback.print_exc()

    elapsed = time.time() - t0
    print(f"[bulk_pump_full] DONE in {elapsed:.1f}s "
          f"({len(posted_voucher_map)} vouchers)", flush=True)

    return {
        "batch": batch_name, "company": company,
        "elapsed_seconds": round(elapsed, 1),
        "voucher_count": len(posted_voucher_map),
        "skipped_count": skip_count,
        "by_doctype": {dt: len(v) for dt, v in by_dt.items()},
        "insert_counts": counts,
        "insert_timings": {k: round(v, 2) for k, v in timings.items()},
        "validate_sample": vsample,
        "audit_fix": audit_summary,
    }


def run_bulk_pump_si_only(batch_name: str, company: str = None) -> dict[str, Any]:
    """Bulk-pump only Sales Invoices for ``batch_name``. Proof-of-concept entry.

    Returns timing + count breakdown. Idempotent: skips vouchers already
    marked Posted in Misa Migration Row.
    """
    t0 = time.time()
    if not company:
        company = (
            frappe.db.get_value("Misa Migration Batch", batch_name, "company")
            or frappe.db.get_value("Company", {}, "name")
        )
    abbr = _company_abbr(company)
    debit_to = _debit_to_account(company)
    placeholder = _ensure_placeholder_item(company)

    print(f"[bulk_pump] Loading SI pairs for batch {batch_name}...", flush=True)
    t_load = time.time()
    pairs = _load_misa_si_pairs(batch_name)
    print(f"[bulk_pump]   {len(pairs)} SI pairs loaded in {time.time()-t_load:.1f}s", flush=True)

    # Build all dicts in-memory
    print(f"[bulk_pump] Building dicts for {len(pairs)} SIs...", flush=True)
    t_build = time.time()
    all_rows: dict[str, list[dict]] = {
        "Sales Invoice": [],
        "Sales Invoice Item": [],
        "Sales Taxes and Charges": [],
        "Payment Schedule": [],
        "GL Entry": [],
    }
    posted_vouchers: list[str] = []
    skipped = 0
    for voucher, invoice in pairs:
        out = build_si_dicts(
            voucher, invoice, company, abbr, placeholder, debit_to,
        )
        if not out:
            skipped += 1
            continue
        for k, v in out.items():
            all_rows[k].extend(v)
        posted_vouchers.append(voucher["voucher_no"])
    print(f"[bulk_pump]   Built in {time.time()-t_build:.1f}s. "
          f"SI={len(all_rows['Sales Invoice'])}, Items={len(all_rows['Sales Invoice Item'])}, "
          f"Taxes={len(all_rows['Sales Taxes and Charges'])}, "
          f"PS={len(all_rows['Payment Schedule'])}, "
          f"GL={len(all_rows['GL Entry'])}", flush=True)

    # Bulk INSERT
    counts: dict[str, int] = {}
    timings: dict[str, float] = {}
    for table in ("Sales Invoice", "Sales Invoice Item",
                  "Sales Taxes and Charges", "Payment Schedule", "GL Entry"):
        n, secs = timed_bulk_insert(table, all_rows[table], batch_size=500)
        counts[table] = n
        timings[table] = secs
        print(f"[bulk_pump]   bulk_insert tab{table}: {n} rows in {secs:.1f}s "
              f"({n/secs:.0f} rows/s)" if secs > 0 else f"[bulk_pump]   {table}: 0", flush=True)

    # Single commit for all bulk inserts
    frappe.db.commit()

    # Mark Misa rows posted (separate commit)
    n_updated = _update_misa_rows_posted(batch_name, posted_vouchers)
    n_ob_inv = _update_ob_inventory_rows_posted(batch_name)
    frappe.db.commit()
    print(f"[bulk_pump] Marked {n_updated} NKC + {n_ob_inv} OB Inventory "
          f"Misa Migration Rows as Posted", flush=True)

    elapsed = time.time() - t0
    print(f"[bulk_pump] DONE in {elapsed:.1f}s "
          f"({len(posted_vouchers)} SIs / {len(posted_vouchers)/elapsed:.0f} SI/s)", flush=True)

    return {
        "batch": batch_name, "company": company,
        "elapsed_seconds": round(elapsed, 1),
        "si_count": len(posted_vouchers),
        "skipped_count": skipped,
        "insert_counts": counts,
        "insert_timings": {k: round(v, 2) for k, v in timings.items()},
    }
