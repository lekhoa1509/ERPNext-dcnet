"""Unit tests for Phase 0 Asset + CCDC opening handler."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestResolveAssetCategory(unittest.TestCase):

    def test_exact_match(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True
            self.assertEqual(
                opening_asset._resolve_asset_category("Máy móc, thiết bị", "DC"),
                "Máy móc, thiết bị",
            )

    def test_hint_fuzzy_match(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            # Exact 'X' doesn't exist, but 'Plant and Machinery' (a candidate) does
            mock_frappe.db.exists.side_effect = (
                lambda dt, name: name == "Plant and Machinery"
            )
            mock_frappe.db.get_value.return_value = None
            self.assertEqual(
                opening_asset._resolve_asset_category("Máy móc đặc thù", "DC"),
                "Plant and Machinery",
            )

    def test_fallback_to_first_category(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False  # nothing exact
            mock_frappe.db.get_value.return_value = "AnyCategory"
            self.assertEqual(
                opening_asset._resolve_asset_category("Random text", "DC"),
                "AnyCategory",
            )


class TestResolveAssetCategoryCCDC(unittest.TestCase):
    """CCDC rows don't carry asset_category in Misa file — handler auto-creates
    a generic 'CCDC' default Asset Category via _ensure_ccdc_default_category.
    """

    def test_ccdc_with_none_category_creates_default(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            # Asset Category 'CCDC' doesn't exist yet, accounts do
            existence = {"CCDC": False}
            mock_frappe.db.exists.side_effect = lambda dt, name=None, *a, **k: (
                existence.get(name, False) if dt == "Asset Category" else False
            )
            mock_frappe.db.get_value.side_effect = (
                lambda dt, filters, field=None, *a, **k:
                    "242 - Acc" if "242" in str(filters)
                    else "6427 - Acc" if "6427" in str(filters)
                    else "214 - Acc" if "214" in str(filters)
                    else None
            )
            created = []
            class FakeCat:
                def __init__(self, p): self.payload = p
                flags = type("F", (), {"ignore_permissions": False})()
                def insert(self, set_name=None):
                    self.name = set_name; created.append(self.payload)
                    existence["CCDC"] = True
            mock_frappe.get_doc = lambda p: FakeCat(p)

            result = opening_asset._resolve_asset_category(
                None, "DCT", is_ccdc=True
            )
            self.assertEqual(result, "CCDC")
            self.assertEqual(len(created), 1)
            # Verify the 3 GL accounts wired into the category
            accounts = created[0]["accounts"][0]
            self.assertEqual(accounts["fixed_asset_account"], "242 - Acc")
            self.assertEqual(accounts["depreciation_expense_account"], "6427 - Acc")
            self.assertEqual(accounts["accumulated_depreciation_account"], "214 - Acc")

    def test_ccdc_when_category_already_exists_returns_it(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = True  # CCDC exists
            r = opening_asset._resolve_asset_category(None, "DCT", is_ccdc=True)
            self.assertEqual(r, "CCDC")

    def test_non_ccdc_with_none_returns_none(self):
        """Regression — non-CCDC FA rows with None category still get None,
        not CCDC default."""
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe"):
            r = opening_asset._resolve_asset_category(None, "DCT", is_ccdc=False)
            self.assertIsNone(r)


class TestResolveAssetItem(unittest.TestCase):

    def test_returns_existing_fixed_asset_item(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "CC_MD_AQ1000"
            self.assertEqual(
                opening_asset._resolve_asset_item("CC_MD_AQ1000", "DC"),
                "CC_MD_AQ1000",
            )

    def test_returns_none_if_not_fixed_asset(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = None
            self.assertIsNone(opening_asset._resolve_asset_item("FOO", "DC"))

    def test_none_code_returns_none(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        self.assertIsNone(opening_asset._resolve_asset_item(None, "DC"))


class TestAddOneMonth(unittest.TestCase):

    def test_normal_month(self):
        from vn_accounting.misa_migration.importers.ob_handlers.opening_asset \
            import _add_one_month
        self.assertEqual(_add_one_month("2025-01-15"), "2025-02-15")
        self.assertEqual(_add_one_month("2025-06-30"), "2025-07-28")  # clamp 30→28

    def test_year_rollover(self):
        from vn_accounting.misa_migration.importers.ob_handlers.opening_asset \
            import _add_one_month
        self.assertEqual(_add_one_month("2025-12-31"), "2026-01-28")

    def test_none(self):
        from vn_accounting.misa_migration.importers.ob_handlers.opening_asset \
            import _add_one_month
        self.assertIsNone(_add_one_month(None))


class TestPostOpeningAssets(unittest.TestCase):

    def _shared_patches(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        return [
            patch.object(opening_asset, "_resolve_asset_item",
                         return_value="ITEM_CODE"),
            patch.object(opening_asset, "_resolve_asset_category",
                         return_value="MyCategory"),
            patch.object(opening_asset, "_resolve_location",
                         return_value=None),
        ]

    def test_empty_returns_failed(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        r = opening_asset.post_opening_assets("BATCH-X", [])
        self.assertEqual(r["status"], "failed")

    def test_creates_asset_doc_with_correct_fields(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        captured = []
        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = p.get("misa_voucher_no")
            def insert(self, set_name=None): self.name = set_name or self.name
            flags = type("F", (), {"ignore_permissions": False})()

        with patch.object(opening_asset, "frappe") as mock_frappe, \
             patch.object(opening_asset, "_resolve_asset_item", return_value="CC_GHE"), \
             patch.object(opening_asset, "_resolve_asset_category",
                          return_value="Office Equipment"), \
             patch.object(opening_asset, "_resolve_location", return_value=None):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = lambda p: captured.append(p) or MockDoc(p)
            # No is_ccdc field on Asset in this site
            meta = MagicMock(); meta.has_field.return_value = False
            mock_frappe.get_meta.return_value = meta

            rows = [{
                "asset_code": "CC_GHE", "asset_name": "Ghế massage",
                "asset_category": "Thiết bị, dụng cụ quản lý",
                "gross_amount": 40_740_741, "accumulated_depreciation": 31_272_284,
                "available_for_use_date": "2022-09-12",
                "depreciation_start_date": "2022-09-12",
                "useful_life_months": 36, "remaining_useful_life_months": 8,
            }]
            r = opening_asset.post_opening_assets("BATCH-X", rows, is_ccdc=False)
            self.assertEqual(r["status"], "created")
            self.assertEqual(r["asset_count"], 1)
            self.assertEqual(r["total_gross"], 40_740_741)
            self.assertEqual(r["total_accumulated_depreciation"], 31_272_284)

            pl = captured[0]
            self.assertEqual(pl["doctype"], "Asset")
            self.assertEqual(pl["is_existing_asset"], 1)
            self.assertEqual(pl["asset_category"], "Office Equipment")
            self.assertEqual(pl["gross_purchase_amount"], 40_740_741)
            self.assertEqual(pl["opening_accumulated_depreciation"], 31_272_284)
            self.assertEqual(pl["total_number_of_depreciations"], 36)
            self.assertEqual(pl["frequency_of_depreciation"], "Monthly")
            self.assertEqual(pl["depreciation_method"], "Đường thẳng")
            self.assertNotIn("is_ccdc", pl)

    def test_ccdc_sets_is_ccdc_when_field_exists(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        captured = []
        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = p.get("misa_voucher_no")
            def insert(self, set_name=None): self.name = set_name or self.name
            flags = type("F", (), {"ignore_permissions": False})()

        with patch.object(opening_asset, "frappe") as mock_frappe, \
             patch.object(opening_asset, "_resolve_asset_item", return_value="DT_YEA"), \
             patch.object(opening_asset, "_resolve_asset_category",
                          return_value="Office Equipment"), \
             patch.object(opening_asset, "_resolve_location", return_value=None):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = lambda p: captured.append(p) or MockDoc(p)
            # is_ccdc field exists on Asset in this site
            meta = MagicMock(); meta.has_field.return_value = True
            mock_frappe.get_meta.return_value = meta

            rows = [{
                "ccdc_code": "DT_YEALINK_T19E2", "ccdc_name": "ĐT YEALINK",
                "available_for_use_date": "2021-06-02",
                "qty": 2, "gross_amount": 1_400_000, "remaining_amount": 0,
                "total_periods": 2, "remaining_periods": 0,
                "per_period_amount": 700_000, "holding_account": "242",
            }]
            r = opening_asset.post_opening_assets("BATCH-Y", rows, is_ccdc=True)
            self.assertEqual(r["status"], "created")
            self.assertTrue(r["is_ccdc"])
            self.assertEqual(captured[0]["is_ccdc"], 1)
            self.assertEqual(captured[0]["total_number_of_depreciations"], 2)
            self.assertEqual(captured[0]["asset_quantity"], 2.0)

    def test_skips_row_without_item(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe, \
             patch.object(opening_asset, "_resolve_asset_item", return_value=None):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            rows = [{
                "asset_code": "GHOST", "asset_name": "X",
                "gross_amount": 100_000_000, "useful_life_months": 36,
            }]
            r = opening_asset.post_opening_assets("BATCH-X", rows)
            self.assertEqual(r["status"], "failed")
            self.assertEqual(len(r["skipped_rows"]), 1)
            self.assertIn("not found or is_fixed_asset=0",
                          r["skipped_rows"][0]["reason"])

    def test_skips_row_without_useful_life(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe, \
             patch.object(opening_asset, "_resolve_asset_item", return_value="X"), \
             patch.object(opening_asset, "_resolve_asset_category", return_value="C"):
            mock_frappe.db.exists.return_value = False
            mock_frappe.defaults.get_global_default.return_value = "DC"
            rows = [{
                "asset_code": "FOO", "gross_amount": 1_000_000,
                "useful_life_months": None,
            }]
            r = opening_asset.post_opening_assets("BATCH-X", rows)
            self.assertEqual(r["status"], "failed")
            self.assertIn("useful_life", r["skipped_rows"][0]["reason"])

    def test_idempotency_existing_asset_skipped(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_asset
        with patch.object(opening_asset, "frappe") as mock_frappe, \
             patch.object(opening_asset, "_resolve_asset_item", return_value="X"), \
             patch.object(opening_asset, "_resolve_asset_category", return_value="C"):
            mock_frappe.db.exists.return_value = True  # Asset already exists
            mock_frappe.defaults.get_global_default.return_value = "DC"
            rows = [{
                "asset_code": "EXISTING",
                "gross_amount": 1_000_000, "useful_life_months": 24,
            }]
            r = opening_asset.post_opening_assets("BATCH-X", rows)
            self.assertEqual(r["status"], "skipped")
            self.assertEqual(r["skipped_existing"], ["EXISTING"])


if __name__ == "__main__":
    unittest.main()
