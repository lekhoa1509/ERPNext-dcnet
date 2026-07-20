"""
Migrate legacy `auth_method` field on EInvoice Provider to per-direction toggles.

v0.4.0: Provider DocType replaces single `auth_method` Select with two
checkboxes (`enable_inward` / `enable_outward`) + per-direction Selects
(`inward_auth_method` / `outward_auth_method`). Same provider can now expose
both directions with different auth schemes (Mắt Bão: inward=Token,
outward=Username-Password).

Migration rules:
    auth_method='Token'             → enable_inward=1, inward_auth_method='Token'
    auth_method='Username-Password' → enable_outward=1, outward_auth_method='Username-Password'
    auth_method='API Key'           → enable_inward=1, inward_auth_method='API Key'
    auth_method=NULL/empty          → enable_inward=1, inward_auth_method='Token'  (Frappe default)

Idempotent: re-runs do nothing if `enable_inward` or `enable_outward` already set.
"""

import frappe


def execute():
    # Force schema sync so the new fields exist before we backfill.
    frappe.reload_doc("einvoice", "doctype", "einvoice_provider")

    if not frappe.db.has_column("EInvoice Provider", "auth_method"):
        return
    if not frappe.db.has_column("EInvoice Provider", "enable_inward"):
        return

    rows = frappe.db.sql(
        """
        SELECT name, auth_method, enable_inward, enable_outward
          FROM `tabEInvoice Provider`
        """,
        as_dict=True,
    )

    migrated = 0
    for r in rows:
        if r.enable_inward or r.enable_outward:
            continue

        method = (r.auth_method or "Token").strip()

        if method == "Username-Password":
            frappe.db.set_value(
                "EInvoice Provider", r.name,
                {
                    "enable_outward": 1,
                    "outward_auth_method": "Username-Password",
                },
                update_modified=False,
            )
        elif method == "API Key":
            frappe.db.set_value(
                "EInvoice Provider", r.name,
                {
                    "enable_inward": 1,
                    "inward_auth_method": "API Key",
                },
                update_modified=False,
            )
        else:
            # Token (or unknown) → default to inward
            frappe.db.set_value(
                "EInvoice Provider", r.name,
                {
                    "enable_inward": 1,
                    "inward_auth_method": "Token",
                },
                update_modified=False,
            )
        migrated += 1

    frappe.db.commit()
    if migrated:
        print(f"[einvoice] Migrated {migrated} EInvoice Provider record(s) to inward/outward toggles.")
