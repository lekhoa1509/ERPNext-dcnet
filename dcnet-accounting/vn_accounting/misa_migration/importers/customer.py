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
import re
import unicodedata
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
        # Load all Customer Group names for fast in-memory conflict check.
        # Normalize to NFC + lowercase so Python comparison matches MySQL's
        # utf8mb4_unicode_ci collation (which normalizes Unicode internally).
        # Without NFC normalization, NFC names from DB vs NFD names from Excel
        # look identical but are byte-different → Python set misses the match.
        self._cg_names: set[str] = set(
            unicodedata.normalize("NFC", n).strip().lower()
            for n in frappe.db.sql_list("SELECT name FROM `tabCustomer Group`")
        )

    def dedupe_key(self, normalized):
        return normalized.get("_code")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_code"):
            errs.append("Thiếu 'Mã khách hàng'")
        if not normalized.get("_name"):
            errs.append("Thiếu 'Tên khách hàng'")
        return errs

    def _safe_customer_name(self, name: str, code: str) -> str:
        """Return a customer_name guaranteed not to collide with any Customer Group.

        Uses NFC-normalized comparison (same as MySQL utf8mb4_unicode_ci) so
        names from Excel (may be NFD) are correctly matched against DB names (NFC).
        Tries: original → "name (code)" → "name (code) 2" → … until unique.
        """
        def _key(s: str) -> str:
            return unicodedata.normalize("NFC", s).strip().lower()

        candidates = [
            name,
            f"{name} ({code})"[:140],
            f"{name} ({code}) 2"[:140],
            f"{name} ({code}) 3"[:140],
        ]
        for c in candidates:
            if _key(c) not in self._cg_names:
                return c
        return f"{name[:100]} ({code})"[:140]

    def _clean_phone(self, raw: str | None) -> str | None:
        """Take first number when Misa stores multiple phones as '0912/0913' or '0912 / 0913'."""
        if not raw:
            return None
        first = re.split(r"\s*/\s*|\s*;\s*", raw.strip())[0].strip()
        # Strip non-digit/non-+ chars (e.g. trailing "CK" note)
        cleaned = re.sub(r"[^\d+]", "", first)
        return cleaned or None

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

        # ERPNext forbids customer_name == any Customer Group name.
        # Use in-memory set for reliable conflict check (frappe.db.exists can
        # miss matches due to Unicode normalization at validate() time).
        customer_name = self._safe_customer_name(
            (normalized["_name"] or code)[:140], code
        )

        payload = {
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_group": self._resolve_customer_group(normalized.get("_group")),
            "territory": "All Territories" if frappe.db.exists("Territory", "All Territories") else (
                frappe.db.get_value("Territory", {"is_group": 0}, "name")
            ),
            "customer_type": customer_type,
            "tax_id": tax_id or None,
            # Misa may store multiple phones as '0912/0913' — take only the first.
            "mobile_no": self._clean_phone(normalized.get("_mobile")),
            # Frappe Customer has no top-level 'phone' field — use mobile_no
            # OR ship a contact later. Phase C v1 captures into mobile only.
            "misa_party_code": code,  # custom field (Phase A C3)
        }
        # Strip None values; Frappe is OK with missing optional fields
        return {k: v for k, v in payload.items() if v is not None}

    def lookup_existing(self, normalized):
        code = normalized.get("_code")
        if not code:
            return None
        return frappe.db.exists("Customer", code) or None

    def _insert_customer(self, payload: dict, code: str) -> object:
        """Insert Customer doc; returns doc on success, None if already exists.

        build_doc guarantees customer_name is conflict-free via _safe_customer_name,
        so only DuplicateEntry (customer already in DB from prior run) needs handling.
        """
        savepoint = "misa_customer_insert"
        frappe.db.savepoint(savepoint)
        doc = frappe.get_doc(payload)
        try:
            doc.insert(ignore_permissions=True, set_name=code)
            return doc
        except Exception as exc:
            # Isolate a failed row without rolling back Customers already
            # imported earlier in the same file-type transaction.
            frappe.db.rollback(save_point=savepoint)
            s = str(exc)
            if "Duplicate entry" in s or type(exc).__name__ == "DuplicateEntryError":
                return None  # already exists — treat as Exists
            if "Customer Group" in s or "same name" in s:
                # _safe_customer_name should have prevented this (Unicode NFC fix),
                # but if it still fires: find a unique name via MySQL-level
                # frappe.db.exists checks (respects utf8mb4_unicode_ci collation),
                # then retry.
                if frappe.db.exists("Customer", code):
                    return None
                base = payload.get("customer_name", code)
                for suffix in (f" ({code})", f" ({code}) 2", f" ({code}) 3", f"-KH"):
                    candidate = f"{base}{suffix}"[:140]
                    if not frappe.db.exists("Customer Group", candidate):
                        payload["customer_name"] = candidate
                        break
                doc2 = frappe.get_doc(payload)
                try:
                    doc2.insert(ignore_permissions=True, set_name=code)
                    return doc2
                except Exception as exc2:
                    frappe.db.rollback(save_point=savepoint)
                    s2 = str(exc2)
                    if "Duplicate entry" in s2:
                        return None
                    raise
            raise

    # Override post_row to set doc.name = Misa Mã before insert
    def post_row(self, row_doc):
        if row_doc.status != "Ready":
            return row_doc.status
        try:
            normalized = json.loads(row_doc.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}
        try:
            code = normalized.get("_code")
            # Idempotency: re-check before insert (preview may have run before
            # a prior post created this record in the same or a previous run).
            existing = self.lookup_existing(normalized)
            if existing:
                self._mark(row_doc, "Exists", None, normalized, target_name=existing)
                self.counts["exists"] += 1
                return "Exists"
            payload = self.build_doc(normalized)
            doc = self._insert_customer(payload, code)
            if doc is None:
                # _insert_customer signals "already exists"
                self._mark(row_doc, "Exists", None, normalized, target_name=code)
                self.counts["exists"] += 1
                return "Exists"
            self._mark(row_doc, "Posted", None, normalized, target_name=doc.name)
            self.counts["posted"] += 1
            return "Posted"
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            frappe.log_error(title="Misa Migration Customer create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"
