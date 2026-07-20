"""Unit tests for COA leaf bootstrap helper."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestEnsureMisaLeaves(unittest.TestCase):

    def test_returns_skipped_no_parent_when_parent_missing(self):
        from vn_accounting.misa_migration.setup import coa_leaves
        with patch.object(coa_leaves, "frappe") as mock_frappe:
            mock_frappe.db.exists.side_effect = (
                lambda dt, *a, **k: dt == "Company"
            )
            mock_frappe.db.get_value.return_value = None  # no parent found
            # Use a single-entry leaf map for isolation
            r = coa_leaves.ensure_misa_leaves_for_company(
                "DCT", extra_leaves={"999": [("9991", "Test leaf")]}
            )
            self.assertIn("9991", r["skipped_no_parent"])

    def test_skip_existing_leaves(self):
        from vn_accounting.misa_migration.setup import coa_leaves
        with patch.object(coa_leaves, "frappe") as mock_frappe, \
             patch.object(coa_leaves, "_find_parent_account",
                          return_value="111 - Cash"):
            # Company exists; leaf 1111 already exists
            mock_frappe.db.exists.side_effect = (
                lambda dt, filters=None, *a, **k:
                    True if dt == "Company"
                    else (filters or {}).get("account_number") == "1111"
            )
            # Limit to a single mapping for the test
            with patch.dict(coa_leaves.MISA_STANDARD_LEAVES,
                            {"111": [("1111", "Tiền mặt VND")]}, clear=True):
                r = coa_leaves.ensure_misa_leaves_for_company("DCT")
                self.assertIn("1111", r["skipped_existing"])
                self.assertEqual(len(r["created"]), 0)

    def test_create_new_leaf_under_existing_parent(self):
        from vn_accounting.misa_migration.setup import coa_leaves
        captured = {}

        class FakeParent:
            root_type = "Asset"
            report_type = "Balance Sheet"
            account_type = "Bank"
            account_currency = "VND"
            is_group = 1  # already a group, no promotion needed
            flags = type("F", (), {"ignore_permissions": False, "ignore_validate": False})()
            def save(self): pass

        class FakeLeaf:
            def __init__(self, p): self.payload = p
            flags = type("F", (), {"ignore_permissions": False})()
            def insert(self):
                captured["payload"] = self.payload
                self.name = self.payload["account_number"] + " - X"

        with patch.object(coa_leaves, "frappe") as mock_frappe:
            mock_frappe.db.exists.side_effect = (
                lambda dt, *a, **k: dt == "Company"
            )
            mock_frappe.db.get_value.return_value = "112 - Bank"
            mock_frappe.get_doc.side_effect = (
                lambda x: FakeParent() if (isinstance(x, str) or (isinstance(x, dict)
                            and x.get("doctype") != "Account")
                            or "name" in str(x) and "Account" in str(x))
                else FakeLeaf(x)
            )
            # Reset get_doc with explicit branching
            def gd(arg, *a, **k):
                if isinstance(arg, str):
                    return FakeParent()
                if isinstance(arg, dict) and arg.get("doctype") == "Account":
                    return FakeLeaf(arg)
                return FakeParent()
            mock_frappe.get_doc.side_effect = gd

            with patch.dict(coa_leaves.MISA_STANDARD_LEAVES,
                            {"112": [("1121", "Tiền gửi VND")]}, clear=True):
                r = coa_leaves.ensure_misa_leaves_for_company("DCT")
                self.assertEqual(len(r["created"]), 1)
                self.assertEqual(r["created"][0], "1121 - X")
                # Verify leaf inherited parent's metadata
                pl = captured["payload"]
                self.assertEqual(pl["account_number"], "1121")
                self.assertEqual(pl["account_name"], "Tiền gửi VND")
                self.assertEqual(pl["root_type"], "Asset")
                self.assertEqual(pl["account_type"], "Bank")
                self.assertEqual(pl["account_currency"], "VND")
                self.assertEqual(pl["is_group"], 0)

    def test_non_existent_company_returns_error(self):
        from vn_accounting.misa_migration.setup import coa_leaves
        with patch.object(coa_leaves, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False
            r = coa_leaves.ensure_misa_leaves_for_company("Ghost Co")
            self.assertEqual(len(r["errors"]), 1)
            self.assertIn("not found", r["errors"][0]["error"])

    def test_promotes_leaf_parent_to_group(self):
        """Parent currently is_group=0 must auto-promote to hold new children."""
        from vn_accounting.misa_migration.setup import coa_leaves
        promote_called = {"value": False}

        class FakeParent:
            root_type = "Asset"
            report_type = "Balance Sheet"
            account_type = ""
            account_currency = "VND"
            is_group = 0
            flags = type("F", (), {"ignore_permissions": False, "ignore_validate": False})()
            def save(self):
                promote_called["value"] = True
                self.is_group = 1

        class FakeLeaf:
            def __init__(self, p): self.payload = p
            flags = type("F", (), {"ignore_permissions": False})()
            def insert(self): self.name = "X"

        def gd(arg, *a, **k):
            if isinstance(arg, str):
                return FakeParent()
            return FakeLeaf(arg)

        with patch.object(coa_leaves, "frappe") as mock_frappe:
            mock_frappe.db.exists.side_effect = (
                lambda dt, *a, **k: dt == "Company"
            )
            mock_frappe.db.get_value.return_value = "999 - Test"
            mock_frappe.get_doc.side_effect = gd
            with patch.dict(coa_leaves.MISA_STANDARD_LEAVES,
                            {"999": [("9991", "Sub")]}, clear=True):
                coa_leaves.ensure_misa_leaves_for_company("DCT")
                self.assertTrue(promote_called["value"])


if __name__ == "__main__":
    unittest.main()
