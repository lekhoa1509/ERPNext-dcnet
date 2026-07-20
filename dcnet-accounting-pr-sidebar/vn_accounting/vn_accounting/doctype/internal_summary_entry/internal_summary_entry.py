from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, flt

from vn_accounting.branch_cash.service import (
	build_branch_cash_entry_permission_query,
	get_user_branch,
	is_privileged_user,
	user_can_access_branch_cash,
	validate_user_can_manage_branch_cash,
)


class InternalSummaryEntry(Document):
	def validate(self):
		if not self.branch and not is_privileged_user():
			self.branch = get_user_branch()

		validate_user_can_manage_branch_cash(
			company=self.company,
			branch=self.branch,
			accounting_unit=self.accounting_unit,
		)
		self._validate_amount()
		self._validate_accounting_unit()

	def _validate_amount(self):
		if flt(self.amount) <= 0:
			frappe.throw(_("Số tiền phải lớn hơn 0."))

		if self.direction not in {"Receive", "Pay"}:
			frappe.throw(_("Loại bút toán chỉ được là Thu hoặc Chi."))

	def _validate_accounting_unit(self):
		accounting_unit = frappe.db.get_value(
			"Cost Center",
			self.accounting_unit,
			["company", "is_group"],
			as_dict=True,
		)

		if not accounting_unit:
			frappe.throw(_("Đơn vị hạch toán {0} không tồn tại.").format(self.accounting_unit))

		if accounting_unit.company != self.company:
			frappe.throw(
				_("Đơn vị hạch toán {0} không thuộc công ty {1}.").format(
					self.accounting_unit,
					self.company,
				)
			)

		if cint(accounting_unit.is_group):
			frappe.throw(_("Đơn vị hạch toán phải là Cost Center lá."))


def get_internal_summary_entry_permission_query_conditions(user: str | None = None) -> str:
	return build_branch_cash_entry_permission_query(
		user=user,
		table_alias="`tabInternal Summary Entry`",
	)


def has_internal_summary_entry_permission(doc=None, user: str | None = None, permission_type: str | None = None) -> bool:
	user = user or frappe.session.user
	if is_privileged_user(user):
		return True

	if doc is None:
		return bool(get_user_branch(user))

	if isinstance(doc, str):
		doc = frappe.get_doc("Internal Summary Entry", doc)

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
