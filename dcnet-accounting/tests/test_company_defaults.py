"""Tests for vn_accounting.setup.company_defaults — VN company default mappings."""

import pytest

from vn_accounting.setup.company_defaults import _get_defaults_large, _get_defaults_small


class TestLargeEnterpriseDefaults:
	"""Tests for _get_defaults_large() — TT99/2025 large enterprise mapping."""

	def test_core_accounts_present(self):
		defaults = _get_defaults_large()
		required_fields = [
			"default_cash_account",
			"default_bank_account",
			"default_receivable_account",
			"default_payable_account",
			"default_income_account",
			"default_expense_account",
		]
		for field in required_fields:
			assert field in defaults, f"Missing required field: {field}"

	def test_cash_is_111(self):
		assert _get_defaults_large()["default_cash_account"] == "111"

	def test_bank_is_112(self):
		assert _get_defaults_large()["default_bank_account"] == "112"

	def test_large_has_manufacturing_depreciation(self):
		"""Large enterprise uses TK 6274 (Chi phí KH TSCĐ sản xuất)."""
		assert _get_defaults_large()["depreciation_expense_account"] == "6274"

	def test_large_has_stock_not_billed(self):
		"""Large enterprise has stock_received_but_not_billed (TK 151)."""
		assert "stock_received_but_not_billed" in _get_defaults_large()


class TestSmallEnterpriseDefaults:
	"""Tests for _get_defaults_small() — TT99/2025 small enterprise mapping."""

	def test_core_accounts_present(self):
		defaults = _get_defaults_small()
		required_fields = [
			"default_cash_account",
			"default_bank_account",
			"default_receivable_account",
			"default_payable_account",
			"default_income_account",
			"default_expense_account",
		]
		for field in required_fields:
			assert field in defaults, f"Missing required field: {field}"

	def test_small_uses_admin_depreciation(self):
		"""Small enterprise uses TK 6424 (Chi phí KH TSCĐ quản lý)."""
		assert _get_defaults_small()["depreciation_expense_account"] == "6424"

	def test_small_no_stock_not_billed(self):
		"""Small enterprise does not have stock_received_but_not_billed."""
		assert "stock_received_but_not_billed" not in _get_defaults_small()

	def test_small_no_capex_wip(self):
		"""Small enterprise does not have capital_work_in_progress_account."""
		assert "capital_work_in_progress_account" not in _get_defaults_small()


class TestLargeVsSmallDifferences:
	"""Cross-check differences between large and small enterprise defaults."""

	def test_shared_accounts_match(self):
		"""Accounts that exist in both templates should have the same numbers."""
		large = _get_defaults_large()
		small = _get_defaults_small()
		shared_fields = set(large.keys()) & set(small.keys())
		# These fields should differ
		differing = {"depreciation_expense_account"}
		for field in shared_fields - differing:
			assert large[field] == small[field], (
				f"{field}: large={large[field]} != small={small[field]}"
			)

	def test_large_has_more_fields(self):
		"""Large enterprise template has more default fields than small."""
		large = _get_defaults_large()
		small = _get_defaults_small()
		assert len(large) > len(small)
