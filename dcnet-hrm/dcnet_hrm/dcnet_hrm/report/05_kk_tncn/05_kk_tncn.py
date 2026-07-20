# Copyright (c) 2026, DCNet and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from dcnet_hrm import constants as const


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"fieldname": "employee", "label": _("Employee"), "fieldtype": "Link", "options": "Employee", "width": 120},
		{"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 180},
		{"fieldname": "personal_tax_code", "label": _("Personal Tax Code"), "fieldtype": "Data", "width": 130},
		{
			"fieldname": "total_taxable_income",
			"label": _("Total Taxable Income"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{"fieldname": "tax_withheld", "label": _("Tax Withheld"), "fieldtype": "Currency", "width": 130},
	]


def get_data(filters):
	conditions = ["ss.docstatus = 1"]
	values = {}

	if filters.get("company"):
		conditions.append("ss.company = %(company)s")
		values["company"] = filters["company"]
	if filters.get("from_date"):
		conditions.append("ss.start_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("ss.end_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	where_clause = " AND ".join(conditions)

	rows = frappe.db.sql(
		f"""
		SELECT
			ss.employee AS employee,
			ss.employee_name AS employee_name,
			emp.personal_tax_code AS personal_tax_code,
			SUM(ss.taxable_income) AS total_taxable_income,
			SUM(sd.amount) AS tax_withheld
		FROM `tabSalary Slip` ss
		INNER JOIN `tabSalary Detail` sd
			ON sd.parent = ss.name AND sd.parentfield = 'deductions' AND sd.salary_component = %(pit_component)s
		LEFT JOIN `tabEmployee` emp ON emp.name = ss.employee
		WHERE {where_clause}
		GROUP BY ss.employee
		ORDER BY ss.employee_name
		""",
		{**values, "pit_component": const.PIT_COMPONENT},
		as_dict=True,
	)
	return rows
