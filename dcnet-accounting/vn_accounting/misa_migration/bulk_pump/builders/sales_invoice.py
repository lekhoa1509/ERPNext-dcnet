"""Sales Invoice bulk-pump builder.

Input: Misa NKC voucher (BH prefix) + matching Bảng kê BR invoice.
Output: dict of lists ready for bulk_insert into 5 tables:
  - Sales Invoice (parent)
  - Sales Invoice Item (children)
  - Sales Taxes and Charges (children)
  - Payment Schedule (1 child per SI)
  - GL Entry (Dr Customer / Cr Income / Cr VAT — derived from NKC legs)

The output rows have docstatus=1 set directly — no submit cycle needed.
"""
from __future__ import annotations

import json
import secrets
import time
from typing import Any

import frappe
from frappe.utils import flt, getdate

from vn_accounting.misa_migration.importers._naming import migrated_doc_name
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    _load_account_mapping,
    _resolve_account,
    extract_line_income_accounts,
    extract_tax_account,
    _group_line_items_by_tax_rate,
)

# Per-process Item resolution cache (avoid repeated lookups).
_ITEM_CACHE: dict[str, str | None] = {}


_HAS_WORKFLOW_STATE: bool | None = None


def _si_has_workflow_state() -> bool:
    """True when tabSales Invoice has the workflow_state column (site has a
    Workflow on SI). Cached per process; None = unchecked."""
    global _HAS_WORKFLOW_STATE
    if _HAS_WORKFLOW_STATE is None:
        _HAS_WORKFLOW_STATE = bool(
            frappe.db.has_column("Sales Invoice", "workflow_state"))
    return _HAS_WORKFLOW_STATE


def _gen_name(prefix: str = "") -> str:
    """10-char random hex for child row names (matches Frappe's autoname)."""
    return secrets.token_hex(5)


def _resolve_item_code(misa_item_name: str | None, placeholder: str) -> str:
    """Match Misa item_name → Item.name (exact match on item_name first).
    Falls back to placeholder Item code."""
    if not misa_item_name:
        return placeholder
    if misa_item_name in _ITEM_CACHE:
        return _ITEM_CACHE[misa_item_name] or placeholder
    code = frappe.db.get_value("Item", {"item_name": misa_item_name}, "name")
    _ITEM_CACHE[misa_item_name] = code
    return code or placeholder


