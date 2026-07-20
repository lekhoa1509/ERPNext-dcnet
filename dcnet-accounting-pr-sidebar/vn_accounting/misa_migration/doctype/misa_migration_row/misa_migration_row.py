from __future__ import annotations

from frappe.model.document import Document


class MisaMigrationRow(Document):
    """Heap of parsed Misa source rows, one row per source row.

    Large volume (~10k-500k per batch). track_changes=0 to avoid Version log
    explosion. autoname=hash for fast inserts.
    """
    pass
