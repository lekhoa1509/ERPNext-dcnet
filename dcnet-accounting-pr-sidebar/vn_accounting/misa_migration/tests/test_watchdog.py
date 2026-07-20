"""Unit tests for the Phase E watchdog cron."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestCheckStuckBatches(unittest.TestCase):

    def test_no_idle_batches_returns_zero(self):
        from vn_accounting.misa_migration.jobs import watchdog
        with patch.object(watchdog, "frappe") as mock_frappe:
            mock_frappe.db.sql.return_value = []
            r = watchdog.check_stuck_batches()
            self.assertEqual(r["checked"], 0)
            self.assertEqual(r["marked_stuck"], [])
            self.assertEqual(r["threshold_minutes"], 10)

    def test_idle_posting_batch_marked_stuck(self):
        from vn_accounting.misa_migration.jobs import watchdog
        with patch.object(watchdog, "frappe") as mock_frappe, \
             patch.object(watchdog, "st") as mock_st:
            mock_frappe.db.sql.return_value = [
                {"name": "BATCH-1", "status": "POSTING", "minutes_idle": 13},
            ]
            mock_st.POSTING = "POSTING"
            mock_st.REVERSING = "REVERSING"
            mock_st.STUCK = "STUCK"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            fake_batch = MagicMock()
            fake_batch.status = "POSTING"
            mock_frappe.get_doc.return_value = fake_batch

            r = watchdog.check_stuck_batches()
            self.assertEqual(r["checked"], 1)
            self.assertEqual(len(r["marked_stuck"]), 1)
            self.assertEqual(r["marked_stuck"][0]["batch"], "BATCH-1")
            self.assertEqual(r["marked_stuck"][0]["minutes_idle"], 13)
            mock_st.transition.assert_called()
            args, kwargs = mock_st.transition.call_args
            self.assertEqual(args[1], "STUCK")
            self.assertIn("watchdog", kwargs.get("reason", ""))

    def test_status_advanced_between_query_and_lock_skipped(self):
        """Race: another worker completed the batch between SELECT and lock."""
        from vn_accounting.misa_migration.jobs import watchdog
        with patch.object(watchdog, "frappe") as mock_frappe, \
             patch.object(watchdog, "st") as mock_st:
            mock_frappe.db.sql.return_value = [
                {"name": "BATCH-1", "status": "POSTING", "minutes_idle": 15},
            ]
            mock_st.POSTING = "POSTING"
            mock_st.REVERSING = "REVERSING"
            mock_st.STUCK = "STUCK"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            fake_batch = MagicMock()
            fake_batch.status = "POSTED"  # advanced!
            mock_frappe.get_doc.return_value = fake_batch

            r = watchdog.check_stuck_batches()
            self.assertEqual(r["checked"], 1)
            self.assertEqual(r["marked_stuck"], [])
            mock_st.transition.assert_not_called()

    def test_per_batch_exception_swallowed_log_then_continue(self):
        from vn_accounting.misa_migration.jobs import watchdog
        with patch.object(watchdog, "frappe") as mock_frappe, \
             patch.object(watchdog, "st") as mock_st:
            mock_frappe.db.sql.return_value = [
                {"name": "BATCH-1", "status": "POSTING", "minutes_idle": 13},
                {"name": "BATCH-2", "status": "REVERSING", "minutes_idle": 20},
            ]
            mock_st.POSTING = "POSTING"
            mock_st.REVERSING = "REVERSING"
            mock_st.STUCK = "STUCK"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            # BATCH-1 explodes, BATCH-2 succeeds
            call_count = {"n": 0}
            def doc_side_effect(*a, **kw):
                call_count["n"] += 1
                if call_count["n"] == 1:
                    raise RuntimeError("DB lock failed")
                m = MagicMock(); m.status = "REVERSING"
                return m
            mock_frappe.get_doc.side_effect = doc_side_effect
            r = watchdog.check_stuck_batches()
            self.assertEqual(r["checked"], 2)
            self.assertEqual(len(r["marked_stuck"]), 1)
            self.assertEqual(r["marked_stuck"][0]["batch"], "BATCH-2")
            mock_frappe.log_error.assert_called()

    def test_custom_threshold_propagated(self):
        from vn_accounting.misa_migration.jobs import watchdog
        with patch.object(watchdog, "frappe") as mock_frappe:
            mock_frappe.db.sql.return_value = []
            r = watchdog.check_stuck_batches(idle_minutes=25)
            self.assertEqual(r["threshold_minutes"], 25)
            args, _ = mock_frappe.db.sql.call_args
            # Third positional arg to the SQL call is the threshold
            sql_args = args[1]
            self.assertEqual(sql_args[2], 25)


class TestHooksRegistration(unittest.TestCase):
    """Verify the watchdog is wired into scheduler_events.cron."""

    def test_watchdog_path_in_hooks(self):
        import vn_accounting.hooks as hooks
        self.assertIn("cron", hooks.scheduler_events)
        cron = hooks.scheduler_events["cron"]
        # 5-minute cron
        self.assertIn("*/5 * * * *", cron)
        targets = cron["*/5 * * * *"]
        self.assertIn(
            "vn_accounting.misa_migration.jobs.watchdog.check_stuck_batches",
            targets,
        )


if __name__ == "__main__":
    unittest.main()
