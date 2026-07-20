"""Tests for BaseImporter ABC — uses a stub subclass against ERPNext UOM."""

from __future__ import annotations

import json
import unittest

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class _StubUomImporter(BaseImporter):
    """Minimal subclass for testing — UOM has no required fields beyond name."""
    file_type = "UOM"
    entity_type = "UOM"
    target_doctype = "UOM"
    column_map = {"uom_name": "Tên đơn vị tính"}

    def dedupe_key(self, normalized):
        return normalized.get("uom_name")

    def validate(self, normalized):
        errs = []
        if not normalized.get("uom_name"):
            errs.append("Tên đơn vị tính trống")
        return errs

    def build_doc(self, normalized):
        return {"doctype": "UOM", "uom_name": normalized["uom_name"]}


class TestBaseImporter(unittest.TestCase):
    """Pure-Python tests; no migration of test fixtures needed."""

    @classmethod
    def setUpClass(cls):
        cls.batch = frappe.get_doc({
            "doctype": "Misa Migration Batch",
            "company": "DCNET",
            "batch_title": "_TEST_BASEIMPORTER_",
            "status": "DRAFT",
        }).insert(ignore_permissions=True)
        cls.importer = _StubUomImporter(cls.batch.name)
        cls.test_uom_names = []

    @classmethod
    def tearDownClass(cls):
        # cleanup created UOMs
        for name in cls.test_uom_names:
            if frappe.db.exists("UOM", name):
                try:
                    frappe.delete_doc("UOM", name, force=True, ignore_permissions=True)
                except Exception:
                    pass
        # cleanup rows + batch
        for r in frappe.get_all("Misa Migration Row", filters={"batch": cls.batch.name}, pluck="name"):
            frappe.delete_doc("Misa Migration Row", r, force=True, ignore_permissions=True)
        frappe.db.set_value("Misa Migration Batch", cls.batch.name, "status", "REVERSED", update_modified=False)
        frappe.delete_doc("Misa Migration Batch", cls.batch.name, force=True, ignore_permissions=True)
        frappe.db.commit()

    def _make_row(self, raw_payload):
        row = frappe.get_doc({
            "doctype": "Misa Migration Row",
            "batch": self.batch.name,
            "file_type": "UOM",
            "entity_type": "UOM",
            "status": "New",
            "raw_payload": json.dumps(raw_payload, ensure_ascii=False),
        }).insert(ignore_permissions=True)
        return row

    def test_normalize_strips_whitespace(self):
        out = self.importer.normalize({"Tên đơn vị tính": "  Cái  ", "Mã": "ignored"})
        self.assertEqual(out, {"uom_name": "Cái"})

    def test_normalize_skips_empty(self):
        out = self.importer.normalize({"Tên đơn vị tính": "   "})
        self.assertEqual(out, {})

    def test_preview_invalid_when_empty(self):
        row = self._make_row({"Tên đơn vị tính": ""})
        status = self.importer.preview_row(row)
        self.assertEqual(status, "Invalid")
        row.reload()
        self.assertIn("trống", row.error_message)

    def test_preview_ready_when_new(self):
        unique = "_TEST_UOM_NEW_42_"
        self.test_uom_names.append(unique)
        if frappe.db.exists("UOM", unique):
            frappe.delete_doc("UOM", unique, force=True, ignore_permissions=True)
        row = self._make_row({"Tên đơn vị tính": unique})
        status = self.importer.preview_row(row)
        self.assertEqual(status, "Ready")

    def test_preview_exists_when_uom_already_in_db(self):
        unique = "_TEST_UOM_EXISTING_42_"
        self.test_uom_names.append(unique)
        if not frappe.db.exists("UOM", unique):
            frappe.get_doc({"doctype": "UOM", "uom_name": unique}).insert(ignore_permissions=True)
        row = self._make_row({"Tên đơn vị tính": unique})
        status = self.importer.preview_row(row)
        self.assertEqual(status, "Exists")
        row.reload()
        self.assertEqual(row.target_name, unique)

    def test_post_creates_doc(self):
        unique = "_TEST_UOM_POST_42_"
        self.test_uom_names.append(unique)
        if frappe.db.exists("UOM", unique):
            frappe.delete_doc("UOM", unique, force=True, ignore_permissions=True)
        row = self._make_row({"Tên đơn vị tính": unique})
        self.importer.preview_row(row)
        status = self.importer.post_row(row)
        self.assertEqual(status, "Posted")
        self.assertTrue(frappe.db.exists("UOM", unique))

    def test_undo_deletes_created_doc(self):
        unique = "_TEST_UOM_UNDO_42_"
        self.test_uom_names.append(unique)
        if frappe.db.exists("UOM", unique):
            frappe.delete_doc("UOM", unique, force=True, ignore_permissions=True)
        row = self._make_row({"Tên đơn vị tính": unique})
        self.importer.preview_row(row)
        self.importer.post_row(row)
        self.assertTrue(frappe.db.exists("UOM", unique))
        status = self.importer.undo_row(row)
        self.assertEqual(status, "Reversed")
        self.assertFalse(frappe.db.exists("UOM", unique))

    def test_counts_accumulate(self):
        unique_a = "_TEST_UOM_COUNT_A_"
        unique_b = "_TEST_UOM_COUNT_B_"
        for n in (unique_a, unique_b):
            self.test_uom_names.append(n)
            if frappe.db.exists("UOM", n):
                frappe.delete_doc("UOM", n, force=True, ignore_permissions=True)
        local = _StubUomImporter(self.batch.name)
        for n in (unique_a, unique_b):
            row = self._make_row({"Tên đơn vị tính": n})
            local.preview_row(row)
            local.post_row(row)
        self.assertEqual(local.counts["posted"], 2)
        self.assertEqual(local.counts["ready"], 2)


if __name__ == "__main__":
    unittest.main()
