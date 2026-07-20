"""Post job — create ERPNext docs from Ready rows.

REVIEWED → POSTING → POSTED (or STUCK on fatal error). Per-row try/except
in BaseImporter.post_row already shields one bad row from killing the
whole batch. Chunked commit handled by orchestrator.run_post (per
file_type group).

Server-load cap: Phase 0 (opening_asset FA/CCDC) and Phase 4 (NKC/phát
sinh) each cap themselves at ~200 rows per call (see their
`max_rows_per_run` params) so one worker doesn't monopolize hours posting
a huge batch in a single unbroken run. When either phase reports
`complete=False`, post_batch re-enqueues itself and returns immediately
(status stays POSTING) instead of proceeding to submit/backfill — the
worker is released back to the pool between chunks. A resumed call skips
the REVIEWED→POSTING transition since the batch is already POSTING.
"""

from __future__ import annotations

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st
from vn_accounting.misa_migration.importers.orchestrator import run_post
from vn_accounting.misa_migration.importers.phase_0_orchestrator import (
    run_phase_0_post,
)
from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
    run_phase_4_post,
    submit_phase_4_drafts,
)


PROGRESS_EVENT = "misa_migration:post_progress"

# Server-load cap for the normal "operator clicks Post" flow. Direct/bulk
# callers of run_phase_0_post / run_phase_4_post (tests, bulk_pump) are
# unaffected — their functions default max_rows_per_run to None (unlimited,
# legacy single-pass behaviour) unless explicitly overridden.
MAX_ROWS_PER_RUN = 200


def _reenqueue_post_batch(batch_name: str, auto_submit: bool) -> None:
    """Queue a follow-up post_batch call to continue a chunked Phase 0/4
    run. Uses the same shard-derived queue the batch was originally
    posted on (falls back to "default") so the continuation doesn't jump
    queues mid-batch."""
    shard_token = frappe.db.get_value("Misa Migration Batch", batch_name, "shard_token")
    from vn_accounting.misa_migration.api.post import _resolve_post_queue
    rq_queue = _resolve_post_queue(shard_token)
    frappe.enqueue(
        "vn_accounting.misa_migration.jobs.post_job.post_batch",
        batch_name=batch_name, auto_submit=auto_submit,
        queue=rq_queue, timeout=14400,
    )


def _partial_result(batch_name: str, summary: dict, resuming_phase: str) -> dict:
    try:
        frappe.publish_realtime(PROGRESS_EVENT, {
            "batch": batch_name, "status": st.POSTING, "summary": summary,
            "partial": True, "resuming_phase": resuming_phase,
        }, after_commit=False)
    except Exception:
        pass
    return {"batch": batch_name, "status": st.POSTING, "summary": summary,
            "partial": True, "resuming_phase": resuming_phase}


