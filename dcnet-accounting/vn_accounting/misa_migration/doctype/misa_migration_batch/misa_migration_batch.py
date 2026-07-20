from __future__ import annotations

import frappe
from frappe.model.document import Document


class MisaMigrationBatch(Document):
    """Misa → ERPNext migration session.

    Lifecycle (status field, NOT docstatus):
        DRAFT → UPLOADED → PARSED → REVIEWED → POSTING → POSTED → REVERSING → REVERSED

    Side states: STUCK (watchdog mark when job idle > 10 min).

    is_submittable=0 because the 8-state lifecycle does not map cleanly to
    docstatus 0/1/2. Locking is done via frappe.db.get_lock per-company in
    api/* endpoints.
    """

    def autoname(self):
        # Frappe v16 native naming pattern: format:MM-{YYYY}-{#####}
        # Set via DocType json autoname; no controller override needed.
        pass

    def validate(self):
        if not self.created_on:
            self.created_on = frappe.utils.now_datetime()
        if not self.status:
            self.status = "DRAFT"
        self.total_files = len(self.files or [])

    def on_trash(self):
        # Block deletion only when ERPNext docs were actually created (must be
        # reversed via Undo first) or a job is mid-flight. Never-posted batches
        # (DRAFT/UPLOADED/PARSED/REVIEWED/STUCK with 0 posted) are safe to delete
        # — this lets the operator clean up parked/abandoned batches from the
        # desk list view AND the hub's "Bỏ batch này" button.
        posted = frappe.utils.cint(self.posted_docs_count)
        if self.status in ("POSTING", "REVERSING"):
            frappe.throw(
                frappe._("Batch đang chạy ({0}) — đợi hoàn tất rồi mới xóa được.").format(self.status)
            )
        # DRAFT / REVERSED are always deletable: docs were never created, or
        # were already reversed via Undo (posted_docs_count stays at its
        # historical value on a REVERSED batch, so don't block on it).
        # Only POSTED batches with live docs must be Undone first.
        if self.status not in ("DRAFT", "REVERSED") and (self.status == "POSTED" or posted > 0):
            frappe.throw(
                frappe._("Batch đã tạo {0} chứng từ vào ERPNext — phải Hoàn tác (Undo) trước khi xóa.").format(posted)
            )
        # Remove linked Misa Migration Row rows first — they link via the
        # `batch` field (not a child table), so they'd otherwise block the
        # delete with LinkExistsError.
        frappe.db.delete("Misa Migration Row", {"batch": self.name})
