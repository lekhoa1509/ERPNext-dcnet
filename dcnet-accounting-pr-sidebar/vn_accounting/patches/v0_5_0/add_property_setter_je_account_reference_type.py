"""Extend Journal Entry Account.reference_type Select options to include
Asset Repair, CCDC Item, CCDC Writeoff, CCDC Allocation Schedule.

Idempotent: skip if Property Setter already exists with the merged options
that include all four custom doctypes.
"""
from __future__ import annotations

import frappe

PROPERTY_SETTER_NAME_PREFIX = "Journal Entry Account-reference_type-options"
EXTRA_OPTIONS = ["Asset Repair", "CCDC Item", "CCDC Writeoff", "CCDC Allocation Schedule"]


def execute() -> None:
    # Read default options from JE Account meta
    meta = frappe.get_meta("Journal Entry Account")
    field = meta.get_field("reference_type")
    if not field:
        return  # JE Account schema unexpectedly missing the field; abort silently

    current_options = (field.options or "").split("\n")
    merged = list(current_options)
    changed = False
    for opt in EXTRA_OPTIONS:
        if opt not in merged:
            merged.append(opt)
            changed = True

    if not changed:
        return

    # Look for an existing Property Setter that already adjusts options
    ps_name = frappe.db.get_value(
        "Property Setter",
        {
            "doc_type": "Journal Entry Account",
            "field_name": "reference_type",
            "property": "options",
        },
        "name",
    )

    options_str = "\n".join(merged)
    if ps_name:
        frappe.db.set_value("Property Setter", ps_name, "value", options_str, update_modified=False)
    else:
        ps = frappe.get_doc({
            "doctype": "Property Setter",
            "doctype_or_field": "DocField",
            "doc_type": "Journal Entry Account",
            "field_name": "reference_type",
            "property": "options",
            "property_type": "Text",
            "value": options_str,
        })
        ps.flags.ignore_permissions = True
        ps.insert()
    frappe.db.commit()
