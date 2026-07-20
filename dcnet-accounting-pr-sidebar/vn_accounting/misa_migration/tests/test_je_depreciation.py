"""Unit tests for PBPTT + KH JE handlers.

Both reuse `_create_je_1to1`. These tests verify the dispatch — that
each handler calls `_create_je_1to1` exactly once with the correct
voucher_type and unmodified voucher dict.

DB-touching insert paths (TK resolution, party detection, real
frappe.get_doc) are covered by E2E commit 15 + the existing C8 JE
handler tests for the shared helper.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch


class TestCreateJeFromPbptt(unittest.TestCase):
    """PBPTT (Phân bổ chi phí trả trước) → Journal Entry."""

    def test_calls_1to1_with_journal_entry_voucher_type(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.return_value = {"status": "created",
                                      "target_name": "PBPTT2026001"}
            v = {"voucher_no": "PBPTT2026001", "prefix": "PBPTT", "legs": []}
            result = journal_entry.create_je_from_pbptt(v)
            self.assertEqual(result["status"], "created")
            mock_1to1.assert_called_once()
            args, kwargs = mock_1to1.call_args
            # Positional: voucher dict; keyword: voucher_type
            self.assertIs(args[0], v)
            self.assertEqual(kwargs.get("voucher_type"), "Journal Entry")

    def test_signature_accepts_optional_invoice(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.return_value = {"status": "created"}
            v = {"voucher_no": "PBPTT2026001", "prefix": "PBPTT", "legs": []}
            # Should work whether invoice is passed or not (consistent with
            # router's create_<x>_from_<prefix>(voucher, invoice) shape).
            journal_entry.create_je_from_pbptt(v, invoice=None)
            journal_entry.create_je_from_pbptt(v, invoice={"foo": "bar"})
            self.assertEqual(mock_1to1.call_count, 2)


class TestCreateJeFromKh(unittest.TestCase):
    """KH (Khấu hao TSCĐ) → Depreciation Entry."""

    def test_calls_1to1_with_depreciation_entry_voucher_type(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.return_value = {"status": "created",
                                      "target_name": "KH2026001",
                                      "voucher_type": "Depreciation Entry"}
            v = {"voucher_no": "KH2026001", "prefix": "KH", "legs": []}
            result = journal_entry.create_je_from_kh(v)
            self.assertEqual(result["status"], "created")
            mock_1to1.assert_called_once()
            args, kwargs = mock_1to1.call_args
            self.assertIs(args[0], v)
            self.assertEqual(kwargs.get("voucher_type"), "Depreciation Entry")

    def test_signature_accepts_optional_invoice(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.return_value = {"status": "created"}
            v = {"voucher_no": "KH2026001", "prefix": "KH", "legs": []}
            journal_entry.create_je_from_kh(v, invoice=None)
            self.assertEqual(mock_1to1.call_count, 1)


class TestVoucherTypeAlignment(unittest.TestCase):
    """Cross-check the voucher_type values used here match ERPNext's
    Journal Entry Select options. If ERPNext ever renames "Depreciation
    Entry" the migration breaks silently — this is a soft contract check.
    """

    EXPECTED_TYPES = {
        "create_je_from_nvk": "Journal Entry",
        "create_je_from_ctnb": "Bank Entry",
        "create_je_from_ck": "Journal Entry",
        "create_je_from_pbdt": "Journal Entry",
        "create_je_from_pbptt": "Journal Entry",
        "create_je_from_kh": "Depreciation Entry",
    }

    def test_each_handler_uses_known_voucher_type(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        for fn_name, expected in self.EXPECTED_TYPES.items():
            with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
                mock_1to1.return_value = {"status": "created"}
                fn = getattr(journal_entry, fn_name)
                v = {"voucher_no": "X", "prefix": "X", "legs": []}
                fn(v)
                args, kwargs = mock_1to1.call_args
                self.assertEqual(
                    kwargs.get("voucher_type"), expected,
                    f"{fn_name} expected voucher_type={expected!r}, "
                    f"got {kwargs.get('voucher_type')!r}",
                )


if __name__ == "__main__":
    unittest.main()
