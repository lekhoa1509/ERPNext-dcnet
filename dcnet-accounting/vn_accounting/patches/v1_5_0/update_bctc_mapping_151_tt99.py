"""Update existing BCTC Mapping rows for mã 151 from TK 142 → TK 242.

TT99/2025 (effective 2026-01-01) retired TK 142 and consolidated short +
long-term prepaid expenses into TK 242 "Chi phí chờ phân bổ". The
small_trade BCTC template was already updated (bctc_template_seed.py),
but mappings cloned to existing tenants before the template fix still
point at TK 142 — which has no balance under TT99/2025, so mã 151
silently reports 0 and breaks the B01 Mã 270 = Mã 440 equation by the
amount of any prepaid expense held in 242.

This patch updates each tenant's BCTC Mapping in place. Skipped if a
tenant has manually customised the formula to something other than the
exact "+142" token.
"""

import frappe


def execute():
    rows = frappe.db.sql(
        """
        SELECT name, parent, account_formula FROM `tabBCTC Line`
        WHERE parenttype = 'BCTC Mapping' AND parentfield = 'b01_lines'
          AND code = '151'
        """,
        as_dict=True,
    )

    updated = 0
    skipped = 0
    for r in rows:
        old = (r.account_formula or "").strip()
        if old == "+142":
            frappe.db.set_value(
                "BCTC Line", r.name, "account_formula", "+242",
                update_modified=False,
            )
            updated += 1
            print(f"  ✓ {r.parent}: mã 151 +142 → +242")
        else:
            skipped += 1
            if old and "242" not in old:
                print(f"  ⚠ {r.parent}: mã 151 customised ({old!r}) — not touching")

    if updated:
        frappe.db.commit()

    print(f"  Patched {updated} BCTC Mapping(s), skipped {skipped}.")
