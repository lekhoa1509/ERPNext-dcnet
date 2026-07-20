"""
Background Job: Sync Inward Invoices from E-Invoice Providers.

Thin wrapper — delegates to services/sync.py.
Kept for backward compatibility with hooks.py import paths.
"""

from einvoice.einvoice.services.sync import run_if_frequency_match, SyncService  # noqa: F401


def run_sync(sync_type="Manual"):
    return SyncService.run_sync(sync_type=sync_type)
