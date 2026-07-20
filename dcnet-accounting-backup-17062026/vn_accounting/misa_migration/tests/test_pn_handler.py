"""Unit tests for PN (Phiếu nhập kho) → Purchase Invoice handler.

PN uses Purchase Invoice with update_stock=1 (combined invoice + stock
receipt in one ERPNext doc). Tests focus on dispatch shape; full insert
of items into a warehouse is exercised in E2E commit 15.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch


class TestCompanyDefaultWarehouse(unittest.TestCase):
    """`_company_default_warehouse` — picks first active non-group warehouse."""

    def test_returns_first_active_warehouse(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "Kho Mặc Định - DC"
            wh = purchase_receipt._company_default_warehouse("DC")
            self.assertEqual(wh, "Kho Mặc Định - DC")
            # Verify filters: company + is_group=0 + disabled=0
            args, _ = mock_frappe.db.get_value.call_args
            self.assertEqual(args[0], "Warehouse")
            self.assertEqual(args[1]["company"], "DC")
            self.assertEqual(args[1]["is_group"], 0)
            self.assertEqual(args[1]["disabled"], 0)

    def test_returns_none_when_no_warehouse_exists(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = None
            wh = purchase_receipt._company_default_warehouse("DC")
            self.assertIsNone(wh)


class TestCreatePiPrFromPn(unittest.TestCase):
    """Dispatch tests for `create_pi_pr_from_pn` — validates the early
    return paths and the payload shape sent to frappe.get_doc on success.
    """

    def test_missing_voucher_no_fails(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        result = purchase_receipt.create_pi_pr_from_pn({})
        self.assertEqual(result["status"], "failed")
        self.assertIn("voucher_no", result["error"])

    def test_missing_party_code_fails(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            mock_frappe.db.exists.return_value = False
            v = {"voucher_no": "PN20260001", "prefix": "PN", "legs": []}
            result = purchase_receipt.create_pi_pr_from_pn(v)
            self.assertEqual(result["status"], "failed")
            self.assertIn("party_code", result["error"])

    def test_supplier_not_found_fails(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            # PI doesn't exist (idempotency check pass), Supplier doesn't exist
            mock_frappe.db.exists.side_effect = lambda dt, name: False
            v = {"voucher_no": "PN20260001", "prefix": "PN",
                 "party_code": "GHOST_SUP", "legs": []}
            result = purchase_receipt.create_pi_pr_from_pn(v)
            self.assertEqual(result["status"], "failed")
            self.assertIn("Supplier", result["error"])

    def test_idempotency_already_exists(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            # PI exists → skip
            mock_frappe.db.exists.return_value = True
            v = {"voucher_no": "PN20260001", "prefix": "PN",
                 "party_code": "VIETTEL", "legs": []}
            result = purchase_receipt.create_pi_pr_from_pn(v)
            self.assertEqual(result["status"], "skipped")
            self.assertEqual(result["target_name"], "PN20260001")
            self.assertEqual(result["target_doctype"], "Purchase Invoice")

    def test_no_warehouse_available_fails(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            # PI doesn't exist, Supplier exists, Company configured
            existence_map = {
                ("Purchase Invoice", "PN20260001"): False,
                ("Supplier", "VIETTEL"): True,
            }
            mock_frappe.db.exists.side_effect = lambda dt, name: \
                existence_map.get((dt, name), False)
            mock_frappe.defaults.get_global_default.return_value = "DCNET"
            # _company_default_warehouse returns None (no warehouse)
            with patch.object(purchase_receipt, "_company_default_warehouse",
                              return_value=None):
                v = {"voucher_no": "PN20260001", "prefix": "PN",
                     "party_code": "VIETTEL", "legs": []}
                result = purchase_receipt.create_pi_pr_from_pn(v)
                self.assertEqual(result["status"], "failed")
                self.assertIn("warehouse", result["error"])

    def test_success_payload_has_update_stock_and_warehouse(self):
        """Verify the payload sent to frappe.get_doc has update_stock=1 +
        per-item warehouse + supplier_warehouse."""
        from vn_accounting.misa_migration.importers.nkc_handlers import purchase_receipt
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

        with patch.object(purchase_receipt, "frappe") as mock_frappe:
            existence_map = {
                ("Purchase Invoice", "PN20260001"): False,
                ("Supplier", "VIETTEL"): True,
                ("UOM", "Nos"): True,
            }
            mock_frappe.db.exists.side_effect = lambda dt, name: \
                existence_map.get((dt, name), False)
            mock_frappe.defaults.get_global_default.return_value = "DCNET"
            mock_frappe.db.get_value.return_value = None  # company default wh
            mock_frappe.get_doc = mock_get_doc
            mock_frappe.log_error = lambda **kw: None

            with patch.object(purchase_receipt, "_company_default_warehouse",
                              return_value="Kho Chính - DC"), \
                 patch.object(purchase_receipt, "_load_account_mapping",
                              return_value={}), \
                 patch.object(purchase_receipt, "_resolve_account",
                              return_value="156 - Hàng hóa - DC"), \
                 patch.object(purchase_receipt, "_ensure_placeholder_item",
                              return_value="MISA-MIGRATION-SVC"), \
                 patch.object(purchase_receipt.vat_extractor,
                              "extract_vat_account", return_value="1331"), \
                 patch.object(purchase_receipt.vat_extractor,
                              "build_tax_rows", return_value=[]):
                v = {
                    "voucher_no": "PN20260001", "prefix": "PN",
                    "party_code": "VIETTEL", "posting_date": "2026-01-15",
                    "voucher_remark": "Nhập kho cáp quang",
                    "legs": [
                        {"account": "1561", "debit": 1000000, "credit": 0},
                        {"account": "1331", "debit": 100000, "credit": 0},
                        {"account": "331", "debit": 0, "credit": 1100000},
                    ],
                }
                invoice = {
                    "line_items": [{
                        "item_name": "Cáp quang 4FO",
                        "description": "Cáp quang 4FO",
                        "uom": "Nos", "qty": 100.0, "rate": 10000.0,
                        "net_amount": 1000000.0,
                        "tax_rate": 10.0, "tax_amount": 100000.0,
                        "tax_account": "1331",
                    }],
                    "invoice_no": "INV2026/001",
                    "invoice_date": "2026-01-15",
                    "party_name": "Viettel Telecom",
                }
                result = purchase_receipt.create_pi_pr_from_pn(v, invoice)
                self.assertEqual(result["status"], "created")
                self.assertEqual(result["target_name"], "PN20260001")
                self.assertEqual(result["target_doctype"], "Purchase Invoice")
                self.assertTrue(result["update_stock"])
                self.assertEqual(result["warehouse"], "Kho Chính - DC")
                self.assertIsNone(result["pr_target_name"])

                # Verify payload shape
                self.assertEqual(len(captured_payloads), 1)
                pl = captured_payloads[0]
                self.assertEqual(pl["doctype"], "Purchase Invoice")
                self.assertEqual(pl["update_stock"], 1)
                self.assertEqual(pl["supplier_warehouse"], "Kho Chính - DC")
                self.assertEqual(pl["supplier"], "VIETTEL")
                self.assertEqual(pl["bill_no"], "INV2026/001")
                self.assertEqual(len(pl["items"]), 1)
                self.assertEqual(pl["items"][0]["warehouse"], "Kho Chính - DC")
                self.assertEqual(pl["misa_voucher_no"], "PN20260001")


if __name__ == "__main__":
    unittest.main()
