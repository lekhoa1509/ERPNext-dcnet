"""Unit test cho payroll engine VN (Phase 1).

Chiến lược:
- pit.calculate() / social_insurance.calculate(): test thuần (không cần
  Salary Slip), chỉ cần Insurance Rate / Statutory Wage đã seed sẵn qua
  app install (xem dcnet_hrm/install.py).
- vn_payroll.calculate(): dựng 1 Salary Slip document TRONG MEMORY (không
  insert/submit) với employee + Salary Structure Assignment thật trong DB,
  rồi gọi hook trực tiếp — tránh lệ thuộc vào Holiday List/working-day
  machinery của HRMS (không liên quan tới logic của app này).
"""

import frappe
from erpnext.setup.doctype.employee.test_employee import make_employee as _make_employee
from frappe.tests.utils import FrappeTestCase

from dcnet_hrm import constants as const
from dcnet_hrm.payroll import pit, social_insurance, vn_payroll

BASIC = const.BASIC_SALARY_COMPONENT
MEAL = const.MEAL_ALLOWANCE_COMPONENT
PHONE = const.PHONE_ALLOWANCE_COMPONENT
OT = const.OVERTIME_COMPONENT


def get_test_company():
	company = frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		company = frappe.get_all("Company", limit=1)[0].name
	return company


def ensure_salary_structure(name, company):
	if frappe.db.exists("Salary Structure", name):
		return
	frappe.get_doc(
		{
			"doctype": "Salary Structure",
			"name": name,
			"company": company,
			"currency": "VND",
			"is_active": "Yes",
			"payroll_frequency": "Monthly",
		}
	).insert(ignore_permissions=True)


def make_ssa(employee, company, base, insurance_salary=None, net_agreement=0, from_date="2026-01-01"):
	structure_name = "_Test VN Salary Structure"
	ensure_salary_structure(structure_name, company)
	if frappe.db.exists("Salary Structure Assignment", {"employee": employee}):
		frappe.db.delete("Salary Structure Assignment", {"employee": employee})
	ssa = frappe.new_doc("Salary Structure Assignment")
	ssa.employee = employee
	ssa.company = company
	ssa.currency = "VND"
	ssa.salary_structure = structure_name
	ssa.from_date = from_date
	ssa.base = base
	ssa.insurance_salary = insurance_salary if insurance_salary is not None else base
	ssa.net_agreement = net_agreement
	ssa.insert(ignore_permissions=True)
	ssa.submit()
	return ssa


def build_payslip(employee, company, start_date, end_date, earnings, payment_days):
	doc = frappe.new_doc("Salary Slip")
	doc.employee = employee
	doc.company = company
	doc.posting_date = end_date
	doc.start_date = start_date
	doc.end_date = end_date
	doc.currency = "VND"
	doc.exchange_rate = 1
	doc.payment_days = payment_days
	for component, amount in earnings.items():
		doc.append("earnings", {"salary_component": component, "amount": amount})
	doc.gross_pay = sum(earnings.values())
	return doc


def get_deduction(doc, component):
	for row in doc.deductions:
		if row.salary_component == component:
			return row.amount
	return 0


class TestPIT(FrappeTestCase):
	"""Thuế TNCN lũy tiến — không cần DB."""

	def test_zero_or_negative_income(self):
		tax, breakdown = pit.calculate(0, "2026-01-01")
		self.assertEqual(tax, 0)
		self.assertEqual(breakdown, [])

		tax, breakdown = pit.calculate(-5_000_000, "2026-01-01")
		self.assertEqual(tax, 0)

	def test_first_bracket_only(self):
		tax, breakdown = pit.calculate(3_000_000, "2026-01-01")
		self.assertEqual(tax, 150_000)  # 5%
		self.assertEqual(len(breakdown), 1)

	def test_multi_bracket(self):
		# 5m@5% + 5m@10% + 8m@15% + 2m@20% = 250k+500k+1200k+400k
		tax, breakdown = pit.calculate(20_000_000, "2026-01-01")
		self.assertEqual(tax, 2_350_000)
		self.assertEqual(len(breakdown), 4)

	def test_top_bracket_matches_quick_formula(self):
		# Công thức rút gọn: 35% * TNTT - 9.85tr
		tax, _breakdown = pit.calculate(100_000_000, "2026-01-01")
		expected = round(0.35 * 100_000_000 - 9_850_000)
		self.assertEqual(tax, expected)
		self.assertEqual(tax, 25_150_000)

	def test_round_vnd_half_up(self):
		self.assertEqual(const.round_vnd(100.5), 101)
		self.assertEqual(const.round_vnd(100.4), 100)


