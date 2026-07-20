"""Validate a Misa import by comparing live DB closing balance vs source.

Two checks per scoped batch:

  1. Account balance — compare ``GL Entry`` net DR-CR per Account against
     the ``Cuối kỳ Nợ / Cuối kỳ Có`` columns from ``Bang_can_doi_tai_khoan``.
  2. Inventory — compare ``Bin.actual_qty`` and ``Bin.stock_value`` per
     (warehouse, item) against the ``Cuối kỳ Số lượng / Giá trị`` columns
     from ``Tong_hop_ton_kho``.

Tolerance defaults: 1 VND for currency, 0.01 for qty.

Public entry: ``validate_closing_balance(batch_name, period_end,
source_dir=None)`` — also whitelisted.
"""
from __future__ import annotations

import datetime
import os
from decimal import Decimal
from typing import Any

import frappe
from openpyxl import load_workbook


CURRENCY_TOLERANCE = 1.0  # VND
QTY_TOLERANCE = 0.01


def _decimal(v) -> Decimal:
    if v is None or v == "":
        return Decimal(0)
    try:
        return Decimal(str(v))
    except Exception:
        return Decimal(0)


def _find_source_file(source_dir: str, pattern: str) -> str | None:
    """Find first .xlsx in dir whose name contains all words in pattern."""
    if not os.path.isdir(source_dir):
        return None
    words = pattern.lower().split()
    for fn in sorted(os.listdir(source_dir)):
        if not fn.lower().endswith(".xlsx"):
            continue
        nm = fn.lower()
        if all(w in nm for w in words):
            return os.path.join(source_dir, fn)
    return None


def _validate_accounts(source_path: str, company: str, period_end: datetime.date) -> dict[str, Any]:
    wb = load_workbook(source_path, read_only=True, data_only=True)
    ws = wb.active

    # Bang_can_doi layout:
    # Row 8: Số TK | Tên TK | Đầu kỳ Nợ | Đầu kỳ Có | PS Nợ | PS Có | Cuối kỳ Nợ | Cuối kỳ Có
    # Data starts row 10
    source: dict[str, tuple[Decimal, Decimal, str]] = {}
    for row in ws.iter_rows(min_row=10, values_only=True):
        tk = str(row[0] or "").strip()
        if not tk or not tk[0].isdigit():
            continue
        cb_dr = _decimal(row[6])
        cb_cr = _decimal(row[7])
        source[tk] = (cb_dr, cb_cr, str(row[1] or "").strip())

    matches = mismatches = missing = 0
    out_rows: list[dict] = []
    for tk, (src_dr, src_cr, name) in sorted(source.items()):
        account_name = frappe.db.get_value(
            "Account", {"account_number": tk, "company": company}, "name",
        )
        if not account_name:
            missing += 1
            out_rows.append({
                "tk": tk, "name": name, "status": "MISSING_DB",
                "src_dr": float(src_dr), "src_cr": float(src_cr),
                "act_dr": 0, "act_cr": 0, "diff": 0,
            })
            continue

        is_group = frappe.db.get_value("Account", account_name, "is_group")
        if is_group:
            balance = frappe.db.sql(
                """
                SELECT COALESCE(SUM(gl.debit - gl.credit), 0)
                FROM `tabGL Entry` gl
                JOIN `tabAccount` a ON a.name = gl.account
                WHERE gl.company = %s AND gl.is_cancelled = 0
                  AND gl.posting_date <= %s
                  AND a.lft >= (SELECT lft FROM `tabAccount` WHERE name = %s)
                  AND a.rgt <= (SELECT rgt FROM `tabAccount` WHERE name = %s)
                """,
                (company, period_end, account_name, account_name),
            )[0][0]
        else:
            balance = frappe.db.sql(
                """
                SELECT COALESCE(SUM(debit - credit), 0)
                FROM `tabGL Entry`
                WHERE company = %s AND account = %s AND is_cancelled = 0
                  AND posting_date <= %s
                """,
                (company, account_name, period_end),
            )[0][0]
        balance = float(balance or 0)
        src_net = float(src_dr - src_cr)
        diff = balance - src_net
        if abs(diff) <= CURRENCY_TOLERANCE:
            matches += 1
            status = "OK"
        else:
            mismatches += 1
            status = "MISMATCH"
        out_rows.append({
            "tk": tk, "name": name, "status": status,
            "src_dr": float(src_dr), "src_cr": float(src_cr),
            "act_dr": max(balance, 0), "act_cr": max(-balance, 0),
            "diff": diff,
        })

    return {
        "source_file": os.path.basename(source_path),
        "total_tks": len(source),
        "matches": matches,
        "mismatches": mismatches,
        "missing_in_db": missing,
        "accuracy_pct": round(matches / len(source) * 100, 2) if source else 0,
        "mismatches_detail": sorted(
            [r for r in out_rows if r["status"] == "MISMATCH"],
            key=lambda x: -abs(x["diff"]),
        )[:50],
        "missing_detail": [r for r in out_rows if r["status"] == "MISSING_DB"],
    }


