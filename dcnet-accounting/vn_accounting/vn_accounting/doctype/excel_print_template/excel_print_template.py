"""Controller for reusable Excel print templates."""

from __future__ import annotations

import json

import frappe
from frappe import _
from frappe.model.document import Document

from vn_accounting.excel_printing.constants import SUPPORTED_DOCTYPES
from vn_accounting.excel_printing.engine import validate_state


class ExcelPrintTemplate(Document):
    """Store the canonical workbook JSON used for preview and export."""

    def validate(self) -> None:
        """Validate supported document type, workbook JSON and default uniqueness."""
        if self.document_type not in SUPPORTED_DOCTYPES:
            frappe.throw(_("Loại chứng từ chưa được hỗ trợ cho mẫu in Excel."))
        if not self.template_name or not self.template_name.strip():
            frappe.throw(_("Tên mẫu là bắt buộc."))
        state = validate_state(self.workbook_state)
        self.workbook_state = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
        if self.is_default:
            self._clear_other_defaults()

    def _clear_other_defaults(self) -> None:
        existing = frappe.get_all(
            "Excel Print Template",
            filters={"document_type": self.document_type, "is_default": 1, "name": ["!=", self.name or ""]},
            pluck="name",
        )
        for name in existing:
            frappe.db.set_value("Excel Print Template", name, "is_default", 0, update_modified=False)