class TestSocialInsurance(FrappeTestCase):
	"""BHXH/BHYT/BHTN/TNLĐ-BNN — dùng Insurance Rate/Statutory Wage đã seed
	qua app install (effective_from 2024-07-01)."""

	ON_DATE = "2026-01-01"

	def test_under_cap(self):
		result = social_insurance.calculate(10_000_000, "Fully Insured", "Region I", self.ON_DATE)
		self.assertEqual(result["types"]["BHXH"]["employee"], 800_000)
		self.assertEqual(result["types"]["BHXH"]["employer"], 1_750_000)
		self.assertEqual(result["types"]["BHYT"]["employee"], 150_000)
		self.assertEqual(result["types"]["BHTN"]["employee"], 100_000)
		self.assertEqual(result["employee_total"], 800_000 + 150_000 + 100_000)

	def test_capped_by_base_salary(self):
		# Trần BHXH/BHYT/TNLĐ-BNN = 20 * 2.340.000 = 46.800.000
		result = social_insurance.calculate(80_000_000, "Fully Insured", "Region I", self.ON_DATE)
		self.assertEqual(result["types"]["BHXH"]["capped_salary"], 46_800_000)
		self.assertEqual(result["types"]["BHXH"]["employee"], 3_744_000)
		self.assertEqual(result["types"]["TNLĐ-BNN"]["employer"], 234_000)
		# BHTN chưa vượt trần vùng I (20*4.960.000=99.200.000) nên KHÔNG bị áp trần
		self.assertEqual(result["types"]["BHTN"]["capped_salary"], 80_000_000)
		self.assertEqual(result["types"]["BHTN"]["employee"], 800_000)

	def test_bhtn_capped_by_region(self):
		# Trần BHTN vùng IV = 20 * 3.450.000 = 69.000.000
		result = social_insurance.calculate(150_000_000, "Fully Insured", "Region IV", self.ON_DATE)
		self.assertEqual(result["types"]["BHTN"]["capped_salary"], 69_000_000)
		self.assertEqual(result["types"]["BHTN"]["employee"], 690_000)
		self.assertEqual(result["types"]["BHXH"]["capped_salary"], 46_800_000)

	def test_health_insurance_only(self):
		result = social_insurance.calculate(10_000_000, "Health Insurance Only", "Region I", self.ON_DATE)
		self.assertNotIn("BHXH", result["types"])
		self.assertNotIn("BHTN", result["types"])
		self.assertEqual(result["types"]["BHYT"]["employee"], 150_000)
		self.assertEqual(result["employee_total"], 150_000)

	def test_not_insured(self):
		result = social_insurance.calculate(10_000_000, "Not Insured", "Region I", self.ON_DATE)
		self.assertEqual(result["types"], {})
		self.assertEqual(result["employee_total"], 0)
		self.assertEqual(result["employer_total"], 0)


