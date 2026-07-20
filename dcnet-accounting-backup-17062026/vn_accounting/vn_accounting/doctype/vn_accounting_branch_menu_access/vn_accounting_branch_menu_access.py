from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint

from vn_accounting.branch_sidebar_access import get_sidebar_item_catalog


class VNAccountingBranchMenuAccess(Document):
    def validate(self):
        self.sync_sidebar_items()
        self._validate_restricted_menu()

    @frappe.whitelist()
    def sync_sidebar_items(self):
        existing_rows = {
            row.sidebar_item_key: cint(row.is_allowed)
            for row in self.menu_items or []
            if row.sidebar_item_key
        }

        self.set("menu_items", [])
        for item in get_sidebar_item_catalog():
            row = self.append("menu_items", {})
            row.section_label = item.get("section_label")
            row.item_label = item.get("item_label")
            row.link_type = item.get("link_type")
            row.link_to = item.get("link_to")
            row.sidebar_item_key = item.get("sidebar_item_key")
            row.is_allowed = existing_rows.get(row.sidebar_item_key, 1)

        return self

    def _validate_restricted_menu(self):
        if not self.restrict_sidebar_items:
            return

        if any(cint(row.is_allowed) for row in self.menu_items or []):
            return

        frappe.throw(_("Vui lòng bật ít nhất một menu hiển thị cho chi nhánh này."))
