"""Purchase Invoice hooks for auto-creating CCDC Items."""
from __future__ import annotations

import frappe


def on_purchase_invoice_submit(doc, method=None):
    """Auto-create draft CCDC Item for each line with is_low_value_asset=1."""
    # TIER 1 PERF: short-circuit during Misa migration
    if getattr(frappe.flags, "misa_migration_active", False):
        return
    created = []
    for item in doc.items:
        if item.get("is_low_value_asset"):
            from vn_accounting.asset.ccdc_item_factory import auto_create_ccdc_item
            name = auto_create_ccdc_item(doc, item)
            if name:
                created.append(name)

    if created:
        frappe.msgprint(
            "Đã tạo {0} CCDC Item: {1}".format(len(created), ", ".join(created)),
            alert=True,
        )
