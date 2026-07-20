"""Undo job — cancel/delete docs created by a POSTED batch.

POSTED → REVERSING → REVERSED. Per-row try/except in BaseImporter.undo_row.
"""

from __future__ import annotations

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st
from vn_accounting.misa_migration.importers.orchestrator import run_undo


PROGRESS_EVENT = "misa_migration:undo_progress"


def undo_batch(batch_name: str) -> dict:
    batch = frappe.get_doc("Misa Migration Batch", batch_name)
    if batch.status != st.POSTED:
        frappe.throw(
            _("Không thể Undo ở trạng thái {0} — phải là POSTED.").format(batch.status)
        )

    with st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        st.transition(batch, st.REVERSING, reason="undo_batch started")
        batch.save(ignore_permissions=True)
        frappe.db.commit()

    try:
        summary = run_undo(batch_name)
    except Exception as exc:
        with st.lock_for_batch(batch):
            batch = frappe.get_doc("Misa Migration Batch", batch_name)
            st.transition(batch, st.STUCK, reason=f"undo fatal: {type(exc).__name__}")
            batch.save(ignore_permissions=True)
            frappe.db.commit()
        frappe.log_error(title="Misa undo_batch fatal", message=str(exc))
        raise

    reversed_count = sum(s.get("reversed", 0) for s in summary.values())
    with st.lock_for_batch(batch):
        batch = frappe.get_doc("Misa Migration Batch", batch_name)
        st.transition(batch, st.REVERSED, reason=f"reversed {reversed_count} docs")
        batch.save(ignore_permissions=True)
        frappe.db.commit()

    try:
        frappe.publish_realtime(PROGRESS_EVENT, {
            "batch": batch_name, "status": st.REVERSED, "summary": summary,
            "reversed": reversed_count,
        }, after_commit=False)
    except Exception:
        pass
    return {"batch": batch_name, "status": st.REVERSED, "summary": summary,
            "reversed": reversed_count}
