from __future__ import annotations

import frappe
from frappe import _

from vn_accounting.branch_cash.service import (
	build_branch_cash_entry_permission_query,
	validate_report_filters,
)
from vn_accounting.vn_accounting.report_utils import build_summary_cards


def execute(filters=None):
	filters = frappe._dict(filters or {})
	validate_filters(filters)
	validate_report_filters(filters)

	if filters.get("view_mode") == "Summary":
		return get_summary_columns(), get_summary_data(filters)

	cols = get_detail_columns()
	data = get_detail_data(filters)

	cards = None
	if len(data) >= 3 and data[0].get("remarks") == _("Số dư đầu kỳ"):
		opening_net = float(data[0].get("balance") or 0)
		period_debit = float(data[1].get("debit") or 0)
		period_credit = float(data[1].get("credit") or 0)
		closing_net = float(data[2].get("balance") or 0)
		cards = build_summary_cards(opening_net, period_debit, period_credit, closing_net)

	return cols, data, None, None, cards


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("{0} is mandatory").format(_("Company")))

	if not filters.get("from_date") or not filters.get("to_date"):
		frappe.throw(_("From Date and To Date are mandatory"))

	if filters.get("from_date") > filters.get("to_date"):
		frappe.throw(_("From Date must be before To Date"))


def get_detail_columns():
	return [
		{"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Chi nhánh"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 180},
		{
			"label": _("Đơn vị hạch toán"),
			"fieldname": "accounting_unit",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 180,
		},
		{
			"label": _("Phiếu quỹ"),
			"fieldname": "branch_cash_entry",
			"fieldtype": "Link",
			"options": "Branch Cash Entry",
			"width": 160,
		},
		{"label": _("Phạm vi"), "fieldname": "posting_scope_label", "fieldtype": "Data", "width": 150},
		{"label": _("Diễn giải"), "fieldname": "remarks", "fieldtype": "Data", "width": 280},
		{
			"label": _("Bút toán official"),
			"fieldname": "official_journal_entry",
			"fieldtype": "Link",
			"options": "Journal Entry",
			"width": 170,
		},
		{"label": _("Thu"), "fieldname": "debit", "fieldtype": "Currency", "width": 140},
		{"label": _("Chi"), "fieldname": "credit", "fieldtype": "Currency", "width": 140},
		{"label": _("Tồn"), "fieldname": "balance", "fieldtype": "Currency", "width": 150},
	]


def get_summary_columns():
	return [
		{"label": _("Chi nhánh"), "fieldname": "branch", "fieldtype": "Data", "width": 180},
		{
			"label": _("Đơn vị hạch toán"),
			"fieldname": "accounting_unit",
			"fieldtype": "Data",
			"width": 180,
		},
		{"label": _("Thu official"), "fieldname": "official_receive", "fieldtype": "Currency", "width": 140},
		{"label": _("Chi official"), "fieldname": "official_pay", "fieldtype": "Currency", "width": 140},
		{"label": _("Thu nội bộ"), "fieldname": "internal_receive", "fieldtype": "Currency", "width": 140},
		{"label": _("Chi nội bộ"), "fieldname": "internal_pay", "fieldtype": "Currency", "width": 140},
		{"label": _("Số dư thuần"), "fieldname": "net_balance", "fieldtype": "Currency", "width": 150},
	]


def get_detail_data(filters):
	opening_balance = get_opening_balance(filters)
	conditions, params = get_conditions(filters, table_alias="bce")

	rows = frappe.db.sql(
		f"""
		SELECT
			bce.name,
			bce.posting_date,
			bce.branch,
			bce.accounting_unit,
			bce.posting_scope,
			bce.remarks,
			bce.official_journal_entry,
			bce.direction,
			bce.amount,
			bce.creation
		FROM `tabBranch Cash Entry` bce
		WHERE {conditions}
		ORDER BY bce.posting_date, bce.creation, bce.name
		""",
		params,
		as_dict=True,
	)

	# Compute period totals + running balance first (needed cho summary block).
	running_balance = opening_balance
	total_debit = 0
	total_credit = 0
	detail = []
	for row in rows:
		debit = row.amount if row.direction == "Receive" else 0
		credit = row.amount if row.direction == "Pay" else 0
		running_balance += debit - credit
		total_debit += debit
		total_credit += credit
		detail.append(
			{
				"posting_date": row.posting_date,
				"branch": row.branch,
				"accounting_unit": row.accounting_unit,
				"branch_cash_entry": row.name,
				"posting_scope_label": get_scope_label(row.posting_scope),
				"remarks": row.remarks,
				"official_journal_entry": row.official_journal_entry,
				"debit": debit,
				"credit": credit,
				"balance": running_balance,
			}
		)

	# 3 dòng tóm tắt PIN ở ĐẦU data table (KTT quét nhanh không cần scroll).
	def _summary_row(remarks, dr, cr, balance):
		return {
			"posting_date": None, "branch": None, "accounting_unit": None,
			"branch_cash_entry": None, "posting_scope_label": None,
			"remarks": remarks, "official_journal_entry": None,
			"debit": dr, "credit": cr, "balance": balance, "bold": 1,
		}
	data = [
		_summary_row(_("Số dư đầu kỳ"), 0, 0, opening_balance),
		_summary_row(_("Cộng phát sinh kỳ"), total_debit, total_credit, None),
		_summary_row(_("Số dư cuối kỳ"), 0, 0, running_balance),
		*detail,
		# Lặp lại tổng kết ở cuối bảng theo dạng sổ truyền thống (FB-2026-01076).
		_summary_row(_("Cộng phát sinh kỳ"), total_debit, total_credit, None),
		_summary_row(_("Số dư cuối kỳ"), 0, 0, running_balance),
	]
	return data


