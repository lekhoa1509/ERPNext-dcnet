"""Build draft Journal Entries for treasury operations.

All JEs are created as Draft. Accountant reviews and submits manually.
"""
from __future__ import annotations

import frappe


def _get_bank_gl_account(bank_account_name: str) -> str:
    """Get the GL account linked to a Bank Account record."""
    return frappe.db.get_value("Bank Account", bank_account_name, "account")


def _create_je(company: str, posting_date, accounts: list[dict], remark: str,
               ref_doctype: str = None, ref_name: str = None,
               source_key: str | None = None) -> str:
    """Create a draft Journal Entry and return its name.

    When source_key is provided, also register in Auto Generated Doc Registry
    so the JE appears in the central worklist report.
    """
    cost_center = frappe.db.get_value("Company", company, "cost_center")
    for acc in accounts:
        if cost_center and "cost_center" not in acc:
            acc["cost_center"] = cost_center
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Bank Entry",
        "company": company,
        "posting_date": posting_date,
        "user_remark": remark,
        "accounts": accounts,
    })
    je.flags.ignore_permissions = True
    je.insert()

    if source_key:
        from vn_accounting.auto_source import register
        register("Journal Entry", je.name, source_key,
                 registered_by="vn_accounting.treasury.journal_entry_builder")

    frappe.db.commit()
    return je.name


def create_deposit_je(term_deposit) -> str:
    """JE for new deposit: Debit deposit_account / Credit bank GL account.

    For Prepaid type: 3-leg JE (Debit 1281 / Credit 112x partial / Credit 515 interest).
    """
    bank_gl = _get_bank_gl_account(term_deposit.bank_account)
    accounts = []

    if term_deposit.interest_type == "Prepaid" and term_deposit.interest_schedule:
        prepaid_interest = term_deposit.interest_schedule[0].interest_amount
        accounts = [
            {"account": term_deposit.deposit_account, "debit_in_account_currency": term_deposit.principal_amount},
            {"account": bank_gl, "credit_in_account_currency": term_deposit.principal_amount - prepaid_interest},
            {"account": term_deposit.interest_income_account, "credit_in_account_currency": prepaid_interest},
        ]
    else:
        accounts = [
            {"account": term_deposit.deposit_account, "debit_in_account_currency": term_deposit.principal_amount},
            {"account": bank_gl, "credit_in_account_currency": term_deposit.principal_amount},
        ]

    return _create_je(
        term_deposit.company, term_deposit.start_date, accounts,
        f"Term Deposit {term_deposit.name} - Deposit",
        source_key="vn_accounting.treasury.deposit_creation",
    )


def create_interest_je(term_deposit, schedule_row) -> str:
    """JE for periodic interest: Debit bank/deposit_account / Credit interest_income_account.

    Compound type: Debit deposit_account (interest reinvested).
    Others: Debit bank GL account (interest received in bank).
    """
    bank_gl = _get_bank_gl_account(term_deposit.bank_account)

    if term_deposit.interest_type == "Compound":
        debit_account = term_deposit.deposit_account
    else:
        debit_account = bank_gl

    accounts = [
        {"account": debit_account, "debit_in_account_currency": schedule_row.interest_amount},
        {"account": term_deposit.interest_income_account, "credit_in_account_currency": schedule_row.interest_amount},
    ]
    return _create_je(
        term_deposit.company, schedule_row.due_date, accounts,
        f"Term Deposit {term_deposit.name} - Interest period {schedule_row.due_date}",
        source_key="vn_accounting.treasury.deposit_interest",
    )


def create_settlement_je(term_deposit, settlement_date=None) -> str:
    """JE for settlement: Debit bank GL / Credit deposit_account.

    If End of Term and not early: include interest leg.
    If early settlement: use early_withdrawal_rate for pro-rata interest.
    """
    bank_gl = _get_bank_gl_account(term_deposit.bank_account)
    posting_date = settlement_date or term_deposit.maturity_date
    accounts = [
        {"account": bank_gl, "debit_in_account_currency": term_deposit.principal_amount},
        {"account": term_deposit.deposit_account, "credit_in_account_currency": term_deposit.principal_amount},
    ]

    # Add interest leg for End of Term (interest not yet paid)
    if term_deposit.interest_type == "End of Term" and not settlement_date:
        interest = term_deposit.interest_schedule[0].interest_amount if term_deposit.interest_schedule else 0
        if interest > 0:
            accounts[0]["debit_in_account_currency"] += interest
            accounts.append({
                "account": term_deposit.interest_income_account,
                "credit_in_account_currency": interest,
            })

    # Early settlement: pro-rata interest adjustment
    if settlement_date:
        from vn_accounting.treasury.interest_calculator import calculate_early_settlement_interest
        paid = sum(r.interest_amount for r in term_deposit.interest_schedule if r.status == "Booked")
        result = calculate_early_settlement_interest(
            principal=term_deposit.principal_amount,
            original_rate=term_deposit.interest_rate,
            early_rate=term_deposit.early_withdrawal_rate or 0,
            start_date=term_deposit.start_date,
            settlement_date=settlement_date,
            interest_already_paid=paid,
        )
        adj = result["adjustment"]
        if adj > 0:
            accounts[0]["debit_in_account_currency"] += adj
            accounts.append({
                "account": term_deposit.interest_income_account,
                "credit_in_account_currency": adj,
            })
        elif adj < 0:
            accounts.append({
                "account": term_deposit.interest_income_account,
                "debit_in_account_currency": abs(adj),
            })
            accounts[0]["debit_in_account_currency"] += adj  # reduces bank debit

    return _create_je(
        term_deposit.company, posting_date, accounts,
        f"Term Deposit {term_deposit.name} - Settlement",
        source_key="vn_accounting.treasury.deposit_settlement",
    )


