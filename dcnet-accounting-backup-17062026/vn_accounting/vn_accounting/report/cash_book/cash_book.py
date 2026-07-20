# Copyright (c) 2026, Long and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _

from vn_accounting.vn_accounting.report_utils import (
	CASH_PREFIX,
	build_summary_cards,
	extract_account_numbers,
	get_accounts_by_prefix,
	get_opening_balance,
	get_transactions,
)


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns()
	data = get_data(filters)

	# Summary rows matched by label (Số dư đầu kỳ at top; Cộng phát sinh / Số dư
	# cuối kỳ at the bottom of the table) so the cards stay correct regardless
	# of where the rows sit.
	cards = None
	opening_row = next((r for r in data if r.get("remarks") == _("Số dư đầu kỳ")), None)
	movement_row = next((r for r in data if r.get("remarks") == _("Cộng phát sinh kỳ")), None)
	closing_row = next((r for r in data if r.get("remarks") == _("Số dư cuối kỳ")), None)
	if opening_row and movement_row and closing_row:
		cards = build_summary_cards(
			float(opening_row.get("balance") or 0),
			float(movement_row.get("debit") or 0),
			float(movement_row.get("credit") or 0),
			float(closing_row.get("balance") or 0),
		)

	return columns, data, None, None, cards


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("{0} is mandatory").format(_("Company")))

	if not filters.get("from_date") or not filters.get("to_date"):
		frappe.throw(_("From Date and To Date are mandatory"))

	if filters.get("from_date") > filters.get("to_date"):
		frappe.throw(_("From Date must be before To Date"))


def get_columns():
	return [
		{
			"label": _("Ngày"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Số chứng từ"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180,
		},
		{
			"label": _("Loại chứng từ"),
			"fieldname": "voucher_type",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Diễn giải"),
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"label": _("TK đối ứng"),
			"fieldname": "against",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Thu"),
			"fieldname": "debit",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Chi"),
			"fieldname": "credit",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Tồn"),
			"fieldname": "balance",
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data(filters):
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	specific_account = filters.get("cash_account")

	# Get cash accounts — specific or all 111%
	cash_accounts = get_accounts_by_prefix(company, CASH_PREFIX, specific_account)
	if not cash_accounts:
		return []

	# Calculate opening balance
	opening_balance = get_opening_balance(cash_accounts, from_date, company)

	# Get transactions in date range
	transaction_type = filters.get("transaction_type")
	transactions = get_transactions(cash_accounts, from_date, to_date, company)

	# Filter by transaction type
	if transaction_type == "Thu":
		transactions = [t for t in transactions if (t.debit or 0) > 0]
	elif transaction_type == "Chi":
		transactions = [t for t in transactions if (t.credit or 0) > 0]

	# Period totals + closing computed up-front for the summary block.
	total_debit = sum(row.debit or 0 for row in transactions)
	total_credit = sum(row.credit or 0 for row in transactions)
	closing_balance = opening_balance + total_debit - total_credit

	# 3 dòng tóm tắt PIN ở ĐẦU bảng (KTT quét nhanh không cần scroll). Đồng thời
	# lặp lại Cộng phát sinh kỳ + Số dư cuối kỳ ở CUỐI bảng theo dạng sổ kế toán
	# truyền thống (FB-2026-01076).
	data = [
		{
			"posting_date": None, "voucher_no": None, "voucher_type": None,
			"remarks": _("Số dư đầu kỳ"), "against": None,
			"debit": 0, "credit": 0, "balance": opening_balance, "bold": 1,
		},
		{
			"posting_date": None, "voucher_no": None, "voucher_type": None,
			"remarks": _("Cộng phát sinh kỳ"), "against": None,
			"debit": total_debit, "credit": total_credit, "balance": None, "bold": 1,
		},
		{
			"posting_date": None, "voucher_no": None, "voucher_type": None,
			"remarks": _("Số dư cuối kỳ"), "against": None,
			"debit": 0, "credit": 0, "balance": closing_balance, "bold": 1,
		},
	]

	# Detail transaction rows with running balance (newest first for cash-flow context).
	running_balance = opening_balance
	detail = []
	for row in transactions:
		running_balance += (row.debit or 0) - (row.credit or 0)
		detail.append(
			{
				"posting_date": row.posting_date,
				"voucher_no": row.voucher_no,
				"voucher_type": row.voucher_type,
				"remarks": row.remarks,
				"against": extract_account_numbers(row.against),
				"debit": row.debit,
				"credit": row.credit,
				"balance": running_balance,
			}
		)
	# Newest first: reverse AFTER running-balance computation.
	detail.reverse()
	data.extend(detail)

	# Tổng kết cuối bảng (FB-2026-01076): Cộng phát sinh kỳ + Số dư cuối kỳ.
	data.append({
		"posting_date": None, "voucher_no": None, "voucher_type": None,
		"remarks": _("Cộng phát sinh kỳ"), "against": None,
		"debit": total_debit, "credit": total_credit, "balance": None, "bold": 1,
	})
	data.append({
		"posting_date": None, "voucher_no": None, "voucher_type": None,
		"remarks": _("Số dư cuối kỳ"), "against": None,
		"debit": 0, "credit": 0, "balance": closing_balance, "bold": 1,
	})
	return data
