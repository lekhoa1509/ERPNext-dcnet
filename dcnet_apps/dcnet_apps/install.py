# Copyright (c) 2025, DCNET Cloud and contributors
# For license information, please see license.txt

import os
import shutil
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from dcnet_apps.migration_install.inventory_status_workflow.inventory_status_workflow_install import setup_purchase_receipt_workflow
from dcnet_apps.migration_install.purchase_order.purchase_order_workflow_install import setup_purchase_order_workflow


def before_migrate():
	"""
	Called BEFORE bench migrate runs schema sync.

	Ensures Module Defs exist so that sync_all() can properly sync
	workspaces, reports, and other standard docs for new modules.

	Frappe only auto-creates Module Defs during `bench install-app`.
	When a new module is added to modules.txt, `bench migrate` won't
	create the Module Def — causing workspace sync to fail silently.
	"""
	setup_module_defs()


def after_install():
	"""
	Called after app installation.
	Setup branding configuration.
	"""
	setup_branding()
	setup_system_settings()
	setup_currency_format()
	# setup_desk()  # TEMP: disabled — show all default icons
	setup_fiscal_year()
	setup_customer_groups()
	sync_frappe_translations()
	sync_erpnext_translations()
	setup_einvoice_custom_fields()
	setup_einvoice_provider()
	setup_htkk_demo_data()


def after_migrate():
	"""
	Called after bench migrate.
	Ensure all configurations are applied for all team members.
	"""
	# IMPORTANT: Remove Frappe CRM app first (migrating to ERPNext built-in CRM)
	remove_frappe_crm_app()

	setup_branding()
	setup_system_settings()
	setup_currency_format()
	# setup_desk()  # TEMP: disabled — show all default icons
	setup_fiscal_year()
	setup_customer_groups()
	sync_frappe_translations()
	sync_erpnext_translations()
	setup_vietnamese_language()

	# TEMP: disabled — show all default modules/domains
	# setup_active_domains()
	# setup_disabled_modules()

	# Add Barcode Label to Stock sidebar
	add_barcode_to_stock_workspace()

	# Create E-Invoice custom fields and seed provider
	setup_einvoice_custom_fields()
	setup_einvoice_provider()

	# Add DCNet Report to Stock sidebar
	add_dcnet_report_to_stock_workspace()

	# Setup Item Image Management tab
	setup_item_image_tab()

	# Create workflow and custom field for Purchase Receipt approval process
	setup_purchase_receipt_workflow()

	# Setup HTKK demo data and sidebar
	setup_htkk_demo_data()

	# Sync workflow_diagram module fixtures (custom fields for Workspace Sidebar Item)
	sync_workflow_diagram_fixtures()

	# Create missing workspaces for diagrams
	setup_workspace_names()

	# Sync all workspace sidebars from JSON
	sync_workspace_sidebars()

	# Patch frappe sidebar template for same-tab navigation
	patch_frappe_sidebar_template()

	# Create workflow and custom field for Purchase Order approval process
	setup_purchase_order_workflow()


def add_barcode_to_stock_workspace():
	"""Add Barcode Label to Stock Workspace sidebar if not exists"""
	if not frappe.db.exists("DocType", "Barcode Label"):
		return

	try:
		# 1. Update standard Workspace (for consistency)
		workspace = frappe.get_doc("Workspace", "Stock")
		if not any(link.link_to == "Barcode Label" for link in workspace.links):
			workspace.append("links", {
				"label": "Barcode Label",
				"link_to": "Barcode Label",
				"link_type": "DocType",
				"icon": "air-vent",
				"type": "Link"
			})
			workspace.save(ignore_permissions=True)
			print("✅ Added Barcode Label to Workspace 'Stock'")

		# 2. Update custom Workspace Sidebar (for the actual UI Sidebar)
		if frappe.db.exists("Workspace Sidebar", "Stock"):
			sidebar = frappe.get_doc("Workspace Sidebar", "Stock")
			if not any(item.link_to == "Barcode Label" for item in sidebar.items):
				sidebar.append("items", {
					"label": "Barcode Label",
					"link_to": "Barcode Label",
					"link_type": "DocType",
					"type": "Link",
					"icon": "air-vent"
				})
				sidebar.save(ignore_permissions=True)
				print("✅ Added Barcode Label to Workspace Sidebar 'Stock'")
		
		frappe.db.commit()
	except Exception as e:
		print(f"⚠️ Could not add link to Stock Sidebar: {e}")


def add_dcnet_report_to_stock_workspace():
	"""Add DCNet Report workspace to Stock sidebar if not exists.

	Note: Only updates Workspace Sidebar (which accepts link_type='Workspace').
	The Workspace doc's links child table does NOT accept 'Workspace' as link_type
	(only DocType/Page/Report), so we skip it.
	"""
	if not frappe.db.exists("Workspace", "DCNet Report"):
		return

	try:
		if frappe.db.exists("Workspace Sidebar", "Stock"):
			sidebar = frappe.get_doc("Workspace Sidebar", "Stock")
			if not any(item.link_to == "DCNet Report" for item in sidebar.items):
				sidebar.append("items", {
					"label": "DCNet Report",
					"link_to": "DCNet Report",
					"link_type": "Workspace",
					"type": "Link",
					"icon": "heart-active"
				})
				sidebar.save(ignore_permissions=True)
				frappe.db.commit()
				print("✅ Added DCNet Report to Workspace Sidebar 'Stock'")
			else:
				print("✅ DCNet Report already in Stock sidebar")
	except Exception as e:
		print(f"⚠️ Could not add DCNet Report to Stock Sidebar: {e}")


