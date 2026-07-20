"""Asset bulk-pump builder for OB Fixed Asset + OB CCDC.

Builds Asset parent + Asset Finance Book child + Depreciation Schedule child rows.
Uses Straight Line ('Đường thẳng') depreciation: monthly amount = gross / total_periods.

Schedule pre-computation:
  For each period 1..total_number_of_depreciations:
    schedule_date = depreciation_start + (period × frequency_months)
    depreciation_amount = gross / total
    accumulated_depreciation_amount = depreciation_amount × period

Status:
  - Submitted (docstatus=1) for fully-tracked Asset
  - GL Entry for opening accumulated depreciation already in OB JE; we don't
    re-create those here.
"""
from __future__ import annotations

import re
import secrets
from typing import Any

import frappe


def _gen_name() -> str:
    return secrets.token_hex(5)


def _add_months(date_str: str | None, n: int) -> str | None:
    if not date_str:
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(date_str))
    if not m:
        return None
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mo_total = mo - 1 + n
    y += mo_total // 12
    mo = (mo_total % 12) + 1
    if d > 28:
        d = 28  # safe day
    return f"{y:04d}-{mo:02d}-{d:02d}"


def build_asset_dicts(
    asset_data: dict[str, Any],
    company: str,
    asset_category: str,
    location: str,
    is_ccdc: bool = False,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    """Build Asset + Finance Book + Depreciation Schedule rows."""
    code = asset_data.get("asset_code") if not is_ccdc else asset_data.get("ccdc_code")
    name = asset_data.get("asset_name") if not is_ccdc else asset_data.get("ccdc_name")
    gross = float(asset_data.get("gross_amount") or 0)
    accum = float(asset_data.get("accumulated_depreciation") or 0)
    useful_life = asset_data.get("useful_life_months") or asset_data.get("total_periods")
    if not code or not name or gross <= 0 or not useful_life or useful_life <= 0:
        return None
    available_date = (
        asset_data.get("available_for_use_date") or asset_data.get("recognition_date")
    )
    if not available_date:
        return None

    item_code = code  # Assume Item matches by name (Phase 3 importer convention)
    now = frappe.utils.now()
    total_periods = int(useful_life)
    monthly_amt = round(gross / total_periods, 0)
    start_date = _add_months(available_date, 1) or available_date

    # Finance Book child row
    fb_rows = [{
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 1,
        "depreciation_method": "Đường thẳng",
        "total_number_of_depreciations": total_periods,
        "frequency_of_depreciation": 1,  # 1 month = Monthly
        "depreciation_start_date": start_date,
        "expected_value_after_useful_life": 0,
        "value_after_depreciation": gross - accum,
        "parent": code, "parenttype": "Asset", "parentfield": "finance_books",
    }]

    # Depreciation Schedule — one row per period
    schedule_rows: list[dict] = []
    remaining = total_periods - int(round(accum / monthly_amt)) if monthly_amt else 0
    acc = accum
    for p in range(1, total_periods + 1):
        sched_date = _add_months(start_date, p - 1)
        acc += monthly_amt
        schedule_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": p,
            "schedule_date": sched_date,
            "depreciation_amount": monthly_amt,
            "accumulated_depreciation_amount": acc,
            "parent": code, "parenttype": "Asset", "parentfield": "schedules",
        })

    asset_row = {
        "name": code,
        "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "item_code": item_code,
        "item_name": str(name)[:140],
        "asset_name": str(name)[:100],
        "asset_category": asset_category,
        "location": location,
        "purchase_date": available_date,
        "available_for_use_date": available_date,
        "purchase_amount": gross,
        "net_purchase_amount": gross,
        "total_asset_cost": gross,
        "additional_asset_cost": 0,
        "asset_quantity": float(asset_data.get("qty") or 1),
        "opening_accumulated_depreciation": accum,
        "value_after_depreciation": gross - accum,
        "calculate_depreciation": 1,
        "depreciation_method": "Đường thẳng",
        "total_number_of_depreciations": total_periods,
        "frequency_of_depreciation": 1,  # 1 month = Monthly
        "next_depreciation_date": start_date,
        "asset_owner": "Company", "asset_owner_company": company,
        "status": "Submitted",
        "depr_entry_posting_status": "Successful",
    }

    out = {"Asset": [asset_row], "Asset Finance Book": fb_rows, "Depreciation Schedule": schedule_rows}
    return out
