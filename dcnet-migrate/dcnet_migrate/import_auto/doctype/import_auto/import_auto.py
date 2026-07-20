import re
import shutil
import json
from datetime import datetime
from pathlib import Path

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


LEGACY_DEFAULT_IMPORT_PATH = "/workspace/data import"
SERVER_UPLOAD_ROOT_PARTS = ("private", "files", "import_auto_uploads")
EXCEL_UPLOAD_EXTENSIONS = {".xlsx", ".xls", ".csv"}


class ImportAuto(Document):
    """Generic Excel folder analysis and controlled one-file-at-a-time import."""

    def before_insert(self):
        self._set_default_server_folder()

    def validate(self):
        self._set_default_server_folder()
        if not self.status:
            self.status = "Draft"
        if not self.file_pattern:
            self.file_pattern = "*.xlsx,*.xls,*.csv"

    def _set_default_server_folder(self):
        if self.name and (not self.folder_path or self.folder_path == LEGACY_DEFAULT_IMPORT_PATH):
            self.folder_path = get_server_upload_folder_path(self.name)

    @frappe.whitelist()
    def test_ai_connection(self):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.ai_client import test_connection

        result = test_connection(self)
        frappe.msgprint(_("AI connection is working."), alert=True)
        return result

    @frappe.whitelist()
    def scan_files(self):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.processor import enqueue_scan_files

        result = enqueue_scan_files(self.name, frappe.session.user)
        frappe.msgprint(_("Scan has been queued. Progress will update here."), alert=True)
        return result

    @frappe.whitelist()
    def analyze_files(self):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.processor import enqueue_analyze_files

        result = enqueue_analyze_files(self.name, frappe.session.user)
        frappe.msgprint(_("Analysis has been queued. Progress will update here."), alert=True)
        return result

    @frappe.whitelist()
    def get_import_audit(self, file_row_name: str | None = None, limit: int = 500):
        """Return a summary of records created by this Import Auto (or a specific file row)."""
        self.check_permission("read")
        return _build_import_audit(self, file_row_name, int(limit or 500))

    @frappe.whitelist()
    def preview_import_file(self, file_row_name: str):
        self.check_permission("read")
        return _build_file_preview(self, file_row_name)

    @frappe.whitelist()
    def check_duplicates_file(self, file_row_name: str):
        self.check_permission("read")
        return _build_duplicate_report(self, file_row_name)

    @frappe.whitelist()
    def smart_plan_file(self, file_row_name: str, user_feedback: str | None = None, force: int = 0):
        self.check_permission("write")
        return _build_smart_plan(self, file_row_name, user_feedback, force=bool(int(force or 0)))

    @frappe.whitelist()
    def smart_execute_file(self, file_row_name: str, plan_json: str | None = None):
        self.check_permission("write")
        return _execute_smart_plan(self, file_row_name, plan_json)

    @frappe.whitelist()
    def smart_fix_file(self, file_row_name: str, plan_json: str, error_json: str):
        self.check_permission("write")
        return _build_smart_fix(self, file_row_name, plan_json, error_json)

    @frappe.whitelist()
    def confirm_smart_fix_dependencies(self, file_row_name: str, plan_json: str,
                                        proposals_json: str, accepted_ids_json: str):
        """Merge AI-proposed dependency steps (user-approved) back into the plan."""
        self.check_permission("write")
        return _confirm_dependency_steps(self, file_row_name, plan_json,
                                          proposals_json, accepted_ids_json)

    @frappe.whitelist()
    def reset_file_for_reimport(self, file_row_name: str):
        """Reset a Partial/Failed file back to Analyzed so it can be executed again.

        Re-running a plan is safe because each step has ignore_duplicates=true:
        already-imported records are skipped; only rows that genuinely failed
        will be retried.
        """
        self.check_permission("write")
        return _reset_file_for_reimport(self, file_row_name)

    @frappe.whitelist()
    def mark_file_imported(self, file_row_name: str):
        self.check_permission("write")
        return _mark_file_imported(self, file_row_name)

    @frappe.whitelist()
    def delete_import_file(self, file_row_name: str):
        self.check_permission("write")
        return _delete_import_file(self, file_row_name)

    @frappe.whitelist()
    def reanalyze_file(self, file_row_name: str, user_feedback: str | None = None):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.processor import enqueue_reanalyze_file

        return enqueue_reanalyze_file(self.name, file_row_name, user_feedback, frappe.session.user)

    @frappe.whitelist()
    def preview_opening_balances(self):
        self.check_permission("read")
        from dcnet_migrate.import_auto.services.opening_balance import preview_opening_balances

        return preview_opening_balances(self)

    @frappe.whitelist()
    def execute_opening_balances(self, posting_date: str | None = None, submit=0, force=0):
        self.check_permission("write")
        from dcnet_migrate.import_auto.services.opening_balance import execute_opening_balances

        return execute_opening_balances(self, posting_date=posting_date, submit=submit, force=force)