def setup_einvoice_custom_fields():
	"""
	Create custom fields for E-Invoice integration on:
	- Purchase Invoice (Staging link + lookup code)
	- Sales Invoice (Issued check + number + lookup code + PDF URL)

	These fields are required for Matbao/Misa/Viettel integration.
	Idempotent: create_custom_fields skips if already exists.
	"""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	CUSTOM_FIELDS = {
		"Purchase Invoice": [
			{
				"fieldname": "einvoice_section",
				"label": "Hóa đơn điện tử",
				"fieldtype": "Section Break",
				"insert_after": "terms",
				"collapsible": 1,
			},
			{
				"fieldname": "einvoice_inward",
				"label": "HĐ mua vào (Staging)",
				"fieldtype": "Link",
				"options": "EInvoice Inward",
				"insert_after": "einvoice_section",
				"read_only": 1,
			},
			{
				"fieldname": "einvoice_lookup_code",
				"label": "Mã tra cứu",
				"fieldtype": "Data",
				"insert_after": "einvoice_inward",
				"read_only": 1,
			},
		],
		"Sales Invoice": [
			{
				"fieldname": "einvoice_section",
				"label": "Hóa đơn điện tử",
				"fieldtype": "Section Break",
				"insert_after": "terms",
				"collapsible": 1,
			},
			{
				"fieldname": "einvoice_issued",
				"label": "Đã xuất HĐ đỏ",
				"fieldtype": "Check",
				"insert_after": "einvoice_section",
				"read_only": 1,
				"default": "0",
				"in_list_view": 1,
				"in_standard_filter": 1,
			},
			{
				"fieldname": "einvoice_col1",
				"fieldtype": "Column Break",
				"insert_after": "einvoice_issued",
			},
			{
				"fieldname": "einvoice_provider",
				"label": "Nhà cung cấp HĐĐT",
				"fieldtype": "Link",
				"options": "EInvoice Provider",
				"insert_after": "einvoice_col1",
				"read_only": 1,
			},
			{
				"fieldname": "einvoice_sb2",
				"fieldtype": "Section Break",
				"insert_after": "einvoice_provider",
			},
			{
				"fieldname": "einvoice_number",
				"label": "Số HĐ đỏ",
				"fieldtype": "Data",
				"insert_after": "einvoice_sb2",
				"read_only": 1,
			},
			{
				"fieldname": "einvoice_lookup_code",
				"label": "Mã tra cứu",
				"fieldtype": "Data",
				"insert_after": "einvoice_number",
				"read_only": 1,
			},
			{
				"fieldname": "einvoice_col2",
				"fieldtype": "Column Break",
				"insert_after": "einvoice_lookup_code",
			},
			{
				"fieldname": "einvoice_pdf_url",
				"label": "Link PDF HĐ đỏ",
				"fieldtype": "Data",
				"insert_after": "einvoice_col2",
				"length": 1000,
				"read_only": 1,
				"options": "URL",
			},
			{
				"fieldname": "einvoice_issued_at",
				"label": "Thời điểm xuất",
				"fieldtype": "Datetime",
				"insert_after": "einvoice_pdf_url",
				"read_only": 1,
			},
		],
	}
	try:
		create_custom_fields(CUSTOM_FIELDS, update=True)
		frappe.db.commit()
		print("✅ E-Invoice custom fields indexed and applied")
	except Exception as e:
		print(f"⚠️ Could not setup E-Invoice custom fields: {e}")


def setup_module_defs():
	"""
	Ensure all modules in modules.txt have corresponding Module Def records.

	Frappe only auto-creates Module Defs during `bench install-app`.
	When a new module is added to modules.txt and team runs `bench migrate`,
	the Module Def won't exist — causing workspace/report sync to fail silently.

	This function reads modules.txt and creates missing Module Def records.
	Must run BEFORE setup_desk() so workspaces are available for Desktop Icons.
	"""
	try:
		app_path = frappe.get_app_path("dcnet_apps")
		modules_txt = os.path.join(app_path, "modules.txt")

		if not os.path.exists(modules_txt):
			return

		with open(modules_txt) as f:
			modules = [line.strip() for line in f if line.strip()]

		created_modules = []
		for module_name in modules:
			if not frappe.db.exists("Module Def", module_name):
				frappe.get_doc({
					"doctype": "Module Def",
					"module_name": module_name,
					"app_name": "dcnet_apps",
				}).insert(ignore_permissions=True)
				created_modules.append(module_name)
				print(f"✅ Module Def '{module_name}' created")

		frappe.db.commit()
		if created_modules:
			frappe.cache().delete_keys("modules*")
	except Exception as e:
		print(f"⚠️ Could not setup Module Defs: {e}")


def remove_frappe_crm_app():
	"""
	Remove Frappe CRM app if installed.

	DCNET Flow migrated from Frappe CRM (separate app) to ERPNext built-in CRM module.
	This function auto-removes the crm app when team pulls code and runs migrate.

	What it does:
	1. Check if 'crm' app is installed on current site
	2. Uninstall the app (removes DocTypes, data, and app from apps.txt)
	3. Remove symlink from apps folder

	Note: This will DELETE all Frappe CRM data (CRM Deal, CRM Lead, etc.)
	ERPNext CRM module uses different DocTypes (Lead, Opportunity, Customer).

	Documentation: CLAUDE.md - Platform Decision section
	"""
	import subprocess

	try:
		site = frappe.local.site

		# Check if crm app is installed
		installed_apps = frappe.get_installed_apps()

		if "crm" not in installed_apps:
			print("✅ Frappe CRM app not installed - nothing to remove")
			return

		print("🔄 Removing Frappe CRM app (migrating to ERPNext built-in CRM)...")

		# Get bench path
		bench_path = frappe.utils.get_bench_path()

		# Uninstall app from site
		# Using subprocess because frappe.installer.remove_app requires more setup
		cmd = f"cd {bench_path} && bench --site {site} uninstall-app crm --yes --no-backup"
		result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

		if result.returncode == 0:
			print("✅ Frappe CRM app uninstalled from site")
		else:
			# App might already be partially removed
			print(f"⚠️ Uninstall command: {result.stderr or result.stdout}")

		# Remove app from apps folder (symlink)
		apps_path = os.path.join(bench_path, "apps", "crm")
		if os.path.exists(apps_path) or os.path.islink(apps_path):
			os.remove(apps_path)
			print("✅ Removed crm symlink from apps folder")

		# Remove from apps.txt
		apps_txt = os.path.join(bench_path, "sites", "apps.txt")
		if os.path.exists(apps_txt):
			with open(apps_txt, "r") as f:
				apps = [line.strip() for line in f if line.strip() and line.strip() != "crm"]
			with open(apps_txt, "w") as f:
				f.write("\n".join(apps) + "\n")
			print("✅ Removed crm from apps.txt")

		print("✅ Frappe CRM app removed successfully")
		print("   → Now using ERPNext built-in CRM module (Lead, Opportunity, Customer)")

	except Exception as e:
		print(f"⚠️ Could not remove Frappe CRM app: {e}")
		print("   → You can manually run: bench --site {site} uninstall-app crm --yes")


