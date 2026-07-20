"""Watchdog: mark long-idle POSTING/REVERSING batches as STUCK.

Phase E commit 5. The Anthropic-API-stall pattern from
~/.claude/rules/multi-session.md (#18) and Frappe RQ-worker crashes both
manifest as a batch sitting in POSTING with no progress for many
minutes. Without watchdog the batch stays POSTING forever; user can't
Resume because Resume requires STUCK.

Idle threshold: 10 minutes since last `modified` timestamp on the
Misa Migration Batch row.  modified is bumped by post_job's chunk
commits (orchestrator sets posted_docs_count / failed_rows_count on the
batch) so a truly active post keeps the timestamp fresh.

Scheduled every 5 minutes via hooks.py:scheduler_events.cron. Manual
invocation: `bench --site <site> execute
vn_accounting.misa_migration.jobs.watchdog.check_stuck_batches`.
"""

from __future__ import annotations

import frappe

from vn_accounting.misa_migration import state as st


# Threshold per spec §8.6 + acceptance criterion #14. Phase E may make
# this configurable on Misa Migration Batch.
IDLE_THRESHOLD_MINUTES = 10

# File-level Parsing stuck-detection threshold. Parse worker bumps the
# Migration File row's modified timestamp every 500-row buffer flush
# (parse_job._publish + db.commit), so 5 minutes without an update is
# strong signal the worker died (SIGKILL, bench restart, OOM).
FILE_PARSE_IDLE_MINUTES = 5


def check_stuck_batches(idle_minutes: int = IDLE_THRESHOLD_MINUTES) -> dict:
    """Scan in-progress batches, mark idle ones as STUCK.

    Args:
      idle_minutes: idle threshold in minutes (default 10).

    Returns:
      {"checked": N, "marked_stuck": [{"batch", "minutes_idle"}, ...]}
    """
    rows = frappe.db.sql(
        f"""
        SELECT name, status, TIMESTAMPDIFF(MINUTE, modified, NOW()) AS minutes_idle
        FROM `tabMisa Migration Batch`
        WHERE status IN (%s, %s)
          AND TIMESTAMPDIFF(MINUTE, modified, NOW()) > %s
        """,
        (st.POSTING, st.REVERSING, idle_minutes),
        as_dict=True,
    )

    marked: list[dict] = []
    for r in rows:
        batch_name = r["name"]
        idle = r["minutes_idle"]
        try:
            batch = frappe.get_doc("Misa Migration Batch", batch_name)
            with st.lock_for_batch(batch):
                batch = frappe.get_doc("Misa Migration Batch", batch_name)
                # Status may have advanced between our query and the lock
                if batch.status not in (st.POSTING, st.REVERSING):
                    continue
                st.transition(
                    batch, st.STUCK,
                    reason=f"watchdog: no progress for {idle} minutes",
                )
                batch.save(ignore_permissions=True)
                frappe.db.commit()
            marked.append({"batch": batch_name, "minutes_idle": idle})
            try:
                frappe.publish_realtime(
                    "misa_migration:post_progress",
                    {"batch": batch_name, "status": st.STUCK,
                     "reason": f"watchdog: idle {idle} min"},
                    after_commit=True,
                )
            except Exception:
                pass
        except Exception as exc:
            frappe.log_error(
                title=f"Misa watchdog failed on {batch_name}",
                message=f"{type(exc).__name__}: {exc}",
            )

    return {"checked": len(rows), "marked_stuck": marked,
            "threshold_minutes": idle_minutes}


def check_stuck_files(idle_minutes: int = FILE_PARSE_IDLE_MINUTES) -> dict:
    """Mark file-level parse_status='Parsing' as Failed when worker stalled.

    Different layer from check_stuck_batches: that one fires on POSTING/
    REVERSING batch-level idle. This one fires on the per-file Migration
    File doc within a batch (the parser bumps the file row's `modified`
    every 500-row chunk). When the worker dies mid-parse (e.g. bench
    restart, SIGKILL, OOM), the file row is left at Parsing status forever.

    Marking Failed allows the operator to (a) see a clear error in the UI
    Lỗi column, and (b) re-trigger parse — the idempotent skip in
    parse_job will pick up only the Failed files for retry, preserving
    progress on the already-Parsed ones.
    """
    rows = frappe.db.sql(
        """
        SELECT mf.name, mf.parent AS batch, mf.original_filename, mf.row_count,
               TIMESTAMPDIFF(MINUTE, mf.modified, NOW()) AS minutes_idle
        FROM `tabMisa Migration File` mf
        JOIN `tabMisa Migration Batch` mb ON mb.name = mf.parent
        WHERE mf.parse_status = 'Parsing'
          AND mb.status = 'UPLOADED'
          AND TIMESTAMPDIFF(MINUTE, mf.modified, NOW()) > %s
        """,
        (idle_minutes,),
        as_dict=True,
    )

    marked: list[dict] = []
    for r in rows:
        try:
            frappe.db.sql(
                """UPDATE `tabMisa Migration File`
                   SET parse_status = 'Failed',
                       parse_error  = %s,
                       modified     = NOW()
                   WHERE name = %s AND parse_status = 'Parsing'""",
                (
                    f"Watchdog: worker stalled — no progress in {r['minutes_idle']}min "
                    f"(stopped at row {r['row_count']}). "
                    "Bấm 'Bắt đầu phân tích' để retry file này.",
                    r["name"],
                ),
            )
            frappe.db.commit()
            marked.append({
                "file": r["name"], "filename": r["original_filename"],
                "batch": r["batch"], "minutes_idle": r["minutes_idle"],
                "row_count": r["row_count"],
            })
            try:
                frappe.publish_realtime(
                    "misa_migration:parse_progress",
                    {"batch": r["batch"], "file": r["name"], "status": "failed",
                     "error": f"watchdog: idle {r['minutes_idle']}min"},
                    after_commit=True,
                )
            except Exception:
                pass
        except Exception as exc:
            frappe.log_error(
                title=f"Misa watchdog check_stuck_files failed on {r['name']}",
                message=f"{type(exc).__name__}: {exc}",
            )

    return {"checked": len(rows), "marked_failed": marked,
            "threshold_minutes": idle_minutes}
