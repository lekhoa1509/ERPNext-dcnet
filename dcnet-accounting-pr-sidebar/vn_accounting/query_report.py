from __future__ import annotations

import json
from typing import Any

import frappe
from frappe.desk import query_report as frappe_query_report

from vn_accounting.branch_cash.service import (
	get_allowed_accounting_units,
	get_user_branch,
	has_company_wide_access,
	is_privileged_user,
)

GENERAL_LEDGER_REPORTS = {"General Ledger"}
IMPOSSIBLE_COST_CENTER = "__vn_accounting_branch_restricted__"


def get_branch_accounting_unit(branch: str | None) -> str | None:
	if not branch or not frappe.db.has_column("Branch", "accounting_unit"):
		return None

	return frappe.db.get_value("Branch", branch, "accounting_unit")


def get_allowed_general_ledger_cost_centers(company: str | None = None, user: str | None = None) -> list[str] | None:
	user = user or frappe.session.user
	if is_privileged_user(user):
		return None

	if company and has_company_wide_access(company, user=user):
		return None

	allowed_units = set(get_allowed_accounting_units(company=company, user=user))
	branch_accounting_unit = get_branch_accounting_unit(get_user_branch(user))
	if branch_accounting_unit:
		allowed_units.add(branch_accounting_unit)

	return sorted(allowed_units)


def normalize_filters(filters) -> frappe._dict:
	if not filters:
		return frappe._dict()

	if isinstance(filters, str):
		filters = json.loads(filters)

	return frappe._dict(filters)


def normalize_multiselect_values(values: Any) -> list[str]:
	if not values:
		return []

	if isinstance(values, str):
		try:
			parsed = json.loads(values)
		except json.JSONDecodeError:
			parsed = values
		values = parsed

	if isinstance(values, (tuple, set)):
		values = list(values)

	if isinstance(values, list):
		return [value for value in values if value]

	return [values]


def apply_general_ledger_branch_restriction(report_name: str, filters=None, user: str | None = None):
	filters = normalize_filters(filters)
	if report_name not in GENERAL_LEDGER_REPORTS:
		return filters

	user = user or frappe.session.user
	allowed_cost_centers = get_allowed_general_ledger_cost_centers(
		company=filters.get("company"),
		user=user,
	)
	if allowed_cost_centers is None:
		return filters

	current_cost_centers = normalize_multiselect_values(filters.get("cost_center"))
	if current_cost_centers:
		allowed_set = set(allowed_cost_centers)
		filters["cost_center"] = [
			cost_center for cost_center in current_cost_centers if cost_center in allowed_set
		] or [IMPOSSIBLE_COST_CENTER]
		return filters

	filters["cost_center"] = allowed_cost_centers or [IMPOSSIBLE_COST_CENTER]
	return filters


@frappe.whitelist()
def get_general_ledger_access_context(company: str | None = None):
	user = frappe.session.user
	allowed_cost_centers = get_allowed_general_ledger_cost_centers(company=company, user=user)

	return {
		"user": user,
		"branch": get_user_branch(user),
		"restricted": allowed_cost_centers is not None,
		"allowed_cost_centers": allowed_cost_centers or [],
		"is_privileged": bool(allowed_cost_centers is None),
		"has_mapping": bool(allowed_cost_centers),
		"allow_manual_subset": len(allowed_cost_centers or []) > 1,
	}


@frappe.whitelist()
@frappe.read_only()
def run(
	report_name,
	filters=None,
	user=None,
	ignore_prepared_report=False,
	custom_columns=None,
	is_tree=False,
	parent_field=None,
	are_default_filters=True,
	js_filters=None,
):
	filters = apply_general_ledger_branch_restriction(report_name, filters=filters, user=user)
	return frappe_query_report.run(
		report_name,
		filters=filters,
		user=user,
		ignore_prepared_report=ignore_prepared_report,
		custom_columns=custom_columns,
		is_tree=is_tree,
		parent_field=parent_field,
		are_default_filters=are_default_filters,
		js_filters=js_filters,
	)
