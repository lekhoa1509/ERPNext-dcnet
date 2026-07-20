"""Fill downtime for Asset Repair records that have both dates but null downtime.

Uses frappe.utils.time_diff_in_hours (same as ERPNext get_downtime).
Idempotent: WHERE clause limits to downtime IS NULL rows only.
"""
from __future__ import annotations

import frappe
from frappe.utils import time_diff_in_hours


def execute() -> None:
    if not frappe.db.exists("DocType", "Asset Repair"):
        return

    rows = frappe.db.sql(
        """SELECT name, failure_date, completion_date
           FROM `tabAsset Repair`
           WHERE failure_date IS NOT NULL
             AND completion_date IS NOT NULL
             AND (downtime IS NULL OR downtime = '')""",
        as_dict=True,
    )

    for row in rows:
        downtime = round(time_diff_in_hours(str(row.completion_date), str(row.failure_date)), 2)
        frappe.db.set_value("Asset Repair", row.name, "downtime", downtime, update_modified=False)

    if rows:
        frappe.db.commit()
