"""Backfill missing Bin rows for items present in source OB Inventory but
absent from DB Bin.

Use case: Misa migration bulk_pump OB Inventory builder skipped some
(item, warehouse) pairs (warehouse mapping miss, item not yet derived, etc.)
After masters are confirmed present, this backfill recovers the missed
opening balance by directly INSERTing Bin + SLE rows.

Idempotent: re-running on existing (item, warehouse) Bin is no-op (skips).

Public entry: ``backfill_missing_ob_bins(company, batch_name)``.
"""
from __future__ import annotations

import secrets
from typing import Any

import frappe
import openpyxl


def _gen_name() -> str:
    return secrets.token_hex(10)


def _to_float(v) -> float:
    if v is None or v == "":
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0


@frappe.whitelist()
def backfill_missing_ob_bins(
    company: str,
    batch_name: str,
    source_file: str | None = None,
    ob_date: str | None = None,
) -> dict[str, Any]:
    """Re-insert Bin + SLE for items missing in DB but present in source OB.

    Args:
      company: Company name
      batch_name: Misa Migration Batch (for source file discovery)
      source_file: Optional override path to ``Tong_hop_ton_kho.xlsx``
      ob_date: Opening posting date — defaults to ``2025-12-31``

    Returns:
      Summary dict.
    """
    if not company:
        frappe.throw(frappe._("Phải chọn Company."))
    abbr = frappe.db.get_value("Company", company, "abbr") or ""
    if not ob_date:
        ob_date = "2025-12-31"

    if not source_file:
        # Default convention
        import os
        bench = "/home/long/long/frappe-bench-dcnet"
        candidate = os.path.join(bench, "docs", "to_migrate", "1-2026",
                                 "Tong_hop_ton_kho.xlsx")
        if os.path.isfile(candidate):
            source_file = candidate
        else:
            frappe.throw(frappe._("source_file not specified."))

    wb = openpyxl.load_workbook(source_file, read_only=True, data_only=True)
    ws = wb.active
    inserted = 0
    skipped_no_item = 0
    skipped_no_wh = 0
    skipped_bin_exists = 0
    skipped_no_qty = 0
    voucher_no = f"OB-INV-BACKFILL-{batch_name}"
    now = frappe.utils.now()

    for row in list(ws.iter_rows(values_only=True))[5:]:
        if not row or len(row) < 54:
            continue
        wh_name = str(row[0] or "").strip()
        item_code = str(row[2] or "").strip()
        if not wh_name or not item_code:
            continue
        item_code = item_code.replace("<", "-").replace(">", "-")

        ob_qty = _to_float(row[7])
        ob_value = _to_float(row[9])
        if ob_qty <= 0:
            skipped_no_qty += 1
            continue

        if not frappe.db.exists("Item", item_code):
            skipped_no_item += 1
            continue
        db_wh = f"{wh_name} - {abbr}" if abbr else wh_name
        if not frappe.db.exists("Warehouse", db_wh):
            skipped_no_wh += 1
            continue
        # Bin existence check
        bin_existing = frappe.db.exists("Bin",
            {"warehouse": db_wh, "item_code": item_code})
        if bin_existing:
            skipped_bin_exists += 1
            continue

        # Create Bin
        bin_doc = frappe.new_doc("Bin")
        bin_doc.item_code = item_code
        bin_doc.warehouse = db_wh
        bin_doc.actual_qty = ob_qty
        bin_doc.stock_value = ob_value
        bin_doc.valuation_rate = round(ob_value / ob_qty, 4) if ob_qty > 0 else 0
        bin_doc.stock_uom = frappe.db.get_value("Item", item_code, "stock_uom") or "Nos"
        bin_doc.flags.ignore_permissions = True
        bin_doc.flags.ignore_mandatory = True
        bin_doc.insert()

        # Insert SLE
        sle_row = {
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": "Administrator", "modified_by": "Administrator",
            "docstatus": 1, "idx": 0,
            "item_code": item_code, "warehouse": db_wh,
            "posting_date": ob_date, "posting_time": "00:00:00",
            "posting_datetime": f"{ob_date} 00:00:00",
            "voucher_type": "Stock Reconciliation", "voucher_no": voucher_no,
            "actual_qty": ob_qty, "qty_after_transaction": ob_qty,
            "incoming_rate": round(ob_value / ob_qty, 4) if ob_qty > 0 else 0,
            "outgoing_rate": 0,
            "valuation_rate": round(ob_value / ob_qty, 4) if ob_qty > 0 else 0,
            "stock_value": ob_value, "stock_value_difference": ob_value,
            "stock_uom": bin_doc.stock_uom,
            "company": company,
            "fiscal_year": ob_date[:4],
            "is_cancelled": 0,
        }
        cols = ",".join(f"`{k}`" for k in sle_row.keys())
        ph = ",".join(["%s"] * len(sle_row))
        frappe.db.sql(
            f"INSERT INTO `tabStock Ledger Entry` ({cols}) VALUES ({ph})",
            tuple(sle_row.values()),
        )
        inserted += 1

    wb.close()
    frappe.db.commit()
    return {
        "inserted": inserted,
        "skipped_no_item": skipped_no_item,
        "skipped_no_wh": skipped_no_wh,
        "skipped_bin_exists": skipped_bin_exists,
        "skipped_no_qty": skipped_no_qty,
    }
