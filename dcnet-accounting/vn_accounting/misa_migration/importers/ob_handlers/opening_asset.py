"""Opening Fixed Asset + CCDC handler.

Phase E commit 13d. For each row in TSCĐ / CCDC files: create one
ERPNext `Asset` doc with `is_existing_asset=1` so the Asset module
doesn't try to back-reference a Purchase Invoice (these came from Misa,
not from this site's procurement chain).

Required dependencies per row:
  - Asset.item_code → Item exists with is_fixed_asset=1
  - Asset.asset_category → Asset Category exists (resolved from Misa
    "Loại tài sản" via fuzzy match, fallback to a default category)
  - Asset.location → Location exists (optional in ERPNext but useful)
  - Asset.company

Opening shape:
  Asset {
    doctype: 'Asset',
    is_existing_asset: 1,
    item_code: <Misa Mã tài sản>,
    asset_name: <Misa Tên tài sản>,
    asset_category: <resolved>,
    location: <resolved or None>,
    company: <Company>,
    gross_purchase_amount: <nguyên giá>,
    opening_accumulated_depreciation: <hao mòn lũy kế>,
    available_for_use_date: <ngày ghi tăng>,
    depreciation_method: 'Straight Line',
    total_number_of_depreciations: <thời gian SD tháng>,
    frequency_of_depreciation: 'Monthly',
    next_depreciation_date: <ngày tính KH + 1 month>,
    asset_quantity: 1,  (CCDC: qty from Misa)
  }

CCDC differentiator: `is_ccdc=1` custom field on Asset (if present in
this site's schema). The `holding_account` from Misa (typically TK 242)
is informational — ERPNext Asset Category drives the actual GL accounts.

Skipped rows (silent, listed in result):
  - Item with is_fixed_asset=1 doesn't exist on company
  - Asset Category doesn't resolve from Misa "Loại tài sản"
  - Required field None (asset_code, gross_amount, useful_life_months)
"""

from __future__ import annotations

import re
from typing import Any

import frappe


from vn_accounting.misa_migration.context import get_active_company as _get_company

_DEFAULT_OPENING_DATE = "2025-12-31"

# Misa "Loại tài sản" canonical → ERPNext Asset Category name patterns.
# Used to fuzzy-resolve when an exact match isn't found.
_CATEGORY_HINTS = {
    "máy móc": ["Máy móc, thiết bị", "Plant and Machinery", "Machinery"],
    "thiết bị": ["Thiết bị, dụng cụ quản lý", "Office Equipment", "Equipment"],
    "phương tiện": ["Phương tiện vận tải", "Vehicle"],
    "nhà cửa": ["Nhà cửa, vật kiến trúc", "Buildings"],
    "vô hình": ["Tài sản cố định vô hình", "Intangible Asset"],
}


_CCDC_DEFAULT_CATEGORY_NAME = "CCDC"


def _ensure_ccdc_default_category(company: str) -> str | None:
    """Ensure a generic 'CCDC' Asset Category exists for CCDC rows that
    don't carry a Misa 'Loại tài sản' value. Auto-create idempotently.

    CCDC tools/equipment depreciate via TK 242 → TK 627/6427 in VAS, which
    differs from TSCĐ TK 214 → TK 6424. For migration purposes, a single
    catch-all CCDC category is sufficient. Per-account-mapping precision
    happens at GL recognition time (out of scope for opening balance).
    """
    if frappe.db.exists("Asset Category", _CCDC_DEFAULT_CATEGORY_NAME):
        return _CCDC_DEFAULT_CATEGORY_NAME
    # Need at least one fixed_asset_account row for the category to validate.
    # Use TK 242 (Prepaid Expense / Chờ phân bổ) — semantically correct for CCDC.
    cca_account = frappe.db.get_value(
        "Account",
        {"account_number": ["like", "242%"], "company": company, "is_group": 0},
        "name",
    ) or frappe.db.get_value(
        "Account",
        {"account_number": ["like", "153%"], "company": company, "is_group": 0},
        "name",
    )
    dep_expense_account = frappe.db.get_value(
        "Account",
        {"account_number": ["like", "6427%"], "company": company, "is_group": 0},
        "name",
    ) or frappe.db.get_value(
        "Account",
        {"account_number": ["like", "642%"], "company": company, "is_group": 0},
        "name",
    )
    accum_dep_account = frappe.db.get_value(
        "Account",
        {"account_number": ["like", "214%"], "company": company, "is_group": 0},
        "name",
    )
    if not (cca_account and dep_expense_account and accum_dep_account):
        return None  # COA not ready — caller will skip
    try:
        cat = frappe.get_doc({
            "doctype": "Asset Category",
            "asset_category_name": _CCDC_DEFAULT_CATEGORY_NAME,
            "accounts": [{
                "company_name": company,
                "fixed_asset_account": cca_account,
                "accumulated_depreciation_account": accum_dep_account,
                "depreciation_expense_account": dep_expense_account,
            }],
        })
        cat.flags.ignore_permissions = True
        cat.insert(set_name=_CCDC_DEFAULT_CATEGORY_NAME)
        return cat.name
    except Exception:
        # Fall back to any existing category
        return frappe.db.get_value(
            "Asset Category", {}, "name", order_by="creation",
        )


