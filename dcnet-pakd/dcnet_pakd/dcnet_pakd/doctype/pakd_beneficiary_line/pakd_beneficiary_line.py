import frappe
from frappe.model.document import Document


class PAKDBeneficiaryLine(Document):
	def validate(self):
		# Auto-compute pit_amount + net_amount when amount + tax_pct present
		amount = float(self.amount_per_period or 0)
		tax_pct = float(self.recipient_tax_pct or 0)
		if self.recipient_name and tax_pct > 0:
			self.pit_amount = round(amount * tax_pct / 100.0, 0)
		else:
			self.pit_amount = 0
		self.net_amount = amount - self.pit_amount
