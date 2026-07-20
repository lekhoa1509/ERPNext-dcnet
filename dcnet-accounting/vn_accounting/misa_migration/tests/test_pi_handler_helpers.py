"""Unit tests for pure helpers in nkc_handlers/purchase_invoice.py.

DB-touching code (Supplier lookup, placeholder Item creation, PI insert)
is exercised via E2E in commit 15.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers.nkc_handlers.purchase_invoice import (
    extract_line_expense_accounts,
)


class TestExtractLineExpenseAccounts(unittest.TestCase):
    def test_2_leg_no_vat_pattern(self):
        # Real MDV20260001: Dr 6322 / Cr 331 (foreign service, KCT)
        legs = [
            {"account": "6322", "debit": 7649330, "credit": 0},
            {"account": "331", "debit": 0, "credit": 7649330},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=1)
        self.assertEqual(out, ["6322"])

    def test_4_leg_with_vat_pattern(self):
        # Real MDV20260003: Dr 6427 / Cr 331 / Dr 1331 / Cr 331
        legs = [
            {"account": "6427", "debit": 1203715, "credit": 0},
            {"account": "331", "debit": 0, "credit": 1203715},
            {"account": "1331", "debit": 96297, "credit": 0},
            {"account": "331", "debit": 0, "credit": 96297},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=1)
        # Dr 1331 is filtered out; only the expense Dr leg returned
        self.assertEqual(out, ["6427"])

    def test_8_leg_2_line_mixed_accounts(self):
        # Real MDV20260301: 2 lines, one 6323 + one 242 (deferred expense)
        legs = [
            {"account": "6323", "debit": 3000000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 3000000},
            {"account": "1331", "debit": 300000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 300000},
            {"account": "242", "debit": 15000000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 15000000},
            {"account": "1331", "debit": 1500000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 1500000},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=2)
        self.assertEqual(out, ["6323", "242"])

    def test_fixed_asset_purchase(self):
        # MH-style with TK 211 (fixed asset)
        legs = [
            {"account": "211", "debit": 50000000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 50000000},
            {"account": "1331", "debit": 5000000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 5000000},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=1)
        self.assertEqual(out, ["211"])

    def test_inventory_purchase(self):
        # PN-style: Dr 152 + Dr 1331 / Cr 331
        legs = [
            {"account": "152", "debit": 1000000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 1000000},
            {"account": "1331", "debit": 100000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 100000},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=1)
        self.assertEqual(out, ["152"])

    def test_dr_1331_excluded(self):
        # If only VAT Dr legs present, expense list is empty
        legs = [
            {"account": "1331", "debit": 100, "credit": 0},
            {"account": "331", "debit": 0, "credit": 100},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=1)
        self.assertEqual(out, [None])

    def test_padded_with_none_when_legs_short(self):
        legs = [
            {"account": "6322", "debit": 1000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 1000},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=3)
        self.assertEqual(out, ["6322", None, None])

    def test_truncated_when_legs_excess(self):
        # NKC has 3 Dr expense legs but bảng kê only has 2 lines
        legs = [
            {"account": "6322", "debit": 1000, "credit": 0},
            {"account": "6323", "debit": 2000, "credit": 0},
            {"account": "242", "debit": 3000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 6000},
        ]
        out = extract_line_expense_accounts(legs, n_line_items=2)
        self.assertEqual(out, ["6322", "6323"])


if __name__ == "__main__":
    unittest.main()
