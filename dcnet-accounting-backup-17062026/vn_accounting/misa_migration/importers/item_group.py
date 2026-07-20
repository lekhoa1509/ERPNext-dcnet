"""Item Group importer — Misa Danh_sach_nhom_vat_tu_hang_hoa_dich_vu → ERPNext Item Group.

v1 flat tree (parent_item_group = 'All Item Groups').
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class ItemGroupImporter(BaseImporter):
    file_type = "Item Group"
    entity_type = "Item Group"
    target_doctype = "Item Group"
    column_map = {
        "_code": "Mã nhóm vật tư, hàng hóa, dịch vụ",
        "_long_name": "Tên nhóm vật tư, hàng hóa, dịch vụ",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        return normalized.get("_code") or normalized.get("_long_name")

    def validate(self, normalized):
        if not normalized.get("_code") and not normalized.get("_long_name"):
            return ["Thiếu cả Mã và Tên nhóm"]
        return []

    def build_doc(self, normalized):
        item_group_name = normalized.get("_code") or normalized["_long_name"]
        payload = {
            "doctype": "Item Group",
            "item_group_name": item_group_name,
            "is_group": 0,
        }
        if frappe.db.exists("Item Group", "All Item Groups"):
            payload["parent_item_group"] = "All Item Groups"
        return payload