def _get_import_doc(docname: str | None = None, permission_type: str = "write") -> ImportAuto:
    docname = docname or _get_docname_from_request()
    if not docname:
        frappe.throw(_("Import Auto document is required."))

    doc = frappe.get_doc("Import Auto", docname)
    doc.check_permission(permission_type)
    return doc


def get_server_upload_folder_path(docname: str, create: bool = True) -> str:
    folder = _server_upload_dir(docname)
    if create:
        folder.mkdir(parents=True, exist_ok=True)
    return str(folder)


def _server_upload_root() -> Path:
    return Path(frappe.get_site_path(*SERVER_UPLOAD_ROOT_PARTS)).resolve()


def _server_upload_dir(docname: str) -> Path:
    if not docname:
        frappe.throw(_("Import Auto document is required."))
    return (_server_upload_root() / _safe_path_part(docname)).resolve()


def _safe_path_part(value: str) -> str:
    text = frappe.as_unicode(value or "").strip()
    text = re.sub(r"[\x00-\x1f<>:\"|?*]", "_", text)
    if not text or text in {".", ".."}:
        frappe.throw(_("Invalid upload path."))
    return text[:160]


def _safe_relative_upload_path(relative_path: str | None, filename: str | None) -> Path:
    raw_path = frappe.as_unicode(relative_path or filename or "").replace("\\", "/").strip()
    if not raw_path or raw_path.startswith("/"):
        frappe.throw(_("Invalid upload path."))

    parts = []
    for part in raw_path.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            frappe.throw(_("Invalid upload path."))
        parts.append(_safe_path_part(part))

    if not parts:
        frappe.throw(_("Invalid upload path."))

    upload_path = Path(*parts)
    if upload_path.suffix.lower() not in EXCEL_UPLOAD_EXTENSIONS or upload_path.name.startswith("~$"):
        frappe.throw(_("Only Excel or CSV files (.xlsx/.xls/.csv) can be uploaded."))
    return upload_path


def _ensure_target_inside_base(base_dir: Path, target: Path) -> None:
    try:
        target.relative_to(base_dir)
    except ValueError:
        frappe.throw(_("Invalid upload path."))


def _get_uploaded_file():
    files = getattr(frappe.request, "files", None)
    uploaded = files.get("file") if files else None
    if not uploaded:
        frappe.throw(_("No file was uploaded."))
    return uploaded


def save_excel_upload(
    upload_key: str,
    relative_path: str | None = None,
    clear_existing: int = 0,
) -> dict:
    """Save an uploaded Excel file in the site's private migration area."""
    uploaded = _get_uploaded_file()
    upload_path = _safe_relative_upload_path(relative_path, uploaded.filename)
    base_dir = _server_upload_dir(upload_key)

    if cint(clear_existing):
        shutil.rmtree(base_dir, ignore_errors=True)
    base_dir.mkdir(parents=True, exist_ok=True)

    target = (base_dir / upload_path).resolve()
    _ensure_target_inside_base(base_dir, target)
    target.parent.mkdir(parents=True, exist_ok=True)
    uploaded.save(str(target))

    return {
        "file_name": target.name,
        "relative_path": upload_path.as_posix(),
        "folder_path": str(base_dir),
        "size": target.stat().st_size,
    }


@frappe.whitelist()
def upload_excel_file(docname: str, relative_path: str | None = None, clear_existing: int = 0):
    doc = _get_import_doc(docname)
    result = save_excel_upload(doc.name, relative_path, clear_existing)

    frappe.db.set_value(
        "Import Auto",
        doc.name,
        {
            "folder_path": result["folder_path"],
            "recursive": 1,
            "file_pattern": "*.xlsx,*.xls",
        },
        update_modified=True,
    )
    frappe.db.commit()
    return result


@frappe.whitelist()
def get_slot_defs():
    """Fixed master-data upload slots (see services/slot_import.py). A
    static list, not doc-specific — callable before the Import Auto
    document is even saved so the slot grid can render immediately."""
    from dcnet_migrate.import_auto.services.slot_import import get_slot_defs

    return get_slot_defs()


