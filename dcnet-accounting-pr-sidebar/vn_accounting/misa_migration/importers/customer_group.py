"""Customer Group importer — Misa Danh_sach_nhom_khach_hang_nha_cung_cap → ERPNext Customer Group.

Note: Misa's KH+NCC group file mixes group rows and individual party rows.
Phase B imports ALL rows as Customer Group. User reviews + skips non-groups.
Phase C importers will then create actual Customer/Supplier records, with
group linkage via Mã.
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class CustomerGroupImporter(BaseImporter):
    file_type = "Customer Group"
    entity_type = "Customer Group"
    target_doctype = "Customer Group"
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
            "doctype": "Customer Group",
            "customer_group_name": name,
            "is_group": 0,
        }
        if frappe.db.exists("Customer Group", "All Customer Groups"):
            payload["parent_customer_group"] = "All Customer Groups"
        return payload
