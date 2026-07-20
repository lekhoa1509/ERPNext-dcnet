"""Static tests for Purchase No VAT report (FB-2026-00840).

Pure source/JSON assertions — no Frappe DB required.
"""
from __future__ import annotations

import json
import os
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
APP_INNER = os.path.normpath(os.path.join(HERE, "..", "vn_accounting"))


class TestPurchaseNoVatReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = os.path.join(APP_INNER, "vn_accounting", "report", "purchase_no_vat")
        with open(os.path.join(d, "purchase_no_vat.json"), encoding="utf-8") as f:
            cls.cfg = json.load(f)
        with open(os.path.join(d, "purchase_no_vat.py"), encoding="utf-8") as f:
            cls.py = f.read()
        with open(os.path.join(d, "purchase_no_vat.js"), encoding="utf-8") as f:
            cls.js = f.read()

    def test_report_registered(self):
        self.assertEqual(self.cfg["ref_doctype"], "Purchase Invoice")
        self.assertEqual(self.cfg["report_type"], "Script Report")
        self.assertEqual(self.cfg["module"], "VN Accounting")
        # add_total_row=0 because we emit manual total from execute()
        self.assertEqual(self.cfg["add_total_row"], 0)

    def test_roles_include_purchase_manager(self):
        # Purchase Manager needs read+report (this is purchasing-side data)
        roles = {r["role"] for r in self.cfg.get("roles", [])}
        self.assertIn("Purchase Manager", roles)
        self.assertIn("Accounts Manager", roles)
        self.assertIn("Accounts User", roles)

    def test_python_2_view_modes(self):
        self.assertIn("Không có HĐ VAT", self.py)
        self.assertIn("Có HĐ VAT", self.py)

    def test_python_uses_einvoice_inward_link(self):
        # The "no VAT invoice" definition: NOT EXISTS EInvoice Inward referencing the PI
        self.assertIn("tabEInvoice Inward", self.py)
        self.assertIn("linked_purchase_invoice", self.py)
        self.assertIn("NOT EXISTS", self.py)
        self.assertIn("EXISTS", self.py)

    def test_python_filters_docstatus_1_only(self):
        self.assertIn("pi.docstatus = 1", self.py)

    def test_python_filters_by_proposed_department(self):
        self.assertIn("custom_proposed_department", self.py)

    def test_python_emits_manual_total_currency_only(self):
        # Total row name + grand_total sum, no other field
        self.assertIn('"name": _("TỔNG CỘNG', self.py)
        self.assertIn('"grand_total": sum', self.py)

    def test_js_default_to_no_vat_mode(self):
        self.assertIn('default: "Không có HĐ VAT"', self.js)
        # No on_change race (lesson from FB-00613)
        self.assertNotIn("on_change", self.js)


class TestSidebarMuaHang(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(APP_INNER, "workspace_sidebar", "vn_accounting.json")
        with open(path, encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.items = cls.data["items"]
        section_start = next(
            i for i, it in enumerate(cls.items)
            if it.get("type") == "Section Break" and it.get("label") == "Mua hàng"
        )
        section_end = next(
            (
                i for i, it in enumerate(cls.items[section_start + 1:], section_start + 1)
                if it.get("type") == "Section Break"
            ),
            len(cls.items),
        )
        cls.section_items = cls.items[section_start + 1:section_end]

    def test_purchase_no_vat_in_mua_hang_section(self):
        item = next(
            (it for it in self.section_items if it.get("link_to") == "Purchase No VAT"),
            None,
        )
        self.assertIsNotNone(item, "Purchase No VAT missing from Mua hàng section")
        self.assertEqual(item["label"], "Mua không VAT")
        self.assertEqual(item["link_type"], "Report")
        self.assertEqual(item["type"], "Link")


class TestHelpRegistered(unittest.TestCase):
    def test_help_article_exists(self):
        self.assertTrue(os.path.isfile(os.path.join(APP_INNER, "help", "mua-hang", "mua-khong-vat.md")))

    def test_hooks_register_report_help(self):
        with open(os.path.join(APP_INNER, "hooks.py"), encoding="utf-8") as f:
            hooks = f.read()
        self.assertIn('"Purchase No VAT"', hooks)
        self.assertIn('"help/mua-hang"', hooks)
        self.assertIn('"mua-khong-vat"', hooks)


if __name__ == "__main__":
    unittest.main()
