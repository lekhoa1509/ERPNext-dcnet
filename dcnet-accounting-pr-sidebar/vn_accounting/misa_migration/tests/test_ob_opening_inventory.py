"""Unit tests for Phase 0 inventory opening handler."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestGroupByWarehouse(unittest.TestCase):

    def test_groups_correctly(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        rows = [
            {"warehouse": "KHO", "item_code": "A"},
            {"warehouse": "KHO_HCM", "item_code": "B"},
            {"warehouse": "KHO", "item_code": "C"},
            {"warehouse": None, "item_code": "D"},
        ]
        g = opening_inventory._group_by_warehouse(rows)
        self.assertEqual(set(g.keys()), {"KHO", "KHO_HCM", None})
        self.assertEqual(len(g["KHO"]), 2)


class TestSafeSuffix(unittest.TestCase):

    def test_strips_special_chars(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        f = opening_inventory._safe_suffix
        self.assertEqual(f("KHO"), "KHO")
        self.assertEqual(f("Kho HCM"), "KHO-HCM")
        self.assertEqual(f("Kho/HN/01"), "KHO-HN-01")
        self.assertEqual(f(None), "DEFAULT")
        self.assertEqual(f(""), "DEFAULT")


class TestResolveWarehouse(unittest.TestCase):

    def test_exact_match_first(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_company_default_warehouse",
                          return_value="DEFAULT - DC"):
            mock_frappe.db.exists.return_value = True
            self.assertEqual(opening_inventory._resolve_warehouse("KHO", "DC"), "KHO")

    def test_fallback_to_company_default(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_company_default_warehouse",
                          return_value="DEFAULT - DC"):
            mock_frappe.db.exists.return_value = False
            mock_frappe.db.get_value.return_value = None
            self.assertEqual(opening_inventory._resolve_warehouse("KHO", "DC"),
                             "DEFAULT - DC")

    def test_misa_uom_resolution(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe:
            mock_frappe.db.exists.side_effect = lambda dt, name: name in ("Cái", "Nos")
            self.assertEqual(opening_inventory._resolve_uom("Cái"), "Cái")
            self.assertEqual(opening_inventory._resolve_uom(None), "Nos")

    def test_uom_unknown_falls_back_to_nos(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe:
            mock_frappe.db.exists.side_effect = lambda dt, name: name == "Nos"
            self.assertEqual(opening_inventory._resolve_uom("UnknownUOM"), "Nos")


class TestResolveItem(unittest.TestCase):

    def test_existing_item_returned(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True
            self.assertEqual(
                opening_inventory._resolve_item("CC_MH_70S", "DC", "PLACEHOLDER"),
                "CC_MH_70S",
            )

    def test_missing_item_falls_back_to_placeholder(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False
            self.assertEqual(
                opening_inventory._resolve_item("GHOST", "DC", "PLACEHOLDER"),
                "PLACEHOLDER",
            )


class TestPostOpeningInventory(unittest.TestCase):

    def _patches(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        return {
            "module": opening_inventory,
            "patches": [
                patch.object(opening_inventory, "_ensure_stock_adjustment_account",
                             return_value="632 - GVHB - DC"),
                patch.object(opening_inventory, "_ensure_placeholder_item",
                             return_value="MISA-MIGRATION-SVC"),
                patch.object(opening_inventory, "_resolve_warehouse",
                             return_value="KHO Chính - DC"),
                patch.object(opening_inventory, "_resolve_uom", return_value="Cái"),
                patch.object(opening_inventory, "_resolve_item",
                             return_value="CC_MH_70S"),
            ],
        }

    def test_empty_rows_returns_failed(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        r = opening_inventory.post_opening_inventory("BATCH-X", [])
        self.assertEqual(r["status"], "failed")
        self.assertEqual(r["error"], "no rows")

    def test_no_stock_adjustment_returns_failed(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_ensure_stock_adjustment_account",
                          return_value=None):
            mock_frappe.defaults.get_global_default.return_value = "DC"
            r = opening_inventory.post_opening_inventory(
                "BATCH-X", [{"warehouse": "KHO", "qty": 1}],
            )
            self.assertEqual(r["status"], "failed")
            self.assertIn("stock_adjustment", r["error"])

    def test_creates_one_se_per_warehouse(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        captured = []

        class MockDoc:
            def __init__(self, payload):
                self.payload = payload
                self.name = payload.get("misa_voucher_no")
                self.flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name or self.name

        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_ensure_stock_adjustment_account",
                          return_value="632 - GVHB - DC"), \
             patch.object(opening_inventory, "_ensure_placeholder_item",
                          return_value="MISA-MIGRATION-SVC"), \
             patch.object(opening_inventory, "_resolve_warehouse",
                          side_effect=lambda wh, c: f"{wh} - DC"), \
             patch.object(opening_inventory, "_resolve_uom", return_value="Cái"), \
             patch.object(opening_inventory, "_resolve_item",
                          return_value="ITEM_A"):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = lambda payload: captured.append(payload) or MockDoc(payload)

            rows = [
                {"warehouse": "KHO", "item_code": "A", "item_name": "Item A",
                 "qty": 5, "rate": 100_000, "amount": 500_000, "uom": "Cái"},
                {"warehouse": "KHO", "item_code": "B", "item_name": "Item B",
                 "qty": 2, "rate": 200_000, "amount": 400_000, "uom": "Cái"},
                {"warehouse": "KHO_HCM", "item_code": "C", "item_name": "Item C",
                 "qty": 10, "rate": 50_000, "amount": 500_000, "uom": "Cái"},
            ]
            r = opening_inventory.post_opening_inventory("BATCH-X", rows)
            self.assertEqual(r["status"], "created")
            self.assertEqual(len(r["created_names"]), 2)  # 2 warehouses
            self.assertEqual(r["warehouse_count"], 2)
            self.assertEqual(r["item_count"], 3)
            self.assertEqual(r["total_value"], 1_400_000.0)

            # First SE has 2 items, second has 1
            payloads_by_wh = {p["to_warehouse"]: p for p in captured}
            self.assertIn("KHO - DC", payloads_by_wh)
            self.assertEqual(len(payloads_by_wh["KHO - DC"]["items"]), 2)
            self.assertEqual(payloads_by_wh["KHO - DC"]["stock_entry_type"],
                             "Material Receipt")
            # Each item has use_serial_batch_fields=1
            for item in payloads_by_wh["KHO - DC"]["items"]:
                self.assertEqual(item["use_serial_batch_fields"], 1)
                self.assertEqual(item["t_warehouse"], "KHO - DC")

    def test_zero_qty_rows_skipped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_ensure_stock_adjustment_account",
                          return_value="632"), \
             patch.object(opening_inventory, "_ensure_placeholder_item",
                          return_value="P"), \
             patch.object(opening_inventory, "_resolve_warehouse", return_value="WH"), \
             patch.object(opening_inventory, "_resolve_uom", return_value="Cái"), \
             patch.object(opening_inventory, "_resolve_item", return_value="I"):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = MagicMock()

            rows = [{"warehouse": "KHO", "qty": 0, "rate": 0, "amount": 0}]
            r = opening_inventory.post_opening_inventory("BATCH-Y", rows)
            # No items remained after filtering → no SE created
            self.assertEqual(r["status"], "failed")
            self.assertEqual(r["item_count"], 0)

    def test_rate_derived_from_amount_when_missing(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        captured = []
        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = p.get("misa_voucher_no")
            def insert(self, set_name=None): self.name = set_name or self.name
            flags = type("F", (), {"ignore_permissions": False})()
        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_ensure_stock_adjustment_account",
                          return_value="632"), \
             patch.object(opening_inventory, "_ensure_placeholder_item",
                          return_value="P"), \
             patch.object(opening_inventory, "_resolve_warehouse", return_value="WH"), \
             patch.object(opening_inventory, "_resolve_uom", return_value="Cái"), \
             patch.object(opening_inventory, "_resolve_item", return_value="I"):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = lambda p: captured.append(p) or MockDoc(p)
            rows = [{"warehouse": "KHO", "qty": 4, "rate": 0, "amount": 800_000, "uom": "C"}]
            r = opening_inventory.post_opening_inventory("BATCH-Z", rows)
            self.assertEqual(r["status"], "created")
            # rate = amount / qty = 200,000
            self.assertEqual(captured[0]["items"][0]["basic_rate"], 200_000.0)

    def test_idempotency_skips_existing(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_inventory
        with patch.object(opening_inventory, "frappe") as mock_frappe, \
             patch.object(opening_inventory, "_ensure_stock_adjustment_account",
                          return_value="632"), \
             patch.object(opening_inventory, "_ensure_placeholder_item",
                          return_value="P"), \
             patch.object(opening_inventory, "_resolve_warehouse", return_value="WH"):
            mock_frappe.db.exists.return_value = True  # SE already exists
            mock_frappe.defaults.get_global_default.return_value = "DC"
            rows = [{"warehouse": "KHO", "qty": 5, "rate": 100_000, "amount": 500_000}]
            r = opening_inventory.post_opening_inventory("BATCH-EXISTING", rows)
            # All SEs already exist → status='skipped', skipped_existing populated
            self.assertEqual(r["status"], "skipped")
            self.assertEqual(len(r["skipped_existing"]), 1)
            self.assertEqual(r["created_names"], [])


if __name__ == "__main__":
    unittest.main()
