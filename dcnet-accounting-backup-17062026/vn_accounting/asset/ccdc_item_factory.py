"""Auto-create CCDC Item from Purchase Invoice line items."""
from __future__ import annotations

import frappe


def auto_create_ccdc_item(pi_doc, pi_item) -> str | None:
    """Create a draft CCDC Item linked to a Purchase Invoice item.

    Returns the CCDC Item name, or None if already created.
    """
    existing = frappe.db.get_value(
        "CCDC Item",
        {"purchase_invoice": pi_doc.name, "purchase_invoice_item": pi_item.name},
        "name",
    )
    if existing:
        return existing

    ccdc = frappe.get_doc({
        "doctype": "CCDC Item",
        "item_code": pi_item.item_code,
        "item_name": pi_item.item_name,
        "company": pi_doc.company,
        "cost": pi_item.amount,
        "purchase_date": pi_doc.posting_date,
        "available_for_use_date": pi_doc.posting_date,
        "purchase_invoice": pi_doc.name,
        "purchase_invoice_item": pi_item.name,
        "status": "Mới mua",
        "scope_for_handover": "CCDC",
    })
    ccdc.flags.ignore_permissions = True
    ccdc.flags.ignore_mandatory = True
    ccdc.insert()
    frappe.db.commit()
    return ccdc.name
