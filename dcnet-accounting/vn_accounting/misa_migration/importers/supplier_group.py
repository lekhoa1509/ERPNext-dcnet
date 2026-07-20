"""Supplier Group importer — Misa Danh_sach_nhom_khach_hang_nha_cung_cap → ERPNext Supplier Group.

Same source file as Customer Group; user uploads it once tagged as
Supplier Group to get supplier group records. See customer_group.py note.
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class SupplierGroupImporter(BaseImporter):
    file_type = "Supplier Group"
    entity_type = "Supplier Group"
    target_doctype = "Supplier Group"
    column_map = {
        "_code": "Mã nhóm KH, NCC",
        "_long_name": "Tên nhóm khách hàng, nhà cung cấp",
        "_description": "Diễn giải",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        return normalized.get("_code") or normalized.get("_long_name")

    def validate(self, normalized):
        if not normalized.get("_code") and not normalized.get("_long_name"):
            return ["Thiếu cả Mã và Tên nhóm"]
        return []

    def build_doc(self, normalized):
        name = normalized.get("_code") or normalized["_long_name"]
        payload = {
            "doctype": "Supplier Group",
            "supplier_group_name": name,
            "is_group": 0,
        }
        if frappe.db.exists("Supplier Group", "All Supplier Groups"):
            payload["parent_supplier_group"] = "All Supplier Groups"
        return payload
