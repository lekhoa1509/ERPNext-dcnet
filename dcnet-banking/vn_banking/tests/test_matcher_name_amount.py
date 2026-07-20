from decimal import Decimal
import unittest

from vn_banking.match.base import InvoiceRef
from vn_banking.match.context import MatchContext
from vn_banking.match.name_amount import NameAmountMatcher


class _FakeTxn:
    def __init__(self, desc, amount):
        self.description = desc
        self.deposit = amount
        self.withdrawal = Decimal("0")
        self.counter_account_no = ""
        self.reference_number = ""


def _ctx(outstanding):
    ctx = MatchContext(
        bank_account="BA", company="CO", direction="credit",
        party_invoice_type="Sales Invoice", party_type="Customer",
        outstanding_invoices=outstanding, tolerance=Decimal("1000"),
    )
    return ctx


class TestNameAmountMatcher(unittest.TestCase):
    def test_fuzzy_name_in_narration(self):
        ctx = _ctx({"ABC Corp": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500000"))]})
        txn = _FakeTxn("CTY ABC CORP TT HD", Decimal("12500000"))
        cands = NameAmountMatcher().match(txn, ctx)
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0].confidence, "Low")

    def test_no_fuzzy_match(self):
        ctx = _ctx({"ABC Corp": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500000"))]})
        txn = _FakeTxn("XYZ LTD TT", Decimal("12500000"))
        self.assertEqual(NameAmountMatcher().match(txn, ctx), [])
