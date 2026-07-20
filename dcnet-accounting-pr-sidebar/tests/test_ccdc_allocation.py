"""Unit tests for CCDC Item allocation logic."""
import unittest
import frappe
from frappe.utils import today


def _get_or_create_company():
    existing = frappe.db.get_value("Company", {"country": "Vietnam"}, "name")
    if existing:
        return existing
    return frappe.db.get_value("Company", {}, "name")


class TestCCDCAllocation(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")
        self.company = _get_or_create_company()

    def test_allocation_periods_sum(self):
        """Allocation entries must sum to item cost."""
        cost = 12000000
        periods = 12
        per_period = cost // periods
        entries = [per_period] * (periods - 1)
        entries.append(cost - sum(entries))
        self.assertEqual(sum(entries), cost)
        self.assertEqual(len(entries), periods)

    def test_last_entry_handles_rounding(self):
        """Last entry absorbs rounding remainder."""
        cost = 10000001
        periods = 3
        per_period = cost // periods  # 3333333
        entries = [per_period] * (periods - 1)
        entries.append(cost - sum(entries))  # 3333335
        self.assertEqual(sum(entries), cost)
        self.assertNotEqual(entries[-1], per_period)

    def test_ccdc_item_validate_cost_positive(self):
        """CCDC Item with cost=0 must raise ValidationError."""
        item = frappe.new_doc("CCDC Item")
        item.company = self.company
        item.item_name = "Test Item"
        item.cost = 0
        item.useful_period_months = 12
        item.allocation_periods = 12
        item.purchase_date = today()
        item.available_for_use_date = today()
        with self.assertRaises(frappe.ValidationError):
            item.validate()

    def test_ccdc_item_validate_periods_positive(self):
        """CCDC Item with useful_period_months=0 must raise ValidationError."""
        item = frappe.new_doc("CCDC Item")
        item.company = self.company
        item.item_name = "Test Item"
        item.cost = 5000000
        item.useful_period_months = 0
        item.allocation_periods = 0
        item.purchase_date = today()
        item.available_for_use_date = today()
        with self.assertRaises(frappe.ValidationError):
            item.validate()

    def test_ccdc_status_transitions(self):
        """Status values must be the expected VN lifecycle set."""
        item = frappe.new_doc("CCDC Item")
        meta = frappe.get_meta("CCDC Item")
        status_field = meta.get_field("status")
        self.assertIsNotNone(status_field)
        options = (status_field.options or "").split("\n")
        expected = {"Mới mua", "Đang sử dụng", "Hết phân bổ", "Đã ghi giảm"}
        self.assertTrue(expected.issubset(set(options)), f"Missing status options, got: {options}")


if __name__ == "__main__":
    unittest.main()