def setup_branding():
	"""
	Setup DCNET branding for navbar and website.
	This ensures all team members get the same branding after git pull + migrate.
	"""
	# Update Navbar Settings
	try:
		navbar = frappe.get_doc("Navbar Settings")
		navbar.app_logo = "/assets/dcnet_apps/images/dcnet-logo.png"
		navbar.save(ignore_permissions=True)
		frappe.db.commit()
		print("✅ Navbar Settings updated with DCNET logo")
	except Exception as e:
		print(f"⚠️ Could not update Navbar Settings: {e}")

	# Update Website Settings
	try:
		frappe.db.set_value(
			"Website Settings",
			"Website Settings",
			{
				"app_name": "DCNET Flow",
				"app_logo": "/assets/dcnet_apps/images/dcnet-logo.png",
				"favicon": "/assets/dcnet_apps/images/favicon.png",
			},
		)
		frappe.db.commit()
		print("✅ Website Settings updated with DCNET branding")
	except Exception as e:
		print(f"⚠️ Could not update Website Settings: {e}")

	# Clear cache to apply changes
	try:
		frappe.cache().delete_keys("bootinfo*")
		frappe.clear_cache()
		print("✅ Cache cleared - branding applied")
	except Exception as e:
		print(f"⚠️ Could not clear cache: {e}")


def setup_system_settings():
	"""
	Setup System Settings for DCNET Flow.
	- Disable "Login with Email Link" button on login page
	"""
	try:
		frappe.db.set_value(
			"System Settings",
			"System Settings",
			{
				"allow_login_using_mobile_number": 0,
				"allow_login_using_user_name": 1,
				"login_with_email_link": 0,  # Disable "Login with Email Link"
			},
		)
		frappe.db.commit()
		print("✅ System Settings updated (disabled Email Link login)")
	except Exception as e:
		print(f"⚠️ Could not update System Settings: {e}")


def setup_currency_format():
	"""
	Configure VND currency display for Vietnamese market.

	Sets VND to show: 2.847.500.000đ (dot thousands, no decimals, đ suffix)
	instead of default: VND 2.847.500.000,00

	Changes:
	- VND Currency: symbol="đ", symbol_on_right=1, number_format="#.###"
	- System Settings: use_number_format_from_currency=1
	  (Currency fields use VND's "#.###" format instead of system "#.###,##")

	Team sync: Pull code + migrate → all devs get same currency format.
	New modules just use fieldtype="Currency" — formatting is automatic.
	"""
	try:
		# 1. Configure VND Currency
		if frappe.db.exists("Currency", "VND"):
			frappe.db.set_value("Currency", "VND", {
				"symbol": "đ",
				"symbol_on_right": 1,
				"number_format": "#.###",
				"smallest_currency_fraction_value": 0,
				"fraction_units": 0,
				"enabled": 1,
			})

		# 2. System Settings: use currency's own number format for Currency fields
		#    currency_precision=0: Frappe defaults to 2 if empty (formatters.js:135)
		frappe.db.set_value("System Settings", "System Settings", {
			"use_number_format_from_currency": 1,
			"currency_precision": "0",
		})

		frappe.db.commit()
		print("✅ VND currency format: 2.847.500.000đ (symbol_on_right, no decimals)")
	except Exception as e:
		print(f"⚠️ Could not setup currency format: {e}")


def setup_desk():
	"""
	Setup Desk for DCNET Flow.

	Called on: after_install, after_migrate

	Strategy: IDEMPOTENT - Delete all Desktop Icons, recreate from config.
	Every migrate produces the exact same result regardless of DB state.

	Layout (English labels, auto-translated to Vietnamese by Frappe):
	  1. CRM               (→ CRM)
	  2. Selling            (→ Bán hàng)
	  3. Buying             (→ Mua hàng)
	  4. Stock              (→ Tồn Kho)
	  5. Assets             (→ Tài sản)
	  6. Invoicing          (→ Kế toán)
	  7. Financial Reports  (→ Báo cáo tài chính)

	To add new icons: edit DESK_ICONS or DESK_FOLDERS below, then migrate.
	"""

	# ── Declarative config (single source of truth) ──────────────────────
	# NOTE: Labels MUST match Workspace Sidebar names (English).
	# Frappe auto-translates to Vietnamese via __() on the client.
	# See: frappe/desk/page/desktop/desktop.js line 50
	#   → frappe.boot.workspace_sidebar_item[desktop_icon.label.toLowerCase()]
	DESK_ICONS = [
		{"label": "Dashboard",         "idx": 1},
		{"label": "CRM",               "idx": 2},
		{"label": "Selling",           "idx": 3},
		{"label": "Buying",            "idx": 4},
		{"label": "Stock",             "idx": 5},
		{"label": "Assets",            "idx": 6},
		{"label": "Invoicing",         "idx": 7},
		{"label": "Financial Reports", "idx": 8},
	]

	DESK_FOLDERS = {
		# TODO: Re-enable when Fitting/Coaching/Trade-in modules are built
		# "Dịch vụ": {
		# 	"idx": 8,
		# 	"icon": "fitting",
		# 	"children": [
		# 		{"label": "Fitting",  "link_to": "Fitting",  "idx": 1},
		# 		{"label": "Coaching", "link_to": "Coaching", "idx": 2},
		# 		{"label": "Trade-in", "link_to": "Trade-in", "idx": 3},
		# 	],
		# },
	}

	# ── Collect all workspace names we need visible ──────────────────────
	needed_workspaces = set()
	for icon in DESK_ICONS:
		needed_workspaces.add(icon["label"])
	for folder_config in DESK_FOLDERS.values():
		for child in folder_config["children"]:
			needed_workspaces.add(child["link_to"])

	try:
		# 1. Delete ALL Desktop Icons (clean slate - no duplicates possible)
		frappe.db.delete("Desktop Icon")

		# 2. Hide ALL workspaces, then unhide only what we need
		frappe.db.sql("UPDATE `tabWorkspace` SET `is_hidden` = 1")

		for ws_name in needed_workspaces:
			if frappe.db.exists("Workspace", ws_name):
				frappe.db.set_value("Workspace", ws_name, "is_hidden", 0)

		# 3. Create standalone icons (label = workspace name for sidebar lookup)
		# SVG resolved by Frappe via: /assets/{app}/icons/desktop_icons/{variant}/{scrub(label)}.svg
		for config in DESK_ICONS:
			ws_name = config["label"]
			if not frappe.db.exists("Workspace", ws_name):
				print(f"   Workspace '{ws_name}' not found - skipping")
				continue

			doc = frappe.get_doc({
				"doctype": "Desktop Icon",
				"label": ws_name,
				"icon_type": "Link",
				"link_type": "Workspace Sidebar",
				"link_to": ws_name,
				"idx": config["idx"],
				"hidden": 0,
				"standard": 1,
				"app": "dcnet_apps",
			})
			doc.flags.ignore_links = True
			doc.insert(ignore_permissions=True)

		# 4. Create folders and their children
		for folder_label, folder_config in DESK_FOLDERS.items():
			frappe.get_doc({
				"doctype": "Desktop Icon",
				"label": folder_label,
				"icon_type": "Folder",
				"icon": folder_config["icon"],
				"idx": folder_config["idx"],
				"hidden": 0,
				"standard": 1,
				"app": "dcnet_apps",
			}).insert(ignore_permissions=True)

			for child in folder_config["children"]:
				if not frappe.db.exists("Workspace", child["link_to"]):
					continue

				child_doc = frappe.get_doc({
					"doctype": "Desktop Icon",
					"label": child["label"],
					"icon_type": "Link",
					"link_type": "Workspace Sidebar",
					"link_to": child["link_to"],
					"parent_icon": folder_label,
					"icon": child.get("icon", ""),
					"idx": child["idx"],
					"hidden": 0,
					"standard": 1,
					"app": "dcnet_apps",
				})
				child_doc.flags.ignore_links = True
				child_doc.insert(ignore_permissions=True)

		# 5. Create Workspace Sidebars (required for Desktop Icon visibility)
		from frappe.desk.doctype.workspace_sidebar.workspace_sidebar import (
			create_workspace_sidebar_for_workspaces,
		)
		create_workspace_sidebar_for_workspaces()

		# 6. Commit and clear cache for ALL users
		frappe.db.commit()
		frappe.cache.delete_keys("desktop_icons")

		total = frappe.db.count("Desktop Icon")
		print(f"✅ Desk setup: {total} icons created (idempotent)")

	except Exception as e:
		print(f"⚠️ Could not setup desk: {e}")
		import traceback
		traceback.print_exc()


