"""UOM importer — Misa Danh_sach_don_vi_tinh.xlsx → ERPNext UOM."""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class UomImporter(BaseImporter):
    file_type = "UOM"
    entity_type = "UOM"
    target_doctype = "UOM"
    column_map = {
        "uom_name": "Đơn vị tính",
        "description": "Mô tả",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        return normalized.get("uom_name")

    def lookup_existing(self, normalized):
        uom_name = normalized.get("uom_name")
        if not uom_name:
            return None
        # UOM autoname = uom_name; guard against DuplicateEntryError on insert
        # when the UOM already exists (e.g. ERPNext defaults or prior run).
        return frappe.db.exists("UOM", uom_name) or None

    def validate(self, normalized):
        errs = []
        if not normalized.get("uom_name"):
            errs.append("Thiếu 'Đơn vị tính'")
        return errs

    def build_doc(self, normalized):
        return {
            "doctype": "UOM",
            "uom_name": normalized["uom_name"],
            "enabled": 0 if (normalized.get("_status") or "").strip().lower() == "ngừng sử dụng" else 1,
        }
