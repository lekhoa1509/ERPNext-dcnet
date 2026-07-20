"""Hide Asset Repair.capitalize_repair_cost and force its default to 0.

Why: ERPNext's `AssetRepair.on_submit` posts a GL entry only when
`capitalize_repair_cost=1`. vn_accounting posts via its own JE under
`Asset Repair → on_submit`. Hiding the field + defaulting to 0 prevents
double-posting.

Idempotent: only writes Property Setter if missing or value differs.
"""
from __future__ import annotations

import frappe

ASSET_REPAIR = "Asset Repair"
FIELD = "capitalize_repair_cost"


def _ensure_ps(field_name: str, prop: str, value: str, prop_type: str = "Check") -> None:
    existing = frappe.db.get_value(
        "Property Setter",
        {"doc_type": ASSET_REPAIR, "field_name": field_name, "property": prop},
        "name",
    )
    if existing:
        cur = frappe.db.get_value("Property Setter", existing, "value")
        if cur == value:
            return
        frappe.db.set_value("Property Setter", existing, "value", value, update_modified=False)
        return
    ps = frappe.get_doc({
        "doctype": "Property Setter",
        "doctype_or_field": "DocField",
        "doc_type": ASSET_REPAIR,
        "field_name": field_name,
        "property": prop,
        "property_type": prop_type,
        "value": value,
    })
    ps.flags.ignore_permissions = True
    ps.insert()


def execute() -> None:
    if not frappe.db.exists("DocType", ASSET_REPAIR):
        return
    _ensure_ps(FIELD, "hidden", "1", prop_type="Check")
    _ensure_ps(FIELD, "default", "0", prop_type="Text")
    frappe.db.commit()
