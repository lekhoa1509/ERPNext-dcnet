"""Unit tests for MatbaoProvider.download_attachment.

Runs without live HTTP or Frappe DB — all external calls are mocked.
Run via bench console:
    import unittest
    from einvoice.einvoice.tests.test_matbao_download import TestMatbaoDownload
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TestMatbaoDownload))
"""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch, call


def _make_provider():
    """Build a MatbaoProvider with a mock provider_doc (no DB needed)."""
    from einvoice.einvoice.providers.matbao import MatbaoProvider

    doc = SimpleNamespace(
        name="MatbaoTest",
        api_url="https://example.matbao.com/api",
        api_url_purchase="https://example.matbao.com/api/purchase",
        tax_code="0123456789",
        username="u",
        password="p",
        purchase_username="pu",
        purchase_password="pp",
        enable_inward=1,
        enable_outward=0,
    )
    # Patch frappe.cache so BaseProvider.__init__ doesn't fail
    with patch("frappe.cache", MagicMock()):
        provider = MatbaoProvider.__new__(MatbaoProvider)
        provider.provider_doc = doc
        provider.provider_name = doc.name
        provider.api_url = doc.api_url
        provider.api_url_purchase = doc.api_url_purchase
        provider.tax_code = doc.tax_code
    return provider


def _resp(status_code, content=b""):
    r = MagicMock()
    r.status_code = status_code
    r.content = content
    r.ok = (200 <= status_code < 300)
    return r


class TestMatbaoDownload(unittest.TestCase):

    def setUp(self):
        self.provider = _make_provider()
        self.provider._get_auth_headers = MagicMock(return_value={"Authorization": "Bearer tok"})
        self.provider._invalidate_cached_token = MagicMock()
        self.provider.authenticate = MagicMock()

    # ------------------------------------------------------------------
    # Success paths
    # ------------------------------------------------------------------

    @patch("time.sleep")
    @patch("requests.get")
    def test_200_ok_pdf(self, mock_get, mock_sleep):
        content = b"%PDF-1.4 hello"
        mock_get.return_value = _resp(200, content)

        result = self.provider.download_attachment("http://ex.com/file.pdf", "pdf")

        self.assertEqual(result, content)
        self.assertEqual(mock_get.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("time.sleep")
    @patch("requests.get")
    def test_200_ok_xml(self, mock_get, mock_sleep):
        content = b"<?xml version='1.0'?><root/>"
        mock_get.return_value = _resp(200, content)

        result = self.provider.download_attachment("http://ex.com/file.xml", "xml")

        self.assertEqual(result, content)
        self.assertEqual(mock_get.call_count, 1)

    # ------------------------------------------------------------------
    # 401 → refresh → success
    # ------------------------------------------------------------------

    @patch("time.sleep")
    @patch("requests.get")
    def test_401_then_200(self, mock_get, mock_sleep):
        content = b"%PDF-1.4 data"
        mock_get.side_effect = [_resp(401), _resp(200, content)]

        result = self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        self.assertEqual(result, content)
        self.provider._invalidate_cached_token.assert_called_once_with("purchase")
        self.provider.authenticate.assert_called_once()

    @patch("time.sleep")
    @patch("requests.get")
    def test_401_max_refresh_exceeded(self, mock_get, mock_sleep):
        """After 2 refreshes, provider should eventually exhaust attempts."""
        from einvoice.einvoice.exceptions import EInvoiceProviderError
        # 401s beyond the cap fill all attempts
        mock_get.return_value = _resp(401)

        with self.assertRaises(EInvoiceProviderError):
            self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        # _invalidate called at most 2 times (cap)
        self.assertLessEqual(self.provider._invalidate_cached_token.call_count, 2)

    # ------------------------------------------------------------------
    # 404 immediate raise
    # ------------------------------------------------------------------

    @patch("time.sleep")
    @patch("requests.get")
    def test_404_immediate_raise(self, mock_get, mock_sleep):
        from einvoice.einvoice.exceptions import EInvoiceProviderError
        mock_get.return_value = _resp(404)

        with self.assertRaises(EInvoiceProviderError) as ctx:
            self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        self.assertIn("404", str(ctx.exception))
        self.assertEqual(mock_get.call_count, 1)  # no retry on 404
        mock_sleep.assert_not_called()

    # ------------------------------------------------------------------
    # 500 retry paths
    # ------------------------------------------------------------------

    @patch("time.sleep")
    @patch("requests.get")
    def test_500_retry_then_success(self, mock_get, mock_sleep):
        content = b"%PDF ok"
        mock_get.side_effect = [_resp(500), _resp(200, content)]

        result = self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        self.assertEqual(result, content)
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called()  # backoff on 500

    @patch("time.sleep")
    @patch("requests.get")
    def test_500_retry_then_exhaust(self, mock_get, mock_sleep):
        from einvoice.einvoice.exceptions import EInvoiceProviderError
        mock_get.return_value = _resp(500)

        with self.assertRaises(EInvoiceProviderError):
            self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        self.assertEqual(mock_get.call_count, 3)  # 3 attempts

    # ------------------------------------------------------------------
    # Content sanity checks
    # ------------------------------------------------------------------

    @patch("time.sleep")
    @patch("requests.get")
    def test_pdf_wrong_magic_retries_and_fails(self, mock_get, mock_sleep):
        from einvoice.einvoice.exceptions import EInvoiceProviderError
        mock_get.return_value = _resp(200, b"<html>not a pdf</html>")

        with self.assertRaises(EInvoiceProviderError):
            self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        # Retried 3 times despite 200 status
        self.assertEqual(mock_get.call_count, 3)

    # ------------------------------------------------------------------
    # Network exception → retry
    # ------------------------------------------------------------------

    @patch("time.sleep")
    @patch("requests.get")
    def test_network_exception_retries(self, mock_get, mock_sleep):
        import requests as _requests
        from einvoice.einvoice.exceptions import EInvoiceProviderError
        mock_get.side_effect = _requests.exceptions.ConnectionError("timeout")

        with self.assertRaises(EInvoiceProviderError):
            self.provider.download_attachment("http://ex.com/f.pdf", "pdf")

        self.assertEqual(mock_get.call_count, 3)

    # ------------------------------------------------------------------
    # Invalid kind guard
    # ------------------------------------------------------------------

    def test_invalid_kind_raises_immediately(self):
        from einvoice.einvoice.exceptions import EInvoiceProviderError
        with self.assertRaises(EInvoiceProviderError):
            self.provider.download_attachment("http://ex.com/f", "zip")


if __name__ == "__main__":
    unittest.main()