def _validate_inventory(source_path: str, company: str) -> dict[str, Any]:
    wb = load_workbook(source_path, read_only=True, data_only=True)
    ws = wb.active

    # Tong_hop_ton_kho layout (variable column count). Find Cuối kỳ idx
    # by scanning main header (row 4) for the literal "Cuối kỳ".
    rows_iter = list(ws.iter_rows(values_only=True))
    main_header = rows_iter[3] if len(rows_iter) > 3 else []
    ck_start = None
    for idx, val in enumerate(main_header):
        if val and "Cuối kỳ" in str(val):
            ck_start = idx
            break
    if ck_start is None:
        # Fallback: assume Cuối kỳ is at column 52, 53, 54 (0-indexed)
        ck_start = 51

    ck_qty_idx = ck_start
    ck_dvc_idx = ck_start + 1
    ck_value_idx = ck_start + 2

    # Source: (warehouse_db_name, item_code) → (qty, value, wh_human_name)
    abbr = frappe.db.get_value("Company", company, "abbr") or ""
    source: dict[tuple, tuple] = {}
    for row in rows_iter[5:]:
        if not row or len(row) < ck_value_idx + 1:
            continue
        wh_name = str(row[0] or "").strip()
        wh_code = str(row[1] or "").strip()
        item_code = str(row[2] or "").strip()
        if not wh_name or not item_code:
            continue
        item_code_sanitized = (
            item_code.replace("<", "-").replace(">", "-")
            if ("<" in item_code or ">" in item_code) else item_code
        )
        cb_qty = _decimal(row[ck_qty_idx])
        cb_value = _decimal(row[ck_value_idx])
        # Warehouse name variants: importer creates "{name} - {abbr}",
        # derive_masters creates "{code} - {name} - {abbr}". Try both,
        # then fuzzy-match by warehouse_name.
        candidates = []
        if abbr:
            if wh_code:
                candidates.append(f"{wh_code} - {wh_name} - {abbr}")
            candidates.append(f"{wh_name} - {abbr}")
            if wh_code:
                candidates.append(f"{wh_code} - {abbr}")
        else:
            candidates.append(wh_name)
        db_wh = next(
            (c for c in candidates if frappe.db.exists("Warehouse", c)), None,
        )
        if not db_wh:
            db_wh = frappe.db.get_value(
                "Warehouse",
                {"company": company, "is_group": 0,
                 "warehouse_name": ["like", f"%{wh_name}%"]},
                "name",
            )
        source[(db_wh, item_code_sanitized)] = (cb_qty, cb_value, wh_name)

    matches = mm_qty = mm_value = missing_bin = no_db_wh = 0
    out_rows: list[dict] = []
    for (db_wh, item_code), (src_qty, src_value, wh_name) in source.items():
        if not db_wh:
            no_db_wh += 1
            continue
        bin_row = frappe.db.sql(
            "SELECT actual_qty, stock_value FROM `tabBin` WHERE warehouse=%s AND item_code=%s",
            (db_wh, item_code), as_dict=True,
        )
        if not bin_row:
            missing_bin += 1
            out_rows.append({
                "warehouse": wh_name, "item_code": item_code,
                "status": "NO_BIN",
                "src_qty": float(src_qty), "src_value": float(src_value),
                "act_qty": 0, "act_value": 0,
                "diff_qty": -float(src_qty), "diff_value": -float(src_value),
            })
            continue
        b = bin_row[0]
        act_qty = float(b["actual_qty"] or 0)
        act_value = float(b["stock_value"] or 0)
        diff_qty = act_qty - float(src_qty)
        diff_value = act_value - float(src_value)
        qty_ok = abs(diff_qty) <= QTY_TOLERANCE
        value_ok = abs(diff_value) <= CURRENCY_TOLERANCE
        if qty_ok and value_ok:
            matches += 1
            status = "OK"
        elif not qty_ok and value_ok:
            mm_qty += 1; status = "QTY_MISMATCH"
        elif qty_ok and not value_ok:
            mm_value += 1; status = "VALUE_MISMATCH"
        else:
            mm_qty += 1; mm_value += 1
            status = "BOTH_MISMATCH"
        out_rows.append({
            "warehouse": wh_name, "item_code": item_code,
            "status": status,
            "src_qty": float(src_qty), "src_value": float(src_value),
            "act_qty": act_qty, "act_value": act_value,
            "diff_qty": diff_qty, "diff_value": diff_value,
        })

    return {
        "source_file": os.path.basename(source_path),
        "total_pairs": len(source),
        "matches": matches,
        "qty_mismatches": mm_qty,
        "value_mismatches": mm_value,
        "missing_bin": missing_bin,
        "no_db_warehouse": no_db_wh,
        "accuracy_pct": round(matches / len(source) * 100, 2) if source else 0,
        "mismatches_detail": sorted(
            [r for r in out_rows if r["status"] != "OK"],
            key=lambda x: -abs(x["diff_value"]),
        )[:50],
    }


