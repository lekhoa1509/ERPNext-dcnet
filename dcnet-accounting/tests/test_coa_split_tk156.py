"""Static tests for COA split TK 156 → 1561 + 1562 (FB-2026-00836).

Pure JSON / fixture / source assertions — no Frappe DB needed. Run via:
    cd apps/vn_accounting && python3 -m unittest tests.test_coa_split_tk156 -v
"""
from __future__ import annotations

import json
import os
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
APP_INNER = os.path.normpath(os.path.join(HERE, "..", "vn_accounting"))


def _load(rel_path: str) -> dict:
    with open(os.path.join(APP_INNER, rel_path), encoding="utf-8") as f:
        return json.load(f)


class TestCoaSplit(unittest.TestCase):
    def test_large_enterprise_template_split(self):
        data = _load("chart_of_accounts/vn_large_enterprise.json")
        node = self._find_account_node(data, "156")
        self.assertIsNotNone(node, "TK 156 missing in large enterprise template")
        self.assertEqual(node.get("is_group"), 1, "TK 156 must be a group after split")
        self.assertIn("1561 - Giá mua hàng hoá", node)
        self.assertIn("1562 - Chi phí thu mua hàng hoá", node)
        self.assertEqual(node["1561 - Giá mua hàng hoá"]["account_type"], "Stock")
        self.assertEqual(node["1562 - Chi phí thu mua hàng hoá"]["account_type"], "Stock")

    def test_small_enterprise_template_split(self):
        data = _load("chart_of_accounts/vn_small_enterprise.json")
        node = self._find_account_node(data, "156")
        self.assertIsNotNone(node, "TK 156 missing in small enterprise template")
        self.assertEqual(node.get("is_group"), 1)
        self.assertIn("1561 - Giá mua hàng hoá", node)
        self.assertIn("1562 - Chi phí thu mua hàng hoá", node)

    def test_company_defaults_point_to_1561(self):
        path = os.path.join(APP_INNER, "setup", "company_defaults.py")
        with open(path, encoding="utf-8") as f:
            content = f.read()
        # Both _get_defaults_large + _get_defaults_small map default_inventory_account → "1561"
        # (count occurrences of `"default_inventory_account": "1561"` — must be ≥ 2)
        n = content.count('"default_inventory_account": "1561"')
        self.assertGreaterEqual(n, 2, "default_inventory_account must be 1561 in both small + large")
        self.assertNotIn(
            '"default_inventory_account": "156"',
            content,
            "Old default '156' (group) still present — must be 1561",
        )

    def test_lcv_inventory_account_custom_field_present(self):
        cf_path = os.path.join(APP_INNER, "fixtures", "custom_field.json")
        with open(cf_path, encoding="utf-8") as f:
            data = json.load(f)
        names = {cf["name"] for cf in data}
        self.assertIn("Landed Cost Voucher-landed_cost_inventory_account", names)
        self.assertIn("Landed Cost Taxes and Charges-landed_cost_inventory_account", names)

    def _find_account_node(self, tree: dict, account_number: str):
        # Tree is nested dict {label_key: {account_number, account_type, is_group, <children>}}
        for key, val in tree.items():
            if isinstance(val, dict):
                if val.get("account_number") == account_number:
                    return val
                found = self._find_account_node(val, account_number)
                if found:
                    return found
        return None


class TestGiaThanhSidebar(unittest.TestCase):
    """Verify Inventory Cost Reallocation appears in 'Giá thành' section of sidebar."""

    @classmethod
    def setUpClass(cls):
        path = os.path.join(APP_INNER, "workspace_sidebar", "vn_accounting.json")
        with open(path, encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.items = cls.data["items"]
        section_start = next(
            i for i, it in enumerate(cls.items)
            if it.get("type") == "Section Break" and it.get("label") == "Giá thành"
        )
        section_end = next(
            (
                i for i, it in enumerate(cls.items[section_start + 1:], section_start + 1)
                if it.get("type") == "Section Break"
            ),
            len(cls.items),
        )
        cls.section_items = cls.items[section_start + 1:section_end]

    def test_section_giathanh_exists(self):
        labels = [it.get("label") for it in self.items if it.get("type") == "Section Break"]
        self.assertIn("Giá thành", labels)

    def test_inventory_cost_reallocation_item_present(self):
        link_tos = [it.get("link_to") for it in self.section_items]
        self.assertIn("Inventory Cost Reallocation", link_tos)

    def test_inventory_cost_reallocation_is_doctype_link(self):
        item = next(
            it for it in self.section_items if it.get("link_to") == "Inventory Cost Reallocation"
        )
        self.assertEqual(item.get("link_type"), "DocType")
        self.assertEqual(item.get("type"), "Link")


if __name__ == "__main__":
    unittest.main()
