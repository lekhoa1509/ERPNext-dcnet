import json
from pathlib import Path

import frappe
from frappe import enqueue

from dcnet_migrate.import_auto.services.analysis import analysis_to_json, analyze_file
from dcnet_migrate.import_auto.services.duplicate_checker import (
    check_duplicates_for_row,
    determine_safety_status,
)
from dcnet_migrate.import_auto.services.excel import AI_SAMPLE_ROWS, summarize_workbook
from dcnet_migrate.import_auto.services.utils import file_fingerprint, scan_excel_files, truncate_text


PROGRESS_EVENT = "import_auto_progress"


def _list_importable_sheets(file_path: str) -> list[str]:
    """Sheet names with detectable tabular data (header row found).

    Used at scan time to split a multi-sheet workbook (e.g. one sheet per
    branch's department list) into one "Import Auto File" row per sheet.
    Single-sheet workbooks (the common case) and CSV files still yield
    exactly one sheet here, so their scan behaviour is unchanged.
    """
    try:
        summary = summarize_workbook(file_path, max_sample_rows=1, sample_strategy="first")
    except Exception:
        return []
    return [
        sheet["sheet_name"]
        for sheet in (summary.get("sheets") or [])
        if sheet.get("detected_header_row")
    ]


def _row_fingerprint(file_path: str, sheet_name: str | None) -> str:
    file_hash = file_fingerprint(file_path)
    return f"{file_hash}::{sheet_name}" if sheet_name else file_hash


def _scope_summary_to_sheet(summary: dict, sheet_name: str | None) -> dict:
    """Pin an already-summarized workbook to one sheet.

    Every Import Auto File row corresponds to exactly one sheet (see
    scan_files). Without this, analyze_file/analyze_with_ai would fall back
    to the workbook's physically-first sheet regardless of which sheet this
    row was scanned for — wrong for multi-sheet workbooks, and lets the AI
    "wander" to a different sheet than the row is pinned to.
    """
    if not sheet_name:
        return summary
    sheets = [s for s in (summary.get("sheets") or []) if s.get("sheet_name") == sheet_name]
    if not sheets:
        return summary
    return {**summary, "sheets": sheets}


def enqueue_scan_files(docname: str, requested_by: str | None = None) -> dict:
    return _enqueue_action(docname, "scan", requested_by)


def enqueue_analyze_files(docname: str, requested_by: str | None = None) -> dict:
    return _enqueue_action(docname, "analyze", requested_by)


def run_scan_files_job(docname: str, requested_by: str | None = None) -> None:
    _run_job(docname, requested_by, scan_files)


def run_analyze_files_job(docname: str, requested_by: str | None = None) -> None:
    _run_job(docname, requested_by, analyze_files)


def run_reanalyze_file_job(
    docname: str,
    file_row_name: str,
    user_feedback: str | None = None,
    requested_by: str | None = None,
    feedback_log_id: str | None = None,
    feedback_context: str | None = None,
) -> None:
    if requested_by:
        frappe.set_user(requested_by)
    try:
        reanalyze_file(docname, file_row_name, user_feedback, feedback_log_id=feedback_log_id, feedback_context=feedback_context)
    except Exception as exc:
        frappe.db.rollback()
        message = f"Phân tích lại thất bại: {truncate_text(str(exc), max_length=180)}"
        _update_feedback_history_for_row(
            file_row_name,
            feedback_log_id,
            {
                "status": "Failed",
                "ai_response": message,
                "error_detail": truncate_text(str(exc)),
                "responded_on": frappe.utils.now_datetime().isoformat(),
            },
        )
        frappe.db.commit()
        _publish_progress(
            docname,
            "reanalyze",
            0,
            0,
            message,
            current_file=file_row_name,
            status="failed",
            user=requested_by,
            persist=False,
        )
        frappe.log_error(frappe.get_traceback(), "Import Auto Reanalyze Failed")
        raise