def setup_fiscal_year():
	"""
	Setup Fiscal Year for current year if not exists.

	ERPNext requires Fiscal Year for all accounting operations:
	- Sales Invoice, Purchase Invoice
	- Payment Entry, Journal Entry
	- Customer/Supplier Dashboard (displays revenue by fiscal year)
	- Financial Reports

	Without Fiscal Year, opening Customer form will fail with:
	"FiscalYearError: Date XX-XX-XXXX is not in any active Fiscal Year"

	This function auto-creates Fiscal Year for current year on migrate.

	Documentation: docs/customization/README.md
	"""
	from datetime import date

	try:
		current_year = date.today().year
		fy_name = str(current_year)

		# Check if Fiscal Year already exists
		if frappe.db.exists("Fiscal Year", fy_name):
			print(f"✅ Fiscal Year {fy_name} already exists")
			return

		# Create Fiscal Year for current year
		fy = frappe.get_doc({
			"doctype": "Fiscal Year",
			"year": fy_name,
			"year_start_date": f"{current_year}-01-01",
			"year_end_date": f"{current_year}-12-31",
		})
		fy.insert(ignore_permissions=True)
		frappe.db.commit()

		print(f"✅ Fiscal Year {fy_name} created (01-01 to 31-12)")

	except Exception as e:
		print(f"⚠️ Could not setup Fiscal Year: {e}")


def setup_customer_groups():
	"""
	Ensure required Customer Groups exist for Dashboard Number Cards.

	Number Cards filter by customer_group to split revenue:
	- "Khách sỉ" → Wholesale Revenue card
	- "Khách lẻ" → Retail Revenue card

	These are created as children of "All Customer Groups" (ERPNext default root).
	Idempotent: skips if already exists.
	"""
	required_groups = ["Khách sỉ", "Khách lẻ"]

	try:
		for group_name in required_groups:
			if frappe.db.exists("Customer Group", group_name):
				continue

			doc = frappe.get_doc({
				"doctype": "Customer Group",
				"customer_group_name": group_name,
				"parent_customer_group": "All Customer Groups",
			})
			doc.insert(ignore_permissions=True)
			print(f"✅ Customer Group '{group_name}' created")

		frappe.db.commit()
	except Exception as e:
		print(f"⚠️ Could not setup Customer Groups: {e}")


def setup_vietnamese_language():
	"""
	Set Vietnamese as default language for all users.

	This ensures UI displays in Vietnamese after:
	- Translations are synced from dcnet_apps/locale/
	- bench migrate (runs this hook)

	Documentation: docs/customization/localization/
	"""
	try:
		# Set system default language
		frappe.db.set_single_value("System Settings", "language", "vi")

		# Set Vietnamese for all existing users (except Guest)
		users = frappe.get_all(
			"User",
			filters={"name": ["not in", ["Guest"]]},
			pluck="name"
		)

		updated_count = 0
		for user in users:
			current_lang = frappe.db.get_value("User", user, "language")
			if current_lang != "vi":
				frappe.db.set_value("User", user, "language", "vi")
				updated_count += 1

		frappe.db.commit()

		# Clear cache to apply language changes
		frappe.cache().delete_keys("bootinfo*")
		frappe.cache().delete_keys("translations*")

		if updated_count > 0:
			print(f"✅ Vietnamese language set for {updated_count} users")
		else:
			print("✅ All users already have Vietnamese language")

	except Exception as e:
		print(f"⚠️ Could not setup Vietnamese language: {e}")


def sync_frappe_translations():
	"""
	Sync Frappe Framework Vietnamese translations from dcnet_apps to frappe locale.

	Translations are stored in:
	- dcnet_apps/locale/frappe/vi.po (tracked in git)

	And copied to:
	- frappe/frappe/locale/vi.po (inside container, not tracked)

	This allows team to maintain Frappe translations in git and auto-deploy via migrate.
	"""
	try:
		# Get paths
		dcnet_apps_path = frappe.get_app_path("dcnet_apps")
		frappe_app_path = frappe.get_app_path("frappe")

		source_file = os.path.join(dcnet_apps_path, "locale", "frappe", "vi.po")
		target_file = os.path.join(frappe_app_path, "locale", "vi.po")

		# Check if source exists
		if not os.path.exists(source_file):
			print("⏭️  Frappe translations source not found - skipping")
			return

		# Copy file
		shutil.copy2(source_file, target_file)
		print(f"✅ Frappe translations synced: vi.po ({os.path.getsize(target_file):,} bytes)")

		# Clear translation cache
		frappe.cache().delete_keys("translations*")

	except Exception as e:
		print(f"⚠️ Could not sync Frappe translations: {e}")


