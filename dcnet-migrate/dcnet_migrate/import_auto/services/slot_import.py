"""Fixed master-data slots for Import Auto.

Import Auto used to scan a whole folder and let the AI classify every file
it found — including many files that have no ERPNext mapping at all (Misa
internal categories, accounting/balance files owned by Opening Balance
Import). That produced a lot of noise ("lỗi linh tinh").

This module gives each master-data category ONE fixed upload slot instead,
mirroring Opening Balance Import's SLOT_GROUPS pattern. Uploading into a
slot skips AI DocType detection entirely — the slot already knows its
target_doctype, so we go straight to the same deterministic mapping
(``heuristic_analysis``) that the old pipeline already used for well-known
master-data files, just without the filename-guessing step
(``infer_import_file``) that used to precede it.

The one exception is the "Cơ cấu tổ chức theo chi nhánh" combo slot: that
workbook genuinely spans two DocTypes (Branch + Department) across multiple
sheets, and doctype_metadata.infer_import_file() already routes each sheet
deterministically by sheet name — so the combo slot reuses that function
per-sheet instead of forcing one DocType for the whole file.
"""

from pathlib import Path

import frappe

from dcnet_migrate.import_auto.services.ai_client import verify_slot_mapping
from dcnet_migrate.import_auto.services.analysis import analysis_to_json, heuristic_analysis
from dcnet_migrate.import_auto.services.doctype_metadata import DOCTYPE_ORDER, infer_import_file
from dcnet_migrate.import_auto.services.excel import AI_SAMPLE_ROWS, summarize_workbook
from dcnet_migrate.import_auto.services.processor import (
    _list_importable_sheets,
    _row_count,
    _row_fingerprint,
    _scope_summary_to_sheet,
)


ORG_STRUCTURE_SLOT_KEY = "org_structure"

# Master data only — Chart of Accounts and everything balance/transaction
# related stays owned by Opening Balance Import, so the two tools never
# fight over the same file. Grouped by theme (mirrors Opening Balance
# Import's SLOT_GROUPS: named group -> list of slot cards) so the grid
# reads as sections, not one flat wall of cards.
GROUP_ORG = "Cơ cấu tổ chức (Organization)"
GROUP_ITEMS = "Danh mục vật tư hàng hóa (Items)"
GROUP_PARTNERS = "Đối tác & Ngân hàng (Partners & Banking)"
GROUP_OTHER = "Khác (Other)"

