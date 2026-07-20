from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document


class LCVAllocationSettings(Document):

    def validate(self):
        self._validate_unique_expense_type_keys()
        self._validate_vat_pct()

    def _validate_unique_expense_type_keys(self):
        seen = set()
        for row in self.expense_types or []:
            if not row.expense_type_key:
                continue
            if row.expense_type_key in seen:
                frappe.throw(
                    _("Duplicate expense_type_key '{0}' in row {1}. Each key must be unique.").format(
                        row.expense_type_key, row.idx
                    )
                )
            seen.add(row.expense_type_key)

    def _validate_vat_pct(self):
        pct = self.import_vat_default_deductible_pct
        if pct is None:
            return
        if not (0 <= pct <= 100):
            frappe.throw(
                _("% VAT NK mặc định được khấu trừ must be between 0 and 100 (got {0})").format(pct)
            )
