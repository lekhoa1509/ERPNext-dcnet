"""CCDC Category importer — Misa Danh_sach_loai_cong_cu_dung_cu → vn_accounting CCDC Category.

Misa cols: STT / Mã loại CCDC / Tên loại CCDC / Diễn giải / Trạng thái

CCDC Category is a custom doctype owned by vn_accounting itself
(category_name, parent_category_account, expense_account_default,
useful_period_default, is_group).
"""

from __future__ import annotations

from vn_accounting.misa_migration.importers.base import BaseImporter


class CcdcCategoryImporter(BaseImporter):
    file_type = "CCDC Category"
    entity_type = "CCDC Category"
    target_doctype = "CCDC Category"
    column_map = {
        "_code": "Mã loại CCDC",
        "_long_name": "Tên loại CCDC",
        "_desc": "Diễn giải",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        return normalized.get("_code") or normalized.get("_long_name")

    def validate(self, normalized):
        if not normalized.get("_code") and not normalized.get("_long_name"):
            return ["Thiếu cả Mã và Tên loại CCDC"]
        return []

    def build_doc(self, normalized):
        name = normalized.get("_code") or normalized["_long_name"]
        return {
            "doctype": "CCDC Category",
            "category_name": name,
            "is_group": 0,
        }
