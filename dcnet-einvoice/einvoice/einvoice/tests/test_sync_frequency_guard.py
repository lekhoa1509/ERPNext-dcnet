"""Regression tests for run_if_frequency_match elapsed-time guard.

Guards against the `datetime - str` TypeError that crashed every scheduled
inward-sync run: in worker context the Single doc's last_sync_datetime can be
returned as a str, so the guard must coerce it before subtracting.

Runs without live HTTP. Needs a connected Frappe (real now_datetime/get_datetime)
so run via bench console, NOT `bench run-tests`:

    import unittest
    from einvoice.einvoice.tests.test_sync_frequency_guard import TestFrequencyGuard
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TestFrequencyGuard))
"""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import frappe
from frappe.utils import now_datetime, add_to_date

from einvoice.einvoice.services import sync as sync_mod


def _settings(last_sync):
    return SimpleNamespace(
        enable_auto_sync=1,
        sync_frequency="Hourly",  # min_interval = 3600s
        last_sync_datetime=last_sync,
    )


class TestFrequencyGuard(unittest.TestCase):
    def _run_with(self, last_sync):
        """Invoke run_if_frequency_match with mocked frappe surface.

        Returns the MagicMock standing in for SyncService.run_sync so callers
        can assert whether the real sync was triggered.
        """
        cache = MagicMock()
        cache.get_value.return_value = None  # no lock held

        run_sync = MagicMock(return_value={"status": "Success"})

        with patch.object(sync_mod.frappe.db, "exists", return_value=True), \
             patch.object(sync_mod.frappe, "get_single", return_value=_settings(last_sync)), \
             patch.object(sync_mod.frappe, "cache", cache), \
             patch.object(sync_mod.SyncService, "run_sync", run_sync):
            sync_mod.run_if_frequency_match()
        return run_sync

    def test_string_last_sync_old_enough_runs(self):
        """STR last_sync older than interval: no TypeError, sync runs."""
        old = str(add_to_date(now_datetime(), hours=-2))  # 2h ago > 1h interval
        run_sync = self._run_with(old)
        run_sync.assert_called_once_with(sync_type="Scheduled")

    def test_string_last_sync_too_recent_gated(self):
        """STR last_sync within interval: no TypeError, sync is skipped."""
        recent = str(add_to_date(now_datetime(), minutes=-5))  # 5m ago < 1h
        run_sync = self._run_with(recent)
        run_sync.assert_not_called()

    def test_datetime_last_sync_still_works(self):
        """Native datetime path keeps working after the coercion change."""
        old = add_to_date(now_datetime(), hours=-2)
        run_sync = self._run_with(old)
        run_sync.assert_called_once_with(sync_type="Scheduled")

    def test_no_last_sync_runs(self):
        """First-ever run (no last_sync_datetime) proceeds to sync."""
        run_sync = self._run_with(None)
        run_sync.assert_called_once_with(sync_type="Scheduled")


if __name__ == "__main__":
    unittest.main()
