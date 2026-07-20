"""Party overlap detection — find Mã that appears in BOTH KH and NCC files.

Per spec §15.4: same Misa Mã (e.g. '1986') often appears in both
Danh_sach_khach_hang and Danh_sach_nha_cung_cap. The two importers create
separate Customer + Supplier records — ERPNext allows same `name` across
DocTypes since name namespaces are per-DocType.

This module provides a passive scanner (informational, no mutation) for
the Review UI to flag overlap rows so accountants notice the dual record.
"""

from __future__ import annotations

import json

import frappe


def _extract_code(row_payload_json: str | None, field_key: str) -> str | None:
    """Pull Misa Mã from a Misa Migration Row's raw_payload JSON."""
    if not row_payload_json:
        return None
    try:
        raw = json.loads(row_payload_json)
    except (ValueError, TypeError):
        return None
    val = raw.get(field_key)
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def detect_overlap(batch_name: str) -> dict:
    """Return overlap report for a batch.

    Result shape:
      {
        "overlapping_codes": ["1986", "20SECTIONS", ...],
        "customer_only": [...],
        "supplier_only": [...],
        "total_customers": int,
        "total_suppliers": int,
        "total_overlap": int,
      }
    """
    customer_rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` WHERE batch=%s AND file_type='Customer'",
        (batch_name,), as_dict=1,
    )
    supplier_rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` WHERE batch=%s AND file_type='Supplier'",
        (batch_name,), as_dict=1,
    )

    customer_codes = {
        _extract_code(r["raw_payload"], "Mã khách hàng")
        for r in customer_rows
    }
    customer_codes.discard(None)
    supplier_codes = {
        _extract_code(r["raw_payload"], "Mã nhà cung cấp")
        for r in supplier_rows
    }
    supplier_codes.discard(None)

    overlap = customer_codes & supplier_codes
    customer_only = customer_codes - supplier_codes
    supplier_only = supplier_codes - customer_codes

    return {
        "overlapping_codes": sorted(overlap),
        "customer_only": sorted(customer_only),
        "supplier_only": sorted(supplier_only),
        "total_customers": len(customer_codes),
        "total_suppliers": len(supplier_codes),
        "total_overlap": len(overlap),
    }


@frappe.whitelist()
def api_detect_overlap(batch_name: str) -> dict:
    """Whitelisted endpoint for Review UI to render overlap warnings."""
    return detect_overlap(batch_name)
