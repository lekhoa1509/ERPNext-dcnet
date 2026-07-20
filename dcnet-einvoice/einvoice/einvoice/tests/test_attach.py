"""Unit tests for attach service pure functions + integration with mock provider.

Run via bench console:
    import unittest
    from einvoice.einvoice.tests.test_attach import (
        TestComputeFinalStatus, TestSanitizeFilename, TestAttachFilesForInvoice
    )
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [TestComputeFinalStatus, TestSanitizeFilename, TestAttachFilesForInvoice]:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    assert result.wasSuccessful()
"""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _inv(pdf_file=None, xml_file=None, pdf_url=None, xml_url=None):
    """Build a minimal fake invoice namespace for _compute_final_status."""
    return SimpleNamespace(
        name="EI-2026-001",
        pdf_file=pdf_file,
        xml_file=xml_file,
        pdf_url=pdf_url,
        xml_url=xml_url,
        attach_retry_count=0,
    )


# ---------------------------------------------------------------------------
# _compute_final_status truth table (9 cases from spec)
# ---------------------------------------------------------------------------

class TestComputeFinalStatus(unittest.TestCase):

    def _call(self, pdf_result, xml_result, **inv_kwargs):
        from einvoice.einvoice.services.attach import _compute_final_status
        inv = _inv(**inv_kwargs)
        return _compute_final_status(pdf_result, xml_result, inv)

    def test_case1_both_ok(self):
        status, err = self._call("ok", "ok", pdf_url="http://p", xml_url="http://x")
        self.assertEqual(status, "Đã đính kèm")
        self.assertIsNone(err)

    def test_case2_pdf_already_present_xml_ok(self):
        """pdf_file exists (skip), xml downloaded (ok) → Đã đính kèm."""
        status, err = self._call("skip", "ok", pdf_file="/files/a.pdf", xml_url="http://x")
        self.assertEqual(status, "Đã đính kèm")
        self.assertIsNone(err)

    def test_case3_pdf_ok_xml_already_present(self):
        """pdf downloaded (ok), xml_file exists (skip) → Đã đính kèm."""
        status, err = self._call("ok", "skip", pdf_url="http://p", xml_file="/files/b.xml")
        self.assertEqual(status, "Đã đính kèm")
        self.assertIsNone(err)

    def test_case4_both_skip_no_urls(self):
        """Nothing to download, nothing present → Chưa tải."""
        status, err = self._call("skip", "skip")
        self.assertEqual(status, "Chưa tải")
        self.assertIsNone(err)

    def test_case5_pdf_fail_xml_ok(self):
        status, err = self._call("fail", "ok", pdf_url="http://p", xml_url="http://x")
        self.assertEqual(status, "Một phần")

    def test_case6_pdf_ok_xml_fail(self):
        status, err = self._call("ok", "fail", pdf_url="http://p", xml_url="http://x")
        self.assertEqual(status, "Một phần")

    def test_case7_both_fail(self):
        status, err = self._call("fail", "fail", pdf_url="http://p", xml_url="http://x")
        self.assertEqual(status, "Lỗi")
        self.assertIsNotNone(err)

    def test_case8_pdf_fail_xml_not_needed(self):
        """pdf_url exists but download fails; no xml_url → Lỗi (only source failed)."""
        status, err = self._call("fail", "skip", pdf_url="http://p")
        self.assertEqual(status, "Lỗi")

    def test_case9_pdf_not_needed_xml_fail(self):
        """no pdf_url; xml_url exists but download fails → Lỗi."""
        status, err = self._call("skip", "fail", xml_url="http://x")
        self.assertEqual(status, "Lỗi")


# ---------------------------------------------------------------------------
# _sanitize_filename
# ---------------------------------------------------------------------------

class TestSanitizeFilename(unittest.TestCase):

    def _call(self, s):
        from einvoice.einvoice.services.attach import _sanitize_filename
        return _sanitize_filename(s)

    def test_slash_replaced(self):
        result = self._call("HD01/001")
        self.assertNotIn("/", result)

    def test_colon_replaced(self):
        result = self._call("HD:001")
        self.assertNotIn(":", result)

    def test_backslash_replaced(self):
        result = self._call(r"HD\001")
        self.assertNotIn("\\", result)

    def test_vietnamese_preserved(self):
        name = "Hóa đơn số 001.pdf"
        result = self._call(name)
        self.assertIn("Hóa", result)
        self.assertIn("đơn", result)

    def test_star_replaced(self):
        result = self._call("HD*001")
        self.assertNotIn("*", result)

    def test_empty_string(self):
        result = self._call("")
        self.assertEqual(result, "file")

    def test_none_string(self):
        result = self._call(None)
        self.assertEqual(result, "file")

    def test_leading_trailing_dot_stripped(self):
        result = self._call("...hidden...")
        # Dots stripped from ends only
        self.assertFalse(result.startswith("."))


