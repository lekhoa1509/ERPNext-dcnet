"""Payments by Contract — phiếu thu tiền gắn với Hợp đồng/PAKD.

Mọi Payment Entry mang custom field dcnet_contract — kế toán xem dòng tiền
thực thu theo từng HĐ, đối chiếu với hóa đơn đã xuất + nền tảng để hệ
thống fire cash-basis commission posting. SI/PE lẻ ngoài hợp đồng nằm ở
list view Payment Entry thông thường.
"""

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return _columns(), _query(filters)


def _columns():
	return [
		{"label": _("Phiếu thu"), "fieldname": "name", "fieldtype": "Link",
		 "options": "Payment Entry", "width": 150},
		{"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 95},
		{"label": _("Khách hàng"), "fieldname": "party", "fieldtype": "Link",
		 "options": "Customer", "width": 200},
		{"label": _("Hợp đồng"), "fieldname": "dcnet_contract", "fieldtype": "Link",
		 "options": "DCNet Contract", "width": 140},
		{"label": _("PAKD"), "fieldname": "dcnet_pakd", "fieldtype": "Link",
		 "options": "Phuong An Kinh Doanh", "width": 140},
		{"label": _("Kỳ"), "fieldname": "billing_period_idx", "fieldtype": "Int", "width": 50},
		{"label": _("Số tiền thu"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 140},
		{"label": _("Hình thức"), "fieldname": "mode_of_payment", "fieldtype": "Data", "width": 130},
		{"label": _("Tham chiếu"), "fieldname": "reference_no", "fieldtype": "Data", "width": 150},
	]


def _query(filters):
	conditions = [
		"pe.docstatus = 1",
		"pe.payment_type = 'Receive'",
		"pe.dcnet_contract IS NOT NULL AND pe.dcnet_contract != ''",
	]
	args = {}
	if filters.get("dcnet_contract"):
		conditions.append("pe.dcnet_contract = %(dcnet_contract)s")
		args["dcnet_contract"] = filters["dcnet_contract"]
	if filters.get("dcnet_pakd"):
		conditions.append("pe.dcnet_pakd = %(dcnet_pakd)s")
		args["dcnet_pakd"] = filters["dcnet_pakd"]
	if filters.get("from_date"):
		conditions.append("pe.posting_date >= %(from_date)s")
		args["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("pe.posting_date <= %(to_date)s")
		args["to_date"] = filters["to_date"]

	where = " AND ".join(conditions)
	return frappe.db.sql(
		f"""
		SELECT pe.name, pe.posting_date, pe.party, pe.dcnet_contract, pe.dcnet_pakd,
		       pe.billing_period_idx, pe.paid_amount, pe.mode_of_payment, pe.reference_no
		FROM `tabPayment Entry` pe
		WHERE {where}
		ORDER BY pe.posting_date DESC, pe.name
		""",
		args,
		as_dict=True,
	)
