import frappe


def after_install():
	_ensure_custom_roles()
	try:
		_ensure_settings_singleton()
		_seed_settings_defaults()
		_seed_default_rule_templates()
	except Exception:
		# DocTypes may not be synced yet during first install.
		# after_migrate will seed these after migrate completes.
		pass


def after_migrate():
	_ensure_settings_singleton()
	_seed_default_rule_templates()
	_ensure_pakd_approval_workflow()
	_ensure_pakd_journal_entry_read()
	_ensure_proportional_post_fields()


def _ensure_proportional_post_fields():
	"""Custom Field auto_posted_pct trên Commission Line + Beneficiary Line.

	Track % đã đăng cumulative cho proportional auto-post (KTT click button
	'Tạo draft hoa hồng PAKD' trên PE form). Mỗi lần click, increment delta
	pct được tạo thành draft JE. Khi cumulative = 100% → line state = Posted.
	"""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
	fields_def = [
		{"fieldname": "auto_posted_pct", "label": "Auto-posted %",
		 "fieldtype": "Percent", "insert_after": "state",
		 "read_only": 1, "default": "0",
		 "description": "% đã đăng draft JE cumulative qua PE proportional trigger. KTT review từng draft + submit."},
	]
	targets = {}
	if frappe.db.exists("DocType", "PAKD Commission Line"):
		targets["PAKD Commission Line"] = fields_def
	if frappe.db.exists("DocType", "PAKD Beneficiary Line"):
		targets["PAKD Beneficiary Line"] = fields_def
	if targets:
		create_custom_fields(targets, update=True)


def _ensure_pakd_journal_entry_read():
	"""Grant PAKD oversight roles read+report on Journal Entry, preserving
	all stock ERPNext role permissions.

	IMPORTANT: When ANY Custom DocPerm row exists on a DocType, Frappe IGNORES
	all Standard DocPerm rows entirely. So adding PAKD Board / PAKD Accountant
	rows alone would silently revoke access from Accounts Manager, Accounts
	User, and Auditor (FB-515/516/523/531/532).

	Fix: mirror every Standard DocPerm row into Custom DocPerm first, then add
	the PAKD oversight rows. Idempotent — `frappe.db.exists` short-circuits
	per-role.

	PAKD reports (Commission Register) link to JEs created by the commission
	posting flow via integrations/accounting.py. Without read access, users
	with only PAKD roles hit Frappe's permission gate when clicking a JE link.
	"""
	perm_fields = (
		"read", "write", "create", "delete", "submit", "cancel", "amend",
		"report", "export", "import_", "share", "print", "email",
		"if_owner", "permlevel",
	)
	# IMPORTANT: `import_` in Python -> column name `import` in DB
	db_col = lambda f: "import" if f == "import_" else f

	std_rows = frappe.db.sql(
		"""SELECT role, permlevel, `read`, `write`, `create`, `delete`,
		          `submit`, `cancel`, `amend`, `report`, `export`, `import`,
		          `share`, `print`, `email`, if_owner
		   FROM `tabDocPerm`
		   WHERE parent = %s""",
		("Journal Entry",),
		as_dict=1,
	)

	for row in std_rows:
		if frappe.db.exists("Custom DocPerm", {
			"parent": "Journal Entry",
			"role": row["role"],
			"permlevel": row["permlevel"],
		}):
			continue
		doc = {
			"doctype": "Custom DocPerm",
			"parent": "Journal Entry",
			"parenttype": "DocType",
			"parentfield": "permissions",
			"role": row["role"],
			"permlevel": row["permlevel"],
			"if_owner": row["if_owner"],
		}
		# Mirror every action flag — keys come back un-quoted from the SELECT
		for f in ("read", "write", "create", "delete", "submit", "cancel",
		          "amend", "report", "export", "import", "share", "print", "email"):
			doc[f] = row[f]
		frappe.get_doc(doc).insert(ignore_permissions=True)

	for role in ("PAKD Board", "PAKD Accountant"):
		if frappe.db.exists("Custom DocPerm", {"parent": "Journal Entry", "role": role, "permlevel": 0}):
			continue
		frappe.get_doc({
			"doctype": "Custom DocPerm",
			"parent": "Journal Entry",
			"parenttype": "DocType",
			"parentfield": "permissions",
			"role": role,
			"permlevel": 0,
			"read": 1,
			"report": 1,
		}).insert(ignore_permissions=True)

	frappe.clear_cache(doctype="Journal Entry")
	frappe.db.commit()


def _ensure_custom_roles():
	roles = [
		"PAKD Sales Rep",
		"PAKD Sales Director HCM",
		"PAKD Sales Director HN",
		"PAKD General Department",
		"PAKD Branch Director HN",
		"PAKD Board",
		"PAKD Accountant",
	]
	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(ignore_permissions=True)
	frappe.db.commit()


