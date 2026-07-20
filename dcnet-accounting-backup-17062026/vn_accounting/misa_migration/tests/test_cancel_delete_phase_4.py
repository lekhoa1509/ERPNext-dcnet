"""Unit tests for cancel_phase_4_drafts + delete_phase_4_drafts (Item 2).

Mirrors `submit_phase_4_drafts` shape with REVERSE dependency order,
per-doc commit isolation, stock-account temp-clear/restore workaround,
and the new typed-confirm API endpoints.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestCancelPhase4Drafts(unittest.TestCase):
    """Orchestrator: cancel_phase_4_drafts."""

    def test_reverse_dependency_order_constant(self):
        """PE first (depends on SI/PI), then PI, SI, JE, SE."""
        from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
            _CANCEL_ORDER,
        )
        self.assertEqual(
            _CANCEL_ORDER,
            ["Payment Entry", "Purchase Invoice", "Sales Invoice",
             "Journal Entry", "Stock Entry"],
        )

    def test_returns_failed_when_no_company(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o
        with patch(
            "vn_accounting.misa_migration.context.get_active_company",
            return_value=None,
        ):
            r = o.cancel_phase_4_drafts(batch_name="MM-X", company=None)
        self.assertEqual(r.get("status"), "failed")
        self.assertIn("Company", r.get("error", ""))

    def test_per_doc_failure_does_not_stop_iteration(self):
        """One failing cancel() rolls back its own commit, continues."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        # Track which names were attempted per DocType
        attempted: dict[str, list[str]] = {dt: [] for dt in o._CANCEL_ORDER}
        # Make second PE fail, others succeed
        with patch.object(o, "frappe") as mock_frappe:
            # _stock_accounts_clear_save returns []
            mock_frappe.db.sql_list.side_effect = _make_sql_list_router(
                stock_to_restore=[],
                per_dt={
                    "Payment Entry": ["PE-1", "PE-2"],
                    "Purchase Invoice": ["PI-1"],
                    "Sales Invoice": [],
                    "Journal Entry": [],
                    "Stock Entry": [],
                },
            )

            def get_doc(dt, name):
                attempted[dt].append(name)
                d = MagicMock()
                d.flags = MagicMock()
                if name == "PE-2":
                    d.cancel.side_effect = RuntimeError("boom")
                return d

            mock_frappe.get_doc.side_effect = get_doc
            mock_frappe.db.set_value = MagicMock()
            mock_frappe.db.commit = MagicMock()
            mock_frappe.db.rollback = MagicMock()
            mock_frappe.log_error = MagicMock()
            mock_frappe.publish_realtime = MagicMock()

            r = o.cancel_phase_4_drafts(batch_name=None, company="DCNET TEST")

        # PE-2 failed; PE-1 + PI-1 succeeded
        self.assertEqual(attempted["Payment Entry"], ["PE-1", "PE-2"])
        self.assertEqual(attempted["Purchase Invoice"], ["PI-1"])
        self.assertEqual(r["cancelled"].get("Payment Entry"), 1)
        self.assertEqual(r["cancelled"].get("Purchase Invoice"), 1)
        self.assertEqual(len(r["failed"]["Payment Entry"]), 1)
        self.assertEqual(r["failed"]["Payment Entry"][0][0], "PE-2")
        self.assertEqual(r["total_cancelled"], 2)
        self.assertEqual(r["total_failed"], 1)

    def test_stock_accounts_temp_clear_and_restore(self):
        """Account.account_type='Stock' rows clear at start, restore at end."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        clear_calls: list[tuple] = []
        restore_calls: list[tuple] = []
        # Stock accounts on company
        stock_accts = ["155 - Stock - X", "154 - WIP - X"]

        with patch.object(o, "frappe") as mock_frappe:
            mock_frappe.db.sql_list.side_effect = _make_sql_list_router(
                stock_to_restore=stock_accts,
                per_dt={dt: [] for dt in o._CANCEL_ORDER},
            )

            def set_value(dt, name, field, val, **kw):
                if dt == "Account" and field == "account_type":
                    if val == "":
                        clear_calls.append((name,))
                    elif val == "Stock":
                        restore_calls.append((name,))

            mock_frappe.db.set_value = set_value
            mock_frappe.db.commit = MagicMock()
            mock_frappe.publish_realtime = MagicMock()

            o.cancel_phase_4_drafts(batch_name=None, company="DCNET TEST")

        self.assertEqual(sorted(c[0] for c in clear_calls), sorted(stock_accts))
        self.assertEqual(sorted(c[0] for c in restore_calls), sorted(stock_accts))

    def test_batch_target_filter_when_batch_name_set(self):
        """batch_name=X must inject IN-subquery against Misa Migration Row."""
        from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
            _batch_target_filter,
        )
        clause, params = _batch_target_filter("MM-2026-00898")
        self.assertIn("`tabMisa Migration Row`", clause)
        self.assertIn("batch=%s", clause)
        self.assertIn("target_doctype=%s", clause)
        self.assertEqual(params, ["MM-2026-00898"])

    def test_batch_target_filter_empty_when_no_batch(self):
        from vn_accounting.misa_migration.importers.phase_4_orchestrator import (
            _batch_target_filter,
        )
        clause, params = _batch_target_filter(None)
        self.assertEqual(clause, "")
        self.assertEqual(params, [])


class TestDeletePhase4Drafts(unittest.TestCase):
    """Orchestrator: delete_phase_4_drafts."""

    def test_skips_submitted_docs(self):
        """docstatus=1 docs go into skipped_submitted, not deleted."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        # Each DocType: 2 drafts to delete + 1 submitted to skip
        per_dt = {dt: [f"{dt[:2]}-DRAFT-1", f"{dt[:2]}-DRAFT-2"]
                  for dt in o._CANCEL_ORDER}
        sub_counts = {dt: 1 for dt in o._CANCEL_ORDER}

        with patch.object(o, "frappe") as mock_frappe:
            mock_frappe.db.sql_list.side_effect = _make_sql_list_router(
                stock_to_restore=[], per_dt=per_dt,
            )
            # sql() returns [(N,)] tuple — for the COUNT(*) submitted query
            def sql_router(query, params=(), *a, **kw):
                if "COUNT(*)" in query:
                    dt = _extract_dt_from_query(query)
                    return [(sub_counts.get(dt, 0),)]
                return []

            mock_frappe.db.sql = sql_router
            mock_frappe.delete_doc = MagicMock()
            mock_frappe.db.commit = MagicMock()
            mock_frappe.db.rollback = MagicMock()
            mock_frappe.publish_realtime = MagicMock()

            r = o.delete_phase_4_drafts(batch_name=None, company="DCNET TEST")

        # All 10 drafts deleted (2 × 5 DocTypes)
        self.assertEqual(r["total_deleted"], 10)
        # All 5 submitted skipped
        self.assertEqual(r["total_skipped"], 5)
        for dt in o._CANCEL_ORDER:
            self.assertEqual(r["deleted"][dt], 2)
            self.assertEqual(r["skipped_submitted"][dt], 1)

    def test_returns_failed_when_no_company(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o
        with patch(
            "vn_accounting.misa_migration.context.get_active_company",
            return_value=None,
        ):
            r = o.delete_phase_4_drafts(batch_name="MM-X", company=None)
        self.assertEqual(r.get("status"), "failed")


class TestPipelineRecoveryAPI(unittest.TestCase):
    """API endpoints require typed-confirm token."""

    def test_cancel_phase_4_rejects_wrong_token(self):
        from vn_accounting.misa_migration.api import post as api_post
        with patch.object(api_post, "frappe") as mock_frappe:
            mock_frappe.throw.side_effect = Exception("vn_accounting throw")
            with self.assertRaises(Exception):
                api_post.cancel_phase_4(
                    batch_name="MM-2026-00898", confirm_token="WRONG-CODE",
                )
            # throw was called (not the orchestrator)
            mock_frappe.throw.assert_called_once()

    def test_delete_phase_4_rejects_wrong_token(self):
        from vn_accounting.misa_migration.api import post as api_post
        with patch.object(api_post, "frappe") as mock_frappe:
            mock_frappe.throw.side_effect = Exception("vn_accounting throw")
            with self.assertRaises(Exception):
                api_post.delete_phase_4(
                    batch_name="MM-2026-00898", confirm_token="",
                )
            mock_frappe.throw.assert_called_once()

    def test_cancel_phase_4_invokes_orchestrator_with_company(self):
        """Right token → resolve_batch_company + orchestrator call."""
        from vn_accounting.misa_migration.api import post as api_post
        with patch.object(api_post, "frappe") as mock_frappe, \
             patch("vn_accounting.misa_migration.importers."
                   "phase_4_orchestrator.cancel_phase_4_drafts") as mock_cancel, \
             patch("vn_accounting.misa_migration.context.set_active_company"), \
             patch("vn_accounting.misa_migration.context.clear_active_company"):
            mock_frappe.db.get_value.return_value = "DCNET TEST"
            mock_frappe.defaults.get_global_default.return_value = None
            mock_cancel.return_value = {
                "cancelled": {"Payment Entry": 5}, "failed": {},
                "total_cancelled": 5, "total_failed": 0,
                "elapsed_seconds": 1.2,
            }
            r = api_post.cancel_phase_4(
                batch_name="MM-X", confirm_token="MM-X",
            )
        mock_cancel.assert_called_once_with(
            batch_name="MM-X", company="DCNET TEST",
        )
        self.assertEqual(r["batch"], "MM-X")
        self.assertEqual(r["total_cancelled"], 5)


# ---------------------------------------- helpers

def _make_sql_list_router(stock_to_restore, per_dt):
    """Return a side_effect fn for frappe.db.sql_list that distinguishes:
      * stock-account preflight query → returns stock_to_restore
      * per-DocType target name query → returns per_dt[<DT>]
    """
    def router(query, params=(), *a, **kw):
        if "account_type='Stock'" in query:
            return list(stock_to_restore)
        # Identify the DocType by parsing `tab<DT>` from the FROM clause
        dt = _extract_dt_from_query(query)
        return list(per_dt.get(dt, []))
    return router


def _extract_dt_from_query(query: str) -> str | None:
    """Extract DocType name from `tab<DT>` reference in SQL."""
    import re
    m = re.search(r"`tab([^`]+)`", query)
    if not m:
        return None
    dt = m.group(1)
    # Skip Misa Migration Row (subquery)
    if dt == "Misa Migration Row":
        # Find the OUTER table reference
        matches = re.findall(r"`tab([^`]+)`", query)
        for mt in matches:
            if mt != "Misa Migration Row":
                return mt
    return dt


if __name__ == "__main__":
    unittest.main()
