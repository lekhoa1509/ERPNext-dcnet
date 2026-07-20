"""Install / migrate hooks for dcnet_migrate."""

import frappe
from frappe.utils import cint


SIDEBAR_NAME = "Import Auto"
WORKSPACE_NAME = "Import Auto Home"
ICON_LABEL = "Import Auto"
MIN_UPLOAD_SIZE_MB = 100
MIN_UPLOAD_SIZE_BYTES = MIN_UPLOAD_SIZE_MB * 1024 * 1024


def after_install():
	_configure_upload_limit()
	_sync_workspace()
	_sync_sidebar()
	_ensure_desktop_icon()
	_normalize_import_auto_paths()


def after_migrate():
	_configure_upload_limit()
	_sync_workspace()
	_sync_sidebar()
	_ensure_desktop_icon()
	_normalize_import_auto_paths()


def _configure_upload_limit():
	"""Keep browser and request upload limits aligned for migration workbooks."""
	from frappe.installer import update_site_config

	if cint(frappe.conf.get("max_file_size")) < MIN_UPLOAD_SIZE_BYTES:
		update_site_config("max_file_size", MIN_UPLOAD_SIZE_BYTES, validate=False)

	current_system_limit = cint(frappe.db.get_single_value("System Settings", "max_file_size"))
	if current_system_limit < MIN_UPLOAD_SIZE_MB:
		frappe.db.set_single_value("System Settings", "max_file_size", MIN_UPLOAD_SIZE_MB)

	frappe.cache.delete_key("bootinfo")


def _sync_workspace():
	"""Sync the Import Auto Workspace before the sidebar points users at it."""
	import json
	import os

	try:
		app_path = frappe.get_app_path("dcnet_migrate")
	except Exception:
		return

	filepath = os.path.join(
		app_path,
		"import_auto",
		"workspace",
		"import_auto_home",
		"import_auto_home.json",
	)
	if not os.path.exists(filepath):
		return

	try:
		with open(filepath, "r", encoding="utf-8") as f:
			data = json.load(f)
	except Exception as exc:
		frappe.log_error(f"dcnet_migrate workspace {WORKSPACE_NAME}: {exc}", "dcnet_migrate")
		return

	doc_data = {
		key: value
		for key, value in data.items()
		if key not in {"creation", "docstatus", "idx", "modified", "modified_by", "owner"}
	}
	doc_data["is_hidden"] = 0
	doc_data["public"] = 1

	previous_in_migrate = frappe.flags.in_migrate
	frappe.flags.in_migrate = True
	try:
		if frappe.db.exists("Workspace", WORKSPACE_NAME):
			doc = frappe.get_doc("Workspace", WORKSPACE_NAME)
			doc.update(doc_data)
			doc.flags.ignore_links = True
			doc.save(ignore_permissions=True)
		else:
			doc = frappe.get_doc(doc_data)
			doc.flags.ignore_links = True
			doc.insert(ignore_permissions=True)
	finally:
		frappe.flags.in_migrate = previous_in_migrate

	frappe.db.commit()


