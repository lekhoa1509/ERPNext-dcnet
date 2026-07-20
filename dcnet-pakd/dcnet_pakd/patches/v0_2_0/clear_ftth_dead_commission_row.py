"""Remove the dead 100% Sales Commission row from FTTH rule template.

For Monthly FTTH Rollup PAKDs, engine.py computes commission directly from
PAKD Item.salary_coefficient × revenue_actual — the rule template is
bypassed entirely. Leaving a rate=100% row in the template misleads users
who edit the rate thinking it applies (it doesn't).
"""

import frappe

TEMPLATE = "Monthly FTTH Rollup Standard"


def execute():
	if not frappe.db.exists("PAKD Commission Rule Template", TEMPLATE):
		return

	frappe.db.sql(
		"""
		DELETE FROM `tabPAKD Rule Component`
		WHERE parent = %s AND parenttype = 'PAKD Commission Rule Template'
		""",
		(TEMPLATE,),
	)
	frappe.db.commit()
	frappe.clear_cache(doctype="PAKD Commission Rule Template")
