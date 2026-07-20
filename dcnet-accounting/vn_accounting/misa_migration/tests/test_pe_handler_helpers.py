"""Unit tests for pure helpers in nkc_handlers/payment_entry.py.

DB-touching code (party_type lookup, account mapping, PE insert) is
exercised via E2E in commit 15.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers.nkc_handlers.payment_entry import (
    _BANK_PREFIXES,
    _CASH_PREFIXES,
    _EMPLOYEE_ADVANCE_PREFIXES,
    _PAYABLE_PREFIXES,
    _RECEIVABLE_PREFIXES,
    _find_leg_by_prefix,
)


class TestFindLegByPrefix(unittest.TestCase):
    def test_finds_dr_bank_leg(self):
        # Real BC20260001: Dr 11215 / Cr 131
        legs = [
            {"account": "11215", "debit": 209000, "credit": 0},
            {"account": "131", "debit": 0, "credit": 209000},
        ]
        leg = _find_leg_by_prefix(legs, _BANK_PREFIXES, "debit")
        self.assertIsNotNone(leg)
        self.assertEqual(leg["account"], "11215")
        self.assertEqual(leg["debit"], 209000)

    def test_finds_cr_receivable_leg(self):
        legs = [
            {"account": "11215", "debit": 209000, "credit": 0},
            {"account": "131", "debit": 0, "credit": 209000},
        ]
        leg = _find_leg_by_prefix(legs, _RECEIVABLE_PREFIXES, "credit")
        self.assertEqual(leg["account"], "131")

    def test_pc_dr_payable_cr_cash(self):
        # Real PC20260001: Dr 331 / Cr 1111
        legs = [
            {"account": "331", "debit": 2500000, "credit": 0},
            {"account": "1111", "debit": 0, "credit": 2500000},
        ]
        dr_leg = _find_leg_by_prefix(legs, _PAYABLE_PREFIXES, "debit")
        cr_leg = _find_leg_by_prefix(legs, _CASH_PREFIXES, "credit")
        self.assertEqual(dr_leg["account"], "331")
        self.assertEqual(cr_leg["account"], "1111")

    def test_unc_simple_dr_payable_cr_bank(self):
        # Real UNC20260002: Dr 331 / Cr 11215
        legs = [
            {"account": "331", "debit": 8856000, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 8856000},
        ]
        dr_leg = _find_leg_by_prefix(legs, _PAYABLE_PREFIXES, "debit")
        cr_leg = _find_leg_by_prefix(legs, _BANK_PREFIXES, "credit")
        self.assertEqual(dr_leg["account"], "331")
        self.assertEqual(cr_leg["account"], "11215")

    def test_no_match_returns_none(self):
        legs = [
            {"account": "511", "debit": 0, "credit": 1000},
            {"account": "131", "debit": 1000, "credit": 0},
        ]
        # Looking for Cr 11215 (bank) — not present
        self.assertIsNone(_find_leg_by_prefix(legs, _BANK_PREFIXES, "credit"))

    def test_zero_amount_filtered(self):
        # Bank account exists but zero amount on requested side
        legs = [
            {"account": "11215", "debit": 0, "credit": 0},
            {"account": "131", "debit": 0, "credit": 100},
        ]
        self.assertIsNone(_find_leg_by_prefix(legs, _BANK_PREFIXES, "debit"))

    def test_employee_advance_prefix(self):
        # PC paying employee advance (Dr 141 / Cr 1111)
        legs = [
            {"account": "141", "debit": 5000000, "credit": 0},
            {"account": "1111", "debit": 0, "credit": 5000000},
        ]
        leg = _find_leg_by_prefix(legs, _EMPLOYEE_ADVANCE_PREFIXES, "debit")
        self.assertEqual(leg["account"], "141")


class TestPrefixConstants(unittest.TestCase):
    def test_bank_prefixes_include_subaccounts(self):
        self.assertIn("11215", _BANK_PREFIXES)
        self.assertIn("11218", _BANK_PREFIXES)
        self.assertIn("1121", _BANK_PREFIXES)

    def test_cash_prefixes_include_1111(self):
        self.assertIn("1111", _CASH_PREFIXES)
        self.assertIn("111", _CASH_PREFIXES)

    def test_receivable_payable_distinct(self):
        # No overlap between 131 (Receivable) and 331 (Payable)
        self.assertEqual(set(_RECEIVABLE_PREFIXES) & set(_PAYABLE_PREFIXES), set())


if __name__ == "__main__":
    unittest.main()
