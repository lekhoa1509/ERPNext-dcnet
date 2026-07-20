"""Auto-pipeline API — one-shot migration endpoints for the hub UI.

The hub's simplified flow: operator picks company + drops files + clicks
ONE button. These endpoints start/poll/resume the background pipeline
(jobs/auto_pipeline.py) that chains parse → masters → preflight → post →
validate without further clicks.
"""

from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st

DOCTYPE_BATCH = "Misa Migration Batch"
PIPELINE_TIMEOUT = 6 * 3600  # full-year batches post for a long time


def _enqueue(batch_name: str, skip_warnings: bool) -> str | None:
    # Queue choice matters: the parse stage dispatches BIG files (NKC/SCT/
    # Bảng kê) onto the `long` queue and polls for them. If this pipeline
    # job also sat on `long`, those parse jobs would queue BEHIND it on the
    # single long worker → the poll never completes. Pipeline lives on
    # `default`; big parses on `long`; small parses on `short`.
    job = frappe.enqueue(
        "vn_accounting.misa_migration.jobs.auto_pipeline.run_auto_pipeline",
        batch_name=batch_name,
        skip_warnings=skip_warnings,
        queue="default",
        timeout=PIPELINE_TIMEOUT,
        job_name=f"misa_auto_pipeline::{batch_name}",
    )
    return getattr(job, "id", None)


@frappe.whitelist()
def start_auto(batch_name: str, skip_warnings: int = 1) -> dict[str, Any]:
    """Kick off the end-to-end pipeline on an UPLOADED batch.

    Also accepts PARSED / REVIEWED (resume after blocker fix or a prior
    partial run) — the job enters at the right stage by status."""
    if not batch_name or not frappe.db.exists(DOCTYPE_BATCH, batch_name):
        frappe.throw(_("Batch không tồn tại: {0}").format(batch_name))
    status = frappe.db.get_value(DOCTYPE_BATCH, batch_name, "status")
    if status not in (st.UPLOADED, st.PARSED, st.REVIEWED):
        frappe.throw(
            _("Không thể chạy pipeline ở trạng thái {0}.").format(status))

    job_id = _enqueue(batch_name, bool(frappe.utils.cint(skip_warnings)))
    frappe.db.set_value(DOCTYPE_BATCH, batch_name, "job_id", job_id or "",
                        update_modified=False)
    return {"batch": batch_name, "job_id": job_id, "status": status}


@frappe.whitelist()
def get_pipeline(batch_name: str) -> dict[str, Any] | None:
    """Poll payload for the hub: batch core fields + parsed pipeline_json
    + live post counters when the post stage is running."""
    if not batch_name or not frappe.db.exists(DOCTYPE_BATCH, batch_name):
        return None
    b = frappe.db.get_value(
        DOCTYPE_BATCH, batch_name,
        ["name", "company", "batch_title", "status", "total_rows",
         "posted_docs_count", "failed_rows_count", "pipeline_json",
         "ob_posting_date", "modified"],
        as_dict=True,
    )
    try:
        pipeline = json.loads(b.pop("pipeline_json") or "null")
    except Exception:
        pipeline = None
    b["pipeline"] = pipeline

    # Dead-job detection: every pipeline write bumps batch.modified. A
    # stage stuck at "running" with no write for minutes = the worker died
    # (bench restart, OOM). UI shows "Chạy tiếp" instead of spinning forever.
    import datetime as _dt
    mod = b.pop("modified", None)
    try:
        b["seconds_since_update"] = int(
            (_dt.datetime.now() - mod).total_seconds()) if mod else None
    except Exception:
        b["seconds_since_update"] = None

    # Row-status counters give the operator live "x/y" numbers during the
    # long stages without a second round trip.
    rows = frappe.db.sql(
        """SELECT status, COUNT(*) FROM `tabMisa Migration Row`
           WHERE batch=%s GROUP BY status""",
        (batch_name,),
    )
    b["row_counts"] = {r[0]: r[1] for r in rows}
    return b


@frappe.whitelist()
def resume_after_stuck(batch_name: str) -> dict[str, Any]:
    """Recover a STUCK batch back to its nearest resumable status and
    re-run the pipeline from there. STUCK → REVIEWED khi đã có rows Ready
    (post lại), STUCK → UPLOADED khi parse chưa xong."""
    if not batch_name or not frappe.db.exists(DOCTYPE_BATCH, batch_name):
        frappe.throw(_("Batch không tồn tại: {0}").format(batch_name))
    batch = frappe.get_doc(DOCTYPE_BATCH, batch_name)
    if batch.status != st.STUCK:
        frappe.throw(_("Batch không ở trạng thái STUCK."))

    # Resume target by FILE state, not row count: a parse that died mid-file
    # leaves partial rows — counting rows would wrongly jump to REVIEWED and
    # post HALF the NKC. Any non-Parsed file → back to UPLOADED (parse_batch
    # skips Parsed files; parse_file wipes its own partial rows first).
    n_unparsed = frappe.db.count(
        "Misa Migration File",
        {"parent": batch_name, "parse_status": ["!=", "Parsed"]},
    )
    # All parsed → PARSED (re-runs masters + preflight, both idempotent)
    # rather than REVIEWED — jumping straight to post would skip the
    # account/danh mục setup when the crash happened during masters.
    target = st.UPLOADED if n_unparsed else st.PARSED
    with st.lock_for_batch(batch):
        batch = frappe.get_doc(DOCTYPE_BATCH, batch_name)
        st.transition(batch, target, reason="auto-pipeline resume after STUCK")
        batch.save(ignore_permissions=True)
        frappe.db.commit()
    return start_auto(batch_name)
