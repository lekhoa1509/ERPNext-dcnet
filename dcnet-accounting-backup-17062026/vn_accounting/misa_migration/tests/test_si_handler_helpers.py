"""Unit tests for pure helpers in nkc_handlers/sales_invoice.py.

DB-touching code (placeholder Item creation, Customer lookup, actual SI
insert) is exercised via E2E in commit 15. Here we test only the
fixture-friendly subroutines.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    _group_line_items_by_tax_rate,
    extract_line_income_accounts,
    extract_tax_account,
)


class TestExtractLineIncomeAccounts(unittest.TestCase):
    def test_single_line_4_leg_pattern(self):
        # Real BH20260001 pattern: 4 legs (Dr 131 net, Cr 3387 net, Dr 131 VAT, Cr 33311 VAT)
        # NB: TK 3387 is "doanh thu chưa thực hiện" (deferred revenue) — sometimes used
        # in place of 511 for prepaid services. Caller treats it as revenue-like.
        # But we test with 511X to lock the prefix-based detection.
        legs = [
            {"account": "131", "debit": 1336364, "credit": 0},
            {"account": "5117", "debit": 0, "credit": 1336364},
            {"account": "131", "debit": 133636, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 133636},
        ]
        out = extract_line_income_accounts(legs, n_line_items=1)
        self.assertEqual(out, ["5117"])

    def test_multi_line_8_leg_pattern(self):
        # Real BH20260005 pattern: 2 invoice lines × 4 legs each
        legs = [
            {"account": "131", "debit": 7985000, "credit": 0},
            {"account": "51134", "debit": 0, "credit": 7985000},
            {"account": "131", "debit": 798500, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 798500},
            {"account": "131", "debit": 15300000, "credit": 0},
            {"account": "51134", "debit": 0, "credit": 15300000},
            {"account": "131", "debit": 1530000, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 1530000},
        ]
        out = extract_line_income_accounts(legs, n_line_items=2)
        self.assertEqual(out, ["51134", "51134"])

    def test_multi_line_mixed_accounts(self):
        # Real BH20260174 pattern: 5 lines, mix of 51134 and 51136
        legs = [
            # Line 1: 51136 (FTTH)
            {"account": "131", "debit": 1000000, "credit": 0},
            {"account": "51136", "debit": 0, "credit": 1000000},
            {"account": "131", "debit": 100000, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 100000},
            # Line 2: 51136
            {"account": "131", "debit": 1000000, "credit": 0},
            {"account": "51136", "debit": 0, "credit": 1000000},
            {"account": "131", "debit": 100000, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 100000},
            # Line 3: 51134 (MPLS/Metronet)
            {"account": "131", "debit": 2200000, "credit": 0},
            {"account": "51134", "debit": 0, "credit": 2200000},
            {"account": "131", "debit": 220000, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 220000},
        ]
        out = extract_line_income_accounts(legs, n_line_items=3)
        self.assertEqual(out, ["51136", "51136", "51134"])

    def test_no_revenue_leg_returns_none(self):
        # Pathological: only Dr 131 + Cr 131 (no revenue leg at all)
        legs = [
            {"account": "131", "debit": 100, "credit": 0},
            {"account": "131", "debit": 0, "credit": 100},
        ]
        out = extract_line_income_accounts(legs, n_line_items=1)
        self.assertEqual(out, [None])

    def test_empty_legs(self):
        self.assertEqual(extract_line_income_accounts([], n_line_items=1), [None])

    def test_521_discount_account_also_counted_as_revenue(self):
        # TK 521 = Sales Returns/Discounts — treated as revenue-like for income_account
        legs = [
            {"account": "131", "debit": 1000, "credit": 0},
            {"account": "521", "debit": 0, "credit": 1000},
        ]
        out = extract_line_income_accounts(legs, n_line_items=1)
        self.assertEqual(out, ["521"])


class TestExtractTaxAccount(unittest.TestCase):
    def test_finds_33311(self):
        legs = [
            {"account": "131", "debit": 1000, "credit": 0},
            {"account": "511", "debit": 0, "credit": 1000},
            {"account": "131", "debit": 100, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 100},
        ]
        self.assertEqual(extract_tax_account(legs), "33311")

    def test_finds_3331_generic(self):
        legs = [
            {"account": "131", "debit": 100, "credit": 0},
            {"account": "3331", "debit": 0, "credit": 100},
        ]
        self.assertEqual(extract_tax_account(legs), "3331")

    def test_no_vat_leg_returns_none(self):
        legs = [
            {"account": "131", "debit": 1000, "credit": 0},
            {"account": "511", "debit": 0, "credit": 1000},
        ]
        self.assertIsNone(extract_tax_account(legs))

    def test_dr_3331_leg_not_picked(self):
        # Output VAT must be a CREDIT leg; an input-VAT Dr 1331 nearby shouldn't match
        legs = [
            {"account": "1331", "debit": 100, "credit": 0},  # input VAT
            {"account": "33311", "debit": 0, "credit": 100},
        ]
        self.assertEqual(extract_tax_account(legs), "33311")


class TestGroupByTaxRate(unittest.TestCase):
    def test_single_rate(self):
        lis = [
            {"tax_rate": 10.0, "tax_amount": 100},
            {"tax_rate": 10.0, "tax_amount": 200},
        ]
        groups = _group_line_items_by_tax_rate(lis)
        self.assertEqual(list(groups.keys()), [10.0])
        self.assertEqual(len(groups[10.0]), 2)

    def test_multiple_rates_preserves_first_seen_order(self):
        lis = [
            {"tax_rate": 10.0},
            {"tax_rate": 8.0},
            {"tax_rate": 10.0},
            {"tax_rate": 0.0},
            {"tax_rate": 8.0},
        ]
        groups = _group_line_items_by_tax_rate(lis)
        self.assertEqual(list(groups.keys()), [10.0, 8.0, 0.0])
        self.assertEqual(len(groups[10.0]), 2)
        self.assertEqual(len(groups[8.0]), 2)
        self.assertEqual(len(groups[0.0]), 1)


if __name__ == "__main__":
    unittest.main()
