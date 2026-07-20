"""Unit tests for run_preflight_setup (Item 3).

Auto-runs ensure_misa_leaves_for_company + ensure_company_defaults_for_misa
+ ensure_party_accounts_for_misa in that order. Idempotent. One step
failure does not abort the other two; failure is captured in `errors`.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestRunPreflightSetup(unittest.TestCase):

    def test_calls_three_helpers_in_order(self):
        """coa_leaves → company_defaults → party_accounts."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        call_order: list[str] = []

        def make_recorder(name):
            def fn(*a, **kw):
                call_order.append(name)
                return {"ok": name}
            return fn

        with patch.object(
            o, "ensure_misa_leaves_for_company",
            side_effect=make_recorder("coa_leaves"),
        ), patch.object(
            o, "ensure_company_defaults_for_misa",
            side_effect=make_recorder("company_defaults"),
        ), patch.object(
            o, "ensure_party_accounts_for_misa",
            side_effect=make_recorder("party_accounts"),
        ):
            summary = o.run_preflight_setup("DCNET TEST")

        self.assertEqual(
            call_order,
            ["coa_leaves", "company_defaults", "party_accounts"],
        )
        self.assertEqual(summary["company"], "DCNET TEST")
        self.assertEqual(summary["coa_leaves"], {"ok": "coa_leaves"})
        self.assertEqual(summary["company_defaults"], {"ok": "company_defaults"})
        self.assertEqual(summary["party_accounts"], {"ok": "party_accounts"})
        self.assertEqual(summary["errors"], [])
        self.assertIn("elapsed_seconds", summary)

    def test_idempotent_double_call(self):
        """Calling twice in a row returns same shape; helpers run again
        but produce no-op results (verified by their own idempotency).
        Here we just verify the wrapper itself doesn't accumulate state."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        with patch.object(o, "ensure_misa_leaves_for_company",
                          return_value={"created": [], "skipped_existing": []}), \
             patch.object(o, "ensure_company_defaults_for_misa",
                          return_value={"already_set": True}), \
             patch.object(o, "ensure_party_accounts_for_misa",
                          return_value={"updated_customers": 0,
                                        "updated_suppliers": 0}):
            r1 = o.run_preflight_setup("DCNET TEST")
            r2 = o.run_preflight_setup("DCNET TEST")

        self.assertEqual(r1["errors"], [])
        self.assertEqual(r2["errors"], [])
        # Both runs return symmetric shape; no leak between invocations
        self.assertEqual(set(r1.keys()), set(r2.keys()))
        # Both successful
        self.assertEqual(r1["coa_leaves"], {"created": [], "skipped_existing": []})
        self.assertEqual(r2["coa_leaves"], {"created": [], "skipped_existing": []})

    def test_one_step_failure_does_not_abort_others(self):
        """company_defaults raises → coa_leaves still runs first, party
        still runs after. Error captured in `errors` list."""
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        order: list[str] = []

        def leaves_fn(*a, **kw):
            order.append("coa_leaves")
            return {}

        def defaults_fn(*a, **kw):
            order.append("company_defaults")
            raise RuntimeError("simulated defaults failure")

        def party_fn(*a, **kw):
            order.append("party_accounts")
            return {}

        with patch.object(o, "ensure_misa_leaves_for_company", side_effect=leaves_fn), \
             patch.object(o, "ensure_company_defaults_for_misa", side_effect=defaults_fn), \
             patch.object(o, "ensure_party_accounts_for_misa", side_effect=party_fn), \
             patch.object(o, "frappe") as mock_frappe:
            mock_frappe.log_error = MagicMock()
            summary = o.run_preflight_setup("DCNET TEST")

        # All three attempted
        self.assertEqual(order,
                         ["coa_leaves", "company_defaults", "party_accounts"])
        # Error recorded for the middle step only
        self.assertEqual(len(summary["errors"]), 1)
        self.assertEqual(summary["errors"][0]["step"], "company_defaults")
        self.assertIn("simulated defaults failure",
                      summary["errors"][0]["error"])
        # Other two steps' results still present
        self.assertEqual(summary["coa_leaves"], {})
        self.assertIsNone(summary["company_defaults"])
        self.assertEqual(summary["party_accounts"], {})
        # frappe.log_error called for the failure
        mock_frappe.log_error.assert_called_once()


class TestRunPhase4PostWiring(unittest.TestCase):
    """run_phase_4_post must call run_preflight_setup at the top."""

    def test_phase_4_post_invokes_preflight_when_company_resolves(self):
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as o

        with patch.object(o, "frappe") as mock_frappe, \
             patch.object(o, "run_preflight_setup") as mock_pre, \
             patch("vn_accounting.misa_migration.context.set_active_company"), \
             patch("vn_accounting.misa_migration.context.clear_active_company"):
            # Batch resolves to DCNET TEST
            mock_frappe.db.get_value.return_value = "DCNET TEST"
            mock_frappe.db.sql.return_value = []
            mock_frappe.publish_realtime = MagicMock()
            mock_pre.return_value = {
                "company": "DCNET TEST", "coa_leaves": {}, "errors": [],
                "company_defaults": {}, "party_accounts": {},
                "elapsed_seconds": 0.1,
            }

            r = o.run_phase_4_post("MM-X")

        mock_pre.assert_called_once_with("DCNET TEST")
        self.assertEqual(r.get("preflight"),
                         mock_pre.return_value)


class TestRunPhase0PostWiring(unittest.TestCase):
    """run_phase_0_post must call run_preflight_setup at the top."""

    def test_phase_0_post_invokes_preflight_when_company_resolves(self):
        from vn_accounting.misa_migration.importers import (
            phase_0_orchestrator as o,
            phase_4_orchestrator,
        )

        with patch.object(o, "frappe") as mock_frappe, \
             patch.object(phase_4_orchestrator, "run_preflight_setup") as mock_pre, \
             patch.object(o, "set_active_company"), \
             patch.object(o, "clear_active_company"):
            mock_frappe.db.get_value.return_value = "DCNET TEST"
            mock_frappe.db.sql.return_value = []
            mock_frappe.publish_realtime = MagicMock()
            mock_pre.return_value = {
                "company": "DCNET TEST", "coa_leaves": {}, "errors": [],
                "company_defaults": {}, "party_accounts": {},
                "elapsed_seconds": 0.1,
            }

            r = o.run_phase_0_post("MM-X")

        mock_pre.assert_called_once_with("DCNET TEST")
        # When no Phase 0 rows present, run_phase_0_post returns early
        # before building summary — preflight call still happens. But
        # the early-return path is checked by `grouped` being empty.
        # The early return shape doesn't include "preflight", that's OK —
        # the important assertion is that preflight WAS invoked.
        # (Full-summary path covered by E2E test.)


if __name__ == "__main__":
    unittest.main()
