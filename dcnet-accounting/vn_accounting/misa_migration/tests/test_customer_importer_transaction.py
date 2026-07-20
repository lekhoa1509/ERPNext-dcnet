"""Regression tests for Customer importer transaction isolation."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from vn_accounting.misa_migration.importers.customer import CustomerImporter


class TestCustomerImporterTransaction(unittest.TestCase):
    def test_duplicate_rolls_back_only_current_row_savepoint(self):
        importer = CustomerImporter.__new__(CustomerImporter)
        mock_frappe = MagicMock(name="frappe")
        mock_doc = MagicMock(name="customer_doc")
        mock_doc.insert.side_effect = Exception("Duplicate entry")
        mock_frappe.get_doc.return_value = mock_doc

        with patch(
            "vn_accounting.misa_migration.importers.customer.frappe",
            mock_frappe,
        ):
            result = importer._insert_customer(
                {"doctype": "Customer", "customer_name": "Khách A"},
                "KH-A",
            )

        self.assertIsNone(result)
        mock_frappe.db.savepoint.assert_called_once_with("misa_customer_insert")
        mock_frappe.db.rollback.assert_called_once_with(
            save_point="misa_customer_insert"
        )


if __name__ == "__main__":
    unittest.main()
