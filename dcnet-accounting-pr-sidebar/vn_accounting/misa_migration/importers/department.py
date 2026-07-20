"""Department importer — Misa Danh_sach_co_cau_to_chuc.xlsx → ERPNext Department.

Misa columns: STT / Mã đơn vị / Tên đơn vị / Địa chỉ / Cấp tổ chức / Trạng thái
v1: flat tree (parent_department = 'All Departments' root). Phase E or later
will reconstruct hierarchy from 'Cấp tổ chức' levels.
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class DepartmentImporter(BaseImporter):
    file_type = "Department"
    entity_type = "Department"
    target_doctype = "Department"
    column_map = {
        "department_name": "Tên đơn vị",
        "_code": "Mã đơn vị",
        "_address": "Địa chỉ",
        "_level": "Cấp tổ chức",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        # ERPNext Department.name = department_name (autoname). For tenancy
        # collision avoidance, prefer Misa Mã đơn vị when present.
        return normalized.get("_code") or normalized.get("department_name")

    def validate(self, normalized):
        if not normalized.get("department_name"):
            return ["Thiếu 'Tên đơn vị'"]
        return []

    def lookup_existing(self, normalized):
        # ERPNext Department uses autoname `field:department_name` AND
        # appends company abbreviation suffix (e.g. "KT_HCM" inserted by
        # a prior run becomes "KT_HCM - DC"). The bare `_code` lookup
        # misses the suffixed row → re-insert collides with
        # DuplicateEntryError. Try three variants in order:
        #   1. Bare code (exact name match)
        #   2. department_name field = code
        #   3. name LIKE "<code> - %" (autoname suffix variant)
        code = normalized.get("_code") or normalized.get("department_name")
        if not code:
            return None
        if frappe.db.exists("Department", code):
            return code
        match = frappe.db.get_value(
            "Department", {"department_name": code}, "name"
        )
        if match:
            return match
        match = frappe.db.get_value(
            "Department", {"name": ("like", f"{code} - %")}, "name"
        )
        return match

    def build_doc(self, normalized):
        # If a Mã đơn vị is present, use it as department_name to match
        # the dedupe_key (so doc.name == Misa Mã).
        name = normalized.get("_code") or normalized["department_name"]
        payload = {
            "doctype": "Department",
            "department_name": name,
            "is_group": 0,
        }
        # parent_department defaults to All Departments root if it exists
        if frappe.db.exists("Department", "All Departments"):
            payload["parent_department"] = "All Departments"
        return payload
