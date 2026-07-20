"""Resolve Misa bare warehouse names → ERPNext Warehouse.name (with abbr).

Misa SCT lines carry warehouse names as bare strings ('KHO CÔNG TY').
ERPNext Warehouse.name is '{Bare Name} - {Abbr}' (e.g. 'KHO CÔNG TY - DCT').

Without this, SE builder writes bare names into Stock Entry Detail + SLE
→ SLE.warehouse doesn't join cleanly to tabWarehouse → Bin rebuild + every
stock report breaks.

Per-process cache; warm once per migration run.
"""
from __future__ import annotations

import frappe

_CACHE: dict[str, dict[str, str]] = {}


def warm_cache(company: str) -> int:
    """Load all warehouses for a Company into cache. Multi-key index per
    Warehouse so SCT lookups by Mã kho code, Tên kho only, or full name
    all resolve to the same Warehouse.

    For 'KHO - KHO CÔNG TY - DCT' (derive_masters format), index keys:
      - 'KHO - KHO CÔNG TY - DCT' (full, idempotent)
      - 'KHO - KHO CÔNG TY'       (without abbr)
      - 'KHO'                      (Mã kho code)
      - 'KHO CÔNG TY'              (Tên kho only)
    """
    rows = frappe.db.sql(
        "SELECT name FROM `tabWarehouse` WHERE company=%s",
        (company,), as_dict=True,
    )
    by_key: dict[str, str] = {}
    for r in rows:
        nm = r["name"]
        by_key.setdefault(nm, nm)
        without_abbr = nm.rsplit(" - ", 1)[0] if " - " in nm else nm
        by_key.setdefault(without_abbr, nm)
        if " - " in without_abbr:
            code, _, ten_kho = without_abbr.partition(" - ")
            code, ten_kho = code.strip(), ten_kho.strip()
            if code:
                by_key.setdefault(code, nm)
            if ten_kho:
                by_key.setdefault(ten_kho, nm)
    _CACHE[company] = by_key
    return len(by_key)


def resolve(bare_name: str | None, company: str) -> str | None:
    """Bare or suffixed warehouse name → full ERPNext Warehouse.name."""
    if not bare_name:
        return None
    if company not in _CACHE:
        warm_cache(company)
    cache = _CACHE.get(company, {})
    return cache.get(str(bare_name).strip())


def reset() -> None:
    _CACHE.clear()
