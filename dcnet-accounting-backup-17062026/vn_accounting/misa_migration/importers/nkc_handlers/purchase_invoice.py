"""MDV (Mua dịch vụ) and MH (Mua hàng CCDC) → Purchase Invoice handler.

Phase D commit 5. Consumes NKC voucher + bảng kê MV invoice and creates
ERPNext Purchase Invoice with:
  - doc.name = Misa Số chứng từ (e.g. 'MDV20260001', 'MH20260001')
  - supplier = Misa Mã NCC (Phase 3 master must exist)
  - items[]: one row per bảng kê line, expense_account extracted from
    NKC's Dr 6XX / Dr 242 / Dr 152-153-156 / Dr 211-213 legs in order
    (any Dr leg that's not Dr 1331 input VAT)
  - taxes[]: one row per VAT rate group (Cr "Tài khoản thuế" pattern is
    input VAT → bookings hit Dr 1331 — different side from SI). Built
    via shared vat_extractor.build_tax_rows().
  - bill_no / bill_date / supplier_name set from bảng kê metadata

PN (Phiếu nhập kho) requires update_stock=1 + Purchase Receipt sibling;
that handler is in purchase_receipt.py (commit 11). MDV/MH are pure
non-stock invoices.
"""

from __future__ import annotations

import json
from typing import Any

import frappe


from vn_accounting.misa_migration.context import (
    get_active_company as _get_company,
)
from vn_accounting.misa_migration.importers import vat_extractor
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    PLACEHOLDER_ITEM_CODE,
    _ensure_placeholder_item,
)

# Misa TK prefixes that may appear as Dr legs in a PI's NKC voucher.
# Includes expense (6XX), prepaid/deferred (242), inventory (152/153/156),
# CCDC (153), fixed asset (211/213), and reimbursable advances.
_PI_EXPENSE_DR_PREFIXES = (
    "152", "153", "156", "157", "158",          # Inventory + CCDC
    "211", "213", "217",                          # Fixed assets
    "242",                                        # Prepaid / deferred expense
    "335", "338",                                 # Accrued / payable misc
    "62", "63", "64", "641", "642", "6421",      # Expenses (broad)
    "627",                                        # Manufacturing overhead
    "811",                                        # Other expenses
    "141",                                        # Employee advances
)
_PI_INPUT_VAT_PREFIXES = ("1331", "13311", "13312")
_PI_PAYABLE_PREFIXES = ("331",)


def extract_line_expense_accounts(
    voucher_legs: list[dict[str, Any]],
    n_line_items: int,
) -> list[str | None]:
    """Extract one Misa TK (expense/asset) per bảng kê line in source order.

    Rule: collect every Dr leg whose account is NOT input VAT (1331). Take
    the first N (where N = n_line_items). Pad with None if NKC is short
    — caller MUST substitute a sensible fallback (Company default expense
    account) before passing to ERPNext, otherwise ERPNext's
    set_missing_values may copy credit_to into the empty slot.

    NOTE: per-line attribution is a heuristic. Misa NKC emits 1 Dr leg
    per UNIQUE expense account (not per line item), so when N>K (more
    bảng kê lines than NKC Dr legs) the slot→line mapping is genuinely
    ambiguous. None-padding preserves that uncertainty; caller decides
    the fallback.

    Real MDV NKC patterns:
      MDV20260001 (2 legs, no VAT): Dr 6322 / Cr 331 → ['6322']
      MDV20260003 (4 legs, 1 line): Dr 6427 / Cr 331 / Dr 1331 / Cr 331 → ['6427']
      MDV20260301 (8 legs, 2 lines mixed): Dr 6323 / Cr 331 / Dr 1331 / Cr 331 /
                  Dr 242 / Cr 331 / Dr 1331 / Cr 331 → ['6323', '242']
    """
    dr_expense: list[str] = []
    for leg in voucher_legs:
        acct = (leg.get("account") or "").strip()
        debit = leg.get("debit") or 0.0
        if debit <= 0 or not acct:
            continue
        if any(acct.startswith(p) for p in _PI_INPUT_VAT_PREFIXES):
            continue
        dr_expense.append(acct)
    # Pad / truncate to n_line_items
    if len(dr_expense) < n_line_items:
        dr_expense = dr_expense + [None] * (n_line_items - len(dr_expense))
    return dr_expense[:n_line_items]


def _load_account_mapping() -> dict[str, str]:
    try:
        doc = frappe.get_single("Misa Account Mapping")
        return json.loads(doc.mappings or "{}")
    except Exception:
        return {}


