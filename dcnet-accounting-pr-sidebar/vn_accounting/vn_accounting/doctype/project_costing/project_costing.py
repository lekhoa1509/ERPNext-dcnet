"""Project Costing — master document gom chi phí + giai đoạn cho 1 công trình.

Phase 1: skeleton only. Lifecycle controllers (close/reopen/cancel) and GL
engines wire in Phase 2 (see services/close_engine.py).
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document


class ProjectCosting(Document):
    def autoname(self):
        # name = project (Link unique). Frappe handles via "By fieldname" naming rule.
        self.name = self.project

    def validate(self):
        self._fetch_project_fields()

    def on_trash(self):
        # GL Entry / Stock Ledger Entry track via is_cancelled, not docstatus;
        # whitelist so delete doesn't trip back-link guard when JEs exist.
        self.ignore_linked_doctypes = ["GL Entry", "Stock Ledger Entry", "Payment Ledger Entry"]

    def _fetch_project_fields(self):
        """Backstop fetch — autoname runs before validate but fetch_from chỉ fire
        khi user pick Link in UI. Bench console / API insert có thể bỏ trống.
        """
        if not (self.project_name and self.customer and self.company):
            p = frappe.db.get_value(
                "Project",
                self.project,
                ["project_name", "customer", "company"],
                as_dict=True,
            )
            if not p:
                frappe.throw(_("Project {0} not found").format(self.project))
            self.project_name = self.project_name or p.project_name
            self.customer = self.customer or p.customer
            self.company = self.company or p.company

    @frappe.whitelist()
    def close(self, writeoff_account=None, writeoff_amount=0, force=False):
        """Close project — see close_engine.close_project for flow."""
        from vn_accounting.project_costing.services.close_engine import close_project
        if isinstance(force, str):
            force = force.lower() in ("true", "1", "yes")
        return close_project(
            self,
            writeoff_account=writeoff_account,
            writeoff_amount=float(writeoff_amount or 0),
            force=bool(force),
        )

    @frappe.whitelist()
    def reopen(self):
        """Reopen a closed project — see close_engine.reopen_project."""
        from vn_accounting.project_costing.services.close_engine import reopen_project
        return reopen_project(self)

    @frappe.whitelist()
    def get_wip_balance(self):
        """Read-only probe: current 154 balance for this project."""
        from vn_accounting.project_costing.services.close_engine import compute_wip_balance
        return {"balance": compute_wip_balance(self.project, self.company)}
