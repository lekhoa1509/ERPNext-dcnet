"""Boot session extensions for the PAKD app — surfaces PAKD Settings flags to JS."""

import frappe


def boot_session(bootinfo):
	try:
		use_hrms = frappe.db.get_single_value("PAKD Settings", "use_hrms_for_commission")
		bootinfo["dcnet_pakd_use_hrms"] = int(use_hrms or 0)
	except Exception:
		bootinfo["dcnet_pakd_use_hrms"] = 0
