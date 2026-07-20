"""Database-backed smoke tests for Excel print template APIs."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase

from vn_accounting.excel_printing.api import (
    delete_excel_template,
    get_templates_for_document,
    preview_excel_template_grid,
    save_template,
)


class TestExcelPrintTemplateAPI(FrappeTestCase):
    def test_save_and_preview_template(self):
        frappe.set_user("Administrator")
        state = {
            "version": 1,
            "active_sheet": 0,
            "sheets": [{
                "title": "Phiếu in",
                "max_row": 2,
                "max_column": 2,
                "cells": {
                    "A1": {"value": "Số chứng từ", "data_type": "s", "style": {}},
                    "B1": {"value": "{{name}}", "data_type": "s", "style": {}},
                    "B2": {"value": "=1+2", "data_type": "f", "style": {}},
                },
                "merged_cells": [],
                "row_heights": {},
                "column_widths": {},
            }],
        }

        saved = save_template("Mẫu smoke test", "Sales Invoice", state)
        self.addCleanup(self._delete_if_exists, saved["name"])

        result = preview_excel_template_grid(template_name=saved["name"])
        cells = result["workbook_state"]["sheets"][0]["cells"]
        self.assertEqual(cells["B1"]["value"], "SALES_INVOICE-MẪU-0001")
        self.assertEqual(cells["B2"]["display_value"], 3)

        listing = get_templates_for_document("Sales Invoice")
        self.assertTrue(listing["can_manage"])
        self.assertIn(saved["name"], [item["name"] for item in listing["templates"]])

        delete_excel_template(saved["name"])
        self.assertFalse(frappe.db.exists("Excel Print Template", saved["name"]))

    @staticmethod
    def _delete_if_exists(name):
        if frappe.db.exists("Excel Print Template", name):
            frappe.delete_doc("Excel Print Template", name, force=True)
