"""Journal Entry hooks for treasury — update schedule row status and outstanding."""
from __future__ import annotations

import frappe


def on_je_submit(doc, method):
    """When a JE is submitted, mark linked schedule rows as Booked."""
    _update_linked_rows(doc.name, "Booked")
    _update_cash_count_on_je(doc.name, submitted=True)


def on_je_cancel(doc, method):
    """When a JE is cancelled, revert linked schedule rows to Draft Created."""
    _update_linked_rows(doc.name, "Draft Created")
    _update_cash_count_on_je(doc.name, submitted=False)


def _update_linked_rows(je_name: str, new_status: str):
    """Find Term Deposit Interest / Bank Loan Repayment rows linked to this JE."""
    # Term Deposit Interest rows
    td_rows = frappe.get_all(
        "Term Deposit Interest",
        filters={"journal_entry": je_name},
        fields=["name", "parent"],
    )
    for row in td_rows:
        frappe.db.set_value("Term Deposit Interest", row.name, "status", new_status, update_modified=False)

    # Bank Loan Repayment rows
    bl_rows = frappe.get_all(
        "Bank Loan Repayment",
        filters={"journal_entry": je_name},
        fields=["name", "parent"],
    )
    parents_to_update = set()
    for row in bl_rows:
        frappe.db.set_value("Bank Loan Repayment", row.name, "status", new_status, update_modified=False)
        parents_to_update.add(row.parent)

    # Recalculate outstanding_amount for affected Bank Loans
    for loan_name in parents_to_update:
        _recalc_outstanding(loan_name)


def _update_cash_count_on_je(je_name: str, submitted: bool):
    """Update Cash Count status when linked pending_je or resolution_je is submitted/cancelled."""
    # Check pending_je link
    cc_pending = frappe.db.get_value("Cash Count", {"pending_je": je_name}, "name")
    if cc_pending:
        if submitted:
            frappe.db.set_value("Cash Count", cc_pending, "status", "Pending Resolution", update_modified=False)
        else:
            frappe.db.set_value("Cash Count", cc_pending, "status", "Approved", update_modified=False)

    # Check resolution_je link
    cc_resolution = frappe.db.get_value("Cash Count", {"resolution_je": je_name}, "name")
    if cc_resolution:
        if submitted:
            frappe.db.set_value("Cash Count", cc_resolution, {
                "status": "Resolved",
                "resolution_status": "Resolved",
            }, update_modified=False)
        else:
            frappe.db.set_value("Cash Count", cc_resolution, {
                "status": "Pending Resolution",
                "resolution_status": "Pending",
            }, update_modified=False)


def _recalc_outstanding(loan_name: str):
    """Recalculate outstanding_amount from Booked repayment rows."""
    loan = frappe.get_doc("Bank Loan", loan_name)
    booked_principal = sum(
        r.principal_amount for r in loan.repayment_schedule if r.status == "Booked"
    )
    outstanding = loan.loan_amount - booked_principal
    frappe.db.set_value("Bank Loan", loan_name, "outstanding_amount", outstanding, update_modified=False)
