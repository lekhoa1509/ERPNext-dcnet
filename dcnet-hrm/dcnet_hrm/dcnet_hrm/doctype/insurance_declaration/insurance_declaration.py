import frappe
from frappe import _
from frappe.model.document import Document


class InsuranceDeclaration(Document):
	def validate(self):
		seen = set()
		for row in self.employees:
			if row.employee in seen:
				frappe.throw(_("Employee {0} appears more than once in the Employees table.").format(row.employee))
			seen.add(row.employee)
