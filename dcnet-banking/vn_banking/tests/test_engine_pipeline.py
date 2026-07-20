import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal

from vn_banking.match.engine import get_enabled_rules_in_priority_order, pick_best
from vn_banking.match.base import MatchCandidate


class TestPickBest(unittest.TestCase):
    def test_high_beats_medium(self):
        a = MatchCandidate(party_type="Customer", party="A", confidence="Medium", difference=Decimal("0"), matched_by="invoice_amount")
        b = MatchCandidate(party_type="Customer", party="B", confidence="High", difference=Decimal("100"), matched_by="invoice_no")
        self.assertEqual(pick_best([a, b]).party, "B")

    def test_smaller_difference_wins_at_same_confidence(self):
        a = MatchCandidate(party="A", party_type="Customer", confidence="Medium", difference=Decimal("500"), matched_by="x")
        b = MatchCandidate(party="B", party_type="Customer", confidence="Medium", difference=Decimal("10"), matched_by="y")
        self.assertEqual(pick_best([a, b]).party, "B")


class TestRuleOrdering(unittest.TestCase):
    def test_priority_order(self):
        """get_enabled_rules_in_priority_order() must return only enabled rules sorted by priority asc."""
        rule_hi = MagicMock(enabled=True, priority=10)
        rule_lo = MagicMock(enabled=True, priority=20)
        rule_off = MagicMock(enabled=False, priority=5)
        mock_settings = MagicMock()
        mock_settings.rules = [rule_lo, rule_hi, rule_off]  # intentionally unsorted

        with patch("vn_banking.match.engine.frappe") as mock_frappe:
            mock_frappe.get_single.return_value = mock_settings
            rules = get_enabled_rules_in_priority_order()

        self.assertEqual(len(rules), 2, "disabled rules must be excluded")
        priorities = [int(r.priority or 9999) for r in rules]
        self.assertEqual(priorities, sorted(priorities), "rules must be ascending by priority")
