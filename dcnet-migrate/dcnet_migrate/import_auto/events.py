import frappe


def ensure_employee_designation(doc, method=None):
    """Auto-create Designation during migration if it doesn't exist yet."""
    if not doc.designation:
        return
    if frappe.db.exists("Designation", doc.designation):
        return
    try:
        frappe.get_doc({
            "doctype": "Designation",
            "designation_name": doc.designation,
        }).insert(ignore_permissions=True, ignore_if_duplicate=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Auto-create Designation: {doc.designation}")
