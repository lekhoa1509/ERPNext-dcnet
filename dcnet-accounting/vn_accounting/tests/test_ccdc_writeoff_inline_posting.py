"""Unit tests for CCDC Writeoff inline accounting (Phase 3).

Pure-function tests (company=None, no DB) run under pytest:
    cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
    python -m pytest vn_accounting/tests/test_ccdc_writeoff_inline_posting.py -v

DB-coupled submit/cancel tests run via bench:
    bench --site dcnet.localhost run-tests --app vn_accounting \
        --module vn_accounting.tests.test_ccdc_writeoff_inline_posting
"""
from __future__ import annotations

import unittest

from vn_accounting.utils.accounting_posting import build_default_entries


class TestCCDCWriteoffBuildEntries(unittest.TestCase):
    """Pure-function tests — no DB, company=None returns raw account-number strings."""

    def test_single_row_rem_242_only(self):
        """Writeoff with only rem_242 → 1 row D 6423/C 242."""
        rows = build_default_entries(
            "CCDC Writeoff", None, 0, False, 10, None,
            remaining_242=4_000_000,
            remaining_153=0,
            compensation_amount=0,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["account_debit"], "6423")
        self.assertEqual(rows[0]["account_credit"], "242")
        self.assertEqual(float(rows[0]["amount"]), 4_000_000)

    def test_two_rows_rem_242_and_rem_153(self):
        """Writeoff with rem_242 + rem_153 → 2 rows."""
        rows = build_default_entries(
            "CCDC Writeoff", None, 0, False, 10, None,
            remaining_242=3_000_000,
            remaining_153=1_000_000,
            compensation_amount=0,
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["account_debit"], "6423")
        self.assertEqual(rows[0]["account_credit"], "242")
        self.assertEqual(rows[1]["account_debit"], "632")
        self.assertEqual(rows[1]["account_credit"], "153")

    def test_three_rows_with_compensation(self):
        """Writeoff with all three amounts → 3 rows."""
        rows = build_default_entries(
            "CCDC Writeoff", None, 0, False, 10, None,
            remaining_242=3_000_000,
            remaining_153=1_000_000,
            compensation_amount=500_000,
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2]["account_debit"], "1388")
        self.assertEqual(rows[2]["account_credit"], "711")
        self.assertEqual(float(rows[2]["amount"]), 500_000)

    def test_empty_when_all_zero(self):
        """All amounts zero → empty list."""
        rows = build_default_entries(
            "CCDC Writeoff", None, 0, False, 10, None,
            remaining_242=0,
            remaining_153=0,
            compensation_amount=0,
        )
        self.assertEqual(len(rows), 0)

    def test_rem_153_only(self):
        """Only rem_153 non-zero → 1 row D 632/C 153."""
        rows = build_default_entries(
            "CCDC Writeoff", None, 0, False, 10, None,
            remaining_242=0,
            remaining_153=2_000_000,
            compensation_amount=0,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["account_debit"], "632")
        self.assertEqual(rows[0]["account_credit"], "153")
        self.assertEqual(float(rows[0]["amount"]), 2_000_000)

    def test_compensation_only(self):
        """Only compensation non-zero → 1 row D 1388/C 711."""
        rows = build_default_entries(
            "CCDC Writeoff", None, 0, False, 10, None,
            remaining_242=0,
            remaining_153=0,
            compensation_amount=500_000,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["account_debit"], "1388")
        self.assertEqual(rows[0]["account_credit"], "711")


if __name__ == "__main__":
    unittest.main()
