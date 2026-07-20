import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"fieldname": "customer", "label": _("Khách hàng"), "fieldtype": "Link", "options": "Customer", "width": 200},
		{"fieldname": "contract", "label": _("Hợp đồng"), "fieldtype": "Link", "options": "DCNet Contract", "width": 150},
		{"fieldname": "service_type", "label": _("Loại dịch vụ"), "fieldtype": "Data", "width": 120},
		{"fieldname": "branch", "label": _("Chi nhánh"), "fieldtype": "Data", "width": 100},
		{"fieldname": "period_start", "label": _("Từ ngày"), "fieldtype": "Date", "width": 110},
		{"fieldname": "period_end", "label": _("Đến ngày"), "fieldtype": "Date", "width": 110},
		{"fieldname": "due_date", "label": _("Hạn thanh toán"), "fieldtype": "Date", "width": 110},
		{"fieldname": "amount", "label": _("Số tiền"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "state", "label": _("Trạng thái"), "fieldtype": "Data", "width": 100},
		{"fieldname": "sales_invoice", "label": _("Hóa đơn"), "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
	]


def get_data(filters):
	conditions = ["c.docstatus = 1"]
	values = {}

	if filters.get("customer"):
		conditions.append("c.customer = %(customer)s")
		values["customer"] = filters["customer"]

	if filters.get("branch"):
		conditions.append("c.branch = %(branch)s")
		values["branch"] = filters["branch"]

	if filters.get("service_type"):
		conditions.append("c.service_type = %(service_type)s")
		values["service_type"] = filters["service_type"]

	if filters.get("status"):
		conditions.append("bs.state = %(status)s")
		values["status"] = filters["status"]
	else:
		conditions.append("bs.state IN ('Projected', 'Invoiced', 'Overdue')")

	if filters.get("from_date"):
		conditions.append("bs.due_date >= %(from_date)s")
		values["from_date"] = getdate(filters["from_date"])

	if filters.get("to_date"):
		conditions.append("bs.due_date <= %(to_date)s")
		values["to_date"] = getdate(filters["to_date"])

	where_clause = " AND ".join(conditions)

	return frappe.db.sql(f"""
		SELECT
			c.customer,
			c.name AS contract,
			c.service_type,
			c.branch,
			bs.period_start,
			bs.period_end,
			bs.due_date,
			bs.amount,
			bs.state,
			bs.sales_invoice
		FROM `tabDCNet Contract Billing Schedule` bs
		JOIN `tabDCNet Contract` c ON c.name = bs.parent
		WHERE {where_clause}
		ORDER BY c.customer, c.name, bs.due_date
	""", values, as_dict=True)
