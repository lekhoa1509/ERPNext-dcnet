"""Static test for FB-2026-00832 — install hook enforces allow_negative_stock=0.

Pure source assertion (no Frappe DB needed). Run via:
    cd apps/vn_accounting && python3 -m unittest tests.test_disallow_negative_stock -v
"""
from __future__ import annotations

import os
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
APP_INNER = os.path.normpath(os.path.join(HERE, "..", "vn_accounting"))


class TestDisallowNegativeStock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(APP_INNER, "install.py"), encoding="utf-8") as f:
            cls.src = f.read()

    def test_helper_function_exists(self):
        self.assertIn("def _enforce_no_negative_stock()", self.src)

    def test_helper_writes_zero_when_not_zero(self):
        # Idempotent guard: only write when current != 0
        self.assertIn('frappe.db.set_single_value("Stock Settings", "allow_negative_stock", 0)', self.src)
        self.assertIn('current = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")', self.src)
        self.assertIn("if current != 0:", self.src)

    def test_called_from_after_install_and_after_migrate(self):
        # Must run on both initial install AND every migrate (so a new vn_accounting
        # install on an existing site picks up the rule, AND a re-toggled site
        # bounces back on the next migrate).
        self.assertEqual(self.src.count("_enforce_no_negative_stock()"), 3)
        # 3 = 1 def + 1 call in after_install + 1 call in after_migrate

    def test_business_logic_doc_section_added(self):
        with open(os.path.join(APP_INNER, "..", "docs", "BUSINESS_LOGIC.md"), encoding="utf-8") as f:
            doc = f.read()
        self.assertIn("4.9 Kho hàng", doc)
        self.assertIn("allow_negative_stock", doc)
        self.assertIn("FB-2026-00832", doc)


if __name__ == "__main__":
    unittest.main()
