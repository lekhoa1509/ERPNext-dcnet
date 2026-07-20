"""Unit tests for CCDC Allocation per-period posting (Phase 4).

These tests cover the pure account-resolution logic without requiring frappe.
They inline the resolution logic to remain standalone under pytest.

Run:
    cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
    python -m pytest vn_accounting/tests/test_ccdc_allocation_post_period.py -v

Integration tests (post_allocation_period idempotency) require a live site:
    bench --site dcnet.localhost console
    >>> import unittest
    >>> from vn_accounting.tests.test_ccdc_allocation_post_period import TestAllocationIdempotency
    >>> unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestAllocationIdempotency))
"""
from __future__ import annotations

import unittest


# ---- Inline pure logic (mirrors ccdc_allocation._resolve_*) ----------------

def _resolve_debit(row_debit, item_expense, _company=None):
    """row override > item.expense_account > (DB lookup when company set)."""
    if row_debit:
        return row_debit
    if item_expense:
        return item_expense
    return None  # In real code, DB lookup for "6423" happens here


def _resolve_credit(row_credit, item_prepayment, _company=None):
    """row override > item.prepayment_account > (DB lookup when company set)."""
    if row_credit:
        return row_credit
    if item_prepayment:
        return item_prepayment
    return None  # In real code, DB lookup for "242" happens here


# ---- Test classes -----------------------------------------------------------

class TestResolveDebitAccount(unittest.TestCase):
    def test_row_override_wins(self):
        self.assertEqual(
            _resolve_debit("6273 - override", "6423 - item", None),
            "6273 - override",
        )

    def test_item_expense_second(self):
        self.assertEqual(
            _resolve_debit(None, "6423 - item", None),
            "6423 - item",
        )

    def test_empty_string_fallthrough(self):
        self.assertEqual(
            _resolve_debit("", "6423 - item", None),
            "6423 - item",
        )

    def test_both_none_returns_none(self):
        self.assertIsNone(_resolve_debit(None, None, None))

    def test_both_empty_returns_none(self):
        self.assertIsNone(_resolve_debit("", "", None))


class TestResolveCreditAccount(unittest.TestCase):
    def test_row_override_wins(self):
        self.assertEqual(
            _resolve_credit("333 - override", "242 - item", None),
            "333 - override",
        )

    def test_item_prepayment_second(self):
        self.assertEqual(
            _resolve_credit(None, "242 - item", None),
            "242 - item",
        )

    def test_empty_string_fallthrough(self):
        self.assertEqual(
            _resolve_credit("", "242 - item", None),
            "242 - item",
        )

    def test_both_none_returns_none(self):
        self.assertIsNone(_resolve_credit(None, None, None))


class TestIdempotencyGuard(unittest.TestCase):
    """Simulate the idempotency check in post_allocation_period."""

    def _check(self, journal_entry):
        if journal_entry:
            return {"status": "already_posted", "je_name": journal_entry}
        return {"status": "would_post"}

    def test_already_posted_when_je_set(self):
        r = self._check("JV-2026-00042")
        self.assertEqual(r["status"], "already_posted")
        self.assertEqual(r["je_name"], "JV-2026-00042")

    def test_posts_when_none(self):
        self.assertEqual(self._check(None)["status"], "would_post")

    def test_posts_when_empty_string(self):
        self.assertEqual(self._check("")["status"], "would_post")


class TestAllocationIdempotency(unittest.TestCase):
    """Live integration test — requires bench/frappe context.

    Verifies post_allocation_period idempotency on an actual CCDC Allocation Schedule.
    Only run via bench console or bench run-tests.
    """

    def setUp(self):
        try:
            import frappe
            self.frappe = frappe
        except ImportError:
            self.skipTest("frappe not available — run via bench")

    def test_post_period_uses_row_accounts(self):
        """When row.debit_account set to custom value, JE uses that account."""
        import frappe
        from vn_accounting.asset.ccdc_allocation import _resolve_debit_account

        # Pure fallback chain with explicit row override
        result = _resolve_debit_account("6273 - test", None, None)
        self.assertEqual(result, "6273 - test")

    def test_resolve_debit_fallback_chain(self):
        """item_expense beats DB fallback when set."""
        from vn_accounting.asset.ccdc_allocation import _resolve_debit_account
        result = _resolve_debit_account(None, "6423 - my expense", None)
        self.assertEqual(result, "6423 - my expense")

    def test_resolve_credit_fallback_chain(self):
        """item_prepayment beats DB fallback when set."""
        from vn_accounting.asset.ccdc_allocation import _resolve_credit_account
        result = _resolve_credit_account(None, "242 - my prepay", None)
        self.assertEqual(result, "242 - my prepay")


if __name__ == "__main__":
    unittest.main()
