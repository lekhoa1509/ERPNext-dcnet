# Copyright (c) 2026, DCNet and contributors
# For license information, please see license.txt

from datetime import date

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, flt, getdate, today

MAX_CONSECUTIVE_FIXED_TERM = 2  # Điều 20 BLLĐ 2019 — lần 3 phải KXĐTH
EXPIRY_NOTIFICATION_DAYS = 30


class LaborContract(Document):
	def before_submit(self):
		self.check_single_active_contract()
		self.check_consecutive_fixed_term()

	def on_submit(self):
		# on_submit chạy SAU db_update() của Document.save() — set self.status
		# thôi sẽ không được ghi xuống DB, phải dùng db_set (giống quy tắc
		# "KHÔNG modify field trong on_update" cho on_submit).
		self.db_set("status", "Active", notify=False)
		if self.previous_contract:
			self.supersede_previous_contract()

	def check_single_active_contract(self):
		filters = {"employee": self.employee, "status": "Active", "docstatus": 1}
		if self.previous_contract:
			filters["name"] = ["!=", self.previous_contract]
		conflicts = frappe.get_all("Labor Contract", filters=filters, fields=["name", "start_date", "end_date"])
		new_end = getdate(self.end_date) if self.end_date else date.max
		for row in conflicts:
			if row.name == self.name:
				continue
			existing_end = getdate(row.end_date) if row.end_date else date.max
			overlap = getdate(row.start_date) <= new_end and existing_end >= getdate(self.start_date)
			if overlap:
				frappe.throw(
					_("Employee {0} already has an Active Labor Contract ({1}) overlapping this period.").format(
						self.employee, row.name
					)
				)

	def check_consecutive_fixed_term(self):
		if self.contract_type != "Fixed-term":
			return
		consecutive = 1  # tính cả hợp đồng hiện tại
		cursor = self.previous_contract
		while cursor:
			prev = frappe.db.get_value("Labor Contract", cursor, ["contract_type", "previous_contract"], as_dict=True)
			if not prev or prev.contract_type != "Fixed-term":
				break
			consecutive += 1
			cursor = prev.previous_contract

		if consecutive > MAX_CONSECUTIVE_FIXED_TERM and not self.override_reason:
			frappe.throw(
				_(
					"This is the {0}th consecutive Fixed-term contract for this employee. Labor law "
					"(Điều 20 BLLĐ 2019) requires converting to Indefinite-term after {1} consecutive "
					"fixed-term contracts. Fill in Override Reason to proceed anyway."
				).format(consecutive, MAX_CONSECUTIVE_FIXED_TERM)
			)
		if consecutive > MAX_CONSECUTIVE_FIXED_TERM and self.override_reason:
			frappe.msgprint(
				_("Overriding consecutive Fixed-term contract limit: {0}").format(self.override_reason),
				indicator="orange",
				alert=True,
			)

	def supersede_previous_contract(self):
		frappe.db.set_value("Labor Contract", self.previous_contract, "status", "Terminated")
		old_insurance_salary = frappe.db.get_value("Labor Contract", self.previous_contract, "insurance_salary")
		if old_insurance_salary is not None and flt(old_insurance_salary) != flt(self.insurance_salary):
			suggest_insurance_adjustment(self, old_insurance_salary)


def suggest_insurance_adjustment(contract, old_insurance_salary):
	"""Gợi ý tạo Insurance Declaration điều chỉnh mức đóng — tạo Draft để HR
	xem lại + duyệt, KHÔNG tự submit (spec 4.5: "gợi ý tạo... điều chỉnh")."""
	si_number = frappe.db.get_value("Employee", contract.employee, "si_number")
	declaration = frappe.new_doc("Insurance Declaration")
	declaration.declaration_type = "Rate Adjustment"
	declaration.month = today()
	declaration.append(
		"employees",
		{
			"employee": contract.employee,
			"si_number": si_number,
			"old_amount": old_insurance_salary,
			"new_amount": contract.insurance_salary,
			"effective_date": contract.start_date,
			"reason": _("Auto-suggested from Labor Contract {0} renewal").format(contract.name),
		},
	)
	declaration.insert(ignore_permissions=True)
	frappe.msgprint(
		_("Insurance contribution salary changed — draft Insurance Declaration {0} created for review.").format(
			frappe.utils.get_link_to_form("Insurance Declaration", declaration.name)
		),
		indicator="blue",
		alert=True,
	)


def run_daily_expiry_check():
	"""Scheduler daily — spec 4.5: HĐ hết hạn trong 30 ngày -> notify HR;
	quá end_date -> chuyển Expired."""
	_notify_upcoming_expiry()
	_expire_overdue_contracts()


def _notify_upcoming_expiry():
	threshold = add_days(today(), EXPIRY_NOTIFICATION_DAYS)
	upcoming = frappe.get_all(
		"Labor Contract",
		filters={
			"status": "Active",
			"docstatus": 1,
			"end_date": ["between", [today(), threshold]],
		},
		fields=["name", "employee_name", "end_date"],
	)
	if not upcoming:
		return
	hr_users = frappe.get_all(
		"Has Role", filters={"role": ["in", ["HR Manager", "HR User"]], "parenttype": "User"}, pluck="parent"
	)
	for contract in upcoming:
		for user in set(hr_users):
			frappe.get_doc(
				{
					"doctype": "Notification Log",
					"for_user": user,
					"type": "Alert",
					"subject": _("Labor Contract {0} ({1}) expires on {2}").format(
						contract.name, contract.employee_name, contract.end_date
					),
					"document_type": "Labor Contract",
					"document_name": contract.name,
				}
			).insert(ignore_permissions=True)


def _expire_overdue_contracts():
	overdue = frappe.get_all(
		"Labor Contract",
		filters={"status": "Active", "docstatus": 1, "end_date": ["<", today()]},
		pluck="name",
	)
	for name in overdue:
		frappe.db.set_value("Labor Contract", name, "status", "Expired")