def sync_erpnext_translations():
	"""
	Sync ERPNext Vietnamese translations from dcnet_apps to erpnext locale.

	Translations are stored in:
	- dcnet_apps/locale/erpnext/vi.po (tracked in git)

	And copied to:
	- erpnext/erpnext/locale/vi.po (inside container, not tracked)

	This allows team to maintain ERPNext translations in git and auto-deploy via migrate.

	Note: ERPNext is symlinked as dcnet_core in this project.
	"""
	try:
		# Get paths
		dcnet_apps_path = frappe.get_app_path("dcnet_apps")
		erpnext_app_path = frappe.get_app_path("erpnext")

		source_file = os.path.join(dcnet_apps_path, "locale", "erpnext", "vi.po")
		target_file = os.path.join(erpnext_app_path, "locale", "vi.po")

		# Check if source exists
		if not os.path.exists(source_file):
			print("⏭️  ERPNext translations source not found - skipping")
			return

		# Ensure target directory exists
		target_dir = os.path.dirname(target_file)
		if not os.path.exists(target_dir):
			os.makedirs(target_dir)

		# Copy file
		shutil.copy2(source_file, target_file)
		print(f"✅ ERPNext translations synced: vi.po ({os.path.getsize(target_file):,} bytes)")

		# Clear translation cache
		frappe.cache().delete_keys("translations*")

	except Exception as e:
		print(f"⚠️ Could not sync ERPNext translations: {e}")




def setup_active_domains():
	"""
	Setup active domains for DCNET Flow.

	This controls which ERPNext modules/features are visible:
	- ENABLED: Distribution, Services, Retail (for CRM, Selling, Buying, Stock, POS)
	- DISABLED: Manufacturing, Education, Healthcare, Agriculture, Non Profit

	When a domain is disabled, ERPNext automatically hides:
	- Related workspaces/modules
	- Dashboard links (e.g., "Work Order" in Sales Order)
	- Buttons (e.g., "Make Work Order" in Sales Order)
	- Roles restricted to that domain

	Team sync: Pull code + run migrate → all devs get same domain settings

	Documentation: docs/customization/ui/2026-01-30-disable-modules.md
	"""
	# Domains to KEEP active (whitelist approach)
	# These are required for Golf shop business
	enabled_domains = [
		"Distribution",  # Selling, Buying, Stock, Warehouse
		"Services",      # CRM, basic services
		"Retail",        # POS
	]

	# Domains to DISABLE (will hide all related features)
	disabled_domains = [
		"Manufacturing",  # Work Order, BOM, Production Planning
		"Education",      # Student, Course, Fee
		"Healthcare",     # Patient, Practitioner, Medical
		"Agriculture",    # Crop, Land, Weather
		"Non Profit",     # Donor, Volunteer, Chapter
	]

	try:
		# Get or create Domain Settings
		if not frappe.db.exists("Domain Settings", "Domain Settings"):
			frappe.get_doc({"doctype": "Domain Settings"}).insert(ignore_permissions=True)

		domain_settings = frappe.get_doc("Domain Settings", "Domain Settings")

		# Get current active domains
		current_domains = [d.domain for d in domain_settings.active_domains]

		# Calculate changes needed
		domains_to_add = [d for d in enabled_domains if d not in current_domains]
		domains_to_remove = [d for d in disabled_domains if d in current_domains]

		# Check if any changes needed
		if not domains_to_add and not domains_to_remove:
			print("✅ Domain Settings already configured correctly")
			return

		# Remove disabled domains
		if domains_to_remove:
			domain_settings.active_domains = [
				d for d in domain_settings.active_domains
				if d.domain not in disabled_domains
			]

		# Add enabled domains (ensure Domain records exist first)
		for domain in domains_to_add:
			# Create Domain record if not exists
			if not frappe.db.exists("Domain", domain):
				frappe.get_doc({
					"doctype": "Domain",
					"domain": domain
				}).insert(ignore_permissions=True)

			# Add to active domains
			domain_settings.append("active_domains", {"domain": domain})

		# Save triggers on_update which applies domain restrictions
		domain_settings.save(ignore_permissions=True)
		frappe.db.commit()

		# Log changes
		if domains_to_add:
			print(f"✅ Enabled domains: {', '.join(domains_to_add)}")
		if domains_to_remove:
			print(f"✅ Disabled domains: {', '.join(domains_to_remove)}")

		print("✅ Domain Settings configured - Manufacturing features hidden")

	except Exception as e:
		print(f"⚠️ Could not setup Domain Settings: {e}")


def setup_disabled_modules():
	"""
	Disable ERPNext modules not used by DCNET Flow (golf shop retail).

	Uses `restrict_to_domain` on Module Def — when the domain is not active,
	the module is hidden from sidebar, search, and DocType access.

	We tie unused modules to "Manufacturing" domain (already disabled in
	setup_active_domains), so they are automatically hidden.

	Effect: Hides module from UI, search bar, and removes related buttons
	(e.g., "Bảng Chấm Công" / Timesheet in Sales Invoice "Get Items From").

	Team sync: Pull code + run migrate → all devs get same module settings.
	"""
	# Modules to disable (tied to "Manufacturing" domain which is not active)
	DISABLED_MODULES = [
		"Projects",            # Timesheet, Project — not needed for retail
		"Manufacturing",       # Work Order, BOM — already disabled via domain
		"Quality Management",  # QA inspection — not needed
		"EDI",                 # Electronic Data Interchange — not needed
		"Subcontracting",      # Gia công — not needed
		"Telephony",           # Call center integration — not needed
	]

	# Domain to restrict to (must NOT be in active domains)
	RESTRICT_DOMAIN = "Manufacturing"

	try:
		changed = []
		for module_name in DISABLED_MODULES:
			if not frappe.db.exists("Module Def", module_name):
				continue

			current = frappe.db.get_value("Module Def", module_name, "restrict_to_domain")
			if current != RESTRICT_DOMAIN:
				frappe.db.set_value(
					"Module Def", module_name,
					"restrict_to_domain", RESTRICT_DOMAIN,
					update_modified=False,
				)
				changed.append(module_name)

		if changed:
			frappe.db.commit()
			frappe.cache().delete_keys("modules*")
			print(f"✅ Disabled modules: {', '.join(changed)}")
		else:
			print("✅ Unused modules already disabled")

	except Exception as e:
		print(f"⚠️ Could not disable modules: {e}")



