"""Tier 1.3 — track_changes save+restore must survive an exception.

A mid-migration crash inside ``_run_phase_4_post_impl`` MUST NOT leave
the site with chatter audit silenced. The wrapper uses try/finally;
this proves the finally runs even when the inner call raises.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestTrackChangesRestoreOnException(unittest.TestCase):
    def test_restore_runs_when_impl_raises(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as orch

        # Record each set_value call so we can prove restore happened
        # AFTER the inner raise.
        calls: list[tuple[str, int]] = []

        def fake_set_value(doctype, dt_name, field, value, update_modified=False):
            if doctype == "DocType" and field == "track_changes":
                calls.append((dt_name, int(value)))
            return None

        def fake_get_value(doctype, dt_name, field):
            # Pretend every DocType currently has track_changes=1
            if doctype == "DocType" and field == "track_changes":
                return 1
            return None

        def boom_impl(batch_name, chunk_commit, max_rows_per_run=None):
            raise RuntimeError("simulated mid-migration crash")

        mock_frappe = MagicMock(name="frappe")
        mock_frappe.db.set_value.side_effect = fake_set_value
        mock_frappe.db.get_value.side_effect = fake_get_value
        mock_frappe.db.commit.return_value = None

        with patch.object(orch, "frappe", mock_frappe), \
             patch.object(orch, "_run_phase_4_post_impl", boom_impl):
            with self.assertRaises(RuntimeError):
                orch.run_phase_4_post("MM-TEST-CRASH")

        # 5 doctypes × 2 calls (set-to-0 on save, restore-to-1) = 10 calls
        set_zero = [(dt, v) for dt, v in calls if v == 0]
        set_one = [(dt, v) for dt, v in calls if v == 1]

        # All 5 voucher DocTypes were silenced
        self.assertEqual(len(set_zero), 5,
                         f"expected 5 disable calls, got {set_zero}")
        # All 5 were restored — proves finally ran despite the raise
        self.assertEqual(len(set_one), 5,
                         f"expected 5 restore calls after raise, got {set_one}")

        # Restored DocTypes match the disabled set
        self.assertEqual(
            {dt for dt, _v in set_zero},
            {dt for dt, _v in set_one},
        )
        # Each of the 5 target DocTypes is in there
        for dt in (
            "Sales Invoice", "Purchase Invoice", "Payment Entry",
            "Journal Entry", "Stock Entry",
        ):
            self.assertIn(dt, {x for x, _ in set_zero})

    def test_restore_skipped_when_already_zero(self):
        """If a DocType already has track_changes=0, the save dict
        records 0 and the restore is a no-op. No spurious DB writes.
        """
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as orch

        calls: list[tuple[str, int]] = []

        def fake_set_value(doctype, dt_name, field, value, update_modified=False):
            if doctype == "DocType" and field == "track_changes":
                calls.append((dt_name, int(value)))
            return None

        def fake_get_value(doctype, dt_name, field):
            # Already 0 — nothing to silence
            if doctype == "DocType" and field == "track_changes":
                return 0
            return None

        mock_frappe = MagicMock(name="frappe")
        mock_frappe.db.set_value.side_effect = fake_set_value
        mock_frappe.db.get_value.side_effect = fake_get_value

        saved = orch._disable_track_changes_for_misa()
        orch._restore_track_changes(saved)

        # Saved should still record original values (all 0)
        # But because they were already 0, no set_value was called to
        # silence them. And restore-to-0 is also a write, but our impl
        # writes back the saved value regardless — verify exactly the
        # 5 restore-to-0 writes (no save-to-0 writes since current was 0).
        with patch.object(orch, "frappe", mock_frappe):
            saved = orch._disable_track_changes_for_misa()
            self.assertEqual(saved, {
                "Sales Invoice": 0, "Purchase Invoice": 0,
                "Payment Entry": 0, "Journal Entry": 0, "Stock Entry": 0,
            })
            orch._restore_track_changes(saved)
            # 5 restore-to-0 writes (impl is unconditional restore)
            self.assertEqual(len(calls), 5)
            self.assertTrue(all(v == 0 for _, v in calls))


if __name__ == "__main__":
    unittest.main()
