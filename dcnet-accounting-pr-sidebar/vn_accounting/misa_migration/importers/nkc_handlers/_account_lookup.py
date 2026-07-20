"""Company-verified Misa TK → ERPNext Account resolution (canonical).

One resolver for every Phase-4 NKC handler + master importer. Fixes the
cross-company leak where ``Misa Account Mapping`` (a site-wide Single,
rewritten by whichever company migrated last) handed another company's
account names to a fresh-company migration — every SI/PI/JE insert then
failed with "Tài khoản X - <abbr> không thuộc về công ty Y" (40k Failed
rows on the first fresh-company E2E, 2026-06-11).

Resolution order (all layers leaf-only):
1. mapping hit — accepted ONLY when that account is a leaf AND belongs to
   the target company (verified via cached Account meta). A stale entry
   (other company / group / deleted account) falls through silently.
2. ``(account_number, company)`` lookup — always company-scoped, cached.
3. Group→leaf self-heal: Misa references a group TK ('8211') but the CoA
   keeps leaves deeper ('82111') — descend to the first leaf.

Caches are per-process and cleared between batches via
``reset_account_caches()`` (chained from payment_entry.reset_perf_caches).
"""
from __future__ import annotations

import frappe

# name → (is_group, account_type, company). Pre-warmed per company by
# warm_account_cache_for_company(); lazily extended on miss.
_ACCOUNT_META_CACHE: dict[str, tuple[int, str, str] | None] = {}
# (account_number, company) → leaf Account.name
_ACCOUNT_BY_NUMBER_CACHE: dict[tuple[str, str], str] = {}


def warm_account_cache_for_company(company: str) -> None:
    """Bulk-load Account meta for every account on company so per-row
    lookups during Phase 4 skip the DB entirely."""
    if not company:
        return
    rows = frappe.db.sql(
        """SELECT name, account_number, is_group,
                  COALESCE(account_type, '') account_type
           FROM `tabAccount` WHERE company=%s""",
        (company,), as_dict=True,
    )
    for r in rows:
        _ACCOUNT_META_CACHE[r["name"]] = (
            int(r["is_group"] or 0), r["account_type"], company,
        )
        if r["account_number"] and not r["is_group"]:
            _ACCOUNT_BY_NUMBER_CACHE[(r["account_number"], company)] = r["name"]


def account_meta(name: str) -> tuple[int, str, str] | None:
    """(is_group, account_type, company) for an Account — cached, lazy.
    Returns None when the account doesn't exist (stale mapping entry)."""
    if name in _ACCOUNT_META_CACHE:
        return _ACCOUNT_META_CACHE[name]
    row = frappe.db.get_value(
        "Account", name, ["is_group", "account_type", "company"], as_dict=True,
    )
    meta = (
        (int(row.is_group or 0), row.account_type or "", row.company)
        if row else None
    )
    _ACCOUNT_META_CACHE[name] = meta
    return meta


def is_group_cached(account_name: str) -> int:
    """is_group (0/1) for an Account; missing account counts as group (=
    unusable in transactions), so callers fall through to live lookup."""
    meta = account_meta(account_name)
    return meta[0] if meta else 1


def resolve_account(misa_tk: str | None, mapping: dict[str, str],
                    company: str | None) -> str | None:
    """Misa TK code → ERPNext Account.name (LEAF only, company-verified)."""
    if not misa_tk:
        return None
    misa_tk = str(misa_tk).strip()
    if not misa_tk:
        return None

    cached = mapping.get(misa_tk)
    if cached:
        meta = account_meta(cached)
        # Leaf + same company → trust the mapping. Anything else (group,
        # deleted, or ANOTHER COMPANY's account) falls through to the
        # company-scoped lookup below.
        if meta and meta[0] == 0 and (not company or meta[2] == company):
            return cached

    if not company:
        return None

    key = (misa_tk, company)
    cached_leaf = _ACCOUNT_BY_NUMBER_CACHE.get(key)
    if cached_leaf:
        mapping[misa_tk] = cached_leaf
        return cached_leaf

    live = frappe.db.get_value(
        "Account",
        {"account_number": misa_tk, "company": company, "is_group": 0},
        "name",
    )
    if live:
        mapping[misa_tk] = live
        _ACCOUNT_BY_NUMBER_CACHE[key] = live
        return live

    # Group-to-leaf self-heal: Misa references TK '8211' but our CoA has
    # 8211 as a group (children 82111, 82112) — descend to first leaf.
    group = frappe.db.get_value(
        "Account",
        {"account_number": misa_tk, "company": company, "is_group": 1},
        ["name", "lft", "rgt"], as_dict=True,
    )
    if group and group.get("lft") is not None and group.get("rgt") is not None:
        leaf = frappe.db.sql(
            """SELECT name FROM `tabAccount`
               WHERE company=%s AND lft > %s AND rgt < %s AND is_group=0
               ORDER BY account_number ASC LIMIT 1""",
            (company, group["lft"], group["rgt"]),
        )
        if leaf:
            leaf_name = leaf[0][0]
            mapping[misa_tk] = leaf_name
            _ACCOUNT_BY_NUMBER_CACHE[key] = leaf_name
            return leaf_name
    return None


def reset_account_caches() -> None:
    """Clear per-process caches between batches (worker stays warm across
    jobs — a stale cache would leak the previous batch's company)."""
    _ACCOUNT_META_CACHE.clear()
    _ACCOUNT_BY_NUMBER_CACHE.clear()