def build_si_dicts(
    voucher: dict[str, Any],
    invoice: dict[str, Any],
    company: str,
    abbr: str,
    placeholder_item: str,
    debit_to_account: str,
    default_income_account: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    """Build the 5-table dict set for one SI. Returns None if voucher unprocessable."""
    voucher_no = voucher.get("voucher_no")
    if not voucher_no:
        return None
    # Company-namespace the doc name (and all parent/child/GL references that
    # use it) so two companies' overlapping Misa voucher numbers don't collide
    # on ERPNext's global doc name. Raw number kept in misa_voucher_no.
    voucher_no_raw = voucher_no
    voucher_no = migrated_doc_name(company, voucher_no)
    party_code = voucher.get("party_code") or ""
    if not party_code:
        return None
    line_items = invoice.get("line_items") or []
    if not line_items:
        return None

    posting_date = voucher.get("posting_date") or invoice.get("posting_date")
    bill_no = invoice.get("invoice_no") or voucher.get("invoice_no")
    bill_date = invoice.get("invoice_date") or voucher.get("invoice_date")

    mapping = _load_account_mapping()
    # Pass per-line amounts for amount-match routing (PR #111). Misa BR/MV
    # often has 'Thành tiền' blank with qty + 'Đơn giá' filled — fall back
    # to qty*rate so amount-match still finds the matching Cr leg.
    def _line_amount(li):
        v = float(li.get("amount") or 0) or float(li.get("net_amount") or 0)
        if v > 0:
            return v
        return float(li.get("qty") or 0) * float(li.get("rate") or 0)
    line_amounts = [_line_amount(li) for li in line_items]
    per_line_tk = extract_line_income_accounts(
        voucher.get("legs") or [], len(line_items), line_amounts,
    )
    per_line_income_acct = [_resolve_account(tk, mapping, company) for tk in per_line_tk]
    vat_tk = extract_tax_account(voucher.get("legs") or [])
    vat_account = _resolve_account(vat_tk, mapping, company) if vat_tk else None

    # === Build SI Item rows + totals ===
    items_rows: list[dict] = []
    net_total = 0.0
    now = frappe.utils.now()
    for idx, li in enumerate(line_items):
        qty = float(li.get("qty") or 0.0)
        rate = float(li.get("rate") or 0.0)
        net_amount = float(li.get("net_amount") or 0.0)
        if qty <= 0:
            qty = 1.0
            rate = net_amount
        if qty != int(qty):
            rate = qty * rate
            qty = 1.0
        amount = round(qty * rate, 2)
        uom = li.get("uom") or "Nos"
        if not frappe.db.exists("UOM", uom):
            uom = "Nos"
        raw_name = li.get("item_name") or li.get("description") or placeholder_item
        item_code_used = _resolve_item_code(li.get("item_name"), placeholder_item)
        income_account = (per_line_income_acct[idx] if idx < len(per_line_income_acct) and per_line_income_acct[idx] else None) or default_income_account

        items_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "item_code": item_code_used,
            "item_name": str(raw_name)[:140],
            "description": (li.get("description") or li.get("item_name") or "")[:5000],
            "qty": qty, "stock_qty": qty,
            "uom": uom, "stock_uom": uom, "conversion_factor": 1,
            "rate": rate, "base_rate": rate,
            "amount": amount, "base_amount": amount,
            "net_rate": rate, "base_net_rate": rate,
            "net_amount": amount, "base_net_amount": amount,
            "income_account": income_account,
            "parent": voucher_no, "parenttype": "Sales Invoice", "parentfield": "items",
        })
        net_total += amount

    # === Build Taxes rows ===
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
            "included_in_print_rate": 0,
            "tax_amount": tax_amount_total, "base_tax_amount": tax_amount_total,
            "total": net_total + total_tax + tax_amount_total,
            "base_total": net_total + total_tax + tax_amount_total,
            "tax_amount_after_discount_amount": tax_amount_total,
            "base_tax_amount_after_discount_amount": tax_amount_total,
            "parent": voucher_no, "parenttype": "Sales Invoice", "parentfield": "taxes",
        })
        total_tax += tax_amount_total

    grand_total = round(net_total + total_tax, 0)  # VND no decimals

    # === Build Payment Schedule (1 row, due=posting) ===
    ps_rows = [{
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 1,
        "due_date": posting_date,
        "invoice_portion": 100,
        "payment_amount": grand_total, "base_payment_amount": grand_total,
        "outstanding": grand_total, "base_outstanding": grand_total,
        "paid_amount": 0, "base_paid_amount": 0, "discounted_amount": 0,
        "parent": voucher_no, "parenttype": "Sales Invoice", "parentfield": "payment_schedule",
    }]

    # === Build parent SI row ===
    si_row = {
        "name": voucher_no,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "customer": party_code,
        "customer_name": party_code,  # FIXME look up real Customer.customer_name
        "posting_date": posting_date,
        "set_posting_time": 1,
        "due_date": posting_date,
        "po_no": bill_no, "po_date": bill_date,  # SI uses po_no/po_date (PI uses bill_no/bill_date)
        "remarks": (voucher.get("voucher_remark") or invoice.get("invoice_no") or "")[:500],
        "currency": "VND", "conversion_rate": 1.0,
        "selling_price_list": "Standard Selling",
        "price_list_currency": "VND", "plc_conversion_rate": 1.0,
        "total_qty": sum(r["qty"] for r in items_rows),
        "base_total": net_total, "base_net_total": net_total,
        "total": net_total, "net_total": net_total,
        "base_total_taxes_and_charges": total_tax, "total_taxes_and_charges": total_tax,
        "grand_total": grand_total, "base_grand_total": grand_total,
        "rounded_total": grand_total, "base_rounded_total": grand_total,
        "rounding_adjustment": 0, "base_rounding_adjustment": 0,
        "outstanding_amount": grand_total,
        "debit_to": debit_to_account,
        "party_account_currency": "VND",
        "ignore_pricing_rule": 1,
        "is_pos": 0, "is_return": 0, "is_opening": "No",
        "status": "Unpaid",
        "misa_voucher_no": voucher_no_raw,
    }
    # docstatus=1 → set workflow_state khớp state Workflow.doc_status='1'
    # (Approved). Tránh `WorkflowStateError: Trạng thái quy trình chưa
    # được thiết lập` mỗi lần mở form (Frappe core gọi get_transitions).
    # Cột chỉ tồn tại khi site có Workflow trên Sales Invoice — site mới
    # không có → INSERT chết "Unknown column 'workflow_state'".
    if _si_has_workflow_state():
        si_row["workflow_state"] = "Approved"

    # === Build GL Entry rows ===
    # Dr debit_to / Cr income_account[per_line] + Cr vat_account
    gl_rows: list[dict] = []
    fiscal_year = posting_date[:4] if isinstance(posting_date, str) else str(getdate(posting_date).year)
    # Dr Customer (receivable)
    gl_rows.append({
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "posting_date": posting_date,
        "transaction_date": posting_date,
        "fiscal_year": fiscal_year,
        "account": debit_to_account, "account_currency": "VND",
        "party_type": "Customer", "party": party_code,
        "voucher_type": "Sales Invoice", "voucher_no": voucher_no,
        "transaction_currency": "VND",
        "against_voucher_type": "Sales Invoice", "against_voucher": voucher_no,
        "transaction_exchange_rate": 1.0,
        "reporting_currency_exchange_rate": 1.0,
        "debit": grand_total, "debit_in_account_currency": grand_total,
        "debit_in_transaction_currency": grand_total, "debit_in_reporting_currency": grand_total,
        "credit": 0, "credit_in_account_currency": 0,
        "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
        "company": company,
        "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
        "remarks": f"SI {voucher_no} → {party_code}",
    })
    # Cr Income (per-line aggregated by account)
    by_income_acct: dict[str, float] = {}
    for idx, r in enumerate(items_rows):
        acct = r["income_account"]
        if not acct:
            continue
        by_income_acct[acct] = by_income_acct.get(acct, 0.0) + r["amount"]
    for acct, amt in by_income_acct.items():
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date,
            "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": acct, "account_currency": "VND",
            "voucher_type": "Sales Invoice", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0,
            "reporting_currency_exchange_rate": 1.0,
            "debit": 0, "debit_in_account_currency": 0,
            "debit_in_transaction_currency": 0, "debit_in_reporting_currency": 0,
            "credit": round(amt, 0), "credit_in_account_currency": round(amt, 0),
            "credit_in_transaction_currency": round(amt, 0), "credit_in_reporting_currency": round(amt, 0),
            "company": company,
            "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"SI {voucher_no} income",
        })
    # Cr VAT (if any)
    if vat_account and total_tax > 0:
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date,
            "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": vat_account, "account_currency": "VND",
            "voucher_type": "Sales Invoice", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0,
            "reporting_currency_exchange_rate": 1.0,
            "debit": 0, "debit_in_account_currency": 0,
            "debit_in_transaction_currency": 0, "debit_in_reporting_currency": 0,
            "credit": round(total_tax, 0), "credit_in_account_currency": round(total_tax, 0),
            "credit_in_transaction_currency": round(total_tax, 0), "credit_in_reporting_currency": round(total_tax, 0),
            "company": company,
            "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"SI {voucher_no} VAT",
        })

    return {
        "Sales Invoice": [si_row],
        "Sales Invoice Item": items_rows,
        "Sales Taxes and Charges": taxes_rows,
        "Payment Schedule": ps_rows,
        "GL Entry": gl_rows,
    }
