"""Unit tests for PX / PXHN / PNHN → Stock Entry handlers.

Focused on dispatch shape — Stock Entry submit logic (SLE creation, batch
validation) is exercised in E2E commit 15. Here we mock frappe and
verify the payload sent to frappe.get_doc.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestSeTypeByPrefix(unittest.TestCase):
    """Static prefix → (stock_entry_type, needs_source, needs_target) map."""

    def test_px_is_material_issue_source_only(self):
        from vn_accounting.misa_migration.importers.nkc_handlers.stock_entry \
            import _SE_TYPE_BY_PREFIX
        self.assertEqual(_SE_TYPE_BY_PREFIX["PX"],
                         ("Material Issue", True, False))

    def test_pxhn_is_material_transfer_both(self):
        from vn_accounting.misa_migration.importers.nkc_handlers.stock_entry \
            import _SE_TYPE_BY_PREFIX
        self.assertEqual(_SE_TYPE_BY_PREFIX["PXHN"],
                         ("Material Transfer", True, True))

    def test_pnhn_is_material_receipt_target_only(self):
        from vn_accounting.misa_migration.importers.nkc_handlers.stock_entry \
            import _SE_TYPE_BY_PREFIX
        self.assertEqual(_SE_TYPE_BY_PREFIX["PNHN"],
                         ("Material Receipt", False, True))


class TestEnsureStockAdjustmentAccount(unittest.TestCase):
    """`_ensure_stock_adjustment_account` — sets default if absent."""

    def test_returns_existing_company_field(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "632 - Giá vốn - DC"
            result = stock_entry._ensure_stock_adjustment_account("DC")
            self.assertEqual(result, "632 - Giá vốn - DC")
            # Only one get_value call (Company.stock_adjustment_account)
            self.assertEqual(mock_frappe.db.get_value.call_count, 1)

    def test_falls_back_to_tk_632_and_sets_company(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "frappe") as mock_frappe:
            # First call: Company.stock_adjustment_account=None
            # Second call: Account lookup for TK 632
            mock_frappe.db.get_value.side_effect = [None, "632 - GVHB - DC"]
            mock_frappe.db.set_value = MagicMock()
            result = stock_entry._ensure_stock_adjustment_account("DC")
            self.assertEqual(result, "632 - GVHB - DC")
            mock_frappe.db.set_value.assert_called_once_with(
                "Company", "DC", "stock_adjustment_account",
                "632 - GVHB - DC", update_modified=False,
            )

    def test_returns_none_when_no_tk_632(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = None
            result = stock_entry._ensure_stock_adjustment_account("DC")
            self.assertIsNone(result)


class TestAltWarehouseForTransfer(unittest.TestCase):
    """`_alt_warehouse_for_transfer` — picks a 2nd warehouse for Transfer."""

    def test_picks_first_warehouse_different_from_primary(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "frappe") as mock_frappe:
            mock_frappe.db.get_all.return_value = [
                {"name": "Kho A - DC"},
                {"name": "Kho B - DC"},
            ]
            result = stock_entry._alt_warehouse_for_transfer("DC", "Kho A - DC")
            self.assertEqual(result, "Kho B - DC")

    def test_returns_none_when_only_primary_exists(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "frappe") as mock_frappe:
            mock_frappe.db.get_all.return_value = [{"name": "Kho A - DC"}]
            result = stock_entry._alt_warehouse_for_transfer("DC", "Kho A - DC")
            self.assertIsNone(result)

    def test_returns_none_when_primary_missing(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        result = stock_entry._alt_warehouse_for_transfer("DC", None)
        self.assertIsNone(result)


class TestCreateSeDispatch(unittest.TestCase):
    """Top-level `_create_se` dispatch — verify payload shape per prefix."""

    def _run_with_mocks(self, voucher, prefix,
                        warehouse="Kho A - DC", alt_warehouse="Kho B - DC",
                        stock_adj="632 - GVHB - DC", uom_exists=True):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        captured_payloads: list[dict] = []

        class MockDoc:
            def __init__(self, payload):
                self.payload = payload
                self.name = payload.get("misa_voucher_no")
                self.flags = type("F", (), {"ignore_permissions": False})()

            def insert(self, set_name=None):
                self.name = set_name or self.name
                return self

        def mock_get_doc(payload):
            captured_payloads.append(payload)
            return MockDoc(payload)

        with patch.object(stock_entry, "frappe") as mock_frappe:
            mock_frappe.db.exists.side_effect = lambda dt, name: \
                (dt, name) != ("Stock Entry", voucher["voucher_no"])
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.get_value.return_value = "DC"
            mock_frappe.get_doc = mock_get_doc
            mock_frappe.log_error = lambda **kw: None

            with patch.object(stock_entry, "_ensure_stock_adjustment_account",
                              return_value=stock_adj), \
                 patch.object(stock_entry, "_company_default_warehouse",
                              return_value=warehouse), \
                 patch.object(stock_entry, "_alt_warehouse_for_transfer",
                              return_value=alt_warehouse), \
                 patch.object(stock_entry, "_ensure_placeholder_item",
                              return_value="MISA-MIGRATION-SVC"):
                result = stock_entry._create_se(voucher, prefix)
        return result, captured_payloads

    def test_px_material_issue_source_warehouse_only(self):
        voucher = {
            "voucher_no": "PX20260001", "prefix": "PX",
            "posting_date": "2026-01-15",
            "voucher_remark": "Xuất kho bán hàng",
            "legs": [
                {"account": "632", "debit": 1000000, "credit": 0},
                {"account": "156", "debit": 0, "credit": 1000000},
            ],
        }
        result, payloads = self._run_with_mocks(voucher, "PX")
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["target_name"], "PX20260001")
        self.assertEqual(result["stock_entry_type"], "Material Issue")
        self.assertEqual(result["source_warehouse"], "Kho A - DC")
        self.assertIsNone(result["target_warehouse"])

        pl = payloads[0]
        self.assertEqual(pl["stock_entry_type"], "Material Issue")
        self.assertEqual(pl["from_warehouse"], "Kho A - DC")
        self.assertNotIn("to_warehouse", pl)
        self.assertEqual(len(pl["items"]), 1)
        self.assertEqual(pl["items"][0]["s_warehouse"], "Kho A - DC")
        self.assertNotIn("t_warehouse", pl["items"][0])
        self.assertEqual(pl["items"][0]["use_serial_batch_fields"], 1)
        # qty/rate: 2 legs → halved → 1,000,000
        self.assertEqual(pl["items"][0]["basic_rate"], 1000000.0)

    def test_pxhn_material_transfer_both_warehouses(self):
        voucher = {
            "voucher_no": "PXHN20260001", "prefix": "PXHN",
            "posting_date": "2026-01-15",
            "voucher_remark": "Chuyển kho nội bộ",
            "legs": [
                {"account": "156", "debit": 500000, "credit": 0},
                {"account": "156", "debit": 0, "credit": 500000},
            ],
        }
        result, payloads = self._run_with_mocks(voucher, "PXHN")
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["stock_entry_type"], "Material Transfer")
        self.assertEqual(result["source_warehouse"], "Kho A - DC")
        self.assertEqual(result["target_warehouse"], "Kho B - DC")

        pl = payloads[0]
        self.assertEqual(pl["from_warehouse"], "Kho A - DC")
        self.assertEqual(pl["to_warehouse"], "Kho B - DC")
        item = pl["items"][0]
        self.assertEqual(item["s_warehouse"], "Kho A - DC")
        self.assertEqual(item["t_warehouse"], "Kho B - DC")

    def test_pnhn_material_receipt_target_warehouse_only(self):
        voucher = {
            "voucher_no": "PNHN20260001", "prefix": "PNHN",
            "posting_date": "2026-01-15",
            "voucher_remark": "Nhập kho nội bộ",
            "legs": [
                {"account": "156", "debit": 200000, "credit": 0},
                {"account": "152", "debit": 0, "credit": 200000},
            ],
        }
        result, payloads = self._run_with_mocks(voucher, "PNHN")
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["stock_entry_type"], "Material Receipt")
        self.assertIsNone(result["source_warehouse"])
        self.assertEqual(result["target_warehouse"], "Kho A - DC")

        pl = payloads[0]
        self.assertEqual(pl["to_warehouse"], "Kho A - DC")
        self.assertNotIn("from_warehouse", pl)
        item = pl["items"][0]
        self.assertNotIn("s_warehouse", item)
        self.assertEqual(item["t_warehouse"], "Kho A - DC")

    def test_transfer_fails_when_only_one_warehouse(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        voucher = {
            "voucher_no": "PXHN20260002", "prefix": "PXHN",
            "voucher_remark": "no alt wh", "legs": []
        }
        result, payloads = self._run_with_mocks(
            voucher, "PXHN", alt_warehouse=None
        )
        self.assertEqual(result["status"], "failed")
        self.assertIn("≥2 warehouses", result["error"])
        self.assertEqual(payloads, [])

    def test_missing_voucher_no_fails(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        result = stock_entry._create_se({}, "PX")
        self.assertEqual(result["status"], "failed")
        self.assertIn("voucher_no", result["error"])

    def test_unknown_prefix_fails(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        # Have to bypass exists-check, easiest: mock frappe
        with patch.object(stock_entry, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False
            result = stock_entry._create_se(
                {"voucher_no": "X1", "prefix": "X"}, "X"
            )
        self.assertEqual(result["status"], "failed")
        self.assertIn("Unknown SE prefix", result["error"])

    def test_idempotency_already_exists(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "frappe") as mock_frappe:
            # Stock Entry exists → skip
            mock_frappe.db.exists.return_value = True
            result = stock_entry._create_se(
                {"voucher_no": "PX20260001", "prefix": "PX"}, "PX"
            )
            self.assertEqual(result["status"], "skipped")
            self.assertEqual(result["target_name"], "PX20260001")


class TestPublicEntryPoints(unittest.TestCase):
    """Verify the 3 public functions dispatch to `_create_se` with the
    right prefix string."""

    def test_create_se_from_px(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "_create_se") as mock:
            mock.return_value = {"status": "created"}
            stock_entry.create_se_from_px({"voucher_no": "PX1"})
            mock.assert_called_once()
            args, _ = mock.call_args
            self.assertEqual(args[1], "PX")

    def test_create_se_from_pxhn(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "_create_se") as mock:
            mock.return_value = {"status": "created"}
            stock_entry.create_se_from_pxhn({"voucher_no": "PXHN1"})
            args, _ = mock.call_args
            self.assertEqual(args[1], "PXHN")

    def test_create_se_from_pnhn(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import stock_entry
        with patch.object(stock_entry, "_create_se") as mock:
            mock.return_value = {"status": "created"}
            stock_entry.create_se_from_pnhn({"voucher_no": "PNHN1"})
            args, _ = mock.call_args
            self.assertEqual(args[1], "PNHN")


if __name__ == "__main__":
    unittest.main()
