"""Tests for ItemImporter — Tính chất → flags mapping + Item Defaults."""

from __future__ import annotations

import json
import unittest

import frappe

from vn_accounting.misa_migration.importers.item import ItemImporter


class TestItemImporter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = frappe.get_doc({
            "doctype": "Misa Migration Batch",
            "company": "DCNET",
            "batch_title": "_TEST_ITEM_IMPORTER_",
            "status": "DRAFT",
        }).insert(ignore_permissions=True)

    @classmethod
    def tearDownClass(cls):
        frappe.db.set_value("Misa Migration Batch", cls.batch.name, "status",
                            "REVERSED", update_modified=False)
        for r in frappe.get_all("Misa Migration Row", filters={"batch": cls.batch.name},
                                 pluck="name"):
            frappe.delete_doc("Misa Migration Row", r, force=True, ignore_permissions=True)
        frappe.delete_doc("Misa Migration Batch", cls.batch.name, force=True,
                          ignore_permissions=True)
        frappe.db.commit()

    def _build(self, **misa_fields):
        imp = ItemImporter(self.batch.name)
        normalized = imp.normalize(misa_fields)
        return imp.build_doc(normalized), imp.validate(normalized)

    def test_hanghoa_is_stock(self):
        doc, errs = self._build(**{"Mã": "T1", "Tên": "T1 name", "Tính chất": "Hàng hóa"})
        self.assertEqual(errs, [])
        self.assertEqual(doc["is_stock_item"], 1)
        self.assertEqual(doc["is_fixed_asset"], 0)

    def test_dich_vu_not_stock(self):
        doc, _ = self._build(**{"Mã": "T2", "Tên": "Service", "Tính chất": "Dịch vụ"})
        self.assertEqual(doc["is_stock_item"], 0)
        self.assertEqual(doc["is_fixed_asset"], 0)

    def test_tscd_is_fixed_asset(self):
        doc, _ = self._build(**{"Mã": "T3", "Tên": "Máy in", "Tính chất": "TSCĐ"})
        self.assertEqual(doc["is_fixed_asset"], 1)
        self.assertEqual(doc["is_stock_item"], 0)

    def test_ccdc_has_marker(self):
        doc, _ = self._build(**{"Mã": "T4", "Tên": "Bút bi", "Tính chất": "CCDC"})
        self.assertEqual(doc["is_stock_item"], 1)
        self.assertIn("[CCDC]", doc["description"])

    def test_blank_tinh_chat_is_service(self):
        doc, _ = self._build(**{"Mã": "T5", "Tên": "Unknown", "Tính chất": ""})
        self.assertEqual(doc["is_stock_item"], 0)

    def test_validate_missing_code(self):
        # Don't call _build() — build_doc requires _code. Only test validate.
        imp = ItemImporter(self.batch.name)
        normalized = imp.normalize({"Tên": "Only name"})
        errs = imp.validate(normalized)
        self.assertTrue(any("Mã" in e for e in errs))

    def test_dedupe_key_is_misa_ma(self):
        imp = ItemImporter(self.batch.name)
        n = imp.normalize({"Mã": "ACQUY_12V_100AH", "Tên": "T"})
        self.assertEqual(imp.dedupe_key(n), "ACQUY_12V_100AH")

    def test_disabled_status(self):
        doc, _ = self._build(**{"Mã": "T6", "Tên": "X", "Tính chất": "Hàng hóa",
                                 "Trạng thái": "Ngừng sử dụng"})
        self.assertEqual(doc["disabled"], 1)

    def test_item_defaults_via_account_mapping(self):
        # Seed mapping for 156 + 511 (exist in DCNET COA)
        mapping_doc = frappe.get_single("Misa Account Mapping")
        try:
            mapping = json.loads(mapping_doc.mappings or "{}")
        except (ValueError, TypeError):
            mapping = {}
        for tk in ("156", "511"):
            acc = frappe.db.get_value("Account",
                                      {"account_number": tk, "company": "DCNET"}, "name")
            if acc:
                mapping[tk] = acc
        mapping_doc.mappings = json.dumps(mapping)
        mapping_doc.total_mapped = len(mapping)
        mapping_doc.flags.ignore_permissions = True
        mapping_doc.save()
        frappe.db.commit()

        doc, _ = self._build(**{"Mã": "T7", "Tên": "ItemWithDefaults",
                                 "TK Kho": "156", "TK  Doanh thu": "511"})
        self.assertIn("item_defaults", doc)
        self.assertEqual(doc["item_defaults"][0]["company"], "DCNET")
        self.assertIn("Doanh thu", doc["item_defaults"][0].get("income_account", ""))


if __name__ == "__main__":
    unittest.main()
