import frappe


def execute():
    """Extend Journal Entry naming_series options with PT-.YYYY.- (Phiếu thu) and PC-.YYYY.- (Phiếu chi)."""
    name = "Journal Entry-naming_series-options"
    desired = "PT-.YYYY.-\nPC-.YYYY.-\nACC-JV-.YYYY.-"
    if frappe.db.exists("Property Setter", name):
        existing = frappe.db.get_value("Property Setter", name, "value") or ""
        if "PT-.YYYY.-" in existing and "PC-.YYYY.-" in existing:
            return
        new_value = "PT-.YYYY.-\nPC-.YYYY.-\n" + existing.lstrip("\n")
        frappe.db.set_value("Property Setter", name, "value", new_value)
        return
    frappe.get_doc({
        "doctype": "Property Setter",
        "name": name,
        "doc_type": "Journal Entry",
        "field_name": "naming_series",
        "property": "options",
        "property_type": "Text",
        "value": desired,
        "doctype_or_field": "DocField",
    }).insert(ignore_permissions=True)
