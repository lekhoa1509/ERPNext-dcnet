"""Golden test — assert engine output matches Excel Mẫu 01 + Mẫu 03 cell-by-cell.

Source files (do NOT modify):
- docs/accounting-requirements/Mẫu số 01.PAKD-DCNET_Vr25.1 (1).xlsx
- docs/accounting-requirements/Mẫu số 03.PAKD-DCNET_Vr25.1 (1).xlsx

This file encodes the Excel inputs + formulas as plain Python so the test runs
without openpyxl / a live xlsx file. Each expected value is computed exactly as
Excel evaluates the formula at qty=1 — the canonical Excel sample case.

Run:
  env/bin/python -m unittest dcnet_pakd.tests.test_golden_excel -v
"""

import unittest

from dcnet_pakd.utils.engine import compute_pakd_line


# ----------------------------------------------------------------------------
# Mẫu 01 — Recurring Telecom (P2P / MPLS / ILL / FTTH DN)
# ----------------------------------------------------------------------------
# Source cell map (sheet "KPI T12"):
#   D16 = 1, E16 = 13500, F16 = 3000 (setup fee)
#   Row 19 MS:       D19=0.1,   E19=E16-E20=10500,   G19=D19*E19=1050     per month
#   Row 20 AC:       D20=0.75,  E20=3000,            G20=E20*D20=2250     per month
#   Row 21 License:  D21=0.022, E21=E16=13500,       G21=D21*E21=297      per month
#   Row 22 SC:       D22=0.06,  E22=E16-E20=10500,   G22=D22*E22=630      per month
#   G17 (revenue_service per month) = G16 - G18 = 13500 - 4227 = 9273
#   G18 (total cost per month) = SUM(G19:G22) = 1050+2250+297+630 = 4227
MAU01_INPUT = {
	"unit_price": 13500,
	"add_costs_unit_price": 3000,
	"qty": 1,
}
MAU01_HEADER = {"pakd_type": "Recurring Telecom"}
MAU01_COMPONENTS = [
	{"component_name": "Manager Services", "rate": 10.0, "base_formula": "unit_price_minus_add_costs"},
	{"component_name": "Add Costs", "rate": 75.0, "base_formula": "add_costs_gross"},
	{"component_name": "License Fee", "rate": 2.2, "base_formula": "unit_price"},
	{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "unit_price_minus_add_costs"},
]
MAU01_EXPECTED = {
	"revenue_contract": 13500,
	"manager_services": 1050,
	"add_costs": 2250,
	"license_fee": 297,
	"sales_commission": 630,
	"total_cost": 4227,
	"revenue_service": 9273,
}


# ----------------------------------------------------------------------------
# Mẫu 03 — One-off Sale/Project (mua bán VTTB, thi công)
# ----------------------------------------------------------------------------
# Source cell map (sheet "KPI T12"):
#   D16 = 1, E16 = 13500
#   F16 = E16 = 13500 (revenue total)
#   Row 19 MS:       D19=0.1,   E19=E16-E20=10500,   F19=D19*(F16-F20)=0.1*(13500-2250)=1125
#   Row 20 AC:       D20=0.75,  E20=3000,            F20=E20*D20=2250
#   Row 21 SC:       D21=0.06,  E21=E16-E20=10500,   F21=D21*E21=0.06*10500=630
#   F18 = SUM(F19:I21) = 1125 + 2250 + 630 = 4005
#   F17 = F16 - F18 = 13500 - 4005 = 9495
#
# NOTE: No License Fee row in Mẫu 03 (License = GPVT only for recurring telecom).
#
# In Mẫu 01 the MS basis subtracts AC_unit_price (full 3000) per Excel row 19
# formula E19=E16-E20. In Mẫu 03 the MS basis subtracts AC_total (E20*D20 = 2250)
# per Excel row 19 formula F19=D19*(F16-F20). Engine v0.2.0 distinguishes via
# two rate_base options: contract_minus_ac_unit (Mẫu 01 MS/SC + Mẫu 03 SC) and
# contract_minus_ac_total (Mẫu 03 MS). The test selectors below assert both.
#
# Legacy compat: passing the 3-component rule_components list (no beneficiary_specs)
# keeps the v0.1.x semantics (engine uses contract_minus_ac_unit for MS), so
# tests for the legacy path live in test_engine.TestComputePAKDLineOneOffLegacy.
# The v0.2.0 Excel-faithful path is exercised in TestGoldenMau03BeneficiaryV02
# below.
MAU03_INPUT = {
	"unit_price": 13500,
	"add_costs_unit_price": 3000,
	"qty": 1,
}
MAU03_HEADER = {"pakd_type": "One-off Sale/Project"}
MAU03_COMPONENTS = [
	{"component_name": "Manager Services", "rate": 10.0, "base_formula": "unit_price_minus_add_costs"},
	{"component_name": "Add Costs", "rate": 75.0, "base_formula": "add_costs_gross"},
	{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "unit_price_minus_add_costs"},
]
# Excel-authoritative values
MAU03_EXPECTED_EXCEL = {
	"revenue_contract": 13500,
	"manager_services": 1125,
	"add_costs": 2250,
	"license_fee": 0,
	"sales_commission": 630,
	"total_cost": 4005,
	"revenue_service": 9495,
}
# Engine v0.1.x values (deviates on MS)
MAU03_EXPECTED_ENGINE_V01 = {
	"revenue_contract": 13500,
	"manager_services": 1050,
	"add_costs": 2250,
	"license_fee": 0,
	"sales_commission": 630,
	"total_cost": 3930,
	"revenue_service": 9570,
}