def _sync_sidebar():
	"""Sync this app's Workspace Sidebar JSON files into the database.

	Mirrors what `dcnet_apps.install.sync_workspace_sidebars` does, but scoped
	to this app so the Import Auto sidebar is registered even when only
	dcnet_migrate is installed.
	"""
	import json
	import os

	try:
		app_path = frappe.get_app_path("dcnet_migrate")
	except Exception:
		return

	sidebar_folder = os.path.join(app_path, "workspace_sidebar")
	if not os.path.isdir(sidebar_folder):
		return

	seen_sidebars = set()

	for filename in sorted(os.listdir(sidebar_folder)):
		if not filename.endswith(".json"):
			continue

		filepath = os.path.join(sidebar_folder, filename)
		try:
			with open(filepath, "r", encoding="utf-8") as f:
				data = json.load(f)
		except Exception as exc:
			frappe.log_error(f"dcnet_migrate sidebar {filename}: {exc}", "dcnet_migrate")
			continue

		name = data.get("name")
		if not name:
			continue
		if name in seen_sidebars:
			print(f"Skipping duplicate Workspace Sidebar '{name}' from {filename}")
			continue
		seen_sidebars.add(name)

		# Filter out items pointing at missing DocTypes/Workspaces/Reports/Pages.
		filtered_items = []
		for item in data.get("items", []):
			link_type = item.get("link_type")
			link_to = item.get("link_to")
			item_type = item.get("type")

			if item_type in ("Section Break", "Card Break"):
				filtered_items.append(item)
				continue

			if not link_to:
				filtered_items.append(item)
				continue

			if link_type == "DocType" and not frappe.db.exists("DocType", link_to):
				continue
			if link_type == "Workspace" and not frappe.db.exists("Workspace", link_to):
				continue
			if link_type == "Report" and not frappe.db.exists("Report", link_to):
				continue
			if link_type == "Page" and not frappe.db.exists("Page", link_to):
				continue

			filtered_items.append(item)

		data["items"] = filtered_items
		doc_data = {
			key: value
			for key, value in data.items()
			if key not in {"creation", "docstatus", "idx", "modified", "modified_by", "owner"}
		}

		previous_in_import = frappe.flags.in_import
		frappe.flags.in_import = True
		try:
			if frappe.db.exists("Workspace Sidebar", name):
				doc = frappe.get_doc("Workspace Sidebar", name)
				doc.update(doc_data)
				doc.flags.ignore_links = True
				doc.save(ignore_permissions=True)
			else:
				doc = frappe.get_doc(doc_data)
				doc.flags.ignore_links = True
				doc.insert(ignore_permissions=True)
		finally:
			frappe.flags.in_import = previous_in_import

	frappe.db.commit()


def _ensure_desktop_icon():
	"""Recreate the Import Auto desktop icon after dcnet_apps resets icons.

	`dcnet_apps.setup_desk()` deletes all Desktop Icon rows on migrate, then
	recreates its own curated set. Since this module is a separate app, keep its
	entry self-healing here.
	"""
	if not frappe.db.exists("Workspace Sidebar", SIDEBAR_NAME):
		return

	if frappe.db.exists("Workspace", WORKSPACE_NAME):
		frappe.db.set_value("Workspace", WORKSPACE_NAME, "is_hidden", 0, update_modified=False)

	link_type_field = frappe.get_meta("Desktop Icon").get_field("link_type")
	allowed_link_types = (link_type_field.options or "").split("\n") if link_type_field else []
	link_type = "Workspace Sidebar" if "Workspace Sidebar" in allowed_link_types else "Workspace"
	link_to = SIDEBAR_NAME if link_type == "Workspace Sidebar" else WORKSPACE_NAME

	values = {
		"label": "Import Auto",
		"icon_type": "Link",
		"link_type": link_type,
		"link_to": link_to,
		"icon": "upload",
		"idx": 90,
		"hidden": 0,
		"standard": 1,
		"app": "dcnet_migrate",
	}

	if frappe.db.exists("Desktop Icon", ICON_LABEL):
		doc = frappe.get_doc("Desktop Icon", ICON_LABEL)
		doc.update(values)
		doc.flags.ignore_links = True
		doc.save(ignore_permissions=True)
		print(f"  ↻ Desktop Icon: {ICON_LABEL}")
	else:
		doc = frappe.get_doc({"doctype": "Desktop Icon", "name": ICON_LABEL, **values})
		doc.flags.ignore_links = True
		doc.insert(ignore_permissions=True)
		print(f"  ✓ Desktop Icon: {ICON_LABEL}")

	frappe.db.commit()
	frappe.cache.delete_keys("desktop_icons")
	frappe.cache.delete_key("bootinfo")


def _normalize_import_auto_paths():
	"""Move legacy local scan paths to per-document server upload folders."""
	if not frappe.db.table_exists("Import Auto"):
		return

	from dcnet_migrate.import_auto.doctype.import_auto.import_auto import (
		LEGACY_DEFAULT_IMPORT_PATH,
		get_server_upload_folder_path,
	)

	for row in frappe.get_all("Import Auto", fields=["name", "folder_path"]):
		default_server_path = get_server_upload_folder_path(row.name)
		if row.folder_path and row.folder_path != LEGACY_DEFAULT_IMPORT_PATH:
			continue

		frappe.db.set_value(
			"Import Auto",
			row.name,
			{
				"folder_path": default_server_path,
				"recursive": 1,
				"file_pattern": "*.xlsx,*.xls",
			},
			update_modified=False,
		)

	frappe.db.commit()
