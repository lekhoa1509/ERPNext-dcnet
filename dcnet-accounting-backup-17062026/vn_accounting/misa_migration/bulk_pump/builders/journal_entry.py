"""Journal Entry bulk-pump builder.

JE is the simplest: NKC source IS already a journal export. Each NKC voucher
becomes one JE doc with N accounts[] rows (one per Dr/Cr leg) + N GL Entry
rows (mirrored 1:1 from accounts[]).

Used for voucher types that don't map to SI/PI/PE/SE:
  - BC* (Bút toán điều chỉnh - adjustment JE)
  - PCK* (Phân bổ chi phí - cost allocation)
  - etc.
"""
from __future__ import annotations

import secrets
from typing import Any

import frappe
from frappe.utils import getdate

from vn_accounting.misa_migration.bulk_pump import account_resolver


def _gen_name() -> str:
    return secrets.token_hex(5)


def build_je_dicts(
    voucher: dict[str, Any],
    company: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    """Build JE + Journal Entry Account + GL Entry rows from one NKC voucher."""
    voucher_no = voucher.get("voucher_no")
    legs = voucher.get("legs") or []
    if not voucher_no or not legs:
        return None
    posting_date = voucher.get("posting_date")
    now = frappe.utils.now()
    fiscal_year = posting_date[:4] if isinstance(posting_date, str) else str(getdate(posting_date).year)

    accounts_rows: list[dict] = []
    gl_rows: list[dict] = []
    total_debit = total_credit = 0.0
    for idx, leg in enumerate(legs):
        raw_acc = leg.get("account_resolved") or leg.get("account")
        # Resolve Misa TK → full ERPNext account name (with abbr suffix).
        # When already a full name (contains ' - '), pass through.
        if raw_acc and " - " not in str(raw_acc):
            account = account_resolver.resolve(raw_acc, company)
        else:
            account = raw_acc
        if not account:
            continue
        debit = float(leg.get("debit") or 0.0)
        credit = float(leg.get("credit") or 0.0)
        party = leg.get("party")
        party_type = leg.get("party_type")
        # Journal Entry Account child
        accounts_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "account": account, "account_currency": "VND",
            "party_type": party_type, "party": party,
            "debit_in_account_currency": debit, "debit": debit,
            "credit_in_account_currency": credit, "credit": credit,
            "user_remark": (leg.get("description") or "")[:240],
            "parent": voucher_no, "parenttype": "Journal Entry", "parentfield": "accounts",
        })
        # GL Entry mirror
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date, "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": account, "account_currency": "VND",
            "party_type": party_type, "party": party,
            "voucher_type": "Journal Entry", "voucher_no": voucher_no,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": debit, "debit_in_account_currency": debit,
            "debit_in_transaction_currency": debit, "debit_in_reporting_currency": debit,
            "credit": credit, "credit_in_account_currency": credit,
            "credit_in_transaction_currency": credit, "credit_in_reporting_currency": credit,
            "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": (leg.get("description") or "")[:240],
        })
        total_debit += debit
        total_credit += credit

    if abs(total_debit - total_credit) > 0.01:
        return None  # Unbalanced — skip

    je_row = {
        "name": voucher_no,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "voucher_type": "Journal Entry",
        "posting_date": posting_date,
        "multi_currency": 0,
        "total_debit": total_debit, "total_credit": total_credit, "difference": 0,
        "total_amount_currency": "VND", "total_amount": total_debit,
        "user_remark": (voucher.get("voucher_remark") or "")[:240],
        "remark": (voucher.get("voucher_remark") or "")[:240],
        "is_opening": "No",
        "misa_voucher_no": voucher_no,
    }

    return {
        "Journal Entry": [je_row],
        "Journal Entry Account": accounts_rows,
        "GL Entry": gl_rows,
    }