def enqueue_reanalyze_file(docname: str, file_row_name: str, user_feedback: str | None = None, requested_by: str | None = None) -> dict:
    requested_by = requested_by or frappe.session.user

    parent = frappe.get_doc("Import Auto", docname)
    parent.check_permission("write")
    target_row = None
    for row in parent.files:
        if row.name == file_row_name:
            target_row = row
            break
    if not target_row:
        frappe.throw("Không tìm thấy dòng tệp cần phân tích lại.")

    feedback = (user_feedback or "").strip()
    feedback_log_entry = _make_feedback_history_entry(target_row, feedback, requested_by)
    feedback_history = _append_feedback_history(target_row.feedback_history_json, feedback_log_entry)
    feedback_context = _build_feedback_context(_parse_feedback_history(feedback_history))
    frappe.db.set_value(
        "Import Auto File",
        file_row_name,
        {
            "status": "Reanalyzing",
            "user_feedback": feedback or None,
            "feedback_history_json": feedback_history,
            "error_detail": None,
        },
        update_modified=False,
    )
    frappe.db.commit()

    _publish_progress(
        docname,
        "reanalyze",
        0,
        1,
        f"Đang phân tích lại: {target_row.file_name}",
        current_file=target_row.file_name,
        status="running",
        user=requested_by,
        persist=False,
        row_name=file_row_name,
        feedback_log_id=feedback_log_entry["id"],
    )

    job_id = f"import_auto::{docname}::reanalyze::{file_row_name}::{feedback_log_entry['id']}"
    enqueue(
        "dcnet_migrate.import_auto.services.processor.run_reanalyze_file_job",
        queue="long",
        timeout=900,
        job_id=job_id,
        deduplicate=True,
        enqueue_after_commit=True,
        docname=docname,
        file_row_name=file_row_name,
        user_feedback=feedback,
        requested_by=requested_by,
        feedback_log_id=feedback_log_entry["id"],
        feedback_context=feedback_context,
    )
    return {"queued": True, "job_id": job_id, "feedback_log_entry": feedback_log_entry}


def reanalyze_file(
    docname: str,
    file_row_name: str,
    user_feedback: str | None = None,
    feedback_log_id: str | None = None,
    feedback_context: str | None = None,
) -> dict:
    doc = frappe.get_doc("Import Auto", docname)
    doc.check_permission("write")

    target_row = None
    for row in doc.files:
        if row.name == file_row_name:
            target_row = row
            break
    if not target_row:
        frappe.throw("Không tìm thấy dòng tệp cần phân tích lại.")

    _publish_progress(
        docname,
        "reanalyze",
        0,
        1,
        f"Đang phân tích lại: {target_row.file_name}",
        current_file=target_row.file_name,
        status="running",
        persist=False,
        row_name=file_row_name,
    )

    try:
        summary = summarize_workbook(
            target_row.file_path,
            max_sample_rows=AI_SAMPLE_ROWS,
            sample_strategy="random",
            sample_seed=target_row.source_hash or target_row.file_path,
        )
        summary = _scope_summary_to_sheet(summary, target_row.sheet_name)
        analysis = analyze_file(doc, summary, user_feedback=feedback_context or user_feedback)
        target_row.import_order = analysis.get("import_order") or 999
        target_row.sheet_name = analysis.get("sheet_name")
        target_row.target_doctype = analysis.get("target_doctype")
        analysis_safety = analysis.get("safety_status")
        target_row.safety_status = analysis_safety
        target_row.row_count = _row_count(summary, analysis)
        target_row.confidence = analysis.get("confidence") or 0
        target_row.analysis_note = analysis.get("reason")
        target_row.analysis_json = analysis_to_json(analysis)
        target_row.error_detail = None if analysis_safety == "Safe" else analysis.get("reason")
        target_row.duplicate_check_status = "Pending"
        target_row.duplicate_match_count = 0
        target_row.duplicate_report_json = None
        if analysis_safety == "Safe":
            duplicate_report = check_duplicates_for_row(doc, target_row)
            target_row.duplicate_report_json = json.dumps(duplicate_report, ensure_ascii=False, indent=2, default=str)
            target_row.duplicate_match_count = duplicate_report.get("total_matches") or 0
            new_safety = determine_safety_status(analysis_safety, duplicate_report)
            target_row.safety_status = new_safety
            if new_safety == "Warning":
                target_row.duplicate_check_status = "Warning"
                warning_note = duplicate_report.get("note") or "Phát hiện dữ liệu trùng chính xác trong cơ sở dữ liệu."
                if target_row.analysis_note and warning_note not in target_row.analysis_note:
                    target_row.analysis_note = f"{target_row.analysis_note}\n{warning_note}"
                else:
                    target_row.analysis_note = warning_note
                target_row.error_detail = warning_note
            else:
                target_row.duplicate_check_status = "Clean"
        target_row.status = "Ready" if target_row.safety_status in ("Safe", "Warning") else "Error"
        if target_row.status == "Ready":
            _publish_progress(
                docname,
                "reanalyze",
                0,
                1,
                f"Đang tạo script import: {target_row.file_name}",
                current_file=target_row.file_name,
                status="running",
                persist=False,
                row_name=file_row_name,
            )
        for fieldname, value in _build_cached_smart_plan_fields(doc, target_row).items():
            setattr(target_row, fieldname, value)
        target_row.user_feedback = (user_feedback or "").strip() or None
        target_row.feedback_history_json = _complete_feedback_history(target_row.feedback_history_json, feedback_log_id, analysis)
        doc.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Import Auto Single File Reanalyze Failed")
        feedback_history = _update_feedback_history_for_row(
            file_row_name,
            feedback_log_id,
            {
                "status": "Failed",
                "ai_response": f"Phân tích lại thất bại: {truncate_text(str(exc))}",
                "error_detail": truncate_text(str(exc)),
                "responded_on": frappe.utils.now_datetime().isoformat(),
            },
        )
        frappe.db.set_value(
            "Import Auto File",
            file_row_name,
            {
                "status": "Error",
                "safety_status": "Error",
                "error_detail": truncate_text(str(exc)),
                "feedback_history_json": feedback_history,
            },
            update_modified=False,
        )
        frappe.db.commit()
        _publish_progress(
            docname,
            "reanalyze",
            1,
            1,
            f"Phân tích lại thất bại: {target_row.file_name}",
            current_file=target_row.file_name,
            status="failed",
            persist=False,
            row_name=file_row_name,
            feedback_log_id=feedback_log_id,
        )
        raise

    _publish_progress(
        docname,
        "reanalyze",
        1,
        1,
        f"Đã phân tích lại: {target_row.file_name}",
        current_file=target_row.file_name,
        status="complete",
        persist=False,
        row_name=file_row_name,
        feedback_log_id=feedback_log_id,
    )
    return {"row_name": file_row_name, "status": target_row.status}


