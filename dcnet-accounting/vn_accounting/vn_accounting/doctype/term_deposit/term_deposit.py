# Copyright (c) 2026, DCNet and Contributors
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta

from vn_accounting.treasury.interest_calculator import build_interest_schedule


class TermDeposit(Document):
    def validate(self):
        self._compute_maturity()
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
        from vn_accounting.treasury.journal_entry_builder import create_deposit_je
        self.db_set("status", "Active")
        je_name = create_deposit_je(self)
        self.db_set("deposit_je", je_name)

    def on_cancel(self):
        if self.deposit_je:
            je = frappe.get_doc("Journal Entry", self.deposit_je)
            if je.docstatus == 0:
                je.delete()
            elif je.docstatus == 1:
                je.cancel()
        self.db_set("status", "Cancelled")

    def _compute_maturity(self):
        if self.start_date and self.term_months:
            self.maturity_date = getdate(self.start_date) + relativedelta(months=int(self.term_months))

    def _build_schedule(self):
        if self.docstatus == 1:
            return  # Never rebuild schedule after submit — Booked rows would be lost
        if not (self.principal_amount and self.interest_rate and self.interest_type
                and self.start_date and self.term_months):
            return
        rows = build_interest_schedule(
            principal=self.principal_amount,
            rate=self.interest_rate,
            interest_type=self.interest_type,
            start_date=getdate(self.start_date),
            term_months=int(self.term_months),
        )
        self.set("interest_schedule", [])
        for r in rows:
            self.append("interest_schedule", {
                "due_date": r["due_date"],
                "interest_amount": r["interest_amount"],
                "principal_at_start": r["principal_at_start"],
                "status": "Pending",
            })

    def _compute_totals(self):
        self.total_interest = sum(r.interest_amount for r in self.interest_schedule)

    def _set_default_accounts(self):
        if not self.deposit_account or not self.interest_income_account or not self.interest_receivable_account:
            from vn_accounting.utils.account_resolver import resolve_account
            company = self.company
            if not company:
                return
            if not self.deposit_account:
                self.deposit_account = resolve_account("default_deposit_account", company)
            if not self.interest_income_account:
                self.interest_income_account = resolve_account("default_interest_income_account", company)
            if not self.interest_receivable_account:
                self.interest_receivable_account = resolve_account("default_deposit_interest_receivable", company)

    @frappe.whitelist()
    def create_accrual(self, accrual_date):
        """Create accrual JE for period-end interest recognition."""
        from vn_accounting.treasury.interest_calculator import calculate_accrued_interest
        from vn_accounting.treasury.journal_entry_builder import create_deposit_accrual_je
        if not self.interest_receivable_account:
            frappe.throw(_("Interest Receivable Account is required for accrual entries"))
        booked = [r for r in self.interest_schedule if r.status == "Booked"]
        last_date = booked[-1].due_date if booked else self.start_date
        amount = calculate_accrued_interest(self.principal_amount, self.interest_rate, getdate(last_date), getdate(accrual_date))
        if amount <= 0:
            frappe.msgprint(_("No accrued interest for this period"))
            return
        je_name = create_deposit_accrual_je(self, accrual_date, amount)
        frappe.msgprint(_("Accrual Journal Entry {0} created").format(je_name), alert=True)
        return je_name

    @frappe.whitelist()
    def settle(self, settlement_date=None):
        """Settle the term deposit at maturity or early."""
        from vn_accounting.treasury.journal_entry_builder import create_settlement_je
        if settlement_date and str(settlement_date) < str(self.maturity_date):
            create_settlement_je(self, settlement_date=settlement_date)
            self.db_set("status", "Early Settled")
        else:
            create_settlement_je(self)
            self.db_set("status", "Settled")

    @frappe.whitelist()
    def renew(self):
        """Create a new Term Deposit from this matured one."""
        if self.status != "Matured":
            frappe.throw(_("Can only renew Matured deposits"))
        new_principal = self.principal_amount
        if self.interest_type in ("Compound", "End of Term"):
            new_principal += self.total_interest
        new_doc = frappe.copy_doc(self)
        new_doc.principal_amount = new_principal
        new_doc.start_date = self.maturity_date
        new_doc.status = "Draft"
        new_doc.alert_sent = 0
        new_doc.set("interest_schedule", [])
        new_doc.insert()
        frappe.msgprint(_("New Term Deposit {0} created").format(new_doc.name), alert=True)
        return new_doc.name
