"""Tests for state_sync service — pure logic, no Frappe ORM."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch, call

from einvoice.einvoice.services.state_sync import _apply_state_update


class TestApplyStateUpdate(unittest.TestCase):
    """Test _apply_state_update without hitting actual DB."""

    def _patch_frappe(self):
        """Patch the frappe module reference inside state_sync (avoids thread-local proxy)."""
        return patch("einvoice.einvoice.services.state_sync.frappe")

    def _patch_now(self):
        return patch("einvoice.einvoice.services.state_sync.now_datetime", return_value="2026-05-07 10:00:00")

    def test_apply_state_signed(self):
        """InvoiceStatus=1 → sets einvoice_issued=1 + lookup fields."""
        state = {
            "invoice_status": 1,
            "status_text": "Đã ký, chờ khai thuế",
            "ikey": "SI-0001",
            "no": "0001234",
            "lookup_code": "ABC123",
            "link_view": "https://tracuu.easyinvoice.vn/test",
            "error": None,
        }
        with self._patch_frappe() as mock_frappe, self._patch_now():
            mock_frappe.db.set_value = MagicMock()
            mock_frappe.enqueue = MagicMock()
            _apply_state_update("SINV-0001", state, "EasyInvoice HTS", MagicMock())

        args, kwargs = mock_frappe.db.set_value.call_args
        updates = args[2]
        self.assertEqual(updates.get("einvoice_issued"), 1)
        self.assertEqual(updates.get("einvoice_number"), "0001234")
        self.assertEqual(updates.get("einvoice_lookup_code"), "ABC123")

    def test_apply_state_cancelled(self):
        """InvoiceStatus=5 → status_text = 'Đã hủy...', einvoice_issued NOT set."""
        state = {
            "invoice_status": 5,
            "status_text": "Đã hủy trên EasyInvoice",
            "ikey": "SI-0001",
            "error": None,
        }
        with self._patch_frappe() as mock_frappe, self._patch_now():
            mock_frappe.db.set_value = MagicMock()
            mock_frappe.enqueue = MagicMock()
            _apply_state_update("SINV-0001", state, "EasyInvoice HTS", MagicMock())

        args, kwargs = mock_frappe.db.set_value.call_args
        updates = args[2]
        self.assertNotIn("einvoice_issued", updates)
        self.assertIn("Đã hủy", updates.get("einvoice_status_text", ""))

    def test_apply_state_pending_no_enqueue(self):
        """InvoiceStatus=0 → no download enqueued."""
        state = {
            "invoice_status": 0,
            "status_text": "Đã đẩy, chờ ký",
            "ikey": "SI-0001",
            "error": None,
        }
        with self._patch_frappe() as mock_frappe, self._patch_now():
            mock_frappe.db.set_value = MagicMock()
            mock_frappe.enqueue = MagicMock()
            _apply_state_update("SINV-0001", state, "EasyInvoice HTS", MagicMock())

        mock_frappe.enqueue.assert_not_called()


if __name__ == "__main__":
    unittest.main()
