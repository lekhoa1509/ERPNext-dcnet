"""Shadow Sales Order — auto-created for One-off VTTB contracts.

Contract is the master. SO is read-only and hidden from non-admin users.
Sync direction: Contract → SO only.
"""

import frappe
from frappe import _


def create_shadow_so(contract):
    """Create a shadow Sales Order from the submitted Contract.

    Called from DCNetContract.on_submit() when contract_type == "One-off"
    and service_type == "VTTB".
    """
    if not _should_create_shadow_so(contract):
        return

    so = frappe.new_doc("Sales Order")
    so.customer = contract.customer
    so.company = contract.company
    so.transaction_date = contract.contract_date
    so.delivery_date = contract.acceptance_date
    so.currency = contract.currency or "VND"
    so.conversion_rate = 1
    so.order_type = "Sales"

    # Custom field to mark this as a shadow SO
    so.is_shadow_contract = 1

    for item in contract.items:
        if not item.erpnext_item:
            continue
        so.append("items", {
            "item_code": item.erpnext_item,
            "qty": item.qty or 1,
            "rate": item.unit_price or 0,
            "uom": item.uom or "Nos",
            "description": item.description or item.item_label,
            "delivery_date": contract.acceptance_date,
            "conversion_factor": 1,
        })

    if not so.items:
        return

    so.flags.ignore_permissions = True
    so.run_method("set_missing_values")
    so.insert()
    so.submit()

    # Link back to contract
    frappe.db.set_value(
        "DCNet Contract", contract.name,
        "shadow_sales_order", so.name,
        update_modified=False,
    )
    contract.shadow_sales_order = so.name


def cancel_shadow_so(contract):
    """Cancel the shadow SO when the contract is cancelled."""
    if not contract.shadow_sales_order:
        return

    so_name = contract.shadow_sales_order
    if not frappe.db.exists("Sales Order", so_name):
        return

    so = frappe.get_doc("Sales Order", so_name)
    if so.docstatus == 1:
        so.flags.ignore_permissions = True
        so.cancel()


def _should_create_shadow_so(contract):
    """Only VTTB one-off contracts get shadow SOs."""
    return (
        contract.contract_type == "One-off"
        and contract.service_type == "VTTB"
    )