def create_disbursement_je(bank_loan) -> str:
    """JE for loan disbursement: Debit bank GL / Credit loan_account."""
    bank_gl = _get_bank_gl_account(bank_loan.bank_account)
    accounts = [
        {"account": bank_gl, "debit_in_account_currency": bank_loan.loan_amount},
        {"account": bank_loan.loan_account, "credit_in_account_currency": bank_loan.loan_amount},
    ]
    return _create_je(
        bank_loan.company, bank_loan.start_date, accounts,
        f"Bank Loan {bank_loan.name} - Disbursement",
        source_key="vn_accounting.treasury.loan_disbursement",
    )


def create_repayment_je(bank_loan, schedule_row) -> str:
    """JE for loan repayment: Debit loan_account + interest_expense / Credit bank GL."""
    bank_gl = _get_bank_gl_account(bank_loan.bank_account)
    accounts = []

    if schedule_row.principal_amount > 0:
        accounts.append({
            "account": bank_loan.loan_account,
            "debit_in_account_currency": schedule_row.principal_amount,
        })
    if schedule_row.interest_amount > 0:
        accounts.append({
            "account": bank_loan.interest_expense_account,
            "debit_in_account_currency": schedule_row.interest_amount,
        })
    accounts.append({
        "account": bank_gl,
        "credit_in_account_currency": schedule_row.total_amount,
    })

    return _create_je(
        bank_loan.company, schedule_row.due_date, accounts,
        f"Bank Loan {bank_loan.name} - Repayment {schedule_row.due_date}",
        source_key="vn_accounting.treasury.loan_repayment",
    )


def create_deposit_accrual_je(term_deposit, accrual_date, amount) -> str:
    """Accrual JE: Debit interest_receivable (1388) / Credit interest_income (515)."""
    accounts = [
        {"account": term_deposit.interest_receivable_account,
         "debit_in_account_currency": amount},
        {"account": term_deposit.interest_income_account,
         "credit_in_account_currency": amount},
    ]
    return _create_je(term_deposit.company, accrual_date, accounts,
        f"Term Deposit {term_deposit.name} - Accrued interest to {accrual_date}",
        source_key="vn_accounting.treasury.deposit_accrual")


def create_loan_accrual_je(bank_loan, accrual_date, amount) -> str:
    """Accrual JE: Debit interest_expense (635) / Credit interest_payable (335)."""
    accounts = [
        {"account": bank_loan.interest_expense_account,
         "debit_in_account_currency": amount},
        {"account": bank_loan.interest_payable_account,
         "credit_in_account_currency": amount},
    ]
    return _create_je(bank_loan.company, accrual_date, accounts,
        f"Bank Loan {bank_loan.name} - Accrued interest to {accrual_date}",
        source_key="vn_accounting.treasury.loan_accrual")


def create_loan_settlement_je(bank_loan, settlement_date) -> str:
    """JE for early loan settlement: remaining principal + pro-rata interest."""
    bank_gl = _get_bank_gl_account(bank_loan.bank_account)

    # Find last booked row to get outstanding
    booked = [r for r in bank_loan.repayment_schedule if r.status == "Booked"]
    outstanding = booked[-1].outstanding_after if booked else bank_loan.loan_amount

    # Pro-rata interest from last payment to settlement
    last_date = booked[-1].due_date if booked else bank_loan.start_date
    if isinstance(last_date, str):
        from frappe.utils import getdate
        last_date = getdate(last_date)
    if isinstance(settlement_date, str):
        from frappe.utils import getdate
        settlement_date = getdate(settlement_date)

    days = (settlement_date - last_date).days
    interest = outstanding * (bank_loan.interest_rate / 100) * days / 365

    accounts = [
        {"account": bank_loan.loan_account, "debit_in_account_currency": round(outstanding, 2)},
    ]
    if round(interest, 2) > 0:
        accounts.append({
            "account": bank_loan.interest_expense_account,
            "debit_in_account_currency": round(interest, 2),
        })
    accounts.append({
        "account": bank_gl,
        "credit_in_account_currency": round(outstanding + interest, 2),
    })

    return _create_je(
        bank_loan.company, settlement_date, accounts,
        f"Bank Loan {bank_loan.name} - Early Settlement",
        source_key="vn_accounting.treasury.loan_settlement",
    )
