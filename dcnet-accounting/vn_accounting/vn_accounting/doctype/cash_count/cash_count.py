# Copyright (c) 2026, DCNet and Contributors
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days

from vn_accounting.vn_accounting.report_utils import get_opening_balance


class CashCount(Document):
    def validate(self):
        # Once a difference JE is created, do not recalculate — the difference is locked
        if self.status in ("Pending Resolution", "Resolved"):
            self._save_defaults()
            return
        self._recalc_book_balance()
        self._recalc_denominations()
        self._calc_difference()
        self._auto_fill_difference_account()
        self._auto_set_resolution_status()
        self._save_defaults()

    def _recalc_book_balance(self):
        if self.cash_account and self.count_date and self.company:
            # get_opening_balance sums GL before from_date, so pass day after count_date
            self.book_balance = get_opening_balance(
                [self.cash_account], add_days(self.count_date, 1), self.company
            )

    def _recalc_denominations(self):
        if self.show_denomination and self.denominations:
            total = 0
            for row in self.denominations:
                row.amount = (row.denomination or 0) * (row.quantity or 0)
                total += row.amount
            self.actual_amount = total

    def _calc_difference(self):
        self.difference = (self.actual_amount or 0) - (self.book_balance or 0)
        if self.difference == 0:
            self.difference_type = "Balanced"
        elif self.difference > 0:
            self.difference_type = "Surplus"
        else:
            self.difference_type = "Deficit"

    def _auto_fill_difference_account(self):
        if not self.difference_type or self.difference_type == "Balanced":
            if not self.difference_account:
                return
            return

        if self.difference_account:
            return  # user already chose

        from vn_accounting.utils.account_resolver import resolve_account
        company = self.company
        if not company:
            return
        if self.difference_type == "Surplus":
            self.difference_account = resolve_account("cash_surplus_account", company)
        elif self.difference_type == "Deficit":
            self.difference_account = resolve_account("cash_deficit_account", company)

    def _auto_set_resolution_status(self):
        if self.difference_type == "Balanced":
            self.resolution_status = "Not Applicable"
        elif not self.resolution_status or self.resolution_status == "Not Applicable":
            self.resolution_status = "Pending"

    def _save_defaults(self):
        if not self.save_as_default or not self.difference_account:
            return
        settings = _get_settings()
        if self.difference_type == "Surplus":
            frappe.db.set_value("VN Accounting Settings", None, "cash_surplus_account",
                                self.difference_account, update_modified=False)
        elif self.difference_type == "Deficit":
            frappe.db.set_value("VN Accounting Settings", None, "cash_deficit_account",
                                self.difference_account, update_modified=False)

    @frappe.whitelist()
    def mark_counted(self):
        if self.status != "Draft":
            frappe.throw(_("Can only mark as Counted from Draft status"))
        if not self.cashier:
            frappe.throw(_("Cashier is required to mark as Counted"))
        self.db_set("status", "Counted")

    @frappe.whitelist()
    def approve(self):
        if self.status != "Counted":
            frappe.throw(_("Can only approve from Counted status"))
        if not self.chief_accountant or not self.director:
            frappe.throw(_("Chief Accountant and Director are required to approve"))
        if self.difference == 0:
            self.db_set("status", "Closed")
        else:
            self.db_set("status", "Approved")

    @frappe.whitelist()
    def record_difference(self):
        if self.status != "Approved":
            frappe.throw(_("Can only record difference from Approved status"))
        if self.difference == 0:
            frappe.throw(_("No difference to record"))
        if not self.difference_account:
            frappe.throw(_("Difference Account is required"))

        je_name = _create_step1_je(self)
        self.db_set("pending_je", je_name)
        frappe.msgprint(_("Draft Journal Entry {0} created").format(je_name), alert=True)
        return je_name

    @frappe.whitelist()
    def resolve_difference(self):
        if self.status != "Pending Resolution":
            frappe.throw(_("Can only resolve from Pending Resolution status"))
        if not self.resolution_type:
            frappe.throw(_("Resolution Type is required"))
        if not self.resolution_target_account:
            frappe.throw(_("Resolution Target Account is required"))

        je_name = _create_step2_je(self)
        self.db_set("resolution_je", je_name)
        frappe.msgprint(_("Draft Resolution Journal Entry {0} created").format(je_name), alert=True)
        return je_name


@frappe.whitelist()
def get_book_balance(cash_account, count_date, company):
    """Get GL balance for a cash account up to count_date."""
    balance = get_opening_balance(
        [cash_account], add_days(count_date, 1), company
    )
    return balance


def _get_settings():
    if frappe.db.exists("DocType", "VN Accounting Settings"):
        return frappe.get_doc("VN Accounting Settings")
    return frappe._dict()


def _create_step1_je(doc):
    """Step 1 JE: record difference to pending account (1381/3381)."""
    cost_center = frappe.db.get_value("Company", doc.company, "cost_center")
    abs_diff = abs(doc.difference)

    if doc.difference_type == "Deficit":
        accounts = [
            {"account": doc.difference_account, "debit_in_account_currency": abs_diff, "cost_center": cost_center},
            {"account": doc.cash_account, "credit_in_account_currency": abs_diff, "cost_center": cost_center},
        ]
    else:  # Surplus
        accounts = [
            {"account": doc.cash_account, "debit_in_account_currency": abs_diff, "cost_center": cost_center},
            {"account": doc.difference_account, "credit_in_account_currency": abs_diff, "cost_center": cost_center},
        ]

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Cash Entry",
        "company": doc.company,
        "posting_date": doc.count_date,
        "user_remark": f"Cash count {doc.name} — {doc.difference_type} {abs_diff}",
        "accounts": accounts,
    })
    je.flags.ignore_permissions = True
    je.insert()
    frappe.db.commit()
    return je.name


def _create_step2_je(doc):
    """Step 2 JE: resolve difference based on resolution_type."""
    cost_center = frappe.db.get_value("Company", doc.company, "cost_center")
    abs_diff = abs(doc.difference)

    if doc.difference_type == "Deficit":
        # 1381 is credit side (closing pending), target is debit
        accounts = [
            {"account": doc.resolution_target_account, "debit_in_account_currency": abs_diff, "cost_center": cost_center},
            {"account": doc.difference_account, "credit_in_account_currency": abs_diff, "cost_center": cost_center},
        ]
    else:  # Surplus
        # 3381 is debit side (closing pending), target is credit
        accounts = [
            {"account": doc.difference_account, "debit_in_account_currency": abs_diff, "cost_center": cost_center},
            {"account": doc.resolution_target_account, "credit_in_account_currency": abs_diff, "cost_center": cost_center},
        ]

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Cash Entry",
        "company": doc.company,
        "posting_date": doc.count_date,
        "user_remark": f"Cash count {doc.name} — Resolution: {doc.resolution_type}",
        "accounts": accounts,
    })
    je.flags.ignore_permissions = True
    je.insert()
    frappe.db.commit()
    return je.name