def setup_item_image_tab():
	"""
	Setup Item Image Management tab in Item doctype
	Creates necessary custom fields for image gallery functionality
	"""
	
	try:
		# 1. Ensure Item Image doctype exists before creating link field
		if not frappe.db.exists("DocType", "Item Image"):
			print("❌ 'Item Image' doctype not found. Please create it first.")
			return
		
		# 2. get list fieldnames of existing custom fields in Item to avoid duplicates
		existing_fields = frappe.get_all(
			"Custom Field",
			filters={"dt": "Item"},
			pluck="fieldname"
		)
		
		# 3. Determine insert_after position for new fields (after taxes or description if exists)
		meta = frappe.get_meta("Item")
		all_fields = [f.fieldname for f in meta.fields]
		
		# Find a reasonable position: prioritize after details
		insert_positions = ["details", "description", "item_name"]
		insert_after = next(
			(f for f in insert_positions if f in all_fields),
			all_fields[-1] if all_fields else None  # fallback: None
		)
		
		# 4. Configure fields to create
		field_configs = {
			"item_image_manage_tab": {
				"label": "Item Image Manage",
				"fieldtype": "Tab Break",
				"insert_after": insert_after
			},
			"custom_image_manager": {
				"label": "Image Manager",
				"fieldtype": "HTML",
				"insert_after": "item_image_manage_tab"
			},
			"custom_item_images": {
				"label": "Item Images",
				"fieldtype": "Table",
				"options": "Item Image",
				"insert_after": "custom_image_manager"
			}
		}
		
		# 5. filter out fields that already exist to avoid duplicates
		fields_to_create = []
		for fieldname, config in field_configs.items():
			if fieldname not in existing_fields:
				field = config.copy()
				field["fieldname"] = fieldname
				fields_to_create.append(field)
		
		# 6. Create fields if needed
		if fields_to_create:
			create_custom_fields({"Item": fields_to_create})
			print(f"✅ Successfully created {len(fields_to_create)} fields:")
			for field in fields_to_create:
				print(f"   - {field['fieldname']} ({field['fieldtype']})")
		else:
			print("ℹ️ All Item Image fields already exist")
		
	except Exception as e:
		error_msg = f"Failed to setup Item Image tab: {str(e)}"
		frappe.log_error(
			title="Item Image Tab Setup Error",
			message=frappe.get_traceback()
		)
		print(f"❌ Failed to setup Item Image tab: {str(e)}")


def setup_einvoice_provider():
	"""
	Seed default Mắt Bão e-invoice provider with demo/sandbox credentials.

	This ensures all new installations have a working provider for testing.
	Provider can be updated with production credentials later.

	Credentials: Mắt Bão sandbox (demo-api-hddt.matbao.in)
	- API URL (Sales): https://demo-api-hddt.matbao.in:11443
	- API URL (Purchase): https://demo-api-hoadondauvao.matbao.in
	- Tax Code: 0302712571-999
	- Invoice Serial: C26TCL

	Idempotent: skips if provider already exists.
	"""
	# Check if EInvoice Provider DocType exists (module might not be installed)
	if not frappe.db.exists("DocType", "EInvoice Provider"):
		return

	provider_name = "Mắt Bão"

	# Skip if already exists
	if frappe.db.exists("EInvoice Provider", provider_name):
		return

	# Get the first company
	company = frappe.db.get_value("Company", filters={}, fieldname="name", order_by="creation asc")
	if not company:
		print("⚠️ EInvoice: No company found, skipping provider seed")
		return

	try:
		# Create provider with demo credentials
		doc = frappe.get_doc({
			"doctype": "EInvoice Provider",
			"provider_name": provider_name,
			"provider_type": "Matbao",
			"enabled": 1,
			"company": company,
			"tax_code": "0302712571-999",
			"api_url": "https://demo-api-hddt.matbao.in:11443",
			"api_url_purchase": "https://demo-api-hoadondauvao.matbao.in",
			"auth_method": "Username-Password",
			"api_username": "admin",
			"api_password": "Gtybf@12sd",
			"api_token": "86bdf9d3-48ff-46d1-91f3-0756965aa3a2",
			"default_invoice_pattern": "1",
			"default_invoice_serial": "C26TCL",
			"connection_status": "Not Tested",
		})
		doc.insert(ignore_permissions=True)
		print(f"✅ EInvoice: Created provider '{provider_name}' for company '{company}'")

		# Set as default in EInvoice Settings
		if frappe.db.exists("DocType", "EInvoice Settings"):
			settings = frappe.get_doc("EInvoice Settings")
			if not settings.default_provider:
				settings.default_provider = provider_name
				settings.save(ignore_permissions=True)
				print(f"✅ EInvoice: Set default provider to '{provider_name}'")

		frappe.db.commit()

	except Exception as e:
		print(f"⚠️ Could not setup EInvoice provider: {e}")

