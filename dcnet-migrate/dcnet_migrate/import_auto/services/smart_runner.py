"""Background runner for AI smart plan generation.

Smart plans can be slow (large files, long AI calls). To avoid HTTP/gunicorn
timeouts we enqueue the plan request and push progress + result to the user
via ``frappe.publish_realtime``. The frontend listens on
``import_auto_smart_plan`` and renders a progress dialog until the plan is
delivered.
"""

from __future__ import annotations

import json

import frappe
from frappe import enqueue


SMART_PLAN_EVENT = "import_auto_smart_plan"
SMART_EXECUTE_EVENT = "import_auto_smart_execute"
AUXILIARY_PLAN_DOCTYPES = {
    "Address",
    "Brand",
    "Contact",
    "Customer Group",
    "Item Group",
    "Supplier Group",
    "Territory",
    "UOM",
}


def enqueue_smart_plan(docname: str, file_row_name: str, user_feedback: str | None = None,
                      requested_by: str | None = None) -> dict:
    requested_by = requested_by or frappe.session.user
    job_id = f"import_auto::{docname}::smart_plan::{file_row_name}"

    enqueue(
        "dcnet_migrate.import_auto.services.smart_runner.run_smart_plan_job",
        queue="long",
        timeout=900,
        job_id=job_id,
        deduplicate=True,
        enqueue_after_commit=True,
        docname=docname,
        file_row_name=file_row_name,
        user_feedback=user_feedback,
        requested_by=requested_by,
    )
    publish_smart_plan_progress(
        docname,
        file_row_name,
        stage="queued",
        percent=2,
        message="Đã đưa vào hàng đợi, AI sẽ bắt đầu ngay...",
        user=requested_by,
    )
    return {"queued": True, "job_id": job_id}


def run_smart_plan_job(docname: str, file_row_name: str,
                      user_feedback: str | None = None,
                      requested_by: str | None = None) -> None:
    if requested_by:
        frappe.set_user(requested_by)

    publish_smart_plan_progress(
        docname,
        file_row_name,
        stage="reading",
        percent=10,
        message="Đang đọc lại tệp Excel...",
        user=requested_by,
    )

    try:
        doc = frappe.get_doc("Import Auto", docname)
        doc.check_permission("write")
        target_row = next((r for r in doc.files if r.name == file_row_name), None)
        if not target_row:
            raise ValueError("Không tìm thấy dòng tệp.")

        publish_smart_plan_progress(
            docname,
            file_row_name,
            stage="thinking",
            percent=35,
            message="AI đang phân tích 10 dòng mẫu random để tạo mapping/script...",
            file_name=target_row.file_name,
            user=requested_by,
        )

        from dcnet_migrate.import_auto.services.smart_planner import build_smart_plan

        plan = build_smart_plan(doc, target_row, user_feedback=user_feedback)
        _store_smart_plan_result(file_row_name, plan)

        publish_smart_plan_progress(
            docname,
            file_row_name,
            stage="materialising",
            percent=80,
            message="Đang chuẩn hoá script import Python cho từng bước...",
            file_name=target_row.file_name,
            user=requested_by,
        )

        target_doctype = _primary_plan_target_doctype(plan) or target_row.target_doctype
        result = {
            "docname": docname,
            "row_name": file_row_name,
            "file_name": target_row.file_name,
            "target_doctype": target_doctype,
            "plan": plan,
            "status": "complete" if not plan.get("error") else "failed",
            "stage": "complete" if not plan.get("error") else "failed",
            "percent": 100,
            "message": plan.get("error") or "Đã tạo mapping/script import. AI sẽ không xử lý phần dữ liệu còn lại.",
        }
        _publish(result, requested_by)
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Import Auto Smart Plan Job Failed")
        _publish({
            "docname": docname,
            "row_name": file_row_name,
            "status": "failed",
            "stage": "failed",
            "percent": 100,
            "message": f"Tạo kế hoạch thất bại: {exc}",
            "plan": {"error": str(exc)},
        }, requested_by)
        raise


