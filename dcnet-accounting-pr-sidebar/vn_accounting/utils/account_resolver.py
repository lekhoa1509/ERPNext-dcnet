"""Resolve VN Accounting Settings account fields per-company.

VN Accounting Settings is a singleton storing account Link fields with
company-specific suffixes (e.g. "154 - Chi phí SXKD dở dang - DC").
When the site has multiple companies, the stored account may belong to
company A while the caller needs company B's equivalent.

This module provides `resolve_account(field, company)` which:
1. Reads the stored account from Settings
2. Extracts account_number from it
3. Looks up the matching account for the target company
4. Falls back to the stored value if resolution fails (single-company)
"""
from __future__ import annotations

import frappe
from frappe.utils import cint

# Cache per-request to avoid repeated DB hits
_SETTINGS_CACHE_KEY = "_vn_acct_settings_cache"


def _get_settings_value(field: str) -> str | None:
    """Read a field from VN Accounting Settings with per-request cache."""
    cache = getattr(frappe.local, _SETTINGS_CACHE_KEY, None)
    if cache is None:
        cache = {}
        frappe.local._vn_acct_settings_cache = cache
    if field not in cache:
        cache[field] = frappe.db.get_single_value("VN Accounting Settings", field)
    return cache[field]


def resolve_account(field: str, company: str) -> str | None:
    """Resolve a Settings account field for a specific company.

    Args:
        field: VN Accounting Settings fieldname (e.g. 'wip_account_project_costing')
        company: Target company name

    Returns:
        Full account name for the target company, or None if not configured.
    """
    stored = _get_settings_value(field)
    if not stored:
        return None

    # Extract account_number from stored account name
    # ERPNext account name format: "<number> - <label> - <company_abbr>"
    # or "<number> - <number> - <label> - <company_abbr>" (double-numbered)
    account_number = _extract_account_number(stored)
    if not account_number:
        return stored  # fallback: return as-is

    # Check if stored account already belongs to the target company
    stored_company = frappe.db.get_value("Account", stored, "company")
    if stored_company == company:
        return stored

    # Resolve for target company by account_number
    resolved = frappe.db.get_value(
        "Account",
        {"account_number": account_number, "company": company, "is_group": 0},
        "name",
    )
    if resolved:
        return resolved

    # Broader fallback: prefix match (handles sub-accounts like 33312)
    resolved = frappe.db.get_value(
        "Account",
        {"account_number": ["like", f"{account_number}%"], "company": company, "is_group": 0},
        "name",
        order_by="account_number",
    )
    return resolved or stored  # last resort: return stored even if wrong company


def resolve_accounts(fields: list[str], company: str) -> dict[str, str | None]:
    """Resolve multiple Settings account fields at once.

    Returns:
        Dict mapping field name → resolved account name.
    """
    return {f: resolve_account(f, company) for f in fields}


def _extract_account_number(account_name: str) -> str | None:
    """Extract account_number from an ERPNext account name string.

    Examples:
        "154 - Chi phí SXKD dở dang - DC" → "154"
        "154 - 154 - Chi phí SXKD dở dang - DC" → "154"
        "33312 - Thuế GTGT hàng NK - DC" → "33312"
    """
    if not account_name:
        return None
    # Account number is the first segment before " - "
    parts = account_name.split(" - ")
    if not parts:
        return None
    candidate = parts[0].strip()
    # Validate: should be numeric (VN COA account numbers are all-digit)
    if candidate.isdigit():
        return candidate
    return None


def invalidate_cache():
    """Clear the per-request settings cache. Call after saving Settings."""
    if hasattr(frappe.local, _SETTINGS_CACHE_KEY):
        delattr(frappe.local, _SETTINGS_CACHE_KEY)


@frappe.whitelist()
def resolve_accounts_api(fields: str, company: str) -> dict[str, str | None]:
    """Whitelisted endpoint for JS forms to resolve Settings accounts per-company.

    Args:
        fields: JSON array of Settings field names, e.g. '["default_deposit_account"]'
        company: Target company name
    """
    import json as _json
    field_list = _json.loads(fields) if isinstance(fields, str) else fields
    return resolve_accounts(field_list, company)
