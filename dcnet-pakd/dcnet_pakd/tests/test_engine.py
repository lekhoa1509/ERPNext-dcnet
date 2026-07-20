"""Golden tests for PAKD rule engine — pure Python, no frappe dependency.

v0.2.0 — Monthly FTTH Rollup branch dropped (per realignment D4). All PAKD
types now use the rule template + beneficiary_specs split. The test_golden_excel
suite covers the Excel-faithful Mẫu 01 + Mẫu 03 cell-by-cell parity.
"""

import datetime
import unittest

from dcnet_pakd.utils.engine import (
	compute_pakd_line,
	resolve_active_revision,
	resolve_rule,
)


# Default rule components per spec
RECURRING_TELECOM_COMPONENTS = [
	{"component_name": "Manager Services", "rate": 10.0, "base_formula": "unit_price_minus_add_costs"},
	{"component_name": "Add Costs", "rate": 75.0, "base_formula": "add_costs_gross"},
	{"component_name": "License Fee", "rate": 2.2, "base_formula": "unit_price"},
	{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "unit_price_minus_add_costs"},
]

# v0.2.0 canonical shape: SC + License in rule_components,
# MS + AC pushed into beneficiary_specs at the PAKD parent level.
RECURRING_RULE_SC_LICENSE_ONLY = [
	{"component_name": "License Fee", "rate": 2.2, "base_formula": "contract_revenue"},
	{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "contract_minus_ac_unit"},
]

MAU01_BENEFICIARY_SPECS = [
	{"kind": "Add Costs", "rate_pct": 75.0, "rate_base": "ac_only"},
	{"kind": "Manager Services", "rate_pct": 10.0, "rate_base": "contract_minus_ac_unit"},
]

MAU03_BENEFICIARY_SPECS = [
	# AC first so contract_minus_ac_total resolves correctly
	{"kind": "Add Costs", "rate_pct": 75.0, "rate_base": "ac_only"},
	{"kind": "Manager Services", "rate_pct": 10.0, "rate_base": "contract_minus_ac_total"},
]

ONEOFF_COMPONENTS = [
	{"component_name": "Manager Services", "rate": 10.0, "base_formula": "unit_price_minus_add_costs"},
	{"component_name": "Add Costs", "rate": 75.0, "base_formula": "add_costs_gross"},
	{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "unit_price_minus_add_costs"},
]


class TestResolveRule(unittest.TestCase):
	"""Test rule resolution priority."""

	def setUp(self):
		self.rules = [
			{
				"template_name": "Generic Recurring",
				"scope_pakd_type": "Recurring Telecom",
				"scope_service_type": "",
				"scope_branch": "",
				"components": RECURRING_TELECOM_COMPONENTS,
			},
			{
				"template_name": "P2P Recurring",
				"scope_pakd_type": "Recurring Telecom",
				"scope_service_type": "P2P",
				"scope_branch": "",
				"components": RECURRING_TELECOM_COMPONENTS,
			},
			{
				"template_name": "P2P HCM Recurring",
				"scope_pakd_type": "Recurring Telecom",
				"scope_service_type": "P2P",
				"scope_branch": "HCM",
				"components": RECURRING_TELECOM_COMPONENTS,
			},
		]

	def test_most_specific_wins_branch_service_pakd(self):
		result = resolve_rule("Recurring Telecom", "P2P", "HCM", self.rules)
		self.assertEqual(result["template_name"], "P2P HCM Recurring")

	def test_service_plus_pakd_when_no_branch_match(self):
		result = resolve_rule("Recurring Telecom", "P2P", "HN", self.rules)
		self.assertEqual(result["template_name"], "P2P Recurring")

	def test_pakd_type_only_fallback(self):
		result = resolve_rule("Recurring Telecom", "MPLS", "HN", self.rules)
		self.assertEqual(result["template_name"], "Generic Recurring")

	def test_no_match_returns_none(self):
		result = resolve_rule("One-off Sale/Project", "P2P", "HCM", self.rules)
		self.assertIsNone(result)


