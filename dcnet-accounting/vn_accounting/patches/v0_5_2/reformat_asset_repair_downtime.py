"""Reformat `Asset Repair.downtime` from raw float to "<hours> Hrs" string.

The original v0_5_0 backfill stored values like "72.0" / "192.0". The field is
Data type, so the value renders verbatim — confusing without unit suffix.
ERPNext's UI handler stores values as "<int> Hrs" (see asset_repair.js
`get_downtime` callback).

This patch normalizes existing values:
  - "72.0"   → "72 Hrs"
  - "192"    → "192 Hrs"
  - "8 Hrs"  → "8 Hrs"  (no-op)
  - empty / NULL → leave as-is

Idempotent: skips values that already contain "Hrs".
"""
from __future__ import annotations

import re

import frappe


def _format_downtime(raw: str | float | None) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    if "Hrs" in s or "Hr" in s:
        return None  # already formatted
    # Try parse as number → strip ".0" suffix → append " Hrs"
    try:
        f = float(s)
        as_int = int(f)
        if abs(f - as_int) < 1e-6:
            return f"{as_int} Hrs"
        return f"{f} Hrs"
    except ValueError:
        return None  # not numeric, leave alone


def execute() -> None:
    rows = frappe.db.sql(
        """SELECT name, downtime FROM `tabAsset Repair`
           WHERE downtime IS NOT NULL AND downtime != ''""",
        as_dict=True,
    )
    fixed = 0
    for r in rows:
        new_value = _format_downtime(r.downtime)
        if new_value and new_value != r.downtime:
            frappe.db.set_value(
                "Asset Repair", r.name, "downtime", new_value, update_modified=False
            )
            fixed += 1
    if fixed:
        frappe.db.commit()
        print(f"v0_5_2: reformatted {fixed} Asset Repair downtime values")
