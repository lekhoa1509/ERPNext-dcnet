from __future__ import annotations

from frappe.model.document import Document


class MisaMigrationFile(Document):
    """Child table row in Misa Migration Batch — one upload per row."""
    pass
