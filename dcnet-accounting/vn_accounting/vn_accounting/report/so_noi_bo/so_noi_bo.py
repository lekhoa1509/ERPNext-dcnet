from __future__ import annotations

from collections.abc import Iterable, Mapping

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

	columns = get_columns()
	data = get_data(filters)

	# Cards lơ lửng trên data table (Frappe report_summary).
	# data[0..2] đã là 3 summary rows (đầu/cộng/cuối) do build_ledger_rows pin top.
	cards = None
	if len(data) >= 3 and data[0].get("bold"):
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
		{"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": _("Chi nhánh"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 180},
		{
			"label": _("Đơn vị hạch toán"),
			"fieldname": "accounting_unit",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 180,
		},
		{"label": _("Loại CT"), "fieldname": "voucher_type", "fieldtype": "Data", "width": 140},
		{
			"label": _("Số CT"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 170,
		},
		{"label": _("Loại phiếu"), "fieldname": "direction_label", "fieldtype": "Data", "width": 110},
		{"label": _("Diễn giải"), "fieldname": "remarks", "fieldtype": "Data", "width": 300},
		{"label": _("Thu"), "fieldname": "debit", "fieldtype": "Currency", "width": 140},
		{"label": _("Chi"), "fieldname": "credit", "fieldtype": "Currency", "width": 140},
		{"label": _("Tồn"), "fieldname": "balance", "fieldtype": "Currency", "width": 150},
	]


def get_data(filters):
	opening_balance = get_opening_balance(filters)
	rows = get_internal_entries(filters)
	return build_ledger_rows(rows, opening_balance)


def build_ledger_rows(entries: Iterable[Mapping], opening_balance: float) -> list[dict]:
	detail = []
	running_balance = opening_balance
	total_debit = 0
	total_credit = 0

	for row in entries:
		amount = flt(row.get("amount"))
		debit = amount if row.get("direction") == "Receive" else 0
		credit = amount if row.get("direction") == "Pay" else 0

		running_balance += debit - credit
		total_debit += debit
		total_credit += credit

		detail.append(
			{
				"posting_date": row.get("posting_date"),
				"branch": row.get("branch"),
				"accounting_unit": row.get("accounting_unit"),
				"voucher_type": row.get("voucher_type"),
				"voucher_no": row.get("name"),
				"direction_label": get_direction_label(row.get("direction")),
				"remarks": row.get("remarks"),
				"debit": debit,
				"credit": credit,
				"balance": running_balance,
			}
		)

	# Display newest first: reverse detail rows AFTER running-balance
	# computation so each row's balance still reflects post-transaction state.
	detail.reverse()

	# Summary block — opening / period movement / closing — as the top 3 rows
	# so the key figures stay visible above the transaction detail.
	summary = [
		{
			"posting_date": None,
			"branch": None,
			"accounting_unit": None,
			"voucher_type": None,
			"voucher_no": None,
			"direction_label": None,
			"remarks": _("Số dư đầu kỳ"),
			"debit": 0,
			"credit": 0,
			"balance": opening_balance,
			"bold": 1,
		},
		{
			"posting_date": None,
			"branch": None,
			"accounting_unit": None,
			"voucher_type": None,
			"voucher_no": None,
			"direction_label": None,
			"remarks": _("Cộng phát sinh kỳ"),
			"debit": total_debit,
			"credit": total_credit,
			"balance": None,
			"bold": 1,
		},
		{
			"posting_date": None,
			"branch": None,
			"accounting_unit": None,
			"voucher_type": None,
			"voucher_no": None,
			"direction_label": None,
			"remarks": _("Số dư cuối kỳ"),
			"debit": 0,
			"credit": 0,
			"balance": running_balance,
			"bold": 1,
		},
	]

	# Lặp lại Cộng phát sinh kỳ + Số dư cuối kỳ ở cuối bảng theo dạng sổ
	# truyền thống (FB-2026-01076). summary[1]=cộng phát sinh, summary[2]=cuối kỳ.
	bottom = [dict(summary[1]), dict(summary[2])]
	return summary + detail + bottom


def get_opening_balance(filters):
	total_balance = 0

	if frappe.db.table_exists("Branch Cash Entry"):
		total_balance += get_signed_balance(
			doctype="Branch Cash Entry",
			table_alias="bce",
			filters=filters,
			opening_only=True,
			internal_scope_field="posting_scope",
		)

	if frappe.db.table_exists("Internal Summary Entry"):
		total_balance += get_signed_balance(
			doctype="Internal Summary Entry",
			table_alias="ise",
			filters=filters,
			opening_only=True,
		)

	return flt(total_balance)


def get_internal_entries(filters):
	queries = []
	params = {"company": filters.get("company")}

	if frappe.db.table_exists("Branch Cash Entry"):
		conditions, params = get_conditions(
			filters,
			table_alias="bce",
			internal_scope_field="posting_scope",
		)
		queries.append(
			f"""
			SELECT
				bce.name,
				bce.posting_date,
				bce.branch,
				bce.accounting_unit,
				bce.direction,
				bce.amount,
				bce.remarks,
				bce.creation,
				'Branch Cash Entry' AS voucher_type
			FROM `tabBranch Cash Entry` bce
			WHERE {conditions}
			"""
		)

	if frappe.db.table_exists("Internal Summary Entry"):
		conditions, params = get_conditions(filters, table_alias="ise")
		queries.append(
			f"""
			SELECT
				ise.name,
				ise.posting_date,
				ise.branch,
				ise.accounting_unit,
				ise.direction,
				ise.amount,
				ise.remarks,
				ise.creation,
				'Internal Summary Entry' AS voucher_type
			FROM `tabInternal Summary Entry` ise
			WHERE {conditions}
			"""
		)

	if not queries:
		return []

	return frappe.db.sql(
		"\nUNION ALL\n".join(queries) + "\nORDER BY posting_date, creation, voucher_type, name",
		params,
		as_dict=True,
	)


def get_signed_balance(
	doctype: str,
	table_alias: str,
	filters,
	opening_only: bool = False,
	internal_scope_field: str | None = None,
):
	conditions, params = get_conditions(
		filters,
		table_alias=table_alias,
		opening_only=opening_only,
		internal_scope_field=internal_scope_field,
	)
	result = frappe.db.sql(
		f"""
		SELECT COALESCE(SUM(
			CASE
				WHEN {table_alias}.direction = 'Receive' THEN {table_alias}.amount
				ELSE -{table_alias}.amount
			END
		), 0) AS balance
		FROM `tab{doctype}` {table_alias}
		WHERE {conditions}
		""",
		params,
		as_dict=True,
	)
	return flt(result[0].balance) if result else 0


def get_conditions(filters, table_alias="entry", opening_only=False, internal_scope_field: str | None = None):
	conditions = [
		f"{table_alias}.docstatus = 1",
		f"{table_alias}.company = %(company)s",
	]
	params = {"company": filters.get("company")}

	if internal_scope_field:
		conditions.append(f"{table_alias}.{internal_scope_field} = 'Internal'")

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

	if filters.get("direction"):
		conditions.append(f"{table_alias}.direction = %(direction)s")
		params["direction"] = filters.get("direction")

	permission_query = build_branch_cash_entry_permission_query(table_alias=table_alias)
	if permission_query:
		conditions.append(f"({permission_query})")

	return " AND ".join(conditions), params


def get_direction_label(direction: str | None) -> str | None:
	if direction == "Receive":
		return _("Thu")
	if direction == "Pay":
		return _("Chi")
	return direction


def flt(value) -> float:
	return frappe.utils.flt(value, 2)