@frappe.whitelist()
def upload_slot_file(docname: str, slot_key: str, relative_path: str):
    """Upload a file directly into one master-data slot — skips AI DocType
    detection entirely since the slot already fixes target_doctype (see
    services/slot_import.py)."""
    from dcnet_migrate.import_auto.services.slot_import import assign_slot_file

    doc = _get_import_doc(docname)
    uploaded = save_excel_upload(doc.name, f"slots/{slot_key}/{relative_path}")
    file_path = str(Path(uploaded["folder_path"]) / uploaded["relative_path"])
    return assign_slot_file(doc, slot_key, file_path)


@frappe.whitelist()
def list_server_upload_folders(docname: str):
    _get_import_doc(docname, permission_type="read")
    root = _server_upload_root()
    root.mkdir(parents=True, exist_ok=True)
    folders = []

    for folder in sorted(root.iterdir(), key=lambda item: item.stat().st_mtime if item.exists() else 0, reverse=True):
        if not folder.is_dir():
            continue
        excel_files = [
            path
            for path in folder.rglob("*")
            if path.is_file()
            and path.suffix.lower() in EXCEL_UPLOAD_EXTENSIONS
            and not path.name.startswith("~$")
        ]
        folders.append(
            {
                "folder_name": folder.name,
                "folder_path": str(folder.resolve()),
                "file_count": len(excel_files),
                "modified": datetime.fromtimestamp(folder.stat().st_mtime).isoformat(),
            }
        )

    return {"root": str(root), "folders": folders}


@frappe.whitelist()
def set_server_upload_folder(docname: str, folder_name: str):
    doc = _get_import_doc(docname)
    folder = (_server_upload_root() / _safe_path_part(folder_name)).resolve()
    _ensure_target_inside_base(_server_upload_root(), folder)
    if not folder.exists() or not folder.is_dir():
        frappe.throw(_("Server folder not found."))

    frappe.db.set_value(
        "Import Auto",
        doc.name,
        {
            "folder_path": str(folder),
            "recursive": 1,
            "file_pattern": "*.xlsx,*.xls",
        },
        update_modified=True,
    )
    frappe.db.commit()
    return {"folder_path": str(folder), "folder_name": folder.name}


def _get_docname_from_request() -> str | None:
    request_doc = frappe.form_dict.get("doc") or frappe.form_dict.get("docs")
    if request_doc:
        parsed = frappe.parse_json(request_doc)
        if isinstance(parsed, dict):
            return parsed.get("name")

    return frappe.form_dict.get("docname") or frappe.form_dict.get("name")


def _get_file_row(doc: ImportAuto, file_row_name: str):
    if not file_row_name:
        frappe.throw(_("File row is required."))

    for row in doc.files:
        if row.name == file_row_name:
            return row

    frappe.throw(_("File row not found."))


def _ensure_import_auto_not_running(doc: ImportAuto) -> None:
    if doc.status in {"Scanning", "Analyzing", "Importing"}:
        frappe.throw(_("Import Auto is running. Please wait until it finishes."))


def _refresh_import_auto_status(doc: ImportAuto) -> None:
    if not doc.files:
        doc.status = "Scanned"
        doc.excel_file_count = 0
        doc.total_files = 0
        doc.processed_files = 0
        doc.progress_percent = 100
        doc.progress_message = _("Scanned 0 Excel file(s).")
        doc.current_file = None
        doc.summary_json = json.dumps({"scanned_files": 0}, ensure_ascii=False, indent=2)
        return

    from dcnet_migrate.import_auto.services.importer import _update_parent_status

    _update_parent_status(doc)


def _get_row_file_path(doc: ImportAuto, row) -> Path:
    file_path = frappe.as_unicode(getattr(row, "file_path", "") or "").strip()
    folder_path = frappe.as_unicode(getattr(doc, "folder_path", "") or "").strip()
    if not file_path:
        frappe.throw(_("File path is missing for this row."))
    if not folder_path:
        frappe.throw(_("Import Auto folder path is missing."))

    base = Path(folder_path).expanduser().resolve()
    target = Path(file_path).expanduser().resolve()
    _ensure_target_inside_base(base, target)
    return target


def _delete_import_file(doc: ImportAuto, file_row_name: str) -> dict:
    _ensure_import_auto_not_running(doc)
    row = _get_file_row(doc, file_row_name)
    file_name = row.file_name
    target = _get_row_file_path(doc, row)
    deleted_file = False

    if target.exists():
        if not target.is_file():
            frappe.throw(_("Import path is not a file: {0}").format(target))
        target.unlink()
        deleted_file = True

    doc.remove(row)
    _refresh_import_auto_status(doc)
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "ok": True,
        "file_name": file_name,
        "file_path": str(target),
        "deleted_file": deleted_file,
        "parent_status": doc.status,
        "message": _("Đã xóa file '{0}' khỏi danh sách import.").format(file_name),
    }


