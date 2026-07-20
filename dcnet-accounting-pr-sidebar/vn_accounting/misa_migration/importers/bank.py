"""Bank importer — Misa Danh_sach_ngan_hang.xlsx → ERPNext Bank entity.

Misa columns: STT / Tên viết tắt / Tên đầy đủ / Trạng thái
Use short name (Tên viết tắt) as ERPNext Bank.name (concise + searchable).
Long name (Tên đầy đủ) → bank_name display field.
"""

from __future__ import annotations

from vn_accounting.misa_migration.importers.base import BaseImporter


class BankImporter(BaseImporter):
    file_type = "Bank"
    entity_type = "Bank"
    target_doctype = "Bank"
    column_map = {
        "short_name": "Tên viết tắt",
        "long_name": "Tên đầy đủ",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        return normalized.get("short_name") or normalized.get("long_name")

    def validate(self, normalized):
        if not normalized.get("short_name") and not normalized.get("long_name"):
            return ["Thiếu cả Tên viết tắt và Tên đầy đủ"]
        return []

    def build_doc(self, normalized):
        # ERPNext Bank: autoname is `bank_name`. We set bank_name = short_name
        # (used as doc.name) so the long name remains searchable in description.
        bank_name = normalized.get("short_name") or normalized.get("long_name")
        return {
            "doctype": "Bank",
            "bank_name": bank_name,
        }
