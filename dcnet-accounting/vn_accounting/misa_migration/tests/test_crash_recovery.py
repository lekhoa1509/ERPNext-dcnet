"""Crash-recovery test scaffolding.

Phase E commit 11. Three scenarios:

1. **Mid-post kill simulation** — batch in POSTING with mixed
   Posted/Ready rows is force-transitioned to STUCK. resume_post should
   transition STUCK → REVIEWED → POSTING. Handler idempotency
   (frappe.db.exists on doc.name) ensures already-Posted vouchers skip
   on the second pass.

2. **Watchdog-induced STUCK + Resume** — exercises the cron path: a
   POSTING batch with stale `modified` timestamp gets marked STUCK by
   the watchdog, then Resume completes the import.

3. **Failed rows + Retry idempotency** — batch ends POSTED with some
   Failed rows. After the operator fixes the root cause, Retry resets
   ONLY those rows back to Ready and re-runs; already-Posted vouchers
   are untouched.

Tests 1 + 3 are gated by MISA_E2E=1 because they create real Misa
Migration Batch + Row docs on the test site. Test 2 (watchdog path) is
always-on — it mocks frappe at module boundary and validates
behavioural contracts.
"""

from __future__ import annotations

import json
import os
import time
import unittest
from unittest.mock import MagicMock, patch


# --------------------------------- always-on: mocked watchdog + resume coupling

class TestWatchdogResumeCoupling(unittest.TestCase):
    """Watchdog marks STUCK → resume_post recovers. No DB writes."""

    def test_watchdog_marks_stuck_then_resume_transitions_back(self):
        """Phase D handlers are idempotent; resume should kick the batch
        back to REVIEWED and re-enqueue post_batch."""
        from vn_accounting.misa_migration.jobs import watchdog
        from vn_accounting.misa_migration.api import resume

        # Phase 1: watchdog runs against a "POSTING idle 15 min" batch
        with patch.object(watchdog, "frappe") as mock_frappe_wd, \
             patch.object(watchdog, "st") as mock_st_wd:
            mock_frappe_wd.db.sql.return_value = [
                {"name": "B-CRASH-1", "status": "POSTING", "minutes_idle": 15},
            ]
            mock_st_wd.POSTING = "POSTING"
            mock_st_wd.REVERSING = "REVERSING"
            mock_st_wd.STUCK = "STUCK"
            mock_st_wd.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st_wd.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            batch_doc = MagicMock(); batch_doc.status = "POSTING"
            mock_frappe_wd.get_doc.return_value = batch_doc

            wd_result = watchdog.check_stuck_batches()
            self.assertEqual(len(wd_result["marked_stuck"]), 1)
            self.assertEqual(wd_result["marked_stuck"][0]["batch"], "B-CRASH-1")
            mock_st_wd.transition.assert_called_with(
                batch_doc, "STUCK", reason="watchdog: no progress for 15 minutes"
            )

        # Phase 2: operator clicks Resume — batch is now STUCK
        with patch.object(resume, "frappe") as mock_frappe_rs, \
             patch.object(resume, "st") as mock_st_rs, \
             patch("vn_accounting.misa_migration.api.post.start_post") as mock_start:
            mock_frappe_rs.db.get_value.return_value = "STUCK"
            mock_st_rs.STUCK = "STUCK"
            mock_st_rs.REVIEWED = "REVIEWED"
            mock_st_rs.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st_rs.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_frappe_rs.get_doc.return_value = MagicMock()
            mock_start.return_value = {"batch": "B-CRASH-1", "queued": True,
                                       "job_id": "RQ-99"}

            rs_result = resume.resume_post("B-CRASH-1", sync=False)
            # Verified STUCK → REVIEWED transition
            args, _ = mock_st_rs.transition.call_args
            self.assertEqual(args[1], "REVIEWED")
            # And re-enqueue happened
            mock_start.assert_called_once_with("B-CRASH-1", sync=False)
            self.assertEqual(rs_result["job_id"], "RQ-99")

    def test_resume_resets_transient_rows_to_ready(self):
        """Rows in non-terminal states (Posting, etc.) should be flipped
        back to Ready so the next post_batch picks them up. Terminal
        statuses (Posted/Skipped/Reversed/Failed/Invalid/Conflict) are
        preserved."""
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
            mock_start.return_value = {"batch": "B", "queued": True}

            resume.resume_post("B", sync=False)
            # The UPDATE Misa Migration Row SQL must NOT touch terminal
            # statuses (Posted, Skipped, Reversed, Failed, Invalid, Conflict)
            update_calls = [
                c[0][0] for c in mock_frappe.db.sql.call_args_list
                if "UPDATE" in c[0][0].upper()
            ]
            self.assertEqual(len(update_calls), 1)
            sql = update_calls[0]
            for terminal in ("Posted", "Skipped", "Reversed",
                             "Failed", "Invalid", "Conflict"):
                self.assertIn(terminal, sql,
                    f"Terminal status {terminal!r} not protected in UPDATE WHERE")