def _ensure_settings_singleton():
	if not frappe.db.exists("PAKD Settings", "PAKD Settings"):
		doc = frappe.new_doc("PAKD Settings")
		doc.insert(ignore_permissions=True)
		frappe.db.commit()


def _seed_settings_defaults():
	settings = frappe.get_doc("PAKD Settings", "PAKD Settings")

	if not settings.cutoff_day_of_month:
		settings.cutoff_day_of_month = 5

	# VN COA TT99/2025 accounts — match by account_name prefix
	company = frappe.defaults.get_defaults().get("company")
	if company:
		account_map = {
			"account_manager_services": "6418",
			"account_add_costs": "6418",
			"account_gpvt": "6425",
			"counter_account_manager_services": "3388",
			"counter_account_add_costs": "3388",
		}
		for field, prefix in account_map.items():
			if not settings.get(field):
				acc = frappe.db.get_value(
					"Account",
					{"account_name": ["like", f"{prefix} - %"], "company": company, "is_group": 0},
					"name",
				)
				if acc:
					settings.set(field, acc)

		# TK 3338 in TT99/2025 VN COA is a group with leaves 33381/33382.
		# Pick 33382 (Các loại thuế khác) for GPVT payable, fall back to any 3338* leaf.
		if not settings.get("counter_account_gpvt"):
			acc = (
				frappe.db.get_value("Account", {"account_name": ["like", "3338 - %"], "company": company, "is_group": 0}, "name")
				or frappe.db.get_value("Account", {"account_name": ["like", "33382 - %"], "company": company, "is_group": 0}, "name")
			)
			if not acc:
				row = frappe.db.sql(
					"""SELECT name FROM `tabAccount`
					   WHERE company = %s AND is_group = 0 AND account_name LIKE '3338%%'
					   ORDER BY account_name LIMIT 1""",
					(company,),
				)
				acc = row[0][0] if row else None
			if acc:
				settings.set("counter_account_gpvt", acc)

	settings.save(ignore_permissions=True)
	frappe.db.commit()


# Default Rule Templates per spec v3
DEFAULT_TEMPLATES = [
	{
		"template_name": "Recurring Telecom Standard",
		"scope_pakd_type": "Recurring Telecom",
		"components": [
			{"component_name": "Manager Services", "rate": 10.0, "base_formula": "unit_price_minus_add_costs"},
			{"component_name": "Add Costs", "rate": 75.0, "base_formula": "add_costs_gross"},
			{"component_name": "License Fee", "rate": 2.2, "base_formula": "unit_price"},
			{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "unit_price_minus_add_costs"},
		],
	},
	{
		"template_name": "One-off Sale Standard",
		"scope_pakd_type": "One-off Sale/Project",
		"components": [
			{"component_name": "Manager Services", "rate": 10.0, "base_formula": "unit_price_minus_add_costs"},
			{"component_name": "Add Costs", "rate": 75.0, "base_formula": "add_costs_gross"},
			{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "unit_price_minus_add_costs"},
		],
	},
]