def _mark_file_imported(doc: ImportAuto, file_row_name: str) -> dict:
    _ensure_import_auto_not_running(doc)
    row = _get_file_row(doc, file_row_name)
    imported_records = cint(row.row_count or row.imported_records or 0)
    imported_on = frappe.utils.now_datetime()

    row.status = "Imported"
    row.imported_records = imported_records
    row.failed_records = 0
    row.imported_on = imported_on
    row.error_detail = None

    _refresh_import_auto_status(doc)
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "ok": True,
        "file_name": row.file_name,
        "row_name": row.name,
        "status": row.status,
        "imported_records": imported_records,
        "imported_on": str(imported_on),
        "parent_status": doc.status,
        "message": _("Đã đánh dấu '{0}' là đã import thành công.").format(row.file_name),
    }


def _build_file_preview(doc: ImportAuto, file_row_name: str) -> dict:
    row = _get_file_row(doc, file_row_name)

    try:
        from dcnet_migrate.import_auto.services.excel import summarize_workbook

        preview_row_limit = 30
        summary = summarize_workbook(row.file_path, max_sample_rows=preview_row_limit)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto Preview Failed")
        frappe.throw(_("Không thể đọc bản xem trước tệp Excel này. Vui lòng kiểm tra đường dẫn hoặc định dạng tệp."))

    return {
        "file_name": row.file_name,
        "file_path": row.file_path,
        "sheet_name": row.sheet_name,
        "target_doctype": row.target_doctype,
        "safety_status": row.safety_status,
        "status": row.status,
        "row_count": row.row_count,
        "confidence": row.confidence,
        "analysis_note": row.analysis_note,
        "error_detail": row.error_detail,
        "preview_row_limit": preview_row_limit,
        "sheets": summary.get("sheets", []),
    }


def _build_duplicate_report(doc: ImportAuto, file_row_name: str) -> dict:
    row = _get_file_row(doc, file_row_name)
    existing_import_report = _parse_smart_import_report(row.error_detail)
    if row.status in {"Imported", "Partial"}:
        return {
            "file_name": row.file_name,
            "target_doctype": row.target_doctype,
            "safety_status": row.safety_status,
            "duplicate_check_status": row.duplicate_check_status,
            "post_import_report": existing_import_report,
            "message": _(
                "Tệp này đã import. Hãy xem danh sách dòng lỗi/bị bỏ qua thay vì kiểm tra trùng lại."
            ),
        }

    from dcnet_migrate.import_auto.services.duplicate_checker import (
        check_duplicates_for_row,
        determine_safety_status,
    )
    import json as _json

    report = check_duplicates_for_row(doc, row)
    new_safety = determine_safety_status(row.safety_status, report)
    updates = {
        "duplicate_report_json": _json.dumps(report, ensure_ascii=False, indent=2, default=str),
        "duplicate_match_count": report.get("total_matches") or 0,
        "duplicate_check_status": "Warning" if (report.get("total_matches") or 0) > 0 else "Clean",
    }
    if row.safety_status in ("Safe", "Warning") and new_safety in ("Safe", "Warning"):
        updates["safety_status"] = new_safety
        if new_safety == "Warning":
            warning_note = report.get("note") or "Phát hiện dữ liệu trùng chính xác trong cơ sở dữ liệu."
            updates["error_detail"] = warning_note
        elif row.safety_status == "Warning":
            updates["error_detail"] = None
    frappe.db.set_value("Import Auto File", row.name, updates, update_modified=False)
    frappe.db.commit()
    return {
        "file_name": row.file_name,
        "target_doctype": report.get("target_doctype") or row.target_doctype,
        "safety_status": updates.get("safety_status", row.safety_status),
        "duplicate_check_status": updates["duplicate_check_status"],
        "report": report,
    }


def _parse_smart_import_report(value) -> dict | None:
    if not value:
        return None
    try:
        parsed = frappe.parse_json(value) if isinstance(value, str) else value
    except Exception:
        return None
    if isinstance(parsed, dict) and parsed.get("type") == "smart_import_execution_report":
        return parsed
    return None


@frappe.whitelist()
def test_ai_connection(docname: str | None = None):
    doc = _get_import_doc(docname)
    from dcnet_migrate.import_auto.services.ai_client import test_connection

    result = test_connection(doc)
    frappe.msgprint(_("AI connection is working."), alert=True)
    return result


@frappe.whitelist()
def scan_files(docname: str | None = None):
    doc = _get_import_doc(docname)
    from dcnet_migrate.import_auto.services.processor import enqueue_scan_files

    result = enqueue_scan_files(doc.name, frappe.session.user)
    frappe.msgprint(_("Scan has been queued. Progress will update here."), alert=True)
    return result


