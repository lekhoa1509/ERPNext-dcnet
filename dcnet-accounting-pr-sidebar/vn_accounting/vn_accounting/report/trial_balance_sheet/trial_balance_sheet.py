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
		frappe.throw(_("Company is required"))
	if not filters.get("from_date") or not filters.get("to_date"):
		frappe.throw(_("From Date and To Date are required"))
	if getdate(filters.get("from_date")) > getdate(filters.get("to_date")):
		frappe.throw(_("From Date must be before To Date"))


def get_columns():
	return [
		{
			"label": _("Số TK"),
			"fieldname": "account_number",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Tên tài khoản"),
			"fieldname": "account_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Dư Nợ đầu kỳ"),
			"fieldname": "opening_debit",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": _("Dư Có đầu kỳ"),
			"fieldname": "opening_credit",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": _("PS Nợ trong kỳ"),
			"fieldname": "period_debit",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": _("PS Có trong kỳ"),
			"fieldname": "period_credit",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": _("Dư Nợ cuối kỳ"),
			"fieldname": "closing_debit",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"label": _("Dư Có cuối kỳ"),
			"fieldname": "closing_credit",
			"fieldtype": "Currency",
			"width": 120,
		},
	]


def get_data(filters):
	# Get all non-group accounts with account_number for the company
	accounts = frappe.db.sql(
		"""
		SELECT name, account_number, account_name
		FROM `tabAccount`
		WHERE company = %(company)s
			AND is_group = 0
			AND account_number IS NOT NULL
			AND account_number != ''
		ORDER BY account_number
		""",
		filters,
		as_dict=True,
	)

	if not accounts:
		return []

	account_names = [a.name for a in accounts]

	# Single query to get opening balances (before from_date)
	opening_data = frappe.db.sql(
		"""
		SELECT
			gle.account,
			IFNULL(SUM(gle.debit), 0) AS total_debit,
			IFNULL(SUM(gle.credit), 0) AS total_credit
		FROM `tabGL Entry` gle
		WHERE
			gle.company = %(company)s
			AND gle.posting_date < %(from_date)s
			AND gle.is_cancelled = 0
			AND gle.account IN %(accounts)s
		GROUP BY gle.account
		""",
		{"company": filters.get("company"), "from_date": filters.get("from_date"), "accounts": account_names},
		as_dict=True,
	)

	# Single query to get period transactions
	period_data = frappe.db.sql(
		"""
		SELECT
			gle.account,
			IFNULL(SUM(gle.debit), 0) AS total_debit,
			IFNULL(SUM(gle.credit), 0) AS total_credit
		FROM `tabGL Entry` gle
		WHERE
			gle.company = %(company)s
			AND gle.posting_date >= %(from_date)s
			AND gle.posting_date <= %(to_date)s
			AND gle.is_cancelled = 0
			AND gle.account IN %(accounts)s
		GROUP BY gle.account
		""",
		{
			"company": filters.get("company"),
			"from_date": filters.get("from_date"),
			"to_date": filters.get("to_date"),
			"accounts": account_names,
		},
		as_dict=True,
	)

	# Build lookup dicts
	opening_map = {d.account: d for d in opening_data}
	period_map = {d.account: d for d in period_data}

	data = []
	totals = {
		"opening_debit": 0,
		"opening_credit": 0,
		"period_debit": 0,
		"period_credit": 0,
		"closing_debit": 0,
		"closing_credit": 0,
	}

	for account in accounts:
		opening = opening_map.get(account.name)
		period = period_map.get(account.name)

		opening_balance = flt((opening.total_debit - opening.total_credit) if opening else 0, 2)
		period_debit = flt(period.total_debit if period else 0, 2)
		period_credit = flt(period.total_credit if period else 0, 2)
		closing_balance = flt(opening_balance + period_debit - period_credit, 2)

		# Skip accounts with no activity and no balance
		if not opening_balance and not period_debit and not period_credit:
			continue

		opening_debit = opening_balance if opening_balance > 0 else 0
		opening_credit = abs(opening_balance) if opening_balance < 0 else 0
		closing_debit = closing_balance if closing_balance > 0 else 0
		closing_credit = abs(closing_balance) if closing_balance < 0 else 0

		row = {
			"account_number": account.account_number,
			"account_name": account.account_name,
			"opening_debit": opening_debit,
			"opening_credit": opening_credit,
			"period_debit": period_debit,
			"period_credit": period_credit,
			"closing_debit": closing_debit,
			"closing_credit": closing_credit,
		}

		data.append(row)

		# Accumulate totals
		totals["opening_debit"] += opening_debit
		totals["opening_credit"] += opening_credit
		totals["period_debit"] += period_debit
		totals["period_credit"] += period_credit
		totals["closing_debit"] += closing_debit
		totals["closing_credit"] += closing_credit

	# Add totals row
	if data:
		data.append(
			{
				"account_number": "",
				"account_name": _("Tổng cộng"),
				"opening_debit": flt(totals["opening_debit"], 2),
				"opening_credit": flt(totals["opening_credit"], 2),
				"period_debit": flt(totals["period_debit"], 2),
				"period_credit": flt(totals["period_credit"], 2),
				"closing_debit": flt(totals["closing_debit"], 2),
				"closing_credit": flt(totals["closing_credit"], 2),
				"bold": 1,
			}
		)

	return data
