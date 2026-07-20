"""Tests for vn_accounting.branch_sidebar_access."""

from pathlib import Path
import sys
import types
import unittest

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))


def install_frappe_stub():
    for module_name in list(sys.modules):
        if module_name == "frappe" or module_name.startswith("frappe."):
            sys.modules.pop(module_name, None)

    frappe = types.ModuleType("frappe")
    frappe._ = lambda value, *args, **kwargs: value
    frappe.session = types.SimpleNamespace(user="tester@example.com")
    frappe.get_roles = lambda user=None: ["Accounts User"]
    frappe.db = types.SimpleNamespace(
        exists=lambda *args, **kwargs: False,
        get_value=lambda *args, **kwargs: None,
        has_column=lambda *args, **kwargs: False,
    )
    sys.modules["frappe"] = frappe
    return frappe


install_frappe_stub()
from vn_accounting.branch_sidebar_access import build_sidebar_item_key, filter_sidebar_items


class TestBuildSidebarItemKey(unittest.TestCase):
    def test_route_options_make_sidebar_keys_distinct(self):
        receive_key = build_sidebar_item_key(
            {
                "type": "Link",
                "label": "Thu tiền",
                "link_type": "DocType",
                "link_to": "Payment Entry",
                "route_options": '{"payment_type":"Receive"}',
            }
        )
        pay_key = build_sidebar_item_key(
            {
                "type": "Link",
                "label": "Chi tiền",
                "link_type": "DocType",
                "link_to": "Payment Entry",
                "route_options": '{"payment_type":"Pay"}',
            }
        )

        self.assertNotEqual(receive_key, pay_key)


class TestFilterSidebarItems(unittest.TestCase):
    def test_hides_disallowed_children_and_empty_sections(self):
        cash_section = {"type": "Section Break", "label": "Quỹ", "icon": "money-coins-1"}
        bank_section = {"type": "Section Break", "label": "Ngân hàng", "icon": "building-2"}
        cash_entry = {
            "type": "Link",
            "label": "Phiếu quỹ chi nhánh",
            "link_type": "DocType",
            "link_to": "Branch Cash Entry",
            "child": 1,
        }
        cash_book = {
            "type": "Link",
            "label": "Sổ quỹ chi nhánh",
            "link_type": "Report",
            "link_to": "So Quy Chi Nhanh",
            "child": 1,
        }
        bank_book = {
            "type": "Link",
            "label": "Sổ tiền gửi ngân hàng",
            "link_type": "Report",
            "link_to": "So Tien Gui Ngan Hang",
            "child": 1,
        }

        allowed_keys = {build_sidebar_item_key(cash_book)}
        result = filter_sidebar_items(
            [cash_section, cash_entry, cash_book, bank_section, bank_book],
            allowed_keys,
        )

        self.assertEqual([item["label"] for item in result], ["Quỹ", "Sổ quỹ chi nhánh"])

    def test_keeps_allowed_root_links(self):
        overview = {
            "type": "Link",
            "label": "Tổng quan",
            "link_type": "Workspace",
            "link_to": "Ke Toan VN",
        }
        settings = {
            "type": "Link",
            "label": "Thiết lập menu chi nhánh",
            "link_type": "DocType",
            "link_to": "VN Accounting Branch Menu Access",
        }

        result = filter_sidebar_items(
            [overview, settings],
            {build_sidebar_item_key(overview)},
        )

        self.assertEqual([item["label"] for item in result], ["Tổng quan"])


if __name__ == "__main__":
    unittest.main()