@frappe.whitelist()
def analyze_files(docname: str | None = None):
    doc = _get_import_doc(docname)
    from dcnet_migrate.import_auto.services.processor import enqueue_analyze_files

    result = enqueue_analyze_files(doc.name, frappe.session.user)
    frappe.msgprint(_("Analysis has been queued. Progress will update here."), alert=True)
    return result


@frappe.whitelist()
def preview_import_file(file_row_name: str, docname: str | None = None):
    doc = _get_import_doc(docname, permission_type="read")
    return _build_file_preview(doc, file_row_name)


@frappe.whitelist()
def reanalyze_file(file_row_name: str, user_feedback: str | None = None, docname: str | None = None):
    doc = _get_import_doc(docname)
    from dcnet_migrate.import_auto.services.processor import enqueue_reanalyze_file

    return enqueue_reanalyze_file(doc.name, file_row_name, user_feedback, frappe.session.user)


@frappe.whitelist()
def preview_opening_balances(docname: str | None = None):
    doc = _get_import_doc(docname, permission_type="read")
    from dcnet_migrate.import_auto.services.opening_balance import preview_opening_balances as _preview

    return _preview(doc)


@frappe.whitelist()
def execute_opening_balances(
    docname: str | None = None,
    posting_date: str | None = None,
    submit=0,
    force=0,
):
    doc = _get_import_doc(docname)
    from dcnet_migrate.import_auto.services.opening_balance import execute_opening_balances as _execute

    return _execute(doc, posting_date=posting_date, submit=submit, force=force)


@frappe.whitelist()
def check_duplicates_file(file_row_name: str, docname: str | None = None):
    doc = _get_import_doc(docname, permission_type="read")
    return _build_duplicate_report(doc, file_row_name)

def _build_smart_plan(doc: ImportAuto, file_row_name: str, user_feedback: str | None, force: bool = False) -> dict:
    """Queue an AI smart-plan job; result is delivered via realtime."""
    row = _get_file_row(doc, file_row_name)
    if row.status == "Imported" and not force:
        return {"error": _("Tệp này đã import rồi.")}
    if not force and (row.safety_status not in ("Safe", "Warning") or not row.target_doctype):
        return {
            "error": _(
                "Tệp này chưa có ánh xạ an toàn để import. "
                "Vui lòng bấm Phân tích lại và nhập hướng dẫn cho AI trước."
            ),
            "detail": row.error_detail or row.analysis_note,
            "status": row.status,
            "safety_status": row.safety_status,
            "target_doctype": row.target_doctype,
        }

    if not force and not (user_feedback or "").strip():
        cached_or_local = _build_or_get_plan_from_saved_analysis(row, doc)
        if cached_or_local and not cached_or_local.get("error"):
            return {
                "queued": False,
                "file_name": row.file_name,
                "row_name": row.name,
                "target_doctype": row.target_doctype,
                "plan": cached_or_local,
                "from_analysis": True,
                "message": _(
                    "Đã dùng mapping từ bước Phân tích để dựng script import, không gọi AI lại."
                ),
            }

    from dcnet_migrate.import_auto.services.smart_runner import enqueue_smart_plan

    if force and not user_feedback:
        user_feedback = (
            "File phân tích tự động bị lỗi hoặc thiếu mapping. "
            "Hãy tự suy luận DocType và lập kế hoạch import từng bước an toàn từ headers/sample. "
            "plan_summary phải nêu rõ hướng xử lý để user duyệt trước khi import; "
            "bỏ qua dòng không hợp lệ và không sửa dữ liệu nguồn quan trọng."
        )

    queued = enqueue_smart_plan(
        doc.name,
        row.name,
        user_feedback=user_feedback,
        requested_by=frappe.session.user,
    )
    return {
        "queued": True,
        "file_name": row.file_name,
        "row_name": row.name,
        "target_doctype": row.target_doctype,
        "job_id": queued.get("job_id"),
        "message": "AI đang phân tích 10 dòng mẫu để tạo mapping/script. Kết quả sẽ trả về khi hoàn tất.",
    }


