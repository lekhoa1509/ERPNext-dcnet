"""Static tests for Term Deposit Summary + Bank Loan Summary reports
(FB-2026-00612, FB-2026-00613).

Pure JSON / source assertions — no Frappe DB required. Run via:
    cd apps/vn_accounting && python3 -m unittest tests.test_treasury_summary_reports -v
"""
from __future__ import annotations

import json
import os
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
APP_INNER = os.path.normpath(os.path.join(HERE, "..", "vn_accounting"))


def _report_dir(name: str) -> str:
    return os.path.join(APP_INNER, "vn_accounting", "report", name)


class TestTermDepositSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = _report_dir("term_deposit_summary")
        with open(os.path.join(cls.dir, "term_deposit_summary.json"), encoding="utf-8") as f:
            cls.cfg = json.load(f)
        with open(os.path.join(cls.dir, "term_deposit_summary.py"), encoding="utf-8") as f:
            cls.py = f.read()
        with open(os.path.join(cls.dir, "term_deposit_summary.js"), encoding="utf-8") as f:
            cls.js = f.read()

    def test_report_registered_for_term_deposit(self):
        self.assertEqual(self.cfg["doctype"], "Report")
        self.assertEqual(self.cfg["ref_doctype"], "Term Deposit")
        self.assertEqual(self.cfg["report_type"], "Script Report")
        self.assertEqual(self.cfg["module"], "VN Accounting")
        self.assertEqual(self.cfg["is_standard"], "Yes")

    def test_report_grants_role_required_for_query_report_run(self):
        # Per claude/rules/frappe-doctype-perms.md: role must have read=1 AND
        # report=1 on the ref_doctype too. Here we just verify the report
        # itself names the expected accounting roles.
        roles = {r["role"] for r in self.cfg.get("roles", [])}
        self.assertIn("Accounts User", roles)
        self.assertIn("Accounts Manager", roles)

    def test_python_has_execute_and_3_view_modes(self):
        self.assertIn("def execute(filters", self.py)
        self.assertIn("Đang gửi tại ngày", self.py)
        self.assertIn("Phát sinh trong kỳ", self.py)
        self.assertIn("Đáo hạn trong kỳ", self.py)

    def test_python_returns_booked_unbooked_interest(self):
        # Two computed columns Long requested ("phát sinh lãi")
        self.assertIn("booked_interest", self.py)
        self.assertIn("unbooked_interest", self.py)
        self.assertIn("days_to_maturity", self.py)

    def test_python_uses_term_deposit_interest_child_table(self):
        # The child table providing the "Lãi đã hạch toán" data
        self.assertIn("tabTerm Deposit Interest", self.py)

    def test_js_has_view_mode_filter_with_default(self):
        self.assertIn('frappe.query_reports["Term Deposit Summary"]', self.js)
        self.assertIn("view_mode", self.js)
        self.assertIn('default: "Đang gửi tại ngày"', self.js)


class TestBankLoanSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = _report_dir("bank_loan_summary")
        with open(os.path.join(cls.dir, "bank_loan_summary.json"), encoding="utf-8") as f:
            cls.cfg = json.load(f)
        with open(os.path.join(cls.dir, "bank_loan_summary.py"), encoding="utf-8") as f:
            cls.py = f.read()
        with open(os.path.join(cls.dir, "bank_loan_summary.js"), encoding="utf-8") as f:
            cls.js = f.read()

    def test_report_registered_for_bank_loan(self):
        self.assertEqual(self.cfg["ref_doctype"], "Bank Loan")
        self.assertEqual(self.cfg["report_type"], "Script Report")
        self.assertEqual(self.cfg["module"], "VN Accounting")

    def test_python_has_3_view_modes(self):
        self.assertIn("Lịch trả nợ trong kỳ", self.py)
        self.assertIn("Đang vay (toàn cảnh)", self.py)
        self.assertIn("Đáo hạn trong kỳ", self.py)

    def test_python_joins_bank_loan_repayment_for_default_mode(self):
        # The repayment mode JOINs parent Bank Loan with child Bank Loan Repayment
        self.assertIn("tabBank Loan Repayment", self.py)
        self.assertIn("tabBank Loan", self.py)
        self.assertIn("INNER JOIN", self.py)

    def test_python_emits_two_column_sets(self):
        # Mode-dependent columns: repayment-row vs loan-row
        self.assertIn("_get_columns_repayment", self.py)
        self.assertIn("_get_columns_loan", self.py)

    def test_python_computes_overdue_days(self):
        self.assertIn("days_to_due", self.py)
        self.assertIn("days_to_maturity", self.py)

    def test_python_computes_periods_progress(self):
        # "Đã trả / Tổng kỳ" column
        self.assertIn("periods_progress", self.py)
        self.assertIn("_periods_progress", self.py)

    def test_js_has_view_mode_default_to_repayment_schedule(self):
        self.assertIn('default: "Lịch trả nợ trong kỳ"', self.js)
        # on_change must refresh because columns are mode-dependent
        self.assertIn("on_change", self.js)

    def test_js_has_overdue_indicator(self):
        self.assertIn("days_to_due", self.js)
        self.assertIn("Quá hạn", self.js)


