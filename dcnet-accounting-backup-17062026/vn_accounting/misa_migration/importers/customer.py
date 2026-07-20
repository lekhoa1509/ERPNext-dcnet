"""Customer importer — Misa Danh_sach_khach_hang → ERPNext Customer.

Misa cols (13):
  STT / Mã khách hàng / Tên khách hàng / Địa chỉ / Diễn giải / Công nợ /
  Nhóm KH, NCC / Mã số thuế/CCCD chủ hộ / Mã số ĐVQHNS / Số hộ chiếu /
  Điện thoại / ĐT di động NLH / Là Đối tượng nội bộ

Per spec §15.4: doc.name = Misa Mã khách hàng (e.g. '1986', '20SECTIONS').
ERPNext Customer autoname is naming_series 'CUST-.YYYY.-.#####'; override
via post_row set_name like Project importer.

Nhóm KH, NCC is multi-value with ';' separator (e.g. 'NCC;CN_HANOI');
take the first matching Customer Group, else fall back to root.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class CustomerImporter(BaseImporter):
    file_type = "Customer"
    entity_type = "Customer"
    target_doctype = "Customer"
    column_map = {
        "_code": "Mã khách hàng",
        "_name": "Tên khách hàng",
        "_address": "Địa chỉ",
        "_desc": "Diễn giải",
        "_group": "Nhóm KH, NCC",
        "_tax_id": "Mã số thuế/CCCD chủ hộ",
        "_phone": "Điện thoại",
        "_mobile": "ĐT di động NLH",
        "_internal": "Là Đối tượng nội bộ",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._default_group = None
        for cg in ("All Customer Groups", "Commercial", "Individual"):
            if frappe.db.exists("Customer Group", cg):
                self._default_group = cg
                break

    def dedupe_key(self, normalized):
        return normalized.get("_code")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_code"):
            errs.append("Thiếu 'Mã khách hàng'")
        if not normalized.get("_name"):
            errs.append("Thiếu 'Tên khách hàng'")
        return errs

    def _resolve_customer_group(self, ngrop: str | None) -> str:
        """Misa 'Nhóm KH, NCC' may be 'NCC;CN_HANOI'. Pick first matching."""
        if not ngrop:
            return self._default_group or "Commercial"
        for raw in str(ngrop).split(";"):
            raw = raw.strip()
            if raw and frappe.db.exists("Customer Group", raw):
                return raw
        return self._default_group or "Commercial"

    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        code = normalized["_code"]
        # customer_type: Individual if tax_id is short (CCCD/CMND ~12 digits)
        # OR has no tax_id; Company if tax_id is MST (10-13 digits, may have -).
        tax_id = (normalized.get("_tax_id") or "").strip()
        customer_type = "Company"
        if tax_id and len(tax_id.replace("-", "").replace(" ", "")) <= 13:
            # Most VN entities: 10-digit MST = Company, 12-digit CCCD = Individual.
            # Misa column mixes both — heuristic: if 12 digits no dash → Individual.
            digits = "".join(c for c in tax_id if c.isdigit())
            if len(digits) == 12 and "-" not in tax_id:
                customer_type = "Individual"

        payload = {
            "doctype": "Customer",
            "customer_name": (normalized["_name"] or code)[:140],
            "customer_group": self._resolve_customer_group(normalized.get("_group")),
            "territory": "All Territories" if frappe.db.exists("Territory", "All Territories") else (
                frappe.db.get_value("Territory", {"is_group": 0}, "name")
            ),
            "customer_type": customer_type,
            "tax_id": tax_id or None,
            "mobile_no": (normalized.get("_mobile") or "").strip() or None,
            # Frappe Customer has no top-level 'phone' field — use mobile_no
            # OR ship a contact later. Phase C v1 captures into mobile only.
            "misa_party_code": code,  # custom field (Phase A C3)
        }
        # Strip None values; Frappe is OK with missing optional fields
        return {k: v for k, v in payload.items() if v is not None}

    # Override post_row to set doc.name = Misa Mã before insert
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
            frappe.log_error(title="Misa Migration Customer create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"
