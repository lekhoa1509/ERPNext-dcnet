"""Tests for vn_accounting.vn_accounting.report_utils — shared report utilities."""

import pytest

from vn_accounting.vn_accounting.report_utils import (
	BANK_PREFIX,
	CASH_PREFIX,
	extract_account_numbers,
)


class TestExtractAccountNumbers:
	"""Tests for extract_account_numbers()."""

	def test_single_account(self):
		result = extract_account_numbers("6421 - Chi phi nhan vien - DCNET")
		assert result == "6421"

	def test_multiple_accounts(self):
		result = extract_account_numbers(
			"6421 - Chi phi nhan vien - DCNET, 111 - Tien mat - DCNET"
		)
		assert result == "6421, 111"

	def test_empty_string(self):
		assert extract_account_numbers("") == ""

	def test_none_input(self):
		assert extract_account_numbers(None) == ""

	def test_deduplicates(self):
		result = extract_account_numbers(
			"111 - Tien mat - DCNET, 111 - Tien mat - DCNET"
		)
		assert result == "111"

	def test_whitespace_handling(self):
		result = extract_account_numbers("  6421 - Chi phi - DCNET ,  112 - Bank - DCNET  ")
		assert result == "6421, 112"

	def test_single_part_no_separator(self):
		# Edge case: account string with no " - " separator
		result = extract_account_numbers("SomeAccount")
		assert result == "SomeAccount"


class TestAccountPrefixConstants:
	"""Verify account prefix constants match TT99/2025."""

	def test_cash_prefix(self):
		assert CASH_PREFIX == "111%"

	def test_bank_prefix(self):
		assert BANK_PREFIX == "112%"

	def test_prefixes_are_sql_wildcards(self):
		"""Both prefixes must end with % for SQL LIKE queries."""
		assert CASH_PREFIX.endswith("%")
		assert BANK_PREFIX.endswith("%")
