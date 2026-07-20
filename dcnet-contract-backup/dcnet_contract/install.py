import json
import os

import frappe


def after_install():
	_ensure_custom_roles()
	_ensure_settings_singleton()
	_seed_settings_defaults()
	_ensure_shadow_so_custom_field()
	_ensure_customer_cmnd_fields()
	_seed_contract_templates()
	_seed_docx_templates()
	_sync_standard_docs()
	_fix_workspace_labels()
	_sync_workspace_sidebar()
	_ensure_desktop_icon()


def after_migrate():
	_ensure_custom_roles()
	_ensure_settings_singleton()
	_ensure_shadow_so_custom_field()
	_ensure_customer_cmnd_fields()
	_seed_contract_templates()
	_seed_docx_templates()
	_sync_standard_docs()
	_fix_workspace_labels()
	_sync_workspace_sidebar()
	_ensure_desktop_icon()
	_migrate_templates_to_dual_format()


def _ensure_custom_roles():
	for role_name in ["DCNet Sales Rep", "DCNet Sales Manager", "Contract Template Manager"]:
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(ignore_permissions=True)
	frappe.db.commit()


def _ensure_settings_singleton():
	if not frappe.db.exists("DCNet Contract Settings", "DCNet Contract Settings"):
		doc = frappe.new_doc("DCNet Contract Settings")
		doc.insert(ignore_permissions=True)
		frappe.db.commit()


def _ensure_shadow_so_custom_field():
	"""Add is_shadow_contract custom field to Sales Order."""
	field_name = "Sales Order-is_shadow_contract"
	if not frappe.db.exists("Custom Field", field_name):
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Sales Order",
			"fieldname": "is_shadow_contract",
			"fieldtype": "Check",
			"label": "Is Shadow Contract",
			"insert_after": "order_type",
			"read_only": 1,
			"hidden": 1,
			"default": "0",
			"owner": "Administrator",
		}).insert(ignore_permissions=True)
		frappe.db.commit()


def _seed_settings_defaults():
	settings = frappe.get_doc("DCNet Contract Settings", "DCNet Contract Settings")

	if not settings.default_rounding_mode:
		settings.default_rounding_mode = "Half-up"
	if not settings.overdue_grace_period_days:
		settings.overdue_grace_period_days = 15
	if not settings.expiry_notification_days:
		settings.expiry_notification_days = 30
	if not settings.proration_formula:
		settings.proration_formula = "days_in_month"

	if not settings.default_payment_terms:
		pt = frappe.db.get_value("Payment Terms Template", {}, "name")
		if pt:
			settings.default_payment_terms = pt

	if not settings.get("branch_cost_center_map"):
		for branch_name in ["HCM", "HN"]:
			if frappe.db.exists("Branch", branch_name):
				cc = frappe.db.get_value("Cost Center", {"branch": branch_name}, "name")
				if cc:
					settings.append("branch_cost_center_map", {"branch": branch_name, "cost_center": cc})

	settings.save(ignore_permissions=True)
	frappe.db.commit()


CUSTOMER_CMND_FIELDS = [
	{"fieldname": "customer_id_number", "label": "Số CMND/CCCD", "fieldtype": "Data", "insert_after": "tax_id"},
	{"fieldname": "customer_id_date", "label": "Ngày cấp CMND", "fieldtype": "Date", "insert_after": "customer_id_number"},
	{"fieldname": "customer_id_place", "label": "Nơi cấp CMND", "fieldtype": "Data", "insert_after": "customer_id_place"},
	{"fieldname": "customer_dob", "label": "Ngày sinh", "fieldtype": "Date", "insert_after": "customer_id_place"},
]


def _ensure_customer_cmnd_fields():
	"""Add CMND/CCCD custom fields to Customer DocType for FTTH HGD contracts."""
	for field_def in CUSTOMER_CMND_FIELDS:
		cf_name = f"Customer-{field_def['fieldname']}"
		if not frappe.db.exists("Custom Field", cf_name):
			frappe.get_doc({
				"doctype": "Custom Field",
				"dt": "Customer",
				"module": "DCNet Contract",
				"owner": "Administrator",
				**field_def,
			}).insert(ignore_permissions=True)
	frappe.db.commit()


