import frappe
from frappe.model.document import Document


class CCDCAllocationSchedule(Document):
    def before_save(self):
        self.progress_text = self._compute_progress()

    def _compute_progress(self):
        rows = self.allocation_entries or []
        total = len(rows)
        posted = sum(1 for r in rows if (r.status or "").strip() == "Posted")
        return f"{posted}/{total}" if total else "0/0"


@frappe.whitelist()
def get_progress(name):
    """Return 'posted/total' allocation entry counts for a schedule."""
    rows = frappe.get_all(
        "CCDC Allocation Entry",
        filters={"parent": name},
        fields=["status"],
    )
    total = len(rows)
    posted = sum(1 for r in rows if (r.status or "").strip() == "Posted")
    return f"{posted}/{total}" if total else "0/0"