@frappe.whitelist()
def validate_closing_balance(
    batch_name: str,
    period_end: str,
    source_dir: str | None = None,
) -> dict[str, Any]:
    """Compare live DB closing balance vs source files.

    Args:
      batch_name: Misa Migration Batch (used to resolve company).
      period_end: ISO date string ``YYYY-MM-DD``. Source files cover the
                  period ending this date.
      source_dir: Folder containing source xlsx files. Defaults to
                  ``<bench>/docs/to_migrate/<period_end YYYY-M>``.

    Returns:
      {
        "company": str, "period_end": str,
        "accounts": { ... },
        "inventory": { ... },
      }
    """
    if not batch_name:
        frappe.throw(frappe._("Phải chọn batch."))
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(frappe._("Batch không có Company."))
    pe = datetime.date.fromisoformat(period_end)

    if not source_dir:
        # Default convention: <bench>/docs/to_migrate/<month>-<year>/
        bench_root = frappe.utils.get_bench_path() if hasattr(frappe.utils, "get_bench_path") else "/home/long/long/frappe-bench-dcnet"
        candidate = os.path.join(bench_root, "docs", "to_migrate", f"{pe.month}-{pe.year}")
        if os.path.isdir(candidate):
            source_dir = candidate
        else:
            frappe.throw(frappe._("source_dir not specified and default not found: {0}").format(candidate))

    out: dict[str, Any] = {
        "batch": batch_name,
        "company": company,
        "period_end": period_end,
        "source_dir": source_dir,
    }

    acct_path = _find_source_file(source_dir, "can doi tai khoan") or \
                _find_source_file(source_dir, "bang can doi")
    inv_path = _find_source_file(source_dir, "tong hop ton kho")

    if acct_path:
        out["accounts"] = _validate_accounts(acct_path, company, pe)
    else:
        out["accounts"] = {"error": "No 'Bang can doi tai khoan' file found in source_dir"}

    if inv_path:
        out["inventory"] = _validate_inventory(inv_path, company)
    else:
        out["inventory"] = {"error": "No 'Tong hop ton kho' file found in source_dir"}

    return out


