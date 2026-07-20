"""Opening inventory handler — Stock Entry Material Receipt per warehouse.

Phase E commit 13c. Per `~/.claude/rules/frappe-erpnext.md`:

  Stock Reconciliation purpose="Opening Stock" needs Asset/Liability
  difference_account — VN COA only has Equity at 411/412/413 which is
  conceptually wrong for mid-year openings. Use Material Receipt Stock
  Entry instead with Company.stock_adjustment_account = TK 632.

For each warehouse in the parsed inventory rows: create ONE Stock
Entry of `stock_entry_type="Material Receipt"` with all items in that
warehouse as line items. Each item line carries:
  - item_code: Misa Mã hàng (or placeholder fallback)
  - qty: Số lượng tồn
  - basic_rate: Đơn giá  (cost per unit)
  - t_warehouse: target warehouse
  - use_serial_batch_fields: 1  (per the v16 rule)

doc.name: `<batch>-OB-INV-<warehouse-suffix>`.

Skipped rows (silent):
  - Item not in ERPNext (unless `auto_create_items=True` enabled, then a
    minimal placeholder Item is created on the fly)
  - Warehouse not in ERPNext + no default available
  - qty <= 0 or rate <= 0 → 0-value row, irrelevant for opening

Stock adjustment account: ensures Company.stock_adjustment_account is
set to TK 632 fallback if absent (delegated to a shared helper).
"""

from __future__ import annotations

from typing import Any

import frappe

from vn_accounting.misa_migration.context import get_active_company as _get_company

from vn_accounting.misa_migration.importers.nkc_handlers.purchase_receipt import (
    _company_default_warehouse,
)
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    _ensure_placeholder_item,
    _ensure_placeholder_stock_item,
)
from vn_accounting.misa_migration.importers.nkc_handlers.stock_entry import (
    _ensure_stock_adjustment_account,
)


_DEFAULT_OPENING_DATE = "2025-12-31"


def _resolve_warehouse(misa_warehouse: str | None, company: str) -> str | None:
    """Match Misa Mã kho → ERPNext Warehouse.name. Falls back to default."""
    if not misa_warehouse:
        return _company_default_warehouse(company)
    # Try exact match first
    if frappe.db.exists("Warehouse", misa_warehouse):
        return misa_warehouse
    # Try with company suffix (ERPNext convention: "Kho A - DC")
    candidate = frappe.db.get_value(
        "Warehouse",
        {"company": company, "warehouse_name": misa_warehouse, "disabled": 0},
        "name",
    )
    if candidate:
        return candidate
    # Try LIKE on warehouse_name (case-insensitive prefix)
    candidate = frappe.db.get_value(
        "Warehouse",
        {"company": company, "warehouse_name": ["like", f"{misa_warehouse}%"], "disabled": 0},
        "name",
    )
    if candidate:
        return candidate
    return _company_default_warehouse(company)


def _resolve_uom(misa_uom: str | None) -> str:
    """Resolve UOM with safe fallback."""
    if misa_uom and frappe.db.exists("UOM", misa_uom):
        return misa_uom
    if frappe.db.exists("UOM", "Nos"):
        return "Nos"
    return "Unit"


def _resolve_item(misa_item_code: str | None, company: str,
                  placeholder_item: str) -> str:
    """Resolve Misa Mã hàng to ERPNext Item.name; fall back to placeholder."""
    if misa_item_code and frappe.db.exists("Item", misa_item_code):
        return misa_item_code
    return placeholder_item


def _group_by_warehouse(rows: list[dict]) -> dict[str | None, list[dict]]:
    grouped: dict[str | None, list[dict]] = {}
    for r in rows:
        wh = (r.get("warehouse") or "").strip() or None
        grouped.setdefault(wh, []).append(r)
    return grouped


def _safe_suffix(s: str | None) -> str:
    """Compact suffix safe for ERPNext doc.name (no slashes / spaces)."""
    if not s:
        return "DEFAULT"
    out = "".join(c if c.isalnum() else "-" for c in s).strip("-").upper()
    return out[:24] or "DEFAULT"