def scan_files(docname: str) -> dict:
    doc = frappe.get_doc("Import Auto", docname)
    doc.check_permission("write")

    _publish_progress(docname, "scan", 0, 0, "Scanning folder...", status="running")
    reusable_rows = {
        row.source_hash: _existing_analysis_payload(row)
        for row in (doc.files or [])
        if row.source_hash and row.analysis_json and not getattr(row, "slot_key", None)
    }
    excel_files = scan_excel_files(doc.folder_path, doc.file_pattern, recursive=bool(doc.recursive))
    # Files uploaded through a master-data slot (see services/slot_import.py)
    # live under folder_path/slots/<slot_key>/ and are already fully analyzed
    # without AI. Never re-discover them here — that would either duplicate
    # them as a second, untagged row or (see below) delete them outright.
    excel_files = [f for f in excel_files if "/slots/" not in Path(f).as_posix()]

    # Multi-sheet support: a workbook with several tabular sheets (e.g. one
    # sheet per branch's department list) becomes one "Import Auto File" row
    # PER importable sheet, each independently analyzed/imported later.
    # Single-sheet workbooks and CSVs still produce exactly one row, so
    # existing single-sheet imports are unaffected.
    row_specs: list[tuple[str, str | None]] = []
    for file_path in excel_files:
        sheet_names = _list_importable_sheets(file_path)
        if sheet_names:
            row_specs.extend((file_path, sheet_name) for sheet_name in sheet_names)
        else:
            row_specs.append((file_path, None))

    # Slot-tagged rows are owned by slot_import.assign_slot_file() — drop only
    # the legacy/generic rows this folder-scan flow is about to rebuild.
    for row in list(doc.files or []):
        if not getattr(row, "slot_key", None):
            doc.remove(row)
    slot_count = len(doc.files or [])
    total = len(row_specs)
    for index, (file_path, sheet_name) in enumerate(row_specs, start=1):
        path = Path(file_path)
        label = f"{path.name} [{sheet_name}]" if sheet_name else path.name
        _publish_progress(docname, "scan", index, total, f"Found {label}", label, status="running")
        source_hash = _row_fingerprint(file_path, sheet_name)
        row_payload = {
            "file_name": path.name,
            "file_path": file_path,
            "sheet_name": sheet_name,
            "source_hash": source_hash,
            "safety_status": "Unknown",
            "status": "Scanned",
        }
        cached = reusable_rows.get(source_hash)
        if cached:
            row_payload.update(cached)
            row_payload["file_name"] = path.name
            row_payload["file_path"] = file_path
            row_payload["sheet_name"] = sheet_name
            row_payload["source_hash"] = source_hash
        doc.append(
            "files",
            row_payload,
        )

    scan_summary = (
        f"Không có file mới ngoài các ô danh mục — {slot_count} file đã được xử lý qua ô danh mục ở trên."
        if total == 0 and slot_count
        else f"Scanned {total} sheet(s) across {len(excel_files)} Excel file(s)."
    )
    doc.excel_file_count = len(doc.files)
    doc.progress_percent = 100
    doc.progress_message = scan_summary
    doc.processed_files = total
    doc.total_files = total
    doc.current_file = None
    doc.status = "Scanned"
    doc.summary_json = json.dumps(
        {"scanned_files": len(excel_files), "scanned_sheets": total}, ensure_ascii=False, indent=2
    )
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    _publish_progress(
        docname,
        "scan",
        total,
        total,
        scan_summary,
        status="complete",
    )
    return {"file_count": total}


