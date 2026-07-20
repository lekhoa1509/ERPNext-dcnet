from __future__ import annotations

from frappe.model.document import Document


class MisaFieldMapping(Document):
    """Single DocType — Misa Excel column → ERPNext field mapping per file type.

    Stored as JSON Long Text per file type to allow inline edit by accountant
    when Misa export format changes between versions.
    """
    pass
