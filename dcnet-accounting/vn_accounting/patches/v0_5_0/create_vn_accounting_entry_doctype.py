"""Reload VN Accounting Entry child DocType so it's available for fixtures
and Custom Field Table options before subsequent patches run.

Idempotent: frappe.reload_doctype is safe to call repeatedly.
"""
from __future__ import annotations

import frappe


def execute() -> None:
    if frappe.db.exists("DocType", "VN Accounting Entry"):
        # Schema already in DB — make sure Frappe re-reads the JSON in case
        # fields evolved.
        frappe.reload_doctype("VN Accounting Entry", force=True)
    else:
        # Trigger import from JSON via reload_doc
        frappe.reload_doc("vn_accounting", "doctype", "vn_accounting_entry", force=True)
    frappe.db.commit()
