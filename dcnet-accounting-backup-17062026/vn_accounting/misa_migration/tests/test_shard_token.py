"""Tests for two-batch parallel — shard_token semantics.

Covers:
1. lock_key_for_company(): empty token = legacy key; non-empty token =
   per-shard key.
2. find_active_batch(): empty-token search returns only empty-token rows;
   token-scoped search returns only matching-token row; sibling shard
   does NOT block.
3. _resolve_post_queue(): legacy (no token) → 'default'; mapped tokens
   route to 'long' / 'default' deterministically; unknown tokens → 'default'.
4. create_batch(): two batches with different non-empty shard_tokens
   for the same Company can coexist; same Company + same shard_token
   raises; same Company + both-empty raises (legacy behavior).
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

import frappe

from vn_accounting.misa_migration import state as st


class TestLockKeyShardScoping(unittest.TestCase):
    def test_empty_token_returns_legacy_key(self):
        self.assertEqual(
            st.lock_key_for_company("DCNET TEST"),
            "misa_migration_dcnet_test",
        )

    def test_none_token_returns_legacy_key(self):
        self.assertEqual(
            st.lock_key_for_company("DCNET TEST", shard_token=None),
            "misa_migration_dcnet_test",
        )

    def test_nonempty_token_appends_shard_suffix(self):
        self.assertEqual(
            st.lock_key_for_company("DCNET TEST", shard_token="A"),
            "misa_migration_dcnet_test__shard_a",
        )

    def test_two_different_tokens_produce_different_keys(self):
        k1 = st.lock_key_for_company("DCNET TEST", shard_token="A")
        k2 = st.lock_key_for_company("DCNET TEST", shard_token="B")
        self.assertNotEqual(k1, k2)

    def test_token_with_spaces_is_scrubbed(self):
        # frappe.scrub turns "2025 Q1" into "2025_q1"
        self.assertEqual(
            st.lock_key_for_company("DCNET TEST", shard_token="2025 Q1"),
            "misa_migration_dcnet_test__shard_2025_q1",
        )


class TestResolvePostQueue(unittest.TestCase):
    def setUp(self):
        from vn_accounting.misa_migration.api.post import _resolve_post_queue
        self._fn = _resolve_post_queue

    def test_empty_token_routes_to_default(self):
        self.assertEqual(self._fn(""), "default")
        self.assertEqual(self._fn(None), "default")
        self.assertEqual(self._fn("   "), "default")

    def test_shard_A_routes_to_long(self):
        self.assertEqual(self._fn("A"), "long")
        self.assertEqual(self._fn("a"), "long")
        self.assertEqual(self._fn("Adam"), "long")  # first char only

    def test_shard_B_routes_to_default(self):
        self.assertEqual(self._fn("B"), "default")
        self.assertEqual(self._fn("b"), "default")

    def test_numeric_shard_1_routes_to_long(self):
        self.assertEqual(self._fn("1"), "long")
        self.assertEqual(self._fn("1-2026"), "long")

    def test_numeric_shard_2_routes_to_default(self):
        self.assertEqual(self._fn("2"), "default")
        self.assertEqual(self._fn("2025"), "default")

    def test_unknown_first_char_falls_back_to_default(self):
        self.assertEqual(self._fn("X"), "default")
        self.assertEqual(self._fn("ZZZ"), "default")


class TestPrewarmFlagShortCircuit(unittest.TestCase):
    """Tier 1.1 — Redis-cached prewarm flag must short-circuit the
    per-shard run_preflight_setup call so parallel workers don't race
    on Company / Party Account row-level locks.
    """

    def test_prewarm_flag_key_is_company_scoped(self):
        from vn_accounting.misa_migration.api.post import prewarm_flag_key
        k1 = prewarm_flag_key("DCNET TEST")
        k2 = prewarm_flag_key("OTHER CO")
        self.assertNotEqual(k1, k2)
        self.assertIn("DCNET TEST", k1)
        self.assertIn("masters_prewarmed", k1)

    def _build_frappe_mock(self, flag_value):
        """Mock the entire `frappe` module reference at the orchestrator's
        import site (per python-quirks.md — LocalProxy can't be patched
        outside a request context)."""
        from unittest.mock import MagicMock
        mock = MagicMock(name="frappe")
        mock.db.get_value.return_value = "DCNET TEST"
        mock.defaults.get_global_default.return_value = "DCNET TEST"
        mock.cache.return_value.get_value.return_value = flag_value
        # set_active_company sets frappe.flags so make those writable
        mock.flags = MagicMock()
        return mock

    def test_run_phase_4_post_skips_preflight_when_flag_set(self):
        """When prewarm_flag is set, run_phase_4_post must NOT call
        run_preflight_setup (which would race on Company row-level locks
        with a sibling shard). It must still warm the per-process
        Account cache.
        """
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as orch

        run_preflight_called = []
        warm_cache_called = []
        mock_frappe = self._build_frappe_mock(flag_value=1)

        def fake_run_preflight(company):
            run_preflight_called.append(company)
            return {"company_defaults": {}, "errors": []}

        def fake_warm_cache(company):
            warm_cache_called.append(company)

        def fake_load(batch_name):
            return {"NKC": [], "Bang ke BR": [], "Bang ke MV": [], "SCT": []}

        with patch.object(orch, "frappe", mock_frappe), \
             patch.object(orch, "run_preflight_setup", fake_run_preflight), \
             patch.object(orch, "_load_phase_4_payloads", fake_load), \
             patch.object(orch, "set_active_company", lambda c: None), \
             patch.object(orch, "clear_active_company", lambda: None), \
             patch.object(orch, "_publish_progress", lambda *a, **k: None), \
             patch("vn_accounting.misa_migration.importers.nkc_handlers.payment_entry."
                   "_warm_account_cache_for_company", fake_warm_cache), \
             patch("vn_accounting.misa_migration.importers.nkc_handlers.payment_entry."
                   "reset_perf_caches", lambda: None), \
             patch("vn_accounting.misa_migration.importers.nkc_handlers."
                   "_party_cache.warm_party_cache",
                   lambda c: {"customers": 0, "suppliers": 0,
                              "employees": 0, "account_leaves": 0}):
            result = orch.run_phase_4_post("MM-TEST-FLAG-SET", chunk_commit=50)

        # Hard contract: the lock-contention-causing call MUST be skipped
        self.assertEqual(run_preflight_called, [],
                         "run_preflight_setup ran despite prewarm flag set")
        # Per-process cache warm SHOULD still run (Redis flag is shared,
        # in-memory cache is not)
        self.assertEqual(warm_cache_called, ["DCNET TEST"])
        self.assertTrue(result["preflight"].get("skipped_via_prewarm_flag"))

    def test_run_phase_4_post_runs_preflight_when_flag_absent(self):
        """When the prewarm flag is NOT set, run_phase_4_post MUST call
        run_preflight_setup (backwards-compat path for serial / non-prewarmed
        runs).
        """
        from vn_accounting.misa_migration.importers import phase_4_orchestrator as orch

        run_preflight_called = []
        mock_frappe = self._build_frappe_mock(flag_value=None)

        def fake_run_preflight(company):
            run_preflight_called.append(company)
            return {"company_defaults": {}, "errors": []}

        def fake_load(batch_name):
            return {"NKC": [], "Bang ke BR": [], "Bang ke MV": [], "SCT": []}

        with patch.object(orch, "frappe", mock_frappe), \
             patch.object(orch, "run_preflight_setup", fake_run_preflight), \
             patch.object(orch, "_load_phase_4_payloads", fake_load), \
             patch.object(orch, "set_active_company", lambda c: None), \
             patch.object(orch, "clear_active_company", lambda: None), \
             patch.object(orch, "_publish_progress", lambda *a, **k: None), \
             patch("vn_accounting.misa_migration.importers.nkc_handlers.payment_entry."
                   "_warm_account_cache_for_company", lambda c: None), \
             patch("vn_accounting.misa_migration.importers.nkc_handlers.payment_entry."
                   "reset_perf_caches", lambda: None), \
             patch("vn_accounting.misa_migration.importers.nkc_handlers."
                   "_party_cache.warm_party_cache",
                   lambda c: {"customers": 0, "suppliers": 0,
                              "employees": 0, "account_leaves": 0}):
            orch.run_phase_4_post("MM-TEST-FLAG-UNSET", chunk_commit=50)

        self.assertEqual(run_preflight_called, ["DCNET TEST"],
                         "run_preflight_setup MUST run when no prewarm flag")


class TestFindActiveBatchShardScoped(unittest.TestCase):
    """Verify the shard-aware filter logic by patching the `frappe` module
    reference at the state.py import site (frappe.db is a LocalProxy that
    can't be patched directly outside a request context — see
    ~/.claude/rules/python-quirks.md "patch module ref, not attribute").
    """

    def test_no_token_filters_for_empty_shard_only(self):
        captured: dict = {}

        def fake_get_value(doctype, filters, field):
            captured["doctype"] = doctype
            captured["filters"] = dict(filters)
            return None

        with patch("vn_accounting.misa_migration.state.frappe") as mock_frappe:
            mock_frappe.db.get_value = fake_get_value
            st.find_active_batch("DCNET TEST")

        self.assertEqual(captured["doctype"], "Misa Migration Batch")
        self.assertEqual(captured["filters"]["company"], "DCNET TEST")
        # Empty token branch must filter for ["", None]
        self.assertEqual(captured["filters"]["shard_token"], ["in", ["", None]])

    def test_with_token_filters_for_exact_match(self):
        captured: dict = {}

        def fake_get_value(doctype, filters, field):
            captured["filters"] = dict(filters)
            return None

        with patch("vn_accounting.misa_migration.state.frappe") as mock_frappe:
            mock_frappe.db.get_value = fake_get_value
            st.find_active_batch("DCNET TEST", shard_token="A")

        self.assertEqual(captured["filters"]["shard_token"], "A")


def _frappe_bound() -> bool:
    """True when a frappe site context is active. Skips integration tests
    when run under pytest (no frappe.init/connect) — those tests must run
    via the unittest pattern documented in test_e2e_phase_b.py.
    """
    try:
        # Accessing frappe.local.site requires LocalProxy to resolve;
        # raises RuntimeError("object is not bound") under bare pytest.
        _ = frappe.local.site
        return True
    except (RuntimeError, AttributeError):
        return False


@unittest.skipUnless(
    _frappe_bound(),
    "Frappe site context not initialized (run via env/bin/python -m unittest "
    "after frappe.init+connect, NOT bare pytest)",
)
class TestCreateBatchShardCoexistence(unittest.TestCase):
    """Integration test against real DB on DCNET TEST. Two batches with
    different shard_tokens must coexist; same token must collide.
    """

    @classmethod
    def setUpClass(cls):
        cls.company = "DCNET TEST"
        if not frappe.db.exists("Company", cls.company):
            raise unittest.SkipTest(f"{cls.company} not present on this site")

    def setUp(self):
        # Clean any active batch from prior runs
        for b in st.find_all_active_batches(self.company):
            frappe.db.set_value(
                "Misa Migration Batch", b["name"],
                "status", st.REVERSED, update_modified=False,
            )
        frappe.db.commit()

    def tearDown(self):
        # Move any batches created during the test out of ACTIVE so the
        # next test in the suite gets a clean slot
        for b in st.find_all_active_batches(self.company):
            frappe.db.set_value(
                "Misa Migration Batch", b["name"],
                "status", st.REVERSED, update_modified=False,
            )
        frappe.db.commit()

    def test_two_different_shards_can_coexist(self):
        from vn_accounting.misa_migration.api.upload import create_batch

        r_a = create_batch(self.company, batch_title="shard A test",
                           shard_token="A")
        r_b = create_batch(self.company, batch_title="shard B test",
                           shard_token="B")

        self.assertNotEqual(r_a["name"], r_b["name"])
        active = {b["name"]: b for b in st.find_all_active_batches(self.company)}
        self.assertIn(r_a["name"], active)
        self.assertIn(r_b["name"], active)
        self.assertEqual(active[r_a["name"]]["shard_token"], "A")
        self.assertEqual(active[r_b["name"]]["shard_token"], "B")

    def test_same_shard_token_collides(self):
        from vn_accounting.misa_migration.api.upload import create_batch

        create_batch(self.company, batch_title="A first", shard_token="A")
        with self.assertRaises(frappe.exceptions.ValidationError):
            create_batch(self.company, batch_title="A second collision",
                         shard_token="A")

    def test_empty_token_collides_with_empty_token(self):
        from vn_accounting.misa_migration.api.upload import create_batch

        # First create with empty shard — legacy behavior.
        create_batch(self.company, batch_title="legacy first")
        with self.assertRaises(frappe.exceptions.ValidationError):
            create_batch(self.company, batch_title="legacy second")

    def test_sharded_batch_doesnt_collide_with_empty_batch(self):
        """An empty-shard active batch should NOT block a sharded create,
        and vice versa — they occupy different lock slots.
        """
        from vn_accounting.misa_migration.api.upload import create_batch

        legacy = create_batch(self.company, batch_title="legacy")
        sharded = create_batch(self.company, batch_title="shard A",
                               shard_token="A")
        self.assertNotEqual(legacy["name"], sharded["name"])

    def test_shard_token_max_length_enforced(self):
        from vn_accounting.misa_migration.api.upload import create_batch

        with self.assertRaises(frappe.exceptions.ValidationError):
            create_batch(self.company, batch_title="too long",
                         shard_token="X" * 33)


if __name__ == "__main__":
    unittest.main()
