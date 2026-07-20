"""Unit tests for CCDC Item inline accounting (Phase 3).

Pure-function tests (company=None, no DB) run under pytest:
    cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
    python -m pytest vn_accounting/tests/test_ccdc_item_inline_posting.py -v

DB-coupled submit/cancel tests require a live site and run via bench:
    bench --site dcnet.localhost run-tests --app vn_accounting \
        --module vn_accounting.tests.test_ccdc_item_inline_posting
"""
from __future__ import annotations

import unittest

from vn_accounting.utils.accounting_posting import build_default_entries


class TestCCDCItemBuildEntries(unittest.TestCase):
    """Pure-function tests — no DB, company=None returns raw account-number strings."""

    def test_two_rows_no_vat(self):
        """Purchase without VAT → 2 rows: Dr 153 / Cr 331, then Dr 242 / Cr 153 (VAS textbook)."""
        rows = build_default_entries(
            "CCDC Item Purchase", None, 5_000_000, has_vat=False, vat_rate=10, company=None
        )
        self.assertEqual(len(rows), 2)
        # Row 1: receive into warehouse — supplier payable
        self.assertEqual(rows[0]["account_debit"], "153")
        self.assertEqual(rows[0]["account_credit"], "331")
        self.assertEqual(float(rows[0]["amount"]), 5_000_000)
        self.assertEqual(rows[0]["is_vat"], 0)
        # Row 2: issue for amortization
        self.assertEqual(rows[1]["account_debit"], "242")
        self.assertEqual(rows[1]["account_credit"], "153")
        self.assertEqual(float(rows[1]["amount"]), 5_000_000)
        self.assertEqual(rows[1]["is_vat"], 0)

    def test_three_rows_with_vat_10pct(self):
        """Purchase with 10% VAT → 3 rows: 153/331, 242/153, then 1331/331 (VAT against payable)."""
        rows = build_default_entries(
            "CCDC Item Purchase", None, 10_000_000, has_vat=True, vat_rate=10, company=None
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["account_debit"], "153")
        self.assertEqual(rows[0]["account_credit"], "331")
        self.assertEqual(rows[1]["account_debit"], "242")
        self.assertEqual(rows[1]["account_credit"], "153")
        vat = rows[2]
        self.assertEqual(vat["account_debit"], "1331")
        self.assertEqual(vat["account_credit"], "331")
        self.assertEqual(float(vat["amount"]), 1_000_000)  # 10%
        self.assertEqual(vat["is_vat"], 1)

    def test_vat_rounding(self):
        """VAT amount rounds to whole VND."""
        rows = build_default_entries(
            "CCDC Item Purchase", None, 3_000_000, has_vat=True, vat_rate=10, company=None
        )
        vat = rows[2]  # VAT row is now 3rd
        self.assertEqual(float(vat["amount"]), 300_000)

    def test_zero_cost_no_vat_row(self):
        """Zero cost with VAT → cost rows still emitted with amt 0, VAT row skipped (amt 0)."""
        rows = build_default_entries(
            "CCDC Item Purchase", None, 0, has_vat=True, vat_rate=10, company=None
        )
        # Two cost rows (153/331, 242/153) always present even at amt 0;
        # VAT row guarded by `amt > 0`, so skipped.
        self.assertEqual(len(rows), 2)

    def test_no_vat_row_when_has_vat_false(self):
        """has_vat=False → only 2 cost rows (153/331, 242/153), no VAT row."""
        rows = build_default_entries(
            "CCDC Item Purchase", None, 8_000_000, has_vat=False, vat_rate=10, company=None
        )
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["is_vat"] == 0 for r in rows))


if __name__ == "__main__":
    unittest.main()
