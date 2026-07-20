"""Stock Entry bulk-pump builder.

SE has 3 main types:
  - Material Receipt (PN*): t_warehouse only, GL Dr Inventory / Cr 632 (or stock_adjust)
  - Material Issue (PX*): s_warehouse only, GL Dr 632 / Cr Inventory
  - Material Transfer (PXHN*): s+t warehouse, GL = balanced (no net change)

Each SE creates:
  - tabStock Entry (parent)
  - tabStock Entry Detail (per-item child)
  - tabStock Ledger Entry (per-item-warehouse — qty_after_transaction is HARD)
  - tabGL Entry (Dr/Cr inventory account vs stock_adjustment)

WARNING: SLE qty_after_transaction requires KNOWING current stock state.
This builder ASSUMES single-batch migration starting from zero stock and
processes in posting_date order so we can accumulate state in memory.
For incremental migration on top of existing stock, would need to read
current Bin balance before each row.
"""
from __future__ import annotations

import secrets
from typing import Any

import frappe
from frappe.utils import getdate, now_datetime

from vn_accounting.misa_migration.bulk_pump import warehouse_resolver, account_resolver
from vn_accounting.misa_migration.importers._naming import migrated_doc_name


def _gen_name() -> str:
    return secrets.token_hex(5)


def _resolve_wh(bare: str | None, company: str) -> str | None:
    """Resolve bare Misa warehouse name → suffixed ERPNext name.
    Returns None if unknown — caller decides to fall back or skip the row.
    """
    if not bare:
        return None
    full = warehouse_resolver.resolve(bare, company)
    return full or bare  # fall back to bare; safer than dropping the line


_WH_ACCOUNT_CACHE: dict[str, str | None] = {}


def _warehouse_account(warehouse: str | None, fallback: str) -> str:
    """Resolve Warehouse.account (the inventory TK like 1561), with caching.
    Falls back to ``fallback`` (typically stock_adjustment_account / TK 632)
    when the warehouse is unknown or has no account configured."""
    if not warehouse:
        return fallback
    if warehouse in _WH_ACCOUNT_CACHE:
        return _WH_ACCOUNT_CACHE[warehouse] or fallback
    acc = frappe.db.get_value("Warehouse", warehouse, "account")
    _WH_ACCOUNT_CACHE[warehouse] = acc
    return acc or fallback


