"""Set expense_account = 6423 for CCDC Items with null expense_account.

Idempotent: only updates rows where expense_account IS NULL.
Uses parameterized SQL to avoid f-string injection.
"""
from __future__ import annotations

import frappe


def execute() -> None:
    if not frappe.db.exists("DocType", "CCDC Item"):
        return

    companies = frappe.db.sql_list("SELECT DISTINCT company FROM `tabCCDC Item` WHERE expense_account IS NULL OR expense_account = ''")
    if not companies:
        return

    for company in companies:
        account_name = frappe.db.get_value(
            "Account",
            {"company": company, "account_number": "6423", "is_group": 0},
            "name",
        )
        if not account_name:
            continue

        frappe.db.sql(
            "UPDATE `tabCCDC Item` SET expense_account = %s WHERE company = %s AND (expense_account IS NULL OR expense_account = '')",
            (account_name, company),
        )

    frappe.db.commit()
