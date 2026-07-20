import frappe
from erpnext.setup.doctype.employee.test_employee import make_employee as _make_employee
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today

from dcnet_hrm.tests.test_vn_payroll import get_test_company


class TestInsuranceDeclaration(FrappeTestCase):
	def setUp(self):
		self.company = get_test_company()

	def _employee(self, suffix):
		email = f"insurance.declaration.test.{suffix}@example.com"
		name = _make_employee(email, company=self.company, date_of_joining="2020-01-01")
		return name

	def test_duplicate_employee_in_table_blocked(self):
		emp = self._employee("dup")
		doc = frappe.get_doc(
			{
				"doctype": "Insurance Declaration",
				"declaration_type": "New Registration",
				"month": today(),
				"employees": [
					{"employee": emp, "new_amount": 10_000_000, "effective_date": today()},
					{"employee": emp, "new_amount": 12_000_000, "effective_date": today()},
				],
			}
		)
		with self.assertRaises(frappe.ValidationError):
			doc.insert(ignore_permissions=True)

	def test_export_d02lt_blocked_without_template(self):
		from dcnet_hrm.export.d02lt import export_d02lt

		emp = self._employee("export")
		doc = frappe.get_doc(
			{
				"doctype": "Insurance Declaration",
				"declaration_type": "Rate Adjustment",
				"month": today(),
				"employees": [{"employee": emp, "new_amount": 10_000_000, "effective_date": today()}],
			}
		)
		doc.insert(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			export_d02lt(doc.name)
