from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import frappe
from frappe import _

PRIVILEGED_ROLES = {"System Manager", "Accounts Manager"}


def is_privileged_user(user: str | None = None) -> bool:
	user = user or frappe.session.user
	if user == "Administrator":
		return True
	return bool(PRIVILEGED_ROLES.intersection(set(frappe.get_roles(user))))


def get_user_branch(user: str | None = None) -> str | None:
	user = user or frappe.session.user
	if not user or not frappe.db.has_column("User", "branch"):
		return None

	return frappe.db.get_value("User", user, "branch")


@frappe.whitelist()
def get_current_user_branch_context() -> dict[str, Any]:
	user = frappe.session.user
	return {
		"user": user,
		"is_privileged": is_privileged_user(user),
		"branch": get_user_branch(user),
	}


def get_active_access_rows(user: str | None = None, company: str | None = None) -> list[dict[str, Any]]:
	user = user or frappe.session.user
	filters: dict[str, Any] = {
		"user": user,
		"is_active": 1,
	}
	if company:
		filters["company"] = company

	return frappe.get_all(
		"Branch Cash Access",
		filters=filters,
		fields=["company", "accounting_unit", "company_wide_view"],
		order_by="company asc, accounting_unit asc",
	)


def has_company_wide_access(company: str, user: str | None = None) -> bool:
	if is_privileged_user(user):
		return True

	for row in get_active_access_rows(user=user, company=company):
		if row.get("company_wide_view"):
			return True

	return False


def get_allowed_accounting_units(company: str | None = None, user: str | None = None) -> list[str]:
	if is_privileged_user(user):
		return []

	units = {
		row.get("accounting_unit")
		for row in get_active_access_rows(user=user, company=company)
		if row.get("accounting_unit")
	}
	return sorted(units)


def user_can_access_branch_cash(
	company: str | None,
	branch: str | None = None,
	accounting_unit: str | None = None,
	user: str | None = None,
) -> bool:
	if is_privileged_user(user):
		return True

	if not company:
		return False

	user_branch = get_user_branch(user)
	if not user_branch or not branch:
		return False

	return branch == user_branch


def validate_user_can_manage_branch_cash(
	company: str | None,
	branch: str | None = None,
	accounting_unit: str | None = None,
	user: str | None = None,
) -> None:
	if user_can_access_branch_cash(
		company=company,
		branch=branch,
		accounting_unit=accounting_unit,
		user=user,
	):
		return

	user = user or frappe.session.user
	user_branch = get_user_branch(user)
	if not user_branch:
		frappe.throw(
			_("Người dùng {0} chưa được gán chi nhánh trên hồ sơ User.").format(user),
		)

	frappe.throw(
		_("Người dùng {0} chỉ được phép quản lý quỹ cho chi nhánh {1}.").format(
			user,
			user_branch,
		),
	)


def build_branch_cash_entry_permission_query(
	user: str | None = None,
	table_alias: str = "`tabBranch Cash Entry`",
) -> str:
	if is_privileged_user(user):
		return ""

	user_branch = get_user_branch(user)
	if not user_branch:
		return "1=0"

	return f"{table_alias}.branch = {frappe.db.escape(user_branch)}"


def get_branch_cash_entry_permission_query_conditions(user: str | None = None) -> str:
	return build_branch_cash_entry_permission_query(user=user)


def has_branch_cash_entry_permission(doc=None, user: str | None = None, permission_type: str | None = None) -> bool:
	user = user or frappe.session.user
	if is_privileged_user(user):
		return True

	if doc is None:
		return bool(get_user_branch(user))

	if isinstance(doc, str):
		doc = frappe.get_doc("Branch Cash Entry", doc)

	company = doc.get("company") if hasattr(doc, "get") else None
	branch = doc.get("branch") if hasattr(doc, "get") else None
	accounting_unit = doc.get("accounting_unit") if hasattr(doc, "get") else None

	if not company:
		return bool(get_user_branch(user))

	return user_can_access_branch_cash(
		company=company,
		branch=branch,
		accounting_unit=accounting_unit,
		user=user,
	)


def validate_report_filters(filters: Mapping[str, Any] | None, user: str | None = None) -> None:
	if is_privileged_user(user):
		return

	filters = filters or {}
	company = filters.get("company")
	branch = filters.get("branch")
	accounting_unit = filters.get("accounting_unit")
	user_branch = get_user_branch(user)

	if not user_branch:
		frappe.throw(
			_("Người dùng {0} chưa được gán chi nhánh trên hồ sơ User.").format(
				user or frappe.session.user
			)
		)

	if branch and branch != user_branch:
		frappe.throw(
			_("Bạn không được phép xem dữ liệu quỹ chi nhánh của chi nhánh {0}.").format(branch)
		)

	if company and not user_can_access_branch_cash(
		company=company,
		branch=branch or user_branch,
		accounting_unit=accounting_unit,
		user=user,
	):
		frappe.throw(
			_("Bạn không được phép xem dữ liệu quỹ chi nhánh của chi nhánh {0}.").format(
				branch or user_branch
			)
		)
