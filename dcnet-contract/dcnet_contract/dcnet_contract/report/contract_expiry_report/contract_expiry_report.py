import frappe
from frappe import _
from frappe.utils import getdate, nowdate, date_diff


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"fieldname": "contract", "label": _("Contract"), "fieldtype": "Link", "options": "DCNet Contract", "width": 150},
		{"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link", "options": "Customer", "width": 200},
		{"fieldname": "service_type", "label": _("Service Type"), "fieldtype": "Data", "width": 120},
		{"fieldname": "branch", "label": _("Branch"), "fieldtype": "Data", "width": 100},
		{"fieldname": "contract_date", "label": _("Start Date"), "fieldtype": "Date", "width": 110},
		{"fieldname": "end_date", "label": _("End Date"), "fieldtype": "Date", "width": 110},
		{"fieldname": "days_remaining", "label": _("Days Remaining"), "fieldtype": "Int", "width": 120},
		{"fieldname": "grand_total", "label": _("Contract Value"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	today = getdate(nowdate())

	# Get notification days from settings, default 30
	expiry_days = filters.get("expiry_days")
	if not expiry_days:
		expiry_days = frappe.db.get_single_value(
			"DCNet Contract Settings", "expiry_notification_days"
		) or 30

	conditions = [
		"c.docstatus = 1",
		"c.status = 'Active'",
		"c.end_date IS NOT NULL",
		"c.end_date <= %(cutoff_date)s",
		"c.end_date >= %(today)s",
	]
	values = {
		"today": today,
		"cutoff_date": frappe.utils.add_days(today, int(expiry_days)),
	}

	if filters.get("customer"):
		conditions.append("c.customer = %(customer)s")
		values["customer"] = filters["customer"]

	if filters.get("branch"):
		conditions.append("c.branch = %(branch)s")
		values["branch"] = filters["branch"]

	if filters.get("service_type"):
		conditions.append("c.service_type = %(service_type)s")
		values["service_type"] = filters["service_type"]

	where_clause = " AND ".join(conditions)

	rows = frappe.db.sql(f"""
		SELECT
			c.name AS contract,
			c.customer,
			c.service_type,
			c.branch,
			c.contract_date,
			c.end_date,
			c.grand_total,
			c.status
		FROM `tabDCNet Contract` c
		WHERE {where_clause}
		ORDER BY c.end_date ASC
	""", values, as_dict=True)

	for row in rows:
		row["days_remaining"] = date_diff(row["end_date"], today)

	return rows
