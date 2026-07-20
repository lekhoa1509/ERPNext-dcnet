"""Unit tests for BCTC resolver engine (no Frappe DB needed)."""
import sys
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

# Inject a stub frappe ONLY when running standalone (frappe not yet imported).
# This allows the resolver module to be imported without a Frappe app context.
# When combined with P3 tests (which use @patch decorators on their own modules),
# frappe is already in sys.modules as the real module — we leave it untouched.
_frappe_injected = "frappe" not in sys.modules
if _frappe_injected:
    sys.modules["frappe"] = MagicMock()
    sys.modules["frappe.utils"] = MagicMock()

# Import the module-under-test after stub is in place
import vn_accounting.financial_reporting.resolver as _resolver_mod  # noqa: E402

_PATCH_TARGET = "vn_accounting.financial_reporting.resolver.frappe"


def tearDownModule():
    """Clean up injected frappe stub after this test file finishes."""
    if _frappe_injected:
        sys.modules.pop("frappe", None)
        sys.modules.pop("frappe.utils", None)
        sys.modules.pop("vn_accounting.financial_reporting.resolver", None)


class TestParseAccountFormula(unittest.TestCase):

    def setUp(self):
        from vn_accounting.financial_reporting.resolver import _parse_account_formula
        self.parse = _parse_account_formula

    def test_empty_formula_returns_empty(self):
        self.assertEqual(self.parse(""), [])
        self.assertEqual(self.parse(None), [])

    def test_single_account_no_sign(self):
        result = self.parse("111")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (Decimal(1), "111"))

    def test_plus_sign_explicit(self):
        result = self.parse("+112")
        self.assertEqual(result[0], (Decimal(1), "112"))

    def test_minus_sign(self):
        result = self.parse("-131")
        self.assertEqual(result[0], (Decimal(-1), "131"))

    def test_multiple_accounts(self):
        result = self.parse("+111,+112,-131")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (Decimal(1), "111"))
        self.assertEqual(result[1], (Decimal(1), "112"))
        self.assertEqual(result[2], (Decimal(-1), "131"))

    def test_wildcard_suffix(self):
        result = self.parse("+511%")
        self.assertEqual(result[0], (Decimal(1), "511%"))

    def test_spaces_stripped(self):
        result = self.parse(" +111 , -131 ")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "111")
        self.assertEqual(result[1][1], "131")

    def test_mixed_wildcard_and_exact(self):
        result = self.parse("+511%,+512,+515,-521")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0][1], "511%")
        self.assertEqual(result[3][0], Decimal(-1))


def _mock_sql_row(debit=0, credit=0):
    row = MagicMock()
    row.total_debit = debit
    row.total_credit = credit
    return row


class TestResolveBctcLine(unittest.TestCase):

    def _make_line(self, code="110", value_type="closing_debit",
                   account_formula="+111", line_formula="", sign_multiplier=1):
        return {
            "code": code,
            "value_type": value_type,
            "account_formula": account_formula,
            "line_formula": line_formula,
            "sign_multiplier": sign_multiplier,
        }

    @patch(_PATCH_TARGET)
    def test_closing_debit_basic(self, mock_frappe):
        """closing_debit returns max(debit - credit, 0)."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=1000, credit=200)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(value_type="closing_debit", account_formula="+111")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("800"))

    @patch(_PATCH_TARGET)
    def test_closing_credit_basic(self, mock_frappe):
        """closing_credit returns max(credit - debit, 0)."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=200, credit=1000)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(value_type="closing_credit", account_formula="+331")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("800"))

    @patch(_PATCH_TARGET)
    def test_closing_debit_floors_at_zero(self, mock_frappe):
        """closing_debit never goes negative (credit > debit)."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=100, credit=500)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(value_type="closing_debit", account_formula="+111")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("0"))

    @patch(_PATCH_TARGET)
    def test_period_debit(self, mock_frappe):
        """period_debit returns total debit movement (no net)."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=5000, credit=1000)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(value_type="period_debit", account_formula="+621")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("5000"))

    @patch(_PATCH_TARGET)
    def test_period_credit(self, mock_frappe):
        """period_credit returns total credit movement (no net)."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=200, credit=8000)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(value_type="period_credit", account_formula="+511")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("8000"))

    @patch(_PATCH_TARGET)
    def test_empty_account_formula_returns_zero(self, mock_frappe):
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(account_formula="")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("0"))

    @patch(_PATCH_TARGET)
    def test_formula_type_uses_resolved_cache(self, mock_frappe):
        """value_type='formula' reads from resolved_cache."""
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        cache = {"10": Decimal("1000"), "11": Decimal("300"), "12": Decimal("200")}
        line = self._make_line(value_type="formula", line_formula="=10+11-12")
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31", cache)
        self.assertEqual(result, Decimal("1100"))

    @patch(_PATCH_TARGET)
    def test_result_stored_in_cache(self, mock_frappe):
        """After resolve, line code is stored in resolved_cache."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=500, credit=0)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        cache = {}
        line = self._make_line(code="110", value_type="closing_debit", account_formula="+111")
        resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31", cache)
        self.assertIn("110", cache)
        self.assertEqual(cache["110"], Decimal("500"))

    @patch(_PATCH_TARGET)
    def test_sign_multiplier_applied(self, mock_frappe):
        """sign_multiplier=-1 negates the result."""
        mock_frappe.db.sql.return_value = [_mock_sql_row(debit=1000, credit=0)]
        from vn_accounting.financial_reporting.resolver import resolve_bctc_line
        line = self._make_line(value_type="closing_debit", account_formula="+111",
                               sign_multiplier=-1)
        result = resolve_bctc_line("TestCo", line, "2026-01-01", "2026-03-31")
        self.assertEqual(result, Decimal("-1000"))


