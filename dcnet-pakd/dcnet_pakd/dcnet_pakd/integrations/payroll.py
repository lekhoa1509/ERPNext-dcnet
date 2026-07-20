"""Payroll integration: create Additional Salary for Sales Commission."""

import frappe
from frappe import _
from frappe.utils import today


def push_to_additional_salary(pakd_doc, total_amount: float, payroll_month: str, pe_name: str) -> str | None:
	"""Create a draft Additional Salary for the Sales Commission amount.

	Returns the Additional Salary name, or None if creation failed.
	"""
	if total_amount <= 0:
		return None

	settings = frappe.get_cached_doc("PAKD Settings", "PAKD Settings")
	salary_component = settings.salary_component_luong_kd

	if not salary_component:
		frappe.throw(
			_("PAKD Settings: Salary Component for Sales Commission (salary_component_luong_kd) not configured")
		)

	# sales_person field is a direct Link to Employee
	employee = pakd_doc.sales_person
	if not employee:
		frappe.log_error(
			f"No Employee set on PAKD {pakd_doc.name} — skipping AS",
			"PAKD Payroll Integration",
		)
		return None

	# payroll_date = last day of payroll_month
	year, month = map(int, payroll_month.split("-"))
	import calendar
	last_day = calendar.monthrange(year, month)[1]
	payroll_date = f"{payroll_month}-{last_day:02d}"

	as_doc = frappe.new_doc("Additional Salary")
	as_doc.employee = employee
	as_doc.salary_component = salary_component
	as_doc.amount = total_amount
	as_doc.payroll_date = payroll_date
	as_doc.company = pakd_doc.company
	as_doc.remarks = f"PAKD {pakd_doc.name} | PE {pe_name}"
	as_doc.insert(ignore_permissions=True)
	# Leave as Draft — accountant submits during payroll processing
	return as_doc.name


