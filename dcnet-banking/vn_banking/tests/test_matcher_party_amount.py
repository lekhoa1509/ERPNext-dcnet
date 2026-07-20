from decimal import Decimal
from frappe.tests.utils import FrappeTestCase

from vn_banking.match.base import InvoiceRef
from vn_banking.match.context import MatchContext
from vn_banking.match.party_amount import PartyAmountMatcher


class _FakeTxn:
    def __init__(self, amount, counter):
        self.deposit = amount
        self.withdrawal = Decimal("0")
        self.counter_account_no = counter
        self.description = ""
        self.reference_number = ""


class _FakeSettings:
    enable_multi_invoice_match = True
    multi_invoice_max_combinations = 5
    tolerance_fixed_amount = 1000
    amount_date_tolerance_days = 3


def _ctx(outstanding, party_map):
    return MatchContext(
        bank_account="BA", company="CO", direction="credit",
        party_invoice_type="Sales Invoice", party_type="Customer",
        outstanding_invoices=outstanding, party_by_bank_account=party_map,
        tolerance=Decimal("1000"), settings=_FakeSettings(),
    )


class TestPartyAmountMatcher(FrappeTestCase):
    def test_single_invoice_by_counter_account(self):
        ctx = _ctx(
            {"ABC Corp": [InvoiceRef("Sales Invoice", "SI-1", Decimal("12500000"))]},
            {"1234567890": "ABC Corp"},
        )
        txn = _FakeTxn(Decimal("12500000"), "1234567890")
        cands = PartyAmountMatcher().match(txn, ctx)
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0].party, "ABC Corp")

    def test_multi_invoice_combo(self):
        ctx = _ctx(
            {"ABC Corp": [
                InvoiceRef("Sales Invoice", "SI-1", Decimal("10000000")),
                InvoiceRef("Sales Invoice", "SI-2", Decimal("2500000")),
                InvoiceRef("Sales Invoice", "SI-3", Decimal("5000000")),
            ]},
            {"1234567890": "ABC Corp"},
        )
        txn = _FakeTxn(Decimal("12500000"), "1234567890")
        cands = PartyAmountMatcher().match(txn, ctx)
        self.assertEqual(len(cands), 1)
        names = {i.name for i in cands[0].invoices}
        self.assertEqual(names, {"SI-1", "SI-2"})

    def test_unknown_counter_skipped(self):
        ctx = _ctx({"A": [InvoiceRef("Sales Invoice", "SI-1", Decimal("100"))]}, {})
        txn = _FakeTxn(Decimal("100"), "9999")
        self.assertFalse(PartyAmountMatcher().applicable(txn, ctx))
