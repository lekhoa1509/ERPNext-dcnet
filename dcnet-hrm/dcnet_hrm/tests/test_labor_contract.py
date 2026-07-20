import frappe
from erpnext.setup.doctype.employee.test_employee import make_employee as _make_employee
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today


def get_test_company():
	company = frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		company = frappe.get_all("Company", limit=1)[0].name
	return company


class TestLaborContract(FrappeTestCase):
	def setUp(self):
		self.company = get_test_company()

	def _employee(self, suffix, **kwargs):
		email = f"labor.contract.test.{suffix}@example.com"
		kwargs.setdefault("date_of_joining", "2020-01-01")
		name = _make_employee(email, company=self.company, **kwargs)
		return frappe.get_doc("Employee", name)

	def _contract(self, employee, contract_number, start_date, end_date=None, contract_type="Fixed-term", **kwargs):
		doc = frappe.get_doc(
			{
				"doctype": "Labor Contract",
				"employee": employee,
				"contract_number": contract_number,
				"contract_type": contract_type,
				"start_date": start_date,
				"end_date": end_date,
				"base_salary": 10_000_000,
				"insurance_salary": 10_000_000,
				**kwargs,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc

	def test_first_contract_submits_and_becomes_active(self):
		emp = self._employee("basic")
		contract = self._contract(emp.name, "LC-BASIC-001", "2026-01-01", "2026-06-30")
		contract.submit()
		self.assertEqual(contract.status, "Active")

	def test_cannot_have_two_overlapping_active_contracts(self):
		emp = self._employee("overlap")
		c1 = self._contract(emp.name, "LC-OVERLAP-001", "2026-01-01", "2026-06-30")
		c1.submit()

		c2 = self._contract(emp.name, "LC-OVERLAP-002", "2026-03-01", "2026-09-30")
		with self.assertRaises(frappe.ValidationError):
			c2.submit()

	def test_renewal_supersedes_previous_contract(self):
		emp = self._employee("renewal")
		c1 = self._contract(emp.name, "LC-RENEW-001", "2026-01-01", "2026-06-30")
		c1.submit()

		c2 = self._contract(
			emp.name, "LC-RENEW-002", "2026-07-01", "2026-12-31", previous_contract=c1.name
		)
		c2.submit()

		self.assertEqual(c2.status, "Active")
		self.assertEqual(frappe.db.get_value("Labor Contract", c1.name, "status"), "Terminated")

	def test_renewal_with_changed_insurance_salary_creates_declaration_suggestion(self):
		emp = self._employee("adjust")
		c1 = self._contract(emp.name, "LC-ADJUST-001", "2026-01-01", "2026-06-30", insurance_salary=10_000_000)
		c1.submit()

		before = frappe.db.count("Insurance Declaration", {"declaration_type": "Rate Adjustment"})
		c2 = self._contract(
			emp.name,
			"LC-ADJUST-002",
			"2026-07-01",
			"2026-12-31",
			previous_contract=c1.name,
			insurance_salary=15_000_000,
		)
		c2.submit()
		after = frappe.db.count("Insurance Declaration", {"declaration_type": "Rate Adjustment"})

		self.assertEqual(after, before + 1)
		declaration = frappe.get_last_doc("Insurance Declaration", filters={"declaration_type": "Rate Adjustment"})
		self.assertEqual(declaration.employees[0].employee, emp.name)
		self.assertEqual(declaration.employees[0].old_amount, 10_000_000)
		self.assertEqual(declaration.employees[0].new_amount, 15_000_000)
		self.assertEqual(declaration.docstatus, 0)  # chỉ tạo Draft, chưa submit

	def test_third_consecutive_fixed_term_blocked_without_override(self):
		emp = self._employee("consecutive")
		c1 = self._contract(emp.name, "LC-CONSEC-001", "2026-01-01", "2026-03-31")
		c1.submit()
		c2 = self._contract(emp.name, "LC-CONSEC-002", "2026-04-01", "2026-06-30", previous_contract=c1.name)
		c2.submit()
		c3 = self._contract(emp.name, "LC-CONSEC-003", "2026-07-01", "2026-09-30", previous_contract=c2.name)

		with self.assertRaises(frappe.ValidationError):
			c3.submit()

	def test_third_consecutive_fixed_term_allowed_with_override(self):
		emp = self._employee("consecutive-ov")
		c1 = self._contract(emp.name, "LC-CONSECOV-001", "2026-01-01", "2026-03-31")
		c1.submit()
		c2 = self._contract(
			emp.name, "LC-CONSECOV-002", "2026-04-01", "2026-06-30", previous_contract=c1.name
		)
		c2.submit()
		c3 = self._contract(
			emp.name,
			"LC-CONSECOV-003",
			"2026-07-01",
			"2026-09-30",
			previous_contract=c2.name,
			override_reason="Khách hàng yêu cầu gia hạn thêm 1 lần, đã giải trình với NLĐ",
		)
		c3.submit()

		self.assertEqual(c3.status, "Active")

	def test_indefinite_term_does_not_require_end_date(self):
		emp = self._employee("indefinite")
		contract = self._contract(emp.name, "LC-INDEF-001", "2026-01-01", end_date=None, contract_type="Indefinite-term")
		contract.submit()
		self.assertEqual(contract.status, "Active")


class TestLaborContractExpiryScheduler(FrappeTestCase):
	def setUp(self):
		self.company = get_test_company()

	def _employee(self, suffix):
		email = f"labor.contract.expiry.{suffix}@example.com"
		name = _make_employee(email, company=self.company, date_of_joining="2020-01-01")
		return frappe.get_doc("Employee", name)

	def test_expire_overdue_contracts(self):
		from dcnet_hrm.dcnet_hrm.doctype.labor_contract.labor_contract import _expire_overdue_contracts

		emp = self._employee("overdue")
		contract = frappe.get_doc(
			{
				"doctype": "Labor Contract",
				"employee": emp.name,
				"contract_number": "LC-OVERDUE-001",
				"contract_type": "Fixed-term",
				"start_date": add_days(today(), -100),
				"end_date": add_days(today(), -1),
				"base_salary": 10_000_000,
				"insurance_salary": 10_000_000,
			}
		)
		contract.insert(ignore_permissions=True)
		contract.submit()
		self.assertEqual(contract.status, "Active")

		_expire_overdue_contracts()

		self.assertEqual(frappe.db.get_value("Labor Contract", contract.name, "status"), "Expired")

	def test_notify_upcoming_expiry_creates_notification_log(self):
		from dcnet_hrm.dcnet_hrm.doctype.labor_contract.labor_contract import _notify_upcoming_expiry

		if not frappe.db.exists("Has Role", {"role": "HR Manager", "parent": "Administrator"}):
			frappe.get_doc({"doctype": "Has Role", "parent": "Administrator", "parenttype": "User", "parentfield": "roles", "role": "HR Manager"}).insert(ignore_permissions=True)

		emp = self._employee("upcoming")
		contract = frappe.get_doc(
			{
				"doctype": "Labor Contract",
				"employee": emp.name,
				"contract_number": "LC-UPCOMING-001",
				"contract_type": "Fixed-term",
				"start_date": add_days(today(), -60),
				"end_date": add_days(today(), 10),
				"base_salary": 10_000_000,
				"insurance_salary": 10_000_000,
			}
		)
		contract.insert(ignore_permissions=True)
		contract.submit()

		before = frappe.db.count("Notification Log", {"document_name": contract.name})
		_notify_upcoming_expiry()
		after = frappe.db.count("Notification Log", {"document_name": contract.name})

		self.assertGreater(after, before)
