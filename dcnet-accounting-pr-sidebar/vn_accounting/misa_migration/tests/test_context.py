"""B2 fix tests — per-request Company override via context flag."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestContextHelper(unittest.TestCase):

    def test_set_and_get_active_company(self):
        from vn_accounting.misa_migration import context
        with patch.object(context, "frappe") as mock_frappe:
            local = MagicMock()
            local.flags = MagicMock()
            local.flags.misa_migration_company = None
            mock_frappe.local = local
            mock_frappe._dict = lambda: MagicMock()
            mock_frappe.defaults.get_global_default.return_value = "FALLBACK"

            context.set_active_company("DCNET TEST")
            self.assertEqual(local.flags.misa_migration_company, "DCNET TEST")

    def test_get_falls_back_to_global_default(self):
        from vn_accounting.misa_migration import context
        with patch.object(context, "frappe") as mock_frappe:
            mock_frappe.local = MagicMock()
            # flags has no misa_migration_company attr
            del mock_frappe.local.flags.misa_migration_company
            mock_frappe.defaults.get_global_default.return_value = "DEFAULT"
            mock_frappe.db.get_value.return_value = None
            r = context.get_active_company()
            self.assertEqual(r, "DEFAULT")

    def test_get_falls_back_to_first_company_when_no_default(self):
        from vn_accounting.misa_migration import context
        with patch.object(context, "frappe") as mock_frappe:
            mock_frappe.local = MagicMock(spec=[])
            mock_frappe.defaults.get_global_default.return_value = None
            mock_frappe.db.get_value.return_value = "FirstCo"
            r = context.get_active_company()
            self.assertEqual(r, "FirstCo")

    def test_clear_resets_to_none(self):
        from vn_accounting.misa_migration import context
        with patch.object(context, "frappe") as mock_frappe:
            local = MagicMock()
            local.flags = MagicMock()
            local.flags.misa_migration_company = "X"
            mock_frappe.local = local
            context.clear_active_company()
            # After clear, the attr is set to None
            self.assertIsNone(local.flags.misa_migration_company)


if __name__ == "__main__":
    unittest.main()
