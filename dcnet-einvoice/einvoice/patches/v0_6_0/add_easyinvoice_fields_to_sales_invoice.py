import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from einvoice.einvoice.install import CUSTOM_FIELDS


def execute():
    # Force schema sync first per ~/.claude/rules/multi-session.md rule #15
    frappe.reload_doc("einvoice", "doctype", "einvoice_provider")
    frappe.reload_doc("einvoice", "doctype", "einvoice_issuance_log")
    # Idempotent: create_custom_fields update=True chỉ tạo mới hoặc update,
    # không duplicate.
    only_si = {"Sales Invoice": CUSTOM_FIELDS["Sales Invoice"]}
    create_custom_fields(only_si, update=True)
    frappe.db.commit()
