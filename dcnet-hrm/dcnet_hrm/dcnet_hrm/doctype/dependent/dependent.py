import frappe
from frappe import _
from frappe.model.document import Document


class Dependent(Document):
	def validate(self):
		if self.deduction_to and self.deduction_from and self.deduction_to < self.deduction_from:
			frappe.throw(_("Deduction To must be on or after Deduction From."))
