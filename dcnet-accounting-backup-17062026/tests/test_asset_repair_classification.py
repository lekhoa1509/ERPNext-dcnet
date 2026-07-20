"""Unit tests for Asset Repair classification routing."""
import unittest
import frappe


class TestAssetRepairClassification(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def test_repair_classification_field_exists(self):
        """Asset Repair must have repair_classification custom field."""
        meta = frappe.get_meta("Asset Repair")
        field = meta.get_field("repair_classification")
        self.assertIsNotNone(field, "repair_classification field must exist on Asset Repair")

    def test_repair_classification_options(self):
        """repair_classification must have 3 VN-compliant options."""
        meta = frappe.get_meta("Asset Repair")
        field = meta.get_field("repair_classification")
        if field:
            options = (field.options or "").split("\n")
            self.assertIn("Chi phí", options)
            self.assertIn("Sửa chữa lớn vốn hóa", options)
            self.assertIn("Nâng cấp cải tạo", options)

    def test_is_low_value_asset_field_on_item(self):
        """Item DocType must have is_low_value_asset custom field."""
        meta = frappe.get_meta("Item")
        field = meta.get_field("is_low_value_asset")
        self.assertIsNotNone(field, "is_low_value_asset must exist on Item")
        self.assertEqual(field.fieldtype, "Check")

    def test_depreciation_method_property_setter(self):
        """Asset.depreciation_method options should be restricted by Property Setter."""
        ps = frappe.db.get_value(
            "Property Setter",
            {"doc_type": "Asset", "field_name": "depreciation_method", "property": "options"},
            "value"
        )
        self.assertIsNotNone(ps, "Property Setter for Asset.depreciation_method must exist")
        options = ps.split("\n")
        self.assertIn("Đường thẳng", options)
        self.assertIn("Số dư giảm dần", options)
        # Must not have the 3 ERPNext defaults we removed
        self.assertNotIn("Written Down Value", options)


if __name__ == "__main__":
    unittest.main()
