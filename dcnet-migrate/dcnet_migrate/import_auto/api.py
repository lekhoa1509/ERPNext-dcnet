"""Public API for worker/job status in dcnet_migrate.

Used by the frontend worker-notification panel to show active background jobs
and allow the user to cancel them.
"""

import frappe
from frappe import _


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _decode_rq_id(rq_id: str, site: str) -> str:
    """Convert a Redis job ID back to the original ``job_id`` string.

    Frappe's ``create_job_id`` does:
        job_id.replace(":", "|")  →  f"{site}||{encoded}"

    So decoding is: strip the site prefix then replace "|" → ":".
    """
    encoded = rq_id[len(site) + 2:]  # remove "site||"
    return encoded.replace("|", ":")


def _get_active_rq_job_ids() -> list[str]:
    """Return original job_ids (not RQ IDs) for all queued/started import_auto jobs."""
    try:
        from frappe.utils.background_jobs import get_queue

        site = frappe.local.site
        site_prefix = f"{site}||import_auto||"
        found = set()

        for queue_name in ("long", "default", "short"):
            try:
                q = get_queue(queue_name)
                for rq_id in q.get_job_ids():
                    if rq_id.startswith(site_prefix):
                        found.add(rq_id)
                for rq_id in q.started_job_registry.get_job_ids():
                    if rq_id.startswith(site_prefix):
                        found.add(rq_id)
            except Exception:
                pass

        return [_decode_rq_id(r, site) for r in sorted(found)]
    except Exception:
        frappe.log_error(frappe.get_traceback(), "dcnet_migrate.get_active_rq_job_ids")
        return []


_TYPE_META = {
    "scan":          ("Quét files",         "📁"),
    "analyze":       ("Phân tích AI",        "🤖"),
    "ob_analyze":    ("Phân tích số dư ĐK",  "🤖"),
    "smart_plan":    ("AI Lên kế hoạch",     "🧠"),
    "smart_execute": ("AI Import",           "📊"),
    "smart_fix":     ("AI Sửa lỗi",         "🔧"),
    "reanalyze":     ("Phân tích lại",       "🔄"),
}


def _build_job_info(job_id: str, docname: str, action: str, file_row_name: str | None) -> dict | None:
    type_label, icon = _TYPE_META.get(action, (action, "⚙️"))

    if action == "ob_analyze":
        ob = frappe.db.get_value(
            "Opening Balance Import",
            docname,
            ["name", "display_name", "company", "status"],
            as_dict=True,
        )
        if not ob:
            return None
        return {
            "job_id": job_id,
            "docname": docname,
            "label": ob.display_name or ob.company or docname,
            "type": action,
            "type_label": type_label,
            "icon": icon,
            "percent": 0,
            "message": "Đang phân tích file đầu kỳ...",
            "current_file": "",
            "processed": 0,
            "total": 0,
        }

    if action in ("scan", "analyze"):
        doc = frappe.db.get_value(
            "Import Auto",
            docname,
            ["name", "company", "progress_percent", "progress_message", "current_file",
             "processed_files", "total_files"],
            as_dict=True,
        )
        if not doc:
            return None
        return {
            "job_id": job_id,
            "docname": docname,
            "label": doc.company or docname,
            "type": action,
            "type_label": type_label,
            "icon": icon,
            "percent": int(doc.progress_percent or 0),
            "message": doc.progress_message or "",
            "current_file": doc.current_file or "",
            "processed": int(doc.processed_files or 0),
            "total": int(doc.total_files or 0),
        }

    if file_row_name:
        file_row = frappe.db.get_value(
            "Import Auto File",
            file_row_name,
            ["name", "file_name"],
            as_dict=True,
        )
        company = frappe.db.get_value("Import Auto", docname, "company") or docname
        if not file_row:
            return None
        file_name = file_row.file_name or file_row_name
        return {
            "job_id": job_id,
            "docname": docname,
            "label": company,
            "type": action,
            "type_label": f"{type_label}: {file_name}",
            "icon": icon,
            "percent": 0,
            "message": "",
            "current_file": file_name,
            "processed": 0,
            "total": 0,
        }

    return None


# ---------------------------------------------------------------------------
# Whitelisted methods
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_active_jobs():
    """Return active background import jobs for the notification panel."""
    job_ids = _get_active_rq_job_ids()
    if not job_ids:
        return []

    jobs = []
    for job_id in job_ids:
        parts = job_id.split("::")
        if len(parts) < 3 or parts[0] != "import_auto":
            continue
        docname = parts[1]
        action = parts[2]
        file_row_name = parts[3] if len(parts) > 3 else None
        try:
            info = _build_job_info(job_id, docname, action, file_row_name)
            if info:
                jobs.append(info)
        except Exception:
            pass

    return jobs


@frappe.whitelist()
def cancel_import_job(job_id):
    """Cancel a queued or running import_auto background job."""
    job_id = str(job_id or "").strip()
    if not job_id.startswith("import_auto::"):
        frappe.throw(_("Job ID không hợp lệ"))

    from frappe.utils.background_jobs import get_redis_conn
    from rq.command import send_stop_job_command
    from rq.exceptions import InvalidJobOperation, NoSuchJobError
    from rq.job import Job, JobStatus

    from frappe.utils.background_jobs import create_job_id

    rq_id = create_job_id(job_id)
    conn = get_redis_conn()
    cancelled_in_rq = False

    try:
        job = Job.fetch(rq_id, connection=conn)
        status = job.get_status(refresh=False)
        if status in (JobStatus.QUEUED, JobStatus.DEFERRED, JobStatus.SCHEDULED):
            job.cancel()
            cancelled_in_rq = True
        elif status == JobStatus.STARTED:
            try:
                send_stop_job_command(connection=conn, job_id=rq_id)
                cancelled_in_rq = True
            except InvalidJobOperation:
                pass
    except (NoSuchJobError, Exception):
        pass

    # Reset DB status regardless of RQ result
    parts = job_id.split("::")
    docname = parts[1] if len(parts) > 1 else None
    action = parts[2] if len(parts) > 2 else None
    file_row_name = parts[3] if len(parts) > 3 else None

    if docname and action:
        try:
            _reset_db_status(docname, action, file_row_name)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "cancel_import_job DB reset")

    return {"success": True, "cancelled_in_rq": cancelled_in_rq, "message": "Đã gửi lệnh hủy"}


def _reset_db_status(docname: str, action: str, file_row_name: str | None) -> None:
    if action == "scan":
        frappe.db.set_value("Import Auto", docname, {
            "status": "Draft",
            "progress_percent": 0,
            "progress_message": "Đã hủy bởi người dùng",
            "current_file": "",
        })
    elif action == "analyze":
        frappe.db.set_value("Import Auto", docname, {
            "status": "Scanned",
            "progress_percent": 0,
            "progress_message": "Đã hủy bởi người dùng",
            "current_file": "",
        })
    elif action in ("smart_plan", "smart_fix") and file_row_name:
        frappe.db.set_value("Import Auto File", file_row_name, {
            "smart_plan_status": "Error",
            "smart_plan_error": "Đã hủy bởi người dùng",
        })
    elif action == "smart_execute" and file_row_name:
        frappe.db.set_value("Import Auto File", file_row_name, {
            "status": "Failed",
            "error_detail": "Đã hủy bởi người dùng",
        })
    elif action == "reanalyze" and file_row_name:
        frappe.db.set_value("Import Auto File", file_row_name, {"status": "Analyzed"})

    frappe.db.commit()
