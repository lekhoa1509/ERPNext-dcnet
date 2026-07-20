"""Invoices Pending eInvoice — hóa đơn HĐ/PAKD chưa xuất hóa đơn đỏ.

Worklist cho kế toán: mỗi sáng mở report này để biết SI nào đã submit
nhưng chưa xuất hóa đơn điện tử (einvoice_issued=0). Chỉ liệt kê SI gắn
với một Hợp đồng (dcnet_contract is set) — SI lẻ ngoài hợp đồng nằm ở
list view Hoá đơn bán hàng thông thường.
"""

import frappe
from frappe import _


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
		{"label": _("Ngày HĐ"), "fieldname": "posting_date", "fieldtype": "Date", "width": 95},
		{"label": _("Hạn TT"), "fieldname": "due_date", "fieldtype": "Date", "width": 95},
		{"label": _("Tổng tiền"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 130},
		{"label": _("Trạng thái"), "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def _query(filters):
	conditions = [
		"si.docstatus = 1",
		"si.dcnet_contract IS NOT NULL AND si.dcnet_contract != ''",
		"IFNULL(si.einvoice_issued, 0) = 0",
	]
	args = {}
	if filters.get("dcnet_contract"):
		conditions.append("si.dcnet_contract = %(dcnet_contract)s")
		args["dcnet_contract"] = filters["dcnet_contract"]
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")
		args["customer"] = filters["customer"]

	where = " AND ".join(conditions)
	return frappe.db.sql(
		f"""
		SELECT si.name, si.customer, si.dcnet_contract, si.dcnet_pakd,
		       si.billing_period_idx, si.posting_date, si.due_date,
		       si.grand_total, si.status
		FROM `tabSales Invoice` si
		WHERE {where}
		ORDER BY si.due_date ASC, si.name
		""",
		args,
		as_dict=True,
	)
