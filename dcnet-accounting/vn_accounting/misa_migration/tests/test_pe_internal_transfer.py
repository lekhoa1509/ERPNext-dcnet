"""Unit tests for PE Internal Transfer detection + JE Bank Entry cheque_no auto-fill.

Both are submit-time fixes that landed after first E2E surfaced:
  - 142× ValidationError "Reference No & Reference Date is required for
    Bank Entry" on JE submit
  - 14× ValidationError "Party Type and Party can only be set for
    Receivable / Payable account" on PE submit (PT internal cash transfer
    misclassified as Customer Receive)

These tests verify the handler builds the right payload BEFORE insert so
the doc submits cleanly downstream.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestPEInternalTransferDetection(unittest.TestCase):
    """When the resolved party_leg account is Bank or Cash (not AR/AP), the
    handler must build the PE as `payment_type='Internal Transfer'` with no
    party — not as Customer Receive."""

    def _common_mocks(self, mock_frappe, *, party_account_type: str,
                      paid_account_type: str = "Cash"):
        """Configure frappe mocks so PE builds for a bank↔cash voucher."""
        # _company_default returns 'DCT'
        mock_frappe.db.exists.return_value = True  # Mode of Payment exists
        mock_frappe.db.get_value.side_effect = (
            lambda dt, name, field=None, *a, **k:
                paid_account_type if "111" in str(name)
                else party_account_type if "112" in str(name)
                else None
        )

    def test_pt_bank_to_cash_classifies_as_internal_transfer(self):
        """PT with Dr 111 / Cr 112 → Internal Transfer, no party set."""
        from vn_accounting.misa_migration.importers.nkc_handlers import payment_entry

        voucher = {
            "voucher_no": "PT20260001",
            "posting_date": "2026-01-15",
            "party_code": "DCNET",  # placeholder, would be Customer in misclass
            "legs": [
                {"account": "111", "debit": 30000000, "credit": 0},
                {"account": "112", "debit": 0, "credit": 30000000},
            ],
        }

        captured_payload: dict = {}

        class MockDoc:
            def __init__(self, p):
                self.payload = p
                self.name = None
            flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name
                captured_payload.update(self.payload)

        with patch.object(payment_entry, "frappe") as mock_frappe, \
             patch.object(payment_entry, "_get_company", return_value="DCT"), \
             patch.object(payment_entry, "_resolve_account",
                          side_effect=lambda tk, m, c: f"{tk} - DCT"):
            # Account.account_type lookup: 111='Cash', 112='Bank'
            def gv(dt, name, field=None, *a, **k):
                if dt == "Account" and field == "account_type":
                    if "111" in str(name): return "Cash"
                    if "112" in str(name): return "Bank"
                return None
            mock_frappe.db.get_value.side_effect = gv
            # Mode of Payment exists; Payment Entry does NOT (so we create new)
            mock_frappe.db.exists.side_effect = (
                lambda dt, name=None, *a, **k:
                    True if dt == "Mode of Payment" else False
            )
            mock_frappe.get_doc = lambda p: MockDoc(p)

            result = payment_entry.create_pe_from_pt(voucher)

            self.assertEqual(result["status"], "created", f'got: {result}')
            # CRITICAL: Internal Transfer, not "Receive"
            self.assertEqual(captured_payload["payment_type"], "Internal Transfer")
            self.assertIsNone(captured_payload["party_type"])
            self.assertIsNone(captured_payload["party"])
            # paid_from = Bank (Cr side); paid_to = Cash (Dr side, paid_leg)
            self.assertIn("112", captured_payload["paid_from"])
            self.assertIn("111", captured_payload["paid_to"])

    def test_pt_customer_receive_keeps_party(self):
        """PT with Dr 111 / Cr 131 → Receive, party preserved."""
        from vn_accounting.misa_migration.importers.nkc_handlers import payment_entry

        voucher = {
            "voucher_no": "PT20260100",
            "posting_date": "2026-01-15",
            "party_code": "CUST001",
            "party_name": "Customer 1",
            "legs": [
                {"account": "111", "debit": 5000000, "credit": 0},
                {"account": "131", "debit": 0, "credit": 5000000},
            ],
        }

        captured_payload: dict = {}

        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = None
            flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name; captured_payload.update(self.payload)

        with patch.object(payment_entry, "frappe") as mock_frappe, \
             patch.object(payment_entry, "_get_company", return_value="DCT"), \
             patch.object(payment_entry, "_resolve_account",
                          side_effect=lambda tk, m, c: f"{tk} - DCT"), \
             patch.object(payment_entry, "_detect_party_type",
                          return_value="Customer"):
            def gv(dt, name, field=None, *a, **k):
                if dt == "Account" and field == "account_type":
                    if "111" in str(name): return "Cash"
                    if "131" in str(name): return "Receivable"
                return None
            mock_frappe.db.get_value.side_effect = gv
            mock_frappe.db.exists.side_effect = (
                lambda dt, name=None, *a, **k:
                    True if dt in ("Mode of Payment", "Customer") else False
            )
            mock_frappe.get_doc = lambda p: MockDoc(p)

            result = payment_entry.create_pe_from_pt(voucher)
            self.assertEqual(result["status"], "created", f'got: {result}')
            self.assertEqual(captured_payload["payment_type"], "Receive")
            self.assertEqual(captured_payload["party_type"], "Customer")
            self.assertEqual(captured_payload["party"], "CUST001")


class TestJEBankEntryChequeAutoFill(unittest.TestCase):
    """Bank Entry / Cash Entry JE need cheque_no + cheque_date on submit.
    The handler sets them at insert-time from voucher_no + posting_date."""

    def test_bank_entry_gets_cheque_no(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry

        voucher = {
            "voucher_no": "CTNB20260001",
            "posting_date": "2026-01-15",
            "voucher_remark": "Chuyển tiền nội bộ",
            "legs": [
                {"account": "1121", "debit": 1000000, "credit": 0},
                {"account": "1122", "debit": 0, "credit": 1000000},
            ],
        }

        captured_payload: dict = {}

        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = None
            flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name; captured_payload.update(self.payload)

        with patch.object(journal_entry, "frappe") as mock_frappe, \
             patch.object(journal_entry, "_get_company", return_value="DCT"), \
             patch.object(journal_entry, "_resolve_account",
                          side_effect=lambda tk, m, c: f"{tk} - DCT"):
            mock_frappe.db.exists.return_value = False  # no dup
            mock_frappe.db.get_value.return_value = None  # not Depreciation, not Stock
            mock_frappe.get_doc = lambda p: MockDoc(p)

            result = journal_entry.create_je_from_ctnb(voucher)

            self.assertEqual(result["status"], "created")
            self.assertEqual(captured_payload["voucher_type"], "Bank Entry")
            # CRITICAL: cheque_no + cheque_date present
            self.assertEqual(captured_payload["cheque_no"], "CTNB20260001")
            self.assertEqual(captured_payload["cheque_date"], "2026-01-15")

    def test_journal_entry_no_cheque_fields(self):
        """Regular Journal Entry voucher_type doesn't get cheque_no
        (only Bank/Cash Entry do)."""
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry

        voucher = {
            "voucher_no": "NVK20260001",
            "posting_date": "2026-01-15",
            "voucher_remark": "Bút toán khác",
            "legs": [
                {"account": "642", "debit": 100000, "credit": 0},
                {"account": "1111", "debit": 0, "credit": 100000},
            ],
        }

        captured_payload: dict = {}

        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = None
            flags = type("F", (), {"ignore_permissions": False})()
            def insert(self, set_name=None):
                self.name = set_name; captured_payload.update(self.payload)

        with patch.object(journal_entry, "frappe") as mock_frappe, \
             patch.object(journal_entry, "_get_company", return_value="DCT"), \
             patch.object(journal_entry, "_resolve_account",
                          side_effect=lambda tk, m, c: f"{tk} - DCT"):
            mock_frappe.db.exists.return_value = False
            mock_frappe.db.get_value.return_value = None
            mock_frappe.get_doc = lambda p: MockDoc(p)

            result = journal_entry.create_je_from_nvk(voucher)
            self.assertEqual(result["status"], "created")
            self.assertEqual(captured_payload["voucher_type"], "Journal Entry")
            # NO cheque_no for non-bank JEs
            self.assertNotIn("cheque_no", captured_payload)


class TestSubmitPhase4Drafts(unittest.TestCase):
    """`submit_phase_4_drafts` orchestrator: per-doc commit, stock workaround,
    large-JE _submit() bypass."""

    def test_returns_summary_with_per_doctype_counts(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator

        # 2 SI, 1 JE — all submit OK
        # Use a counter to return different name lists per DocType call
        sql_list_results = iter([
            [],  # workaround query (Stock accounts)
            ["SE-001"],  # Stock Entry
            ["JE-001"],  # JE
            ["SI-001", "SI-002"],  # SI
            [],  # PI
            [],  # PE
        ])

        class MockDoc:
            def __init__(self, name): self.name = name; self.accounts = []
            flags = type("F", (), {"ignore_permissions": False})()
            def submit(self): pass
            def _submit(self): pass

        with patch.object(phase_4_orchestrator, "frappe") as mock_frappe, \
             patch("vn_accounting.misa_migration.context.get_active_company",
                   return_value="DCT"):
            mock_frappe.db.sql_list = lambda *a, **k: next(sql_list_results)
            mock_frappe.db.commit = lambda: None
            mock_frappe.db.rollback = lambda: None
            mock_frappe.db.set_value = lambda *a, **k: None
            mock_frappe.get_doc = lambda dt, name: MockDoc(name)

            r = phase_4_orchestrator.submit_phase_4_drafts(company="DCT")
            self.assertEqual(r["total_submitted"], 4)
            self.assertEqual(r["total_failed"], 0)
            self.assertEqual(r["submitted"].get("Stock Entry"), 1)
            self.assertEqual(r["submitted"].get("Journal Entry"), 1)
            self.assertEqual(r["submitted"].get("Sales Invoice"), 2)

    def test_per_doc_failure_doesnt_cascade(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator

        # 3 PE: 1st fails, 2nd OK, 3rd OK → 2 submitted, 1 failed
        sql_list_results = iter([
            [],  # Stock account workaround query
            [],  # Stock Entry
            [],  # JE
            [],  # SI
            [],  # PI
            ["PE-001", "PE-002", "PE-003"],  # PE
        ])
        call_count = [0]

        class MockDoc:
            def __init__(self, name):
                self.name = name; self.accounts = []
            flags = type("F", (), {"ignore_permissions": False})()
            def submit(self):
                call_count[0] += 1
                if call_count[0] == 1:
                    raise RuntimeError("kaboom")
            def _submit(self): pass

        with patch.object(phase_4_orchestrator, "frappe") as mock_frappe, \
             patch("vn_accounting.misa_migration.context.get_active_company",
                   return_value="DCT"):
            mock_frappe.db.sql_list = lambda *a, **k: next(sql_list_results)
            mock_frappe.db.commit = lambda: None
            mock_frappe.db.rollback = lambda: None
            mock_frappe.db.set_value = lambda *a, **k: None
            mock_frappe.get_doc = lambda dt, name: MockDoc(name)
            mock_frappe.log_error = lambda **k: None

            r = phase_4_orchestrator.submit_phase_4_drafts(company="DCT")
            self.assertEqual(r["submitted"].get("Payment Entry"), 2)
            self.assertEqual(len(r["failed"].get("Payment Entry", [])), 1)
            self.assertEqual(r["failed"]["Payment Entry"][0][0], "PE-001")


if __name__ == "__main__":
    unittest.main()