def _build_or_get_plan_from_saved_analysis(row, doc: ImportAuto) -> dict | None:
    if getattr(row, "smart_plan_status", None) == "Ready" and getattr(row, "smart_plan_json", None):
        try:
            plan = frappe.parse_json(row.smart_plan_json)
            if isinstance(plan, dict) and plan.get("steps"):
                # A Department plan cached before its Branch was imported never
                # got a `branch` value (Branch didn't exist yet to resolve).
                # Re-check on every reuse — cheap (one DB lookup) and Branch
                # may well exist by now — instead of permanently shipping
                # Department records with no branch link forever.
                if row.target_doctype == "Department":
                    from dcnet_migrate.import_auto.services.smart_planner import (
                        _post_process_department_branch_plan,
                    )

                    _post_process_department_branch_plan(plan, doc, row.sheet_name)
                return plan
        except Exception:
            pass

    if not getattr(row, "analysis_json", None):
        return None

    try:
        analysis = frappe.parse_json(row.analysis_json)
    except Exception:
        return None

    if not isinstance(analysis, dict) or not analysis.get("mappings"):
        return None

    try:
        from dcnet_migrate.import_auto.services.smart_planner import (
            build_smart_plan_from_analysis,
        )

        plan = build_smart_plan_from_analysis(doc, row)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto Build Plan From Analysis Failed")
        return None

    if not isinstance(plan, dict) or plan.get("error") or not plan.get("steps"):
        return None

    frappe.db.set_value(
        "Import Auto File",
        row.name,
        {
            "smart_plan_status": "Ready",
            "smart_plan_json": json.dumps(plan, ensure_ascii=False, indent=2, default=str),
            "smart_plan_generated_on": frappe.utils.now_datetime(),
            "smart_plan_error": None,
        },
        update_modified=False,
    )
    frappe.db.commit()
    return plan


def _execute_smart_plan(doc: ImportAuto, file_row_name: str, plan_json: str | None = None) -> dict:
    row = _get_file_row(doc, file_row_name)
    if not plan_json:
        plan_json = getattr(row, "smart_plan_json", None)
    if not plan_json:
        frappe.throw(_("Chưa có script import cho tệp này. Hãy chạy Phân tích trước để tạo script."))

    from dcnet_migrate.import_auto.services.smart_runner import enqueue_smart_execute

    queued = enqueue_smart_execute(
        doc.name,
        row.name,
        plan_json,
        requested_by=frappe.session.user,
    )
    return {
        "queued": True,
        "file_name": row.file_name,
        "row_name": row.name,
        "job_id": queued.get("job_id"),
        "message": "Script import đang chạy trong nền. Kết quả sẽ trả về khi hoàn tất.",
    }


def _execute_smart_plan_now(
    doc: ImportAuto,
    file_row_name: str,
    plan_json: str | None = None,
    progress_callback=None,
) -> dict:
    row = _get_file_row(doc, file_row_name)
    if not plan_json:
        plan_json = getattr(row, "smart_plan_json", None)
    if not plan_json:
        frappe.throw(_("Chưa có script import cho tệp này. Hãy chạy Phân tích trước để tạo script."))

    try:
        plan = frappe.parse_json(plan_json)
    except Exception:
        frappe.throw(_("Plan không phải JSON hợp lệ."))

    from dcnet_migrate.import_auto.services.smart_executor import execute_plan

    result = execute_plan(doc, row, plan, dry_run=False, progress_callback=progress_callback)
    import_report = _build_smart_import_report(row, result)
    result["import_report"] = import_report
    if (
        result.get("ok")
        or result.get("can_resume")
        or result.get("rollback_scope") in {"failed_row_only", "failed_rows_only"}
    ):
        failed_count = result.get("total_failed") or 0
        skipped_count = import_report.get("total_skipped") or 0
        error_detail = (
            json.dumps(import_report, ensure_ascii=False, indent=2, default=str)
            if import_report.get("total_skipped") or import_report.get("total_failed")
            else None
        )
        updates = {
            "status": "Imported" if not (failed_count or skipped_count) else "Partial",
            "imported_records": result.get("total_inserted") or 0,
            "failed_records": failed_count,
            "imported_on": frappe.utils.now_datetime(),
            "error_detail": error_detail,
        }
        for fieldname, value in updates.items():
            setattr(row, fieldname, value)
        from dcnet_migrate.import_auto.services.importer import _update_parent_status

        _update_parent_status(doc)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
    return result


