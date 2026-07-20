"""Unit tests for Phase 0 prepaid expense (TK 242) row builder."""

from __future__ import annotations

import unittest
from unittest.mock import patch


class TestBuildPrepaidRows(unittest.TestCase):

    def test_emits_dr_242_row_per_active_prepaid(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_prepaid
        with patch.object(opening_prepaid, "frappe") as mock_frappe:
            mock_frappe.get_single.return_value = type(
                "X", (), {"mappings": '{"242":"242 - Prepaid - DC"}'}
            )()
            mock_frappe.db.get_value.return_value = None  # mapping covers it

            rows = [
                {"prepaid_code": "CPTTK_205VIETTELHC", "prepaid_name": "Thuê HTHCC",
                 "recognition_date": "2024-11-01",
                 "total_amount": 738_000, "remaining_amount": 246_000,
                 "total_periods": 3, "remaining_periods": 1,
                 "per_period_amount": 246_000, "holding_account": "242"},
                {"prepaid_code": "CPTTVT_549VIETTEL", "prepaid_name": "Cước FTTH",
                 "recognition_date": "2024-10-01",
                 "total_amount": 3_600_000, "remaining_amount": 2_057_142,
                 "total_periods": 7, "remaining_periods": 4,
                 "per_period_amount": 514_286, "holding_account": "242"},
            ]
            r = opening_prepaid.build_prepaid_rows(rows, "DC")
            self.assertEqual(r["prepaid_count"], 2)
            self.assertEqual(len(r["rows"]), 2)
            self.assertEqual(r["total_dr"], 246_000 + 2_057_142)
            self.assertEqual(r["schedule_pending"], 2)
            for row in r["rows"]:
                self.assertEqual(row["account"], "242 - Prepaid - DC")
                self.assertEqual(row["credit_in_account_currency"], 0.0)
                self.assertGreater(row["debit_in_account_currency"], 0)
                self.assertIn("OB Prepaid", row["user_remark"])

    def test_skips_zero_remaining_amount(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_prepaid
        with patch.object(opening_prepaid, "frappe") as mock_frappe:
            mock_frappe.get_single.return_value = type(
                "X", (), {"mappings": '{"242":"X"}'}
            )()
            rows = [
                {"prepaid_code": "FULL_AMORTIZED", "remaining_amount": 0,
                 "holding_account": "242"},
                {"prepaid_code": "STILL_OPEN", "remaining_amount": 500_000,
                 "holding_account": "242", "total_periods": 5,
                 "remaining_periods": 1},
            ]
            r = opening_prepaid.build_prepaid_rows(rows, "DC")
            self.assertEqual(r["prepaid_count"], 1)
            self.assertEqual(r["rows"][0]["debit_in_account_currency"], 500_000)

    def test_skips_when_tk_unmappable(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_prepaid
        with patch.object(opening_prepaid, "frappe") as mock_frappe:
            mock_frappe.get_single.return_value = type(
                "X", (), {"mappings": '{}'}
            )()
            mock_frappe.db.get_value.return_value = None  # not in DB either
            rows = [{
                "prepaid_code": "X", "remaining_amount": 100_000,
                "holding_account": "242",
            }]
            r = opening_prepaid.build_prepaid_rows(rows, "DC")
            self.assertEqual(r["prepaid_count"], 0)
            self.assertEqual(len(r["skipped"]), 1)
            self.assertIn("không map", r["skipped"][0]["reason"])

    def test_defaults_to_tk_242_when_holding_account_missing(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_prepaid
        with patch.object(opening_prepaid, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "242 - Prepaid - DC"
            rows = [{
                "prepaid_code": "X", "remaining_amount": 100_000,
                # holding_account omitted → defaults to "242"
            }]
            r = opening_prepaid.build_prepaid_rows(rows, "DC", mapping={})
            self.assertEqual(r["prepaid_count"], 1)
            # Verify get_value was called with account_number="242"
            args, kwargs = mock_frappe.db.get_value.call_args
            self.assertEqual(args[1]["account_number"], "242")

    def test_skipped_records_when_no_code(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_prepaid
        with patch.object(opening_prepaid, "frappe"):
            rows = [{"prepaid_code": None, "remaining_amount": 100}]
            r = opening_prepaid.build_prepaid_rows(rows, "DC", mapping={})
            self.assertEqual(len(r["skipped"]), 1)
            self.assertEqual(r["skipped"][0]["code"], None)

    def test_user_remark_truncation(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_prepaid
        long_name = "X" * 300
        with patch.object(opening_prepaid, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "ACCT"
            rows = [{
                "prepaid_code": "CODE", "prepaid_name": long_name,
                "remaining_amount": 100, "holding_account": "242",
                "total_periods": 10, "remaining_periods": 5,
            }]
            r = opening_prepaid.build_prepaid_rows(rows, "DC", mapping={})
            self.assertLessEqual(len(r["rows"][0]["user_remark"]), 140)


class TestOpeningJournalIntegration(unittest.TestCase):
    """Verify post_opening_journal now accepts + processes prepaid_rows."""

    def test_prepaid_rows_appended_to_je(self):
        from vn_accounting.misa_migration.importers.ob_handlers import opening_journal
        captured = []

        class MockDoc:
            def __init__(self, p): self.payload = p; self.name = p.get("misa_voucher_no")
            def insert(self, set_name=None): self.name = set_name or self.name
            flags = type("F", (), {"ignore_permissions": False})()

        with patch.object(opening_journal, "frappe") as mock_frappe, \
             patch.object(opening_journal, "_resolve_account",
                          return_value="X - DC"), \
             patch.object(opening_journal, "_account_is_leaf", return_value=True), \
             patch.object(opening_journal, "_load_account_mapping", return_value={}), \
             patch.object(opening_journal, "_temporary_opening_account",
                          return_value="4211"):
            mock_frappe.db.exists.side_effect = lambda dt, name: dt != "Journal Entry"
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.get_doc = lambda p: captured.append(p) or MockDoc(p)
            # Mock the build_prepaid_rows call inside opening_journal
            with patch("vn_accounting.misa_migration.importers.ob_handlers"
                       ".opening_prepaid.build_prepaid_rows") as mock_build:
                mock_build.return_value = {
                    "rows": [{
                        "account": "242 - DC",
                        "debit_in_account_currency": 1_000_000,
                        "credit_in_account_currency": 0.0,
                        "user_remark": "OB Prepaid CODE — Test",
                    }],
                    "skipped": [],
                    "total_dr": 1_000_000,
                    "prepaid_count": 1,
                    "schedule_pending": 1,
                }
                r = opening_journal.post_opening_journal(
                    batch_name="BATCH-P",
                    prepaid_rows=[{"prepaid_code": "CODE",
                                   "remaining_amount": 1_000_000,
                                   "holding_account": "242"}],
                )
                self.assertEqual(r["status"], "created")
                self.assertEqual(r["prepaid_count"], 1)
                # Verify the 242 row landed in the JE accounts
                pl = captured[0]
                accounts = pl["accounts"]
                # Includes 1 prepaid row + 1 residual balancing row
                self.assertGreaterEqual(len(accounts), 1)
                self.assertTrue(
                    any(a["account"] == "242 - DC" for a in accounts),
                    "Prepaid 242 row missing from Opening JE accounts"
                )


if __name__ == "__main__":
    unittest.main()
