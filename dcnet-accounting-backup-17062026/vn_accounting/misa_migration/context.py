"""Misa migration context — per-request batch company override.

B2 fix: handlers should respect the Company set on the active Misa
Migration Batch, not the site-wide default. We avoid changing every
handler's signature by stashing the batch's company in a request-local
flag.

Orchestrators (`phase_0_orchestrator`, `phase_4_orchestrator`) call
`set_active_company(batch.company)` at start, `clear_active_company()`
in a `finally`. Handlers read via `get_active_company()` which falls
back to global default + first-company-found.

Why a flag instead of arg-threading: handlers chain into multiple
helpers (`_resolve_account`, `_company_default_warehouse`,
`_ensure_stock_adjustment_account`, …) and adding a `company` param
to all of them touches ~30 functions. The flag is a single insertion
point.
"""

from __future__ import annotations

import frappe


_FLAG_KEY = "misa_migration_company"
_SCT_KEY = "misa_migration_sct_voucher_map"


def set_active_company(company: str | None) -> None:
    """Set the active Company for the duration of the current request.

    Called by orchestrators at start of Phase 0 / Phase 4 post.
    Idempotent — calling with the same value twice is fine.
    """
    if not company:
        clear_active_company()
        return
    try:
        frappe.local.flags = getattr(frappe.local, "flags", None) or frappe._dict()
        setattr(frappe.local.flags, _FLAG_KEY, company)
    except Exception:
        # Bare-module / test context without frappe.local — silent skip
        pass


def clear_active_company() -> None:
    """Reset the active Company override."""
    try:
        if hasattr(frappe, "local") and hasattr(frappe.local, "flags"):
            if hasattr(frappe.local.flags, _FLAG_KEY):
                setattr(frappe.local.flags, _FLAG_KEY, None)
    except Exception:
        pass


def set_sct_voucher_map(m: dict | None) -> None:
    """Stash the parsed SCT voucher map for the active Phase 4 run.

    Set by ``phase_4_orchestrator.run_phase_4_post`` once per request
    after parsing the SCT file. Read by the SE handler to look up real
    item lines for PX / PXHN / PNHN / PN vouchers.

    The map shape is ``{voucher_no: voucher_dict}`` where each
    voucher_dict carries a "lines" list (see sct_parser.group_by_voucher).
    """
    try:
        frappe.local.flags = getattr(frappe.local, "flags", None) or frappe._dict()
        setattr(frappe.local.flags, _SCT_KEY, m or {})
    except Exception:
        pass


def clear_sct_voucher_map() -> None:
    try:
        if hasattr(frappe, "local") and hasattr(frappe.local, "flags"):
            if hasattr(frappe.local.flags, _SCT_KEY):
                setattr(frappe.local.flags, _SCT_KEY, None)
    except Exception:
        pass


def get_sct_voucher(voucher_no: str) -> dict | None:
    """Return the SCT voucher dict for ``voucher_no``, or None if no
    SCT data was loaded for the active batch (legacy single-file mode).
    """
    try:
        if hasattr(frappe, "local") and hasattr(frappe.local, "flags"):
            m = getattr(frappe.local.flags, _SCT_KEY, None)
            if m:
                return m.get(voucher_no)
    except Exception:
        pass
    return None


def get_active_company() -> str | None:
    """Return the active Company, with fallback chain:

      1. frappe.local.flags.misa_migration_company (set by orchestrator)
      2. frappe.defaults.get_global_default("company")
      3. First Company.name found

    Returns None only when the site has zero Companies.
    """
    try:
        if hasattr(frappe, "local") and hasattr(frappe.local, "flags"):
            v = getattr(frappe.local.flags, _FLAG_KEY, None)
            if v:
                return v
    except Exception:
        pass
    return (
        frappe.defaults.get_global_default("company")
        or frappe.db.get_value("Company", {}, "name")
    )
