"""Project importer — Misa Danh_sach_cong_trinh → ERPNext Project.

Misa cols: STT / Mã công trình / Tên công trình / Loại công trình /
           Tình trạng / Ngày bắt đầu / Ngày kết thúc / Dự toán /
           Chủ đầu tư / Chi nhánh / Trạng thái

ERPNext Project autoname = naming_series 'PROJ-.YYYY.-' by default. We
override to Misa Mã công trình via post-build doc.name set so spec §15
(doc.name = Misa code) holds.
"""

from __future__ import annotations

from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class ProjectImporter(BaseImporter):
    file_type = "Project"
    entity_type = "Project"
    target_doctype = "Project"
    column_map = {
        "_code": "Mã công trình",
        "_long_name": "Tên công trình",
        "_kind": "Loại công trình",
        "_state": "Tình trạng",
        "_start": "Ngày bắt đầu",
        "_end": "Ngày kết thúc",
        "_budget": "Dự toán",
        "_owner": "Chủ đầu tư",
        "_status": "Trạng thái",
    }

    def dedupe_key(self, normalized):
        return normalized.get("_code")

    def validate(self, normalized):
        if not normalized.get("_code"):
            return ["Thiếu 'Mã công trình' — required cho dedupe + name"]
        if not normalized.get("_long_name"):
            return ["Thiếu 'Tên công trình'"]
        return []

    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "doctype": "Project",
            "project_name": normalized["_long_name"],
            "status": "Open",
        }
        # ERPNext Project has VN-accounting extension fields
        if normalized.get("_kind"):
            payload["vn_construction_phase"] = normalized["_kind"]
        if normalized.get("_start"):
            payload["expected_start_date"] = str(normalized["_start"])[:10]
        if normalized.get("_end"):
            payload["expected_end_date"] = str(normalized["_end"])[:10]
        if normalized.get("_budget"):
            try:
                payload["estimated_costing"] = float(normalized["_budget"])
            except (TypeError, ValueError):
                pass
        return payload

    # Override post_row to set doc.name = Misa Mã before insert (bypass
    # naming_series). Project doesn't have a direct field-based autoname,
    # so we use the `name` kwarg trick.
    def post_row(self, row_doc):
        import json as _json
        if row_doc.status != "Ready":
            return row_doc.status
        try:
            normalized = _json.loads(row_doc.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}
        try:
            payload = self.build_doc(normalized)
            code = normalized.get("_code")
            doc = frappe.get_doc(payload)
            if code:
                doc.name = code
                doc.flags.name_set = True  # signal naming layer
            doc.insert(ignore_permissions=True, set_name=code if code else None)
            self._mark(row_doc, "Posted", None, normalized, target_name=doc.name)
            self.counts["posted"] += 1
            return "Posted"
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            frappe.log_error(title="Misa Migration Project create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"