def _resolve_asset_category(
    misa_category: str | None,
    company: str,
    is_ccdc: bool = False,
) -> str | None:
    """Resolve Misa 'Loại tài sản' string → ERPNext Asset Category.name.

    For CCDC rows (which don't carry asset_category in the Misa file),
    auto-create + use a generic 'CCDC' default category.
    """
    if not misa_category:
        if is_ccdc:
            return _ensure_ccdc_default_category(company)
        return None
    cat = misa_category.strip()
    # Exact match
    if frappe.db.exists("Asset Category", cat):
        return cat
    # Hint-driven fuzzy match
    cat_lower = cat.lower()
    for hint, candidates in _CATEGORY_HINTS.items():
        if hint in cat_lower:
            for cand in candidates:
                if frappe.db.exists("Asset Category", cand):
                    return cand
    # Last-resort: pick any active category (caller may want to handle this)
    fallback = frappe.db.get_value(
        "Asset Category", {}, "name", order_by="creation",
    )
    return fallback


_DEFAULT_LOCATION_NAME = "DCNET TEST - Default"


def _ensure_default_location() -> str | None:
    """Ensure a fallback Location exists for Misa migration. Idempotent."""
    if frappe.db.exists("Location", _DEFAULT_LOCATION_NAME):
        return _DEFAULT_LOCATION_NAME
    # Fall back to any existing Location first
    existing = frappe.db.get_value("Location", {}, "name")
    if existing:
        return existing
    try:
        loc = frappe.get_doc({
            "doctype": "Location",
            "location_name": _DEFAULT_LOCATION_NAME,
        })
        loc.flags.ignore_permissions = True
        loc.insert(set_name=_DEFAULT_LOCATION_NAME)
        return loc.name
    except Exception:
        return None


def _resolve_location(misa_location: str | None) -> str | None:
    """Resolve Misa 'Đơn vị sử dụng' string → ERPNext Location.name.

    ERPNext Asset.location is reqd=1, so fall back to a default Location
    (auto-created) when Misa value doesn't match.
    """
    if misa_location:
        loc = misa_location.strip()
        if frappe.db.exists("Location", loc):
            return loc
    return _ensure_default_location()


def _resolve_asset_item(
    misa_code: str | None,
    company: str,
) -> str | None:
    """Return Item.name if exists with is_fixed_asset=1, else None."""
    if not misa_code:
        return None
    item = frappe.db.get_value(
        "Item", {"name": misa_code, "is_fixed_asset": 1}, "name",
    )
    return item


def _add_one_month(date_str: str | None) -> str | None:
    """Add 1 month to ISO date string (depreciation start typically 1
    month after available_for_use_date)."""
    if not date_str:
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", date_str)
    if not m:
        return None
    y, mm, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mm += 1
    if mm > 12:
        mm = 1
        y += 1
    # Clamp day to safe value (most months have 28+ days)
    if d > 28:
        d = 28
    return f"{y:04d}-{mm:02d}-{d:02d}"


