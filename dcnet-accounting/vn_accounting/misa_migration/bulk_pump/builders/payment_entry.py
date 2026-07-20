"""Payment Entry bulk-pump builder.

Canonical Misa prefix → PE direction (aligned with ORM voucher_router):
  - Receive: BC (Báo Có / bank credit), PT (Phiếu Thu / cash receipt)
  - Pay:     PC (Phiếu Chi / cash payment), UNC (Ủy Nhiệm Chi / bank pay order)

GL for Receive: Dr Bank / Cr Receivable (Customer party).
GL for Pay:     Dr Payable (Supplier party) / Cr Bank.

mode_of_payment from prefix:
  - BC, UNC → Bank Draft
  - PT, PC  → Cash

references[] (link to SI/PI) optional — migration can post as unallocated
and run a PE→SI/PI backfill pass later.
"""
from __future__ import annotations

import secrets
from typing import Any

import frappe
from frappe.utils import getdate

from vn_accounting.misa_migration.bulk_pump import account_resolver
from vn_accounting.misa_migration.importers._naming import migrated_doc_name


def _gen_name() -> str:
    return secrets.token_hex(5)


def _resolve_acc(raw: str | None, company: str) -> str | None:
    """Bare TK ('1111') → suffixed name ('1111 - Tiền mặt - DCT'). Idempotent."""
    if not raw:
        return None
    return account_resolver.resolve(raw, company) or raw


