"""Link query filters for Asset Depreciation Schedule form."""
from __future__ import annotations

import frappe


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def assets_without_schedule(doctype, txt, searchfield, start, page_len, filters):
	"""Return assets that don't yet have a submitted Asset Depreciation Schedule.

	Used by the asset Link field on Asset Depreciation Schedule new-form so users
	only pick assets still pending depreciation setup. Assets with draft schedules
	are still selectable so users can replace them.
	"""
	conditions = ["a.docstatus = 1"]
	values = {"txt": f"%{txt or ''}%", "start": start, "page_len": page_len}

	if filters and isinstance(filters, dict):
		if filters.get("company"):
			conditions.append("a.company = %(company)s")
			values["company"] = filters["company"]

	where = " AND ".join(conditions)
	return frappe.db.sql(
		f"""
		SELECT a.name, a.asset_name, a.company
		FROM `tabAsset` a
		WHERE {where}
		  AND NOT EXISTS (
		      SELECT 1 FROM `tabAsset Depreciation Schedule` ads
		      WHERE ads.asset = a.name AND ads.docstatus = 1
		  )
		  AND (a.{searchfield} LIKE %(txt)s OR a.asset_name LIKE %(txt)s)
		ORDER BY a.name
		LIMIT %(start)s, %(page_len)s
		""",
		values,
	)
