"""Validate hook: block saving source docs with a locked (invoiced) stage.

Registered on Purchase Invoice, Stock Entry, Delivery Note, Expense Claim
via doc_events.validate. Prevents assigning costs to stages whose COGS
has already been recognized.
"""
from __future__ import annotations

import frappe
from frappe import _


def validate_stage_not_locked(doc, method=None, *args, **kwargs):
    """Check project_costing_stage on parent or child rows — block if locked."""
    # Parent-level stage (Stock Entry, Expense Claim)
    stage = doc.get("project_costing_stage")
    if stage:
        _check_stage(stage, doc.name)

    # Child-level stage (Purchase Invoice Item, Delivery Note Item)
    for row in doc.get("items") or []:
        stage = row.get("project_costing_stage")
        if stage:
            _check_stage(stage, f"{doc.name} row #{row.idx}")


def _check_stage(stage: str, context: str):
    cogs_je = frappe.db.get_value("Project Costing Stage", stage, "cogs_je")
    if cogs_je:
        frappe.throw(
            _("Giai đoạn {0} đã xuất hóa đơn và giá vốn đã khóa (COGS JE: {1}). "
              "Không thể gắn chi phí vào giai đoạn này. "
              "Chọn giai đoạn khác hoặc bỏ trống để vào Tập hợp chi phí chưa gắn."
              ).format(stage, cogs_je),
            title=_("Giai đoạn đã khóa"),
        )