def analyze_files(docname: str) -> dict:
    doc = frappe.get_doc("Import Auto", docname)
    doc.check_permission("write")

    if not doc.files:
        scan_files(docname)
        doc.reload()

    # Slot-tagged rows (services/slot_import.py) are already fully analyzed
    # without AI at upload time — never re-analyze or rebuild them here.
    rows_to_analyze = [row for row in doc.files if not getattr(row, "slot_key", None)]

    total_files = len(rows_to_analyze)
    existing_feedback = {
        (row.source_hash or row.file_path or row.file_name): {
            "user_feedback": row.user_feedback,
            "feedback_history_json": row.feedback_history_json,
        }
        for row in rows_to_analyze
    }
    doc.db_set("status", "Analyzing")
    _publish_progress(docname, "analyze", 0, total_files, "Starting fast file analysis...", status="running")
    analyzed_rows = []
    for index, row in enumerate(rows_to_analyze, start=1):
        feedback_state = existing_feedback.get(row.source_hash or row.file_path or row.file_name, {})
        if _can_reuse_analysis(row):
            row_payload = _existing_analysis_payload(row, feedback_state)
            if row_payload.get("duplicate_check_status") in (None, "Pending") and row_payload.get("safety_status") == "Safe":
                try:
                    proxy = frappe._dict(row_payload)
                    proxy.name = row.name
                    duplicate_report = check_duplicates_for_row(doc, proxy)
                    row_payload["duplicate_report_json"] = json.dumps(duplicate_report, ensure_ascii=False, indent=2, default=str)
                    row_payload["duplicate_match_count"] = duplicate_report.get("total_matches") or 0
                    new_safety = determine_safety_status(row_payload["safety_status"], duplicate_report)
                    row_payload["safety_status"] = new_safety
                    if new_safety == "Warning":
                        row_payload["duplicate_check_status"] = "Warning"
                        warning_note = duplicate_report.get("note") or "Phát hiện dữ liệu trùng chính xác trong cơ sở dữ liệu."
                        note = row_payload.get("analysis_note") or ""
                        row_payload["analysis_note"] = f"{note}\n{warning_note}".strip() if note else warning_note
                        row_payload["error_detail"] = warning_note
                    else:
                        row_payload["duplicate_check_status"] = "Clean"
                except Exception:
                    frappe.log_error(frappe.get_traceback(), "Import Auto Duplicate Check (Reuse) Failed")
                    row_payload["duplicate_check_status"] = "Pending"
            analyzed_rows.append(row_payload)
            _save_analyzed_row_progress(row.name, row_payload)
            _publish_progress(docname, "analyze", index, total_files, f"Reused analysis for {row.file_name}", row.file_name, "running")
            frappe.db.commit()
            continue

        _publish_progress(docname, "analyze", index - 1, total_files, f"Analyzing sample rows from {row.file_name}", row.file_name, "running")
        try:
            summary = summarize_workbook(
                row.file_path,
                max_sample_rows=AI_SAMPLE_ROWS,
                sample_strategy="first",
                sample_seed=row.source_hash or row.file_path,
            )
            summary = _scope_summary_to_sheet(summary, row.sheet_name)
            analysis = analyze_file(doc, summary)
            row_payload = {
                "file_name": row.file_name,
                "file_path": row.file_path,
                "source_hash": row.source_hash,
                "import_order": analysis.get("import_order") or 999,
                "sheet_name": analysis.get("sheet_name"),
                "target_doctype": analysis.get("target_doctype"),
                "safety_status": analysis.get("safety_status"),
                "row_count": _row_count(summary, analysis),
                "confidence": analysis.get("confidence") or 0,
                "analysis_note": analysis.get("reason"),
                "analysis_json": analysis_to_json(analysis),
                "error_detail": None if analysis.get("safety_status") == "Safe" else analysis.get("reason"),
                "user_feedback": feedback_state.get("user_feedback"),
                "feedback_history_json": feedback_state.get("feedback_history_json"),
                "duplicate_check_status": "Pending",
                "duplicate_match_count": 0,
                "duplicate_report_json": None,
            }
            row_payload["status"] = "Ready" if row_payload["safety_status"] in ("Safe", "Warning") else "Error"
            row_payload.update(_pending_smart_plan_fields())
            analyzed_rows.append(row_payload)
        except Exception as exc:
            frappe.log_error(frappe.get_traceback(), "Import Auto File Analysis Failed")
            analyzed_rows.append(
                {
                    "file_name": row.file_name,
                    "file_path": row.file_path,
                    "source_hash": row.source_hash,
                    "import_order": 999,
                    "safety_status": "Error",
                    "status": "Error",
                    "analysis_note": "Phân tích thất bại.",
                    "analysis_json": None,
                    "error_detail": truncate_text(str(exc)),
                    "smart_plan_status": "Error",
                    "smart_plan_error": truncate_text(str(exc)),
                    "user_feedback": feedback_state.get("user_feedback"),
                    "feedback_history_json": feedback_state.get("feedback_history_json"),
                    "duplicate_check_status": "Error",
                    "duplicate_match_count": 0,
                    "duplicate_report_json": None,
                }
            )
        _save_analyzed_row_progress(row.name, analyzed_rows[-1])
        _publish_progress(docname, "analyze", index, total_files, f"Analyzed {row.file_name}", row.file_name, "running")
        frappe.db.commit()

    analyzed_rows.sort(key=lambda item: (item.get("import_order") or 999, item.get("file_name") or ""))
    next_safe_order = 1
    for row in analyzed_rows:
        if row.get("safety_status") in ("Safe", "Warning"):
            row["import_order"] = next_safe_order
            next_safe_order += 1
        else:
            row["import_order"] = 999

    doc = frappe.get_doc("Import Auto", docname)
    # Only replace the rows this generic pipeline owns — slot-tagged rows
    # (services/slot_import.py) are already analyzed and must survive.
    for row in list(doc.files or []):
        if not getattr(row, "slot_key", None):
            doc.remove(row)
    slot_count = len(doc.files or [])
    for row in analyzed_rows:
        doc.append("files", row)

    safe_count = sum(1 for row in analyzed_rows if row.get("safety_status") == "Safe")
    warning_count = sum(1 for row in analyzed_rows if row.get("safety_status") == "Warning")
    error_count = len(analyzed_rows) - safe_count - warning_count
    analyze_summary = (
        f"Không có file mới ngoài các ô danh mục — {slot_count} file đã được phân tích sẵn khi upload vào ô danh mục."
        if not analyzed_rows and slot_count
        else f"Analyzed {len(analyzed_rows)} Excel file(s)."
    )
    doc.status = "Analyzed"
    doc.excel_file_count = len(doc.files)
    doc.progress_percent = 100
    doc.progress_message = analyze_summary
    doc.processed_files = len(analyzed_rows)
    doc.total_files = len(analyzed_rows)
    doc.current_file = None
    doc.summary_json = json.dumps(
        {
            "analyzed_files": len(analyzed_rows),
            "safe_files": safe_count,
            "warning_files": warning_count,
            "error_files": error_count,
            "import_rule": (
                "Phân tích nhanh bằng mapping local/AI trên sample đầu file. "
                "Khi bấm Import, hệ thống ưu tiên dùng mapping đã lưu để dựng script Python; "
                "AI chỉ lập lại kế hoạch nếu mapping phân tích chưa đủ."
            ),
        },
        ensure_ascii=False,
        indent=2,
    )
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    _publish_progress(
        docname,
        "analyze",
        len(analyzed_rows),
        len(analyzed_rows),
        analyze_summary,
        status="complete",
    )
    return {
        "file_count": len(analyzed_rows),
        "safe_count": safe_count,
        "warning_count": warning_count,
        "error_count": error_count,
    }


