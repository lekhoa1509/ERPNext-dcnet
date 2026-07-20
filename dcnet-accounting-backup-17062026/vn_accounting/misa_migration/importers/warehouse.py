"""Warehouse importer — Misa Danh_sach_kho.xlsx → ERPNext Warehouse."""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class WarehouseImporter(BaseImporter):
    file_type = "Warehouse"
    entity_type = "Warehouse"
    target_doctype = "Warehouse"
    column_map = {
        "_code": "Mã kho",
        "_long_name": "Tên kho",
        "_address": "Địa chỉ",
        "_branch": "Chi nhánh",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")

    def dedupe_key(self, normalized):
        # ERPNext Warehouse autoname is "warehouse_name + - + company_abbr".
        # We can't predict the abbr cleanly here, so fall back to checking
        # whether a Warehouse with warehouse_name == Mã kho already exists.
        # The base class lookup_existing() uses frappe.db.exists which checks
        # the .name column — for Warehouse this misses our case. Override.
        return None  # handled by lookup_existing override below

    def lookup_existing(self, normalized):
        code = normalized.get("_code")
        if not code:
            return None
        # Match by warehouse_name + company instead of name
        return frappe.db.get_value(
            "Warehouse",
            {"warehouse_name": code, "company": self._company},
            "name",
        )

    def validate(self, normalized):
        if not normalized.get("_code") and not normalized.get("_long_name"):
            return ["Thiếu cả Mã kho và Tên kho"]
        if not self._company:
            return ["Batch không có Company"]
        return []

    def build_doc(self, normalized):
        return {
            "doctype": "Warehouse",
            "warehouse_name": normalized.get("_code") or normalized["_long_name"],
            "company": self._company,
            "is_group": 0,
            "disabled": 1 if (normalized.get("_status") or "").strip().lower() == "ngừng sử dụng" else 0,
        }
