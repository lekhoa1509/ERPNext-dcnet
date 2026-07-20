"""Purchase Invoice bulk-pump builder.

Mirror of sales_invoice.py with:
  - debit_to → credit_to (Cr Supplier, TK 331)
  - party_type=Supplier
  - bill_no/bill_date ARE valid fields on PI
  - GL: Dr Expense / Cr Supplier (party_type=Supplier)
"""
from __future__ import annotations

import secrets
from typing import Any

import frappe
from frappe.utils import getdate

from vn_accounting.misa_migration.importers._naming import migrated_doc_name
from vn_accounting.misa_migration.importers.nkc_handlers.purchase_invoice import (
    _load_account_mapping,
)
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    _resolve_account, _group_line_items_by_tax_rate,
)
from vn_accounting.misa_migration.bulk_pump import account_resolver


def _leg_account(leg: dict, company: str) -> str | None:
    """Pull an account name off a leg, resolving bare TK → suffixed ERPNext name.
    Idempotent: pass-through if already suffixed.
    """
    raw = leg.get("account_resolved") or leg.get("account")
    if not raw:
        return None
    return account_resolver.resolve(raw, company) or raw

_ITEM_CACHE: dict[str, str | None] = {}


def _gen_name() -> str:
    return secrets.token_hex(5)


def _resolve_item_code(misa_item_name: str | None, placeholder: str) -> str:
    if not misa_item_name:
        return placeholder
    if misa_item_name in _ITEM_CACHE:
        return _ITEM_CACHE[misa_item_name] or placeholder
    code = frappe.db.get_value("Item", {"item_name": misa_item_name}, "name")
    _ITEM_CACHE[misa_item_name] = code
    return code or placeholder