def publish_smart_plan_progress(docname: str, file_row_name: str, stage: str,
                                percent: int, message: str,
                                file_name: str | None = None,
                                user: str | None = None) -> None:
    payload = {
        "docname": docname,
        "row_name": file_row_name,
        "file_name": file_name,
        "status": "running",
        "stage": stage,
        "percent": percent,
        "message": message,
    }
    _publish(payload, user)


def _publish(payload: dict, user: str | None) -> None:
    try:
        frappe.publish_realtime(SMART_PLAN_EVENT, payload,
                                user=user or frappe.session.user,
                                after_commit=False)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Plan Publish Failed")


def _store_smart_plan_result(file_row_name: str, plan: dict) -> None:
    if not file_row_name:
        return

    if plan.get("error"):
        updates = {
            "smart_plan_status": "Error",
            "smart_plan_error": plan.get("error"),
            "smart_plan_json": None,
            "smart_plan_generated_on": None,
        }
    else:
        target_doctype = _primary_plan_target_doctype(plan)
        updates = {
            "smart_plan_status": "Ready",
            "smart_plan_error": None,
            "smart_plan_json": json.dumps(plan, ensure_ascii=False, indent=2, default=str),
            "smart_plan_generated_on": frappe.utils.now_datetime(),
        }
        if target_doctype:
            updates["target_doctype"] = target_doctype
            current_safety = frappe.db.get_value("Import Auto File", file_row_name, "safety_status")
            if current_safety not in ("Safe", "Warning"):
                updates["safety_status"] = "Warning"
                updates["error_detail"] = None
                if plan.get("plan_summary"):
                    updates["analysis_note"] = plan.get("plan_summary")

    try:
        frappe.db.set_value("Import Auto File", file_row_name, updates, update_modified=False)
        frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Plan Cache Save Failed")


def _primary_plan_target_doctype(plan: dict) -> str | None:
    """Pick a display target DocType from a generated multi-step plan."""
    if not isinstance(plan, dict):
        return None

    steps = [step for step in (plan.get("steps") or []) if isinstance(step, dict)]
    if not steps:
        return None

    usable_steps = [step for step in steps if step.get("target_doctype")]
    primary_steps = [
        step for step in usable_steps
        if step.get("target_doctype") not in AUXILIARY_PLAN_DOCTYPES
    ]
    picked = (primary_steps[-1] if primary_steps else (usable_steps[0] if usable_steps else None))
    return picked.get("target_doctype") if picked else None


# ---------------------------------------------------------------------------
# Smart execute runner — background job with realtime result delivery.
# ---------------------------------------------------------------------------


def enqueue_smart_execute(docname: str, file_row_name: str, plan_json: str,
                          requested_by: str | None = None) -> dict:
    requested_by = requested_by or frappe.session.user
    job_id = f"import_auto::{docname}::smart_execute::{file_row_name}"

    # Use a short statement_timeout so the HTTP request never waits >5s on a locked
    # tabImport Auto row (can happen when a running background job holds a write lock).
    try:
        frappe.db.set_value(
            "Import Auto",
            docname,
            {
                "status": "Importing",
                "progress_percent": 0,
                "progress_message": "Smart Import queued. Waiting for background worker...",
                "current_file": file_row_name,
            },
            update_modified=False,
        )
    except frappe.QueryTimeoutError:
        # Row is locked by a running background job — the job is already in progress,
        # so just proceed to (re-)enqueue without resetting status.
        pass

    enqueue(
        "dcnet_migrate.import_auto.services.smart_runner.run_smart_execute_job",
        queue="long",
        timeout=7200,
        job_id=job_id,
        deduplicate=True,
        enqueue_after_commit=True,
        docname=docname,
        file_row_name=file_row_name,
        plan_json=plan_json,
        requested_by=requested_by,
    )
    _publish_execute({
        "docname": docname,
        "row_name": file_row_name,
        "status": "running",
        "stage": "queued",
        "percent": 2,
        "message": "Đã đưa script import vào hàng đợi nền...",
    }, requested_by)
    return {"queued": True, "job_id": job_id}


