# Copyright (c) 2026, DCNet and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from dcnet_hrm import constants as const
from dcnet_hrm.payroll import pit


class PITAnnualSettlement(Document):
	@frappe.whitelist()
	def aggregate_from_salary_slips(self):
		fiscal_year = frappe.get_doc("Fiscal Year", self.fiscal_year)
		slips = frappe.get_all(
			"Salary Slip",
			filters={
				"company": self.company,
				"docstatus": 1,
				"start_date": [">=", fiscal_year.year_start_date],
				"end_date": ["<=", fiscal_year.year_end_date],
			},
			fields=["name", "employee", "taxable_income", "assessable_income"],
		)
		if not slips:
			frappe.msgprint(_("No submitted Salary Slip found for this Fiscal Year/Company."), alert=True)
			self.employees = []
			return

		by_employee = {}
		for slip in slips:
			bucket = by_employee.setdefault(
				slip.employee,
				{
					"total_taxable_income": 0,
					"total_assessable_income": 0,
					"tax_withheld": 0,
					"insurance_deducted": 0,
				},
			)
			bucket["total_taxable_income"] += flt(slip.taxable_income)
			bucket["total_assessable_income"] += flt(slip.assessable_income)

		slip_names = [s.name for s in slips]
		slip_to_employee = {s.name: s.employee for s in slips}
		deduction_rows = frappe.get_all(
			"Salary Detail",
			filters={
				"parenttype": "Salary Slip",
				"parentfield": "deductions",
				"parent": ["in", slip_names],
				"salary_component": ["in", [const.PIT_COMPONENT, *const.EMPLOYEE_INSURANCE_COMPONENTS.values()]],
			},
			fields=["parent", "salary_component", "amount"],
		)
		for row in deduction_rows:
			bucket = by_employee.get(slip_to_employee.get(row.parent))
			if not bucket:
				continue
			if row.salary_component == const.PIT_COMPONENT:
				bucket["tax_withheld"] += flt(row.amount)
			else:
				bucket["insurance_deducted"] += flt(row.amount)

		self.employees = []
		for employee, bucket in by_employee.items():
			total_deductions = (
				bucket["total_taxable_income"] - bucket["total_assessable_income"] - bucket["insurance_deducted"]
			)
			tax_payable_annual, _breakdown = pit.calculate_annual(
				bucket["total_assessable_income"], fiscal_year.year_end_date
			)
			self.append(
				"employees",
				{
					"employee": employee,
					"total_taxable_income": bucket["total_taxable_income"],
					"total_deductions": total_deductions,
					"tax_withheld": bucket["tax_withheld"],
					"tax_payable_annual": tax_payable_annual,
					"difference": tax_payable_annual - bucket["tax_withheld"],
				},
			)
		self.save()
