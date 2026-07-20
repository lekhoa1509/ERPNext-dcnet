"""B7 fix: UNC 'deferred' status → JE handler fallback in orchestrator."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestUncDeferredRouting(unittest.TestCase):
    """Phase 4 orchestrator: UNC handler returns 'deferred' for vouchers
    without Dr 331/141. Orchestrator must route to create_je_from_unc_deferred
    instead of marking the row Failed.

    Real-data E2E found 86 UNC vouchers in this state (loan principal,
    interest, tax, salary, bank fees) — all valid postings that should
    land as JE.
    """

    def _make_voucher(self):
        return {
            "voucher_no": "UNC20260003", "prefix": "UNC",
            "posting_date": "2026-01-05",
            "voucher_remark": "THANH TOAN LAI",
            "party_code": "VPBANK",
            "legs": [
                {"account": "635", "debit": 521_108, "credit": 0,
                 "leg_desc": "Interest"},
                {"account": "11218", "debit": 0, "credit": 521_108,
                 "leg_desc": "VPBank"},
            ],
        }

    def test_deferred_status_routes_to_je_fallback(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator
        from vn_accounting.misa_migration.importers import voucher_router

        # Mock router to return deferred status (simulates UNC handler
        # finding no Dr 331/141)
        deferred_result = {
            "status": "deferred",
            "voucher_no": "UNC20260003",
            "prefix": "UNC",
            "target_doctype": "Payment Entry",
            "target_name": None,
            "error": "UNC20260003: no Dr 331 / Dr 141 leg — route to JE handler",
            "voucher_kind": "je_fallback",
        }

        with patch.object(voucher_router, "route_voucher",
                          return_value=deferred_result), \
             patch.object(phase_4_orchestrator, "frappe") as mock_frappe, \
             patch.object(phase_4_orchestrator.nkc_parser, "parse_nkc_rows",
                          return_value=[self._make_voucher()]), \
             patch.object(phase_4_orchestrator.invoice_list_parser,
                          "parse_invoice_list", return_value=[]):
            mock_frappe.db.get_value.return_value = "DCNET TEST"
            mock_frappe.defaults.get_global_default.return_value = "DCNET TEST"
            mock_frappe.db.sql.return_value = [{
                "name": "row1", "file_type": "NKC",
                "raw_payload": '{"Số chứng từ": "UNC20260003"}',
            }]
            mock_frappe.log_error = MagicMock()

            # Mock create_je_from_unc_deferred to succeed
            with patch("vn_accounting.misa_migration.importers.nkc_handlers"
                       ".journal_entry.create_je_from_unc_deferred") as mock_je:
                mock_je.return_value = {
                    "status": "created",
                    "target_doctype": "Journal Entry",
                    "target_name": "UNC20260003",
                    "voucher_type": "Bank Entry",
                }
                summary = phase_4_orchestrator.run_phase_4_post("BATCH-X")
                # Voucher should land in Journal Entry posted bucket, NOT
                # Payment Entry failed bucket
                self.assertEqual(summary["total_vouchers"], 1)
                mock_je.assert_called_once()
                # by_target_doctype reflects the FINAL doctype (JE not PE)
                self.assertIn("Journal Entry", summary["by_target_doctype"])
                self.assertEqual(
                    summary["by_target_doctype"]["Journal Entry"]["posted"], 1,
                )

    def test_deferred_je_fallback_failure_counts_as_failed(self):
        """If even the JE fallback fails, voucher counts as failed."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator
        from vn_accounting.misa_migration.importers import voucher_router

        with patch.object(voucher_router, "route_voucher",
                          return_value={"status": "deferred",
                                        "target_doctype": "Payment Entry",
                                        "error": "deferred"}), \
             patch.object(phase_4_orchestrator, "frappe") as mock_frappe, \
             patch.object(phase_4_orchestrator.nkc_parser, "parse_nkc_rows",
                          return_value=[self._make_voucher()]), \
             patch.object(phase_4_orchestrator.invoice_list_parser,
                          "parse_invoice_list", return_value=[]):
            mock_frappe.db.get_value.return_value = "DC"
            mock_frappe.defaults.get_global_default.return_value = "DC"
            mock_frappe.db.sql.return_value = [{
                "name": "row1", "file_type": "NKC",
                "raw_payload": '{"Số chứng từ": "UNC20260003"}',
            }]
            mock_frappe.log_error = MagicMock()
            with patch("vn_accounting.misa_migration.importers.nkc_handlers"
                       ".journal_entry.create_je_from_unc_deferred") as mock_je:
                mock_je.return_value = {
                    "status": "failed",
                    "error": "TK X not mapped",
                }
                summary = phase_4_orchestrator.run_phase_4_post("BATCH-Y")
                self.assertGreater(len(summary["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
