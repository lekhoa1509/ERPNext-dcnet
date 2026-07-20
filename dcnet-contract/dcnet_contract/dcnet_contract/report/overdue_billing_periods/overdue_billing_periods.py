"""Overdue Billing Periods — kỳ thu tiền của Hợp đồng đã quá hạn nhưng chưa thu đủ.

Joins DCNet Contract + DCNet Contract Billing Schedule where state='Overdue',
returns one row per overdue billing period with contract + customer + amount.
"""

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = _columns()
	data = _data(filters)
	return columns, data


def _columns():
	return [
		{"label": _("Hợp đồng"), "fieldname": "contract", "fieldtype": "Link", "options": "DCNet Contract", "width": 150},
		{"label": _("Khách hàng"), "fieldname": "customer_name", "fieldtype": "Data", "width": 220},
		{"label": _("Kỳ"), "fieldname": "month_index", "fieldtype": "Int", "width": 60},
		{"label": _("Từ"), "fieldname": "period_start", "fieldtype": "Date", "width": 100},
		{"label": _("Đến"), "fieldname": "period_end", "fieldtype": "Date", "width": 100},
		{"label": _("Đến hạn"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": _("Số ngày quá hạn"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 130},
		{"label": _("Số tiền"), "fieldname": "amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Hoá đơn"), "fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
		{"label": _("NVKD"), "fieldname": "sales_person_name", "fieldtype": "Data", "width": 160},
		{"label": _("Chi nhánh"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 100},
	]


def _data(filters):
	conditions = []
	values = {}

	if filters.get("company"):
		conditions.append("c.company = %(company)s")
		values["company"] = filters["company"]

	if filters.get("branch"):
		conditions.append("c.branch = %(branch)s")
		values["branch"] = filters["branch"]

	where_extra = (" AND " + " AND ".join(conditions)) if conditions else ""

	return frappe.db.sql(
		f"""
		SELECT
			c.name AS contract,
			c.customer_name,
			c.sales_person_name,
			c.branch,
			bs.month_index,
			bs.period_start,
			bs.period_end,
			bs.due_date,
			DATEDIFF(CURDATE(), bs.due_date) AS days_overdue,
			bs.amount,
			bs.sales_invoice
		FROM `tabDCNet Contract Billing Schedule` bs
		INNER JOIN `tabDCNet Contract` c ON c.name = bs.parent
		WHERE bs.state = 'Overdue'
		  AND c.docstatus = 1
		  {where_extra}
		ORDER BY bs.due_date ASC, c.name
		""",
		values,
		as_dict=True,
	)
