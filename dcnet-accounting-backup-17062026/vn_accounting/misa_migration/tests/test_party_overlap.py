"""Tests for party_overlap detection."""

from __future__ import annotations

import json
import unittest

import frappe

from vn_accounting.misa_migration.importers.party_overlap import (
    _extract_code, detect_overlap,
)


class TestPartyOverlap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = frappe.get_doc({
            "doctype": "Misa Migration Batch",
            "company": "DCNET",
            "batch_title": "_TEST_OVERLAP_",
            "status": "DRAFT",
        }).insert(ignore_permissions=True)

        # Seed 3 customer rows + 3 supplier rows; 2 overlap (1986, 20SECTIONS)
        def _row(file_type, payload):
            frappe.get_doc({
                "doctype": "Misa Migration Row",
                "batch": cls.batch.name,
                "file_type": file_type,
                "entity_type": file_type,
                "status": "New",
                "raw_payload": json.dumps(payload, ensure_ascii=False),
            }).insert(ignore_permissions=True)

        _row("Customer", {"Mã khách hàng": "1986", "Tên khách hàng": "1986 KH"})
        _row("Customer", {"Mã khách hàng": "20SECTIONS", "Tên khách hàng": "20S"})
        _row("Customer", {"Mã khách hàng": "ONLY_C", "Tên khách hàng": "Only Customer"})
        _row("Supplier", {"Mã nhà cung cấp": "1986", "Tên nhà cung cấp": "1986 NCC"})
        _row("Supplier", {"Mã nhà cung cấp": "20SECTIONS", "Tên nhà cung cấp": "20S NCC"})
        _row("Supplier", {"Mã nhà cung cấp": "ONLY_S", "Tên nhà cung cấp": "Only Supplier"})
        frappe.db.commit()

    @classmethod
    def tearDownClass(cls):
        frappe.db.sql("DELETE FROM `tabMisa Migration Row` WHERE batch=%s", (cls.batch.name,))
        frappe.db.set_value("Misa Migration Batch", cls.batch.name, "status",
                            "REVERSED", update_modified=False)
        frappe.delete_doc("Misa Migration Batch", cls.batch.name, force=True, ignore_permissions=True)
        frappe.db.commit()

    def test_extract_code_basic(self):
        self.assertEqual(_extract_code(json.dumps({"Mã khách hàng": "X"}), "Mã khách hàng"), "X")

    def test_extract_code_strip(self):
        self.assertEqual(_extract_code(json.dumps({"K": " X "}), "K"), "X")

    def test_extract_code_none(self):
        self.assertIsNone(_extract_code(None, "K"))
        self.assertIsNone(_extract_code("", "K"))
        self.assertIsNone(_extract_code("not json", "K"))
        self.assertIsNone(_extract_code(json.dumps({}), "K"))

    def test_detect_overlap_counts(self):
        r = detect_overlap(self.batch.name)
        self.assertEqual(r["total_customers"], 3)
        self.assertEqual(r["total_suppliers"], 3)
        self.assertEqual(r["total_overlap"], 2)
        self.assertEqual(r["overlapping_codes"], ["1986", "20SECTIONS"])
        self.assertEqual(r["customer_only"], ["ONLY_C"])
        self.assertEqual(r["supplier_only"], ["ONLY_S"])


if __name__ == "__main__":
    unittest.main()
