"""Unit tests for Item 1B-2 opening_journal helpers — parent-summary
dedup + leaf-only resolver guard + data-driven detail-handled prefix.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestDedupeMisaParentSummary(unittest.TestCase):
    """_dedupe_misa_parent_summary_rows filters out parent codes that
    are strict prefixes of another code in the same list."""

    def setUp(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        self._fn = oj._dedupe_misa_parent_summary_rows

    def test_parent_only_keeps_parent(self):
        """When no descendants present, parent is NOT dropped."""
        rows = [{"account_number": "111", "dr": 100}]
        self.assertEqual(self._fn(rows), rows)

    def test_parent_with_one_leaf_drops_parent(self):
        rows = [
            {"account_number": "111", "dr": 100},
            {"account_number": "1111", "dr": 100},
        ]
        out = self._fn(rows)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["account_number"], "1111")

    def test_three_level_drops_grandparent_and_parent(self):
        """411 → 4111 → 41111: only 41111 kept."""
        rows = [
            {"account_number": "411", "dr": 30_000},
            {"account_number": "4111", "dr": 30_000},
            {"account_number": "41111", "dr": 30_000},
        ]
        out = self._fn(rows)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["account_number"], "41111")

    def test_multi_child_parent_dropped(self):
        """156 = sum(1561, 1563): parent 156 dropped, both leaves kept."""
        rows = [
            {"account_number": "156", "dr": 2_702},
            {"account_number": "1561", "dr": 2_690},
            {"account_number": "1563", "dr": 12},
        ]
        out = self._fn(rows)
        codes = sorted(r["account_number"] for r in out)
        self.assertEqual(codes, ["1561", "1563"])

    def test_bank_subcodes_dotted_handled(self):
        """1121 is prefix of 1121.81, 11210, 11214, 11215, 11218 —
        all should be kept; 1121 dropped."""
        rows = [
            {"account_number": "1121", "dr": 728},
            {"account_number": "1121.81", "dr": 506},
            {"account_number": "11210", "dr": 7},
            {"account_number": "11214", "dr": 11},
            {"account_number": "11215", "dr": 165},
            {"account_number": "11218", "dr": 39},
        ]
        out = self._fn(rows)
        codes = sorted(r["account_number"] for r in out)
        self.assertEqual(
            codes, ["1121.81", "11210", "11214", "11215", "11218"]
        )

    def test_no_duplicates_no_change(self):
        """When no parent/leaf relationship exists, all rows kept."""
        rows = [
            {"account_number": "131", "dr": 100},
            {"account_number": "331", "dr": 200},
            {"account_number": "511", "dr": 300},
        ]
        out = self._fn(rows)
        self.assertEqual(len(out), 3)

    def test_empty_input(self):
        self.assertEqual(self._fn([]), [])

    def test_row_without_account_number_kept(self):
        """Defensive: row missing account_number shouldn't crash."""
        rows = [{"foo": "bar"}, {"account_number": "111"}]
        out = self._fn(rows)
        self.assertEqual(len(out), 2)


