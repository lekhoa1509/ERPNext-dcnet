"""Unit tests for Phase E Undo constraint check + force-undo."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestFindExternalDependents(unittest.TestCase):

    def test_no_dependents_returns_empty(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe:
            meta = MagicMock(); meta.has_field.return_value = True
            meta.istable = False
            mock_frappe.get_meta.return_value = meta
            mock_frappe.db.sql.return_value = []
            posted = [{"target_doctype": "Sales Invoice", "target_name": "BH001"}]
            r = undo._find_external_dependents(posted, {"BH001"})
            self.assertEqual(r, [])

    def test_payment_entry_reference_in_batch_excluded(self):
        """PE that allocates to a batch-created SI is OK if PE is also
        in the batch (will be undone together)."""
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe:
            meta = MagicMock(); meta.has_field.return_value = True
            meta.istable = True
            mock_frappe.get_meta.return_value = meta
            mock_frappe.db.sql.return_value = [
                {"parent": "BC001", "parenttype": "Payment Entry",
                 "dep_name": "BH001"},
            ]
            posted = [{"target_doctype": "Sales Invoice", "target_name": "BH001"}]
            r = undo._find_external_dependents(
                posted, {"BH001", "BC001"}  # BC001 is in same batch
            )
            self.assertEqual(r, [])

    def test_external_payment_entry_blocks(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe:
            meta = MagicMock(); meta.has_field.return_value = True
            meta.istable = True
            mock_frappe.get_meta.return_value = meta
            # SI has 2 dependent edges (Payment Entry Reference + Delivery
            # Note Item). Only the first returns a hit; second returns [].
            call_count = {"n": 0}
            def sql_side_effect(*a, **kw):
                call_count["n"] += 1
                if call_count["n"] == 1:
                    return [{"parent": "PE-MANUAL-001",
                             "parenttype": "Payment Entry",
                             "dep_name": "BH001"}]
                return []
            mock_frappe.db.sql.side_effect = sql_side_effect
            posted = [{"target_doctype": "Sales Invoice", "target_name": "BH001"}]
            r = undo._find_external_dependents(posted, {"BH001"})
            self.assertEqual(len(r), 1)
            self.assertEqual(r[0]["posted_doctype"], "Sales Invoice")
            self.assertEqual(r[0]["posted_name"], "BH001")
            self.assertEqual(r[0]["dependent_doctype"], "Payment Entry")
            self.assertEqual(r[0]["dependent_name"], "PE-MANUAL-001")

    def test_skips_when_field_doesnt_exist_on_dependent(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe:
            meta = MagicMock(); meta.has_field.return_value = False
            meta.istable = True
            mock_frappe.get_meta.return_value = meta
            posted = [{"target_doctype": "Sales Invoice", "target_name": "BH001"}]
            r = undo._find_external_dependents(posted, {"BH001"})
            # No SQL called when field absent
            self.assertEqual(r, [])
            mock_frappe.db.sql.assert_not_called()


class TestConstraintCheck(unittest.TestCase):

    def test_returns_envelope(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "_list_batch_posted_targets") as mock_posted, \
             patch.object(undo, "_find_external_dependents") as mock_find:
            mock_posted.return_value = [
                {"target_doctype": "Sales Invoice", "target_name": "BH001"},
            ]
            mock_find.return_value = [
                {"posted_doctype": "Sales Invoice", "posted_name": "BH001",
                 "dependent_doctype": "Payment Entry",
                 "dependent_name": "PE-EXT", "dependent_field": "reference_name"},
            ]
            r = undo.constraint_check("BATCH-X")
            self.assertEqual(r["batch"], "BATCH-X")
            self.assertEqual(r["blocked_count"], 1)
            self.assertEqual(r["checked_posted_count"], 1)
            self.assertFalse(r["can_undo_cleanly"])
            self.assertEqual(len(r["blocked_docs"]), 1)


class TestStartUndoWithConstraints(unittest.TestCase):

    def test_blocks_when_not_posted(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe:
            mock_frappe.db.get_value.return_value = "REVIEWED"
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                undo.start_undo("BATCH-X")
            self.assertIn("POSTED", str(ctx.exception))

    def test_blocks_when_dependents_and_not_forced(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe, \
             patch.object(undo, "constraint_check") as mock_cc:
            mock_frappe.db.get_value.return_value = "POSTED"
            mock_cc.return_value = {
                "batch": "BATCH-X",
                "blocked_docs": [
                    {"posted_doctype": "Sales Invoice", "posted_name": "BH001",
                     "dependent_doctype": "Payment Entry",
                     "dependent_name": "PE-EXT", "dependent_field": "reference_name"},
                ],
                "blocked_count": 1, "checked_posted_count": 1,
                "can_undo_cleanly": False,
            }
            def fake_throw(msg):
                raise RuntimeError(str(msg))
            mock_frappe.throw.side_effect = fake_throw
            mock_frappe._.side_effect = lambda s: s
            with self.assertRaises(RuntimeError) as ctx:
                undo.start_undo("BATCH-X", force=False)
            self.assertIn("force=true", str(ctx.exception).lower())

    def test_force_bypasses_with_warning_log(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe, \
             patch.object(undo, "constraint_check") as mock_cc, \
             patch.object(undo, "st") as mock_st:
            mock_frappe.db.get_value.return_value = "POSTED"
            mock_st.POSTED = "POSTED"
            mock_cc.return_value = {
                "batch": "BATCH-X", "blocked_docs": [{"x": 1}],
                "blocked_count": 1, "checked_posted_count": 1,
                "can_undo_cleanly": False,
            }
            job = MagicMock(); job.id = "JOB-9"
            mock_frappe.enqueue.return_value = job
            r = undo.start_undo("BATCH-X", force=True, sync=False)
            self.assertTrue(r["forced"])
            self.assertEqual(r["dependent_count"], 1)
            self.assertEqual(r["job_id"], "JOB-9")
            mock_frappe.log_error.assert_called()

    def test_clean_undo_proceeds_without_force(self):
        from vn_accounting.misa_migration.api import undo
        with patch.object(undo, "frappe") as mock_frappe, \
             patch.object(undo, "constraint_check") as mock_cc, \
             patch.object(undo, "st") as mock_st:
            mock_frappe.db.get_value.return_value = "POSTED"
            mock_st.POSTED = "POSTED"
            mock_cc.return_value = {
                "batch": "BATCH-X", "blocked_docs": [],
                "blocked_count": 0, "checked_posted_count": 5,
                "can_undo_cleanly": True,
            }
            job = MagicMock(); job.id = "JOB-1"
            mock_frappe.enqueue.return_value = job
            r = undo.start_undo("BATCH-X", force=False, sync=False)
            self.assertTrue(r["queued"])
            self.assertEqual(r["dependent_count"], 0)
            self.assertFalse(r["forced"])
            mock_frappe.log_error.assert_not_called()


if __name__ == "__main__":
    unittest.main()
