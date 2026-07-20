"""Tests for IssuanceService.issue_single dispatcher — kiểm tra route theo
provider.OUTWARD_CAPABILITY chuyển hướng đúng path."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch

from einvoice.einvoice.services.issuance import IssuanceService


def _make_si_doc(name="SI-001"):
    si = MagicMock()
    si.name = name
    si.docstatus = 1
    si.einvoice_issued = 0
    si.get = lambda k, default=None: 0 if k == "einvoice_pushed" else default
    return si


def _make_provider_instance(capability):
    p = MagicMock()
    p.OUTWARD_CAPABILITY = capability
    p.authenticate = MagicMock()
    p.map_sales_invoice_to_payload = MagicMock(return_value={"ikey": "SI-001", "pattern": "1", "serial": ""})
    p.issue_outward_invoice = MagicMock(return_value={
        "success": True, "invoice_number": "0000123", "lookup_code": "ABC", "pdf_url": "http://x/y.pdf",
    })
    p.push_draft_invoice = MagicMock(return_value={
        "success": True, "ikey": "SI-001", "status_text": "Đã đẩy, chờ ký",
    })
    return p


class TestIssueSingleDispatcher(unittest.TestCase):

    def _patch_frappe_and_resolver(self, capability):
        prov_doc = MagicMock()
        prov_doc.name = "TestProvider"
        prov_instance = _make_provider_instance(capability)
        prov_doc.get_provider_instance = MagicMock(return_value=prov_instance)

        si = _make_si_doc()

        frappe_mock = MagicMock()
        frappe_mock.get_doc = MagicMock(return_value=si)
        frappe_mock.get_single = MagicMock(return_value=MagicMock(default_issue_mode=None))
        frappe_mock.db.set_value = MagicMock()
        frappe_mock.db.commit = MagicMock()

        return frappe_mock, prov_doc, prov_instance, si

    def test_direct_capability_calls_issue_outward(self):
        frappe_mock, prov_doc, prov_instance, si = self._patch_frappe_and_resolver("direct")
        with patch("einvoice.einvoice.services.issuance.frappe", frappe_mock), \
             patch("einvoice.einvoice.services.issuance._resolve_provider", return_value=prov_doc), \
             patch("einvoice.einvoice.services.issuance._create_issuance_log"), \
             patch("einvoice.einvoice.services.issuance.now_datetime", return_value="2026-05-08 18:00:00"):
            result = IssuanceService.issue_single("SI-001")

        self.assertTrue(result["success"])
        prov_instance.issue_outward_invoice.assert_called_once()
        prov_instance.push_draft_invoice.assert_not_called()
        # SI updated as ISSUED (not pushed)
        update_call = frappe_mock.db.set_value.call_args
        self.assertEqual(update_call.args[0:2], ("Sales Invoice", "SI-001"))
        self.assertEqual(update_call.args[2]["einvoice_issued"], 1)
        self.assertEqual(update_call.args[2]["einvoice_number"], "0000123")
        self.assertNotIn("einvoice_pushed", update_call.args[2])

    def test_pushdraft_capability_calls_push_draft(self):
        frappe_mock, prov_doc, prov_instance, si = self._patch_frappe_and_resolver("push-draft")
        with patch("einvoice.einvoice.services.issuance.frappe", frappe_mock), \
             patch("einvoice.einvoice.services.issuance._resolve_provider", return_value=prov_doc), \
             patch("einvoice.einvoice.services.issuance._create_issuance_log"), \
             patch("einvoice.einvoice.services.issuance.now_datetime", return_value="2026-05-08 18:00:00"):
            result = IssuanceService.issue_single("SI-001")

        self.assertTrue(result["success"])
        prov_instance.push_draft_invoice.assert_called_once()
        prov_instance.issue_outward_invoice.assert_not_called()
        # SI updated as PUSHED (not issued)
        update_call = frappe_mock.db.set_value.call_args
        self.assertEqual(update_call.args[0:2], ("Sales Invoice", "SI-001"))
        self.assertEqual(update_call.args[2]["einvoice_pushed"], 1)
        self.assertEqual(update_call.args[2]["einvoice_ikey"], "SI-001")
        self.assertNotIn("einvoice_issued", update_call.args[2])

    def test_blocks_already_pushed_si(self):
        prov_doc = MagicMock()
        prov_instance = _make_provider_instance("push-draft")
        prov_doc.get_provider_instance = MagicMock(return_value=prov_instance)

        si = _make_si_doc()
        si.get = lambda k, default=None: 1 if k == "einvoice_pushed" else default

        frappe_mock = MagicMock()
        frappe_mock.get_doc = MagicMock(return_value=si)

        with patch("einvoice.einvoice.services.issuance.frappe", frappe_mock):
            result = IssuanceService.issue_single("SI-001")

        self.assertFalse(result["success"])
        self.assertIn("đã đẩy", result["message"].lower())
        prov_instance.push_draft_invoice.assert_not_called()


if __name__ == "__main__":
    unittest.main()
