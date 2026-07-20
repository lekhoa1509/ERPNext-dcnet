import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class BranchCashAccess(Document):
	def validate(self):
		if self.company_wide_view:
			self.accounting_unit = None
			return

		if not self.accounting_unit:
			frappe.throw(_("Đơn vị hạch toán là bắt buộc nếu chưa bật xem toàn công ty."))

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
