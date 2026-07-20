"""Resolve Misa TK strings → ERPNext Account.name with company abbr suffix.

Misa NKC legs reference accounts by bare TK code ('111', '1121', '6321').
ERPNext Account.name is '{TK} - {Display Name} - {Abbr}' (e.g. '111 - Tiền mặt - DCT').

This module builds a per-process cache from tabAccount and resolves quickly.
"""
from __future__ import annotations

import frappe

# Per-process cache: {company: {misa_tk: full_account_name}}
_CACHE: dict[str, dict[str, str]] = {}


def warm_cache(company: str) -> int:
    """Load all leaf accounts for a Company into cache, keyed by stripped TK.

    Account name format: '{prefix} - {label} - {abbr}'. The prefix part is
    the Misa TK; cache by that.
    """
    rows = frappe.db.sql(
        "SELECT name FROM `tabAccount` WHERE company=%s AND is_group=0",
        (company,), as_dict=True,
    )
    by_tk: dict[str, str] = {}
    for r in rows:
        # Extract leading numeric prefix before ' - '
        name = r["name"]
        if " - " not in name:
            continue
        prefix = name.split(" - ", 1)[0].strip()
        # Use shortest-prefix lookup: 111 → '111 - ...'; 1121 → '1121 - ...'
        by_tk.setdefault(prefix, name)
    _CACHE[company] = by_tk
    return len(by_tk)


def resolve(misa_tk: str | None, company: str) -> str | None:
    """Misa TK string → full ERPNext Account.name (with abbr). Cached.

    Idempotent: if the input already looks like an ERPNext-suffixed name
    ('{TK} - {Label} - {Abbr}') it's returned unchanged after a sanity
    check that the name exists in the cache.
    """
    if not misa_tk:
        return None
    if company not in _CACHE:
        warm_cache(company)
    tk = str(misa_tk).strip()
    cache = _CACHE.get(company, {})
    # Pass-through if already a full ERPNext account name (contains " - ").
    # We still verify it exists by checking if any cached value equals it.
    if " - " in tk:
        # Cache values are full names; build a set on demand and cache it.
        full_names = _CACHE.setdefault(f"__full_set__::{company}", set(cache.values()))
        if tk in full_names:
            return tk
        # Strip the abbr+label and fall through to TK-prefix lookup
        # (handles drift between Misa TK and the company's actual abbr).
        tk = tk.split(" - ", 1)[0].strip()
    # Exact match
    if tk in cache:
        return cache[tk]
    # Strip trailing decimal suffix Misa uses for sub-bank-accounts (1121.81 → 1121)
    if "." in tk:
        base = tk.split(".")[0]
        if base in cache:
            return cache[base]
    # Try ascending prefix match (longest match wins). This handles
    # 'subcode → parent group' (e.g. '11218' → '1121' when CoA has 4-digit leaves).
    for length in range(len(tk), 0, -1):
        prefix = tk[:length]
        if prefix in cache:
            return cache[prefix]
    # Descendant fallback: if Misa uses a parent code ('8211') but CoA only
    # has a deeper leaf ('82111'), find the shortest cache key for which the
    # input is a prefix. Avoids posting GL to a non-existent bare-code account.
    candidates = [k for k in cache if k.startswith(tk) and k != tk]
    if candidates:
        return cache[min(candidates, key=len)]
    return None


def reset() -> None:
    _CACHE.clear()
