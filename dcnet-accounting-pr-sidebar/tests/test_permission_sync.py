"""Unit tests for VN Accounting Settings permission matrix sync."""
import unittest
import frappe


class TestPermissionSync(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def test_permission_defaults_fixture_exists(self):
        """asset_permission_defaults.json fixture must exist and have ≥15 rows."""
        import json
        import os
        # fixture lives inside inner package: vn_accounting/vn_accounting/fixtures/
        app_inner = frappe.get_app_path("vn_accounting")  # .../vn_accounting/vn_accounting
        fixture_path = os.path.join(app_inner, "fixtures", "asset_permission_defaults.json")
        self.assertTrue(os.path.exists(fixture_path), f"Fixture not found at {fixture_path}")
        with open(fixture_path) as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 15, f"Expected ≥15 default rules, got {len(data)}")

    def test_settings_has_permission_matrix_field(self):
        """VN Accounting Settings must have permission_matrix Table field."""
        meta = frappe.get_meta("VN Accounting Settings")
        field = meta.get_field("permission_matrix")
        self.assertIsNotNone(field, "permission_matrix field must exist on VN Accounting Settings")
        self.assertEqual(field.fieldtype, "Table")

    def test_settings_has_threshold_fields(self):
        """VN Accounting Settings must have value threshold fields."""
        meta = frappe.get_meta("VN Accounting Settings")
        self.assertIsNotNone(meta.get_field("enable_value_thresholds"))
        self.assertIsNotNone(meta.get_field("handover_threshold"))

    def test_asset_permission_rule_doctype(self):
        """Asset Permission Rule child DocType must exist."""
        self.assertTrue(frappe.db.exists("DocType", "Asset Permission Rule"))

    def test_asset_handover_doctype_fields(self):
        """Asset Handover must have scope, co_signer_employee, before_handover_snapshot."""
        meta = frappe.get_meta("Asset Handover")
        self.assertIsNotNone(meta.get_field("scope"))
        self.assertIsNotNone(meta.get_field("co_signer_employee"))
        self.assertIsNotNone(meta.get_field("before_handover_snapshot"))


if __name__ == "__main__":
    unittest.main()
