"""Document event handlers for DCNet Contract integration."""

import frappe


def on_payment_entry_submit(doc, method):
    """When a Payment Entry is submitted, check if it pays a Sales Invoice linked to a billing schedule row.

    Transitions: Invoiced → Paid (only if SI fully paid).
    For Prepay contracts, all billing_schedule rows linked to the same SI flip together.
    """
    if doc.payment_type != "Receive":
        return

    # Find all SI references in this PE
    si_names = set()
    for ref in doc.references:
        if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
            si_names.add(ref.reference_name)

    if not si_names:
        return

    for si_name in si_names:
        _process_si_payment(si_name, doc.name)


def on_payment_entry_cancel(doc, method):
    """When a Payment Entry is cancelled, revert billing_schedule rows Paid → Invoiced."""
    if doc.payment_type != "Receive":
        return

    si_names = {
        ref.reference_name
        for ref in doc.references
        if ref.reference_doctype == "Sales Invoice" and ref.reference_name
    }
    if not si_names:
        return

    for si_name in si_names:
        bs_rows = frappe.get_all(
            "DCNet Contract Billing Schedule",
            filters={"sales_invoice": si_name, "state": "Paid", "payment_entry": doc.name},
            fields=["name"],
        )
        for row in bs_rows:
            frappe.db.set_value(
                "DCNet Contract Billing Schedule",
                row.name,
                {"state": "Invoiced", "payment_entry": None},
                update_modified=False,
            )


def _process_si_payment(si_name: str, pe_name: str):
    """Check if SI is fully paid, then update linked billing schedule rows."""
    try:
        si = frappe.get_doc("Sales Invoice", si_name)
    except frappe.DoesNotExistError:
        frappe.log_error(
            f"Sales Invoice {si_name} không tồn tại — bỏ qua xử lý billing schedule",
            "DCNet Contract PE Hook",
        )
        return

    # Don't flip to Paid if there's still outstanding
    if si.outstanding_amount > 0:
        return

    # Find billing schedule rows linked to this SI
    bs_rows = frappe.get_all(
        "DCNet Contract Billing Schedule",
        filters={"sales_invoice": si_name, "state": ["in", ["Invoiced", "Overdue"]]},
        fields=["name", "parent"],
    )

    if not bs_rows:
        return

    contract_names = set()
    for row in bs_rows:
        frappe.db.set_value(
            "DCNet Contract Billing Schedule",
            row.name,
            {"state": "Paid", "payment_entry": pe_name},
            update_modified=False,
        )
        contract_names.add(row.parent)

    # Fire event for each affected contract (for future PAKD integration)
    for contract_name in contract_names:
        frappe.publish_realtime(
            "dcnet_contract.billing_period_paid",
            {"contract": contract_name, "sales_invoice": si_name, "payment_entry": pe_name},
        )
