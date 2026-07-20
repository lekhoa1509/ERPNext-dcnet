from datetime import date
from decimal import Decimal

import frappe
from frappe.tests.utils import FrappeTestCase

from vn_banking.parser.normalizer import compute_dedupe_hash, parse_amount, parse_date


class TestDedupeHash(FrappeTestCase):
    def test_same_inputs_yield_same_hash(self):
        h1 = compute_dedupe_hash(date(2026, 4, 8), Decimal("12500000"), "FT123", "TT HD SI-0123")
        h2 = compute_dedupe_hash(date(2026, 4, 8), Decimal("12500000"), "FT123", "TT HD SI-0123")
        self.assertEqual(h1, h2)

    def test_different_amount_yields_different_hash(self):
        h1 = compute_dedupe_hash(date(2026, 4, 8), Decimal("12500000"), "FT123", "x")
        h2 = compute_dedupe_hash(date(2026, 4, 8), Decimal("12500001"), "FT123", "x")
        self.assertNotEqual(h1, h2)

    def test_whitespace_in_ref_normalized(self):
        h1 = compute_dedupe_hash(date(2026, 4, 8), Decimal("100"), "  FT123  ", "x")
        h2 = compute_dedupe_hash(date(2026, 4, 8), Decimal("100"), "FT123", "x")
        self.assertEqual(h1, h2)


class TestParseAmount(FrappeTestCase):
    def test_vn_format_dot_thousands(self):
        self.assertEqual(parse_amount("12.500.000", decimal_sep=",", thousands_sep="."), Decimal("12500000"))

    def test_vn_format_with_decimal(self):
        self.assertEqual(parse_amount("12.500.000,50", decimal_sep=",", thousands_sep="."), Decimal("12500000.50"))

    def test_us_format(self):
        self.assertEqual(parse_amount("12,500,000.50"), Decimal("12500000.50"))

    def test_empty_is_zero(self):
        self.assertEqual(parse_amount(""), Decimal("0"))
        self.assertEqual(parse_amount(None), Decimal("0"))


class TestParseDate(FrappeTestCase):
    def test_dmy_slash(self):
        self.assertEqual(parse_date("08/04/2026", "%d/%m/%Y"), date(2026, 4, 8))

    def test_already_date(self):
        self.assertEqual(parse_date(date(2026, 4, 8), "%d/%m/%Y"), date(2026, 4, 8))
