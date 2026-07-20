"""Tests for party_type_detect — pure functions, no DB."""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.importers.party_type_detect import (
    classify_accounts, detect_for_voucher,
)


class TestPartyTypeDetect(unittest.TestCase):
    """13 cases covering all spec §6.1 priority rules + edge cases."""

    def test_only_131_is_customer(self):
        self.assertEqual(classify_accounts(["131"]), "Customer")
        self.assertEqual(classify_accounts(["131", "5111"]), "Customer")

    def test_only_331_is_supplier(self):
        self.assertEqual(classify_accounts(["331"]), "Supplier")
        self.assertEqual(classify_accounts(["331", "6322"]), "Supplier")

    def test_both_131_and_331_is_ambiguous(self):
        self.assertEqual(classify_accounts(["131", "331"]), "ambiguous")

    def test_334_or_141_is_employee(self):
        self.assertEqual(classify_accounts(["334"]), "Employee")
        self.assertEqual(classify_accounts(["141"]), "Employee")
        self.assertEqual(classify_accounts(["3341", "1411"]), "Employee")

    def test_138_no_131_is_customer(self):
        self.assertEqual(classify_accounts(["138"]), "Customer")

    def test_338_no_331_is_supplier(self):
        self.assertEqual(classify_accounts(["338"]), "Supplier")

    def test_unrelated_accounts_ambiguous(self):
        self.assertEqual(classify_accounts(["511", "632"]), "ambiguous")

    def test_empty_is_ambiguous(self):
        self.assertEqual(classify_accounts([]), "ambiguous")

    def test_subcodes_match_prefix(self):
        # 1311 is a 131 subcode, 3311 is a 331 subcode
        self.assertEqual(classify_accounts(["1311"]), "Customer")
        self.assertEqual(classify_accounts(["3311"]), "Supplier")

    def test_detect_for_voucher_filters_by_party_code(self):
        rows = [
            {"account": "131", "party_code": "A"},
            {"account": "511", "party_code": "A"},
            {"account": "331", "party_code": "B"},
            {"account": "1121", "party_code": ""},
        ]
        self.assertEqual(detect_for_voucher("A", rows), "Customer")
        self.assertEqual(detect_for_voucher("B", rows), "Supplier")
        self.assertEqual(detect_for_voucher("UNKNOWN", rows), "ambiguous")
        self.assertEqual(detect_for_voucher("", rows), "ambiguous")

    def test_handles_none_and_blank_codes(self):
        self.assertEqual(classify_accounts([None, "131", "", " "]), "Customer")


if __name__ == "__main__":
    unittest.main()
