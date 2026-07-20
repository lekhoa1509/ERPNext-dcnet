"""Tests for EasyInvoiceProvider Phase 4+5: push_draft + sync_state + download."""
import base64
import json
import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from einvoice.einvoice.providers.easyinvoice import EasyInvoiceProvider
from einvoice.einvoice.exceptions import EInvoiceProviderError


def _make_provider(pattern="1C26TYY", serial="K24TYY"):
    doc = MagicMock()
    doc.name = "EasyInvoice HTS"
    doc.api_url = "https://api.easyinvoice.vn"
    doc.api_url_purchase = "https://api.easyinvoice.vn"
    doc.tax_code = "0106936409"
    doc.api_username = "API_ERP"
    doc.get_password.return_value = "TESTPASS"
    doc.get.side_effect = lambda k, default=None: {
        "api_username": "API_ERP",
        "default_invoice_pattern": pattern,
        "default_invoice_serial": serial,
    }.get(k, default)
    doc.default_invoice_pattern = pattern
    doc.default_invoice_serial = serial
    return EasyInvoiceProvider(doc)


def _make_payload(pattern="1C26TYY", serial="K24TYY"):
    return {
        "pattern": pattern,
        "serial": serial,
        "invoice_dict": {
            "ikey": "SI-TEST-0001",
            "customer_code": "CUST-001",
            "customer_name": "Công ty Test",
            "address": "Hà Nội",
            "tax_id": "0123456789",
            "email": "test@example.com",
            "phone": "0912345678",
            "payment_method": "TM/CK",
            "arising_date": "07/05/2026",
            "currency": "VND",
            "exchange_rate": 1,
            "products": [
                {
                    "no": 1, "code": "ITEM-001", "name": "Sản phẩm A",
                    "unit": "Cái", "qty": 2, "price": 100000,
                    "total": 200000, "vat_rate": 10,
                    "vat_amount": 20000, "amount": 220000,
                }
            ],
            "total": 200000,
            "vat_rate": 10,
            "vat_amount": 20000,
            "amount": 220000,
            "amount_in_words": "Hai trăm hai mươi nghìn đồng",
        },
    }


class TestPushDraftSuccess(unittest.TestCase):
    def test_push_draft_success(self):
        provider = _make_provider()
        mock_resp = {
            "Status": 2,
            "Message": "Ok",
            "Data": {
                "Invoices": [{"Ikey": "SI-TEST-0001", "InvoiceStatus": 0}]
            },
        }
        with patch.object(provider, "_api_call_easy", return_value=mock_resp):
            result = provider.push_draft_invoice(_make_payload())
        self.assertTrue(result["success"])
        self.assertEqual(result["ikey"], "SI-TEST-0001")
        self.assertEqual(result["status_code"], 0)
        self.assertIn("chờ ký", result["status_text"])
        self.assertIsNone(result["error"])

    def test_push_draft_validation_error(self):
        provider = _make_provider()
        mock_resp = {
            "Status": 4,
            "Message": "Validation failed",
            "Data": {
                "KeyInvoiceMsg": {"SI-TEST-0001": "Mẫu hóa đơn không hợp lệ"}
            },
        }
        with patch.object(provider, "_api_call_easy", return_value=mock_resp):
            result = provider.push_draft_invoice(_make_payload())
        self.assertFalse(result["success"])
        self.assertIn("Mẫu hóa đơn", result["error"])

    def test_push_draft_server_error(self):
        provider = _make_provider()
        mock_resp = {"Status": 5, "Message": "Internal server error", "Data": {}}
        with patch.object(provider, "_api_call_easy", return_value=mock_resp):
            result = provider.push_draft_invoice(_make_payload())
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_payload_includes_pattern_serial(self):
        provider = _make_provider(pattern="1C26TYY", serial="K24TYY")
        captured = {}
        def fake_api_call(method, resource, **kwargs):
            captured.update(kwargs.get("json", {}))
            return {
                "Status": 2,
                "Data": {"Invoices": [{"Ikey": "SI-TEST-0001", "InvoiceStatus": 0}]},
            }
        with patch.object(provider, "_api_call_easy", side_effect=fake_api_call):
            provider.push_draft_invoice(_make_payload())
        self.assertEqual(captured.get("Pattern"), "1C26TYY")
        self.assertEqual(captured.get("Serial"), "K24TYY")
        self.assertIn("XmlData", captured)

    def test_payload_missing_pattern_throws(self):
        provider = _make_provider(pattern="", serial="K24TYY")
        # The provider-level check is in map_sales_invoice_to_payload.
        # The EInvoiceProviderError is raised before si_doc fields are touched.
        with self.assertRaises(EInvoiceProviderError):
            provider.map_sales_invoice_to_payload(MagicMock(), None)

    def test_payload_empty_serial_allowed(self):
        """SoftDreams 2026-05-08: chỉ Pattern bắt buộc, Serial gửi rỗng."""
        provider = _make_provider(pattern="1C26TYY", serial="")
        captured = {}
        def fake_api_call(method, resource, **kwargs):
            captured.update(kwargs.get("json", {}))
            return {
                "Status": 2,
                "Data": {"Invoices": [{"Ikey": "SI-TEST-0002", "InvoiceStatus": 0}]},
            }
        with patch.object(provider, "_api_call_easy", side_effect=fake_api_call):
            provider.push_draft_invoice(_make_payload(pattern="1C26TYY", serial=""))
        self.assertEqual(captured.get("Pattern"), "1C26TYY")
        self.assertEqual(captured.get("Serial"), "")

    def test_xml_data_well_formed(self):
        from xml.etree import ElementTree as ET
        provider = _make_provider()
        captured = {}
        def fake_api_call(method, resource, **kwargs):
            captured.update(kwargs.get("json", {}))
            return {
                "Status": 2,
                "Data": {"Invoices": [{"Ikey": "SI-TEST-0001", "InvoiceStatus": 0}]},
            }
        with patch.object(provider, "_api_call_easy", side_effect=fake_api_call):
            provider.push_draft_invoice(_make_payload())
        xml_str = captured.get("XmlData", "")
        self.assertTrue(xml_str, "XmlData should not be empty")
        root = ET.fromstring(xml_str)
        self.assertEqual(root.tag, "Invoices")


