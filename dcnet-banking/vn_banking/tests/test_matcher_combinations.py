from decimal import Decimal
from frappe.tests.utils import FrappeTestCase

from vn_banking.match.combinations import combinations_sum_match
from vn_banking.match.base import InvoiceRef


def _mk(*amounts):
    return [InvoiceRef("Sales Invoice", f"SI-{i}", Decimal(str(a))) for i, a in enumerate(amounts)]


class TestCombinations(FrappeTestCase):
    def test_single_invoice_exact(self):
        invs = _mk(100, 200, 300)
        combo = combinations_sum_match(invs, Decimal("200"), Decimal("0"), max_k=3)
        self.assertEqual(len(combo), 1)
        self.assertEqual(combo[0].name, "SI-1")

    def test_two_invoice_combo(self):
        invs = _mk(100, 200, 300)
        combo = combinations_sum_match(invs, Decimal("500"), Decimal("0"), max_k=3)
        self.assertEqual(sum(i.outstanding for i in combo), Decimal("500"))
        self.assertEqual(len(combo), 2)

    def test_prefers_smaller_k(self):
        invs = _mk(100, 200, 300, 500)
        combo = combinations_sum_match(invs, Decimal("500"), Decimal("0"), max_k=3)
        self.assertEqual(len(combo), 1)
        self.assertEqual(combo[0].outstanding, Decimal("500"))

    def test_within_tolerance(self):
        invs = _mk(100, 201)
        combo = combinations_sum_match(invs, Decimal("300"), Decimal("2"), max_k=2)
        self.assertEqual(len(combo), 2)

    def test_no_combo(self):
        invs = _mk(100, 200)
        self.assertEqual(combinations_sum_match(invs, Decimal("999"), Decimal("0"), max_k=2), [])
