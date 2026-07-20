"""Test that B01 balance sheet equation holds: mã_270 (Total Assets) == mã_440 (Total Equity + Liabilities).

These tests use mock GL data to verify that the resolver correctly computes balanced financials.
No Frappe DB context required — frappe.db.sql is patched per test.
"""
import sys
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

# Inject frappe stub for standalone running (without bench init)
_frappe_injected = "frappe" not in sys.modules
if _frappe_injected:
    sys.modules["frappe"] = MagicMock()
    sys.modules["frappe.utils"] = MagicMock()

import vn_accounting.financial_reporting.resolver as _resolver_mod  # noqa: E402

_PATCH_TARGET = "vn_accounting.financial_reporting.resolver.frappe"


def tearDownModule():
    if _frappe_injected:
        sys.modules.pop("frappe", None)
        sys.modules.pop("frappe.utils", None)
        sys.modules.pop("vn_accounting.financial_reporting.resolver", None)


def _sql_row(debit=0, credit=0):
    row = MagicMock()
    row.total_debit = Decimal(str(debit))
    row.total_credit = Decimal(str(credit))
    return row


def _build_b01_lines(asset_accounts, liability_equity_accounts):
    """Build a minimal B01 line list with formula lines 270 and 440.

    asset_accounts: list of (code, account_pattern, balance_as_debit)
    liability_equity_accounts: list of (code, account_pattern, balance_as_credit)
    """
    lines = []
    asset_codes = []
    for code, pattern, _ in asset_accounts:
        lines.append({
            "code": code,
            "value_type": "closing_debit",
            "account_formula": f"+{pattern}",
            "line_formula": "",
            "sign_multiplier": 1,
        })
        asset_codes.append(code)

    lines.append({
        "code": "270",
        "value_type": "formula",
        "account_formula": "",
        "line_formula": "=" + "+".join(asset_codes),
        "sign_multiplier": 1,
    })

    liability_codes = []
    for code, pattern, _ in liability_equity_accounts:
        lines.append({
            "code": code,
            "value_type": "closing_credit",
            "account_formula": f"+{pattern}",
            "line_formula": "",
            "sign_multiplier": 1,
        })
        liability_codes.append(code)

    lines.append({
        "code": "440",
        "value_type": "formula",
        "account_formula": "",
        "line_formula": "=" + "+".join(liability_codes),
        "sign_multiplier": 1,
    })
    return lines