def setup_htkk_demo_data():
	"""
	Automatically seed HTKK demo data and sync sidebar.
	Ensures all developers have the same starting environment.
	"""
	import json
	from frappe.desk.doctype.workspace_sidebar.workspace_sidebar import create_workspace_sidebar_for_workspaces

	print("🚀 Setting up HTKK Demo Data and Sidebar...")

	# 1. Force sidebar sync and Desktop Icon
	try:
		create_workspace_sidebar_for_workspaces()
		setup_htkk_desktop_icon()
		print("✅ HTKK Sidebar and Desktop Icon synced")
	except Exception as e:
		print(f"⚠️ Could not sync Sidebar/Icon: {e}")

	# 2. Check for company
	company = frappe.db.get_value("Company", filters={}, fieldname="name", order_by="creation asc")
	if not company:
		return

	required_doctypes = ["HTKK Settings", "HTKK Declaration"]
	missing_doctypes = [doctype for doctype in required_doctypes if not frappe.db.exists("DocType", doctype)]
	if missing_doctypes:
		print(f"⚠️ HTKK DocTypes not synced yet, skipping demo seed: {', '.join(missing_doctypes)}")
		return

	# 3. Setup HTKK Settings
	if not frappe.db.exists("HTKK Settings"):
		try:
			frappe.get_doc({
				"doctype": "HTKK Settings",
				"company": company,
				"tax_code": "0123456789",
				"finance_book": "Standard"
			}).insert(ignore_permissions=True)
			print("✅ Created HTKK Settings")
		except Exception as e:
			print(f"⚠️ Could not create HTKK Settings: {e}")

	# 4. Create Demo Declaration 01/GTGT
	filters = {"period": 1, "year": 2026, "declaration_type": "01/GTGT"}
	existing = frappe.db.get_value("HTKK Declaration", filters)
	if existing:
		frappe.delete_doc("HTKK Declaration", existing)
		print(f"🗑️ Removed existing HTKK Demo Declaration: {existing}")

	try:
		# Sample Appendix Data
		appendix_data = {
			"PL01_1_GTGT": [
				{"SHDon": "INV-2026-001", "NLap": "05/01/2026", "NMua": "Công ty TNHH Giải pháp Số", "MST": "0102030405", "DThuaKCT": 45000000, "TSuat": "10%", "TienThue": 4500000},
				{"SHDon": "INV-2026-002", "NLap": "15/02/2026", "NMua": "Cá nhân mua lẻ", "MST": "", "DThuaKCT": 12000000, "TSuat": "10%", "TienThue": 1200000}
			],
			"PL01_2_GTGT": [
				{"SHDon": "B123/2026", "NLap": "01/01/2026", "NBan": "Tòa nhà Văn phòng", "MST": "0314567890", "DThuaKCT": 100000000, "TSuat": "10%", "TienThue": 10000000},
				{"SHDon": "E-00456", "NLap": "20/02/2026", "NBan": "Điện lực Hà Nội", "MST": "0100100100", "DThuaKCT": 5000000, "TSuat": "10%", "TienThue": 500000}
			],
			"PL_NQ142_GTGT": {
				"HH_DV_BanRaTrongKy": {
					"BangKeTenHHDV": [
						{"tenHHDV": "Gậy Golf TaylorMade", "giaTriHHDV": 45000000, "thueSuatTheoQuyDinh": 10, "thueSuatSauGiam": 8, "thueGTGTDuocGiam": 900000}
					],
					"tongCongGiaTriHHDV": 45000000,
					"tongCongThueGTGTDuocGiam": 900000
				}
			}
		}
		
		decl = frappe.get_doc({
			"doctype": "HTKK Declaration",
			"company": company,
			"declaration_type": "01/GTGT",
			"period_type": "Quý",
			"period": 1,
			"year": 2026,
			"status": "Nháp",
			"from_date": "2026-01-01",
			"to_date": "2026-03-31",
			"appendix_data": json.dumps(appendix_data, ensure_ascii=False)
		})
		
		# Add CT values
		decl.append("ct_values", {"ct_name": "ct22", "auto_value": 5000000, "label": "Thuế GTGT còn khấu trừ kỳ trước chuyển sang"})
		decl.append("ct_values", {"ct_name": "ct32", "auto_value": 57000000, "label": "Hàng hoá, dịch vụ chịu thuế suất 10% — giá trị"})
		decl.append("ct_values", {"ct_name": "ct33", "auto_value": 5700000, "label": "Hàng hoá, dịch vụ chịu thuế suất 10% — thuế GTGT"})
		
		decl.insert(ignore_permissions=True)
		frappe.db.commit()
		print("✅ Seeded HTKK Demo Declaration (01/GTGT)")
	except Exception as e:
		print(f"⚠️ Could not seed HTKK Declaration: {e}")

def setup_htkk_desktop_icon():
	"""Ensures the HTKK Desktop Icon exists and links to HTKK Workspace."""
	icon_label = "HTKK"

	# Update existing or create new - use Workspace Sidebar (required by Frappe)
	if frappe.db.exists("Desktop Icon", icon_label):
		frappe.db.set_value("Desktop Icon", icon_label, {
			"icon_type": "Link",
			"link_type": "Workspace Sidebar",
			"link_to": "HTKK",
			"link": "",
			"bg_color": "#6366f1"
		})
		print(f"✅ Updated Desktop Icon for {icon_label} → HTKK Workspace")
	else:
		frappe.get_doc({
			"doctype": "Desktop Icon",
			"label": icon_label,
			"module_name": "HTKK",
			"icon_type": "Link",
			"link_type": "Workspace Sidebar",
			"link_to": "HTKK",
			"icon": "octicon octicon-file",
			"bg_color": "#6366f1",
			"standard": 1,
			"idx": 100
		}).insert(ignore_permissions=True)
		print(f"✅ Created Desktop Icon for {icon_label} → HTKK Workspace")



def sync_workflow_diagram_fixtures():
	"""
	Sync custom fields for workflow_diagram module.
	Loads fixtures from workflow_diagram/fixtures/ folder.
	"""
	import os
	import json
	try:
		app_path = frappe.get_app_path('dcnet_apps')
		fixtures_file = os.path.join(app_path, 'workflow_diagram', 'fixtures', 'custom_field.json')

		if not os.path.exists(fixtures_file):
			print("ℹ️ workflow_diagram fixtures not found, skipping")
			return

		with open(fixtures_file, 'r', encoding='utf-8') as f:
			custom_fields = json.load(f)

		created = 0
		for field_data in custom_fields:
			field_name = field_data.get('name')
			if not field_name:
				continue

			if not frappe.db.exists('Custom Field', field_name):
				doc = frappe.get_doc({**field_data})
				doc.insert(ignore_permissions=True)
				created += 1

		if created:
			frappe.db.commit()
			print(f"✅ workflow_diagram: created {created} custom fields")
		else:
			print("ℹ️ workflow_diagram custom fields already exist")
	except Exception as e:
		print(f"⚠️ Error in sync_workflow_diagram_fixtures: {e}")