def build_se_dicts(
    voucher: dict[str, Any],
    company: str,
    stock_adjustment_account: str,
    posting_user: str = "Administrator",
    sct_lines: list[dict] | None = None,
    sle_state: dict[tuple, dict] | None = None,
) -> dict[str, list[dict]] | None:
    """Build SE + Stock Entry Detail + SLE + GL rows for one SE voucher.

    sct_lines: pre-loaded SCT item-line list for this voucher (qty + value)
    sle_state: {(item_code, warehouse): {qty, value, rate}} — mutated in place
               so successive vouchers can use prior balance.
    """
    voucher_no = voucher.get("voucher_no")
    if not voucher_no or not sct_lines:
        return None
    posting_date = voucher.get("posting_date")
    if not posting_date:
        return None
    now = frappe.utils.now()
    posting_time = "00:00:00"
    posting_dt_str = f"{posting_date} {posting_time}"
    fiscal_year = str(getdate(posting_date).year)
    if sle_state is None:
        sle_state = {}

    prefix = voucher_no[:2].upper()
    is_receipt = prefix == "PN"
    is_issue = prefix == "PX" and not voucher_no.startswith("PXHN")
    is_transfer = voucher_no.startswith("PXHN") or voucher_no.startswith("PNHN")

    # Company-namespace the doc name AFTER prefix detection (which needs the
    # raw voucher_no). Raw kept for misa_voucher_no.
    voucher_no_raw = voucher_no
    voucher_no = migrated_doc_name(company, voucher_no)

    # Refine PXHN/PNHN classification from SCT shape. Some Misa tenants (DCNET)
    # use PXHN as one-way Issue (Dr 6xxx/Cr 1561), not a Transfer. SCT shape is
    # the truth: pure qty_out → Issue, pure qty_in → Receipt, both → Transfer.
    # Without this override, PXHN posts no GL (Transfer wash on same warehouse)
    # → TK 1561 short by source's PXHN Cr movements.
    if is_transfer and sct_lines:
        has_in = any(float(line.get("qty_in") or 0) > 0 for line in sct_lines)
        has_out = any(float(line.get("qty_out") or 0) > 0 for line in sct_lines)
        if has_out and not has_in:
            is_transfer = False
            is_issue = True
        elif has_in and not has_out:
            is_transfer = False
            is_receipt = True

    if is_receipt:
        se_type = "Material Receipt"
    elif is_transfer:
        se_type = "Material Transfer"
    elif is_issue:
        se_type = "Material Issue"
    else:
        return None  # Unknown type

    # Build details + SLE + GL
    details_rows: list[dict] = []
    sle_rows: list[dict] = []
    gl_rows: list[dict] = []
    total_outgoing = total_incoming = 0.0
    # Per-warehouse aggregation for GL postings.
    # For Material Issue: out_by_wh[wh] += amount → Cr wh.account / Dr stock_adj.
    # For Material Receipt: in_by_wh[wh] += amount → Dr wh.account / Cr stock_adj.
    # For Material Transfer: out_by_wh + in_by_wh both populated; GL Dr target.account / Cr source.account per pair.
    out_by_wh: dict[str, float] = {}
    in_by_wh: dict[str, float] = {}
    # For Transfer, track (source_wh, target_wh) → amount so we can post a
    # paired Dr/Cr instead of bucketing by side.
    transfer_pairs: dict[tuple[str, str], float] = {}

    for idx, line in enumerate(sct_lines):
        item_code = line.get("item_code")
        if not item_code:
            continue
        # SCT separates incoming (qty_in/value_in) vs outgoing (qty_out/value_out)
        qty_in = float(line.get("qty_in") or 0)
        qty_out = float(line.get("qty_out") or 0)
        value_in = float(line.get("value_in") or 0)
        value_out = float(line.get("value_out") or 0)
        qty = qty_in if is_receipt else (qty_out if is_issue else (qty_in or qty_out))
        amount = value_in if is_receipt else (value_out if is_issue else (value_in or value_out))
        if qty <= 0:
            continue
        rate = round(amount / qty, 2) if qty > 0 else 0
        # Warehouse from line — resolve to suffixed ERPNext Warehouse.name so
        # SLE/SED join cleanly to tabWarehouse (Bin rebuild + stock reports).
        wh_code = line.get("warehouse_name") or line.get("warehouse_code")
        wh_resolved = _resolve_wh(wh_code, company)
        s_wh = wh_resolved if is_issue or is_transfer else None
        t_wh = wh_resolved if is_receipt or is_transfer else None

        details_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "item_code": item_code,
            "item_name": str(line.get("item_name") or item_code)[:140],
            "qty": qty, "transfer_qty": qty,
            "uom": "Nos", "stock_uom": "Nos", "conversion_factor": 1,
            "s_warehouse": s_wh, "t_warehouse": t_wh,
            "basic_rate": rate, "valuation_rate": rate,
            "basic_amount": amount, "amount": amount,
            "expense_account": stock_adjustment_account,
            "use_serial_batch_fields": 1,
            "parent": voucher_no, "parenttype": "Stock Entry", "parentfield": "items",
        })
        if t_wh:
            total_incoming += amount
            in_by_wh[t_wh] = in_by_wh.get(t_wh, 0.0) + amount
        if s_wh:
            total_outgoing += amount
            out_by_wh[s_wh] = out_by_wh.get(s_wh, 0.0) + amount
        if is_transfer and s_wh and t_wh:
            transfer_pairs[(s_wh, t_wh)] = transfer_pairs.get((s_wh, t_wh), 0.0) + amount

        # SLE — outgoing
        if s_wh:
            key = (item_code, s_wh)
            cur = sle_state.get(key) or {"qty": 0, "value": 0}
            new_qty = cur["qty"] - qty
            new_value = cur["value"] - amount
            sle_state[key] = {"qty": new_qty, "value": new_value, "rate": rate}
            sle_rows.append({
                "name": _gen_name(),
                "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
                "docstatus": 1, "idx": 0,
                "item_code": item_code, "warehouse": s_wh,
                "posting_date": posting_date, "posting_time": posting_time,
                "posting_datetime": now_datetime(),
                "voucher_type": "Stock Entry", "voucher_no": voucher_no,
                "actual_qty": -qty, "qty_after_transaction": new_qty,
                "incoming_rate": 0, "outgoing_rate": rate, "valuation_rate": rate,
                "stock_value": new_value, "stock_value_difference": -amount,
                "stock_uom": "Nos",
                "company": company, "fiscal_year": fiscal_year,
                "is_cancelled": 0,
            })
        # SLE — incoming
        if t_wh:
            key = (item_code, t_wh)
            cur = sle_state.get(key) or {"qty": 0, "value": 0}
            new_qty = cur["qty"] + qty
            new_value = cur["value"] + amount
            sle_state[key] = {"qty": new_qty, "value": new_value, "rate": rate}
            sle_rows.append({
                "name": _gen_name(),
                "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
                "docstatus": 1, "idx": 0,
                "item_code": item_code, "warehouse": t_wh,
                "posting_date": posting_date, "posting_time": posting_time,
                "posting_datetime": now_datetime(),
                "voucher_type": "Stock Entry", "voucher_no": voucher_no,
                "actual_qty": qty, "qty_after_transaction": new_qty,
                "incoming_rate": rate, "outgoing_rate": 0, "valuation_rate": rate,
                "stock_value": new_value, "stock_value_difference": amount,
                "stock_uom": "Nos",
                "company": company, "fiscal_year": fiscal_year,
                "is_cancelled": 0,
            })

    if not details_rows:
        return None

    se_row = {
        "name": voucher_no,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "stock_entry_type": se_type, "purpose": se_type,
        "posting_date": posting_date, "posting_time": posting_time,
        "set_posting_time": 1,
        "total_outgoing_value": total_outgoing, "total_incoming_value": total_incoming,
        "value_difference": total_incoming - total_outgoing,
        "total_amount": total_incoming if is_receipt else total_outgoing,
        "remarks": (voucher.get("voucher_remark") or "")[:240],
        "is_opening": "No", "is_return": 0,
        "misa_voucher_no": voucher_no_raw,
    }

    # GL — per-warehouse Dr/Cr to the warehouse's inventory account so the BS
    # actually reflects stock movement instead of net-zeroing TK 632.
    #
    #   Material Receipt:   Dr <warehouse.account>  / Cr <stock_adjustment>
    #   Material Issue:     Dr <stock_adjustment>   / Cr <warehouse.account>
    #   Material Transfer:  Dr <target.account>     / Cr <source.account>
    #
    # If two warehouses on the same Transfer share the same Warehouse.account
    # the entry is a wash on that TK — that's correct, no posting needed.
    def _gl_row(account: str, debit: float, credit: float, label: str) -> dict:
        return {
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date, "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": account, "account_currency": "VND",
            "voucher_type": "Stock Entry", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": round(debit, 0), "debit_in_account_currency": round(debit, 0),
            "debit_in_transaction_currency": round(debit, 0), "debit_in_reporting_currency": round(debit, 0),
            "credit": round(credit, 0), "credit_in_account_currency": round(credit, 0),
            "credit_in_transaction_currency": round(credit, 0), "credit_in_reporting_currency": round(credit, 0),
            "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"SE {voucher_no} {label}",
        }

    # When PN voucher has Supplier party_code, route Cr to TK 331 (party_account)
    # instead of stock_adjustment — matches Misa NKC pattern Dr 156 / Cr 331.
    # Without this fix, source's TK 331 Cr 1.25B from PN vouchers ends up
    # mis-routed to stock_adjustment, leaving 331 CB Cr short by 1.25B.
    pn_supplier = None
    pn_party_account = None
    if is_receipt:
        party_code = (voucher.get("party_code") or "").strip()
        if party_code:
            from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache
            if _party_cache.is_supplier(party_code):
                canon = frappe.db.get_value("Supplier", party_code, "name")
                if canon:
                    pn_supplier = canon
                    pn_party_account = account_resolver.resolve("331", company)

    # Resolve actual contra TK from NKC legs. For Issue, the Dr leg's TK
    # (6xxx/8xxx) is the right "expense" account — using default
    # stock_adjustment_account loses sub-account precision (632 vs 6321/6322/
    # 6323/6427). For Receipt return-to-inventory pattern (PN with Cr 6xxx
    # contra), the Cr leg's TK overrides the default Cr 331 supplier route.
    def _bare(raw):
        return (raw if " - " not in raw else raw.split(" - ", 1)[0]).strip()

    issue_dr_acc = None
    receipt_cr_acc = None
    legs = voucher.get("legs") or []
    for leg in legs:
        raw_acc = leg.get("account_resolved") or leg.get("account") or ""
        bare = _bare(raw_acc)
        dr = float(leg.get("debit") or 0)
        cr = float(leg.get("credit") or 0)
        # Issue / Transfer: Dr leg on 6xxx/8xxx is the contra
        if is_issue and dr > 0 and bare.startswith(("6", "8")) and not issue_dr_acc:
            issue_dr_acc = account_resolver.resolve(bare, company) or raw_acc
        # Receipt return: Cr leg on 6xxx/8xxx replaces supplier Cr 331
        if is_receipt and cr > 0 and bare.startswith(("6", "8")) and not receipt_cr_acc:
            receipt_cr_acc = account_resolver.resolve(bare, company) or raw_acc

    if is_receipt:
        for wh, amt in in_by_wh.items():
            if amt <= 0: continue
            inv_acc = _warehouse_account(wh, stock_adjustment_account)
            gl_rows.append(_gl_row(inv_acc, amt, 0, f"Receipt → {wh}"))
            if receipt_cr_acc:
                # Return-to-inventory pattern: Cr 6xxx not Cr 331
                gl_rows.append(_gl_row(receipt_cr_acc, 0, amt, f"Receipt ← (return) Cr {_bare(receipt_cr_acc)}"))
            elif pn_party_account:
                gl_row = _gl_row(pn_party_account, 0, amt, f"Receipt ← {wh} Cr 331")
                gl_row["party_type"] = "Supplier"
                gl_row["party"] = pn_supplier
                gl_rows.append(gl_row)
            else:
                gl_rows.append(_gl_row(stock_adjustment_account, 0, amt, f"Receipt ← {wh}"))
    elif is_issue:
        # Route Dr to actual NKC 6xxx contra (e.g. 6321/6322/6323/6427)
        # instead of generic stock_adjustment_account (TK 632 root).
        dr_acc = issue_dr_acc or stock_adjustment_account
        for wh, amt in out_by_wh.items():
            if amt <= 0: continue
            inv_acc = _warehouse_account(wh, stock_adjustment_account)
            gl_rows.append(_gl_row(dr_acc, amt, 0, f"Issue ← {wh} Dr {_bare(dr_acc)}"))
            gl_rows.append(_gl_row(inv_acc, 0, amt, f"Issue → {wh}"))
    elif is_transfer:
        for (s_wh, t_wh), amt in transfer_pairs.items():
            if amt <= 0: continue
            s_acc = _warehouse_account(s_wh, stock_adjustment_account)
            t_acc = _warehouse_account(t_wh, stock_adjustment_account)
            if s_acc == t_acc:
                continue  # same inventory TK both sides — no GL needed
            gl_rows.append(_gl_row(t_acc, amt, 0, f"Transfer Dr {t_wh}"))
            gl_rows.append(_gl_row(s_acc, 0, amt, f"Transfer Cr {s_wh}"))

    # VAT supplement for PN/PNHN: source NKC carries Dr 1331 / Cr 331 alongside
    # the stock Dr 156x / Cr 331. SE doesn't have a tax field, so SCT-driven
    # build never sees the VAT split. Mirror it directly: for each Dr 1331 leg
    # in voucher.legs, emit Dr 1331 / Cr <party_account or stock_adjustment>.
    # Without this, TK 1331 is short ~95M Dr (109 PN vouchers in DCNET T1/2026).
    if is_receipt:
        legs = voucher.get("legs") or []
        for leg in legs:
            raw_acc = leg.get("account_resolved") or leg.get("account") or ""
            bare = raw_acc if " - " not in raw_acc else raw_acc.split(" - ", 1)[0]
            vat_amt = float(leg.get("debit") or 0)
            if bare == "1331" and vat_amt > 0:
                vat_acc = account_resolver.resolve("1331", company) or raw_acc
                gl_rows.append(_gl_row(vat_acc, vat_amt, 0, "VAT input Dr 1331"))
                cr_acc = pn_party_account or stock_adjustment_account
                cr_row = _gl_row(cr_acc, 0, vat_amt, "VAT input Cr 331")
                if pn_party_account:
                    cr_row["party_type"] = "Supplier"
                    cr_row["party"] = pn_supplier
                gl_rows.append(cr_row)

    return {
        "Stock Entry": [se_row],
        "Stock Entry Detail": details_rows,
        "Stock Ledger Entry": sle_rows,
        "GL Entry": gl_rows,
    }
