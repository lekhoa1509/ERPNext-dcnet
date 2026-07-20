import frappe
from erpnext.setup.doctype.employee.test_employee import make_employee as _make_employee
from frappe.tests.utils import FrappeTestCase

from dcnet_hrm.payroll import pit
from dcnet_hrm.tests.test_vn_payroll import ensure_salary_structure, get_test_company


def ensure_fiscal_year(year_start_date, year_end_date):
	existing = frappe.db.get_value(
		"Fiscal Year", {"year_start_date": ["<=", year_start_date], "year_end_date": [">=", year_end_date]}, "name"
	)
	if existing:
		return existing
	doc = frappe.get_doc(
		{
			"doctype": "Fiscal Year",
			"year": "_Test PIT Fiscal Year",
			"year_start_date": year_start_date,
			"year_end_date": year_end_date,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def make_submitted_salary_slip(
	employee, company, start_date, end_date, taxable_income, assessable_income, bhxh, bhyt, bhtn, tax
):
	structure_name = "_Test VN Salary Structure"
	ensure_salary_structure(structure_name, company)
	doc = frappe.new_doc("Salary Slip")
	doc.employee = employee
	doc.company = company
	doc.posting_date = end_date
	doc.start_date = start_date
	doc.end_date = end_date
	doc.salary_structure = structure_name
	doc.currency = "VND"
	doc.exchange_rate = 1
	doc.total_working_days = 26
	doc.payment_days = 26
	doc.taxable_income = taxable_income
	doc.assessable_income = assessable_income
	doc.append("deductions", {"salary_component": "BHXH (NLĐ)", "amount": bhxh})
	doc.append("deductions", {"salary_component": "BHYT (NLĐ)", "amount": bhyt})
	doc.append("deductions", {"salary_component": "BHTN (NLĐ)", "amount": bhtn})
	doc.append("deductions", {"salary_component": "Thuế TNCN", "amount": tax})
	# Bỏ qua validate() của HRMS (cần Holiday List/Attendance...) — test này
	# chỉ cần bản ghi docstatus=1 với đúng số liệu để query aggregation, không
	# đi qua luồng payroll thật.
	doc.flags.ignore_validate = True
	doc.insert(ignore_permissions=True)
	frappe.db.set_value("Salary Slip", doc.name, "docstatus", 1)
	return doc.name


class TestPITAnnual(FrappeTestCase):
	"""pit.calculate_annual() — thuần, không cần DB."""

	def test_annual_brackets_scale_by_12(self):
		# 13.8tr/năm vẫn nằm trong bậc 1 (5m*12=60m) => 5%
		tax, breakdown = pit.calculate_annual(13_800_000, "2026-01-01")
		self.assertEqual(tax, 690_000)
		self.assertEqual(len(breakdown), 1)

	def test_annual_multi_bracket(self):
		# 240tr/năm: 60m@5%+60m@10%+96m@15%+24m@20%
		tax, _breakdown = pit.calculate_annual(240_000_000, "2026-01-01")
		expected = 60_000_000 * 0.05 + 60_000_000 * 0.10 + 96_000_000 * 0.15 + 24_000_000 * 0.20
		self.assertEqual(tax, round(expected))


class TestPITAnnualSettlementAggregation(FrappeTestCase):
	def setUp(self):
		self.company = get_test_company()
		self.fiscal_year = ensure_fiscal_year("2026-01-01", "2026-12-31")

	def test_aggregate_from_salary_slips(self):
		email = "pit.annual.test@example.com"
		employee = _make_employee(email, company=self.company, date_of_joining="2020-01-01")

		make_submitted_salary_slip(
			employee, self.company, "2026-01-01", "2026-01-31", 20_000_000, 6_900_000, 1_600_000, 300_000, 200_000, 440_000
		)
		make_submitted_salary_slip(
			employee, self.company, "2026-02-01", "2026-02-28", 20_000_000, 6_900_000, 1_600_000, 300_000, 200_000, 440_000
		)

		settlement = frappe.get_doc(
			{"doctype": "PIT Annual Settlement", "fiscal_year": self.fiscal_year, "company": self.company}
		)
		settlement.insert(ignore_permissions=True)
		settlement.aggregate_from_salary_slips()
		settlement.reload()

		row = next(r for r in settlement.employees if r.employee == employee)
		self.assertEqual(row.total_taxable_income, 40_000_000)
		self.assertEqual(row.tax_withheld, 880_000)
		self.assertEqual(row.total_deductions, 40_000_000 - 13_800_000 - 4_200_000)
		self.assertEqual(row.tax_payable_annual, 690_000)  # 13.8tr @ 5%
		self.assertEqual(row.difference, 690_000 - 880_000)  # âm => được hoàn thuế
