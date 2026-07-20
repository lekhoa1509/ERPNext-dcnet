"""Tier 1.5 — _party_cache helpers contract:

- Unwarmed cache (None state) falls back to frappe.db.exists so that
  handler unit-tests that don't bother calling warm_party_cache still work.
- Warmed cache (set state) does pure set-lookup — never hits DB.
- reset_party_cache returns the cache to None state for both branches.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestPartyCacheFallback(unittest.TestCase):
    def setUp(self):
        # Force-reset before each test so state from a previous test
        # never leaks.
        from vn_accounting.misa_migration.importers.nkc_handlers import (
            _party_cache,
        )
        _party_cache.reset_party_cache()
        self.pc = _party_cache

    def tearDown(self):
        self.pc.reset_party_cache()

    def test_unwarmed_falls_back_to_db(self):
        """When the cache is None (never warmed), is_customer hits DB."""
        mock_frappe = MagicMock(name="frappe")
        mock_frappe.db.exists.return_value = True

        with patch.object(self.pc, "frappe", mock_frappe):
            self.assertTrue(self.pc.is_customer("FOO"))
            self.assertTrue(self.pc.is_supplier("BAR"))
            self.assertTrue(self.pc.is_employee("BAZ"))

        # Three DB round-trips
        self.assertEqual(mock_frappe.db.exists.call_count, 3)

    def test_warmed_skips_db(self):
        """When warmed, set-lookup returns; DB is never touched."""
        # Manually populate the module sets to simulate a successful warm.
        self.pc._CUSTOMERS = {"CUS-A", "CUS-B"}
        self.pc._SUPPLIERS = {"SUP-A"}
        self.pc._EMPLOYEES = set()
        self.pc._ACCOUNT_LEAVES = {"111 - X - DCT"}
        self.pc._WARM_COMPANY = "DCNET TEST"

        mock_frappe = MagicMock(name="frappe")
        mock_frappe.db.exists.return_value = "MUST_NEVER_BE_CALLED"

        with patch.object(self.pc, "frappe", mock_frappe):
            self.assertTrue(self.pc.is_customer("CUS-A"))
            self.assertFalse(self.pc.is_customer("CUS-Z"))
            self.assertTrue(self.pc.is_supplier("SUP-A"))
            self.assertFalse(self.pc.is_employee("ANYTHING"))

        # Zero DB round-trips — pure set-lookup
        self.assertEqual(mock_frappe.db.exists.call_count, 0)

    def test_empty_or_none_code_returns_false(self):
        # Defensive: empty / None must short-circuit to False without
        # any DB or set lookup.
        self.assertFalse(self.pc.is_customer(""))
        self.assertFalse(self.pc.is_customer(None))
        self.assertFalse(self.pc.is_supplier(""))
        self.assertFalse(self.pc.is_employee(""))
        self.assertFalse(self.pc.is_account_leaf(""))

    def test_account_leaf_company_mismatch_falls_back(self):
        """Account cache is company-scoped. If queried for a DIFFERENT
        company than the one warmed, fall back to DB (don't trust stale
        cache)."""
        self.pc._ACCOUNT_LEAVES = {"111 - DCNET"}
        self.pc._WARM_COMPANY = "DCNET TEST"

        mock_frappe = MagicMock(name="frappe")
        mock_frappe.db.exists.return_value = True

        with patch.object(self.pc, "frappe", mock_frappe):
            # Same company → hits cache, no DB
            self.assertTrue(self.pc.is_account_leaf("111 - DCNET", "DCNET TEST"))
            self.assertEqual(mock_frappe.db.exists.call_count, 0)
            # Different company → falls back to DB
            self.assertTrue(self.pc.is_account_leaf("111 - OTHER", "OTHER CO"))
            self.assertEqual(mock_frappe.db.exists.call_count, 1)

    def test_reset_party_cache_returns_to_unwarmed(self):
        self.pc._CUSTOMERS = {"X"}
        self.pc._SUPPLIERS = {"Y"}
        self.pc._EMPLOYEES = {"Z"}
        self.pc._ACCOUNT_LEAVES = {"A"}
        self.pc._WARM_COMPANY = "C"

        self.pc.reset_party_cache()

        state = self.pc._state_for_test()
        self.assertEqual(state, {
            "customers": None, "suppliers": None, "employees": None,
            "account_leaves": None, "warm_company": None,
        })


if __name__ == "__main__":
    unittest.main()
