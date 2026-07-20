"""Unit tests for MisaDefaultAccountImporter — Phase 2 default-account derivation."""
from __future__ import annotations

import json
import unittest
from collections import Counter
from unittest.mock import MagicMock, patch


class TestMisaDefaultAccountImporter(unittest.TestCase):

    def _make(self, company="DCNET TEST", mock_frappe=None):
        from vn_accounting.misa_migration.importers import misa_defaults as m
        mock_frappe = mock_frappe or MagicMock()
        mock_frappe.db.get_value.return_value = company
        with patch.object(m, "frappe", mock_frappe):
            imp = m.MisaDefaultAccountImporter("MM-T")
        imp._company = company
        return imp, mock_frappe

    def test_row_candidates_dr_cash_cr_receivable(self):
        imp, _ = self._make()
        cands = imp._row_candidates({
            "_loai": "Phiếu thu tiền khách hàng",
            "_tk_no": "1111",
            "_tk_co": "131",
        })
        # 1111 → default_cash_account, 131 → default_receivable_account
        fields = {(dt, fld) for dt, fld, _ in cands}
        self.assertIn(("Company", "default_cash_account"), fields)
        self.assertIn(("Company", "default_receivable_account"), fields)

    def test_row_candidates_vn_settings_loan(self):
        imp, _ = self._make()
        cands = imp._row_candidates({
            "_loai": "Vay ngân hàng",
            "_tk_no": "",
            "_tk_co": "3411",
        })
        fields = {(dt, fld) for dt, fld, _ in cands}
        self.assertIn(("VN Accounting Settings", "default_loan_account"), fields)

    def test_row_candidates_blank_returns_empty(self):
        imp, _ = self._make()
        self.assertEqual(imp._row_candidates({"_tk_no": "", "_tk_co": ""}), [])

    def test_row_candidates_unknown_tk_returns_empty(self):
        imp, _ = self._make()
        # 9999 is not in either map
        self.assertEqual(imp._row_candidates({"_tk_no": "9999", "_tk_co": ""}), [])

    def test_finalize_picks_most_frequent_tk_per_field(self):
        """Two candidate TKs for the same field → most-frequent wins."""
        imp, mf = self._make()
        # Seed bin manually — simulate 5 rows mapping to default_bank_account:
        # 11215 wins (3 votes) over 1121 (2 votes).
        imp._candidates = [
            ("Company", "default_bank_account", "1121"),
            ("Company", "default_bank_account", "11215"),
            ("Company", "default_bank_account", "11215"),
            ("Company", "default_bank_account", "11215"),
            ("Company", "default_bank_account", "1121"),
        ]
        # Mock account resolution + Company write
        def _resolve(tk, co):
            return f"{tk} - Acct - DCT"
        mf.db.set_value = MagicMock()
        with patch("vn_accounting.misa_migration.importers.misa_defaults._resolve_account_on_company",
                   side_effect=_resolve):
            with patch("vn_accounting.misa_migration.importers.misa_defaults.frappe", mf):
                result = imp.finalize()
        self.assertEqual(len(result["applied"]), 1)
        winner = result["applied"][0]
        self.assertEqual(winner["tk"], "11215")
        self.assertEqual(winner["vote_count"], 3)
        self.assertEqual(result["company_writes"]["default_bank_account"],
                         "11215 - Acct - DCT")

    def test_finalize_unresolved_tk_lands_in_skipped(self):
        imp, mf = self._make()
        imp._candidates = [("Company", "default_cash_account", "9999")]
        with patch("vn_accounting.misa_migration.importers.misa_defaults._resolve_account_on_company",
                   return_value=None):
            with patch("vn_accounting.misa_migration.importers.misa_defaults.frappe", mf):
                result = imp.finalize()
        self.assertEqual(len(result["applied"]), 0)
        self.assertEqual(len(result["skipped"]), 1)
        self.assertEqual(result["skipped"][0]["tk"], "9999")
        self.assertEqual(result["skipped"][0]["doctype"], "Company")
        self.assertEqual(result["skipped"][0]["field"], "default_cash_account")

    def test_finalize_empty_bin_returns_empty_summary(self):
        imp, _ = self._make()
        imp._candidates = []
        result = imp.finalize()
        self.assertEqual(result["applied"], [])
        self.assertIn("summary", result)

    def test_finalize_tie_break_lexicographic(self):
        """When two TKs tie on count, lexicographic ascending wins."""
        imp, mf = self._make()
        imp._candidates = [
            ("Company", "default_cash_account", "1112"),
            ("Company", "default_cash_account", "1111"),
        ]
        with patch("vn_accounting.misa_migration.importers.misa_defaults._resolve_account_on_company",
                   side_effect=lambda tk, _: f"{tk}-X"):
            with patch("vn_accounting.misa_migration.importers.misa_defaults.frappe", mf):
                result = imp.finalize()
        # Both tied at 1 vote — "1111" < "1112" lexicographic
        self.assertEqual(result["applied"][0]["tk"], "1111")

    def test_tk_to_company_field_map_covers_core_defaults(self):
        from vn_accounting.misa_migration.importers.misa_defaults import (
            TK_TO_COMPANY_FIELD as M,
        )
        # Sanity: critical Vietnamese accounts must map somewhere
        self.assertEqual(M.get("1111"), "default_cash_account")
        self.assertEqual(M.get("1121"), "default_bank_account")
        self.assertEqual(M.get("11215"), "default_bank_account")
        self.assertEqual(M.get("131"), "default_receivable_account")
        self.assertEqual(M.get("331"), "default_payable_account")
        self.assertEqual(M.get("5111"), "default_income_account")
        self.assertEqual(M.get("6321"), "default_expense_account")
        self.assertEqual(M.get("3341"), "default_payroll_payable_account")
        self.assertEqual(M.get("141"), "default_employee_advance_account")

    def test_tk_to_vn_settings_map_covers_vn_specific(self):
        from vn_accounting.misa_migration.importers.misa_defaults import (
            TK_TO_VN_SETTINGS_FIELD as M,
        )
        self.assertEqual(M.get("3411"), "default_loan_account")
        self.assertEqual(M.get("8211"), "corporate_income_tax_account")
        self.assertEqual(M.get("4211"), "retained_earnings_prior_year")
        self.assertEqual(M.get("4212"), "retained_earnings_current_year")
        self.assertEqual(M.get("911"), "pnl_account_911")
        self.assertEqual(M.get("154"), "wip_account_project_costing")


if __name__ == "__main__":
    unittest.main()