TEMPLATES = [
	{"template_name": "P2P chuẩn", "service_type": "P2P", "contract_type": "Recurring", "payment_mode": "Monthly", "package_term_months": 12, "items": [{"item_label": "Kênh P2P", "qty": 1, "unit_price": 0}]},
	{"template_name": "MPLS chuẩn", "service_type": "MPLS", "contract_type": "Recurring", "payment_mode": "Monthly", "package_term_months": 12, "items": [{"item_label": "Kênh MPLS", "qty": 1, "unit_price": 0}]},
	{"template_name": "ILL chuẩn", "service_type": "ILL", "contract_type": "Recurring", "payment_mode": "Monthly", "package_term_months": 12, "items": [{"item_label": "Kênh ILL", "qty": 1, "unit_price": 0}]},
	{"template_name": "FTTH DN chuẩn", "service_type": "FTTH DN", "contract_type": "Recurring", "payment_mode": "Monthly", "package_term_months": 12, "items": [{"item_label": "FTTH Doanh nghiệp", "qty": 1, "unit_price": 0}]},
	{"template_name": "IT Managed chuẩn", "service_type": "IT Managed", "contract_type": "Recurring", "payment_mode": "Monthly", "package_term_months": 12, "items": [{"item_label": "Dịch vụ IT Managed", "qty": 1, "unit_price": 0}]},
	{"template_name": "VTTB chuẩn", "service_type": "VTTB", "contract_type": "One-off", "payment_mode": "OneOff", "items": [{"item_label": "Vật tư thiết bị", "qty": 1, "unit_price": 0}]},
	{"template_name": "Thi công chuẩn", "service_type": "Thi công", "contract_type": "One-off", "payment_mode": "OneOff", "items": [{"item_label": "Thi công hạ tầng", "qty": 1, "unit_price": 0}]},
	{"template_name": "Hợp đồng chung", "service_type": "", "contract_type": "", "payment_mode": "", "items": [{"item_label": "Dịch vụ", "qty": 1, "unit_price": 0}]},
]


def _seed_contract_templates():
	for tpl in TEMPLATES:
		if frappe.db.exists("DCNet Contract Template", tpl["template_name"]):
			continue
		doc = frappe.new_doc("DCNet Contract Template")
		doc.template_name = tpl["template_name"]
		doc.service_type = tpl.get("service_type", "")
		doc.contract_type = tpl.get("contract_type", "")
		doc.payment_mode = tpl.get("payment_mode", "")
		doc.package_term_months = tpl.get("package_term_months", 0)
		for item in tpl.get("items", []):
			doc.append("default_items", item)
		doc.insert(ignore_permissions=True)
	frappe.db.commit()


DOCX_TEMPLATES = [
	{
		"template_name": "HD Dich vu Vien thong",
		"template_category": "H\u1ee3p \u0111\u1ed3ng",
		"service_type": "",
		"contract_type": "Recurring",
		"payment_mode": "Monthly",
		"docx_file": "hd-dich-vu-vien-thong.docx",
	},
	{
		"template_name": "HD FTTH Doanh nghiep",
		"template_category": "H\u1ee3p \u0111\u1ed3ng",
		"service_type": "FTTH DN",
		"contract_type": "Recurring",
		"payment_mode": "Monthly",
		"docx_file": "hd-ftth-doanh-nghiep.docx",
	},
	{
		"template_name": "HD FTTH Ho gia dinh",
		"template_category": "H\u1ee3p \u0111\u1ed3ng",
		"service_type": "FTTH DN",
		"contract_type": "Recurring",
		"payment_mode": "Monthly",
		"docx_file": "hd-ftth-ho-gia-dinh.docx",
	},
	{
		"template_name": "PL Kenh thue rieng P2P",
		"template_category": "Ph\u1ee5 l\u1ee5c",
		"service_type": "P2P",
		"contract_type": "Recurring",
		"payment_mode": "Monthly",
		"docx_file": "pl-kenh-thue-rieng-p2p.docx",
	},
	{
		"template_name": "PL Internet Leased Line",
		"template_category": "Ph\u1ee5 l\u1ee5c",
		"service_type": "ILL",
		"contract_type": "Recurring",
		"payment_mode": "Monthly",
		"docx_file": "pl-internet-leased-line-ill.docx",
	},
	{
		"template_name": "PL Truyen so lieu MPLS",
		"template_category": "Ph\u1ee5 l\u1ee5c",
		"service_type": "MPLS",
		"contract_type": "Recurring",
		"payment_mode": "Monthly",
		"docx_file": "pl-truyen-so-lieu-mpls.docx",
	},
]


