# Copyright (c) 2026, VN Accounting and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("Công ty là bắt buộc"))
	if filters.get("from_date") and filters.get("to_date"):
		if getdate(filters["from_date"]) > getdate(filters["to_date"]):
			frappe.throw(_("Từ ngày phải trước Đến ngày"))


def get_columns():
	return [
		{
			"fieldname": "posting_date",
			"label": _("Ngày"),
			"fieldtype": "Date",
			"width": 100,
			"description": _("Ngày hạch toán bút toán"),
		},
		{
			"fieldname": "voucher_no",
			"label": _("Số CT"),
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 160,
			"description": _("Số chứng từ gốc tạo ra chi phí này (hóa đơn, phiếu chi, ...)"),
		},
		{
			"fieldname": "voucher_type",
			"label": _("Loại CT"),
			"fieldtype": "Link",
			"options": "DocType",
			"width": 130,
			"description": _("Loại chứng từ: Purchase Invoice, Payment Entry, Journal Entry..."),
		},
		{
			"fieldname": "party",
			"label": _("Nhà cung cấp"),
			"fieldtype": "Data",
			"width": 160,
			"description": _("Tên nhà cung cấp vận chuyển / hải quan / bảo hiểm"),
		},
		{
			"fieldname": "account",
			"label": _("TK"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 160,
			"description": _("Tài khoản treo chi phí chờ phân bổ (thường là 1388 - Chi phí chờ phân bổ hoặc 331)"),
		},
		{
			"fieldname": "amount",
			"label": _("Số tiền"),
			"fieldtype": "Currency",
			"width": 120,
			"description": _("Số tiền chi phí chưa phân bổ vào giá vốn"),
		},
		{
			"fieldname": "remarks",
			"label": _("Diễn giải"),
			"fieldtype": "Data",
			"width": 220,
			"description": _("Nội dung giao dịch từ chứng từ gốc"),
		},
	]


def get_data(filters):
	conditions = "AND gle.is_cancelled = 0 AND gle.debit > 0"
	values = {"company": filters["company"]}

	if filters.get("from_date"):
		conditions += " AND gle.posting_date >= %(from_date)s"
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions += " AND gle.posting_date <= %(to_date)s"
		values["to_date"] = filters["to_date"]

	if filters.get("account"):
		conditions += " AND gle.account = %(account)s"
		values["account"] = filters["account"]
	else:
		# Default: show accounts in 1388 family (chi phí chờ phân bổ)
		conditions += " AND (gle.account LIKE %(account_prefix)s)"
		values["account_prefix"] = "1388%"

	rows = frappe.db.sql(
		"""
		SELECT
			gle.posting_date,
			gle.voucher_no,
			gle.voucher_type,
			gle.party,
			gle.account,
			gle.debit AS amount,
			gle.remarks
		FROM `tabGL Entry` gle
		WHERE gle.company = %(company)s
		{conditions}
		ORDER BY gle.posting_date ASC, gle.creation ASC
		""".format(conditions=conditions),
		values,
		as_dict=True,
	)

	# Highlight rows where amount > 0 (all rows here, but add indicator)
	result = []
	for row in rows:
		result.append(
			{
				"posting_date": row.posting_date,
				"voucher_no": row.voucher_no,
				"voucher_type": row.voucher_type,
				"party": row.party or "",
				"account": row.account,
				"amount": flt(row.amount),
				"remarks": row.remarks or "",
			}
		)

	return result