def post_opening_assets(
    batch_name: str,
    parsed_rows: list[dict],
    is_ccdc: bool = False,
    company: str | None = None,
    max_rows_per_run: int | None = None,
) -> dict[str, Any]:
    """Create N Asset docs from FA or CCDC opening rows.

    Args:
      batch_name: parent Misa Migration Batch.
      parsed_rows: output of parse_fixed_asset() or parse_ccdc().
      is_ccdc: True for CCDC rows (sets is_ccdc=1 + uses ccdc_code/name fields).
      company: ERPNext Company.
      max_rows_per_run: stop after creating this many NEW Assets and leave
        the rest unprocessed (caller checks `complete` and re-invokes with
        the same parsed_rows on the next post_batch resume — already-
        created assets are cheap no-ops via the target_name exists check
        below). None/0 = no cap, process the whole list in one call.

    Returns:
      {
        status: 'created' | 'partial' | 'skipped' | 'failed',
        target_doctype: 'Asset',
        created_names: list[str],
        skipped_rows: list[{code, reason}],
        skipped_existing: list[str],
        errors: list[{code, error}],
        total_gross: float,
        total_accumulated_depreciation: float,
        remaining_rows: int,
        complete: bool,
      }
    """
    if not parsed_rows:
        return {"status": "failed", "error": "no rows"}

    company = company or _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    created: list[str] = []
    skipped_rows: list[dict] = []
    skipped_existing: list[str] = []
    errors: list[dict] = []
    total_gross = 0.0
    total_accum = 0.0
    created_this_run = 0
    stopped_at = len(parsed_rows)

    for idx, r in enumerate(parsed_rows):
        # Field-name variance between FA + CCDC parsers
        code = r.get("asset_code") if not is_ccdc else r.get("ccdc_code")
        name = r.get("asset_name") if not is_ccdc else r.get("ccdc_name")
        gross = float(r.get("gross_amount") or 0.0)
        accum = float(r.get("accumulated_depreciation") or 0.0)  # FA only
        available_date = (
            r.get("available_for_use_date")
            or r.get("recognition_date")
        )
        useful_life = (
            r.get("useful_life_months")
            or r.get("total_periods")  # CCDC schedule field
        )
        category = r.get("asset_category")
        location = r.get("location")

        if not code:
            skipped_rows.append({"code": None, "reason": "missing code"})
            continue

        # Idempotency: skip if Asset already exists with this name
        target_name = code  # Use Misa code directly (matches Phase 3 Item naming)
        if frappe.db.exists("Asset", target_name):
            skipped_existing.append(target_name)
            continue

        item_code = _resolve_asset_item(code, company)
        if not item_code:
            skipped_rows.append({
                "code": code,
                "reason": f"Item '{code}' not found or is_fixed_asset=0",
            })
            continue

        asset_category = _resolve_asset_category(category, company, is_ccdc=is_ccdc)
        if not asset_category:
            skipped_rows.append({
                "code": code,
                "reason": "No Asset Category configured on company",
            })
            continue

        if not useful_life or useful_life <= 0:
            skipped_rows.append({
                "code": code,
                "reason": "useful_life_months / total_periods missing or 0",
            })
            continue

        if gross <= 0:
            skipped_rows.append({"code": code, "reason": "gross_amount <= 0"})
            continue

        # FIX 3: Item.is_stock_item must be 0 for Asset.item_code. Phase 3
        # Item importer may have set is_stock_item=1 on fixed-asset Items.
        # Flip on disk before insert (update_modified=False keeps the Item's
        # modification audit clean).
        if frappe.db.get_value("Item", item_code, "is_stock_item"):
            frappe.db.set_value("Item", item_code, "is_stock_item", 0,
                                update_modified=False)

        # FIX 2: pre-populate finance_books with VN depreciation_method so
        # ERPNext Asset.set_missing_values() does NOT copy from Asset
        # Category seed (dcnet_sample seeds English "Straight Line", which
        # the vn_accounting Property Setter rejects).
        finance_book_row = {
            "depreciation_method": "Đường thẳng",
            "total_number_of_depreciations": int(useful_life),
            "frequency_of_depreciation": "Monthly",
            "depreciation_start_date": _add_one_month(
                r.get("depreciation_start_date") or available_date
            ),
            "expected_value_after_useful_life": 0,
        }

        asset_payload = {
            "doctype": "Asset",
            "is_existing_asset": 1,
            "item_code": item_code,
            # FIX 4: tighter cap (140 → 100). Vietnamese diacritic-heavy
            # spec strings + quote escaping can still push the stored value
            # past Frappe's Data validation even after [:140] slice.
            "asset_name": (str(name or code))[:100],
            "asset_category": asset_category,
            "company": company,
            "gross_purchase_amount": gross,
            # ERPNext Asset DocType has 3 amount fields all required for
            # is_existing_asset=1: gross_purchase_amount + purchase_amount
            # + net_purchase_amount. For Misa opening (no separate VAT
            # line), all equal nguyên giá.
            "purchase_amount": gross,
            "net_purchase_amount": gross,
            "purchase_date": available_date,  # reqd=1
            "asset_quantity": float(r.get("qty") or 1.0),
            "available_for_use_date": available_date,
            "depreciation_method": "Đường thẳng",  # VN-localised method (vn_accounting)
            "total_number_of_depreciations": int(useful_life),
            "frequency_of_depreciation": "Monthly",
            "opening_accumulated_depreciation": accum,
            "next_depreciation_date": _add_one_month(
                r.get("depreciation_start_date") or available_date
            ),
            "misa_voucher_no": f"{batch_name}-OB-{'CCDC' if is_ccdc else 'ASSET'}-{code}",
            "finance_books": [finance_book_row],
        }
        # FIX 1: Asset.location is reqd=1. _resolve_location already has a
        # default fallback chain; if it still returns None (Location table
        # truly empty), set explicitly to "" only fails — we still must
        # provide a value. Ensure non-None before set.
        resolved_loc = _resolve_location(location) or _ensure_default_location()
        if resolved_loc:
            asset_payload["location"] = resolved_loc
        # CCDC custom field — only set if present in schema (skip otherwise)
        if is_ccdc and frappe.get_meta("Asset").has_field("is_ccdc"):
            asset_payload["is_ccdc"] = 1

        try:
            doc = frappe.get_doc(asset_payload)
            doc.flags.ignore_permissions = True
            doc.insert(set_name=target_name)
            created.append(doc.name)
            total_gross += gross
            total_accum += accum
            created_this_run += 1
            if created_this_run % 50 == 0:
                frappe.db.commit()
        except Exception as exc:
            errors.append({
                "code": code,
                "error": f"{type(exc).__name__}: {exc}",
            })
            frappe.log_error(
                title=f"OB Asset insert failed: {code}",
                message=f"{type(exc).__name__}: {exc}",
            )

        # Server-load cap: create at most max_rows_per_run new Assets per
        # invocation. Rows after this point are simply never looked at —
        # left in parsed_rows for the caller's next resume pass (already-
        # created assets are skipped cheaply via the exists-check above).
        if max_rows_per_run and created_this_run >= max_rows_per_run:
            stopped_at = idx + 1
            break

    if not created and not skipped_existing and not skipped_rows and not errors:
        return {"status": "failed", "error": "all rows filtered with no signal"}
    if not created and skipped_existing and not errors:
        status = "skipped"
    elif not created:
        status = "failed"
    elif errors or skipped_rows:
        status = "partial"
    else:
        status = "created"

    remaining = max(len(parsed_rows) - stopped_at, 0)
    return {
        "status": status,
        "target_doctype": "Asset",
        "is_ccdc": is_ccdc,
        "created_names": created,
        "skipped_rows": skipped_rows,
        "skipped_existing": skipped_existing,
        "errors": errors,
        "total_gross": total_gross,
        "total_accumulated_depreciation": total_accum,
        "asset_count": len(created),
        "remaining_rows": remaining,
        "complete": remaining == 0,
    }
