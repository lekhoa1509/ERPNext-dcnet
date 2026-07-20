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
        if self.status not in ("DRAFT", "REVERSED"):
            frappe.throw(
                frappe._("Không thể xóa batch ở trạng thái {0}. Phải Undo về REVERSED trước.").format(self.status)
            )
