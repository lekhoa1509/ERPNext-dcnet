"""Invoices Overdue by Contract — hóa đơn HĐ/PAKD quá hạn cần đôn thúc.

Worklist cho kế toán: SI gắn Hợp đồng, status=Overdue, còn nợ > 0.
Cột "Số ngày quá hạn" tính sẵn để kế toán ưu tiên gọi đôn thúc khách nợ
lâu nhất trước.
"""

import frappe
from frappe import _
from frappe.utils import getdate, today


def execute(filters=None):
	filters = filters or {}
	return _columns(), _query(filters)


def _columns():
	return [
		{"label": _("Hóa đơn"), "fieldname": "name", "fieldtype": "Link",
		 "options": "Sales Invoice", "width": 150},
		{"label": _("Khách hàng"), "fieldname": "customer", "fieldtype": "Link",
		 "options": "Customer", "width": 200},
		{"label": _("Hợp đồng"), "fieldname": "dcnet_contract", "fieldtype": "Link",
		 "options": "DCNet Contract", "width": 140},
		{"label": _("PAKD"), "fieldname": "dcnet_pakd", "fieldtype": "Link",
		 "options": "Phuong An Kinh Doanh", "width": 140},
		{"label": _("Kỳ"), "fieldname": "billing_period_idx", "fieldtype": "Int", "width": 50},
		{"label": _("Hạn TT"), "fieldname": "due_date", "fieldtype": "Date", "width": 95},
		{"label": _("Quá hạn (ngày)"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 110},
		{"label": _("Còn nợ"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Tổng tiền"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 130},
	]


def _query(filters):
	conditions = [
		"si.docstatus = 1",
		"si.dcnet_contract IS NOT NULL AND si.dcnet_contract != ''",
		"si.status = 'Overdue'",
		"si.outstanding_amount > 0",
	]
	args = {}
	if filters.get("dcnet_contract"):
		conditions.append("si.dcnet_contract = %(dcnet_contract)s")
		args["dcnet_contract"] = filters["dcnet_contract"]
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")
		args["customer"] = filters["customer"]
	if filters.get("min_days_overdue"):
		conditions.append("DATEDIFF(%(today)s, si.due_date) >= %(min_days_overdue)s")
		args["min_days_overdue"] = filters["min_days_overdue"]
		args["today"] = today()

	where = " AND ".join(conditions)
	rows = frappe.db.sql(
		f"""
		SELECT si.name, si.customer, si.dcnet_contract, si.dcnet_pakd,
		       si.billing_period_idx, si.due_date,
		       si.outstanding_amount, si.grand_total
		FROM `tabSales Invoice` si
		WHERE {where}
		ORDER BY si.due_date ASC, si.name
		""",
		args,
		as_dict=True,
	)
	_today = getdate(today())
	for r in rows:
		r["days_overdue"] = (_today - getdate(r["due_date"])).days if r.get("due_date") else 0
	return rows
