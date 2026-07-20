"""Backfill PAKD Settings.counter_account_gpvt on existing installs.

Before this version, License Fee posted DR-only (account_gpvt) and produced
unbalanced Journal Entries (Frappe rejected on submit, "Total Debit must
equal Total Credit"). Add a sensible default — TK 3338 (Phí, lệ phí và các
khoản phải nộp NN khác) — matched per company.
"""

import frappe


def execute():
	# Reload doctype so the new field is in metadata before we try to set it.
	frappe.reload_doc("dcnet_pakd", "doctype", "pakd_settings", force=True)

	if not frappe.db.exists("PAKD Settings", "PAKD Settings"):
		return

	settings = frappe.get_doc("PAKD Settings", "PAKD Settings")
	if settings.get("counter_account_gpvt"):
		return

	company = frappe.defaults.get_defaults().get("company")
	if not company:
		# Pick any active company — single-company benches won't have it set
		# in defaults but still need the seed.
		row = frappe.db.get_value("Company", {}, "name")
		if not row:
			return
		company = row

	# VN COA TT99/2025 has TK 3338 as a group with 33381/33382 leaves.
	# 33382 (Các loại thuế khác) is the semantically correct match for GPVT.
	# Fall back: any leaf under 3338*, lowest code first.
	acc = (
		frappe.db.get_value("Account", {"account_name": ["like", "3338 - %"], "company": company, "is_group": 0}, "name")
		or frappe.db.get_value("Account", {"account_name": ["like", "33382 - %"], "company": company, "is_group": 0}, "name")
		or frappe.db.sql(
			"""SELECT name FROM `tabAccount`
			   WHERE company = %s AND is_group = 0 AND account_name LIKE '3338%%'
			   ORDER BY account_name LIMIT 1""",
			(company,),
		)
	)
	if isinstance(acc, list) and acc:
		acc = acc[0][0]
	if not acc:
		return  # Account not present — admin must configure manually

	settings.counter_account_gpvt = acc
	settings.save(ignore_permissions=True)
	frappe.db.commit()
