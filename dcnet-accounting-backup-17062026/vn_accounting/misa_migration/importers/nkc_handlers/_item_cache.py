"""Item name → code resolution cache for SI/PI/PR line items.

Bảng kê (BR/MV/SCT) line items carry "Mặt hàng" (item_name) but NOT the
Misa "Mã" (item_code). Phase 3 master imports Items by code as PK;
``Item.item_name`` stores Misa "Tên" truncated to 140 chars.

To match line items to real Item codes (avoiding the
MISA-MIGRATION-SVC / MISA-MIGRATION-STOCK placeholder fallback for the
14,990 lines on T1/2026 datasets), we build a normalized
``{item_name → item_code}`` map once per phase-4 run.

Contract:
- ``warm_item_cache()`` MUST be called by phase_4_orchestrator after
  Phase 3 Items have been imported. Items are global per site (not
  Company-scoped at PK level), so no company filter.
- ``reset_item_cache()`` clears state — invoked by
  ``reset_perf_caches`` chain.
- ``match_item_code(name, require_stock=...)`` returns ``Item.name`` for
  an exact normalized-name match, or ``None``. Falls back to live DB
  query when cache unwarmed (parity with _party_cache).

Normalization: lowercase + strip + collapse internal whitespace.
Truncation to 140 chars mirrors Item importer's cap so cache keys and
fresh line-item lookups produce identical strings.

Collision policy: when N Items share the same normalized name, the
FIRST one inserted wins (Misa typically has 1:1 mapping; duplicates
are rare and acceptable because both candidates carry the same
descriptive name → either choice is correct from line-description POV).
"""

from __future__ import annotations

import re

import frappe


# None = uninitialized; empty dict = warmed-but-empty. Mirrors
# _party_cache semantics.
_ITEM_NAME_TO_CODE: dict[str, str] | None = None
_ITEM_STOCK_CODES: set[str] | None = None


_WS_RE = re.compile(r"\s+")


def _normalize(name: str | None) -> str:
    if not name:
        return ""
    n = _WS_RE.sub(" ", str(name).strip()).lower()
    return n[:140]


def warm_item_cache() -> dict[str, int]:
    """Pre-load every Item.item_name → Item.name pair into the cache.

    Returns ``{"items": N, "stock_items": K}`` for progress reporting.
    """
    global _ITEM_NAME_TO_CODE, _ITEM_STOCK_CODES

    rows = frappe.db.sql(
        "SELECT name, item_name, is_stock_item FROM `tabItem` WHERE disabled=0",
        as_dict=True,
    )
    name_map: dict[str, str] = {}
    stock_codes: set[str] = set()
    for r in rows:
        code = r.get("name")
        item_name = r.get("item_name")
        if not code or not item_name:
            continue
        key = _normalize(item_name)
        if key and key not in name_map:
            name_map[key] = code
        if r.get("is_stock_item"):
            stock_codes.add(code)

    _ITEM_NAME_TO_CODE = name_map
    _ITEM_STOCK_CODES = stock_codes
    return {"items": len(name_map), "stock_items": len(stock_codes)}


def reset_item_cache() -> None:
    """Clear the cache — next warm_item_cache rebuilds from scratch."""
    global _ITEM_NAME_TO_CODE, _ITEM_STOCK_CODES
    _ITEM_NAME_TO_CODE = None
    _ITEM_STOCK_CODES = None


def match_item_code(
    name: str | None,
    *,
    require_stock: bool = False,
    require_non_stock: bool = False,
) -> str | None:
    """Resolve a Misa "Mặt hàng" line-item name to an ERPNext Item code.

    Args:
      name: Misa bảng kê "Mặt hàng" cell value.
      require_stock: when True, only match Items with ``is_stock_item=1``.
        Used by Stock Entry / Purchase Receipt handlers that reject
        service items.
      require_non_stock: when True, only match Items with ``is_stock_item=0``.
        Used by SI/PI MDV/MH handlers (update_stock=0) — matching a stock
        Item on a non-stock PI triggers ERPNext's set_expense_account
        override that forces expense_account = Company.stock_received_but_not_billed,
        which on VN small-template Companies equals payable account 331
        (= credit_to) → ValidationError "Expense = Credit To". Skipping
        stock-Item matches falls back to the placeholder Item path, which
        keeps the Dr expense from NKC honored.

    Returns:
      ``Item.name`` if a normalized-name match exists and meets the stock
      requirement, else ``None``.
    """
    if not name:
        return None
    key = _normalize(name)
    if not key:
        return None
    if _ITEM_NAME_TO_CODE is None:
        # Unwarmed — fall back to a single live DB lookup. Slower but
        # correct (matches _party_cache.is_customer semantics).
        live = frappe.db.get_value("Item", {"item_name": name[:140], "disabled": 0}, "name")
        if not live:
            return None
        is_stock = bool(frappe.db.get_value("Item", live, "is_stock_item"))
        if require_stock and not is_stock:
            return None
        if require_non_stock and is_stock:
            return None
        return live
    code = _ITEM_NAME_TO_CODE.get(key)
    if not code:
        return None
    is_stock = (_ITEM_STOCK_CODES is not None) and (code in _ITEM_STOCK_CODES)
    if require_stock and not is_stock:
        return None
    if require_non_stock and is_stock:
        return None
    return code


# Test / introspection — never use in handler code.
def _state_for_test() -> dict[str, int | None]:
    return {
        "items": None if _ITEM_NAME_TO_CODE is None else len(_ITEM_NAME_TO_CODE),
        "stock_items": None if _ITEM_STOCK_CODES is None else len(_ITEM_STOCK_CODES),
    }