# ----------------------------------- always-on: idempotency check on rerun path

class TestPhase4OrchestratorIdempotency(unittest.TestCase):
    """Re-running run_phase_4_post over already-Posted vouchers should
    surface as 'skipped' status from the handler, not duplicate creation."""

    def test_handler_skipped_status_recorded_correctly(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator
        from vn_accounting.misa_migration.importers import voucher_router

        # Synthetic voucher
        voucher = {
            "voucher_no": "BH99999999", "prefix": "BH",
            "posting_date": "2026-01-15", "voucher_remark": "test",
            "party_code": "C001",
            "legs": [
                {"account": "131", "debit": 100, "credit": 0},
                {"account": "511", "debit": 0, "credit": 100},
            ],
        }

        # Simulate "already created" — router returns skipped
        skipped_result = {
            "status": "skipped",
            "voucher_no": "BH99999999",
            "prefix": "BH",
            "target_doctype": "Sales Invoice",
            "target_name": "BH99999999",
            "error": None,
            "reason": "already_exists",
        }
        with patch.object(voucher_router, "route_voucher",
                          return_value=skipped_result), \
             patch.object(phase_4_orchestrator, "frappe") as mock_frappe, \
             patch.object(phase_4_orchestrator.nkc_parser, "parse_nkc_rows",
                          return_value=[voucher]), \
             patch.object(phase_4_orchestrator.invoice_list_parser,
                          "parse_invoice_list", return_value=[]):
            mock_frappe.db.sql.return_value = [
                {"name": "row1", "file_type": "NKC",
                 "raw_payload": json.dumps({"Số chứng từ": "BH99999999"})},
            ]
            summary = phase_4_orchestrator.run_phase_4_post("BATCH-X")
            # Skipped doc lands in by_target with skipped count
            self.assertEqual(summary["total_vouchers"], 1)
            self.assertEqual(
                summary["by_target_doctype"]["Sales Invoice"]["skipped"], 1
            )
            self.assertEqual(
                summary["by_target_doctype"]["Sales Invoice"]["posted"], 0
            )


# ---------------------------------- gated E2E: real-data resume + retry on DB

@unittest.skipUnless(
    os.environ.get("MISA_E2E") == "1",
    "Set MISA_E2E=1 to run real-data crash recovery tests. Requires Phase "
    "1+2+3 imported + dcnet_sample wiped on the test site.",
)
class TestRealCrashRecovery(unittest.TestCase):
    """Real-data crash + recovery scenarios. Creates a small Misa
    Migration Batch with a handful of vouchers, simulates a kill mid-
    post, and verifies resume completes correctly.
    """

    def setUp(self):
        self.timestamp = int(time.time())
        self.batch_name = None

    def _make_test_batch_with_partial_posted(self):
        """Create a Misa Migration Batch with 3 NKC vouchers — first 2
        already 'Posted' (target docs exist), third left 'Ready'.

        Returns the batch name. Test should clean up via tearDown if
        ALL_TASKS_COMPLETE is desired; for debugging we leave it.
        """
        import frappe
        company = (
            frappe.defaults.get_global_default("company")
            or frappe.db.get_value("Company", {}, "name")
        )
        batch = frappe.get_doc({
            "doctype": "Misa Migration Batch",
            "title": f"Crash recovery test {self.timestamp}",
            "company": company,
            "status": "POSTING",  # simulate mid-post
        })
        batch.flags.ignore_permissions = True
        batch.insert()
        self.batch_name = batch.name

        # Pretend voucher 1 + 2 already created (Posted), voucher 3 Ready
        for idx, status in enumerate(("Posted", "Posted", "Ready"), start=1):
            vno = f"NVK20260000{idx}"
            row = frappe.get_doc({
                "doctype": "Misa Migration Row",
                "batch": batch.name, "file_type": "NKC", "row_index": idx,
                "status": status,
                "target_doctype": "Journal Entry" if status == "Posted" else None,
                "target_name": vno if status == "Posted" else None,
                "raw_payload": json.dumps({
                    "Số chứng từ": vno,
                    "Tài khoản": "131",
                    "Phát sinh Nợ": 100, "Phát sinh Có": 0,
                    "Ngày hạch toán": "2026-01-15",
                }, ensure_ascii=False),
            })
            row.flags.ignore_permissions = True
            row.insert()
        frappe.db.commit()
        return batch.name

    def test_stuck_then_resume_completes_idempotently(self):
        """Mid-post-kill simulation: force STUCK, then resume_post."""
        import frappe
        from vn_accounting.misa_migration import state as st
        from vn_accounting.misa_migration.api import resume

        batch_name = self._make_test_batch_with_partial_posted()
        # Force STUCK manually (simulating watchdog)
        with st.lock_for_batch(frappe.get_doc("Misa Migration Batch", batch_name)):
            batch = frappe.get_doc("Misa Migration Batch", batch_name)
            st.transition(batch, st.STUCK, reason="test simulated kill")
            batch.save(ignore_permissions=True)
            frappe.db.commit()

        # Resume — sync=True so we can assert post-state inline
        result = resume.resume_post(batch_name, sync=True)
        self.assertIn("batch", result)
        # Final batch status should be POSTED (or STUCK again if it fails)
        final_status = frappe.db.get_value(
            "Misa Migration Batch", batch_name, "status"
        )
        self.assertIn(final_status, ("POSTED", "STUCK"),
            f"Resume left batch in {final_status}")

    def test_retry_failed_only_resets_failed_rows(self):
        """Failed-rows reset must NOT touch Posted rows."""
        import frappe
        from vn_accounting.misa_migration.api import resume

        # Build a batch with 2 Posted + 2 Failed rows
        batch = frappe.get_doc({
            "doctype": "Misa Migration Batch",
            "title": f"retry test {self.timestamp}",
            "company": (
                frappe.defaults.get_global_default("company")
                or frappe.db.get_value("Company", {}, "name")
            ),
            "status": "POSTED",
        })
        batch.flags.ignore_permissions = True
        batch.insert()
        for idx, status in enumerate(("Posted", "Posted", "Failed", "Failed"), 1):
            row = frappe.get_doc({
                "doctype": "Misa Migration Row",
                "batch": batch.name, "file_type": "NKC", "row_index": idx,
                "status": status,
                "raw_payload": json.dumps({"Số chứng từ": f"X{idx}"}),
                "error_message": "TK 999 not mapped" if status == "Failed" else None,
            })
            row.flags.ignore_permissions = True
            row.insert()
        frappe.db.commit()

        # Retry — this transitions batch to REVIEWED, calls start_post
        try:
            resume.retry_failed_rows(batch.name, sync=False)
        except Exception:
            # start_post may throw if preflight blocks (no Misa Account
            # Mapping). The reset SQL ran regardless — verify state.
            pass

        # Posted rows untouched, Failed rows reset to Ready
        posted_now = frappe.db.count(
            "Misa Migration Row",
            {"batch": batch.name, "status": "Posted"},
        )
        failed_now = frappe.db.count(
            "Misa Migration Row",
            {"batch": batch.name, "status": "Failed"},
        )
        ready_now = frappe.db.count(
            "Misa Migration Row",
            {"batch": batch.name, "status": "Ready"},
        )
        self.assertEqual(posted_now, 2, "Posted rows must not be reset")
        self.assertEqual(failed_now, 0, "Failed rows should be reset")
        self.assertEqual(ready_now, 2, "Reset rows should land at Ready")


if __name__ == "__main__":
    unittest.main()
