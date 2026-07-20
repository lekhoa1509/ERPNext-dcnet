"""Permission query conditions for shadow Sales Orders.

Shadow SOs (is_shadow_contract=1) are hidden from non-admin users in list view.
"""

import frappe


def so_permission_query(user=None):
    """Hide shadow Sales Orders from non-admin users."""
    if not user:
        user = frappe.session.user

    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return ""

    return "`tabSales Order`.is_shadow_contract = 0 OR `tabSales Order`.is_shadow_contract IS NULL"