def build_pe_dicts(
    voucher: dict[str, Any],
    company: str,
    default_cash_account: str,
    default_receivable: str,
    default_payable: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    voucher_no = voucher.get("voucher_no")
    legs = voucher.get("legs") or []
    if not voucher_no or not legs:
        return None
    party_code = voucher.get("party_code") or ""
    posting_date = voucher.get("posting_date")
    now = frappe.utils.now()
    fiscal_year = posting_date[:4] if isinstance(posting_date, str) else str(getdate(posting_date).year)

    # Derive direction from FULL Misa prefix (BC/PT/PC/UNC).
    # Fallback to vno leading-letters when voucher.prefix unset.
    import re as _re
    prefix = (voucher.get("prefix") or "").upper()
    if not prefix:
        m = _re.match(r"^([A-Z]+)", voucher_no or "")
        prefix = m.group(1) if m else ""

    # Company-namespace the doc name AFTER prefix derivation (which needs the
    # raw voucher_no). Raw kept for reference_no + misa_voucher_no.
    voucher_no_raw = voucher_no
    voucher_no = migrated_doc_name(company, voucher_no)

    PE_RECEIVE = {"BC", "PT"}
    PE_PAY = {"PC", "UNC"}
    BANK_DRAFT = {"BC", "UNC"}

    def _bare(raw):
        return (raw if " - " not in raw else raw.split(" - ", 1)[0]).strip()

    # Detect Internal Transfer: ALL legs reference 111/112 cash-or-bank accounts
    # (no party). Misa bank-to-cash + bank-to-bank PTs/PCs have this shape.
    bank_legs = [
        L for L in legs
        if _bare(L.get("account_resolved") or L.get("account") or "").startswith(("111", "112"))
    ]
    is_internal_transfer = len(bank_legs) == len(legs) and len(legs) >= 2

    # PE represents exactly one Dr + one Cr leg pair. Vouchers with more legs
    # (Misa lumps multi-period tax payments into one UNC, or compound expense+VAT
    # paid direct, or customer payment with bank-fee split) cannot fit. Defer
    # to JE which handles N legs natively. Internal transfer 2-bank shape is
    # the only legitimate 2-leg PE.
    if len(legs) > 2:
        return None

    is_receive = prefix in PE_RECEIVE
    is_pay = prefix in PE_PAY
    if not (is_receive or is_pay) and not is_internal_transfer:
        first_leg = legs[0]
        first_acc = (first_leg.get("account_resolved") or first_leg.get("account") or "")
        is_receive = first_acc.startswith("131") and float(first_leg.get("credit") or 0) > 0
        is_pay = first_acc.startswith("331") and float(first_leg.get("debit") or 0) > 0
        if not (is_receive or is_pay):
            return None

    # Detect party_type by master existence — Misa "Mã đối tượng" can be a
    # Customer code, Supplier code, OR Employee code (e.g. PC paying advance
    # to an employee). Hardcoding Supplier for Pay misroutes employee
    # advances to TK 331 (Supplier Payable) instead of TK 141 (Tạm ứng).
    # Also canonicalize party_code to the DB-stored case (Misa 'VIETTEL' →
    # master 'Viettel') so case-sensitive qb queries in ERPNext reports work.
    detected_party_type = None
    if party_code and not is_internal_transfer:
        for dt in ("Employee", "Customer", "Supplier"):
            canonical = frappe.db.get_value(dt, party_code, "name")
            if canonical:
                party_code = canonical
                break
        if frappe.db.exists("Employee", party_code):
            detected_party_type = "Employee"
        elif is_receive:
            if frappe.db.exists("Customer", party_code):
                detected_party_type = "Customer"
            elif frappe.db.exists("Supplier", party_code):
                detected_party_type = "Supplier"
        else:  # is_pay
            if frappe.db.exists("Supplier", party_code):
                detected_party_type = "Supplier"
            elif frappe.db.exists("Customer", party_code):
                detected_party_type = "Customer"

    if is_internal_transfer:
        payment_type = "Internal Transfer"
        party_type = None
    else:
        payment_type = "Receive" if is_receive else "Pay"
        party_type = detected_party_type or ("Customer" if is_receive else "Supplier")
    mode_of_payment = "Bank Draft" if prefix in BANK_DRAFT else "Cash"
    # Internal Transfer doesn't need a party; Receive/Pay does.
    if not is_internal_transfer and not party_code:
        return None

    # Find total paid amount + accounts. The "party account" is whatever
    # Misa puts on the non-bank leg — could be:
    #   131 Receivable (Customer Receive)
    #   331 Payable (Supplier Pay)
    #   141 Advance / 334x Salary (Employee)
    #   3411 Loans / 635 Financial Exp / etc. (bank-related Misa PE)
    # Using the ACTUAL leg account preserves the source semantics —
    # hardcoding 331 for every Supplier-party PE silently misroutes
    # loan repayments and bank fees.
    # Default only kicks in if NO non-bank leg is found.
    if party_type == "Employee":
        default_party_acc = (account_resolver.resolve("141", company)
                             or account_resolver.resolve("3341", company))
    elif party_type == "Customer":
        default_party_acc = default_receivable
    else:  # Supplier or fallback
        default_party_acc = default_payable

    bank_account = None          # Receive/Pay: the single bank/cash leg
    bank_from = bank_account_to = None  # Internal Transfer: paid_from + paid_to
    party_account = None         # Discovered from first non-bank leg
    total_amount = 0.0
    for leg in legs:
        raw = leg.get("account_resolved") or leg.get("account") or ""
        acc = _resolve_acc(raw, company) or raw
        debit = float(leg.get("debit") or 0)
        credit = float(leg.get("credit") or 0)
        bare = _bare(raw)
        if is_internal_transfer:
            if bare.startswith(("111", "112")):
                if debit > 0 and not bank_account_to:
                    bank_account_to = acc
                    total_amount = debit
                elif credit > 0 and not bank_from:
                    bank_from = acc
        else:
            if bare.startswith(("111", "112")):
                bank_account = acc
                if is_receive:
                    total_amount = debit  # Dr Bank
                else:
                    total_amount = credit  # Cr Bank
            else:
                # Non-bank leg = the actual offset account (data-driven).
                # First non-bank leg wins; bigger legs override.
                amt = debit if not is_receive else credit
                if not party_account or amt > 0:
                    party_account = acc
    if not party_account:
        party_account = default_party_acc

    if is_internal_transfer:
        if not bank_from or not bank_account_to or total_amount <= 0:
            return None
        paid_from = bank_from
        paid_to = bank_account_to
    else:
        if not bank_account or total_amount <= 0:
            return None
        paid_from = party_account if is_receive else bank_account
        paid_to = bank_account if is_receive else party_account

    # Internal Transfer: blank party fields (ERPNext requires party empty for IT)
    pe_party_type = None if is_internal_transfer else party_type
    pe_party = None if is_internal_transfer else party_code
    pe_party_name = None if is_internal_transfer else party_code

    # PE parent row
    pe_row = {
        "name": voucher_no,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "payment_type": payment_type,
        "mode_of_payment": mode_of_payment,
        "posting_date": posting_date,
        "party_type": pe_party_type, "party": pe_party, "party_name": pe_party_name,
        "paid_from": paid_from, "paid_from_account_currency": "VND",
        "paid_to": paid_to, "paid_to_account_currency": "VND",
        "paid_amount": total_amount, "base_paid_amount": total_amount,
        "received_amount": total_amount, "base_received_amount": total_amount,
        "source_exchange_rate": 1.0, "target_exchange_rate": 1.0,
        "total_allocated_amount": 0, "base_total_allocated_amount": 0,
        "unallocated_amount": total_amount,
        "difference_amount": 0,
        "status": "Submitted",
        "reference_no": voucher_no_raw, "reference_date": posting_date,
        "remarks": (voucher.get("voucher_remark") or "")[:240],
        "misa_voucher_no": voucher_no_raw,
    }

    # GL: 2 rows.
    # Receive:  Dr Bank,    Cr Party (Customer)
    # Pay:      Dr Party,   Cr Bank
    # Internal: Dr paid_to, Cr paid_from
    if is_internal_transfer:
        gl_dr_acc, gl_cr_acc = paid_to, paid_from
    elif is_receive:
        gl_dr_acc, gl_cr_acc = bank_account, party_account
    else:
        gl_dr_acc, gl_cr_acc = party_account, bank_account
    gl_rows = []
    # Dr leg
    gl_rows.append({
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "posting_date": posting_date, "transaction_date": posting_date,
        "fiscal_year": fiscal_year,
        "account": gl_dr_acc, "account_currency": "VND",
        "party_type": party_type if gl_dr_acc == party_account else None,
        "party": party_code if gl_dr_acc == party_account else None,
        "voucher_type": "Payment Entry", "voucher_no": voucher_no,
        "transaction_currency": "VND",
        "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
        "debit": total_amount, "debit_in_account_currency": total_amount,
        "debit_in_transaction_currency": total_amount, "debit_in_reporting_currency": total_amount,
        "credit": 0, "credit_in_account_currency": 0,
        "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
        "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
        "remarks": f"PE {voucher_no} {payment_type}",
    })
    # Cr leg
    gl_rows.append({
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "posting_date": posting_date, "transaction_date": posting_date,
        "fiscal_year": fiscal_year,
        "account": gl_cr_acc, "account_currency": "VND",
        "party_type": party_type if gl_cr_acc == party_account else None,
        "party": party_code if gl_cr_acc == party_account else None,
        "voucher_type": "Payment Entry", "voucher_no": voucher_no,
        "transaction_currency": "VND",
        "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
        "debit": 0, "debit_in_account_currency": 0,
        "debit_in_transaction_currency": 0, "debit_in_reporting_currency": 0,
        "credit": total_amount, "credit_in_account_currency": total_amount,
        "credit_in_transaction_currency": total_amount, "credit_in_reporting_currency": total_amount,
        "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
        "remarks": f"PE {voucher_no} {payment_type}",
    })

    return {
        "Payment Entry": [pe_row],
        "GL Entry": gl_rows,
    }