def run_smart_execute_job(docname: str, file_row_name: str,
                          plan_json: str,
                          requested_by: str | None = None) -> None:
    if requested_by:
        frappe.set_user(requested_by)

    try:
        doc = frappe.get_doc("Import Auto", docname)
        doc.check_permission("write")
        target_row = next((r for r in doc.files if r.name == file_row_name), None)
        if not target_row:
            raise ValueError("Không tìm thấy dòng tệp.")

        _publish_execute({
            "docname": docname,
            "row_name": file_row_name,
            "file_name": target_row.file_name,
            "status": "running",
            "stage": "reading",
            "percent": 10,
            "message": "Đang đọc Excel và mở rộng script import...",
        }, requested_by)

        from dcnet_migrate.import_auto.doctype.import_auto.import_auto import (
            _execute_smart_plan_now,
        )

        _publish_execute({
            "docname": docname,
            "row_name": file_row_name,
            "file_name": target_row.file_name,
            "status": "running",
            "stage": "executing",
            "percent": 30,
            "message": "Python đang import từng dòng bằng savepoint...",
        }, requested_by)

        def progress_callback(payload: dict) -> None:
            event = {
                "docname": docname,
                "row_name": file_row_name,
                "file_name": target_row.file_name,
                "status": "running",
                **(payload or {}),
            }
            _publish_execute(event, requested_by)

            # Keep the parent form's global progress fields roughly in sync.
            # Commit after each update to release the write lock on tabImport Auto —
            # holding an open write lock for the entire 5k+ row transaction blocks
            # subsequent HTTP requests with QueryTimeoutError (innodb_lock_wait_timeout=50s).
            try:
                if event.get("total_records"):
                    frappe.db.set_value(
                        "Import Auto",
                        docname,
                        {
                            "progress_percent": int(event.get("percent") or 0),
                            "progress_message": (event.get("message") or "")[:180],
                            "processed_files": int(event.get("total_processed") or 0),
                            "total_files": int(event.get("total_records") or 0),
                            "current_file": target_row.file_name,
                        },
                        update_modified=False,
                    )
                    frappe.db.commit()
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Smart Execute Progress Persist Failed")

        result = _execute_smart_plan_now(
            doc,
            file_row_name,
            plan_json,
            progress_callback=progress_callback,
        )
        status = "complete" if result.get("ok") else "failed"
        if status == "failed" and not result.get("can_resume"):
            frappe.db.set_value(
                "Import Auto File",
                file_row_name,
                {
                    "status": "Failed",
                    "error_detail": (result.get("error") or "Import thất bại.")[:1000],
                },
                update_modified=False,
            )
            frappe.db.set_value(
                "Import Auto",
                docname,
                {
                    "status": "Failed",
                    "progress_percent": 100,
                    "progress_message": (result.get("error") or "Smart Import failed.")[:180],
                    "current_file": None,
                },
                update_modified=False,
            )
            frappe.db.commit()
        _publish_execute({
            "docname": docname,
            "row_name": file_row_name,
            "file_name": target_row.file_name,
            "status": status,
            "stage": status,
            "percent": 100,
            "message": result.get("error") or "Import nền đã hoàn tất.",
            "result": result,
        }, requested_by)
    except Exception as exc:
        frappe.db.rollback()
        error_text = str(exc)
        try:
            frappe.db.set_value(
                "Import Auto File",
                file_row_name,
                {
                    "status": "Failed",
                    "error_detail": error_text[:1000],
                },
                update_modified=False,
            )
            frappe.db.set_value(
                "Import Auto",
                docname,
                {
                    "status": "Failed",
                    "progress_percent": 100,
                    "progress_message": f"Smart Import failed: {error_text[:180]}",
                    "current_file": None,
                },
                update_modified=False,
            )
            frappe.db.commit()
        except Exception:
            frappe.db.rollback()

        frappe.log_error(frappe.get_traceback(), "Import Auto Smart Execute Job Failed")
        _publish_execute({
            "docname": docname,
            "row_name": file_row_name,
            "status": "failed",
            "stage": "failed",
            "percent": 100,
            "message": f"Import thất bại: {error_text}",
            "result": {"ok": False, "error": error_text},
        }, requested_by)
        raise


