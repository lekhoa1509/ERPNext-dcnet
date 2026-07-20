"""Unit tests for UNC multi-leg classification (PE handler).

Tests the _split_unc_legs pure helper that buckets legs into party / fee /
vat / paid groups before deductions[] construction.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers.nkc_handlers.payment_entry import (
    _split_unc_legs,
)


class TestSplitUncLegs(unittest.TestCase):
    def test_simple_2_leg_unc(self):
        # Real UNC20260002: Dr 331 / Cr 11215 (party=GIGANET supplier)
        legs = [
            {"account": "331", "debit": 8856000, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 8856000},
        ]
        buckets = _split_unc_legs(legs)
        self.assertEqual(len(buckets["party_dr"]), 1)
        self.assertEqual(buckets["party_dr"][0]["account"], "331")
        self.assertEqual(len(buckets["paid_cr"]), 1)
        self.assertEqual(buckets["paid_cr"][0]["account"], "11215")
        self.assertEqual(len(buckets["fee_dr"]), 0)
        self.assertEqual(len(buckets["vat_dr"]), 0)

    def test_4_leg_bank_fee_with_vat(self):
        # Real UNC20260001: Dr 6427 + Dr 1331 / Cr 11215×2 (VIB bank fee)
        legs = [
            {"account": "6427", "debit": 279750, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 279750},
            {"account": "1331", "debit": 27975, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 27975},
        ]
        buckets = _split_unc_legs(legs)
        # No party Dr — pure fee+VAT case
        self.assertEqual(len(buckets["party_dr"]), 0)
        self.assertEqual(len(buckets["fee_dr"]), 1)
        self.assertEqual(buckets["fee_dr"][0]["account"], "6427")
        self.assertEqual(len(buckets["vat_dr"]), 1)
        self.assertEqual(buckets["vat_dr"][0]["account"], "1331")
        self.assertEqual(len(buckets["paid_cr"]), 2)

    def test_6_leg_pure_interest(self):
        # Real UNC20260096: Dr 635×3 / Cr 11218×3 (VPBANK interest)
        legs = [
            {"account": "635", "debit": 2017, "credit": 0},
            {"account": "11218", "debit": 0, "credit": 2017},
            {"account": "635", "debit": 9955, "credit": 0},
            {"account": "11218", "debit": 0, "credit": 9955},
            {"account": "635", "debit": 3681385, "credit": 0},
            {"account": "11218", "debit": 0, "credit": 3681385},
        ]
        buckets = _split_unc_legs(legs)
        self.assertEqual(len(buckets["party_dr"]), 0)
        self.assertEqual(len(buckets["fee_dr"]), 3)
        for fee in buckets["fee_dr"]:
            self.assertEqual(fee["account"], "635")
        self.assertEqual(len(buckets["paid_cr"]), 3)

    def test_multi_leg_with_party_and_fees(self):
        # Hypothetical: pay supplier 100k for service + 5k late fee + 0.5k VAT on fee
        # Dr 331 100000 / Cr 11215 100000
        # Dr 6427 5000  / Cr 11215 5000
        # Dr 1331 500   / Cr 11215 500
        legs = [
            {"account": "331", "debit": 100000, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 100000},
            {"account": "6427", "debit": 5000, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 5000},
            {"account": "1331", "debit": 500, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 500},
        ]
        buckets = _split_unc_legs(legs)
        self.assertEqual(len(buckets["party_dr"]), 1)
        self.assertEqual(buckets["party_dr"][0]["debit"], 100000)
        self.assertEqual(len(buckets["fee_dr"]), 1)
        self.assertEqual(buckets["fee_dr"][0]["account"], "6427")
        self.assertEqual(len(buckets["vat_dr"]), 1)
        self.assertEqual(buckets["vat_dr"][0]["account"], "1331")

    def test_employee_advance_treated_as_party(self):
        # PC/UNC paying employee advance: Dr 141 / Cr 11215
        legs = [
            {"account": "141", "debit": 5000000, "credit": 0},
            {"account": "11215", "debit": 0, "credit": 5000000},
        ]
        buckets = _split_unc_legs(legs)
        self.assertEqual(len(buckets["party_dr"]), 1)
        self.assertEqual(buckets["party_dr"][0]["account"], "141")

    def test_other_bucket_picks_up_non_bank_cr(self):
        # Edge: Cr to cash (1111) instead of bank — sits in 'other' for UNC
        # (real UNC always uses bank, but defensive)
        legs = [
            {"account": "331", "debit": 100, "credit": 0},
            {"account": "1111", "debit": 0, "credit": 100},
        ]
        buckets = _split_unc_legs(legs)
        self.assertEqual(len(buckets["paid_cr"]), 0)
        self.assertEqual(len(buckets["other"]), 1)
        self.assertEqual(buckets["other"][0]["account"], "1111")


if __name__ == "__main__":
    unittest.main()