def post_batch(batch_name: str, auto_submit: bool = True) -> dict:
    """Run post phase on a REVIEWED (or resuming POSTING) batch.
       REVIEWED → POSTING → POSTED (success) or STUCK (any unhandled exc).

    UX Gap 3: when `auto_submit=True` (default), the per-doc
    `submit_phase_4_drafts` pass runs AFTER all Phase 0+4 inserts so
    operator gets submitted (docstatus=1) docs in one Post click —
    matching the natural meaning of "Đăng vào ERPNext" (publish to
    accounting GL). Set `auto_submit=False` to leave drafts at
    docstatus=0 (e.g. for inspect-before-submit workflows).
    """
    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    if batch.status not in (st.REVIEWED, st.POSTING):
        frappe.throw(
            _("Không thể post ở trạng thái {0} — phải là REVIEWED.").format(batch.status)
        )

    # A resumed chunked run re-enters with status already POSTING — skip
    # the transition (it's not a REVIEWED→POSTING edge on resume).
    if batch.status == st.REVIEWED:
        with st.lock_for_batch(batch):
            batch = frappe.get_doc("Misa Migration Batch", batch_name)
            st.transition(batch, st.POSTING, reason="post_batch started")
            batch.save(ignore_permissions=True)
            frappe.db.commit()

    try:
        summary = run_post(batch_name)
        # Phase 0 — Opening Balance (runs AFTER Phase 1+2+3 masters are
        # ready, BEFORE Phase 4 transactions). Posts to Dec 31 of prior
        # year so T1/2026 transactions build on real opening balances.
        # Capped at ~200 new Assets/run (FA+CCDC) — re-enqueue and stop
        # here if there's more left, before touching Phase 4 at all.
        phase_0_summary = run_phase_0_post(batch_name, max_rows_per_run=MAX_ROWS_PER_RUN)
        summary["__phase_0__"] = phase_0_summary
        if not phase_0_summary.get("complete", True):
            _reenqueue_post_batch(batch_name, auto_submit)
            return _partial_result(batch_name, summary, "phase_0")

        # Phase 4 — dispatch NKC/BR/MV vouchers through the router. The
        # phase_4 summary has a different shape; we keep it under a
        # separate top-level key. Capped at ~200 vouchers/run — re-enqueue
        # and stop here (before submit/backfill) if there's more left.
        phase_4_summary = run_phase_4_post(batch_name, max_rows_per_run=MAX_ROWS_PER_RUN)
        summary["__phase_4__"] = phase_4_summary
        if not phase_4_summary.get("complete", True):
            _reenqueue_post_batch(batch_name, auto_submit)
            return _partial_result(batch_name, summary, "phase_4")

        # UX Gap 3 — auto-submit Phase 0 OB JE + Phase 4 drafts so the
        # operator's "Đăng" click produces submitted docs (docstatus=1).
        # The submit_phase_4_drafts helper handles the stock-account +
        # large-JE workarounds; it's safe to re-run (idempotent on
        # already-submitted docs since they're filtered by docstatus=0).
        if auto_submit:
            company = (
                frappe.db.get_value("Misa Migration Batch", batch_name, "company")
                or frappe.defaults.get_global_default("company")
                or frappe.db.get_value("Company", {}, "name")
            )
            if company:
                from vn_accounting.misa_migration.context import (
                    set_active_company,
                    clear_active_company,
                )
                set_active_company(company)
                try:
                    submit_summary = submit_phase_4_drafts(
                        batch_name=batch_name, company=company,
                    )
                    summary["__submit__"] = submit_summary
                    # Phase 4 PE→SI/PI link backfill — MUST run AFTER
                    # submit because:
                    # (1) the resolver queries `WHERE docstatus=1` (draft
                    #     SI/PI have no outstanding_amount populated),
                    # (2) PE.references validates against submitted SI/PI
                    #     only — linking against drafts would fail submit.
                    # Cancel + amend pattern adds references to each
                    # already-submitted PE.
                    try:
                        from vn_accounting.misa_migration.importers.phase_4_orchestrator \
                            import _backfill_pe_references_for_batch
                        bf = _backfill_pe_references_for_batch(
                            batch_name, company,
                        )
                        summary["__pe_backfill__"] = bf
                    except Exception as exc:
                        frappe.log_error(
                            title="Misa PE backfill failed",
                            message=str(exc),
                        )
                finally:
                    clear_active_company()
    except Exception as exc:
        with st.lock_for_batch(batch):
            batch = frappe.get_doc("Misa Migration Batch", batch_name)
            st.transition(batch, st.STUCK, reason=f"post fatal: {type(exc).__name__}")
            batch.save(ignore_permissions=True)
            frappe.db.commit()
        frappe.log_error(title="Misa post_batch fatal", message=str(exc))
        raise

    # Aggregate counts on batch
    phase_4 = summary.get("__phase_4__") or {}
    phase_4_posted = sum(
        v.get("posted", 0) for v in (phase_4.get("by_target_doctype") or {}).values()
    )
    phase_4_failed = sum(
        v.get("failed", 0) for v in (phase_4.get("by_target_doctype") or {}).values()
    )
    # Skip the structurally-different summary keys when aggregating
    # per-row counts. __phase_4__ keeps its own by_target_doctype
    # breakdown; __submit__ (UX Gap 3) reports dict shapes (`submitted`
    # by DocType + `failed` as list of tuples) — fold its scalar
    # totals in separately.
    _SUMMARY_SKIP = {"__phase_4__", "__submit__"}
    posted = sum(
        s.get("posted", 0) for k, s in summary.items()
        if k not in _SUMMARY_SKIP and isinstance(s, dict)
    ) + phase_4_posted
    failed = sum(
        s.get("failed", 0) for k, s in summary.items()
        if k not in _SUMMARY_SKIP and isinstance(s, dict)
    ) + phase_4_failed
    # Fold submit totals (UX Gap 3): submitted docs ARE posted; submit
    # failures count as additional failures for the operator-facing
    # batch counters.
    submit = summary.get("__submit__") or {}
    posted += submit.get("total_submitted", 0)
    failed += submit.get("total_failed", 0)

    with st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        batch.posted_docs_count = posted
        batch.failed_rows_count = failed
        st.transition(batch, st.POSTED,
                      reason=f"posted {posted}, failed {failed}")
        batch.save(ignore_permissions=True)
        frappe.db.commit()

    try:
        frappe.publish_realtime(PROGRESS_EVENT, {
            "batch": batch_name, "status": st.POSTED, "summary": summary,
            "posted": posted, "failed": failed,
        }, after_commit=False)
    except Exception:
        pass
    return {"batch": batch_name, "status": st.POSTED, "summary": summary,
            "posted": posted, "failed": failed}