def _seed_docx_templates():
	"""Seed 6 default docx templates with attached .docx files."""
	app_path = os.path.dirname(__file__)
	docx_dir = os.path.join(app_path, "dcnet_contract", "templates", "docx")

	if not os.path.isdir(docx_dir):
		return

	for tpl in DOCX_TEMPLATES:
		tpl_name = tpl["template_name"]
		docx_file = tpl["docx_file"]
		docx_path = os.path.join(docx_dir, docx_file)

		if not os.path.isfile(docx_path):
			continue

		# Create or update template record
		if not frappe.db.exists("DCNet Contract Template", tpl_name):
			doc = frappe.new_doc("DCNet Contract Template")
			doc.template_name = tpl_name
			doc.template_category = tpl.get("template_category", "")
			doc.service_type = tpl.get("service_type", "")
			doc.contract_type = tpl.get("contract_type", "")
			doc.payment_mode = tpl.get("payment_mode", "")
			doc.flags.ignore_permissions = True
			doc.flags.ignore_validate = True
			doc.insert()
			frappe.db.commit()

		template = frappe.get_doc("DCNet Contract Template", tpl_name)

		# Attach or update .docx file — always re-upload if disk file changed
		with open(docx_path, "rb") as f:
			content = f.read()

		needs_upload = True
		if template.template_file:
			try:
				existing_file = frappe.get_doc("File", {"file_url": template.template_file})
				existing_content = open(existing_file.get_full_path(), "rb").read()
				if existing_content == content:
					needs_upload = False
			except Exception:
				pass  # file missing or corrupt — re-upload

		if needs_upload:
			# Delete old file attachment if exists
			if template.template_file:
				try:
					old_file = frappe.get_doc("File", {"file_url": template.template_file})
					old_file.flags.ignore_permissions = True
					old_file.delete()
				except Exception:
					pass

			file_doc = frappe.get_doc({
				"doctype": "File",
				"file_name": docx_file,
				"content": content,
				"attached_to_doctype": "DCNet Contract Template",
				"attached_to_name": tpl_name,
				"is_private": 1,
			})
			file_doc.flags.ignore_permissions = True
			file_doc.save()

			template.template_file = file_doc.file_url
			template.flags.ignore_permissions = True
			template.save()
			frappe.db.commit()

	frappe.db.commit()


def _sync_standard_docs():
	"""Upsert Number Card and Dashboard Chart from JSON files."""
	app_path = os.path.dirname(__file__)
	for doctype, folder in [
		("Number Card", "number_card"),
		("Dashboard Chart", "dashboard_chart"),
	]:
		folder_path = os.path.join(app_path, "dcnet_contract", folder)
		if not os.path.isdir(folder_path):
			continue
		for subfolder in os.listdir(folder_path):
			json_path = os.path.join(folder_path, subfolder, f"{subfolder}.json")
			if not os.path.isfile(json_path):
				continue
			with open(json_path) as f:
				data = json.load(f)
			name = data.get("name")
			if not name:
				continue

			if frappe.db.exists(doctype, name):
				skip = {"doctype", "creation", "modified", "modified_by", "owner", "idx", "name"}
				for field, val in data.items():
					if field not in skip and not isinstance(val, (list, dict)):
						frappe.db.set_value(doctype, name, field, val, update_modified=False)
			else:
				doc = frappe.get_doc(data)
				doc.flags.ignore_permissions = True
				doc.flags.ignore_links = True
				doc.flags.ignore_validate = True
				doc.insert()
	frappe.db.commit()