def _can_reuse_analysis(row) -> bool:
    return bool(
        getattr(row, "analysis_json", None)
        and getattr(row, "source_hash", None)
        and getattr(row, "target_doctype", None)
        and getattr(row, "safety_status", None) in ("Safe", "Warning")
        and getattr(row, "status", None) not in ("Reanalyzing", "Failed")
        and getattr(row, "smart_plan_status", None) != "Error"
    )


def _existing_analysis_payload(row, feedback_state: dict | None = None) -> dict:
    feedback_state = feedback_state or {}
    payload = {}
    for fieldname in (
        "file_name",
        "file_path",
        "source_hash",
        "import_order",
        "sheet_name",
        "target_doctype",
        "safety_status",
        "status",
        "row_count",
        "confidence",
        "data_import",
        "generated_file",
        "imported_records",
        "failed_records",
        "imported_on",
        "analysis_note",
        "analysis_json",
        "error_detail",
        "duplicate_check_status",
        "duplicate_match_count",
        "duplicate_report_json",
        "smart_plan_status",
        "smart_plan_json",
        "smart_plan_generated_on",
        "smart_plan_error",
    ):
        payload[fieldname] = getattr(row, fieldname, None)

    payload["user_feedback"] = feedback_state.get("user_feedback")
    payload["feedback_history_json"] = feedback_state.get("feedback_history_json")

    if not payload.get("smart_plan_status"):
        payload.update(_pending_smart_plan_fields())
    if not payload.get("duplicate_check_status"):
        payload["duplicate_check_status"] = "Pending"
        payload["duplicate_match_count"] = 0
        payload["duplicate_report_json"] = None
    return payload


