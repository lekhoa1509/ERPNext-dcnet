from decimal import Decimal

import frappe
from frappe.tests.utils import FrappeTestCase

from vn_banking.match.base import InvoiceRef
from vn_banking.match.context import MatchContext
from vn_banking.match.invoice_no import InvoiceNoMatcher


class _FakeTxn:
    def __init__(self, description, deposit=Decimal("0"), withdrawal=Decimal("0"), reference_number=""):
        self.description = description
        self.deposit = deposit
        self.withdrawal = withdrawal
        self.reference_number = reference_number


def _ctx(outstanding: dict[str, list[InvoiceRef]]):
    settings = frappe.get_single("Bank Statement Settings")
    return MatchContext(
        bank_account="TEST-BA", company="TEST-CO", direction="credit",
        party_invoice_type="Sales Invoice", party_type="Customer",
        outstanding_invoices=outstanding, tolerance=Decimal("1000"),
        settings=settings,
    )


class TestInvoiceNoMatcher(FrappeTestCase):
    def test_single_invoice_exact_amount_high(self):
        ctx = _ctx({"ABC Corp": [InvoiceRef("Sales Invoice", "ACC-SI-2026-0123", Decimal("12500000"))]})
        # Need to inject party→invoice reverse map; matcher iterates party-keyed map
        txn = _FakeTxn(description="TT HD ACC-SI-2026-0123", deposit=Decimal("12500000"))
        m = InvoiceNoMatcher()
        cands = m.match(txn, ctx)
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0].confidence, "High")
        self.assertEqual(cands[0].invoices[0].name, "ACC-SI-2026-0123")

    def test_amount_mismatch_drops_to_low(self):
        ctx = _ctx({"ABC Corp": [InvoiceRef("Sales Invoice", "SI-001", Decimal("10000000"))]})
        txn = _FakeTxn(description="TT HD SI-001", deposit=Decimal("5000000"))
        cands = InvoiceNoMatcher().match(txn, ctx)
        self.assertEqual(cands[0].confidence, "Low")

    def test_within_tolerance_medium(self):
        ctx = _ctx({"ABC Corp": [InvoiceRef("Sales Invoice", "SI-001", Decimal("10000000"))]})
        txn = _FakeTxn(description="TT SI-001 phi 500", deposit=Decimal("9999500"))
        cands = InvoiceNoMatcher().match(txn, ctx)
        self.assertEqual(cands[0].confidence, "Medium")

    def test_no_invoice_no_in_narration(self):
        ctx = _ctx({"ABC Corp": [InvoiceRef("Sales Invoice", "SI-001", Decimal("10000000"))]})
        txn = _FakeTxn(description="random text", deposit=Decimal("10000000"))
        self.assertEqual(InvoiceNoMatcher().match(txn, ctx), [])
