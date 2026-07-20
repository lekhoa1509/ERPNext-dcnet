import unittest
from unittest.mock import MagicMock
from decimal import Decimal

from vn_banking.match.base import InvoiceRef, MatchCandidate
from vn_banking.match.invoice_amount import InvoiceAmountMatcher


class _FakeTxn:
    def __init__(self, amount, desc="x"):
        self.deposit = amount
        self.withdrawal = Decimal("0")
        self.description = desc
        self.reference_number = ""


def _ctx(outstanding, tolerance=Decimal("1000")):
    ctx = MagicMock()
    ctx.party_type = "Customer"
    ctx.party_invoice_type = "Sales Invoice"
    ctx.outstanding_invoices = outstanding
    ctx.tolerance = tolerance
    return ctx


class TestInvoiceAmountMatcher(unittest.TestCase):
    def test_unique_amount_match_medium(self):
        ctx = _ctx({
            "A": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500000"))],
            "B": [InvoiceRef("Sales Invoice", "SI-2", Decimal("9999999"))],
        })
        txn = _FakeTxn(Decimal("12500000"))
        cands = InvoiceAmountMatcher().match(txn, ctx)
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0].confidence, "Medium")
        self.assertEqual(cands[0].invoices[0].name, "SI-1")

    def test_ambiguous_skipped(self):
        ctx = _ctx({
            "A": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500000"))],
            "B": [InvoiceRef("Sales Invoice", "SI-2", Decimal("12500000"))],
        })
        txn = _FakeTxn(Decimal("12500000"))
        self.assertEqual(InvoiceAmountMatcher().match(txn, ctx), [])

    def test_within_tolerance_counts(self):
        ctx = _ctx({"A": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500500"))]})
        txn = _FakeTxn(Decimal("12500000"))
        cands = InvoiceAmountMatcher().match(txn, ctx)
        self.assertEqual(len(cands), 1)

    def test_zero_amount_not_applicable(self):
        ctx = _ctx({})
        txn = _FakeTxn(Decimal("0"))
        self.assertFalse(InvoiceAmountMatcher().applicable(txn, ctx))

    def test_no_invoices_returns_empty(self):
        ctx = _ctx({})
        txn = _FakeTxn(Decimal("12500000"))
        self.assertEqual(InvoiceAmountMatcher().match(txn, ctx), [])

    def test_difference_calculated(self):
        ctx = _ctx({"A": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500500"))]})
        txn = _FakeTxn(Decimal("12500000"))
        cands = InvoiceAmountMatcher().match(txn, ctx)
        self.assertEqual(cands[0].difference, Decimal("-500"))

    def test_outside_tolerance_no_match(self):
        ctx = _ctx({"A": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12502000"))]})
        txn = _FakeTxn(Decimal("12500000"))
        self.assertEqual(InvoiceAmountMatcher().match(txn, ctx), [])
