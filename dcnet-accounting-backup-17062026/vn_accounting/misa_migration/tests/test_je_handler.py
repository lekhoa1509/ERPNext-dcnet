"""Unit tests for pure helpers in nkc_handlers/journal_entry.py.

DB-touching code (party_type DB lookups, JE insert) is exercised via E2E
in commit 15. Here we test the leg-classification logic with mock
frappe.db.exists.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch


class TestDetectLegParty(unittest.TestCase):
    """Tests for _detect_leg_party — needs frappe.db mocked since helper
    calls frappe.db.exists to confirm party master existence.
    """

    def _detect(self, leg_account, party_code, exists_map):
        """Run _detect_leg_party with mocked frappe.db.exists.

        exists_map: dict like {('Customer', '1986'): True} — returns True
                    for the listed pairs, False otherwise.
        """
        with patch("vn_accounting.misa_migration.importers.nkc_handlers."
                   "journal_entry.frappe") as mock_frappe:
            mock_frappe.db.exists = lambda dt, name: exists_map.get((dt, name), False)
            from vn_accounting.misa_migration.importers.nkc_handlers.journal_entry \
                import _detect_leg_party
            return _detect_leg_party(leg_account, party_code)

    def test_receivable_131_with_customer_match(self):
        result = self._detect("131", "1986", {("Customer", "1986"): True})
        self.assertEqual(result, ("Customer", "1986"))

    def test_receivable_131_falls_back_to_supplier(self):
        # 131 entry with code that's only in Supplier master (refund case)
        result = self._detect("131", "VIETTEL", {("Supplier", "VIETTEL"): True})
        self.assertEqual(result, ("Supplier", "VIETTEL"))

    def test_payable_331_with_supplier_match(self):
        result = self._detect("331", "DECIX", {("Supplier", "DECIX"): True})
        self.assertEqual(result, ("Supplier", "DECIX"))

    def test_payable_3341_employee_salary(self):
        result = self._detect("3341", "NV00001", {("Employee", "NV00001"): True})
        self.assertEqual(result, ("Employee", "NV00001"))

    def test_employee_advance_141(self):
        result = self._detect("141", "NV00002", {("Employee", "NV00002"): True})
        self.assertEqual(result, ("Employee", "NV00002"))

    def test_non_party_account_returns_none(self):
        # TK 6421 = operating expense — never a party leg
        result = self._detect("6421", "WHATEVER", {})
        self.assertEqual(result, (None, None))

    def test_bank_account_not_a_party(self):
        result = self._detect("11215", "1986", {("Customer", "1986"): True})
        self.assertEqual(result, (None, None))

    def test_revenue_account_not_a_party(self):
        result = self._detect("511", "DECIX", {("Supplier", "DECIX"): True})
        self.assertEqual(result, (None, None))

    def test_party_code_missing_returns_none(self):
        # Even if account looks like party, missing party_code → no party
        result = self._detect("131", None, {})
        self.assertEqual(result, (None, None))
        result = self._detect("131", "", {})
        self.assertEqual(result, (None, None))

    def test_party_code_not_in_any_master(self):
        # 131 with code that doesn't exist anywhere → None (not a forced party)
        result = self._detect("131", "GHOST_CODE", {})
        self.assertEqual(result, (None, None))


class TestPrefixConstants(unittest.TestCase):
    def test_party_prefix_constants_well_formed(self):
        from vn_accounting.misa_migration.importers.nkc_handlers.journal_entry import (
            _PARTY_RECEIVABLE_PREFIXES,
            _PARTY_PAYABLE_PREFIXES,
            _PARTY_EMPLOYEE_PREFIXES,
        )
        # 131 in receivable, 331 in payable, 3341 in employee
        self.assertIn("131", _PARTY_RECEIVABLE_PREFIXES)
        self.assertIn("331", _PARTY_PAYABLE_PREFIXES)
        self.assertIn("3341", _PARTY_EMPLOYEE_PREFIXES)
        # No cross-contamination
        self.assertEqual(
            set(_PARTY_RECEIVABLE_PREFIXES) & set(_PARTY_PAYABLE_PREFIXES),
            set(),
        )
        self.assertEqual(
            set(_PARTY_PAYABLE_PREFIXES) & set(_PARTY_EMPLOYEE_PREFIXES),
            set(),
        )


if __name__ == "__main__":
    unittest.main()