class TestSyncInvoiceState(unittest.TestCase):
    def test_sync_state_signed(self):
        provider = _make_provider()
        mock_resp = {
            "Status": 2,
            "Data": {
                "Invoices": [
                    {"Ikey": "SI-0001", "InvoiceStatus": 1, "InvoiceNo": "001", "LookupCode": "ABC123"}
                ]
            },
        }
        captured = {}
        def fake(method, path, **kw):
            captured["method"] = method
            captured["path"] = path
            return mock_resp
        with patch.object(provider, "_api_call_easy", side_effect=fake):
            result = provider.sync_invoice_state(["SI-0001"])
        # Endpoint verified 2026-05-08 against api.easyinvoice.vn — getInvoicesByIkeys
        # (not queryInvoicesByIkeys, that path 404s)
        self.assertEqual(captured["method"], "POST")
        self.assertEqual(captured["path"], "api/publish/getInvoicesByIkeys")
        self.assertIn("SI-0001", result)
        state = result["SI-0001"]
        self.assertEqual(state["invoice_status"], 1)
        self.assertIn("khai thuế", state["status_text"])
        self.assertEqual(state["no"], "001")
        self.assertEqual(state["lookup_code"], "ABC123")

    def test_sync_state_partial(self):
        provider = _make_provider()
        mock_resp = {
            "Status": 2,
            "Data": {
                "Invoices": [
                    {"Ikey": "SI-0001", "InvoiceStatus": 2, "InvoiceNo": "001"}
                ]
            },
        }
        with patch.object(provider, "_api_call_easy", return_value=mock_resp):
            result = provider.sync_invoice_state(["SI-0001", "SI-9999"])
        self.assertIn("SI-0001", result)
        self.assertIn("SI-9999", result)
        self.assertEqual(result["SI-9999"]["error"], "not_found")

    def test_status_code_to_text_all(self):
        provider = _make_provider()
        mapping = {
            0: "chờ ký", -1: "chờ ký", 1: "khai thuế",
            2: "khai thuế", 3: "thay thế", 4: "điều chỉnh",
            5: "hủy", 6: "chờ ký",
        }
        for code, fragment in mapping.items():
            text = provider._map_status_code_to_text(code)
            self.assertIn(fragment, text.lower(), f"Status {code}: '{text}' missing '{fragment}'")

    def test_download_pdf_magic_ok(self):
        provider = _make_provider()
        pdf_content = b"%PDF-1.5 test content"
        mock_resp = {
            "Status": 2,
            "Data": {"Content": base64.b64encode(pdf_content).decode()},
        }
        captured = {}
        def fake(method, path, **kw):
            captured["method"] = method
            captured["path"] = path
            captured["body"] = kw.get("json")
            return mock_resp
        with patch.object(provider, "_api_call_easy", side_effect=fake):
            result = provider.download_attachment("SI-0001", "pdf")
        # Endpoint verified 2026-05-08 — getInvoicePdf, body {"Ikey": ...} (no FileType)
        self.assertEqual(captured["path"], "api/publish/getInvoicePdf")
        self.assertEqual(captured["body"], {"Ikey": "SI-0001"})
        self.assertEqual(result, pdf_content)

    def test_download_pdf_magic_fail(self):
        provider = _make_provider()
        bad_content = b"<html>Error page</html>"
        mock_resp = {
            "Status": 2,
            "Data": {"Content": base64.b64encode(bad_content).decode()},
        }
        with patch.object(provider, "_api_call_easy", return_value=mock_resp):
            with self.assertRaises(EInvoiceProviderError):
                provider.download_attachment("SI-0001", "pdf")

    def test_download_xml_raises_until_endpoint_known(self):
        """XML download endpoint chưa xác định — raise rõ ràng để state_sync log + skip."""
        provider = _make_provider()
        with self.assertRaises(EInvoiceProviderError) as ctx:
            provider.download_attachment("SI-0001", "xml")
        self.assertIn("XML", str(ctx.exception.message))
        self.assertIn("SoftDreams", str(ctx.exception.message))


if __name__ == "__main__":
    unittest.main()
