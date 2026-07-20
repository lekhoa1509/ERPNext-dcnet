# Copyright (c) 2026, Long and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _

from vn_accounting.vn_accounting.report_utils import (
	BANK_PREFIX,
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

	cards = None
	if len(data) >= 3 and data[0].get("remarks") == _("Số dư đầu kỳ"):
		opening_net = float(data[0].get("balance") or 0)
		period_debit = float(data[1].get("debit") or 0)
		period_credit = float(data[1].get("credit") or 0)
		closing_net = float(data[2].get("balance") or 0)
		cards = build_summary_cards(opening_net, period_debit, period_credit, closing_net)

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
			"label": _("Gửi vào"),
			"fieldname": "debit",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Rút ra"),
			"fieldname": "credit",
			"fieldtype": "Currency",
			"width": 130,
		},
		{
			"label": _("Số dư"),
			"fieldname": "balance",
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data(filters):
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	bank_account = filters.get("bank_account")

	# Get bank accounts (112%) for the company
	bank_accounts = get_accounts_by_prefix(company, BANK_PREFIX, bank_account)
	if not bank_accounts:
		return []

	# Calculate opening balance
	opening_balance = get_opening_balance(bank_accounts, from_date, company)

	# Get transactions in date range
	transaction_type = filters.get("transaction_type")
	transactions = get_transactions(bank_accounts, from_date, to_date, company)

	# Filter by transaction type
	if transaction_type == "Gửi vào":
		transactions = [t for t in transactions if (t.debit or 0) > 0]
	elif transaction_type == "Rút ra":
		transactions = [t for t in transactions if (t.credit or 0) > 0]

	# Period totals + closing balance (computed up front for the summary block)
	total_debit = sum(row.debit or 0 for row in transactions)
	total_credit = sum(row.credit or 0 for row in transactions)
	closing_balance = opening_balance + total_debit - total_credit

	# Summary block — opening / period movement / closing — as the top 3 rows
	# so the key figures are visible without scrolling past every transaction.
	data = [
		{
			"posting_date": None,
			"voucher_no": None,
			"voucher_type": None,
			"remarks": _("Số dư đầu kỳ"),
			"against": None,
			"debit": 0,
			"credit": 0,
			"balance": opening_balance,
		},
		{
			"posting_date": None,
			"voucher_no": None,
			"voucher_type": None,
			"remarks": _("Cộng phát sinh kỳ"),
			"against": None,
			"debit": total_debit,
			"credit": total_credit,
			"balance": None,
		},
		{
			"posting_date": None,
			"voucher_no": None,
			"voucher_type": None,
			"remarks": _("Số dư cuối kỳ"),
			"against": None,
			"debit": 0,
			"credit": 0,
			"balance": closing_balance,
		},
	]

	# Detail transaction rows with running balance
	running_balance = opening_balance
	for row in transactions:
		running_balance += (row.debit or 0) - (row.credit or 0)
		data.append(
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

	# Lặp lại Cộng phát sinh kỳ + Số dư cuối kỳ ở cuối bảng theo dạng sổ
	# truyền thống (FB-2026-01076).
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
