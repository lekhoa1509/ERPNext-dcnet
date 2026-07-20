"""v2 scaffold — scheduled background tasks for API-based bank sync.

When v2 (`BankApiSource` family) is implemented, uncomment the `scheduler_events`
block in hooks.py to enable hourly polling.
"""
import frappe


def sync_all_api_banks():
    """Iterate all Bank Accounts with `api_source` set and trigger import."""
    raise NotImplementedError(
        "v2: implement BankApiSource registry + per-account fetch loop. "
        "See docs/superpowers/specs/2026-04-10-vn-banking-v1-design.md §8."
    )