class TestResolveLineFormula(unittest.TestCase):

    def _make_formula_line(self, formula):
        return {
            "code": "270",
            "value_type": "formula",
            "account_formula": "",
            "line_formula": formula,
            "sign_multiplier": 1,
        }

    @patch(_PATCH_TARGET)
    def test_simple_addition(self, mock_frappe):
        from vn_accounting.financial_reporting.resolver import _resolve_line_formula
        cache = {"10": Decimal("500"), "20": Decimal("300")}
        result = _resolve_line_formula("Co", self._make_formula_line("=10+20"),
                                       "2026-01-01", "2026-03-31", cache)
        self.assertEqual(result, Decimal("800"))

    @patch(_PATCH_TARGET)
    def test_simple_subtraction(self, mock_frappe):
        from vn_accounting.financial_reporting.resolver import _resolve_line_formula
        cache = {"100": Decimal("1000"), "50": Decimal("400")}
        result = _resolve_line_formula("Co", self._make_formula_line("=100-50"),
                                       "2026-01-01", "2026-03-31", cache)
        self.assertEqual(result, Decimal("600"))

    @patch(_PATCH_TARGET)
    def test_multi_term_formula(self, mock_frappe):
        from vn_accounting.financial_reporting.resolver import _resolve_line_formula
        cache = {"10": Decimal("100"), "11": Decimal("200"), "12": Decimal("50")}
        result = _resolve_line_formula("Co", self._make_formula_line("=10+11-12"),
                                       "2026-01-01", "2026-03-31", cache)
        self.assertEqual(result, Decimal("250"))

    @patch(_PATCH_TARGET)
    def test_missing_prefix_returns_zero(self, mock_frappe):
        """Formula without '=' prefix returns 0."""
        from vn_accounting.financial_reporting.resolver import _resolve_line_formula
        cache = {"10": Decimal("500")}
        result = _resolve_line_formula("Co", self._make_formula_line("10+11"),
                                       "2026-01-01", "2026-03-31", cache)
        self.assertEqual(result, Decimal("0"))

    @patch(_PATCH_TARGET)
    def test_unknown_code_skipped(self, mock_frappe):
        """Unknown code not in cache is skipped (treated as 0)."""
        from vn_accounting.financial_reporting.resolver import _resolve_line_formula
        cache = {"10": Decimal("100")}
        result = _resolve_line_formula("Co", self._make_formula_line("=10+99"),
                                       "2026-01-01", "2026-03-31", cache)
        self.assertEqual(result, Decimal("100"))


class TestResolveAllLines(unittest.TestCase):

    @patch(_PATCH_TARGET)
    def test_two_pass_order(self, mock_frappe):
        """Formula lines resolve after account-based lines."""
        row = MagicMock()
        row.total_debit = 500
        row.total_credit = 0
        mock_frappe.db.sql.return_value = [row]

        from vn_accounting.financial_reporting.resolver import resolve_all_lines

        lines = [
            {"code": "110", "value_type": "closing_debit",
             "account_formula": "+111", "line_formula": "", "sign_multiplier": 1},
            {"code": "270", "value_type": "formula",
             "account_formula": "", "line_formula": "=110+120", "sign_multiplier": 1},
            {"code": "120", "value_type": "closing_debit",
             "account_formula": "+112", "line_formula": "", "sign_multiplier": 1},
        ]

        results = resolve_all_lines("TestCo", lines, "2026-01-01", "2026-03-31")
        self.assertEqual(len(results), 3)

        code_map = {line["code"]: val for line, val in results}
        self.assertEqual(code_map["110"], Decimal("500"))
        self.assertEqual(code_map["120"], Decimal("500"))
        self.assertEqual(code_map["270"], Decimal("1000"))

    @patch(_PATCH_TARGET)
    def test_placeholders_filled_in_pass2(self, mock_frappe):
        """Formula lines which were None placeholders get values in pass 2."""
        row = MagicMock()
        row.total_debit = 200
        row.total_credit = 0
        mock_frappe.db.sql.return_value = [row]

        from vn_accounting.financial_reporting.resolver import resolve_all_lines

        lines = [
            {"code": "F1", "value_type": "formula",
             "account_formula": "", "line_formula": "=A1", "sign_multiplier": 1},
            {"code": "A1", "value_type": "closing_debit",
             "account_formula": "+111", "line_formula": "", "sign_multiplier": 1},
        ]
        results = resolve_all_lines("TestCo", lines, "2026-01-01", "2026-03-31")
        code_map = {line["code"]: val for line, val in results}
        self.assertEqual(code_map["F1"], Decimal("200"))

    @patch(_PATCH_TARGET)
    def test_all_none_values_replaced(self, mock_frappe):
        """No None values remain in the output."""
        row = MagicMock()
        row.total_debit = 100
        row.total_credit = 0
        mock_frappe.db.sql.return_value = [row]

        from vn_accounting.financial_reporting.resolver import resolve_all_lines
        lines = [
            {"code": "X", "value_type": "formula", "account_formula": "",
             "line_formula": "=Y", "sign_multiplier": 1},
            {"code": "Y", "value_type": "closing_debit", "account_formula": "+111",
             "line_formula": "", "sign_multiplier": 1},
        ]
        results = resolve_all_lines("TestCo", lines, "2026-01-01", "2026-03-31")
        for line, val in results:
            self.assertIsNotNone(val)


if __name__ == "__main__":
    unittest.main()
