"""Shared doc-naming for Misa migration (Phase 4 vouchers).

ERPNext doc `name` is globally unique per site. The migration derives a
migrated voucher's doc name from its Misa voucher_no — but Misa voucher
numbers (BH20260001, MDV20260001, ...) restart per company, so two
companies migrated onto the SAME site collide on identical names (and the
pre-flight duplicate guard false-blocks). Namespace every migrated Phase-4
doc name by the target Company's abbr:

    ("DCNET Test migrate 1", "BH20260001") -> "DTM1-BH20260001"

This mirrors how ERPNext already namespaces account names per company
("111 - Tiền mặt - DT"). The raw voucher_no is still stored in the
`misa_voucher_no` custom field on every migrated doc AND remains a
substring of the name, so search/traceability by the original number is
preserved.

NB: OB (Phase 0) docs already namespace by `batch_name` (globally unique),
so they do NOT use this helper.
"""

from __future__ import annotations

import frappe

# abbr is immutable for a Company; cache to avoid a DB hit per voucher
# (Phase 4 calls this 10k+ times). Keyed by company name.
_abbr_cache: dict[str, str] = {}


def company_abbr(company: str) -> str:
    if company not in _abbr_cache:
        _abbr_cache[company] = (
            frappe.db.get_value("Company", company, "abbr") or company
        )
    return _abbr_cache[company]


def migrated_doc_name(
    company: str | None, voucher_no: str, suffix: str = ""
) -> str:
    """Company-namespaced ERPNext doc name for a Misa voucher.

    e.g. ("DCNET Test migrate 1", "BH20260001") -> "DTM1-BH20260001".
    Falls back to the bare voucher_no when company is falsy (preserves the
    legacy standalone-handler behaviour). `suffix` is appended after the
    voucher_no (e.g. "-PR" for the purchase-receipt variant).
    """
    base = f"{company_abbr(company)}-{voucher_no}" if company else voucher_no
    return f"{base}{suffix}" if suffix else base
