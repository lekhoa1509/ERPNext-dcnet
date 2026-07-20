import frappe


def ensure_customer(name="_Test DCNet Customer"):
	if not frappe.db.exists("Customer", name):
		frappe.get_doc({
			"doctype": "Customer",
			"customer_name": name,
			"customer_group": frappe.db.get_single_value("Selling Settings", "customer_group")
				or frappe.db.get_value("Customer Group", {"is_group": 0}, "name"),
			"territory": frappe.db.get_single_value("Selling Settings", "territory")
				or frappe.db.get_value("Territory", {"is_group": 0}, "name"),
		}).insert(ignore_permissions=True)
	return name


def ensure_employee(name="_Test Sales Rep HCM"):
	if frappe.db.exists("Employee", {"employee_name": name}):
		return frappe.db.get_value("Employee", {"employee_name": name}, "name")
	company = (
		frappe.db.get_single_value("Global Defaults", "default_company")
		or frappe.db.get_value("Company", {}, "name")
	)
	doc = frappe.get_doc({
		"doctype": "Employee",
		"employee_name": name,
		"first_name": name,
		"company": company,
		"status": "Active",
		"gender": "Male",
		"date_of_birth": "1990-01-01",
		"date_of_joining": "2020-01-01",
	}).insert(ignore_permissions=True)
	return doc.name


def ensure_branch(name="HCM"):
	if not frappe.db.exists("Branch", name):
		frappe.get_doc({"doctype": "Branch", "branch": name}).insert(ignore_permissions=True)
	return name


def ensure_cost_center_mapping(branch="HCM"):
	"""Ensure DCNet Contract Settings has a branch→cost_center mapping for integration tests."""
	company = (
		frappe.db.get_single_value("Global Defaults", "default_company")
		or frappe.db.get_value("Company", {}, "name")
	)
	# Find any leaf cost center
	cc = frappe.db.get_value("Cost Center", {"company": company, "is_group": 0}, "name")
	if not cc:
		return

	settings = frappe.get_doc("DCNet Contract Settings", "DCNet Contract Settings")
	# Check if mapping already exists for this branch
	for row in settings.get("branch_cost_center_map", []):
		if row.branch == branch:
			return
	settings.append("branch_cost_center_map", {"branch": branch, "cost_center": cc})
	settings.save(ignore_permissions=True)


def ensure_item(name="_Test VTTB Router", uom="Nos"):
	if not frappe.db.exists("Item", name):
		frappe.get_doc({
			"doctype": "Item",
			"item_code": name,
			"item_name": name,
			"item_group": frappe.db.get_value("Item Group", {"is_group": 0}, "name") or "All Item Groups",
			"stock_uom": uom,
		}).insert(ignore_permissions=True)
	return name


def make_active_contract(customer, sales_person, **kwargs):
	defaults = {
		"doctype": "DCNet Contract",
		"customer": customer,
		"sales_person": sales_person,
		"branch": "HCM",
		"contract_type": "Recurring",
		"service_type": "P2P",
		"project_category": "Telecom",
		"payment_mode": "Monthly",
		"package_term_months": 12,
		"contract_date": "2026-01-01",
		"acceptance_date": "2026-01-01",
		"items": [{"item_label": "P2P HCM-HN 100M", "qty": 1, "unit_price": 10500}],
	}
	defaults.update(kwargs)
	doc = frappe.get_doc(defaults).insert(ignore_permissions=True)
	doc.submit()
	doc.reload()
	return doc