class TestResolveRuleChannel(unittest.TestCase):
	"""Channel-aware resolution: scope_channel filters + ranks between service and branch."""

	def setUp(self):
		self.rules = [
			{
				"template_name": "Generic Recurring",
				"scope_pakd_type": "Recurring Telecom",
				"scope_service_type": "",
				"scope_branch": "",
				"scope_channel": "",
				"components": RECURRING_TELECOM_COMPONENTS,
			},
			{
				"template_name": "Board Recurring",
				"scope_pakd_type": "Recurring Telecom",
				"scope_service_type": "",
				"scope_branch": "",
				"scope_channel": "Board",
				"components": RECURRING_TELECOM_COMPONENTS,
			},
			{
				"template_name": "Staff P2P Recurring",
				"scope_pakd_type": "Recurring Telecom",
				"scope_service_type": "P2P",
				"scope_branch": "",
				"scope_channel": "Staff",
				"components": RECURRING_TELECOM_COMPONENTS,
			},
		]

	def test_board_channel_picks_board_specific_rule(self):
		result = resolve_rule("Recurring Telecom", "MPLS", "HCM", self.rules, channel="Board")
		self.assertEqual(result["template_name"], "Board Recurring")

	def test_staff_channel_with_service_match_picks_specific_rule(self):
		result = resolve_rule("Recurring Telecom", "P2P", "HCM", self.rules, channel="Staff")
		self.assertEqual(result["template_name"], "Staff P2P Recurring")

	def test_channel_mismatch_excludes_rule(self):
		result = resolve_rule("Recurring Telecom", "MPLS", "HCM", self.rules, channel="Staff")
		self.assertEqual(result["template_name"], "Generic Recurring")

	def test_empty_channel_falls_back_to_unconstrained_rule(self):
		result = resolve_rule("Recurring Telecom", "MPLS", "HCM", self.rules)
		self.assertEqual(result["template_name"], "Generic Recurring")


class TestResolveActiveRevision(unittest.TestCase):
	"""Active revision = most recent Approved revision with effective_from ≤ period."""

	def setUp(self):
		self.revisions = [
			{
				"revision_idx": 0,
				"effective_from": datetime.date(2026, 1, 1),
				"workflow_state": "Approved",
			},
			{
				"revision_idx": 1,
				"effective_from": datetime.date(2026, 7, 1),
				"workflow_state": "Approved",
			},
			{
				"revision_idx": 2,
				"effective_from": datetime.date(2027, 1, 1),
				"workflow_state": "Draft",
			},
		]

	def test_picks_v0_before_v1_effective(self):
		result = resolve_active_revision(self.revisions, datetime.date(2026, 3, 15))
		self.assertEqual(result["revision_idx"], 0)

	def test_picks_v1_after_effective(self):
		result = resolve_active_revision(self.revisions, datetime.date(2026, 8, 1))
		self.assertEqual(result["revision_idx"], 1)

	def test_skips_draft_revision(self):
		# 2027-06 → only Approved v0 + v1; Draft v2 ignored even though effective_from ≤ period
		result = resolve_active_revision(self.revisions, datetime.date(2027, 6, 1))
		self.assertEqual(result["revision_idx"], 1)

	def test_no_approved_before_period(self):
		# Period earlier than v0 effective_from
		result = resolve_active_revision(self.revisions, datetime.date(2025, 12, 1))
		self.assertIsNone(result)

	def test_empty_revisions_returns_none(self):
		self.assertIsNone(resolve_active_revision([], datetime.date(2026, 1, 1)))


