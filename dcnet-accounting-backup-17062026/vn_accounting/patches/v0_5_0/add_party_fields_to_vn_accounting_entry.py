"""Add party_type + party fields to VN Accounting Entry child DocType.

Frappe silently drops unknown fields when child rows are appended via
`parent.append("table", row_dict)`. The seeder + helpers were trying to
attach `party_type`/`party` to entries (needed for TK 331 Payable
validation), but those fields didn't exist on the child schema → values
dropped → JE creation failed validation → on_submit rolled back → AR
submitted with `posted_je=NULL`.

This patch reloads the DocType to pick up the new fields from JSON.
After this patch + bench migrate, the seeder's party logic actually
takes effect.

Idempotent: `frappe.reload_doc` is safe to re-run.
"""
from __future__ import annotations

import frappe


def execute() -> None:
    if not frappe.db.exists("DocType", "VN Accounting Entry"):
        return
    frappe.reload_doc("vn_accounting", "doctype", "vn_accounting_entry")
    frappe.db.commit()