def build_pi_dicts(
    voucher: dict[str, Any],
    invoice: dict[str, Any],
    company: str,
    placeholder_item: str,
    credit_to_account: str,
    default_expense_account: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    voucher_no = voucher.get("voucher_no")
    if not voucher_no:
        return None
    # Company-namespace the doc name (see sales_invoice builder note).
    voucher_no_raw = voucher_no
    voucher_no = migrated_doc_name(company, voucher_no)
    party_code = voucher.get("party_code") or ""
    if not party_code:
        return None
    # Canonicalize supplier name to the DB-stored case. MySQL collation makes
    # FK joins case-insensitive, but `frappe.qb.where(name.isin(...))` is
    # case-sensitive — a Misa export with 'VIETTEL' against a master 'Viettel'
    # silently breaks Purchase Register + AP reports.
    canonical_supplier = frappe.db.get_value("Supplier", party_code, "name")
    if canonical_supplier:
        party_code = canonical_supplier
    line_items = invoice.get("line_items") or []
    if not line_items:
        return None
    posting_date = voucher.get("posting_date") or invoice.get("posting_date")
    bill_no = invoice.get("invoice_no") or voucher.get("invoice_no")
    bill_date = invoice.get("invoice_date") or voucher.get("invoice_date")
    mapping = _load_account_mapping() if callable(globals().get('_load_account_mapping')) else {}

    # VAT input legs: TK 1331 (bare or suffixed). Match by leading TK prefix
    # before resolving so bare-TK leg shapes still match.
    def _starts_1331(leg):
        raw = (leg.get("account_resolved") or leg.get("account") or "").strip()
        return raw.startswith("1331")
    # Cost-side legs (debit > 0) EXCLUDING the VAT-input legs — they're
    # captured separately into `pi.taxes`, not as item lines. Without this
    # exclusion the builder used to map line_item[idx] → leg[idx] and
    # whichever line happened to align with the 1331 leg got
    # `expense_account = TK 1331` (input-VAT refund), mis-routing 48.9% of
    # PI item value on the DCNET TEST batch.
    expense_legs = [
        l for l in (voucher.get("legs") or [])
        if float(l.get("debit") or 0) > 0 and not _starts_1331(l)
    ]
    vat_legs = [l for l in (voucher.get("legs") or []) if _starts_1331(l)]
    vat_account = _leg_account(vat_legs[0], company) if vat_legs else None

    # Override credit_to when source NKC has a single non-331/non-VAT Cr
    # contra (e.g. small MDV with Cr 711 Other Income offset, or Cr 242
    # prepaid). Without this, PI defaults to 331 supplier → BCDTK shows
    # 331 over-credited + 711 (or other) under-credited. DCNET T1/2026
    # had 6 small MDV (MDV20260296-300/477) totaling 37,673 đồng on Cr 711.
    _credit_to_override = None
    cr_legs_non_vat = [
        l for l in (voucher.get("legs") or [])
        if float(l.get("credit") or 0) > 0 and not _starts_1331(l)
    ]
    if cr_legs_non_vat:
        _bare = lambda raw: (raw if " - " not in (raw or "") else raw.split(" - ", 1)[0]).strip()
        cr_tks = {_bare(l.get("account_resolved") or l.get("account") or "")
                  for l in cr_legs_non_vat}
        cr_tks.discard("")
        # Single non-331 contra → use it. Multi-contra is rare for PI; default.
        non_331 = [t for t in cr_tks if not t.startswith("331")]
        if len(cr_tks) == 1 and len(non_331) == 1:
            resolved = account_resolver.resolve(non_331[0], company)
            if resolved:
                _credit_to_override = resolved
    if _credit_to_override:
        credit_to_account = _credit_to_override

    now = frappe.utils.now()
    fiscal_year = posting_date[:4] if isinstance(posting_date, str) else str(getdate(posting_date).year)

    # GAP FIX: when MV invoice's line_items có amount=0 (Misa sometimes exports
    # MV with item names but blank qty/rate/net_amount), distribute the NKC
    # expense leg amounts evenly across items so expense actually posts to GL.
    # Without this, items get amount=0 → PI grand_total=0 → only VAT posts
    # → expense accounts (632x/642x) stay at 0 → P&L lệch source.
    line_items_total = sum(
        float(li.get("net_amount") or 0)
        or (float(li.get("qty") or 0) * float(li.get("rate") or 0))
        for li in line_items
    )
    # WHITELIST chỉ expense legs (TK 6xx, 8xx, 142/242 prepaid) cho fallback.
    # PR #96 dùng blacklist (skip 152-158) chỉ cover 1 loại — miss TK 211
    # (TSCD) → MH cho TSCD over-state TS 1.8B. Mọi non-expense TK (15x stock,
    # 21x TSCD, 22x đầu tư, 24x CWIP, 13x phải thu, 33x AP, 36x phải thu nội
    # bộ, etc.) cần offsetting entry riêng (SE, Asset, PE, JE) — PI tự Dr
    # những TK đó sẽ dup-count.
    def _is_safe_expense_leg(leg):
        acc = (leg.get("account_resolved") or leg.get("account") or "").strip()
        return acc.startswith(("6", "8")) or acc.startswith(("142", "242"))
    safe_expense_legs = [l for l in expense_legs if _is_safe_expense_leg(l)]
    nkc_expense_total = sum(float(l.get("debit") or 0) for l in safe_expense_legs)
    use_nkc_fallback = (
        line_items_total < 1 and nkc_expense_total > 0 and len(line_items) > 0
    )
    if use_nkc_fallback:
        if len(safe_expense_legs) == len(line_items):
            _fallback_amounts = [float(l.get("debit") or 0) for l in safe_expense_legs]
        else:
            per_line = nkc_expense_total / len(line_items)
            _fallback_amounts = [per_line] * len(line_items)
    else:
        _fallback_amounts = [None] * len(line_items)

    # Aggregate source expense legs by TK (covers multi-leg same-TK vouchers
    # like MDV20260017: 5× Dr 6322 in NKC; positional mapping leg[idx]→item[idx]
    # loses legs N+ when line_items count < expense_legs count). Two-tier:
    # per-line amount-match FIRST (1:1 leg→item by amount), greedy fallback.
    from collections import OrderedDict
    def _bare_tk(raw):
        return (raw if " - " not in (raw or "") else raw.split(" - ", 1)[0]).strip()
    # Mutable per-leg pool: [tk_bare, amount, used_flag]
    expense_legs_pool: list[list] = []
    for leg in safe_expense_legs:
        tk = _bare_tk(leg.get("account_resolved") or leg.get("account") or "")
        amt = float(leg.get("debit") or 0)
        if tk and amt > 0:
            expense_legs_pool.append([tk, amt, False])
    tk_budgets: "OrderedDict[str, float]" = OrderedDict()
    for tk, amt, _used in expense_legs_pool:
        tk_budgets[tk] = tk_budgets.get(tk, 0.0) + amt
    tk_to_account = {
        tk: account_resolver.resolve(tk, company) for tk in tk_budgets
    }

    items_rows: list[dict] = []
    net_total = 0.0
    for idx, li in enumerate(line_items):
        qty = float(li.get("qty") or 0.0)
        rate = float(li.get("rate") or 0.0)
        net_amount = float(li.get("net_amount") or 0.0)
        # Apply NKC fallback when invoice line is zero-valued
        if _fallback_amounts[idx] is not None and net_amount < 1 and rate * qty < 1:
            net_amount = _fallback_amounts[idx]
            qty = 1.0
            rate = net_amount
        if qty <= 0:
            qty = 1.0
            rate = net_amount
        elif rate == 0.0 and net_amount > 0:
            # Service-class MV register provides 'net_amount' (total per
            # line) but no 'rate' column. Derive rate from net_amount.
            # Without this fallback, the prior `if qty != int(qty)` branch
            # never fires for typical qty=1 service lines → rate stays 0
            # → PI grand_total = 0 → 331 balance silently short.
            rate = net_amount / qty
        if qty != int(qty):
            rate = qty * rate
            qty = 1.0
        amount = round(qty * rate, 2)
        uom = li.get("uom") or "Nos"
        if not frappe.db.exists("UOM", uom):
            uom = "Nos"
        raw_name = li.get("item_name") or li.get("description") or placeholder_item
        item_code_used = _resolve_item_code(li.get("item_name"), placeholder_item)
        # Resolve expense_acct: amount-match leg first, greedy fallback.
        # On fuzzy match: SNAP item amount to leg amount (NKC is authoritative
        # — MV bảng kê may have currency-floor-rounded its 'Đơn giá'/'Thành
        # tiền' below the actual GL movement). MDV20260003: NKC Dr 6427 =
        # 1,203,715, MV rate = 1,203,666 (49 đồng floor). Without snap, PI
        # short by 49 → PCV closes 49 to 4212 → BCDTK 4212 -49.
        expense_acct = default_expense_account
        matched = False
        # 1. Exact match (≤ 1 VND tolerance)
        for leg_entry in expense_legs_pool:
            if not leg_entry[2] and abs(leg_entry[1] - amount) <= 1.0:
                tk_bare = leg_entry[0]
                expense_acct = tk_to_account.get(tk_bare) or default_expense_account
                leg_entry[2] = True
                tk_budgets[tk_bare] = tk_budgets.get(tk_bare, 0) - leg_entry[1]
                matched = True
                break
        # 2. Fuzzy match (≤ 5%, min 100 VND) — snap amount to leg
        if not matched and amount > 0:
            fuzzy_tol = max(100.0, amount * 0.05)
            for leg_entry in expense_legs_pool:
                if not leg_entry[2] and abs(leg_entry[1] - amount) <= fuzzy_tol:
                    tk_bare = leg_entry[0]
                    expense_acct = tk_to_account.get(tk_bare) or default_expense_account
                    leg_entry[2] = True
                    tk_budgets[tk_bare] = tk_budgets.get(tk_bare, 0) - leg_entry[1]
                    # Snap to leg amount — preserves NKC's authoritative value
                    amount = leg_entry[1]
                    rate = amount / qty if qty else amount
                    matched = True
                    break
        # 3. Greedy fallback: largest remaining TK budget
        if not matched and tk_budgets:
            best_tk = max(tk_budgets, key=lambda k: tk_budgets[k])
            if tk_budgets[best_tk] > 0.5:
                expense_acct = tk_to_account.get(best_tk) or default_expense_account
                tk_budgets[best_tk] -= amount
                if tk_budgets[best_tk] <= 0.5 and len(tk_budgets) > 1:
                    del tk_budgets[best_tk]

        items_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "item_code": item_code_used,
            "item_name": str(raw_name)[:140],
            "description": (li.get("description") or li.get("item_name") or "")[:5000],
            "received_qty": qty, "qty": qty, "stock_qty": qty,
            "uom": uom, "stock_uom": uom, "conversion_factor": 1,
            "rate": rate, "base_rate": rate,
            "amount": amount, "base_amount": amount,
            "net_rate": rate, "base_net_rate": rate,
            "net_amount": amount, "base_net_amount": amount,
            "expense_account": expense_acct,
            "parent": voucher_no, "parenttype": "Purchase Invoice", "parentfield": "items",
        })
        net_total += amount

    # Phantom items for any remaining TK budgets — covers MDV20260017 (5
    # Dr 6322 legs, 4 line_items: 5th leg of 13.79M now posts as phantom).
    for tk, remaining in list(tk_budgets.items()):
        if remaining <= 0.5:
            continue
        phantom_acct = tk_to_account.get(tk) or default_expense_account
        items_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": len(items_rows) + 1,
            "item_code": placeholder_item,
            "item_name": f"[Misa phantom] TK {tk}",
            "description": f"NKC leg residual TK {tk} (no matching MV/BR line)",
            "received_qty": 1, "qty": 1, "stock_qty": 1,
            "uom": "Nos", "stock_uom": "Nos", "conversion_factor": 1,
            "rate": round(remaining, 2), "base_rate": round(remaining, 2),
            "amount": round(remaining, 2), "base_amount": round(remaining, 2),
            "net_rate": round(remaining, 2), "base_net_rate": round(remaining, 2),
            "net_amount": round(remaining, 2), "base_net_amount": round(remaining, 2),
            "expense_account": phantom_acct,
            "parent": voucher_no, "parenttype": "Purchase Invoice", "parentfield": "items",
        })
        net_total += remaining

    # Taxes
    tax_groups = _group_line_items_by_tax_rate(line_items)
    taxes_rows: list[dict] = []
    total_tax = 0.0
    for tax_idx, (rate, lis) in enumerate(tax_groups.items()):
        if rate == 0.0 or not vat_account:
            continue
        tax_amount_total = sum(float(li.get("tax_amount") or 0.0) for li in lis)
        if tax_amount_total <= 0:
            continue
        taxes_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": tax_idx + 1,
            "charge_type": "On Net Total",
            "account_head": vat_account,
            "description": f"VAT {rate:g}%",
            "rate": rate,
            "tax_amount": tax_amount_total, "base_tax_amount": tax_amount_total,
            "total": net_total + total_tax + tax_amount_total,
            "base_total": net_total + total_tax + tax_amount_total,
            "tax_amount_after_discount_amount": tax_amount_total,
            "base_tax_amount_after_discount_amount": tax_amount_total,
            "category": "Total", "add_deduct_tax": "Add",
            "parent": voucher_no, "parenttype": "Purchase Invoice", "parentfield": "taxes",
        })
        total_tax += tax_amount_total

    grand_total = round(net_total + total_tax, 0)

    # Payment Schedule
    ps_rows = [{
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 1,
        "due_date": posting_date,
        "invoice_portion": 100,
        "payment_amount": grand_total, "base_payment_amount": grand_total,
        "outstanding": grand_total, "base_outstanding": grand_total,
        "paid_amount": 0, "base_paid_amount": 0, "discounted_amount": 0,
        "parent": voucher_no, "parenttype": "Purchase Invoice", "parentfield": "payment_schedule",
    }]

    # Parent PI
    pi_row = {
        "name": voucher_no,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "supplier": party_code, "supplier_name": party_code,
        "posting_date": posting_date, "set_posting_time": 1,
        "due_date": posting_date,
        "bill_no": bill_no, "bill_date": bill_date,
        "remarks": (voucher.get("voucher_remark") or invoice.get("invoice_no") or "")[:500],
        "currency": "VND", "conversion_rate": 1.0,
        "buying_price_list": "Standard Buying",
        "price_list_currency": "VND", "plc_conversion_rate": 1.0,
        "total_qty": sum(r["qty"] for r in items_rows),
        "base_total": net_total, "base_net_total": net_total,
        "total": net_total, "net_total": net_total,
        "base_total_taxes_and_charges": total_tax, "total_taxes_and_charges": total_tax,
        "grand_total": grand_total, "base_grand_total": grand_total,
        "rounded_total": grand_total, "base_rounded_total": grand_total,
        "rounding_adjustment": 0, "base_rounding_adjustment": 0,
        "outstanding_amount": grand_total,
        "credit_to": credit_to_account, "party_account_currency": "VND",
        "ignore_pricing_rule": 1,
        "is_return": 0, "is_paid": 0, "is_opening": "No",
        "status": "Unpaid",
        "misa_voucher_no": voucher_no_raw,
    }

    # GL: Cr Supplier (grand_total) + Dr Expense (per-line) + Dr VAT (if any).
    # When credit_to was overridden to a non-Supplier account (e.g. Cr 711
    # Other Income contra), suppress party_type/party — only Receivable /
    # Payable accounts carry party. Account 711 is a Revenue type.
    gl_rows: list[dict] = []
    _is_override = bool(_credit_to_override)
    cr_row = {
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "posting_date": posting_date, "transaction_date": posting_date,
        "fiscal_year": fiscal_year,
        "account": credit_to_account, "account_currency": "VND",
        "voucher_type": "Purchase Invoice", "voucher_no": voucher_no,
        "against_voucher_type": "Purchase Invoice", "against_voucher": voucher_no,
        "transaction_currency": "VND",
        "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
        "debit": 0, "debit_in_account_currency": 0,
        "debit_in_transaction_currency": 0, "debit_in_reporting_currency": 0,
        "credit": grand_total, "credit_in_account_currency": grand_total,
        "credit_in_transaction_currency": grand_total, "credit_in_reporting_currency": grand_total,
        "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
        "remarks": f"PI {voucher_no} ← {party_code}",
    }
    if not _is_override:
        cr_row["party_type"] = "Supplier"
        cr_row["party"] = party_code
    gl_rows.append(cr_row)
    # Dr Expense per account
    by_expense_acct: dict[str, float] = {}
    for r in items_rows:
        acct = r["expense_account"]
        if not acct:
            continue
        by_expense_acct[acct] = by_expense_acct.get(acct, 0.0) + r["amount"]
    for acct, amt in by_expense_acct.items():
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date, "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": acct, "account_currency": "VND",
            "voucher_type": "Purchase Invoice", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": round(amt, 0), "debit_in_account_currency": round(amt, 0),
            "debit_in_transaction_currency": round(amt, 0), "debit_in_reporting_currency": round(amt, 0),
            "credit": 0, "credit_in_account_currency": 0,
            "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
            "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"PI {voucher_no} expense",
        })
    # Dr VAT
    if vat_account and total_tax > 0:
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date, "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": vat_account, "account_currency": "VND",
            "voucher_type": "Purchase Invoice", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": round(total_tax, 0), "debit_in_account_currency": round(total_tax, 0),
            "debit_in_transaction_currency": round(total_tax, 0), "debit_in_reporting_currency": round(total_tax, 0),
            "credit": 0, "credit_in_account_currency": 0,
            "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
            "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"PI {voucher_no} VAT input",
        })

    return {
        "Purchase Invoice": [pi_row],
        "Purchase Invoice Item": items_rows,
        "Purchase Taxes and Charges": taxes_rows,
        "Payment Schedule": ps_rows,
        "GL Entry": gl_rows,
    }
