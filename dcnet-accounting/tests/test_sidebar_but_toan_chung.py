"""Static test: 'Bút toán chung' sidebar item in both Mua hàng + Bán hàng sections (FB-2026-00839)."""
from __future__ import annotations

import json
import os
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
APP_INNER = os.path.normpath(os.path.join(HERE, "..", "vn_accounting"))


class TestButToanChungSidebar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(APP_INNER, "workspace_sidebar", "vn_accounting.json")
        with open(path, encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.items = [it for it in cls.data["items"] if it]

    def _section_items(self, label):
        idx = next(
            i for i, it in enumerate(self.items)
            if it.get("type") == "Section Break" and it.get("label") == label
        )
        end = next(
            (i for i, it in enumerate(self.items[idx + 1:], idx + 1) if it.get("type") == "Section Break"),
            len(self.items),
        )
        return self.items[idx + 1:end]

    def _assert_btc_in(self, section_label):
        items = self._section_items(section_label)
        btc = next((it for it in items if it.get("label") == "Bút toán chung"), None)
        self.assertIsNotNone(btc, f"Section {section_label} thiếu 'Bút toán chung'")
        self.assertEqual(btc["link_to"], "Journal Entry")
        self.assertEqual(btc["link_type"], "DocType")
        self.assertEqual(btc["type"], "Link")
        # No filter — must NOT have route_options (link to plain JE list)
        self.assertNotIn("route_options", btc, f"'Bút toán chung' in {section_label} không nên có route_options")

    def test_in_mua_hang_section(self):
        self._assert_btc_in("Mua hàng")

    def test_in_ban_hang_section(self):
        self._assert_btc_in("Bán hàng")


if __name__ == "__main__":
    unittest.main()
