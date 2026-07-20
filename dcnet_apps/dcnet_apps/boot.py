# Copyright (c) 2025, DCNET Cloud and contributors
# For license information, please see license.txt

import frappe


def boot_session(bootinfo):
	"""
	Override Frappe boot session to customize branding.
	This function is called on every session boot.

	Refs:
	- https://docs.frappe.io/framework/user/en/python-api/hooks#boot_session
	"""

	# Override app logo and name for navbar/sidebar
	# Override ALL apps to show DCNET branding
	if bootinfo.get("app_data"):
		for app in bootinfo["app_data"]:
			app["app_logo_url"] = "/assets/dcnet_apps/images/dcnet-logo.png"
			app["app_title"] = "DCNET"
			# Also override the 'title' key used by add_to_apps_screen
			if "title" in app:
				app["title"] = "DCNET"

	# Override app name
	bootinfo["app_name"] = "DCNET"

	# Hide Frappe/ERPNext version update popup from users
	bootinfo.has_app_updates = False
