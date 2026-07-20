"""Invoices to Post — hóa đơn HĐ/PAKD dạng nháp chờ ghi sổ.

Worklist cho kế toán: hóa đơn được scheduler sinh tự động từ hợp đồng khi
thuê bao đến kỳ hạn (run_auto_invoice) được để dạng nháp (docstatus=0).
Kế toán mở report này để review + ghi sổ (submit) — sau đó mới xuất hóa
đơn VAT chính thức. Chỉ liệt kê SI gắn với một Hợp đồng (dcnet_contract
is set); SI nháp lẻ ngoài hợp đồng nằm ở list view Hoá đơn bán hàng.

Cột "Chờ ghi sổ (ngày)" tính sẵn để kế toán ưu tiên ghi sổ hóa đơn tồn
nháp lâu nhất trước.
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
		{"label": _("Ngày HĐ"), "fieldname": "posting_date", "fieldtype": "Date", "width": 95},
		{"label": _("Ngày tạo nháp"), "fieldname": "created_date", "fieldtype": "Date", "width": 105},
		{"label": _("Chờ ghi sổ (ngày)"), "fieldname": "days_waiting", "fieldtype": "Int", "width": 130},
		{"label": _("Tổng tiền"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 130},
	]


def _query(filters):
	conditions = [
		"si.docstatus = 0",
		"si.dcnet_contract IS NOT NULL AND si.dcnet_contract != ''",
	]
	args = {}
	if filters.get("dcnet_contract"):
		conditions.append("si.dcnet_contract = %(dcnet_contract)s")
		args["dcnet_contract"] = filters["dcnet_contract"]
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")
		args["customer"] = filters["customer"]

	where = " AND ".join(conditions)
	rows = frappe.db.sql(
		f"""
		SELECT si.name, si.customer, si.dcnet_contract, si.dcnet_pakd,
		       si.billing_period_idx, si.posting_date,
		       DATE(si.creation) AS created_date, si.grand_total
		FROM `tabSales Invoice` si
		WHERE {where}
		ORDER BY si.creation ASC, si.name
		""",
		args,
		as_dict=True,
	)
	_today = getdate(today())
	for r in rows:
		r["days_waiting"] = (_today - getdate(r["created_date"])).days if r.get("created_date") else 0
	return rows