def _resolve_account(misa_tk: str | None, mapping: dict[str, str],
                     company: str | None) -> str | None:
    if not misa_tk:
        return None
    misa_tk = str(misa_tk).strip()
    if not misa_tk:
        return None
    # PERF: shared cache (warmed once at orchestrator start)
    from vn_accounting.misa_migration.importers.nkc_handlers.payment_entry import (
        _is_group_cached, _ACCOUNT_BY_NUMBER_CACHE,
    )
    cached = mapping.get(misa_tk)
    if cached and _is_group_cached(cached) == 0:
        return cached
    if company:
        key = (misa_tk, company)
        cached_leaf = _ACCOUNT_BY_NUMBER_CACHE.get(key)
        if cached_leaf:
            mapping[misa_tk] = cached_leaf
            return cached_leaf
        live = frappe.db.get_value(
            "Account",
            {"account_number": misa_tk, "company": company, "is_group": 0},
            "name",
        )
        if live:
            mapping[misa_tk] = live
            _ACCOUNT_BY_NUMBER_CACHE[key] = live
            return live
    return None


def _create_pi(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None,
    voucher_no: str,
    prefix: str,
) -> dict[str, Any]:
    """Shared PI creation logic for MDV + MH. PN has its own handler with PR."""
    if frappe.db.exists("Purchase Invoice", voucher_no):
        return {"status": "skipped", "target_name": voucher_no,
                "error": None, "reason": "already_exists"}

    party_code = voucher.get("party_code") or ""
    if not party_code:
        return {"status": "failed",
                "error": f"voucher {voucher_no} missing party_code"}
    # PERF (Tier 1.5): set-lookup vs per-call DB round-trip
    from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache
    if not _party_cache.is_supplier(party_code):
        return {"status": "failed",
                "error": f"Supplier {party_code!r} not found — run Phase 3 first"}

    company = _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    mapping = _load_account_mapping()

    # Bảng kê line items — synthesize a single line if none (no-VAT foreign
    # service vendors sometimes appear in NKC only).
    line_items: list[dict[str, Any]] = []
    if invoice and invoice.get("line_items"):
        line_items = list(invoice["line_items"])
    else:
        # Synthesize 1 line from NKC totals
        total_dr_expense = 0.0
        for leg in (voucher.get("legs") or []):
            acct = (leg.get("account") or "").strip()
            debit = leg.get("debit") or 0.0
            if debit > 0 and not any(acct.startswith(p) for p in _PI_INPUT_VAT_PREFIXES):
                total_dr_expense += debit
        line_items = [{
            "item_name": voucher.get("voucher_remark") or voucher_no,
            "description": voucher.get("voucher_remark") or voucher_no,
            "uom": "Nos",
            "qty": 1.0,
            "rate": total_dr_expense,
            "net_amount": total_dr_expense,
            "tax_rate": 0.0,
            "tax_amount": 0.0,
            "tax_account": None,
        }]

    # Per-line expense accounts from NKC
    per_line_tk = extract_line_expense_accounts(
        voucher.get("legs") or [], len(line_items)
    )
    per_line_expense_acct: list[str | None] = [
        _resolve_account(tk, mapping, company) for tk in per_line_tk
    ]
    # Fill remaining empty slots with Company.default_expense_account.
    # Critical: leaving row.expense_account empty triggers ERPNext's
    # set_missing_values fallback, which on PI ends up copying credit_to
    # (TK 331 payable) into expense_account → ValidationError "Expense =
    # Credit To". Falling back to the Company default expense account
    # (typically 6321 - Giá vốn hàng bán) keeps GL sensible. Per-line
    # attribution is genuinely ambiguous when bảng kê has more lines
    # than NKC has Dr legs — Misa emits 1 Dr leg per UNIQUE expense
    # account, not per line.
    if any(a is None for a in per_line_expense_acct):
        co_default_expense = frappe.db.get_value(
            "Company", company, "default_expense_account"
        )
        if co_default_expense:
            per_line_expense_acct = [
                a if a else co_default_expense for a in per_line_expense_acct
            ]

    # Input VAT account
    vat_tk = vat_extractor.extract_vat_account(
        voucher.get("legs") or [], side="input"
    )
    vat_account = _resolve_account(vat_tk, mapping, company) if vat_tk else None

    placeholder_item = _ensure_placeholder_item(company)
    from vn_accounting.misa_migration.importers.nkc_handlers import _item_cache

    items_payload: list[dict[str, Any]] = []
    line_is_return_flags: list[bool] = []
    for idx, li in enumerate(line_items):
        qty = float(li.get("qty") or 0.0)
        rate = float(li.get("rate") or 0.0)
        net_amount = float(li.get("net_amount") or 0.0)
        if qty == 0:
            qty = 1.0
            rate = net_amount
        # Detect return / credit-note line BEFORE normalising qty.
        # Misa source can encode credit notes either as qty<0 OR
        # net_amount<0 OR rate<0; ERPNext expects is_return=1 with
        # qty<0 and rate>0.
        line_amount = qty * rate
        is_return_line = (line_amount < 0) or (net_amount < 0)
        line_is_return_flags.append(is_return_line)
        if is_return_line:
            qty = -abs(qty) if qty != 0 else -1.0
            rate = abs(rate)
        elif qty < 0:
            # qty<0 but amount>=0 (shouldn't happen in practice) — flip
            qty = abs(qty)
        uom = li.get("uom") or "Nos"
        if not frappe.db.exists("UOM", uom):
            uom = "Nos" if frappe.db.exists("UOM", "Nos") else "Unit"
        # Fractional qty + placeholder Item (stock_uom='Nos' must_be_whole=1)
        # always fails ERPNext validation because the SI/PI overrides the
        # row UOM to match the Item's stock_uom regardless of li.uom.
        # Unconditionally collapse fractional qty to qty=±1 + rate*=qty:
        # the financial total stays exact; only "qty × rate" decomposition
        # is lossy (acceptable for placeholder Item where qty isn't tracked).
        if qty != int(qty):
            rate = qty * rate
            qty = -1.0 if is_return_line else 1.0
            # For return lines we need positive rate again after the
            # qty * rate collapse; preserve overall sign via qty only.
            if is_return_line and rate < 0:
                rate = abs(rate)
        raw_name = li.get("item_name") or li.get("description") or placeholder_item
        # Real Item match by name. require_non_stock=True because PI MDV/MH
        # runs update_stock=0; if a stock Item matches, ERPNext's PI controller
        # forces expense_account=Company.stock_received_but_not_billed (= 331
        # on VN small-template) → conflicts with credit_to=331 → fail.
        # Stock items stay on the placeholder Item path; the line description
        # still carries the verbatim Misa "Mặt hàng" text for reporting.
        matched_code = _item_cache.match_item_code(
            li.get("item_name"), require_non_stock=True
        )
        item_code_used = matched_code or placeholder_item
        row = {
            "item_code": item_code_used,
            "item_name": str(raw_name)[:140],  # ERPNext Item Name 140-char cap
            "description": li.get("description") or li.get("item_name") or "",
            "qty": qty,
            "uom": uom,
            "stock_uom": uom,
            "conversion_factor": 1,
            "rate": rate,
        }
        if per_line_expense_acct[idx]:
            row["expense_account"] = per_line_expense_acct[idx]
        items_payload.append(row)

    is_return = any(line_is_return_flags)

    taxes_payload = vat_extractor.build_tax_rows(line_items, vat_account)

    posting_date = voucher.get("posting_date") or (
        invoice.get("posting_date") if invoice else None
    )
    bill_no = (invoice or {}).get("invoice_no") or voucher.get("invoice_no")
    bill_date = (invoice or {}).get("invoice_date") or voucher.get("invoice_date")
    supplier_name = (invoice or {}).get("party_name") or voucher.get("party_name")

    # FIX (UNC PE consistency): derive credit_to from the voucher's Cr 331-like
    # leg, NOT from the Supplier master default. When a supplier is also paid
    # via salary (TK 3341), the master default may be 3341 — but the actual PI
    # leg is Cr 331. UNC PE referencing this PI would then fail with
    # "Purchase Invoice X is associated with 331, but Party Account is 3341".
    credit_to = None
    for leg in (voucher.get("legs") or []):
        acct_no = (leg.get("account") or "").strip()
        credit = float(leg.get("credit") or 0.0)
        if credit > 0 and any(acct_no.startswith(p) for p in _PI_PAYABLE_PREFIXES):
            credit_to = _resolve_account(acct_no, mapping, company)
            if credit_to:
                break

    payload = {
        "doctype": "Purchase Invoice",
        "supplier": party_code,
        "supplier_name": supplier_name,
        "company": company,
        "posting_date": posting_date,
        "set_posting_time": 1,
        "bill_no": bill_no,
        "bill_date": bill_date,
        "remarks": voucher.get("voucher_remark") or voucher_no,
        "items": items_payload,
        "taxes": taxes_payload,
        "update_stock": 0,
        "misa_voucher_no": voucher_no,
    }
    if credit_to:
        payload["credit_to"] = credit_to
    if is_return:
        # Credit-note / refund — ERPNext requires this flag whenever any
        # line carries negative amount, otherwise PI validate() rejects
        # with "Grand Total must be >= 0".
        payload["is_return"] = 1

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight already validated Supplier / Account
        # links; skip ERPNext's per-row Link integrity check.
        doc.flags.ignore_links = True
        doc.insert(set_name=voucher_no)
        return {"status": "created", "target_name": doc.name,
                "target_doctype": "Purchase Invoice",
                "vat_account": vat_account,
                "line_count": len(items_payload),
                "tax_rows": len(taxes_payload),
                "prefix_handled": prefix}
    except Exception as exc:
        import traceback
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(
            title=f"Misa PI create failed: {voucher_no}",
            message=f"{err}\n\nVoucher legs: {len(voucher.get('legs') or [])}\n\n"
                    f"{traceback.format_exc()}",
        )
        return {"status": "failed", "target_name": None, "error": err}


# ----------------------------------------------------------- public entry points

def create_pi_from_mdv(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """MDV (Mua dịch vụ) → Purchase Invoice."""
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}
    return _create_pi(voucher, invoice, voucher_no, "MDV")


def create_pi_from_mh(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """MH (Mua hàng CCDC) → Purchase Invoice."""
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}
    return _create_pi(voucher, invoice, voucher_no, "MH")