SLOT_DEFS = [
    # --- Cơ cấu tổ chức ---
    {"key": ORG_STRUCTURE_SLOT_KEY, "target_doctype": None, "is_combo": True, "group": GROUP_ORG,
     "label": "Cơ cấu tổ chức theo chi nhánh (Branch + Department)", "icon": "🏢",
     "hint": "File nhiều sheet: 1 sheet Chi nhánh + 1 sheet Phòng ban mỗi chi nhánh"},
    {"key": "department", "target_doctype": "Department", "group": GROUP_ORG,
     "label": "Phòng ban (Department)", "icon": "🗂️",
     "hint": "Danh sách phòng ban phẳng — không theo chi nhánh"},
    {"key": "employee", "target_doctype": "Employee", "group": GROUP_ORG,
     "label": "Nhân viên (Employee)", "icon": "👔",
     "hint": "Tên nhân viên · Bộ phận · Chức danh"},

    # --- Danh mục vật tư hàng hóa ---
    {"key": "uom", "target_doctype": "UOM", "group": GROUP_ITEMS,
     "label": "Đơn vị tính (UOM)", "icon": "📏",
     "hint": "Tên đơn vị tính · Mô tả"},
    {"key": "item_group", "target_doctype": "Item Group", "group": GROUP_ITEMS,
     "label": "Nhóm vật tư (Item Group)", "icon": "🏷️",
     "hint": "Tên nhóm vật tư hàng hóa dịch vụ"},
    {"key": "item", "target_doctype": "Item", "group": GROUP_ITEMS,
     "label": "Hàng hóa dịch vụ (Item)", "icon": "📋",
     "hint": "Mã · Tên · Nhóm VTHH · Đơn vị tính"},
    {"key": "warehouse", "target_doctype": "Warehouse", "group": GROUP_ITEMS,
     "label": "Kho (Warehouse)", "icon": "📦",
     "hint": "Tên kho · Địa chỉ"},

    # --- Đối tác & Ngân hàng ---
    {"key": "customer_supplier_group", "dual_targets": ["Customer Group", "Supplier Group"], "group": GROUP_PARTNERS,
     "label": "Nhóm khách hàng & nhà cung cấp (Customer/Supplier Group)", "icon": "👥",
     "hint": "1 file dùng chung — tạo cả Customer Group và Supplier Group cùng tên"},
    {"key": "customer", "target_doctype": "Customer", "group": GROUP_PARTNERS,
     "label": "Khách hàng (Customer)", "icon": "👤",
     "hint": "Tên khách hàng · Mã số thuế · Địa chỉ"},
    {"key": "supplier", "target_doctype": "Supplier", "group": GROUP_PARTNERS,
     "label": "Nhà cung cấp (Supplier)", "icon": "🏭",
     "hint": "Tên nhà cung cấp · Mã số thuế · Địa chỉ"},
    {"key": "bank", "target_doctype": "Bank", "group": GROUP_PARTNERS,
     "label": "Ngân hàng (Bank)", "icon": "🏦",
     "hint": "Tên đầy đủ / viết tắt ngân hàng"},
    {"key": "bank_account", "target_doctype": "Bank Account", "group": GROUP_PARTNERS,
     "label": "Tài khoản ngân hàng (Bank Account)", "icon": "💳",
     "hint": "Số tài khoản · Tên ngân hàng · Chủ tài khoản"},

    # --- Khác ---
    {"key": "project", "target_doctype": "Project", "group": GROUP_OTHER,
     "label": "Công trình (Project)", "icon": "🏗️",
     "hint": "Tên công trình · Ngày bắt đầu/kết thúc"},
]

SLOT_BY_KEY = {slot["key"]: slot for slot in SLOT_DEFS}


def get_slot_defs() -> list[dict]:
    return SLOT_DEFS


def assign_slot_file(doc, slot_key: str, file_path: str) -> dict:
    """(Re)build the Import Auto File row(s) for one slot from an uploaded file.

    Never calls AI to pick the DocType — the slot's DocType(s) are already
    known (simple slot), deterministically resolved by sheet name (combo
    slot), or fixed to more than one DocType from the same rows (dual-target
    slot — e.g. one shared Customer/Supplier Group list that becomes both
    DocTypes). AI is only used afterwards, as an optional QA pass over the
    resulting column mapping (see _apply_ai_mapping_check) — it can flag a
    mismapped/missing column but never overrides the fixed target_doctype.
    """
    slot = SLOT_BY_KEY.get(slot_key)
    if not slot:
        frappe.throw(frappe._("Unknown import slot: {0}").format(slot_key))

    _remove_existing_slot_rows(doc, slot_key)

    file_name = Path(file_path).name
    sheet_names = _list_importable_sheets(file_path) or [None]

    created = []
    for sheet_name in sheet_names:
        hints = [h for h in _resolve_hints(slot, file_name, sheet_name) if h.get("target_doctype")]
        if not hints:
            continue  # e.g. the "Công ty" sheet — company already exists, nothing to import

        summary = _scope_summary_to_sheet(
            summarize_workbook(file_path, max_sample_rows=AI_SAMPLE_ROWS, sample_strategy="first"),
            sheet_name,
        )
        for hint in hints:
            analysis = heuristic_analysis(doc, summary, hint)
            analysis = _apply_ai_mapping_check(doc, summary, analysis)
            row = _build_row_payload(slot_key, file_path, file_name, sheet_name, summary, analysis)
            doc.append("files", row)
            created.append(row)

    _refresh_status(doc)
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "slot_key": slot_key,
        "file_name": file_name,
        "rows_created": len(created),
        "safe_count": sum(1 for r in created if r["safety_status"] == "Safe"),
        "error_count": sum(1 for r in created if r["safety_status"] == "Error"),
    }


