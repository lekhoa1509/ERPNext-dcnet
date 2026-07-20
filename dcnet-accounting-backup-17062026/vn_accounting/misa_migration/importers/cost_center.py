"""Cost Center importer — Misa Doi_tuong_tap_hop_chi_phi → ERPNext Cost Center.

Misa cols: STT / Mã đối tượng THCP / Tên đối tượng THCP / Loại / Diễn giải /
           Chi nhánh / Trạng thái
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class CostCenterImporter(BaseImporter):
    file_type = "Cost Center"
    entity_type = "Cost Center"
    target_doctype = "Cost Center"
    column_map = {
        "_code": "Mã đối tượng THCP",
        "_long_name": "Tên đối tượng THCP",
        "_kind": "Loại",
        "_desc": "Diễn giải",
        "_branch": "Chi nhánh",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
        self._root_parent = _find_root_cost_center(self._company) if self._company else None

    def dedupe_key(self, normalized):
        return None  # delegated to lookup_existing override

    def lookup_existing(self, normalized):
        code = normalized.get("_code")
        if not code:
            return None
        return frappe.db.get_value(
            "Cost Center",
            {"cost_center_name": code, "company": self._company},
            "name",
        )

    def validate(self, normalized):
        if not normalized.get("_code") and not normalized.get("_long_name"):
            return ["Thiếu Mã và Tên Cost Center"]
        if not self._company:
            return ["Batch không có Company"]
        return []

    def build_doc(self, normalized):
        doc = {
            "doctype": "Cost Center",
            "cost_center_name": normalized.get("_code") or normalized["_long_name"],
            "company": self._company,
            "is_group": 0,
            "disabled": 1 if (normalized.get("_status") or "").strip().lower() == "ngừng sử dụng" else 0,
        }
        # Misa Doi_tuong_tap_hop_chi_phi file is flat — no parent column.
        # ERPNext requires every non-root Cost Center to have a parent.
        # Default to the company's root group; operator can re-parent in
        # the UI after import. Surfaces in preflight as an auto-correction.
        if self._root_parent:
            doc["parent_cost_center"] = self._root_parent
        return doc


def _find_root_cost_center(company: str) -> str | None:
    """Find the company's root (is_group=1, no parent) Cost Center.

    Each ERPNext Company auto-creates a single root Cost Center on Company
    insert (e.g. 'DCNET TEST - DCT'). Returns its name or None.
    """
    if not company:
        return None
    root = frappe.db.sql(
        """SELECT name FROM `tabCost Center`
           WHERE company=%s AND is_group=1
             AND (parent_cost_center IS NULL OR parent_cost_center='')
           ORDER BY lft ASC LIMIT 1""",
        (company,),
    )
    return root[0][0] if root else None
