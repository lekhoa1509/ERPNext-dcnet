"""Copy capitalization_je → posted_je for Asset Repairs where posted_je is null.

Handles records created before v0.5.0 that used the old capitalization_je field.
Idempotent: only copies where posted_je IS NULL AND capitalization_je IS NOT NULL.
"""
from __future__ import annotations

import frappe


def execute() -> None:
    if not frappe.db.exists("DocType", "Asset Repair"):
        return

    # Check capitalization_je column exists (custom field added in Phase 1)
    columns = [col[0] for col in frappe.db.sql("SHOW COLUMNS FROM `tabAsset Repair` LIKE 'capitalization_je'")]
    if not columns:
        return

    frappe.db.sql(
        """UPDATE `tabAsset Repair`
           SET posted_je = capitalization_je
           WHERE (posted_je IS NULL OR posted_je = '')
             AND capitalization_je IS NOT NULL
             AND capitalization_je != ''""",
    )
    frappe.db.commit()