def post_opening_inventory(
    batch_name: str,
    parsed_rows: list[dict],
    opening_date: str = _DEFAULT_OPENING_DATE,
    company: str | None = None,
) -> dict[str, Any]:
    """Create N Stock Entries (one per warehouse) for opening inventory.

    Args:
      batch_name: parent Misa Migration Batch.
      parsed_rows: output of parse_inventory().
      opening_date: posting_date (default 2025-12-31).
      company: ERPNext Company (default global default).

    Returns:
      {
        status: 'created' | 'partial' | 'failed' | 'skipped',
        target_doctype: 'Stock Entry',
        created_names: list[str],
        skipped_existing: list[str],
        warehouse_count: int,
        item_count: int,
        total_value: float,
        errors: list[{warehouse, error}],
      }
    """
    if not parsed_rows:
        return {"status": "failed", "error": "no rows"}

    company = company or _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    # Ensure stock_adjustment_account set (default 632)
    stock_adj = _ensure_stock_adjustment_account(company)
    if not stock_adj:
        return {"status": "failed",
                "error": f"No stock_adjustment_account on {company} "
                         f"and TK 632 not found"}

    placeholder_item = _ensure_placeholder_stock_item(company)

    grouped = _group_by_warehouse(parsed_rows)
    created: list[str] = []
    skipped_existing: list[str] = []
    errors: list[dict] = []
    total_items = 0
    total_value = 0.0

    for misa_wh, rows in grouped.items():
        target_wh = _resolve_warehouse(misa_wh, company)
        if not target_wh:
            errors.append({
                "warehouse": misa_wh,
                "error": f"Cannot resolve warehouse {misa_wh!r} and no "
                         f"company default on {company}",
            })
            continue

        target_name = f"{batch_name}-OB-INV-{_safe_suffix(misa_wh)}"
        if frappe.db.exists("Stock Entry", target_name):
            skipped_existing.append(target_name)
            continue

        items_payload: list[dict] = []
        for r in rows:
            qty = float(r.get("qty") or 0.0)
            rate = float(r.get("rate") or 0.0)
            amount = float(r.get("amount") or 0.0)
            # Skip zero-qty rows
            if qty <= 0:
                continue
            # Derive rate from amount when only amount + qty available
            if rate <= 0 and amount > 0:
                rate = amount / qty
            uom = _resolve_uom(r.get("uom"))
            item_code = _resolve_item(r.get("item_code"), company, placeholder_item)
            items_payload.append({
                "item_code": item_code,
                "qty": qty,
                "basic_rate": rate,
                "uom": uom,
                "stock_uom": uom,
                "conversion_factor": 1,
                "use_serial_batch_fields": 1,
                "allow_zero_valuation_rate": 1,
                "t_warehouse": target_wh,
                "description": (r.get("item_name") or r.get("item_code") or "")[:140],
            })
            total_items += 1
            total_value += qty * rate

        if not items_payload:
            continue

        payload = {
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "company": company,
            "posting_date": opening_date,
            "set_posting_time": 1,
            "to_warehouse": target_wh,
            "remarks": f"OB inventory — Misa migration batch {batch_name}, "
                       f"warehouse {misa_wh or '(default)'}",
            "items": items_payload,
            "misa_voucher_no": target_name,
        }

        try:
            doc = frappe.get_doc(payload)
            doc.flags.ignore_permissions = True
            doc.insert(set_name=target_name)
            created.append(doc.name)
        except Exception as exc:
            errors.append({
                "warehouse": misa_wh,
                "error": f"{type(exc).__name__}: {exc}",
            })
            frappe.log_error(
                title=f"OB Inventory SE failed: {target_name}",
                message=f"{type(exc).__name__}: {exc}",
            )

    if not created and not skipped_existing:
        return {
            "status": "failed",
            "error": "No Stock Entries created — see errors list",
            "errors": errors,
            "warehouse_count": len(grouped),
            "item_count": 0,
            "total_value": 0.0,
        }

    if not created and skipped_existing:
        status = "skipped"
    elif errors:
        status = "partial"
    else:
        status = "created"
    return {
        "status": status,
        "target_doctype": "Stock Entry",
        "created_names": created,
        "skipped_existing": skipped_existing,
        "warehouse_count": len(grouped),
        "item_count": total_items,
        "total_value": total_value,
        "errors": errors,
    }
