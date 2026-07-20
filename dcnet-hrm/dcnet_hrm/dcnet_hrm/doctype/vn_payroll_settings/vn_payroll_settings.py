import frappe
from frappe.model.document import Document


class VNPayrollSettings(Document):
	def onload(self):
		latest = frappe.db.get_value(
			"Insurance Rate", {}, "name", order_by="effective_from desc"
		)
		if latest:
			self.current_insurance_rate = latest