def _build_smart_import_report(row, result: dict) -> dict:
    """Build a compact per-row execution report for the Import Auto UI."""
    result = result or {}
    steps = []
    total_skipped = int(result.get("total_skipped") or 0)
    total_failed = int(result.get("total_failed") or 0)
    skipped_by_type: dict[str, int] = {}
    skipped_non_duplicate = 0

    for step_result in result.get("results") or []:
        if not isinstance(step_result, dict):
            continue
        step_skipped_by_type = step_result.get("skipped_by_type") or {}
        for reason_type, count in step_skipped_by_type.items():
            count = int(count or 0)
            skipped_by_type[reason_type] = skipped_by_type.get(reason_type, 0) + count
            if reason_type not in {"duplicate", "source_duplicate"}:
                skipped_non_duplicate += count

        steps.append({
            "step": step_result.get("step"),
            "title": step_result.get("title"),
            "target_doctype": step_result.get("target_doctype"),
            "inserted": step_result.get("inserted") or 0,
            "skipped": step_result.get("skipped") or 0,
            "failed": step_result.get("failed") or 0,
            "skipped_by_type": step_skipped_by_type,
            "skipped_rows": step_result.get("skipped_rows") or [],
            "skipped_rows_truncated": bool(step_result.get("skipped_rows_truncated")),
            "errors": step_result.get("errors") or [],
        })

    created = int(result.get("total_inserted") or 0)
    source_rows = int(getattr(row, "row_count", None) or 0)
    summary_parts = [f"Đã tạo {created} bản ghi"]
    if total_skipped:
        summary_parts.append(f"bỏ qua {total_skipped} dòng")
    if total_failed:
        summary_parts.append(f"lỗi {total_failed} dòng")
    summary = ", ".join(summary_parts) + f" / {source_rows} dòng nguồn."

    return {
        "type": "smart_import_execution_report",
        "summary": summary,
        "file_name": getattr(row, "file_name", None),
        "target_doctype": getattr(row, "target_doctype", None),
        "source_rows": source_rows,
        "total_inserted": created,
        "total_skipped": total_skipped,
        "total_failed": total_failed,
        "total_skipped_by_type": skipped_by_type,
        "total_skipped_non_duplicate": skipped_non_duplicate,
        "detail_limit": 500,
        "steps": steps,
    }


@frappe.whitelist()
def smart_plan_file(file_row_name: str, docname: str | None = None,
                    user_feedback: str | None = None, force: int = 0):
    doc = _get_import_doc(docname)
    return _build_smart_plan(doc, file_row_name, user_feedback, force=bool(int(force or 0)))


@frappe.whitelist()
def smart_execute_file(file_row_name: str, plan_json: str | None = None, docname: str | None = None):
    doc = _get_import_doc(docname)
    return _execute_smart_plan(doc, file_row_name, plan_json)


def _build_smart_fix(doc, file_row_name: str, plan_json: str, error_json: str) -> dict:
    """Queue AI fix as a background job; result is delivered via realtime.

    The job publishes progress events on ``import_auto_smart_fix`` so the UI
    can render a progress dialog (like smart_plan). The patching itself is
    done server-side with allowed/protected-field enforcement.
    """
    row = _get_file_row(doc, file_row_name)
    if not plan_json:
        frappe.throw(_("Plan rỗng, không thể sửa."))

    from dcnet_migrate.import_auto.services.smart_runner import enqueue_smart_fix

    queued = enqueue_smart_fix(doc.name, row.name, plan_json, error_json or "{}",
                               requested_by=frappe.session.user)
    return {
        "queued": True,
        "file_name": row.file_name,
        "row_name": row.name,
        "job_id": queued.get("job_id"),
        "message": "AI đang phân tích và sửa lỗi trong nền. Kết quả sẽ trả về khi hoàn tất.",
    }


@frappe.whitelist()
def smart_fix_file(file_row_name: str, plan_json: str, error_json: str, docname: str | None = None):
    doc = _get_import_doc(docname)
    return _build_smart_fix(doc, file_row_name, plan_json, error_json)


def _confirm_dependency_steps(doc, file_row_name: str, plan_json: str,
                                proposals_json: str, accepted_ids_json: str) -> dict:
    """Merge approved AI dependency proposals into the plan and return it."""
    # file_row_name kept for future per-row validation
    if not plan_json:
        frappe.throw(_("Plan rỗng, không thể merge."))

    try:
        plan = frappe.parse_json(plan_json)
    except Exception:
        frappe.throw(_("Plan không phải JSON hợp lệ."))

    try:
        proposals = frappe.parse_json(proposals_json) if proposals_json else []
    except Exception:
        frappe.throw(_("Danh sách proposals không hợp lệ."))

    try:
        accepted_ids = frappe.parse_json(accepted_ids_json) if accepted_ids_json else []
    except Exception:
        accepted_ids = []

    if not isinstance(accepted_ids, list):
        accepted_ids = []
    if not isinstance(proposals, list):
        proposals = []

    from dcnet_migrate.import_auto.services.smart_planner import (
        merge_dependency_steps_into_plan,
    )

    merged_plan = merge_dependency_steps_into_plan(plan, accepted_ids, proposals)
    return {
        "ok": True,
        "plan": merged_plan,
        "accepted_count": len(accepted_ids),
    }