class TestResolveAccountLeafOnly(unittest.TestCase):
    """Item 1B-2: _resolve_account must NEVER return a group account,
    even when the mapping has an explicit entry pointing at a group."""

    def test_mapping_to_leaf_returns_leaf(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        with patch.object(oj, "frappe") as mf:
            # mapping target is a leaf
            mf.db.get_value.return_value = 0  # is_group=0
            r = oj._resolve_account("141", {"141": "141 - Leaf - X"}, "X")
        self.assertEqual(r, "141 - Leaf - X")

    def test_mapping_to_group_falls_back_to_leaf_lookup(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj

        # Reset the per-process stale-mapping warning cache so this test
        # runs deterministically.
        oj._STALE_MAPPING_WARNED.clear()

        with patch.object(oj, "frappe") as mf:
            # First call (mapping target is_group check): returns 1 → group
            # Second call (leaf account_number lookup): returns leaf name
            def get_value(*args, **kwargs):
                # First arg is doctype 'Account'
                if len(args) >= 3 and args[2] == "is_group":
                    return 1   # mapping target is group
                # Lookup-by-account_number path
                return "1111 - Leaf - X"
            mf.db.get_value.side_effect = get_value
            mf.log_error = MagicMock()
            r = oj._resolve_account(
                "1111", {"1111": "111 - GROUP - X"}, "X",
            )
        self.assertEqual(r, "1111 - Leaf - X")
        # Stale-mapping warning fired
        mf.log_error.assert_called_once()
        call_kwargs = mf.log_error.call_args.kwargs
        self.assertIn("1111", call_kwargs.get("title", ""))

    def test_no_mapping_returns_leaf_lookup(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        with patch.object(oj, "frappe") as mf:
            mf.db.get_value.return_value = "1111 - Leaf - X"
            r = oj._resolve_account("1111", {}, "X")
        self.assertEqual(r, "1111 - Leaf - X")

    def test_empty_input_returns_none(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        self.assertIsNone(oj._resolve_account(None, {}, "X"))
        self.assertIsNone(oj._resolve_account("", {}, "X"))
        self.assertIsNone(oj._resolve_account("   ", {}, "X"))

    def test_stale_mapping_warning_fires_only_once(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj

        oj._STALE_MAPPING_WARNED.clear()
        with patch.object(oj, "frappe") as mf:
            def get_value(*args, **kwargs):
                if len(args) >= 3 and args[2] == "is_group":
                    return 1
                return "1111 - Leaf - X"
            mf.db.get_value.side_effect = get_value
            mf.log_error = MagicMock()
            # Call 3 times with same (tk, group) pair
            for _ in range(3):
                oj._resolve_account(
                    "1111", {"1111": "111 - GROUP - X"}, "X",
                )
        self.assertEqual(mf.log_error.call_count, 1)


class TestIsDetailHandledDataDriven(unittest.TestCase):
    """Item 1B-3: _is_detail_handled honors detail_handled_categories."""

    def test_legacy_behavior_when_none(self):
        """When categories=None, all configured prefixes are detail-handled."""
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        # 131, 331, 1121, 242 are in the narrowed prefix list
        self.assertTrue(oj._is_detail_handled("131", None))
        self.assertTrue(oj._is_detail_handled("331", None))
        self.assertTrue(oj._is_detail_handled("1121.81", None))
        self.assertTrue(oj._is_detail_handled("242", None))

    def test_data_driven_skip_when_category_present(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        # customer present → 131 IS detail-handled (skip)
        self.assertTrue(oj._is_detail_handled("131", {"customer"}))
        # bank absent → 1121 NOT detail-handled (post via general)
        self.assertFalse(oj._is_detail_handled("1121", {"customer"}))

    def test_unrecognized_prefix_returns_false(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        # 511 not in any prefix → not skipped regardless of categories
        self.assertFalse(oj._is_detail_handled("511", None))
        self.assertFalse(oj._is_detail_handled("511", {"customer", "bank"}))

    def test_empty_account_number(self):
        from vn_accounting.misa_migration.importers.ob_handlers \
            import opening_journal as oj
        self.assertFalse(oj._is_detail_handled(None, None))
        self.assertFalse(oj._is_detail_handled("", {"customer"}))


class TestRollUpBalancesByMisaCodes(unittest.TestCase):
    """test_trial_balance helper roll_up_balances_by_misa_codes."""

    def test_no_descendants_returns_self(self):
        from vn_accounting.misa_migration.tests.test_trial_balance_t1_2026 \
            import roll_up_balances_by_misa_codes
        tb = {"111": {"dr": 100, "cr": 0, "balance": 100}}
        out = roll_up_balances_by_misa_codes(tb)
        self.assertEqual(out["111"]["dr"], 100)
        self.assertEqual(out["111"]["balance"], 100)

    def test_parent_rolls_up_children(self):
        from vn_accounting.misa_migration.tests.test_trial_balance_t1_2026 \
            import roll_up_balances_by_misa_codes
        tb = {
            "1561": {"dr": 2_690, "cr": 0},
            "1563": {"dr": 12, "cr": 0},
        }
        out = roll_up_balances_by_misa_codes(
            tb, misa_codes=["156", "1561", "1563"],
        )
        self.assertEqual(out["156"]["dr"], 2_702)
        self.assertEqual(out["1561"]["dr"], 2_690)
        self.assertEqual(out["1563"]["dr"], 12)

    def test_three_level_rollup(self):
        from vn_accounting.misa_migration.tests.test_trial_balance_t1_2026 \
            import roll_up_balances_by_misa_codes
        tb = {"41111": {"dr": 0, "cr": 30_000}}
        out = roll_up_balances_by_misa_codes(
            tb, misa_codes=["411", "4111", "41111"],
        )
        # All three should show same rolled-up value
        self.assertEqual(out["411"]["cr"], 30_000)
        self.assertEqual(out["4111"]["cr"], 30_000)
        self.assertEqual(out["41111"]["cr"], 30_000)

    def test_missing_code_present_with_zero_when_in_misa_codes(self):
        """Code only in misa_codes (not in tb) gets a zero entry."""
        from vn_accounting.misa_migration.tests.test_trial_balance_t1_2026 \
            import roll_up_balances_by_misa_codes
        tb = {"131": {"dr": 100, "cr": 0}}
        out = roll_up_balances_by_misa_codes(
            tb, misa_codes=["131", "141"],
        )
        self.assertEqual(out["141"]["dr"], 0)
        self.assertEqual(out["141"]["cr"], 0)


if __name__ == "__main__":
    unittest.main()
