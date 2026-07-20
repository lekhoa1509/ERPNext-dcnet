"""Unit tests for B3+B4 company defaults helper."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestFindLeaf(unittest.TestCase):

    def test_returns_leaf_name(self):
        from vn_accounting.misa_migration.setup import company_defaults
        with patch.object(company_defaults, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "131 - AR - DCT"
            self.assertEqual(
                company_defaults._find_leaf("DCT", "131"),
                "131 - AR - DCT",
            )

    def test_returns_none_when_no_leaf(self):
        from vn_accounting.misa_migration.setup import company_defaults
        with patch.object(company_defaults, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = None
            self.assertIsNone(company_defaults._find_leaf("DCT", "999"))


class TestEnsureCompanyDefaults(unittest.TestCase):

    def test_sets_each_field_when_unset(self):
        from vn_accounting.misa_migration.setup import company_defaults
        with patch.object(company_defaults, "frappe") as mock_frappe:
            # Schema has all fields
            meta = MagicMock()
            meta.fields = [
                type("F", (), {"fieldname": fn})()
                for fn in ["default_receivable_account", "default_payable_account",
                           "stock_received_but_not_billed", "stock_adjustment_account",
                           "cost_center"]
            ]
            mock_frappe.get_meta.return_value = meta
            # All currently NULL
            mock_frappe.db.get_value.side_effect = lambda dt, name, fn=None, **kw: (
                None  # for Company.<field>
                if dt == "Company" and fn in ("default_receivable_account",
                                              "default_payable_account",
                                              "stock_received_but_not_billed",
                                              "stock_adjustment_account",
                                              "cost_center")
                else "RESOLVED - DCT"
            )
            r = company_defaults.ensure_company_defaults_for_misa("DCT")
            # Should set all 5 fields
            self.assertEqual(len(r), 5)
            self.assertEqual(r["default_receivable_account"], "RESOLVED - DCT")
            self.assertEqual(r["stock_received_but_not_billed"], "RESOLVED - DCT")
            # set_value called multiple times
            self.assertGreaterEqual(mock_frappe.db.set_value.call_count, 5)

    def test_preserves_operator_config(self):
        """Already-set fields are NOT overwritten."""
        from vn_accounting.misa_migration.setup import company_defaults
        with patch.object(company_defaults, "frappe") as mock_frappe:
            meta = MagicMock()
            meta.fields = [type("F", (), {"fieldname": "default_receivable_account"})()]
            mock_frappe.get_meta.return_value = meta
            mock_frappe.db.get_value.return_value = "EXISTING - DCT"
            r = company_defaults.ensure_company_defaults_for_misa("DCT")
            self.assertEqual(r, {})
            mock_frappe.db.set_value.assert_not_called()

    def test_skips_missing_schema_fields(self):
        """v16 Company schema may not have all fields — skip silently."""
        from vn_accounting.misa_migration.setup import company_defaults
        with patch.object(company_defaults, "frappe") as mock_frappe:
            meta = MagicMock()
            # Only one field present
            meta.fields = [type("F", (), {"fieldname": "default_receivable_account"})()]
            mock_frappe.get_meta.return_value = meta

            # Company.get_value(company, fieldname) returns None (unset).
            # Account leaf lookup returns "131 - AR - DCT".
            def fake_get_value(dt, name, fn=None, **kw):
                # Account lookup: filters dict in `name` param
                if dt == "Account" and isinstance(name, dict):
                    return "131 - AR - DCT"
                # Company.<field> lookup
                return None
            mock_frappe.db.get_value.side_effect = fake_get_value

            r = company_defaults.ensure_company_defaults_for_misa("DCT")
            # Only the present field gets set
            self.assertIn("default_receivable_account", r)
            self.assertNotIn("stock_received_but_not_billed", r)


class TestEnsurePartyAccounts(unittest.TestCase):

    def test_sets_receivable_on_missing_customers(self):
        from vn_accounting.misa_migration.setup import company_defaults
        captured_calls = []
        class MockDoc:
            def __init__(self, dt, name):
                self.dt, self.name = dt, name
                self.accounts = []
                self.flags = type("F", (), {"ignore_permissions": False})()
            def append(self, fld, val):
                self.accounts.append(val)
                captured_calls.append(("append", self.name, val))
            def save(self):
                captured_calls.append(("save", self.name))

        with patch.object(company_defaults, "frappe") as mock_frappe:
            mock_frappe.db.get_value.side_effect = lambda dt, name, fn=None: \
                "131 - AR - DCT" if fn == "default_receivable_account" else None
            mock_frappe.db.sql.return_value = [
                {"name": "C001"}, {"name": "C002"},
            ]
            mock_frappe.get_doc = lambda dt, name: MockDoc(dt, name)
            r = company_defaults.ensure_party_accounts_for_misa("DCT")
            self.assertEqual(r["customer_updated"], 2)
            # Each customer got an append("accounts", {company, account})
            append_calls = [c for c in captured_calls if c[0] == "append"]
            self.assertEqual(len(append_calls), 2)
            self.assertEqual(append_calls[0][2]["account"], "131 - AR - DCT")
            self.assertEqual(append_calls[0][2]["company"], "DCT")


if __name__ == "__main__":
    unittest.main()