def _fix_workspace_labels():
	"""Ensure workspace title/label are ASCII for correct URL slug generation."""
	if frappe.db.exists("Workspace", "DCNet Contract"):
		ws = frappe.get_doc("Workspace", "DCNet Contract")
		ws.title = "DCNET Contract"
		ws.label = "DCNET Contract"
		ws.public = 1
		ws.is_hidden = 0
		if not ws.type:
			ws.type = "Workspace"
		ws.flags.ignore_permissions = True
		ws.flags.ignore_links = True
		ws.save()

	if frappe.db.exists("Workspace Sidebar", "DCNet Contract"):
		sidebar = frappe.get_doc("Workspace Sidebar", "DCNet Contract")
		sidebar.title = "DCNET Contract"
		sidebar.module = "DCNet Contract"
		sidebar.flags.ignore_permissions = True
		sidebar.flags.ignore_links = True
		sidebar.save()

	frappe.db.commit()


def _sync_workspace_sidebar():
	"""Re-sync Workspace Sidebar items from JSON fixture."""
	app_path = os.path.dirname(__file__)
	sidebar_json = os.path.join(app_path, "workspace_sidebar", "dcnet_contract.json")
	if not os.path.isfile(sidebar_json):
		return
	if not frappe.db.exists("Workspace Sidebar", "DCNet Contract"):
		return

	with open(sidebar_json) as f:
		data = json.load(f)

	doc = frappe.get_doc("Workspace Sidebar", "DCNet Contract")
	doc.set("items", data.get("items", []))
	doc.flags.ignore_permissions = True
	doc.flags.ignore_links = True
	doc.save()
	frappe.db.commit()


def _ensure_desktop_icon():
	"""Create/update Desktop Icon for DCNET Contract on Desk home.

	Display label is "DCNET" (brand). Workspace Sidebar primary key remains
	"DCNet Contract" (kept for stability — every code reference uses that name).
	"""
	display_label = "DCNET Contract"
	sidebar_name = "DCNet Contract"
	desired = {
		"label": display_label,
		"icon": "file",
		"link_type": "Workspace Sidebar",
		"link_to": sidebar_name,
		"hidden": 0,
	}

	# Clean up the legacy "DCNet Contract" icon row from earlier installs
	# so the new label takes the unique slot.
	legacy = frappe.db.get_value("Desktop Icon", {"label": "DCNet Contract"}, "name")
	if legacy and legacy != display_label:
		frappe.delete_doc("Desktop Icon", legacy, force=True, ignore_permissions=True)

	if frappe.db.exists("Desktop Icon", {"label": display_label}):
		name = frappe.db.get_value("Desktop Icon", {"label": display_label}, "name")
		doc = frappe.get_doc("Desktop Icon", name)
		changed = False
		for field, val in desired.items():
			if doc.get(field) != val:
				doc.set(field, val)
				changed = True
		if changed:
			doc.flags.ignore_permissions = True
			doc.save()
			frappe.db.commit()
		return

	doc = frappe.get_doc({
		"doctype": "Desktop Icon",
		"parent_icon": "",
		**desired,
	})
	doc.flags.ignore_permissions = True
	doc.insert()
	frappe.db.commit()


def _migrate_templates_to_dual_format():
	"""Migrate existing templates: mammoth → template_html, set status=Approved, version=1."""
	try:
		import mammoth
	except ImportError:
		return

	templates = frappe.get_all(
		"DCNet Contract Template",
		filters={"template_file": ["is", "set"]},
		fields=["name", "template_file", "template_html", "status", "version"],
	)

	for t in templates:
		if t.template_html:
			continue  # already migrated

		doc = frappe.get_doc("DCNet Contract Template", t.name)
		file_path = doc._get_template_file_path() if hasattr(doc, "_get_template_file_path") else None

		if not file_path:
			continue

		try:
			with open(file_path, "rb") as f:
				result = mammoth.convert_to_html(f)
				template_html = result.value
		except Exception as e:
			frappe.log_error(f"Failed to convert template {t.name}: {e}")
			continue

		from dcnet_contract.dcnet_contract.utils.placeholder_engine import (
			extract_placeholders_from_html,
			generate_placeholder_guide_html,
		)

		keys = extract_placeholders_from_html(template_html)
		guide_html = generate_placeholder_guide_html(keys)

		frappe.db.set_value(
			"DCNet Contract Template",
			t.name,
			{
				"template_html": template_html,
				"placeholder_guide_html": guide_html,
				"status": "Approved" if (not t.status or t.status == "Draft") else t.status,
				"version": t.version or 1,
			},
			update_modified=False,
		)

	frappe.db.commit()
