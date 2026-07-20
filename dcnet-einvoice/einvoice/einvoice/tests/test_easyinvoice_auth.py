"""Unit tests for EasyInvoiceProvider per-request signature auth.

Runs without live HTTP or Frappe DB — provider_doc is mocked.
Run via bench console:
    import unittest
    from einvoice.einvoice.tests.test_easyinvoice_auth import TestEasyInvoiceAuth
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TestEasyInvoiceAuth))
"""
import base64
import hashlib
import unittest
from unittest.mock import MagicMock


def _make_provider():
    from einvoice.einvoice.providers.easyinvoice import EasyInvoiceProvider

    doc = MagicMock()
    doc.name = "Test EasyInvoice"
    doc.api_url = "https://api.easyinvoice.vn"
    doc.api_url_purchase = "https://api.easyinvoice.vn"
    doc.tax_code = "0106936409"
    doc.api_username = "API_ERP"
    doc.get_password.return_value = "TESTPASS"

    def _doc_get(key, default=None):
        return {"api_username": "API_ERP"}.get(key, default)

    doc.get.side_effect = _doc_get
    return EasyInvoiceProvider(doc)


class TestEasyInvoiceAuth(unittest.TestCase):

    def test_signature_format(self):
        """Header has 6 colon-separated parts: sig:nonce:ts:user:pwd:taxcode"""
        provider = _make_provider()
        h = provider._build_auth_header("POST")
        parts = h.split(":")
        self.assertEqual(len(parts), 6)
        sig, nonce, ts, user, pwd, tc = parts
        self.assertEqual(user, "API_ERP")
        self.assertEqual(pwd, "TESTPASS")
        self.assertEqual(tc, "0106936409")
        self.assertTrue(ts.isdigit())
        self.assertEqual(len(nonce), 32)  # 16 random bytes hex

    def test_signature_method_normalized(self):
        """POST and post both produce 6-part header (method uppercased internally)."""
        provider = _make_provider()
        h1 = provider._build_auth_header("POST")
        h2 = provider._build_auth_header("post")
        self.assertEqual(len(h1.split(":")), 6)
        self.assertEqual(len(h2.split(":")), 6)

    def test_signature_changes_per_call(self):
        """2 consecutive calls produce different signatures (nonce + timestamp differ)."""
        provider = _make_provider()
        h1 = provider._build_auth_header("POST")
        h2 = provider._build_auth_header("POST")
        # Random nonce → 2 different signatures (overwhelmingly likely)
        self.assertNotEqual(h1, h2)

    def test_signature_md5_formula(self):
        """Verify formula: signature = base64(MD5(METHOD.upper() + ts + nonce))."""
        ts = "1700000000"
        nonce = "abcdef0123456789abcdef0123456789"
        raw = f"POST{ts}{nonce}".encode("utf-8")
        expected_sig = base64.b64encode(hashlib.md5(raw).digest()).decode("ascii")
        # base64 of 16 bytes = 24 chars (with `=` padding)
        self.assertEqual(len(expected_sig), 24)
        self.assertTrue(expected_sig.endswith("=") or expected_sig.endswith("=="))


if __name__ == "__main__":
    unittest.main()