def get_summary_data(filters):
	conditions, params = get_conditions(filters, table_alias="bce")
	rows = frappe.db.sql(
		f"""
		SELECT
			bce.branch,
			bce.accounting_unit,
			COALESCE(SUM(CASE
				WHEN bce.direction = 'Receive' AND bce.posting_scope = 'Official' THEN bce.amount
				ELSE 0
			END), 0) AS official_receive,
			COALESCE(SUM(CASE
				WHEN bce.direction = 'Pay' AND bce.posting_scope = 'Official' THEN bce.amount
				ELSE 0
			END), 0) AS official_pay,
			COALESCE(SUM(CASE
				WHEN bce.direction = 'Receive' AND bce.posting_scope = 'Internal' THEN bce.amount
				ELSE 0
			END), 0) AS internal_receive,
			COALESCE(SUM(CASE
				WHEN bce.direction = 'Pay' AND bce.posting_scope = 'Internal' THEN bce.amount
				ELSE 0
			END), 0) AS internal_pay,
			COALESCE(SUM(CASE
				WHEN bce.direction = 'Receive' THEN bce.amount
				ELSE -bce.amount
			END), 0) AS net_balance
		FROM `tabBranch Cash Entry` bce
		WHERE {conditions}
		GROUP BY bce.branch, bce.accounting_unit
		ORDER BY bce.branch, bce.accounting_unit
		""",
		params,
		as_dict=True,
	)

	if not rows:
		return []

	total_row = {
		"branch": _("Tổng cộng"),
		"accounting_unit": None,
		"official_receive": sum(row.official_receive or 0 for row in rows),
		"official_pay": sum(row.official_pay or 0 for row in rows),
		"internal_receive": sum(row.internal_receive or 0 for row in rows),
		"internal_pay": sum(row.internal_pay or 0 for row in rows),
		"net_balance": sum(row.net_balance or 0 for row in rows),
	}
	rows.append(total_row)
	return rows


def get_opening_balance(filters):
	conditions, params = get_conditions(filters, table_alias="bce", opening_only=True)
	result = frappe.db.sql(
		f"""
		SELECT COALESCE(SUM(
			CASE
				WHEN bce.direction = 'Receive' THEN bce.amount
				ELSE -bce.amount
			END
		), 0) AS balance
		FROM `tabBranch Cash Entry` bce
		WHERE {conditions}
		""",
		params,
		as_dict=True,
	)
	return result[0].balance if result else 0


def get_conditions(filters, table_alias="bce", opening_only=False):
	conditions = [
		f"{table_alias}.docstatus = 1",
		f"{table_alias}.company = %(company)s",
	]
	params = {"company": filters.get("company")}

	if opening_only:
		conditions.append(f"{table_alias}.posting_date < %(from_date)s")
		params["from_date"] = filters.get("from_date")
	else:
		conditions.extend(
			[
				f"{table_alias}.posting_date >= %(from_date)s",
				f"{table_alias}.posting_date <= %(to_date)s",
			]
		)
		params["from_date"] = filters.get("from_date")
		params["to_date"] = filters.get("to_date")

	if filters.get("branch"):
		conditions.append(f"{table_alias}.branch = %(branch)s")
		params["branch"] = filters.get("branch")

	if filters.get("accounting_unit"):
		conditions.append(f"{table_alias}.accounting_unit = %(accounting_unit)s")
		params["accounting_unit"] = filters.get("accounting_unit")

	if filters.get("posting_scope"):
		conditions.append(f"{table_alias}.posting_scope = %(posting_scope)s")
		params["posting_scope"] = filters.get("posting_scope")

	permission_query = build_branch_cash_entry_permission_query(table_alias=table_alias)
	if permission_query:
		conditions.append(f"({permission_query})")

	return " AND ".join(conditions), params


def get_scope_label(scope):
	if scope == "Official":
		return _("Hạch toán sổ cái")
	if scope == "Internal":
		return _("Nội bộ chi nhánh")
	return scope
