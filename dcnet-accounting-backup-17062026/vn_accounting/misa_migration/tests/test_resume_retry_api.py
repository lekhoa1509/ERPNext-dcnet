"""Unit tests for resume_post + retry_failed_rows API."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestResumePost(unittest.TestCase):

    def test_throws_when_not_stuck(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "POSTED"
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                resume.resume_post("BATCH-X")
            self.assertIn("STUCK", str(ctx.exception))

    def test_transitions_stuck_to_reviewed_then_delegates_to_start_post(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe, \
             patch.object(resume, "st") as mock_st, \
             patch("vn_accounting.misa_migration.api.post.start_post") as mock_start:
            mock_frappe.db.get_value.return_value = "STUCK"
            mock_st.STUCK = "STUCK"
            mock_st.REVIEWED = "REVIEWED"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_frappe.get_doc.return_value = MagicMock()
            mock_start.return_value = {"batch": "BATCH-X", "queued": True}

            r = resume.resume_post("BATCH-X", sync=False)
            # Verified transition called with REVIEWED
            mock_st.transition.assert_called()
            args, kwargs = mock_st.transition.call_args
            self.assertEqual(args[1], "REVIEWED")
            # Delegated to start_post with sync flag pass-through
            mock_start.assert_called_once_with("BATCH-X", sync=False)
            self.assertEqual(r, {"batch": "BATCH-X", "queued": True})


class TestRetryFailedRows(unittest.TestCase):

    def test_throws_when_not_posted_or_stuck(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "POSTING"
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                resume.retry_failed_rows("BATCH-X")
            self.assertIn("POSTED", str(ctx.exception))

    def test_throws_when_no_failed_rows(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "POSTED"
            mock_frappe.db.count.return_value = 0
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                resume.retry_failed_rows("BATCH-X")
            self.assertIn("Failed", str(ctx.exception))

    def test_resets_failed_rows_and_delegates_from_posted(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe, \
             patch.object(resume, "st") as mock_st, \
             patch("vn_accounting.misa_migration.api.post.start_post") as mock_start:
            mock_frappe.db.get_value.return_value = "POSTED"
            mock_frappe.db.count.return_value = 12
            mock_st.POSTED = "POSTED"
            mock_st.STUCK = "STUCK"
            mock_st.REVIEWED = "REVIEWED"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_frappe.get_doc.return_value = MagicMock()
            mock_start.return_value = {"batch": "BATCH-X", "queued": True}

            r = resume.retry_failed_rows("BATCH-X")
            # Status forced to REVIEWED via set_value (POSTED can't transition
            # naturally to REVIEWED via state machine)
            mock_frappe.db.set_value.assert_called()
            args, _ = mock_frappe.db.set_value.call_args
            self.assertEqual(args[0], "Misa Migration Batch")
            self.assertEqual(args[1], "BATCH-X")
            self.assertEqual(args[2]["status"], "REVIEWED")
            # SQL UPDATE called to reset Failed rows
            update_calls = [c for c in mock_frappe.db.sql.call_args_list
                            if "UPDATE" in str(c[0][0]).upper()]
            self.assertGreaterEqual(len(update_calls), 1)
            # Delegated to start_post
            mock_start.assert_called_once()
            # Retried_count included in response
            self.assertEqual(r["retried_count"], 12)

    def test_resets_from_stuck_via_state_transition(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe, \
             patch.object(resume, "st") as mock_st, \
             patch("vn_accounting.misa_migration.api.post.start_post") as mock_start:
            mock_frappe.db.get_value.return_value = "STUCK"
            mock_frappe.db.count.return_value = 5
            mock_st.POSTED = "POSTED"
            mock_st.STUCK = "STUCK"
            mock_st.REVIEWED = "REVIEWED"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_frappe.get_doc.return_value = MagicMock()
            mock_start.return_value = {"batch": "BATCH-X", "queued": True}

            r = resume.retry_failed_rows("BATCH-X")
            # Goes through state transition for STUCK→REVIEWED
            mock_st.transition.assert_called()
            args, _ = mock_st.transition.call_args
            self.assertEqual(args[1], "REVIEWED")


class TestGetFailedRows(unittest.TestCase):

    def test_returns_rows_and_total(self):
        from vn_accounting.misa_migration.api import resume
        with patch.object(resume, "frappe") as mock_frappe:
            mock_frappe.db.sql.return_value = [
                {"name": "row-1", "file_type": "NKC", "row_index": 5,
                 "target_doctype": None, "error_message": "TK 999 not mapped",
                 "payload_preview": "{...}"},
            ]
            mock_frappe.db.count.return_value = 1
            r = resume.get_failed_rows("BATCH-X", limit=50)
            self.assertEqual(r["total"], 1)
            self.assertEqual(len(r["rows"]), 1)
            self.assertEqual(r["limit"], 50)
            self.assertEqual(r["rows"][0]["error_message"], "TK 999 not mapped")


if __name__ == "__main__":
    unittest.main()