def _ensure_pakd_approval_workflow():
	"""Create or recreate the PAKD Approval workflow with English state names."""
	# Delete old workflow if exists (recreate with English states)
	if frappe.db.exists("Workflow", "PAKD Approval"):
		frappe.delete_doc("Workflow", "PAKD Approval", ignore_permissions=True, force=1)

	# Ensure all workflow actions exist
	actions = [
		"Submit for Approval (Staff)",
		"Submit for Approval (Board)",
		"Approve Sales Director",
		"Forward to Branch Director",
		"Forward to Board",
		"Approve Branch Director",
		"Approve Board",
		"Reject",
		"Revise",
	]
	for action in actions:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc({
				"doctype": "Workflow Action Master",
				"workflow_action_name": action,
			}).insert(ignore_permissions=True)

	# Ensure all workflow states exist
	states = [
		"Draft",
		"Pending Sales Director",
		"Pending General Dept",
		"Pending Branch Director",
		"Pending Board",
		"Approved",
		"Rejected",
	]
	state_styles = {
		"Draft": "",
		"Pending Sales Director": "Warning",
		"Pending General Dept": "Warning",
		"Pending Branch Director": "Warning",
		"Pending Board": "Info",
		"Approved": "Success",
		"Rejected": "Danger",
	}
	for state in states:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc({
				"doctype": "Workflow State",
				"workflow_state_name": state,
				"style": state_styles.get(state, "grey"),
			}).insert(ignore_permissions=True)

	# Transitions: (action, state, next_state, allowed_roles, condition)
	transitions = [
		{
			"action": "Submit for Approval (Staff)",
			"state": "Draft",
			"next_state": "Pending Sales Director",
			"allowed": "PAKD Sales Rep",
			"condition": "doc.channel == 'Staff'",
		},
		{
			"action": "Submit for Approval (Board)",
			"state": "Draft",
			"next_state": "Pending General Dept",
			"allowed": "PAKD Sales Rep",
			"condition": "doc.channel == 'Board'",
		},
		{
			"action": "Approve Sales Director",
			"state": "Pending Sales Director",
			"next_state": "Pending General Dept",
			"allowed": "PAKD Sales Director HCM",
			"condition": None,
		},
		{
			"action": "Approve Sales Director",
			"state": "Pending Sales Director",
			"next_state": "Pending General Dept",
			"allowed": "PAKD Sales Director HN",
			"condition": None,
		},
		{
			"action": "Forward to Branch Director",
			"state": "Pending General Dept",
			"next_state": "Pending Branch Director",
			"allowed": "PAKD General Department",
			"condition": "doc.branch == 'HN' and doc.channel == 'Staff'",
		},
		{
			"action": "Forward to Board",
			"state": "Pending General Dept",
			"next_state": "Pending Board",
			"allowed": "PAKD General Department",
			"condition": None,
		},
		{
			"action": "Approve Branch Director",
			"state": "Pending Branch Director",
			"next_state": "Pending Board",
			"allowed": "PAKD Branch Director HN",
			"condition": None,
		},
		{
			"action": "Approve Board",
			"state": "Pending Board",
			"next_state": "Approved",
			"allowed": "PAKD Board",
			"condition": None,
		},
		{
			"action": "Reject",
			"state": "Pending Sales Director",
			"next_state": "Rejected",
			"allowed": "PAKD Sales Director HCM",
			"condition": None,
		},
		{
			"action": "Reject",
			"state": "Pending Sales Director",
			"next_state": "Rejected",
			"allowed": "PAKD Sales Director HN",
			"condition": None,
		},
		{
			"action": "Reject",
			"state": "Pending General Dept",
			"next_state": "Rejected",
			"allowed": "PAKD General Department",
			"condition": None,
		},
		{
			"action": "Reject",
			"state": "Pending Branch Director",
			"next_state": "Rejected",
			"allowed": "PAKD Branch Director HN",
			"condition": None,
		},
		{
			"action": "Reject",
			"state": "Pending Board",
			"next_state": "Rejected",
			"allowed": "PAKD Board",
			"condition": None,
		},
		{
			"action": "Revise",
			"state": "Rejected",
			"next_state": "Draft",
			"allowed": "PAKD Sales Rep",
			"condition": None,
		},
	]

	# Build states list for workflow
	wf_states = []
	for state in states:
		doc_status = "0"
		if state == "Approved":
			doc_status = "1"
		elif state == "Rejected":
			doc_status = "0"
		wf_states.append({
			"state": state,
			"doc_status": doc_status,
			"update_field": "status",
			"update_value": state,
			"allow_edit": _state_edit_role(state),
		})

	# Build transitions list
	wf_transitions = []
	for t in transitions:
		row = {
			"action": t["action"],
			"state": t["state"],
			"next_state": t["next_state"],
			"allowed": t["allowed"],
		}
		if t.get("condition"):
			row["condition"] = t["condition"]
		wf_transitions.append(row)

	wf_doc = frappe.new_doc("Workflow")
	wf_doc.workflow_name = "PAKD Approval"
	wf_doc.document_type = "Phuong An Kinh Doanh"
	wf_doc.is_active = 1
	wf_doc.send_email_alert = 0
	wf_doc.workflow_state_field = "workflow_state"
	for s in wf_states:
		wf_doc.append("states", s)
	for t in wf_transitions:
		wf_doc.append("transitions", t)
	wf_doc.insert(ignore_permissions=True)
	frappe.db.commit()


def _state_edit_role(state):
	"""Return the role allowed to edit the doc at each workflow state.

	In Frappe v16 ``Workflow Document State.allow_edit`` is a Link → Role and
	the runtime check (``frappe.workflow.is_read_only``) does NOT split on
	commas — only a single role name (or the magic role "All") is accepted.

	Draft + Rejected use "All" so DocType permissions determine actual write
	access. Roles with write perm on Phuong An Kinh Doanh (PAKD Sales Rep on
	their own drafts, Sales Director / General Dept / Branch Director / Board,
	and System Manager) can each intervene on a stuck draft.
	Approver states stay locked to the specific reviewer role.
	"""
	return {
		"Draft": "All",
		"Pending Sales Director": "PAKD Sales Director HCM",
		"Pending General Dept": "PAKD General Department",
		"Pending Branch Director": "PAKD Branch Director HN",
		"Pending Board": "PAKD Board",
		"Approved": "System Manager",
		"Rejected": "All",
	}.get(state, "System Manager")


def _seed_default_rule_templates():
	for tpl in DEFAULT_TEMPLATES:
		if frappe.db.exists("PAKD Commission Rule Template", tpl["template_name"]):
			continue
		doc = frappe.new_doc("PAKD Commission Rule Template")
		doc.template_name = tpl["template_name"]
		doc.scope_pakd_type = tpl["scope_pakd_type"]
		for comp in tpl["components"]:
			doc.append("components", comp)
		doc.insert(ignore_permissions=True)
	frappe.db.commit()