def _pending_smart_plan_fields() -> dict:
    return {
        "smart_plan_status": "Pending",
        "smart_plan_json": None,
        "smart_plan_generated_on": None,
        "smart_plan_error": None,
    }


def _save_analyzed_row_progress(row_name: str | None, row_payload: dict) -> None:
    if not row_name or not frappe.db.exists("Import Auto File", row_name):
        return

    allowed_fields = {
        "import_order",
        "sheet_name",
        "target_doctype",
        "safety_status",
        "status",
        "row_count",
        "confidence",
        "data_import",
        "generated_file",
        "imported_records",
        "failed_records",
        "imported_on",
        "analysis_note",
        "analysis_json",
        "error_detail",
        "user_feedback",
        "feedback_history_json",
        "duplicate_check_status",
        "duplicate_match_count",
        "duplicate_report_json",
        "smart_plan_status",
        "smart_plan_json",
        "smart_plan_generated_on",
        "smart_plan_error",
    }
    updates = {
        fieldname: row_payload.get(fieldname)
        for fieldname in allowed_fields
        if fieldname in row_payload
    }
    if updates:
        frappe.db.set_value("Import Auto File", row_name, updates, update_modified=False)


def _build_cached_smart_plan_fields(doc, row_data) -> dict:
    """Create the import script plan saved on each Import Auto File row."""
    updates = _pending_smart_plan_fields()
    if _row_value(row_data, "safety_status") not in ("Safe", "Warning"):
        return updates
    if not _row_value(row_data, "target_doctype"):
        return updates

    try:
        from dcnet_migrate.import_auto.services.smart_planner import (
            build_smart_plan_from_analysis,
        )

        plan = build_smart_plan_from_analysis(doc, _smart_plan_row(row_data))
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Import Auto Smart Plan From Analysis Failed")
        plan = {"error": str(exc)}

    if plan.get("error"):
        error = truncate_text(plan.get("error"), max_length=1000)
        updates.update(
            {
                "smart_plan_status": "Error",
                "smart_plan_error": error,
                "safety_status": "Error",
                "status": "Error",
                "error_detail": error,
            }
        )
        return updates

    updates.update(
        {
            "smart_plan_status": "Ready",
            "smart_plan_json": json.dumps(plan, ensure_ascii=False, indent=2, default=str),
            "smart_plan_generated_on": frappe.utils.now_datetime(),
            "smart_plan_error": None,
        }
    )
    return updates


