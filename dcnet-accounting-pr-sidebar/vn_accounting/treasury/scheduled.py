"""Daily scheduled job for treasury operations.

Processes due interest/repayment rows, updates maturity status, sends alerts.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import today, add_days, getdate


def process_treasury_schedules():
    """Main entry point — called daily by scheduler."""
    _process_deposit_interest()
    _process_loan_repayments()
    _check_deposit_maturity()
    _check_loan_maturity()
    _send_maturity_alerts()


def _process_deposit_interest():
    """Create draft JEs for due deposit interest rows."""
    from vn_accounting.treasury.journal_entry_builder import create_interest_je

    deposits = frappe.get_all(
        "Term Deposit",
        filters={"status": "Active", "docstatus": 1},
        pluck="name",
    )
    for name in deposits:
        doc = frappe.get_doc("Term Deposit", name)
        for row in doc.interest_schedule:
            if row.status == "Pending" and str(row.due_date) <= today():
                je_name = create_interest_je(doc, row)
                frappe.db.set_value(
                    "Term Deposit Interest", row.name,
                    {"status": "Draft Created", "journal_entry": je_name},
                    update_modified=False,
                )
        frappe.db.commit()


def _process_loan_repayments():
    """Create draft JEs for due loan repayment rows."""
    from vn_accounting.treasury.journal_entry_builder import create_repayment_je

    loans = frappe.get_all(
        "Bank Loan",
        filters={"status": "Active", "docstatus": 1},
        pluck="name",
    )
    for name in loans:
        doc = frappe.get_doc("Bank Loan", name)
        for row in doc.repayment_schedule:
            if row.status == "Pending" and str(row.due_date) <= today():
                je_name = create_repayment_je(doc, row)
                frappe.db.set_value(
                    "Bank Loan Repayment", row.name,
                    {"status": "Draft Created", "journal_entry": je_name},
                    update_modified=False,
                )
        frappe.db.commit()


def _check_deposit_maturity():
    """Move Active deposits past maturity to Matured status."""
    from vn_accounting.treasury.journal_entry_builder import create_settlement_je

    deposits = frappe.get_all(
        "Term Deposit",
        filters={"status": "Active", "docstatus": 1, "maturity_date": ["<=", today()]},
        pluck="name",
    )
    for name in deposits:
        doc = frappe.get_doc("Term Deposit", name)
        frappe.db.set_value("Term Deposit", name, "status", "Matured", update_modified=False)
        # For End of Term type: create settlement JE with interest
        if doc.interest_type == "End of Term":
            create_settlement_je(doc)
        frappe.db.commit()


def _check_loan_maturity():
    """Check if all repayments are booked → mark Settled."""
    loans = frappe.get_all(
        "Bank Loan",
        filters={"status": "Active", "docstatus": 1},
        pluck="name",
    )
    for name in loans:
        doc = frappe.get_doc("Bank Loan", name)
        all_booked = all(r.status == "Booked" for r in doc.repayment_schedule)
        if all_booked and doc.repayment_schedule:
            frappe.db.set_value("Bank Loan", name, {"status": "Settled", "outstanding_amount": 0}, update_modified=False)
            frappe.db.commit()


def _send_maturity_alerts():
    """Send Notification Log for deposits/loans approaching maturity."""
    settings = frappe.get_doc("VN Accounting Settings")

    # Deposit alerts
    deposit_alert_days = settings.deposit_alert_days or 7
    alert_date = add_days(today(), deposit_alert_days)
    deposits = frappe.get_all(
        "Term Deposit",
        filters={
            "status": "Active",
            "docstatus": 1,
            "maturity_date": ["<=", alert_date],
            "alert_sent": 0,
        },
        fields=["name", "maturity_date", "principal_amount", "bank"],
    )
    for d in deposits:
        _create_alert(
            _("Term Deposit {0} maturing on {1}").format(d.name, d.maturity_date),
            _("Term Deposit {0} ({1}) with principal {2:,.0f} VND matures on {3}.").format(
                d.name, d.bank, d.principal_amount, d.maturity_date),
            "Term Deposit", d.name,
        )
        frappe.db.set_value("Term Deposit", d.name, "alert_sent", 1, update_modified=False)

    # Loan alerts
    loan_alert_days = settings.loan_alert_days or 7
    alert_date = add_days(today(), loan_alert_days)
    loans = frappe.get_all(
        "Bank Loan",
        filters={
            "status": "Active",
            "docstatus": 1,
            "maturity_date": ["<=", alert_date],
            "alert_sent": 0,
        },
        fields=["name", "maturity_date", "loan_amount", "bank"],
    )
    for ln in loans:
        _create_alert(
            _("Bank Loan {0} maturing on {1}").format(ln.name, ln.maturity_date),
            _("Bank Loan {0} ({1}) with amount {2:,.0f} VND matures on {3}.").format(
                ln.name, ln.bank, ln.loan_amount, ln.maturity_date),
            "Bank Loan", ln.name,
        )
        frappe.db.set_value("Bank Loan", ln.name, "alert_sent", 1, update_modified=False)

    frappe.db.commit()


def _create_alert(subject: str, message: str, ref_doctype: str, ref_name: str):
    """Create Notification Log for Accounts Manager users."""
    users = frappe.get_all(
        "Has Role",
        filters={"role": "Accounts Manager", "parenttype": "User"},
        pluck="parent",
    )
    for user in set(users):
        if not frappe.db.exists("User", {"name": user, "enabled": 1}):
            continue
        frappe.get_doc({
            "doctype": "Notification Log",
            "for_user": user,
            "type": "Alert",
            "document_type": ref_doctype,
            "document_name": ref_name,
            "subject": subject,
            "email_content": message,
        }).insert(ignore_permissions=True)
