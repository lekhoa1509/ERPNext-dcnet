"""Blank dangling Account links on the VN Accounting Settings Single.

VN Accounting Settings is a Single shared by the project-costing seed
(`setup/company_defaults.py`) and the period-closing seed
(`period_closing/seed.py`). The project-costing seed's "first company wins"
logic can leave a Link field (e.g. `wip_account_project_costing`) pointing at
an Account whose company COA was later removed. That dangling link makes ANY
`save()` of the Single throw `LinkValidationError` — both in `after_migrate`
(which aborts migrate for the whole site) and on any UI save of Settings.

The seed guard (period_closing/seed.py, ignore_links=True) stops migrate from
being blocked. This patch heals the stored data so UI saves work too: it blanks
every top-level Account Link on the Single whose target no longer exists. The
next `Company.on_update` re-seeds the field with the current company's account.

Uses frappe.db directly (not doc.save) so healing itself doesn't re-trigger
_validate_links. Idempotent: re-running finds nothing once cleaned.
"""

import frappe

DOCTYPE = "VN Accounting Settings"


def execute():
    meta = frappe.get_meta(DOCTYPE)
    account_fields = [
        f.fieldname
        for f in meta.fields
        if f.fieldtype == "Link" and f.options == "Account"
    ]

    cleared = []
    for field in account_fields:
        value = frappe.db.get_single_value(DOCTYPE, field)
        if value and not frappe.db.exists("Account", value):
            frappe.db.set_single_value(DOCTYPE, field, None)
            cleared.append(f"{field}={value}")

    if cleared:
        frappe.db.commit()

    print(
        f"[clear_dangling_settings_account_links] cleared {len(cleared)} "
        f"dangling link(s): {', '.join(cleared) or '-'}"
    )
