# Copyright (c) 2026, DCNet and Contributors
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

from vn_accounting.treasury.repayment_calculator import build_repayment_schedule


class BankLoan(Document):
    def validate(self):
        self._validate_company()
        self._build_schedule()
        self._compute_totals()
        self._set_default_accounts()

    def _validate_company(self):
        if self.bank_account and self.company:
            ba_company = frappe.db.get_value("Bank Account", self.bank_account, "company")
            if ba_company and ba_company != self.company:
                frappe.throw(_("Bank Account {0} belongs to company {1}, not {2}").format(
                    self.bank_account, ba_company, self.company))

    def on_submit(self):
        from vn_accounting.treasury.journal_entry_builder import create_disbursement_je
        self.db_set("status", "Active")
        self.db_set("outstanding_amount", self.loan_amount)
        je_name = create_disbursement_je(self)
        self.db_set("disbursement_je", je_name)

    def on_cancel(self):
        if self.disbursement_je:
            je = frappe.get_doc("Journal Entry", self.disbursement_je)
            if je.docstatus == 0:
                je.delete()
            elif je.docstatus == 1:
                je.cancel()
        self.db_set("status", "Cancelled")
        self.db_set("outstanding_amount", 0)

    def _build_schedule(self):
        if self.docstatus == 1:
            return  # Never rebuild schedule after submit — Booked rows would be lost
        if not (self.loan_amount and self.interest_rate and self.repayment_type
                and self.repayment_frequency and self.start_date and self.maturity_date):
            return
        rows = build_repayment_schedule(
            loan_amount=self.loan_amount,
            rate=self.interest_rate,
            repayment_type=self.repayment_type,
            frequency=self.repayment_frequency,
            start_date=getdate(self.start_date),
            maturity_date=getdate(self.maturity_date),
        )
        self.set("repayment_schedule", [])
        for r in rows:
            self.append("repayment_schedule", {
                "due_date": r["due_date"],
                "principal_amount": r["principal_amount"],
                "interest_amount": r["interest_amount"],
                "total_amount": r["total_amount"],
                "outstanding_after": r["outstanding_after"],
                "status": "Pending",
            })

    def _compute_totals(self):
        self.total_interest = sum(r.interest_amount for r in self.repayment_schedule)
        self.total_repayment = sum(r.total_amount for r in self.repayment_schedule)

    def _set_default_accounts(self):
        if not self.loan_account or not self.interest_expense_account or not self.interest_payable_account:
            from vn_accounting.utils.account_resolver import resolve_account
            company = self.company
            if not company:
                return
            if not self.loan_account:
                self.loan_account = resolve_account("default_loan_account", company)
            if not self.interest_expense_account:
                self.interest_expense_account = resolve_account("default_interest_expense_account", company)
            if not self.interest_payable_account:
                self.interest_payable_account = resolve_account("default_loan_interest_payable", company)

    @frappe.whitelist()
    def create_accrual(self, accrual_date):
        """Create accrual JE for period-end interest recognition."""
        from vn_accounting.treasury.interest_calculator import calculate_accrued_interest
        from vn_accounting.treasury.journal_entry_builder import create_loan_accrual_je
        if not self.interest_payable_account:
            frappe.throw(_("Interest Payable Account is required for accrual entries"))
        booked = [r for r in self.repayment_schedule if r.status == "Booked"]
        last_date = booked[-1].due_date if booked else self.start_date
        outstanding = booked[-1].outstanding_after if booked else self.loan_amount
        amount = calculate_accrued_interest(outstanding, self.interest_rate, getdate(last_date), getdate(accrual_date))
        if amount <= 0:
            frappe.msgprint(_("No accrued interest for this period"))
            return
        je_name = create_loan_accrual_je(self, accrual_date, amount)
        frappe.msgprint(_("Accrual Journal Entry {0} created").format(je_name), alert=True)
        return je_name

    @frappe.whitelist()
    def settle_early(self, settlement_date=None):
        """Early settlement: pay remaining principal + pro-rata interest."""
        from vn_accounting.treasury.journal_entry_builder import create_loan_settlement_je
        settlement_date = settlement_date or frappe.utils.today()
        create_loan_settlement_je(self, settlement_date)
        self.db_set("status", "Settled")
        self.db_set("outstanding_amount", 0)

    @frappe.whitelist()
    def update_rate(self, new_rate, effective_date):
        """Update interest rate (floating) and regenerate schedule from next unbooked period."""
        if self.rate_type != "Floating":
            frappe.throw(_("Rate can only be updated for Floating rate loans"))
        self.interest_rate = new_rate
        booked = [r for r in self.repayment_schedule if r.status == "Booked"]
        outstanding = booked[-1].outstanding_after if booked else self.loan_amount
        remaining_start = booked[-1].due_date if booked else self.start_date

        new_rows = build_repayment_schedule(
            loan_amount=outstanding,
            rate=new_rate,
            repayment_type=self.repayment_type,
            frequency=self.repayment_frequency,
            start_date=getdate(remaining_start),
            maturity_date=getdate(self.maturity_date),
        )
        self.set("repayment_schedule", [])
        for r in booked:
            self.append("repayment_schedule", r.as_dict())
        for r in new_rows:
            self.append("repayment_schedule", {**r, "status": "Pending"})
        self._compute_totals()
        self.save()