def _publish_execute(payload: dict, user: str | None) -> None:
    try:
        frappe.publish_realtime(SMART_EXECUTE_EVENT, payload,
                                user=user or frappe.session.user,
                                after_commit=False)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Execute Publish Failed")


# ---------------------------------------------------------------------------
# Smart fix runner — background job with realtime progress events.
# ---------------------------------------------------------------------------

SMART_FIX_EVENT = "import_auto_smart_fix"


def enqueue_smart_fix(docname: str, file_row_name: str, plan_json: str,
                      error_json: str, requested_by: str | None = None) -> dict:
    requested_by = requested_by or frappe.session.user
    job_id = f"import_auto::{docname}::smart_fix::{file_row_name}"

    enqueue(
        "dcnet_migrate.import_auto.services.smart_runner.run_smart_fix_job",
        queue="long",
        timeout=900,
        job_id=job_id,
        deduplicate=True,
        enqueue_after_commit=True,
        docname=docname,
        file_row_name=file_row_name,
        plan_json=plan_json,
        error_json=error_json,
        requested_by=requested_by,
    )
    _publish_fix({
        "docname": docname,
        "row_name": file_row_name,
        "status": "running",
        "stage": "queued",
        "percent": 2,
        "message": "Đã đưa vào hàng đợi, AI sẽ bắt đầu ngay...",
    }, requested_by)
    return {"queued": True, "job_id": job_id}


def run_smart_fix_job(docname: str, file_row_name: str,
                      plan_json: str, error_json: str,
                      requested_by: str | None = None) -> None:
    if requested_by:
        frappe.set_user(requested_by)

    try:
        doc = frappe.get_doc("Import Auto", docname)
        doc.check_permission("write")
        target_row = next((r for r in doc.files if r.name == file_row_name), None)
        if not target_row:
            raise ValueError("Không tìm thấy dòng tệp.")

        try:
            plan = frappe.parse_json(plan_json) if plan_json else {}
        except Exception:
            plan = {}
        try:
            error_info = frappe.parse_json(error_json) if error_json else {}
        except Exception:
            error_info = {}
        if not isinstance(error_info, dict):
            error_info = {}

        from dcnet_migrate.import_auto.services.smart_planner import fix_plan_errors

        def progress(stage: str, percent: int, message: str):
            _publish_fix({
                "docname": docname,
                "row_name": file_row_name,
                "file_name": target_row.file_name,
                "status": "running",
                "stage": stage,
                "percent": percent,
                "message": message,
            }, requested_by)

        result = fix_plan_errors(doc, target_row, plan, error_info,
                                 progress_callback=progress)

        final = {
            "docname": docname,
            "row_name": file_row_name,
            "file_name": target_row.file_name,
            "percent": 100,
            "message": result.get("error") or "AI đã đề xuất các sửa đổi.",
            "status": "failed" if result.get("error") else "complete",
            "stage": "failed" if result.get("error") else "complete",
            "result": result,
        }
        _publish_fix(final, requested_by)
    except Exception as exc:
        frappe.log_error(frappe.get_traceback(), "Import Auto Smart Fix Job Failed")
        _publish_fix({
            "docname": docname,
            "row_name": file_row_name,
            "status": "failed",
            "stage": "failed",
            "percent": 100,
            "message": f"Sửa thất bại: {exc}",
            "result": {"error": str(exc)},
        }, requested_by)
        raise


def _publish_fix(payload: dict, user: str | None) -> None:
    try:
        frappe.publish_realtime(SMART_FIX_EVENT, payload,
                                user=user or frappe.session.user,
                                after_commit=False)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Smart Fix Publish Failed")
