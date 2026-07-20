"""PERF (Tier 1.5) — module-level cache for Customer / Supplier /
Employee / Account existence checks.

Hot Phase 4 path: handlers call ``frappe.db.exists("Supplier", code)``
once or twice per voucher × ~10k vouchers = ~20k DB round-trips just
to confirm parties exist (preflight already validated them upstream).

This module pre-loads ALL party names for the active Company into
Python sets once per run, so every subsequent membership check is a
~0.1µs set lookup instead of a ~1ms DB round-trip.

Contract:
- ``warm_party_cache(company)`` MUST be called at the start of each
  ``run_phase_4_post`` (per process, per company). It rebuilds the sets.
- ``reset_party_cache()`` clears the sets — used by orchestrator's
  ``reset_perf_caches`` chain.
- ``is_customer``/``is_supplier``/``is_employee``/``is_account_leaf``
  fall back to ``frappe.db.exists`` if the cache is unwarmed (None
  state vs empty set) so handler tests that don't warm the cache
  still work.

Notes:
- Customer / Supplier / Employee are NOT company-scoped at the
  parent-record level in ERPNext — they're global per site. Cache is
  a single set per type.
- Account IS company-scoped — the leaf set covers ``company=<X>`` and
  ``is_group=0``.
"""

from __future__ import annotations

import frappe


# None = uninitialized; empty set = warmed-but-empty. Distinct so that
# unwarmed reads fall through to DB while warmed-but-empty correctly
# rejects unknown codes.
_CUSTOMERS: set[str] | None = None
_SUPPLIERS: set[str] | None = None
_EMPLOYEES: set[str] | None = None
_ACCOUNT_LEAVES: set[str] | None = None
_WARM_COMPANY: str | None = None


def warm_party_cache(company: str) -> dict[str, int]:
    """Pre-load every Customer / Supplier / Employee / Account leaf
    name into module sets. Idempotent — safe to call multiple times.

    Returns ``{"customers", "suppliers", "employees", "account_leaves"}``
    with the count of names loaded into each set.
    """
    global _CUSTOMERS, _SUPPLIERS, _EMPLOYEES, _ACCOUNT_LEAVES, _WARM_COMPANY

    customers = frappe.db.sql_list("SELECT name FROM `tabCustomer`")
    suppliers = frappe.db.sql_list("SELECT name FROM `tabSupplier`")
    employees = frappe.db.sql_list("SELECT name FROM `tabEmployee`")
    account_leaves = frappe.db.sql_list(
        "SELECT name FROM `tabAccount` WHERE company=%s AND is_group=0",
        (company,),
    )

    # Store lowercase keys — MariaDB utf8mb4 default collation is
    # case+accent-insensitive, so frappe.db.exists("Supplier", "VIETTEL")
    # finds "Viettel". Our Python set-lookup must mirror that behavior,
    # otherwise voucher party_code="VIETTEL" fails is_supplier() while
    # the Supplier record stored as "Viettel" exists.
    _CUSTOMERS = {c.lower() for c in customers if c}
    _SUPPLIERS = {s.lower() for s in suppliers if s}
    _EMPLOYEES = {e.lower() for e in employees if e}
    _ACCOUNT_LEAVES = set(account_leaves)  # Account names are exact-case (TK code prefixes)
    _WARM_COMPANY = company

    return {
        "customers": len(_CUSTOMERS),
        "suppliers": len(_SUPPLIERS),
        "employees": len(_EMPLOYEES),
        "account_leaves": len(_ACCOUNT_LEAVES),
    }


def reset_party_cache() -> None:
    """Clear all party / account sets — invalidates the cache so the
    next ``warm_party_cache`` rebuilds from scratch."""
    global _CUSTOMERS, _SUPPLIERS, _EMPLOYEES, _ACCOUNT_LEAVES, _WARM_COMPANY
    _CUSTOMERS = None
    _SUPPLIERS = None
    _EMPLOYEES = None
    _ACCOUNT_LEAVES = None
    _WARM_COMPANY = None


def is_customer(code: str | None) -> bool:
    """True iff a Customer with this name exists (case-insensitive match,
    mirroring MariaDB utf8mb4 default collation). Falls back to
    ``frappe.db.exists`` when the cache hasn't been warmed."""
    if not code:
        return False
    if _CUSTOMERS is None:
        return bool(frappe.db.exists("Customer", code))
    return code.lower() in _CUSTOMERS


def is_supplier(code: str | None) -> bool:
    if not code:
        return False
    if _SUPPLIERS is None:
        return bool(frappe.db.exists("Supplier", code))
    return code.lower() in _SUPPLIERS


def is_employee(code: str | None) -> bool:
    if not code:
        return False
    if _EMPLOYEES is None:
        return bool(frappe.db.exists("Employee", code))
    return code.lower() in _EMPLOYEES


def is_account_leaf(name: str | None, company: str | None = None) -> bool:
    """True iff a non-group Account named ``name`` exists for the
    company that was warmed last. If ``company`` is given and differs
    from the warmed company, falls back to DB (don't trust stale cache)."""
    if not name:
        return False
    if _ACCOUNT_LEAVES is None:
        return bool(frappe.db.exists("Account", {"name": name, "is_group": 0}))
    if company and company != _WARM_COMPANY:
        return bool(frappe.db.exists(
            "Account", {"name": name, "company": company, "is_group": 0}
        ))
    return name in _ACCOUNT_LEAVES


# Test / introspection helpers — never use these in handler code.
def _state_for_test() -> dict[str, int | None]:
    return {
        "customers": None if _CUSTOMERS is None else len(_CUSTOMERS),
        "suppliers": None if _SUPPLIERS is None else len(_SUPPLIERS),
        "employees": None if _EMPLOYEES is None else len(_EMPLOYEES),
        "account_leaves": None if _ACCOUNT_LEAVES is None else len(_ACCOUNT_LEAVES),
        "warm_company": _WARM_COMPANY,
    }