class TestComputePAKDLineMau01Legacy(unittest.TestCase):
	"""Backward compat: legacy 4-component rule (MS+AC+License+SC) still works."""

	def test_golden_values(self):
		line = {"unit_price": 13500, "add_costs_unit_price": 3000, "qty": 1}
		header = {"pakd_type": "Recurring Telecom"}

		result = compute_pakd_line(line, header, RECURRING_TELECOM_COMPONENTS)

		self.assertEqual(result["revenue_contract"], 13500)
		self.assertEqual(result["add_costs"], 2250)
		self.assertEqual(result["manager_services"], 1050)
		self.assertAlmostEqual(result["license_fee"], 297, places=2)
		self.assertEqual(result["sales_commission"], 630)
		self.assertAlmostEqual(result["total_cost"], 4227, places=2)
		self.assertAlmostEqual(result["revenue_service"], 9273, places=2)


class TestComputePAKDLineMau01BeneficiaryV02(unittest.TestCase):
	"""v0.2.0: SC + License from rule_components, MS + AC from beneficiary_specs."""

	def test_split_output(self):
		line = {"unit_price": 13500, "add_costs_unit_price": 3000, "qty": 1}
		header = {"pakd_type": "Recurring Telecom"}

		result = compute_pakd_line(
			line, header,
			RECURRING_RULE_SC_LICENSE_ONLY,
			beneficiary_specs=MAU01_BENEFICIARY_SPECS,
		)

		# Commission line side
		self.assertAlmostEqual(result["license_fee"], 297, places=2)
		self.assertEqual(result["sales_commission"], 630)

		# Beneficiary side — 2 rows
		self.assertEqual(len(result["beneficiaries"]), 2)
		by_kind = {b["kind"]: b for b in result["beneficiaries"]}
		self.assertEqual(by_kind["Add Costs"]["amount"], 2250)
		self.assertEqual(by_kind["Manager Services"]["amount"], 1050)

		# No recipient → no PIT withholding
		self.assertEqual(by_kind["Manager Services"]["pit_amount"], 0)
		self.assertEqual(by_kind["Manager Services"]["net_amount"], 1050)

		# Totals: MS+AC+SC+License = 4227, revenue_service = 9273
		self.assertAlmostEqual(result["total_cost"], 4227, places=2)
		self.assertAlmostEqual(result["revenue_service"], 9273, places=2)


class TestComputePAKDLineMau03BeneficiaryV02(unittest.TestCase):
	"""v0.2.0 Mẫu 03: MS uses contract_minus_ac_total (Excel-faithful)."""

	def test_one_off_excel_match(self):
		line = {"unit_price": 13500, "add_costs_unit_price": 3000, "qty": 1}
		header = {"pakd_type": "One-off Sale/Project"}

		oneoff_rule_sc = [
			{"component_name": "Sales Commission", "rate": 6.0, "base_formula": "contract_minus_ac_unit"},
		]

		result = compute_pakd_line(
			line, header, oneoff_rule_sc,
			beneficiary_specs=MAU03_BENEFICIARY_SPECS,
		)

		# Excel Mẫu 03 cells: F19=1125, F20=2250, F21=630
		self.assertEqual(result["license_fee"], 0)
		self.assertEqual(result["sales_commission"], 630)

		by_kind = {b["kind"]: b for b in result["beneficiaries"]}
		self.assertEqual(by_kind["Add Costs"]["amount"], 2250)
		self.assertEqual(
			by_kind["Manager Services"]["amount"], 1125,
			msg="Excel F19 = 0.1 × (13500 - 2250) = 1125 — engine v0.2.0 contract_minus_ac_total",
		)

		# Totals from Excel: F18=4005, F17=9495
		self.assertAlmostEqual(result["total_cost"], 4005, places=2)
		self.assertAlmostEqual(result["revenue_service"], 9495, places=2)