class TestSidebarItemsRegistered(unittest.TestCase):
    """Verify both reports are linked from Section 'Ngân hàng' in workspace sidebar."""

    @classmethod
    def setUpClass(cls):
        path = os.path.join(APP_INNER, "workspace_sidebar", "vn_accounting.json")
        with open(path, encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.items = cls.data["items"]
        section_start = next(
            i for i, it in enumerate(cls.items)
            if it.get("type") == "Section Break" and it.get("label") == "Ngân hàng"
        )
        section_end = next(
            (
                i for i, it in enumerate(cls.items[section_start + 1:], section_start + 1)
                if it.get("type") == "Section Break"
            ),
            len(cls.items),
        )
        cls.section_items = cls.items[section_start + 1:section_end]

    def test_term_deposit_summary_in_ngan_hang(self):
        td_summary = next(
            (it for it in self.section_items if it.get("link_to") == "Term Deposit Summary"),
            None,
        )
        self.assertIsNotNone(td_summary, "Term Deposit Summary missing from Ngân hàng section")
        self.assertEqual(td_summary["link_type"], "Report")
        self.assertEqual(td_summary["type"], "Link")

    def test_bank_loan_summary_in_ngan_hang(self):
        bl_summary = next(
            (it for it in self.section_items if it.get("link_to") == "Bank Loan Summary"),
            None,
        )
        self.assertIsNotNone(bl_summary, "Bank Loan Summary missing from Ngân hàng section")
        self.assertEqual(bl_summary["link_type"], "Report")

    def test_term_deposit_summary_placed_after_term_deposit_list(self):
        # Sidebar order: ... → Term Deposit (DocType) → Term Deposit Summary (Report) → ...
        td_list_idx = next(
            (i for i, it in enumerate(self.section_items) if it.get("link_to") == "Term Deposit"
             and it.get("link_type") == "DocType"),
            None,
        )
        td_summary_idx = next(
            (i for i, it in enumerate(self.section_items) if it.get("link_to") == "Term Deposit Summary"),
            None,
        )
        self.assertIsNotNone(td_list_idx)
        self.assertIsNotNone(td_summary_idx)
        self.assertEqual(td_summary_idx, td_list_idx + 1, "Summary must immediately follow list item")


class TestHelpRegistered(unittest.TestCase):
    def test_help_articles_exist(self):
        for slug in ("term-deposit-summary.md", "bank-loan-summary.md"):
            path = os.path.join(APP_INNER, "help", "ngan-hang", slug)
            self.assertTrue(os.path.isfile(path), f"missing help article: {slug}")

    def test_hooks_register_report_help_mapping(self):
        with open(os.path.join(APP_INNER, "hooks.py"), encoding="utf-8") as f:
            hooks = f.read()
        self.assertIn('"Term Deposit Summary"', hooks)
        self.assertIn('"Bank Loan Summary"', hooks)
        self.assertIn('"help/ngan-hang"', hooks)


if __name__ == "__main__":
    unittest.main()
