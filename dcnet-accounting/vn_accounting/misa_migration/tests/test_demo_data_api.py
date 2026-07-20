"""Unit tests for the demo-data detection + wipe API."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestDcnetSampleInstalledCheck(unittest.TestCase):

    def test_returns_true_when_present(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = [
                "frappe", "erpnext", "vn_accounting", "dcnet_sample",
            ]
            self.assertTrue(demo_data._dcnet_sample_installed())

    def test_returns_false_when_absent(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = ["frappe", "erpnext"]
            self.assertFalse(demo_data._dcnet_sample_installed())

    def test_swallows_get_installed_apps_exceptions(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.side_effect = RuntimeError("boom")
            self.assertFalse(demo_data._dcnet_sample_installed())


class TestDemoFlagSet(unittest.TestCase):

    def test_returns_true_when_flag_is_string_one(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.db.get_default.return_value = "1"
            self.assertTrue(demo_data._demo_flag_set())

    def test_returns_false_when_flag_none(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.db.get_default.return_value = None
            self.assertFalse(demo_data._demo_flag_set())

    def test_returns_false_when_flag_other_value(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.db.get_default.return_value = "0"
            self.assertFalse(demo_data._demo_flag_set())


class TestDetectDemoData(unittest.TestCase):

    def test_dcnet_sample_absent_returns_no_demo(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = ["frappe", "erpnext"]
            mock_frappe.db.get_default.return_value = None
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.count.return_value = 0
            meta = MagicMock()
            meta.has_field.return_value = True
            mock_frappe.get_meta.return_value = meta
            r = demo_data.detect_demo_data()
            self.assertFalse(r["dcnet_sample_installed"])
            self.assertFalse(r["has_demo_data"])
            self.assertFalse(r["wipe_available"])

    def test_flag_set_with_zero_counts_still_detects(self):
        """Edge case: flag stuck at '1' but rows manually wiped → still flag."""
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = ["dcnet_sample"]
            mock_frappe.db.get_default.return_value = "1"
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.count.return_value = 0
            meta = MagicMock()
            meta.has_field.return_value = True
            mock_frappe.get_meta.return_value = meta
            r = demo_data.detect_demo_data()
            self.assertTrue(r["dcnet_sample_installed"])
            self.assertTrue(r["demo_flag_set"])
            self.assertTrue(r["has_demo_data"])
            self.assertEqual(r["total"], 0)

    def test_counts_use_company_filter_when_field_present(self):
        from vn_accounting.misa_migration.api import demo_data
        captured_filters = []
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = ["dcnet_sample"]
            mock_frappe.db.get_default.return_value = "1"
            mock_frappe.defaults.get_global_default.return_value = "DC"

            def fake_count(dt, filters=None):
                captured_filters.append((dt, filters))
                return 5
            mock_frappe.db.count.side_effect = fake_count
            meta = MagicMock()
            meta.has_field.return_value = True
            mock_frappe.get_meta.return_value = meta
            r = demo_data.detect_demo_data(company="DC")
            self.assertEqual(r["company"], "DC")
            self.assertGreater(len(captured_filters), 0)
            # First captured was called with filters={"company": "DC"}
            for dt, flt in captured_filters:
                self.assertEqual(flt, {"company": "DC"})

    def test_counts_no_filter_when_company_field_absent(self):
        """Item has no company field — should call db.count(dt) without filter."""
        from vn_accounting.misa_migration.api import demo_data
        captured = []
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = ["dcnet_sample"]
            mock_frappe.db.get_default.return_value = "1"
            mock_frappe.defaults.get_global_default.return_value = "DC"

            def fake_count(dt, filters=None):
                captured.append((dt, filters))
                return 1
            mock_frappe.db.count.side_effect = fake_count

            def make_meta(dt):
                m = MagicMock()
                # Pretend Item lacks company; everything else has it
                m.has_field.return_value = (dt != "Item")
                return m
            mock_frappe.get_meta.side_effect = make_meta
            demo_data.detect_demo_data(company="DC")
            item_call = [c for c in captured if c[0] == "Item"]
            self.assertEqual(len(item_call), 1)
            # Item filters arg is None
            self.assertIsNone(item_call[0][1])


class TestWipeDemoData(unittest.TestCase):

    def test_missing_confirm_token_throws(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                demo_data.wipe_demo_data(confirm="")
            self.assertIn("WIPE-DEMO-DATA", str(ctx.exception))

    def test_wrong_confirm_token_throws(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError):
                demo_data.wipe_demo_data(confirm="yes-please")

    def test_dcnet_sample_not_installed_throws(self):
        from vn_accounting.misa_migration.api import demo_data
        with patch.object(demo_data, "frappe") as mock_frappe:
            mock_frappe.get_installed_apps.return_value = ["frappe", "erpnext"]
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                demo_data.wipe_demo_data(confirm="WIPE-DEMO-DATA")
            self.assertIn("dcnet_sample chưa", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
