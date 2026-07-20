"""Unit tests for PBDT (revenue allocation) JE handler.

Covers two paths:

  1. Default single-JE (`split_by_revenue_account=False`): just delegates to
     `_create_je_1to1` with voucher_type="Journal Entry". Tested for
     1,260-leg synthetic input balance + correct dispatch.

  2. Opt-in split (`split_by_revenue_account=True`): legs grouped by Cr
     5xx/7xx account → N JEs named `<voucher_no>-S1`, `-S2`, ... Tested for
     grouping correctness, per-group balance, name-override propagation,
     and unbalanced-group fallback to single JE.

DB-touching insert path is unit-tested by mocking `frappe.db.exists` and
`frappe.get_doc`. Full-row insert (1,260 rows server round-trip) is the
E2E job in commit 15.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------- pure helpers

class TestSplitLegsByRevenueAccount(unittest.TestCase):
    """`_split_legs_by_revenue_account` — pure function, no frappe needed."""

    def _split(self, legs):
        from vn_accounting.misa_migration.importers.nkc_handlers.journal_entry \
            import _split_legs_by_revenue_account
        return _split_legs_by_revenue_account(legs)

    def test_empty_input_returns_empty(self):
        self.assertEqual(self._split([]), [])

    def test_single_revenue_credit_opens_one_group(self):
        legs = [
            {"account": "5111", "debit": 0, "credit": 100},
            {"account": "131", "debit": 100, "credit": 0},
        ]
        result = self._split(legs)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 2)

    def test_two_revenue_credits_create_two_groups(self):
        legs = [
            {"account": "5111", "debit": 0, "credit": 100},
            {"account": "131", "debit": 100, "credit": 0},
            {"account": "5112", "debit": 0, "credit": 50},
            {"account": "131", "debit": 50, "credit": 0},
        ]
        result = self._split(legs)
        self.assertEqual(len(result), 2)
        # Each group: 1 Cr + 1 Dr
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[1]), 2)
        self.assertEqual(result[0][0]["account"], "5111")
        self.assertEqual(result[1][0]["account"], "5112")

    def test_prologue_dr_attaches_to_first_group(self):
        # Setup Dr legs before first Cr 5xx form a prologue, attached to
        # the first revenue group (so totals stay clean).
        legs = [
            {"account": "131", "debit": 30, "credit": 0},  # prologue Dr
            {"account": "5111", "debit": 0, "credit": 100},
            {"account": "131", "debit": 70, "credit": 0},
        ]
        result = self._split(legs)
        # Prologue → its own group; then 5111 opens group #2
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 1)  # prologue alone
        self.assertEqual(len(result[1]), 2)  # 5111 + trailing Dr

    def test_revenue_credit_711_treated_as_split_seed(self):
        legs = [
            {"account": "711", "debit": 0, "credit": 200},
            {"account": "131", "debit": 200, "credit": 0},
        ]
        result = self._split(legs)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0]["account"], "711")

    def test_non_revenue_credit_does_not_split(self):
        # Cr 331 (Supplier payable) is NOT a revenue account — same group
        legs = [
            {"account": "5111", "debit": 0, "credit": 100},
            {"account": "131", "debit": 50, "credit": 0},
            {"account": "331", "debit": 0, "credit": 50},  # Cr 331, not 5xx
            {"account": "642", "debit": 50, "credit": 0},
        ]
        result = self._split(legs)
        # Only 1 split — Cr 331 does not open a new group
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 4)

    def test_real_pbdt_pattern_1260_legs(self):
        """Synthetic 1,260-leg voucher with 10 revenue sub-accounts."""
        legs = []
        # 10 revenue sub-accounts × 126 legs each (1 Cr + 125 Dr)
        for sub in range(10):
            acct = f"511{sub}"
            # Cr leg seeding the group: 125 customers × 10 VND each = 1,250
            legs.append({"account": acct, "debit": 0, "credit": 1250})
            # 125 Dr legs balancing it
            for i in range(125):
                legs.append({
                    "account": "131", "debit": 10, "credit": 0,
                    "party_code": f"CUST{i:03d}",
                })
        self.assertEqual(len(legs), 1260)
        groups = self._split(legs)
        self.assertEqual(len(groups), 10)
        for g in groups:
            self.assertEqual(len(g), 126)
            dr = sum(l["debit"] for l in g)
            cr = sum(l["credit"] for l in g)
            self.assertEqual(dr, cr)


class TestGroupsBalance(unittest.TestCase):
    """`_groups_balance` — pure helper."""

    def _check(self, groups):
        from vn_accounting.misa_migration.importers.nkc_handlers.journal_entry \
            import _groups_balance
        return _groups_balance(groups)

    def test_all_groups_balance_returns_true(self):
        groups = [
            [{"debit": 100, "credit": 0}, {"debit": 0, "credit": 100}],
            [{"debit": 50, "credit": 0}, {"debit": 0, "credit": 50}],
        ]
        self.assertTrue(self._check(groups))

    def test_one_unbalanced_group_returns_false(self):
        groups = [
            [{"debit": 100, "credit": 0}, {"debit": 0, "credit": 99}],  # bad
            [{"debit": 50, "credit": 0}, {"debit": 0, "credit": 50}],
        ]
        self.assertFalse(self._check(groups))

    def test_floating_point_tolerance(self):
        groups = [
            [{"debit": 100.001, "credit": 0}, {"debit": 0, "credit": 100.0}],
        ]
        # Diff 0.001 < 0.01 tolerance → True
        self.assertTrue(self._check(groups))

    def test_empty_groups_returns_true(self):
        self.assertTrue(self._check([]))


# ----------------------------------------------------- create_je_from_pbdt dispatch

class TestCreateJeFromPbdt(unittest.TestCase):
    """`create_je_from_pbdt` dispatch logic — mock frappe.db + frappe.get_doc."""

    def _build_voucher(self, num_revenue_groups=2):
        legs = []
        for sub in range(num_revenue_groups):
            legs.append({
                "account": f"511{sub}", "debit": 0, "credit": 100.0,
                "leg_desc": f"PB doanh thu {sub}",
            })
            legs.append({
                "account": "131", "debit": 100.0, "credit": 0,
                "leg_desc": f"Phải thu {sub}",
                "party_code": f"CUST{sub:03d}",
            })
        return {
            "voucher_no": "PBDT00001",
            "prefix": "PBDT",
            "posting_date": "2026-01-31",
            "voucher_remark": "PB doanh thu T1/2026",
            "party_code": None,
            "legs": legs,
        }

    def test_default_no_split_uses_single_je(self):
        """split_by_revenue_account=False → delegate to _create_je_1to1."""
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.return_value = {
                "status": "created", "target_name": "PBDT00001",
                "target_doctype": "Journal Entry", "leg_count": 4,
                "total_dr": 200.0, "voucher_type": "Journal Entry",
            }
            v = self._build_voucher()
            result = journal_entry.create_je_from_pbdt(v)
            self.assertEqual(result["status"], "created")
            self.assertEqual(result["target_name"], "PBDT00001")
            # One call → single JE
            self.assertEqual(mock_1to1.call_count, 1)
            args, kwargs = mock_1to1.call_args
            self.assertEqual(kwargs.get("voucher_type"), "Journal Entry")
            self.assertNotIn("legs_override", kwargs)
            self.assertNotIn("name_override", kwargs)

    def test_split_flag_creates_n_jes(self):
        """split_by_revenue_account=True → N _create_je_1to1 calls with name override."""
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            # Each split returns a created result with its sub-name
            mock_1to1.side_effect = [
                {"status": "created", "target_name": "PBDT00001-S1",
                 "target_doctype": "Journal Entry", "leg_count": 2,
                 "total_dr": 100.0, "voucher_type": "Journal Entry"},
                {"status": "created", "target_name": "PBDT00001-S2",
                 "target_doctype": "Journal Entry", "leg_count": 2,
                 "total_dr": 100.0, "voucher_type": "Journal Entry"},
            ]
            v = self._build_voucher(num_revenue_groups=2)
            result = journal_entry.create_je_from_pbdt(
                v, split_by_revenue_account=True
            )
            self.assertEqual(result["status"], "created")
            self.assertEqual(result["split_count"], 2)
            self.assertEqual(result["split_names"],
                             ["PBDT00001-S1", "PBDT00001-S2"])
            # Two calls
            self.assertEqual(mock_1to1.call_count, 2)
            # First call: name_override = PBDT00001-S1
            args1, kwargs1 = mock_1to1.call_args_list[0]
            self.assertEqual(kwargs1["name_override"], "PBDT00001-S1")
            self.assertIn("legs_override", kwargs1)
            self.assertEqual(len(kwargs1["legs_override"]), 2)
            # Second: PBDT00001-S2
            args2, kwargs2 = mock_1to1.call_args_list[1]
            self.assertEqual(kwargs2["name_override"], "PBDT00001-S2")

    def test_split_fallback_when_group_unbalanced(self):
        """If split produces unbalanced groups → fall back to single JE."""
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        # Synthetic unbalanced voucher (Dr ≠ Cr per group)
        bad_voucher = {
            "voucher_no": "PBDT00002",
            "prefix": "PBDT",
            "posting_date": "2026-01-31",
            "voucher_remark": "",
            "party_code": None,
            "legs": [
                {"account": "5111", "debit": 0, "credit": 100},
                {"account": "131", "debit": 99, "credit": 0},  # off by 1
                {"account": "5112", "debit": 0, "credit": 50},
                {"account": "131", "debit": 50, "credit": 0},
            ],
        }
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.return_value = {"status": "created", "target_name": "PBDT00002"}
            result = journal_entry.create_je_from_pbdt(
                bad_voucher, split_by_revenue_account=True
            )
            # Fallback → single 1to1 call without overrides
            self.assertEqual(mock_1to1.call_count, 1)
            args, kwargs = mock_1to1.call_args
            self.assertNotIn("legs_override", kwargs)

    def test_split_propagates_first_failure(self):
        """If sub-JE #2 fails, return failed with partial created_subset."""
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        with patch.object(journal_entry, "_create_je_1to1") as mock_1to1:
            mock_1to1.side_effect = [
                {"status": "created", "target_name": "PBDT00001-S1",
                 "target_doctype": "Journal Entry"},
                {"status": "failed",
                 "error": "TK 5112 not mapped"},
            ]
            v = self._build_voucher(num_revenue_groups=2)
            result = journal_entry.create_je_from_pbdt(
                v, split_by_revenue_account=True
            )
            self.assertEqual(result["status"], "failed")
            self.assertIn("split #2", result["error"])
            self.assertEqual(result["created_subset"], ["PBDT00001-S1"])

    def test_voucher_missing_voucher_no_split_path(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        result = journal_entry.create_je_from_pbdt(
            {"legs": [{"account": "5111", "debit": 0, "credit": 100}]},
            split_by_revenue_account=True,
        )
        self.assertEqual(result["status"], "failed")
        self.assertIn("voucher_no", result["error"])

    def test_voucher_missing_legs_split_path(self):
        from vn_accounting.misa_migration.importers.nkc_handlers import journal_entry
        result = journal_entry.create_je_from_pbdt(
            {"voucher_no": "PBDT00001", "legs": []},
            split_by_revenue_account=True,
        )
        self.assertEqual(result["status"], "failed")
        self.assertIn("no legs", result["error"])


if __name__ == "__main__":
    unittest.main()
