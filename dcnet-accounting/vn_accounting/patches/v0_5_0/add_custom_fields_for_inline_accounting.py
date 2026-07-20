"""Ensure inline-accounting Custom Fields are live + fix TK 2412/2413 account_type.

1. Calls reload_doctype so Frappe rebuilds meta cache for doctypes that received
   Custom Fields in Phase 2/3 (Asset Repair) and Phase 4 (CCDC Allocation Entry).

2. Changes account_type of TK 2412 (XDCB) and TK 2413 (Sửa chữa lớn TSCĐ)
   from "Capital Work in Progress" → "" (blank). ERPNext prevents Journal Entry
   from posting to CWIP accounts, but TT99/2025 requires D 2413 / C 331 for
   capitalized-repair JEs. Removing the CWIP type allows JE while preserving
   correct account classification in the COA.

Idempotent: reload_doctype is safe to call repeatedly; account_type update only
runs when the value differs.
"""
from __future__ import annotations

import frappe


def _clear_cwip_for_vn_accounts() -> None:
    """Remove CWIP account_type from TK 2412 and 2413 in all companies."""
    accounts = frappe.db.get_all(
        "Account",
        filters={"account_number": ["in", ["2412", "2413"]], "account_type": "Capital Work in Progress", "is_group": 0},
        fields=["name"],
    )
    for acc in accounts:
        frappe.db.set_value("Account", acc.name, "account_type", "", update_modified=False)


def execute() -> None:
    if frappe.db.exists("DocType", "Asset Repair"):
        frappe.reload_doctype("Asset Repair", force=True)
    if frappe.db.exists("DocType", "CCDC Allocation Entry"):
        frappe.reload_doctype("CCDC Allocation Entry", force=True)
    _clear_cwip_for_vn_accounts()
    frappe.db.commit()
