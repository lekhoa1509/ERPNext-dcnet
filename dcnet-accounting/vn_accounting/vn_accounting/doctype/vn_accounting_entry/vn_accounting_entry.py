"""VN Accounting Entry — child table row representing a single Debit/Credit pair.

Validation lives at parent level (Asset Repair, CCDC Item, CCDC Writeoff, CCDC
Allocation Schedule) because total balance and account combinations are
event-specific. This controller is intentionally minimal.
"""
from __future__ import annotations

from frappe.model.document import Document


class VNAccountingEntry(Document):
    pass