@frappe.whitelist()
def confirm_smart_fix_dependencies(file_row_name: str, plan_json: str,
                                    proposals_json: str, accepted_ids_json: str,
                                    docname: str | None = None):
    doc = _get_import_doc(docname)
    return _confirm_dependency_steps(doc, file_row_name, plan_json,
                                      proposals_json, accepted_ids_json)


def _reset_file_for_reimport(doc: ImportAuto, file_row_name: str) -> dict:
    row = _get_file_row(doc, file_row_name)

    if row.status not in ("Partial", "Failed"):
        return {
            "ok": False,
            "message": _("Chỉ có thể reset file có trạng thái Partial hoặc Failed. Trạng thái hiện tại: {0}").format(row.status),
        }

    if not getattr(row, "smart_plan_json", None):
        return {
            "ok": False,
            "message": _("File này chưa có Smart Plan. Hãy chạy Phân tích trước."),
        }

    row.status = "Analyzed"
    row.imported_records = 0
    row.failed_records = 0
    row.imported_on = None
    row.error_detail = None
    row.duplicate_check_status = None
    row.duplicate_match_count = 0
    row.duplicate_report_json = None

    from dcnet_migrate.import_auto.services.importer import _update_parent_status
    _update_parent_status(doc)
    doc.save(ignore_permissions=True)

    return {
        "ok": True,
        "file_name": row.file_name,
        "row_name": row.name,
        "message": _(
            "Đã reset '{0}' về trạng thái Analyzed. "
            "Smart Plan vẫn còn — bấm Execute để chạy lại. "
            "Các bản ghi đã import trước đó sẽ được bỏ qua (ignore_duplicates)."
        ).format(row.file_name),
    }


@frappe.whitelist()
def reset_file_for_reimport(file_row_name: str, docname: str | None = None):
    doc = _get_import_doc(docname)
    return _reset_file_for_reimport(doc, file_row_name)


@frappe.whitelist()
def mark_file_imported(file_row_name: str, docname: str | None = None):
    doc = _get_import_doc(docname)
    return _mark_file_imported(doc, file_row_name)


@frappe.whitelist()
def delete_import_file(file_row_name: str, docname: str | None = None):
    doc = _get_import_doc(docname)
    return _delete_import_file(doc, file_row_name)


@frappe.whitelist()
def clear_slot_file(docname: str, slot_key: str):
    from dcnet_migrate.import_auto.services.slot_import import clear_slot_file as _clear_slot_file

    doc = _get_import_doc(docname)
    return _clear_slot_file(doc, slot_key)


def _build_import_audit(doc: ImportAuto, file_row_name: str | None, limit: int) -> dict:
    """Query Data Import Log to show which records were created by this import session."""
    if not frappe.db.exists("DocType", "Data Import Log"):
        return {"error": _("Data Import Log DocType không tồn tại."), "rows": [], "summary": {}}

    # Use LIKE filter on the JSON messages field — compatible with all MariaDB versions
    search_pattern = f'%"import_auto": "{doc.name}"%'
    filters: list = [
        ["Data Import Log", "success", "=", 1],
        ["Data Import Log", "messages", "like", search_pattern],
    ]
    if file_row_name:
        file_pattern = f'%"import_auto_file": "{file_row_name}"%'
        filters.append(["Data Import Log", "messages", "like", file_pattern])

    logs = frappe.get_all(
        "Data Import Log",
        filters=filters,
        fields=["docname", "messages", "creation"],
        order_by="creation asc",
        limit=limit,
    )

    rows: list[dict] = []
    summary: dict[str, int] = {}
    for log in logs:
        try:
            meta = frappe.parse_json(log.messages) if log.messages else {}
        except Exception:
            meta = {}

        target_doctype = meta.get("target_doctype") or ""
        file_name = meta.get("file_name") or ""
        row = {
            "docname": log.docname,
            "target_doctype": target_doctype,
            "file_name": file_name,
            "import_auto_file": meta.get("import_auto_file") or "",
            "step": meta.get("step"),
            "step_title": meta.get("step_title") or "",
            "created_at": str(log.creation or ""),
            "doc_url": f"/app/{target_doctype.lower().replace(' ', '-')}/{log.docname}" if target_doctype else "",
        }
        rows.append(row)
        if target_doctype:
            summary[target_doctype] = summary.get(target_doctype, 0) + 1

    return {
        "import_auto": doc.name,
        "file_row_name": file_row_name,
        "total": len(rows),
        "limit": limit,
        "truncated": len(rows) >= limit,
        "summary": summary,
        "rows": rows,
    }


@frappe.whitelist()
def get_import_audit(docname: str | None = None, file_row_name: str | None = None, limit: int = 500):
    doc = _get_import_doc(docname, permission_type="read")
    return _build_import_audit(doc, file_row_name, int(limit or 500))