def _smart_plan_row(row_data) -> frappe._dict:
    fields = (
        "file_name",
        "file_path",
        "source_hash",
        "sheet_name",
        "target_doctype",
        "safety_status",
        "row_count",
        "analysis_json",
    )
    return frappe._dict({fieldname: _row_value(row_data, fieldname) for fieldname in fields})


def _row_value(row_data, fieldname: str):
    if isinstance(row_data, dict):
        return row_data.get(fieldname)
    if hasattr(row_data, "get"):
        return row_data.get(fieldname)
    return getattr(row_data, fieldname, None)


def _row_count(summary: dict, analysis: dict) -> int:
    sheet_name = analysis.get("sheet_name")
    for sheet in summary.get("sheets", []):
        if sheet.get("sheet_name") == sheet_name:
            header_row = int(analysis.get("header_row_number") or sheet.get("detected_header_row") or 1)
            return max(int(sheet.get("max_row") or 0) - header_row, 0)
    return 0


def _make_feedback_history_entry(row, feedback: str, requested_by: str | None) -> dict:
    now = frappe.utils.now_datetime().isoformat()
    user = requested_by or frappe.session.user
    full_name = frappe.db.get_value("User", user, "full_name") if user else None

    return {
        "id": frappe.generate_hash(length=10),
        "created_on": now,
        "user": user,
        "user_name": full_name or user,
        "feedback": feedback or "Yêu cầu phân tích lại không có ghi chú cụ thể.",
        "status": "Running",
        "file_name": row.file_name,
        "target_doctype_before": row.target_doctype,
        "safety_status_before": row.safety_status,
        "confidence_before": row.confidence,
        "ai_response": None,
    }


def _parse_feedback_history(history_json: str | None) -> list[dict]:
    if not history_json:
        return []

    try:
        history = json.loads(history_json)
    except Exception:
        return []

    return history if isinstance(history, list) else []


def _dump_feedback_history(history: list[dict]) -> str:
    return json.dumps(history, ensure_ascii=False, indent=2, default=str)


def _append_feedback_history(history_json: str | None, entry: dict) -> str:
    history = _parse_feedback_history(history_json)
    history.append(entry)
    return _dump_feedback_history(history)


def _build_feedback_context(history: list[dict]) -> str:
    if not history:
        return ""

    lines = [
        "Lịch sử góp ý của người dùng cho riêng file này. "
        "Hãy xem đây là context hội thoại, ưu tiên ý kiến mới nhất nhưng vẫn cân nhắc các phản hồi trước đó."
    ]
    for index, entry in enumerate(history, start=1):
        lines.append(f"Lần {index} - Người dùng: {entry.get('feedback') or ''}")
        if entry.get("ai_response"):
            lines.append(f"Lần {index} - Phản hồi AI trước đó: {entry.get('ai_response')}")

    return "\n".join(lines)


def _complete_feedback_history(history_json: str | None, feedback_log_id: str | None, analysis: dict) -> str:
    target_status = "Ready" if analysis.get("safety_status") == "Safe" else "Error"
    return _update_feedback_history(
        history_json,
        feedback_log_id,
        {
            "status": target_status,
            "responded_on": frappe.utils.now_datetime().isoformat(),
            "ai_response": analysis.get("reason") or "AI đã phân tích lại nhưng không trả về phần giải thích.",
            "target_doctype_after": analysis.get("target_doctype"),
            "safety_status_after": analysis.get("safety_status"),
            "confidence_after": analysis.get("confidence") or 0,
            "sheet_name": analysis.get("sheet_name"),
            "source": analysis.get("source"),
        },
    )


def _update_feedback_history(history_json: str | None, feedback_log_id: str | None, updates: dict) -> str:
    history = _parse_feedback_history(history_json)
    if feedback_log_id:
        for entry in history:
            if entry.get("id") == feedback_log_id:
                entry.update(updates)
                return _dump_feedback_history(history)

    if feedback_log_id:
        history.append({"id": feedback_log_id, **updates})
    return _dump_feedback_history(history)