class TestVNPayrollEngine(FrappeTestCase):
	"""Test end-to-end hook `vn_payroll.calculate()` trên Salary Slip dựng
	trong memory (không insert/submit) + Employee/SSA thật trong DB."""

	def setUp(self):
		self.company = get_test_company()
		# VN Payroll Settings là Single — set_single_value không nằm trong
		# savepoint rollback per-test của FrappeTestCase, nên reset tay ở
		# đầu mỗi test để tránh 1 test rò state sang test chạy sau (theo
		# thứ tự alphabet của unittest).
		frappe.db.set_single_value("VN Payroll Settings", "union_fee_monthly_cap", 0)

	def _employee(self, suffix, **kwargs):
		email = f"vn.payroll.test.{suffix}@example.com"
		kwargs.setdefault("date_of_joining", "2020-01-01")
		name = _make_employee(email, company=self.company, **kwargs)
		return frappe.get_doc("Employee", name)

	def _dependent(self, employee, deduction_from, deduction_to=None):
		frappe.get_doc(
			{
				"doctype": "Dependent",
				"employee": employee,
				"full_name": "Test Dependent",
				"relationship": "Child",
				"registration_status": "Registered",
				"deduction_from": deduction_from,
				"deduction_to": deduction_to,
			}
		).insert(ignore_permissions=True)

	def test_basic_case_no_dependents(self):
		emp = self._employee("basic", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=20_000_000, insurance_salary=20_000_000)
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 20_000_000}, payment_days=26
		)

		vn_payroll.calculate(doc)

		self.assertEqual(get_deduction(doc, "BHXH (NLĐ)"), 1_600_000)
		self.assertEqual(get_deduction(doc, "BHYT (NLĐ)"), 300_000)
		self.assertEqual(get_deduction(doc, "BHTN (NLĐ)"), 200_000)
		self.assertEqual(doc.taxable_income, 20_000_000)
		self.assertEqual(doc.dependent_count, 0)
		self.assertEqual(doc.assessable_income, 6_900_000)  # 20m - 2.1m BH - 11m
		self.assertEqual(get_deduction(doc, "Thuế TNCN"), 440_000)  # 5m@5%+1.9m@10%
		self.assertEqual(doc.net_pay, 20_000_000 - 2_100_000 - 440_000)

	def test_dependent_counted_when_active(self):
		emp = self._employee("dep-active", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=20_000_000, insurance_salary=20_000_000)
		self._dependent(emp.name, deduction_from="2025-06-01")
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 20_000_000}, payment_days=26
		)

		vn_payroll.calculate(doc)

		self.assertEqual(doc.dependent_count, 1)
		self.assertEqual(doc.assessable_income, 2_500_000)  # 6.9m - 4.4m
		self.assertEqual(get_deduction(doc, "Thuế TNCN"), 125_000)  # 5%

	def test_dependent_not_counted_before_deduction_from(self):
		emp = self._employee("dep-future", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=20_000_000, insurance_salary=20_000_000)
		# Kỳ lương là tháng 1/2026, NPT chỉ có hiệu lực từ tháng 3/2026 → chưa tính
		self._dependent(emp.name, deduction_from="2026-03-01")
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 20_000_000}, payment_days=26
		)

		vn_payroll.calculate(doc)

		self.assertEqual(doc.dependent_count, 0)
		self.assertEqual(doc.assessable_income, 6_900_000)

	def test_skips_insurance_when_payment_days_below_minimum(self):
		emp = self._employee("under-min-days", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=20_000_000, insurance_salary=20_000_000)
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 20_000_000}, payment_days=10
		)

		vn_payroll.calculate(doc)

		self.assertEqual(get_deduction(doc, "BHXH (NLĐ)"), 0)
		self.assertEqual(get_deduction(doc, "BHXH (DN)"), 0)
		self.assertEqual(doc.capped_insurance_salary, 0)
		# Không BH => giảm trừ chỉ còn bản thân: 20m - 11m = 9m => 5m@5%+4m@10%
		self.assertEqual(doc.assessable_income, 9_000_000)
		self.assertEqual(get_deduction(doc, "Thuế TNCN"), 650_000)

	def test_maternity_like_zero_payment_days_no_insurance(self):
		"""Nghỉ thai sản cả tháng: BHXH chi trả trực tiếp, DN không tính lương
		=> Salary Slip tháng đó payment_days=0, không phát sinh BH qua payroll."""
		emp = self._employee("maternity", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=20_000_000, insurance_salary=20_000_000)
		doc = build_payslip(emp.name, self.company, "2026-01-01", "2026-01-31", {}, payment_days=0)

		vn_payroll.calculate(doc)

		self.assertEqual(get_deduction(doc, "BHXH (NLĐ)"), 0)
		self.assertEqual(get_deduction(doc, "BHXH (DN)"), 0)
		self.assertEqual(doc.taxable_income, 0)
		self.assertEqual(get_deduction(doc, "Thuế TNCN"), 0)
		self.assertEqual(doc.net_pay, 0)

	def test_probation_flat_tax_10_percent(self):
		emp = self._employee(
			"probation",
			insurance_status="Fully Insured",
			minimum_wage_region="Region I",
			employment_type="Probation",
		)
		make_ssa(emp.name, self.company, base=6_000_000, insurance_salary=6_000_000)
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 6_000_000}, payment_days=26
		)

		vn_payroll.calculate(doc)

		self.assertEqual(get_deduction(doc, "Thuế TNCN"), 600_000)  # 10% flat, không giảm trừ
		self.assertEqual(doc.assessable_income, doc.taxable_income)

	def test_meal_allowance_partial_exemption(self):
		emp = self._employee("meal", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=15_000_000, insurance_salary=15_000_000)
		doc = build_payslip(
			emp.name,
			self.company,
			"2026-01-01",
			"2026-01-31",
			{BASIC: 15_000_000, MEAL: 1_000_000},
			payment_days=26,
		)

		vn_payroll.calculate(doc)

		# Cơm miễn tối đa 730k, phần vượt (270k) vẫn chịu thuế
		self.assertEqual(doc.taxable_income, 16_000_000 - 730_000)

	def test_phone_allowance_fully_exempt_uncapped(self):
		emp = self._employee("phone", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=15_000_000, insurance_salary=15_000_000)
		doc = build_payslip(
			emp.name,
			self.company,
			"2026-01-01",
			"2026-01-31",
			{BASIC: 15_000_000, PHONE: 2_000_000},
			payment_days=26,
		)

		vn_payroll.calculate(doc)

		# Phụ cấp điện thoại: miễn thuế toàn bộ theo cờ exempted_from_income_tax
		# (không áp trần như phụ cấp cơm) — khác test_meal_allowance ở trên.
		self.assertEqual(doc.taxable_income, 15_000_000)

	def test_overtime_fully_taxable_phase1_gap(self):
		"""⚠️ Ghi nhận hạn chế Phase 1: chưa tách được phần OT miễn thuế
		(vượt hệ số 100%) do thiếu breakdown giờ OT theo hệ số (Overtime
		Request — Phase 3). Test này PIN hành vi hiện tại; cập nhật khi
		Phase 3 triển khai và xoá comment này."""
		emp = self._employee("ot-gap", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=15_000_000, insurance_salary=15_000_000)
		doc = build_payslip(
			emp.name,
			self.company,
			"2026-01-01",
			"2026-01-31",
			{BASIC: 15_000_000, OT: 2_000_000},
			payment_days=26,
		)

		vn_payroll.calculate(doc)

		self.assertEqual(doc.taxable_income, 17_000_000)

	def test_union_fee_uncapped(self):
		emp = self._employee(
			"union", insurance_status="Fully Insured", minimum_wage_region="Region I", union_member=1
		)
		make_ssa(emp.name, self.company, base=15_000_000, insurance_salary=15_000_000)
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 15_000_000}, payment_days=26
		)

		vn_payroll.calculate(doc)

		self.assertEqual(get_deduction(doc, "Đoàn phí công đoàn"), 150_000)  # 1% * 15m
		self.assertEqual(get_deduction(doc, "Kinh phí công đoàn (DN)"), 300_000)  # 2% * 15m
		# Kinh phí công đoàn (DN) là statistical — không trừ vào net_pay
		self.assertEqual(doc.net_pay, 15_000_000 - get_deduction(doc, "BHXH (NLĐ)")
			- get_deduction(doc, "BHYT (NLĐ)") - get_deduction(doc, "BHTN (NLĐ)")
			- get_deduction(doc, "Thuế TNCN") - 150_000)

	def test_union_fee_capped(self):
		emp = self._employee(
			"union-cap", insurance_status="Fully Insured", minimum_wage_region="Region I", union_member=1
		)
		frappe.db.set_single_value("VN Payroll Settings", "union_fee_monthly_cap", 100_000)
		make_ssa(emp.name, self.company, base=15_000_000, insurance_salary=15_000_000)
		doc = build_payslip(
			emp.name, self.company, "2026-01-01", "2026-01-31", {BASIC: 15_000_000}, payment_days=26
		)

		vn_payroll.calculate(doc)

		self.assertEqual(get_deduction(doc, "Đoàn phí công đoàn"), 100_000)

	def test_net_to_gross_converges(self):
		emp = self._employee("net-agreement", insurance_status="Fully Insured", minimum_wage_region="Region I")
		make_ssa(emp.name, self.company, base=15_000_000, insurance_salary=15_000_000, net_agreement=1)
		doc = build_payslip(emp.name, self.company, "2026-01-01", "2026-01-31", {}, payment_days=26)

		vn_payroll.calculate(doc)

		self.assertLess(abs(doc.net_pay - 15_000_000), 2)
		# Gross phải > NET (vì có BH + thuế)
		self.assertGreater(doc.gross_pay, 15_000_000)
