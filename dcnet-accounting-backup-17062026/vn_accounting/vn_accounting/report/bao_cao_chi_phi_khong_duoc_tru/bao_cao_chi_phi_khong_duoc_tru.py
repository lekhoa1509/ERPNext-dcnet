# Copyright (c) 2026, VN Accounting and contributors
# For license information, please see license.txt

"""Báo cáo chi phí không được trừ (TNDN) — chỉ tiêu B4 của Form 03/TNDN.

Aggregates GL Entry rows with is_non_deductible=1 across all source paths
(Journal Entry, Purchase Invoice, Expense Claim, Salary Slip, Depreciation
Entry). Output feeds the B4 line of Form 03/TNDN — điều chỉnh tăng thu nhập
chịu thuế.

Spec: apps/vn_accounting/docs/specs/2026-05-25-non-deductible-expense-tracking.md
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, get_first_day, get_last_day, today


def execute(filters=None):
	filters = filters or {}
	validate_filters(filters)

	columns = get_columns()
	data, total = get_data(filters)
	chart = build_chart(data)
	summary = build_summary(filters, total)

	return columns, data, None, chart, summary


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("Công ty là bắt buộc"))
	if not filters.get("from_date"):
		filters["from_date"] = get_first_day(today()).isoformat()
	if not filters.get("to_date"):
		filters["to_date"] = get_last_day(today()).isoformat()
	if getdate(filters["from_date"]) > getdate(filters["to_date"]):
		frappe.throw(_("Từ ngày phải trước Đến ngày"))


def get_columns():
	return [
		{
			"fieldname": "posting_date",
			"label": _("Ngày"),
			"fieldtype": "Date",
			"width": 95,
		},
		{
			"fieldname": "voucher_type",
			"label": _("Loại CT"),
			"fieldtype": "Link",
			"options": "DocType",
			"width": 130,
		},
		{
			"fieldname": "voucher_no",
			"label": _("Số CT"),
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 170,
		},
		{
			"fieldname": "account",
			"label": _("Tài khoản"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 220,
		},
		{
			"fieldname": "party_type",
			"label": _("Loại bên"),
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"fieldname": "party",
			"label": _("Bên liên quan"),
			"fieldtype": "Dynamic Link",
			"options": "party_type",
			"width": 160,
		},
		{
			"fieldname": "non_deductible_reason",
			"label": _("Lý do"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "debit",
			"label": _("Số tiền"),
			"fieldtype": "Currency",
			"options": "Company:company:default_currency",
			"width": 140,
		},
		{
			"fieldname": "remarks",
			"label": _("Ghi chú"),
			"fieldtype": "Small Text",
			"width": 280,
		},
	]


def get_data(filters):
	conds = ["gle.company = %(company)s",
	         "gle.is_non_deductible = 1",
	         "gle.is_cancelled = 0",
	         "gle.debit > 0",
	         "gle.posting_date BETWEEN %(from_date)s AND %(to_date)s"]
	if filters.get("account"):
		conds.append("gle.account = %(account)s")
	if filters.get("voucher_type"):
		conds.append("gle.voucher_type = %(voucher_type)s")
	if filters.get("non_deductible_reason"):
		conds.append("gle.non_deductible_reason = %(non_deductible_reason)s")

	where = " AND ".join(conds)
	rows = frappe.db.sql(
		f"""SELECT
			gle.posting_date,
			gle.voucher_type,
			gle.voucher_no,
			gle.account,
			gle.party_type,
			gle.party,
			gle.non_deductible_reason,
			gle.debit,
			gle.remarks
		FROM `tabGL Entry` gle
		WHERE {where}
		ORDER BY gle.posting_date, gle.voucher_no, gle.account""",
		filters,
		as_dict=True,
	)

	total = sum(flt(r.debit) for r in rows)

	if rows:
		rows.append({
			"posting_date": None,
			"voucher_type": "",
			"voucher_no": "",
			"account": _("TỔNG CỘNG (B4)"),
			"party_type": "",
			"party": "",
			"non_deductible_reason": "",
			"debit": total,
			"remarks": _("Cộng vào chỉ tiêu B4 của Form 03/TNDN — điều chỉnh tăng thu nhập chịu thuế"),
		})

	return rows, total


def build_chart(data):
	"""Group by reason for stacked-bar chart."""
	if not data:
		return None
	by_reason = {}
	for r in data:
		if not r.get("non_deductible_reason"):
			continue
		key = r["non_deductible_reason"]
		by_reason[key] = by_reason.get(key, 0) + flt(r.get("debit") or 0)
	if not by_reason:
		return None
	labels = sorted(by_reason.keys())
	values = [by_reason[k] for k in labels]
	return {
		"data": {"labels": labels, "datasets": [{"name": _("CP không được trừ"), "values": values}]},
		"type": "bar",
		"barOptions": {"stacked": False},
	}


def build_summary(filters, total):
	from_d = filters.get("from_date") or ""
	to_d = filters.get("to_date") or ""
	return [
		{
			"value": total,
			"label": _("Tổng CP không được trừ (B4)"),
			"datatype": "Currency",
			"indicator": "Red" if total > 0 else "Green",
		},
		{
			"value": f"{from_d} → {to_d}",
			"label": _("Kỳ"),
			"datatype": "Data",
		},
	]