class TestBeneficiaryWithRecipientTNCN(unittest.TestCase):
	"""3-leg shape: recipient + tax_pct > 0 → PIT withholding."""

	def test_referral_with_10pct_tncn(self):
		line = {"unit_price": 100000, "add_costs_unit_price": 0, "qty": 1}
		header = {"pakd_type": "Recurring Telecom"}

		referral_spec = [{
			"kind": "Referral",
			"rate_pct": 5.0,
			"rate_base": "contract_revenue",
			"recipient_name": "Anh A",
			"recipient_tax_pct": 10.0,
		}]

		result = compute_pakd_line(line, header, [], beneficiary_specs=referral_spec)
		ref = result["beneficiaries"][0]
		self.assertEqual(ref["amount"], 5000)  # 5% × 100,000
		self.assertEqual(ref["pit_amount"], 500)  # 10% × 5,000
		self.assertEqual(ref["net_amount"], 4500)

	def test_no_recipient_no_pit(self):
		line = {"unit_price": 100000, "add_costs_unit_price": 0, "qty": 1}
		header = {"pakd_type": "Recurring Telecom"}

		ms_spec = [{
			"kind": "Manager Services",
			"rate_pct": 5.0,
			"rate_base": "contract_revenue",
			# no recipient_name → PIT skipped even if tax_pct set
			"recipient_tax_pct": 10.0,
		}]

		result = compute_pakd_line(line, header, [], beneficiary_specs=ms_spec)
		ms = result["beneficiaries"][0]
		self.assertEqual(ms["amount"], 5000)
		self.assertEqual(ms["pit_amount"], 0)
		self.assertEqual(ms["net_amount"], 5000)


class TestComputePAKDLineOneOffLegacy(unittest.TestCase):
	"""Backward compat: Mẫu 03 with v0.1.x rule (no License Fee, MS via legacy formula)."""

	def test_oneoff_no_gpvt(self):
		line = {"unit_price": 50000, "add_costs_unit_price": 10000, "qty": 2}
		header = {"pakd_type": "One-off Sale/Project"}

		result = compute_pakd_line(line, header, ONEOFF_COMPONENTS)

		# Legacy engine v0.1.x: MS = (unit-AC_unit)*qty*rate = 40000*2*0.1 = 8000
		# (contract_minus_ac_unit, NOT _total)
		self.assertEqual(result["revenue_contract"], 100000)
		self.assertEqual(result["add_costs"], 15000)
		self.assertEqual(result["manager_services"], 8000)
		self.assertEqual(result["license_fee"], 0)
		self.assertEqual(result["sales_commission"], 4800)
		self.assertEqual(result["total_cost"], 27800)
		self.assertEqual(result["revenue_service"], 72200)


class TestComputePAKDLineWithOverrides(unittest.TestCase):
	"""compute_pakd_line ``overrides`` argument — per-PAKD rate adjustment."""

	_LINE = {"unit_price": 10000, "add_costs_unit_price": 0, "qty": 1}
	_HEADER = {"pakd_type": "Recurring Telecom"}

	def test_baseline_no_overrides(self):
		result = compute_pakd_line(self._LINE, self._HEADER, RECURRING_TELECOM_COMPONENTS)
		self.assertEqual(result["sales_commission"], 600)
		self.assertEqual(result["manager_services"], 1000)

	def test_override_replaces_template(self):
		result = compute_pakd_line(
			self._LINE, self._HEADER, RECURRING_TELECOM_COMPONENTS,
			overrides={"Sales Commission": 3.0},
		)
		self.assertEqual(result["sales_commission"], 300)
		self.assertEqual(result["manager_services"], 1000)

	def test_zero_override_falls_back_to_template(self):
		result = compute_pakd_line(
			self._LINE, self._HEADER, RECURRING_TELECOM_COMPONENTS,
			overrides={"Sales Commission": 0},
		)
		self.assertEqual(result["sales_commission"], 600)

	def test_none_override_falls_back_to_template(self):
		result = compute_pakd_line(
			self._LINE, self._HEADER, RECURRING_TELECOM_COMPONENTS,
			overrides={"Sales Commission": None},
		)
		self.assertEqual(result["sales_commission"], 600)


if __name__ == "__main__":
	unittest.main()
