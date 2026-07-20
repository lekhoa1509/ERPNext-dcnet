"""Unit tests for importers/vat_extractor.py — pure VAT extraction logic.

Shared between SI (output VAT) and PI (input VAT) handlers.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers import vat_extractor


class TestExtractVatAccount(unittest.TestCase):
    def test_output_vat_33311(self):
        legs = [
            {"account": "131", "debit": 100, "credit": 0},
            {"account": "33311", "debit": 0, "credit": 100},
        ]
        self.assertEqual(vat_extractor.extract_vat_account(legs, side="output"), "33311")

    def test_output_vat_3331_generic(self):
        legs = [
            {"account": "131", "debit": 100, "credit": 0},
            {"account": "3331", "debit": 0, "credit": 100},
        ]
        self.assertEqual(vat_extractor.extract_vat_account(legs, side="output"), "3331")

    def test_input_vat_1331(self):
        # PI legs: Dr 6322 / Cr 331 / Dr 1331 / Cr 331
        legs = [
            {"account": "6322", "debit": 1000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 1000},
            {"account": "1331", "debit": 100, "credit": 0},
            {"account": "331", "debit": 0, "credit": 100},
        ]
        self.assertEqual(vat_extractor.extract_vat_account(legs, side="input"), "1331")

    def test_no_vat_returns_none(self):
        legs = [
            {"account": "6322", "debit": 1000, "credit": 0},
            {"account": "331", "debit": 0, "credit": 1000},
        ]
        self.assertIsNone(vat_extractor.extract_vat_account(legs, side="input"))
        self.assertIsNone(vat_extractor.extract_vat_account(legs, side="output"))

    def test_invalid_side(self):
        with self.assertRaises(ValueError):
            vat_extractor.extract_vat_account([], side="both")

    def test_side_specific_amount_field(self):
        # An identical-prefix Dr 33311 leg must NOT be picked for output (which wants Cr).
        legs = [
            {"account": "33311", "debit": 100, "credit": 0},  # Dr — wrong side for output
        ]
        self.assertIsNone(vat_extractor.extract_vat_account(legs, side="output"))
        # Same for Cr 1331 not being picked for input
        legs2 = [
            {"account": "1331", "debit": 0, "credit": 100},  # Cr — wrong side for input
        ]
        self.assertIsNone(vat_extractor.extract_vat_account(legs2, side="input"))


class TestComputeTotalVat(unittest.TestCase):
    def test_single_rate(self):
        lis = [
            {"tax_rate": 10.0, "tax_amount": 100},
            {"tax_rate": 10.0, "tax_amount": 200},
        ]
        self.assertEqual(vat_extractor.compute_total_vat(lis), {10.0: 300.0})

    def test_multiple_rates(self):
        lis = [
            {"tax_rate": 10.0, "tax_amount": 100},
            {"tax_rate": 8.0, "tax_amount": 80},
            {"tax_rate": 10.0, "tax_amount": 50},
        ]
        self.assertEqual(vat_extractor.compute_total_vat(lis), {10.0: 150.0, 8.0: 80.0})


class TestBuildTaxRows(unittest.TestCase):
    def test_single_rate_single_row(self):
        lis = [
            {"tax_rate": 10.0, "tax_amount": 100},
            {"tax_rate": 10.0, "tax_amount": 200},
        ]
        rows = vat_extractor.build_tax_rows(lis, vat_account="Output VAT - DC")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rate"], 10.0)
        self.assertEqual(rows[0]["account_head"], "Output VAT - DC")
        self.assertEqual(rows[0]["charge_type"], "On Net Total")
        self.assertEqual(rows[0]["included_in_print_rate"], 0)

    def test_multiple_rates_emit_one_row_each(self):
        lis = [
            {"tax_rate": 10.0, "tax_amount": 100},
            {"tax_rate": 8.0, "tax_amount": 80},
        ]
        rows = vat_extractor.build_tax_rows(lis, vat_account="Output VAT - DC")
        rates = [r["rate"] for r in rows]
        self.assertEqual(rates, [10.0, 8.0])

    def test_zero_rate_skipped_by_default(self):
        lis = [
            {"tax_rate": 0.0, "tax_amount": 0},
            {"tax_rate": 10.0, "tax_amount": 100},
        ]
        rows = vat_extractor.build_tax_rows(lis, vat_account="Output VAT - DC")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rate"], 10.0)

    def test_zero_rate_kept_when_skip_zero_false(self):
        lis = [
            {"tax_rate": 0.0, "tax_amount": 0},
        ]
        # Even with skip_zero=False, zero tax_amount means row is dropped
        rows = vat_extractor.build_tax_rows(lis, vat_account="VAT", skip_zero=False)
        self.assertEqual(rows, [])

    def test_no_vat_account_emits_empty(self):
        lis = [{"tax_rate": 10.0, "tax_amount": 100}]
        self.assertEqual(vat_extractor.build_tax_rows(lis, vat_account=None), [])
        self.assertEqual(vat_extractor.build_tax_rows(lis, vat_account=""), [])


if __name__ == "__main__":
    unittest.main()