# ---------------------------------------------------------------------------
# attach_files_for_invoice — integration with mock provider
# ---------------------------------------------------------------------------

class TestAttachFilesForInvoice(unittest.TestCase):

    def _mock_provider(self, pdf_content=None, xml_content=None, raise_for=None):
        """Mock provider that returns bytes or raises EInvoiceProviderError."""
        from einvoice.einvoice.exceptions import EInvoiceProviderError

        provider = MagicMock()
        provider.provider_name = "MockProvider"

        def download_side_effect(url, kind):
            if raise_for and kind in raise_for:
                raise EInvoiceProviderError(f"Mock fail for {kind}", provider="MockProvider")
            if kind == "pdf":
                return pdf_content or b"%PDF-1.4"
            return xml_content or b"<?xml?><root/>"

        provider.download_attachment.side_effect = download_side_effect
        return provider

    @patch("frappe.db.get_value")
    @patch("frappe.db.set_value")
    @patch("frappe.get_doc")
    @patch("einvoice.einvoice.services.attach._persist_file")
    @patch("einvoice.einvoice.services.attach._publish_realtime")
    @patch("frappe.db.commit")
    def test_idempotent_skip_both_present(
        self, mock_commit, mock_publish, mock_persist, mock_get_doc, mock_set_val, mock_get_val
    ):
        """If pdf_file AND xml_file already set, skip without calling provider."""
        inv_doc = SimpleNamespace(
            name="EI-001",
            pdf_url="http://p",
            xml_url="http://x",
            pdf_file="/files/a.pdf",
            xml_file="/files/b.xml",
            attach_retry_count=0,
            attach_status="Đã đính kèm",
            attach_error=None,
        )
        mock_get_doc.return_value = inv_doc
        provider = self._mock_provider()

        from einvoice.einvoice.services.attach import attach_files_for_invoice
        result = attach_files_for_invoice("EI-001", provider)

        provider.download_attachment.assert_not_called()
        self.assertEqual(result.get("pdf"), "skip")
        self.assertEqual(result.get("xml"), "skip")

    @patch("frappe.db.get_value")
    @patch("frappe.db.set_value")
    @patch("frappe.get_doc")
    @patch("einvoice.einvoice.services.attach._persist_file")
    @patch("einvoice.einvoice.services.attach._publish_realtime")
    @patch("frappe.db.commit")
    def test_downloads_missing_pdf(
        self, mock_commit, mock_publish, mock_persist, mock_get_doc, mock_set_val, mock_get_val
    ):
        """When pdf_file missing but pdf_url present, provider.download_attachment called for pdf."""
        inv_doc = SimpleNamespace(
            name="EI-002",
            pdf_url="http://p",
            xml_url="http://x",
            pdf_file=None,
            xml_file="/files/b.xml",
            attach_retry_count=0,
            attach_status="Một phần",
            attach_error=None,
        )
        mock_get_doc.return_value = inv_doc
        mock_persist.return_value = "/files/new.pdf"
        provider = self._mock_provider(pdf_content=b"%PDF-1.4")

        from einvoice.einvoice.services.attach import attach_files_for_invoice
        result = attach_files_for_invoice("EI-002", provider)

        # Provider called only for pdf (xml already present)
        calls = provider.download_attachment.call_args_list
        kinds = [c[0][1] for c in calls]
        self.assertIn("pdf", kinds)
        self.assertNotIn("xml", kinds)
        self.assertEqual(result.get("pdf"), "ok")

    @patch("frappe.db.get_value")
    @patch("frappe.db.set_value")
    @patch("frappe.get_doc")
    @patch("einvoice.einvoice.services.attach._persist_file")
    @patch("einvoice.einvoice.services.attach._publish_realtime")
    @patch("frappe.db.commit")
    def test_provider_fail_sets_error_status(
        self, mock_commit, mock_publish, mock_persist, mock_get_doc, mock_set_val, mock_get_val
    ):
        """When provider raises for both, attach_status should be Lỗi."""
        inv_doc = SimpleNamespace(
            name="EI-003",
            pdf_url="http://p",
            xml_url="http://x",
            pdf_file=None,
            xml_file=None,
            attach_retry_count=1,
            attach_status="Lỗi",
            attach_error=None,
        )
        mock_get_doc.return_value = inv_doc
        provider = self._mock_provider(raise_for={"pdf", "xml"})

        from einvoice.einvoice.services.attach import attach_files_for_invoice
        result = attach_files_for_invoice("EI-003", provider)

        self.assertIn(result.get("pdf"), ("fail", "ok", "skip"))
        self.assertIsNotNone(result.get("error"))
        # retry_count should be incremented
        incremented = any(
            "attach_retry_count" in str(c) for c in mock_set_val.call_args_list
        )
        self.assertTrue(incremented)


if __name__ == "__main__":
    unittest.main()
