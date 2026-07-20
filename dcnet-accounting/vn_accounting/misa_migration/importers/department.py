"""Department importer — Misa Danh_sach_co_cau_to_chuc*.xlsx → ERPNext Department.

Two source file shapes are supported:

  v1 (flat) — single sheet, columns STT / Mã đơn vị / Tên đơn vị / Địa chỉ /
              Cấp tổ chức / Trạng thái. Every row becomes a direct child of
              the "All Departments" root (no hierarchy) — original behaviour,
              kept for backward compatibility with already-parsed batches.

  v2 (theo chi nhánh) — multi-sheet workbook. parse_job._iter_department_rows
              reads every sheet except "Công ty" (the company itself already
              exists in ERPNext — not re-imported) and tags each row with a
              synthetic "_sheet" key (not a real Excel header):
                "Chi nhánh"        → branch master list, each row becomes an
                                     is_group=1 Department under the root.
                "PB - Trụ Sở HCM"  → HQ departments — parent is the root
                                     directly, NOT the "Trụ Sở HCM" branch
                                     node from the Chi nhánh sheet (HCM HQ
                                     departments sit at company level).
                "PB - CN <tên>"    → per-branch departments, parent = the
                                     matching branch's Department (resolved
                                     by Mã đơn vị at post time).
              row_index is assigned by parse_job in sheet order with
              "Chi nhánh" forced first, so by the time a branch-department
              row's post_row runs, its branch Department already exists.
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration.importers.base import BaseImporter

# Sheet name (exact, as exported) → Mã đơn vị of the branch it belongs to.
_BRANCH_SHEETS = {
    "PB - CN Hà Nội": "DCNET_HNI",
    "PB - CN Đà Nẵng": "DCNET_DNG",
    "PB - TT Công Nghệ": "TTCN",
}
_BRANCH_MASTER_SHEET = "Chi nhánh"
# HQ department sheet — parent is the company root, not a branch node, even
# though "Trụ Sở HCM" is also listed as a row in the Chi nhánh sheet.
_HQ_SHEETS = {"PB - Trụ Sở HCM"}

ROOT_DEPARTMENT = "All Departments"


class DepartmentImporter(BaseImporter):
    file_type = "Department"
    entity_type = "Department"
    target_doctype = "Department"

    def __init__(self, batch_name: str):
        super().__init__(batch_name)
        self._company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")

    # --------------------------------------------------------------- shape

    def normalize(self, raw_payload):
        # v2 sheets use different name headers per row kind ("Tên chi
        # nhánh" vs "Tên phòng ban"); v1 flat file uses "Tên đơn vị". Check
        # all three rather than a static 1:1 column_map.
        name = (
            raw_payload.get("Tên chi nhánh")
            or raw_payload.get("Tên phòng ban")
            or raw_payload.get("Tên đơn vị")
        )
        out: dict = {
            "_sheet": raw_payload.get("_sheet"),
            "_code": raw_payload.get("Mã đơn vị"),
            "_status": raw_payload.get("Trạng thái"),
        }
        if name:
            out["department_name"] = str(name).strip()
        for key in ("_code", "_status"):
            if isinstance(out.get(key), str):
                out[key] = out[key].strip() or None
        return out

    def _kind(self, normalized) -> str:
        sheet = normalized.get("_sheet")
        if sheet == _BRANCH_MASTER_SHEET:
            return "branch"
        if sheet in _BRANCH_SHEETS:
            return "branch_dept"
        # v1 flat file (no _sheet tag) and the HQ sheet both parent to root.
        return "hq_dept"

    # ------------------------------------------------------------- contract

    def dedupe_key(self, normalized):
        return None  # delegated to lookup_existing (see docstring in CostCenterImporter)

    def validate(self, normalized):
        if not normalized.get("department_name"):
            return ["Thiếu tên phòng ban/chi nhánh"]
        if not self._company:
            return ["Batch không có Company"]
        sheet = normalized.get("_sheet")
        known = {_BRANCH_MASTER_SHEET, *_BRANCH_SHEETS, *_HQ_SHEETS}
        if sheet and sheet not in known:
            return [f"Sheet '{sheet}' không xác định được cấp tổ chức (chi nhánh/phòng ban)"]
        return []

    def lookup_existing(self, normalized):
        # ERPNext Department autoname appends " - <company_abbr>" unless
        # the row IS the tree root, so a bare-code match misses the
        # suffixed row → re-insert collides with DuplicateEntryError. Try:
        #   1. Bare code (exact name match — covers pre-autoname edge cases)
        #   2. department_name field = code, scoped to this company
        #   3. name LIKE "<code> - %" (autoname suffix variant)
        code = normalized.get("_code") or normalized.get("department_name")
        if not code:
            return None
        if frappe.db.exists("Department", code):
            return code
        match = frappe.db.get_value(
            "Department", {"department_name": code, "company": self._company}, "name"
        )
        if match:
            return match
        return frappe.db.get_value(
            "Department", {"name": ("like", f"{code} - %"), "company": self._company}, "name"
        )

    def _resolve_branch_parent(self, branch_code: str) -> str | None:
        match = frappe.db.get_value(
            "Department", {"department_name": branch_code, "company": self._company}, "name"
        )
        if match:
            return match
        return frappe.db.get_value(
            "Department", {"name": ("like", f"{branch_code} - %"), "company": self._company}, "name"
        )

    def build_doc(self, normalized):
        # If a Mã đơn vị is present, use it as department_name to match
        # the lookup_existing key (so doc.name == Misa Mã before suffixing).
        name = normalized.get("_code") or normalized["department_name"]
        kind = self._kind(normalized)
        payload = {
            "doctype": "Department",
            "department_name": name,
            "company": self._company,
            "is_group": 1 if kind == "branch" else 0,
            "disabled": 1 if (normalized.get("_status") or "").strip().lower() == "ngừng sử dụng" else 0,
        }
        if kind == "branch_dept":
            branch_code = _BRANCH_SHEETS[normalized["_sheet"]]
            parent = self._resolve_branch_parent(branch_code)
            if not parent:
                frappe.throw(
                    f"Chưa import Chi nhánh '{branch_code}' — hãy đảm bảo sheet "
                    f"'{_BRANCH_MASTER_SHEET}' được post trước phòng ban của chi nhánh này."
                )
            payload["parent_department"] = parent
        elif frappe.db.exists("Department", ROOT_DEPARTMENT):
            payload["parent_department"] = ROOT_DEPARTMENT
        return payload
