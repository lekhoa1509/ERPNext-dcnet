"""Misa Migration parse API — Phase B implementation."""

from __future__ import annotations

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st
from vn_accounting.misa_migration.jobs import parse_job


@frappe.whitelist()
def start_parse(batch_name: str, sync: bool = False) -> dict:
    """Parse all files in an UPLOADED batch.

    sync=True runs in-process (for tests + small files).
    sync=False (default) enqueues to RQ default queue.
    """
    status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    if status != st.UPLOADED:
        frappe.throw(_("Không thể parse ở trạng thái {0} — phải là UPLOADED.").format(status))

    if sync:
        # Sync = single process; tests + small files. parallel=False keeps
        # parse_file calls in-process so test sites without RQ workers still
        # complete.
        return parse_job.parse_batch(batch_name, parallel=False)

    # Async: parse_batch orchestrator runs on `default` queue and dispatches
    # per-file parse_file jobs to short/long queues for real parallelism.
    job = frappe.enqueue(
        "vn_accounting.misa_migration.jobs.parse_job.parse_batch",
        batch_name=batch_name,
        parallel=True,
        queue="default",
        timeout=14400,  # spec §8.1 JOB_TIMEOUT_SECONDS
    )
    frappe.db.set_value("Misa Migration Batch", batch_name, "job_id", job.id, update_modified=False)
    frappe.db.commit()
    return {"batch": batch_name, "queued": True, "job_id": job.id}


@frappe.whitelist()
def get_parse_progress(batch_name: str) -> dict:
    """Best-effort progress: row counts + file parse_status."""
    row_count = frappe.db.count("Misa Migration Row", {"batch": batch_name})
    files = frappe.db.sql(
        """SELECT name, file_type, parse_status, row_count, parse_error
           FROM `tabMisa Migration File` WHERE parent=%s""",
        (batch_name,), as_dict=1,
    )
    batch_status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    return {
        "batch": batch_name, "status": batch_status,
        "total_rows": row_count, "files": [dict(f) for f in files],
    }
