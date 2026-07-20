"""Project Costing Stage — 1 giai đoạn của Project Costing.

Phase 1: skeleton with override tracking + lock guard only. Engines (markup
calc, COGS recognition) wire in Phase 2.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class ProjectCostingStage(Document):
    def autoname(self):
        """Format: <parent_costing>-S<stage_order zero-padded>.

        Frappe's `format:` autoname doesn't support Python format-spec like
        {stage_order:02d} — falls back to literal substitution. Hand-format
        here for stable, sortable stage names.
        """
        if not self.parent_costing or not self.stage_order:
            return
        self.name = f"{self.parent_costing}-S{int(self.stage_order):02d}"

    def validate(self):
        self._track_override()
        self._lock_when_si_submitted()

    def _track_override(self):
        """When KTT changes price_override, stamp user + timestamp."""
        if self.has_value_changed("price_override"):
            self.override_by = frappe.session.user
            self.override_on = now_datetime()

    def _lock_when_si_submitted(self):
        """BL R4.3: stage locked when its SI is submitted."""
        if not self.sales_invoice:
            return
        si_docstatus = frappe.db.get_value(
            "Sales Invoice", self.sales_invoice, "docstatus"
        )
        if si_docstatus != 1:
            return
        locked_fields = (
            "markup_method",
            "markup_value",
            "price_override",
            "stage_name",
            "stage_order",
            "parent_costing",
        )
        for f in locked_fields:
            if self.has_value_changed(f):
                frappe.throw(
                    _(
                        "Stage {0} has a submitted invoice ({1}); field {2} cannot be modified."
                    ).format(self.name, self.sales_invoice, f)
                )
