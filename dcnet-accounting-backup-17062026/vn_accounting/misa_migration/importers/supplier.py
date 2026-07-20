"""Supplier importer — Misa Danh_sach_nha_cung_cap → ERPNext Supplier.

Misa cols (15): STT / Mã nhà cung cấp / Tên nhà cung cấp / Địa chỉ /
  Diễn giải / Số tiền nợ / Nhóm KH, NCC / Mã số thuế/CCCD chủ hộ /
  Mã số ĐVQHNS / Số hộ chiếu / Rủi ro về hóa đơn / Văn bản tham chiếu /
  Điện thoại / Là Đối tượng nội bộ / Là Tổng công ty/chi nhánh

Mirror of CustomerImporter: dedupe by Mã, doc.name = Mã via set_name,
multi-value 'Nhóm KH, NCC' → first matching Supplier Group + fallback.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class SupplierImporter(BaseImporter):
    file_type = "Supplier"
    entity_type = "Supplier"
    target_doctype = "Supplier"
    column_map = {
        "_code": "Mã nhà cung cấp",
        "_name": "Tên nhà cung cấp",
        "_address": "Địa chỉ",
        "_desc": "Diễn giải",
        "_group": "Nhóm KH, NCC",
        "_tax_id": "Mã số thuế/CCCD chủ hộ",
        "_phone": "Điện thoại",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._default_group = None
        for sg in ("All Supplier Groups", "Local", "Distributor"):
            if frappe.db.exists("Supplier Group", sg):
                self._default_group = sg
                break

    def dedupe_key(self, normalized):
        return normalized.get("_code")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_code"):
            errs.append("Thiếu 'Mã nhà cung cấp'")
        if not normalized.get("_name"):
            errs.append("Thiếu 'Tên nhà cung cấp'")
        return errs

    def _resolve_supplier_group(self, ngrop: str | None) -> str:
        if not ngrop:
            return self._default_group or "Local"
        for raw in str(ngrop).split(";"):
            raw = raw.strip()
            if raw and frappe.db.exists("Supplier Group", raw):
                return raw
        return self._default_group or "Local"

    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        code = normalized["_code"]
        tax_id = (normalized.get("_tax_id") or "").strip()
        supplier_type = "Company"
        if tax_id:
            digits = "".join(c for c in tax_id if c.isdigit())
            if len(digits) == 12 and "-" not in tax_id:
                supplier_type = "Individual"

        payload = {
            "doctype": "Supplier",
            "supplier_name": (normalized["_name"] or code)[:140],
            "supplier_group": self._resolve_supplier_group(normalized.get("_group")),
            "supplier_type": supplier_type,
            "tax_id": tax_id or None,
            "misa_party_code": code,
        }
        return {k: v for k, v in payload.items() if v is not None}

    def post_row(self, row_doc):
        if row_doc.status != "Ready":
            return row_doc.status
        try:
            normalized = json.loads(row_doc.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}
        try:
            payload = self.build_doc(normalized)
            code = normalized.get("_code")
            doc = frappe.get_doc(payload)
            doc.insert(ignore_permissions=True, set_name=code)
            self._mark(row_doc, "Posted", None, normalized, target_name=doc.name)
            self.counts["posted"] += 1
            return "Posted"
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            frappe.log_error(title="Misa Migration Supplier create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"