def clear_slot_file(doc, slot_key: str) -> dict:
    removed = _remove_existing_slot_rows(doc, slot_key, delete_files=True)
    _refresh_status(doc)
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"slot_key": slot_key, "rows_removed": removed}


def _resolve_hints(slot: dict, file_name: str, sheet_name: str | None) -> list[dict]:
    if slot.get("is_combo"):
        return [infer_import_file(file_name, sheet_name)]
    target_doctypes = slot.get("dual_targets") or [slot["target_doctype"]]
    return [_fixed_hint(slot, dt) for dt in target_doctypes]


def _fixed_hint(slot: dict, target_doctype: str) -> dict:
    return {
        "target_doctype": target_doctype,
        "is_supported": True,
        "known_file_type": True,
        "note": slot["label"],
        "import_order": DOCTYPE_ORDER.get(target_doctype, 999),
    }


def _apply_ai_mapping_check(doc, summary: dict, analysis: dict) -> dict:
    """Optional AI QA pass over heuristic_analysis()'s column mapping.

    Slot uploads never let AI pick the DocType (see assign_slot_file's
    docstring) — this only asks AI to double-check the mapping heuristic_
    analysis() already produced against a data sample, so an obviously
    mismapped/missing column gets flagged before the row is marked Ready
    instead of surfacing only after import. Best-effort: if AI is not
    configured, times out, or errors, the heuristic result is kept as-is —
    this check must never block an otherwise-valid slot upload.
    """
    if analysis.get("safety_status") != "Safe" or not analysis.get("mappings"):
        return analysis

    verdict = verify_slot_mapping(
        doc, summary, analysis.get("target_doctype"), analysis.get("mappings"), analysis.get("defaults") or {}
    )
    if not verdict or verdict.get("ok", True):
        return analysis

    issues = [str(issue) for issue in (verdict.get("issues") or []) if issue]
    if not issues:
        return analysis

    note = "AI kiểm tra mapping phát hiện vấn đề:\n- " + "\n- ".join(issues)
    analysis = dict(analysis)
    analysis["safety_status"] = "Warning"
    analysis["reason"] = f"{analysis.get('reason') or ''}\n{note}".strip()
    return analysis


def _build_row_payload(slot_key, file_path, file_name, sheet_name, summary, analysis) -> dict:
    safety_status = analysis.get("safety_status") or "Error"
    resolved_sheet = analysis.get("sheet_name") or sheet_name

    return {
        "slot_key": slot_key,
        "file_name": file_name,
        "file_path": file_path,
        "sheet_name": resolved_sheet,
        "source_hash": _row_fingerprint(file_path, resolved_sheet),
        "import_order": analysis.get("import_order") or 999,
        "target_doctype": analysis.get("target_doctype"),
        "safety_status": safety_status,
        "status": "Ready" if safety_status in ("Safe", "Warning") else "Error",
        "row_count": _row_count(summary, analysis),
        "confidence": analysis.get("confidence") or 0,
        "analysis_note": analysis.get("reason"),
        "analysis_json": analysis_to_json(analysis),
        "error_detail": None if safety_status == "Safe" else analysis.get("reason"),
        "duplicate_check_status": "Pending",
        "duplicate_match_count": 0,
        "duplicate_report_json": None,
    }


def _remove_existing_slot_rows(doc, slot_key: str, delete_files: bool = False) -> int:
    rows = [row for row in (doc.files or []) if getattr(row, "slot_key", None) == slot_key]
    removed_paths = set()
    for row in rows:
        if row.file_path:
            removed_paths.add(row.file_path)
        doc.remove(row)

    if delete_files:
        for path in removed_paths:
            try:
                target = Path(path)
                if target.is_file():
                    target.unlink()
            except OSError:
                frappe.log_error(frappe.get_traceback(), "Import Auto Slot Clear Failed")

    return len(rows)


def _refresh_status(doc) -> None:
    from dcnet_migrate.import_auto.doctype.import_auto.import_auto import _refresh_import_auto_status

    doc.excel_file_count = len(doc.files or [])
    _refresh_import_auto_status(doc)