def sync_workspace_sidebars():
	"""
	Synchronize Workspace Sidebar JSON files with the database.
	Syncs from both dcnet_apps and erpnext (dcnet_core) folders.
	"""
	import os
	import json

	sidebar_folders = []

	# 1. dcnet_apps sidebars
	dcnet_apps_path = frappe.get_app_path('dcnet_apps')
	dcnet_sidebar = os.path.join(dcnet_apps_path, 'workspace_sidebar')
	if os.path.exists(dcnet_sidebar):
		sidebar_folders.append(('dcnet_apps', dcnet_sidebar))

	# 2. erpnext (dcnet_core) sidebars
	try:
		erpnext_path = frappe.get_app_path('erpnext')
		erpnext_sidebar = os.path.join(erpnext_path, 'workspace_sidebar')
		if os.path.exists(erpnext_sidebar):
			sidebar_folders.append(('erpnext', erpnext_sidebar))
	except Exception:
		pass

	if not sidebar_folders:
		print("ℹ️ No workspace_sidebar folders found")
		return

	synced_count = 0
	skipped_items = []

	for app_name, sidebar_folder in sidebar_folders:
		for filename in os.listdir(sidebar_folder):
			if not filename.endswith('.json'):
				continue

			filepath = os.path.join(sidebar_folder, filename)
			try:
				with open(filepath, 'r', encoding='utf-8') as f:
					data = json.load(f)
					name = data.get('name')
					if not name:
						continue

					# Filter items to skip missing DocTypes/Reports/Pages/Workspaces
					filtered_items = []
					for item in data.get('items', []):
						link_type = item.get('link_type')
						link_to = item.get('link_to')
						item_type = item.get('type')

						# Skip Section Break / Spacer types - they don't have link_to
						if item_type in ('Section Break', 'Spacer'):
							filtered_items.append(item)
							continue

						# Skip items with missing targets
						if link_to:
							if link_type == 'DocType' and not frappe.db.exists('DocType', link_to):
								skipped_items.append(f"{name}: {link_to} (DocType)")
								continue
							if link_type == 'Report' and not frappe.db.exists('Report', link_to):
								skipped_items.append(f"{name}: {link_to} (Report)")
								continue
							if link_type == 'Page' and not frappe.db.exists('Page', link_to):
								skipped_items.append(f"{name}: {link_to} (Page)")
								continue
							if link_type == 'Workspace' and not frappe.db.exists('Workspace', link_to):
								skipped_items.append(f"{name}: {link_to} (Workspace)")
								continue
							# URL type - no validation needed, always include
						filtered_items.append(item)

					if frappe.db.exists('Workspace Sidebar', name):
						doc = frappe.get_doc('Workspace Sidebar', name)
						doc.items = []
						for item in filtered_items:
							doc.append('items', item)
						doc.header_icon = data.get('header_icon', doc.header_icon)
						# Skip link validation - URL type items cause "DocType URL not found"
						# because DynamicLink tries to validate against non-existent "URL" DocType
						doc.flags.ignore_links = True
						doc.save(ignore_permissions=True)
					else:
						doc_data = data.copy()
						doc_data['items'] = filtered_items
						doc = frappe.get_doc({'doctype': 'Workspace Sidebar', **doc_data})
						doc.flags.ignore_links = True
						doc.insert(ignore_permissions=True)
					synced_count += 1
			except Exception as e:
				print(f"⚠️ Could not sync sidebar {app_name}/{filename}: {e}")

	frappe.db.commit()

	if skipped_items:
		print(f"ℹ️ Skipped {len(skipped_items)} items with missing targets: {', '.join(skipped_items[:5])}" + ("..." if len(skipped_items) > 5 else ""))

	print(f"✅ Workspace Sidebars synchronized: {synced_count} sidebars from {len(sidebar_folders)} app(s)")


def setup_workspace_names():
	"""
	Create missing Workspaces so that sidebar diagrams have a target.
	"""
	workspaces = [
		{"name": "Products", "label": "Sản phẩm", "module": "Stock"},
		{"name": "Accounts", "label": "Kế toán", "module": "Accounts"},
		{"name": "HR", "label": "Nhân sự & Chi nhánh", "module": "DCNET Apps"},
		{"name": "EInvoice", "label": "Hóa đơn điện tử", "module": "EInvoice"},
		{"name": "Trade-in", "label": "Trade-in", "module": "DCNET Apps"},
		{"name": "Fitting", "label": "Fitting", "module": "DCNET Apps"},
		{"name": "Coaching", "label": "Coaching", "module": "DCNET Apps"},
	]

	try:
		changed = False
		for ws_config in workspaces:
			name = ws_config["name"]
			label = ws_config.get("label", name)
			module = ws_config.get("module", "DCNET Apps")

			if not frappe.db.exists("Workspace", name):
				frappe.get_doc({
					"doctype": "Workspace",
					"name": name,
					"label": label,
					"module": module,
					"public": 1,
					"title": label
				}).insert(ignore_permissions=True)
				print(f"✅ Created Workspace: {name}")
				changed = True

		if changed:
			frappe.db.commit()
	except Exception as e:
		print(f"⚠️ Error in setup_workspace_names: {e}")


def patch_frappe_sidebar_template():
	"""
	Patch Frappe sidebar template to open internal URL links in same tab.

	Note: Frappe v16+ already includes this logic natively:
	  target="{%= (item.link_type === "URL" && !path.startsWith("/app/")) ? "_blank" : "" %}"

	This function checks if patching is needed and skips if Frappe already handles it.
	"""
	import os
	try:
		frappe_path = frappe.get_app_path('frappe')
		template_path = os.path.join(frappe_path, 'public', 'js', 'frappe', 'ui', 'sidebar', 'sidebar_item.html')

		if not os.path.exists(template_path):
			print("⚠️ Frappe sidebar template not found")
			return

		with open(template_path, 'r', encoding='utf-8') as f:
			content = f.read()

		# Frappe v16+ already has correct logic - check for native implementation
		native_pattern = '!path.startsWith("/app/")'
		if native_pattern in content:
			print("✅ Frappe sidebar template: native /app/ handling detected (no patch needed)")
			return

		# Legacy patterns (older Frappe versions)
		old_target = 'target="{{ item.is_external ? \'_blank\' : \'\' }}"'
		new_target = 'target="{{ item.is_external ? \'_blank\' : (item.link_to && item.link_to.startsWith(\'/app/\') ? \'\' : \'_blank\') }}"'

		if new_target in content:
			print("✅ Frappe sidebar template already patched")
			return

		if old_target not in content:
			print("ℹ️ Frappe sidebar template: unknown format, skipping patch")
			return

		content = content.replace(old_target, new_target)

		with open(template_path, 'w', encoding='utf-8') as f:
			f.write(content)

		print("✅ Frappe sidebar template patched (run `bench build --app frappe` to apply)")
	except Exception as e:
		print(f"⚠️ Error patching sidebar template: {e}")