class TestGoldenMau01(unittest.TestCase):
	"""Mẫu 01 — Excel cell-by-cell vs engine output."""

	def test_revenue_contract(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertEqual(result["revenue_contract"], MAU01_EXPECTED["revenue_contract"])

	def test_manager_services(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertEqual(result["manager_services"], MAU01_EXPECTED["manager_services"])

	def test_add_costs(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertEqual(result["add_costs"], MAU01_EXPECTED["add_costs"])

	def test_license_fee(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertAlmostEqual(result["license_fee"], MAU01_EXPECTED["license_fee"], places=2)

	def test_sales_commission(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertEqual(result["sales_commission"], MAU01_EXPECTED["sales_commission"])

	def test_total_cost(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertAlmostEqual(result["total_cost"], MAU01_EXPECTED["total_cost"], places=2)

	def test_revenue_service(self):
		result = compute_pakd_line(MAU01_INPUT, MAU01_HEADER, MAU01_COMPONENTS)
		self.assertAlmostEqual(result["revenue_service"], MAU01_EXPECTED["revenue_service"], places=2)


class TestGoldenMau03EngineCurrent(unittest.TestCase):
	"""Mẫu 03 — assert engine v0.1.x semantics (DEVIATES from Excel on MS).

	Until anh Long decides whether to bring engine in line with Excel Mẫu 03,
	these tests freeze the v0.1.x behavior so any silent regression is caught.
	"""

	def test_revenue_contract(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, MAU03_COMPONENTS)
		self.assertEqual(result["revenue_contract"], MAU03_EXPECTED_ENGINE_V01["revenue_contract"])

	def test_manager_services_engine_current(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, MAU03_COMPONENTS)
		self.assertEqual(
			result["manager_services"],
			MAU03_EXPECTED_ENGINE_V01["manager_services"],
			msg="Engine v0.1.x uses unit_price_minus_add_costs (unit-level subtraction)",
		)

	def test_add_costs(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, MAU03_COMPONENTS)
		self.assertEqual(result["add_costs"], MAU03_EXPECTED_ENGINE_V01["add_costs"])

	def test_sales_commission(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, MAU03_COMPONENTS)
		self.assertEqual(result["sales_commission"], MAU03_EXPECTED_ENGINE_V01["sales_commission"])

	def test_license_fee_zero(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, MAU03_COMPONENTS)
		self.assertEqual(result["license_fee"], 0)


class TestGoldenMau03BeneficiaryV02(unittest.TestCase):
	"""Mẫu 03 v0.2.0 path: MS via contract_minus_ac_total → Excel-faithful 1125."""

	_RULE_SC_ONLY = [
		{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "contract_minus_ac_unit"},
	]
	_BENEFICIARY_SPECS = [
		# AC first so contract_minus_ac_total resolves in pass 2
		{"kind": "Add Costs", "rate_pct": 75.0, "rate_base": "ac_only"},
		{"kind": "Manager Services", "rate_pct": 10.0, "rate_base": "contract_minus_ac_total"},
	]

	def test_manager_services_matches_excel(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, self._RULE_SC_ONLY, self._BENEFICIARY_SPECS)
		by_kind = {b["kind"]: b for b in result["beneficiaries"]}
		self.assertEqual(
			by_kind["Manager Services"]["amount"],
			MAU03_EXPECTED_EXCEL["manager_services"],
			msg="Excel Mẫu 03 F19 = D19*(F16-F20) = 0.1*(13500-2250) = 1125",
		)

	def test_add_costs_matches_excel(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, self._RULE_SC_ONLY, self._BENEFICIARY_SPECS)
		by_kind = {b["kind"]: b for b in result["beneficiaries"]}
		self.assertEqual(by_kind["Add Costs"]["amount"], MAU03_EXPECTED_EXCEL["add_costs"])

	def test_sales_commission_matches_excel(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, self._RULE_SC_ONLY, self._BENEFICIARY_SPECS)
		self.assertEqual(result["sales_commission"], MAU03_EXPECTED_EXCEL["sales_commission"])

	def test_total_cost_matches_excel(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, self._RULE_SC_ONLY, self._BENEFICIARY_SPECS)
		self.assertEqual(result["total_cost"], MAU03_EXPECTED_EXCEL["total_cost"])

	def test_revenue_service_matches_excel(self):
		result = compute_pakd_line(MAU03_INPUT, MAU03_HEADER, self._RULE_SC_ONLY, self._BENEFICIARY_SPECS)
		self.assertEqual(result["revenue_service"], MAU03_EXPECTED_EXCEL["revenue_service"])


if __name__ == "__main__":
	unittest.main()