def _update_feedback_history_for_row(file_row_name: str, feedback_log_id: str | None, updates: dict) -> str:
    history_json = frappe.db.get_value("Import Auto File", file_row_name, "feedback_history_json")
    updated_history = _update_feedback_history(history_json, feedback_log_id, updates)
    frappe.db.set_value(
        "Import Auto File",
        file_row_name,
        "feedback_history_json",
        updated_history,
        update_modified=False,
    )
    return updated_history


def _enqueue_action(docname: str, action: str, requested_by: str | None = None) -> dict:
    requested_by = requested_by or frappe.session.user
    current = frappe.db.get_value(
        "Import Auto",
        docname,
        ["status", "processed_files", "total_files"],
        as_dict=True,
    )
    if current and current.status in {"Scanning", "Analyzing", "Importing"}:
        message = f"{current.status} is already running. Waiting for background worker..."
        _publish_progress(
            docname,
            action,
            int(current.processed_files or 0),
            int(current.total_files or 0),
            message,
            status="queued",
            user=requested_by,
            persist=False,
        )
        return {"queued": True, "already_queued": True, "job_id": None}

    job_id = f"import_auto::{docname}::{action}"
    if _is_job_enqueued(job_id):
        message = "Job is already queued. Waiting for worker..."
        _publish_progress(docname, action, 0, 0, message, status="queued", user=requested_by, persist=False)
        return {"queued": True, "already_queued": True, "job_id": job_id}

    if action == "scan":
        method = "dcnet_migrate.import_auto.services.processor.run_scan_files_job"
        status = "Scanning"
        message = "Scan queued. Waiting for background worker..."
    else:
        method = "dcnet_migrate.import_auto.services.processor.run_analyze_files_job"
        status = "Analyzing"
        message = "Analysis queued. Waiting for background worker..."

    frappe.db.set_value(
        "Import Auto",
        docname,
        {
            "status": status,
            "progress_percent": 0,
            "progress_message": message,
            "processed_files": 0,
            "current_file": None,
        },
        update_modified=False,
    )
    _publish_progress(docname, action, 0, 0, message, status="queued", user=requested_by)
    enqueue(
        method,
        queue="long",
        timeout=3600,
        job_id=job_id,
        deduplicate=True,
        enqueue_after_commit=True,
        docname=docname,
        requested_by=requested_by,
    )
    return {"queued": True, "already_queued": False, "job_id": job_id}


def _run_job(docname: str, requested_by: str | None, runner) -> None:
    if requested_by:
        frappe.set_user(requested_by)

    try:
        runner(docname)
    except Exception as exc:
        frappe.db.rollback()
        message = f"Processing failed: {truncate_text(str(exc), max_length=180)}"
        frappe.db.set_value(
            "Import Auto",
            docname,
            {
                "status": "Failed",
                "progress_message": message,
                "current_file": None,
            },
            update_modified=False,
        )
        frappe.db.commit()
        _publish_progress(docname, "failed", 0, 0, message, status="failed", user=requested_by)
        frappe.log_error(frappe.get_traceback(), "Import Auto Background Job Failed")
        raise


def _is_job_enqueued(job_id: str) -> bool:
    try:
        from frappe.utils.background_jobs import is_job_enqueued

        return is_job_enqueued(job_id)
    except Exception:
        return False


def _publish_progress(
    docname: str,
    stage: str,
    processed: int,
    total: int,
    message: str,
    current_file: str | None = None,
    status: str = "running",
    user: str | None = None,
    persist: bool = True,
    row_name: str | None = None,
    feedback_log_id: str | None = None,
) -> None:
    percent = 100 if status == "complete" else (int((processed / total) * 100) if total else 0)
    payload = {
        "docname": docname,
        "stage": stage,
        "status": status,
        "processed": processed,
        "total": total,
        "percent": percent,
        "message": message,
        "current_file": current_file,
        "row_name": row_name,
        "feedback_log_id": feedback_log_id,
    }

    if persist:
        frappe.db.set_value(
            "Import Auto",
            docname,
            {
                "progress_percent": percent,
                "progress_message": message,
                "processed_files": processed,
                "total_files": total,
                "current_file": current_file,
            },
            update_modified=False,
        )
    frappe.publish_realtime(PROGRESS_EVENT, payload, user=user or frappe.session.user, after_commit=False)
