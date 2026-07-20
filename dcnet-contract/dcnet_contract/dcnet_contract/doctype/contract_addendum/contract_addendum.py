import frappe
from frappe.model.document import Document


class ContractAddendum(Document):
	def validate(self):
		if self.effective_from and self.addendum_date and self.effective_from < self.addendum_date:
			frappe.throw("Ngày hiệu lực không được trước ngày ký phụ lục")
