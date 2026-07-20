"""Employee importer — Misa Danh_sach_nhan_vien → ERPNext Employee.

Misa cols (10): STT / Mã nhân viên / Tên nhân viên / Chức danh /
  Trạng thái người dùng / Tên đơn vị / Số tài khoản / Tên ngân hàng /
  Trạng thái / Là danh mục tập đoàn

ERPNext Employee required fields: naming_series, first_name, gender,
date_of_birth, date_of_joining, status, company. Misa provides employee
code + full name + department + designation. Phase C v1 uses sensible
defaults for missing fields (gender='Prefer not to say', DOB=2000-01-01,
date_of_joining=today). User can correct in Employee form post-import.

Per spec §15.4 doc.name = Misa Mã nhân viên via post_row set_name.
"""

from __future__ import annotations

import json
from typing import Any

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter


class EmployeeImporter(BaseImporter):
    file_type = "Employee"
    entity_type = "Employee"
    target_doctype = "Employee"
    column_map = {
        "_code": "Mã nhân viên",
        "_name": "Tên nhân viên",
        "_designation": "Chức danh",
        "_dept_name": "Tên đơn vị",
        "_bank_acc": "Số tài khoản",
        "_bank_name": "Tên ngân hàng",
        "_status": "Trạng thái",
    }

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")

    def dedupe_key(self, normalized):
        return normalized.get("_code")

    def validate(self, normalized):
        errs = []
        if not normalized.get("_code"):
            errs.append("Thiếu 'Mã nhân viên'")
        if not normalized.get("_name"):
            errs.append("Thiếu 'Tên nhân viên'")
        if not self._company:
            errs.append("Batch không có Company")
        return errs

    def lookup_existing(self, normalized):
        code = normalized.get("_code")
        if not code:
            return None
        # Employee may have name = naming series (HR-EMP-...) or = code via set_name
        return frappe.db.exists("Employee", code)

    def _split_name(self, full_name: str) -> tuple[str, str]:
        """VN convention: first word = first_name, rest = last_name? Reversed.

        Actually in VN, order is FAMILY-then-given (e.g. 'PHẠM NGỌC ĐANG' —
        Phạm=family, Ngọc=middle, Đang=given). ERPNext first_name expects
        the given name, last_name the family. Conservative: put given name
        (last token) as first_name, prepend rest as last_name.
        """
        parts = (full_name or "").strip().split()
        if not parts:
            return ("Unknown", "")
        if len(parts) == 1:
            return (parts[0], "")
        return (parts[-1], " ".join(parts[:-1]))

    def _resolve_department(self, dept_name: str | None) -> str | None:
        if not dept_name:
            return None
        # Misa stores Tên đơn vị (e.g. 'PHÒNG KỸ THUẬT HẠ TẦNG') —
        # Department importer Phase B used Mã as department_name when present,
        # else Tên. Try both.
        if frappe.db.exists("Department", dept_name):
            return dept_name
        # Try matching by department_name field
        return frappe.db.get_value("Department", {"department_name": dept_name}, "name")

    def _ensure_designation(self, name: str | None) -> str | None:
        """Misa exports designation as a free-text Chức danh; ERPNext
        requires it to be a Designation link. Auto-create the row if
        missing — best practice, but Misa export can have 30+ distinct
        Vietnamese titles that ERPNext doesn't ship templates for.
        """
        if not name:
            return None
        name = str(name).strip()
        if not name:
            return None
        if frappe.db.exists("Designation", name):
            return name
        try:
            d = frappe.get_doc({
                "doctype": "Designation",
                "designation_name": name[:140],
            })
            d.flags.ignore_permissions = True
            d.insert()
            frappe.db.commit()  # commit so re-lookup in same loop succeeds
            return d.name
        except Exception:
            # If insert fails (rare — duplicate race, invalid chars),
            # drop the field rather than blocking employee insert.
            return None

    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        code = normalized["_code"]
        full_name = normalized["_name"]
        first_name, last_name = self._split_name(full_name)
        misa_status = (normalized.get("_status") or "").strip().lower()
        status = "Left" if misa_status == "ngừng sử dụng" else "Active"

        payload = {
            "doctype": "Employee",
            "employee": code,  # external employee ID; also dedupe key
            "first_name": first_name[:140],
            "last_name": last_name[:140] or None,
            "employee_name": full_name[:140],
            "gender": "Prefer not to say",  # required field — user can correct
            "date_of_birth": "2000-01-01",  # placeholder — user corrects
            "date_of_joining": frappe.utils.today(),
            "status": status,
            "company": self._company,
            "designation": self._ensure_designation(normalized.get("_designation")),
            "department": self._resolve_department(normalized.get("_dept_name")),
        }
        # ERPNext requires relieving_date when status='Left'. Misa export
        # doesn't carry it — use today() as placeholder so insert validates;
        # operator corrects later if needed.
        if status == "Left":
            payload["relieving_date"] = frappe.utils.today()
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
            frappe.log_error(title="Misa Migration Employee create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"
