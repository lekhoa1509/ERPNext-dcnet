from __future__ import annotations

from frappe.model.document import Document


class MisaAccountMapping(Document):
    """Single DocType — Misa account code → ERPNext Account.name mapping.

    Populated by Phase 2 importer (3-way reconcile: match / new leaf / conflict).
    Used by Phase 4 voucher importers to translate NKC.account → ERPNext leaf.
    """
    pass