class TestB01Equation(unittest.TestCase):
    """B01 balance sheet: mã_270 == mã_440 for various scenarios."""

    def _resolve_with_balances(self, mock_frappe, asset_accounts, liability_equity_accounts):
        """Run resolver with mocked GL returning specified balances, return code->Decimal map."""
        from vn_accounting.financial_reporting.resolver import resolve_all_lines

        # Map pattern (without trailing %) → balance
        debit_map = {pattern.rstrip("%"): Decimal(str(bal)) for _, pattern, bal in asset_accounts}
        credit_map = {pattern.rstrip("%"): Decimal(str(bal)) for _, pattern, bal in liability_equity_accounts}

        def fake_sql(query, values=None, *args, **kwargs):
            # resolver calls db.sql with a dict as values: {"company":..., "pattern":"111%", ...}
            # Extract pattern from the dict; fall back to iterating tuple/list.
            pat = None
            if isinstance(values, dict):
                pat = str(values.get("pattern", "")).rstrip("%")
            elif isinstance(values, (list, tuple)):
                for v in values:
                    v_str = str(v).rstrip("%")
                    if v_str in debit_map or v_str in credit_map:
                        pat = v_str
                        break

            if pat is not None:
                if pat in debit_map:
                    bal = float(debit_map[pat])
                    return [_sql_row(debit=bal, credit=0)]
                if pat in credit_map:
                    bal = float(credit_map[pat])
                    return [_sql_row(debit=0, credit=bal)]
            return [_sql_row(debit=0, credit=0)]

        mock_frappe.db.sql.side_effect = fake_sql
        mock_frappe.utils.getdate.side_effect = lambda d: d

        lines = _build_b01_lines(asset_accounts, liability_equity_accounts)
        results = resolve_all_lines("TestCo", lines, "2026-01-01", "2026-12-31")
        return {line["code"]: val for line, val in results}

    @patch(_PATCH_TARGET)
    def test_simple_balanced_sheet(self, mock_frappe):
        """Simple case: 2 asset accounts = 2 liability/equity accounts."""
        assets = [
            ("110", "111", 30_000_000),
            ("120", "112", 70_000_000),
        ]
        liabilities = [
            ("300", "331", 20_000_000),
            ("410", "411", 80_000_000),
        ]
        codes = self._resolve_with_balances(mock_frappe, assets, liabilities)
        self.assertEqual(codes["270"], codes["440"],
                         f"mã_270={codes['270']} ≠ mã_440={codes['440']}")
        self.assertEqual(codes["270"], Decimal("100000000"))

    @patch(_PATCH_TARGET)
    def test_larger_balanced_sheet(self, mock_frappe):
        """More accounts, still balanced."""
        assets = [
            ("110", "111", 5_000_000),
            ("111", "112", 15_000_000),
            ("130", "131", 50_000_000),
            ("150", "152", 80_000_000),
            ("220", "211", 150_000_000),
        ]
        liabilities = [
            ("310", "331", 100_000_000),
            ("320", "341", 50_000_000),
            ("400", "411", 100_000_000),
            ("430", "421", 50_000_000),
        ]
        codes = self._resolve_with_balances(mock_frappe, assets, liabilities)
        self.assertEqual(codes["270"], codes["440"],
                         f"mã_270={codes['270']} ≠ mã_440={codes['440']}")
        self.assertEqual(codes["270"], Decimal("300000000"))

    @patch(_PATCH_TARGET)
    def test_zero_balance_sheet(self, mock_frappe):
        """Zero balances — equation still holds (0 == 0)."""
        assets = [
            ("110", "111", 0),
            ("120", "112", 0),
        ]
        liabilities = [
            ("300", "331", 0),
            ("410", "411", 0),
        ]
        codes = self._resolve_with_balances(mock_frappe, assets, liabilities)
        self.assertEqual(codes["270"], codes["440"])
        self.assertEqual(codes["270"], Decimal("0"))

    @patch(_PATCH_TARGET)
    def test_equation_tolerance(self, mock_frappe):
        """Equation check passes when values differ by less than tolerance (1 VND)."""
        # This test verifies that the resolver itself computes consistently.
        # Real tolerance check (rounding differences) is handled at report level.
        assets = [("110", "111", 100_000_000)]
        liabilities = [("300", "331", 100_000_000)]
        codes = self._resolve_with_balances(mock_frappe, assets, liabilities)
        diff = abs(codes.get("270", 0) - codes.get("440", 0))
        self.assertLessEqual(diff, Decimal("1"),
                             f"Balance sheet off by {diff} — exceeds 1 VND tolerance")

    @patch(_PATCH_TARGET)
    def test_formula_line_correctly_sums_account_lines(self, mock_frappe):
        """270 = sum of all account-based asset lines (formula aggregation)."""
        assets = [
            ("A1", "111", 10_000_000),
            ("A2", "112", 20_000_000),
            ("A3", "131", 30_000_000),
        ]
        liabilities = [("L1", "411", 60_000_000)]

        codes = self._resolve_with_balances(mock_frappe, assets, liabilities)
        expected_270 = Decimal("60000000")
        self.assertEqual(codes["270"], expected_270)
        self.assertEqual(codes["270"], codes["440"])


class TestB01EquationWithResolveAllLines(unittest.TestCase):
    """Integration test using resolve_all_lines directly with a structured B01."""

    @patch(_PATCH_TARGET)
    def test_resolve_all_lines_produces_balanced_result(self, mock_frappe):
        """resolve_all_lines correctly handles two-pass resolution for formula lines."""
        from vn_accounting.financial_reporting.resolver import resolve_all_lines

        # Set up mock to return consistent values
        call_count = [0]

        def fake_sql(query, values=None, *args, **kwargs):
            call_count[0] += 1
            # Return 500M for all accounts (makes 270 = 440 easy to verify)
            return [_sql_row(debit=500_000_000, credit=500_000_000)]

        mock_frappe.db.sql.side_effect = fake_sql
        mock_frappe.utils.getdate.side_effect = lambda d: d

        lines = [
            # Asset side
            {"code": "110", "value_type": "closing_debit", "account_formula": "+111",
             "line_formula": "", "sign_multiplier": 1},
            {"code": "270", "value_type": "formula", "account_formula": "",
             "line_formula": "=110", "sign_multiplier": 1},
            # Equity/liability side
            {"code": "300", "value_type": "closing_credit", "account_formula": "+331",
             "line_formula": "", "sign_multiplier": 1},
            {"code": "440", "value_type": "formula", "account_formula": "",
             "line_formula": "=300", "sign_multiplier": 1},
        ]

        results = resolve_all_lines("TestCo", lines, "2026-01-01", "2026-12-31")
        code_map = {line["code"]: val for line, val in results}

        # 270 and 440 should both equal 500M (from mock)
        self.assertEqual(code_map["270"], code_map["440"])
        self.assertIsNotNone(code_map["270"])
        # No None values should remain
        for code, val in code_map.items():
            self.assertIsNotNone(val, f"Line {code} has None value after resolve_all_lines")


if __name__ == "__main__":
    unittest.main()