@frappe.whitelist()
def list_stock_entries_needing_review(
    company: str,
    batch_name: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """List Stock Entries with suspicious or missing accounting entries.

    Categories an accountant should investigate:

      1. ``no_gl`` — SE moved stock but produced ZERO GL Entry. Either
         intentional (internal transfer same-warehouse-account) or a
         data gap (source NKC missing the double-entry).
      2. ``orphan_no_nkc`` — SE exists but no NKC source rows found.
         Means SE was auto-created (perhaps from SCT alone) without an
         accounting voucher.
      3. ``gl_to_stock_adj_only`` — SE Cr leg posts to
         ``stock_adjustment_account`` (TK 632 by default) instead of the
         payable (TK 331). Means the PN-repost helper hasn't been run,
         or NKC doesn't reveal a payable counter-party (e.g. internal
         consumption SE that should NOT post to 331).

    Returns a categorised list the accountant can paste into a Misa
    review session: ``[{voucher_no, posting_date, total_amount,
    category, hint}]``.
    """
    if not company:
        frappe.throw(frappe._("Phải chọn Company."))
    if not batch_name:
        batch_name = frappe.db.get_value(
            "Misa Migration Batch", {"company": company},
            "name", order_by="creation desc",
        )

    out: dict[str, list[dict]] = {
        "no_gl": [],
        "orphan_no_nkc": [],
        "gl_to_stock_adj_only": [],
    }

    co_doc = frappe.get_doc("Company", company)
    stock_adj = co_doc.stock_adjustment_account

    # Get all SEs for this company
    se_rows = frappe.db.sql(
        "SELECT name, posting_date, total_amount FROM `tabStock Entry` WHERE company=%s",
        (company,), as_dict=True,
    )

    for se in se_rows:
        vno = se["name"]
        # GL count for this SE
        n_gl = frappe.db.sql(
            "SELECT COUNT(*) FROM `tabGL Entry` WHERE voucher_type='Stock Entry' AND voucher_no=%s AND is_cancelled=0",
            (vno,),
        )[0][0]
        # NKC rows for this voucher_no
        n_nkc = 0
        if batch_name:
            n_nkc = frappe.db.sql(
                """SELECT COUNT(*) FROM `tabMisa Migration Row`
                   WHERE batch=%s AND file_type='NKC'
                   AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))=%s""",
                (batch_name, vno),
            )[0][0]

        if n_gl == 0:
            out["no_gl"].append({
                "voucher_no": vno,
                "posting_date": str(se["posting_date"]),
                "total_amount": float(se["total_amount"] or 0),
                "hint": "SE recorded stock movement but no accounting GL. "
                        "Confirm with accountant: was this internal/no-money "
                        "transfer, or is the source NKC missing the JE?",
            })
        elif n_nkc == 0:
            out["orphan_no_nkc"].append({
                "voucher_no": vno,
                "posting_date": str(se["posting_date"]),
                "total_amount": float(se["total_amount"] or 0),
                "hint": "SE exists but no NKC source — auto-created from SCT? "
                        "Verify by asking accountant about voucher origin.",
            })
        elif stock_adj:
            # Check if SE GL only goes to stock_adjustment (potential payable bug)
            n_stock_adj = frappe.db.sql(
                """SELECT COUNT(*) FROM `tabGL Entry`
                   WHERE voucher_type='Stock Entry' AND voucher_no=%s
                   AND account=%s AND credit > 0 AND is_cancelled=0""",
                (vno, stock_adj),
            )[0][0]
            n_payable = frappe.db.sql(
                """SELECT COUNT(*) FROM `tabGL Entry` gl
                   JOIN `tabAccount` a ON a.name=gl.account
                   WHERE gl.voucher_type='Stock Entry' AND gl.voucher_no=%s
                   AND (a.account_number LIKE '331%%' OR a.account_number LIKE '338%%')
                   AND gl.credit > 0 AND gl.is_cancelled=0""",
                (vno,),
            )[0][0]
            if n_stock_adj > 0 and n_payable == 0:
                out["gl_to_stock_adj_only"].append({
                    "voucher_no": vno,
                    "posting_date": str(se["posting_date"]),
                    "total_amount": float(se["total_amount"] or 0),
                    "hint": f"SE Cr posts to stock_adjustment ({stock_adj}). "
                            "If voucher_no matches a Misa purchase (PN/PNHN/MH "
                            "with 331 in NKC), run repost_pn_stock_to_payable. "
                            "Otherwise confirm with accountant.",
                })

    return {
        "company": company,
        "batch_name": batch_name,
        "total_se_count": len(se_rows),
        "summary": {k: len(v) for k, v in out.items()},
        "details": {k: v[:limit] for k, v in out.items()},
    }


@frappe.whitelist()
def print_validation_report(batch_name: str, period_end: str, source_dir: str | None = None) -> str:
    """Same as validate_closing_balance() but returns a formatted text report."""
    r = validate_closing_balance(batch_name, period_end, source_dir)
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append(f"CLOSING BALANCE VALIDATION — {r['company']} — period end {r['period_end']}")
    lines.append("=" * 100)

    # Accounts
    a = r.get("accounts", {})
    lines.append("\n--- PART 1: ACCOUNT BALANCE ---")
    if "error" in a:
        lines.append(f"  {a['error']}")
    else:
        lines.append(f"  Source: {a['source_file']}")
        lines.append(f"  Total TKs: {a['total_tks']}")
        lines.append(f"  ✓ Matches: {a['matches']} ({a['accuracy_pct']}%)")
        lines.append(f"  ✗ Mismatches: {a['mismatches']}")
        lines.append(f"  - Missing in DB: {a['missing_in_db']}")
        if a.get("mismatches_detail"):
            lines.append(f"  Top {len(a['mismatches_detail'])} mismatches (by abs diff):")
            lines.append(f"    {'TK':<10s} {'src_dr':>16s} {'src_cr':>16s} {'act_dr':>16s} {'act_cr':>16s} {'diff':>16s}  Name")
            for m in a["mismatches_detail"][:20]:
                lines.append(
                    f"    {m['tk']:<10s} {m['src_dr']:>16,.0f} {m['src_cr']:>16,.0f} "
                    f"{m['act_dr']:>16,.0f} {m['act_cr']:>16,.0f} {m['diff']:>+16,.0f}  {m['name'][:40]}"
                )

    # Inventory
    inv = r.get("inventory", {})
    lines.append("\n--- PART 2: INVENTORY ---")
    if "error" in inv:
        lines.append(f"  {inv['error']}")
    else:
        lines.append(f"  Source: {inv['source_file']}")
        lines.append(f"  Total (warehouse, item) pairs: {inv['total_pairs']}")
        lines.append(f"  ✓ Matches: {inv['matches']} ({inv['accuracy_pct']}%)")
        lines.append(f"  ✗ Qty mismatches: {inv['qty_mismatches']}")
        lines.append(f"  ✗ Value mismatches: {inv['value_mismatches']}")
        lines.append(f"  - Missing Bin: {inv['missing_bin']}")
        lines.append(f"  - No DB Warehouse: {inv['no_db_warehouse']}")
        if inv.get("mismatches_detail"):
            lines.append(f"  Top {len(inv['mismatches_detail'])} mismatches (by abs diff_value):")
            for m in inv["mismatches_detail"][:20]:
                lines.append(
                    f"    {m['warehouse'][:14]:<15s} {m['item_code'][:30]:<30s} {m['status']:<14s} "
                    f"src_qty={m['src_qty']:>10,.2f} src_val={m['src_value']:>13,.0f} "
                    f"act_qty={m['act_qty']:>10,.2f} act_val={m['act_value']:>13,.0f} "
                    f"diff_val={m['diff_value']:>+12,.0f}"
                )

    return "\n".join(lines)
