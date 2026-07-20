"""Snap DB Bin to source Tong_hop_ton_kho closing balance.

After bulk_pump + audit + per-voucher repost, residual Stock Entry routing
errors (wrong warehouse, missed transfer, mistyped destination) leave a
small set of (item, warehouse) Bins that don't match source's reported
period-end qty/value.

This script applies a Stock Reconciliation-style adjustment at period_end:
  1. For each (item, warehouse) in source where DB Bin ≠ source CB,
     compute the adjustment qty/value delta.
  2. Insert a single SLE row carrying the delta + update Bin to source values.
  3. Voucher type = ``Stock Reconciliation``, voucher_no = ``SNAP-<batch>``.

Use this ONLY when:
  - You've already run bulk_pump and audit-repost passes.
  - Remaining mismatches are < 10% and are residue of wrong-warehouse routing.
  - You accept lossy "snap to closing" semantics for archival migration.

Public entry: ``snap_bin_to_source_cb(company, batch_name, period_end)``.
"""
from __future__ import annotations

import os
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
def snap_bin_to_source_cb(
    company: str,
    batch_name: str,
    period_end: str,
    source_file: str | None = None,
) -> dict[str, Any]:
    if not company:
        frappe.throw(frappe._("Phải chọn Company."))
    abbr = frappe.db.get_value("Company", company, "abbr") or ""
    if not source_file:
        pe = period_end
        bench = "/home/long/long/frappe-bench-dcnet"
        candidate = os.path.join(bench, "docs", "to_migrate",
                                  f"{int(pe[5:7])}-{pe[:4]}",
                                  "Tong_hop_ton_kho.xlsx")
        if os.path.isfile(candidate):
            source_file = candidate
        else:
            frappe.throw(frappe._("source_file not found: {0}").format(candidate))

    wb = openpyxl.load_workbook(source_file, read_only=True, data_only=True)
    ws = wb.active
    adjusted = 0
    skipped_no_wh = 0
    skipped_no_item = 0
    skipped_matched = 0
    voucher_no = f"SNAP-{batch_name}"
    now = frappe.utils.now()

    # Aggregate source by (wh, item) — file may have multiple lots; sum
    src_map: dict[tuple, tuple] = {}
    for row in list(ws.iter_rows(values_only=True))[5:]:
        if not row or len(row) < 54:
            continue
        wh = str(row[0] or "").strip()
        it = str(row[2] or "").strip()
        if not wh or not it:
            continue
        it = it.replace("<", "-").replace(">", "-")
        q = _to_float(row[51])
        v = _to_float(row[53])
        key = (wh, it)
        prev_q, prev_v = src_map.get(key, (0.0, 0.0))
        src_map[key] = (prev_q + q, prev_v + v)
    wb.close()

    for (wh_name, item_code), (src_qty, src_value) in src_map.items():
        if not frappe.db.exists("Item", item_code):
            skipped_no_item += 1
            continue
        db_wh = f"{wh_name} - {abbr}" if abbr else wh_name
        if not frappe.db.exists("Warehouse", db_wh):
            skipped_no_wh += 1
            continue
        bin_row = frappe.db.sql(
            "SELECT name, actual_qty, stock_value FROM `tabBin` WHERE warehouse=%s AND item_code=%s",
            (db_wh, item_code), as_dict=True,
        )
        if bin_row:
            cur = bin_row[0]
            cur_qty = float(cur["actual_qty"] or 0)
            cur_val = float(cur["stock_value"] or 0)
            if abs(cur_qty - src_qty) < 0.01 and abs(cur_val - src_value) < 1:
                skipped_matched += 1
                continue
            delta_qty = src_qty - cur_qty
            delta_val = src_value - cur_val
            new_rate = round(src_value / src_qty, 4) if src_qty > 0 else 0
            frappe.db.sql(
                "UPDATE `tabBin` SET actual_qty=%s, stock_value=%s, valuation_rate=%s WHERE name=%s",
                (src_qty, src_value, new_rate, cur["name"]),
            )
        else:
            # No Bin — create one
            if src_qty <= 0:
                continue
            new_rate = round(src_value / src_qty, 4) if src_qty > 0 else 0
            stock_uom = frappe.db.get_value("Item", item_code, "stock_uom") or "Nos"
            bin_doc = frappe.new_doc("Bin")
            bin_doc.item_code = item_code
            bin_doc.warehouse = db_wh
            bin_doc.actual_qty = src_qty
            bin_doc.stock_value = src_value
            bin_doc.valuation_rate = new_rate
            bin_doc.stock_uom = stock_uom
            bin_doc.flags.ignore_permissions = True
            bin_doc.flags.ignore_mandatory = True
            bin_doc.insert()
            delta_qty = src_qty
            delta_val = src_value

        # Insert SLE for the adjustment
        sle = {
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": "Administrator", "modified_by": "Administrator",
            "docstatus": 1, "idx": 0,
            "item_code": item_code, "warehouse": db_wh,
            "posting_date": period_end, "posting_time": "23:59:59",
            "posting_datetime": f"{period_end} 23:59:59",
            "voucher_type": "Stock Reconciliation", "voucher_no": voucher_no,
            "actual_qty": delta_qty, "qty_after_transaction": src_qty,
            "incoming_rate": (round(delta_val / delta_qty, 4) if delta_qty > 0 else 0),
            "outgoing_rate": 0,
            "valuation_rate": round(src_value / src_qty, 4) if src_qty > 0 else 0,
            "stock_value": src_value, "stock_value_difference": delta_val,
            "stock_uom": frappe.db.get_value("Item", item_code, "stock_uom") or "Nos",
            "company": company,
            "fiscal_year": period_end[:4],
            "is_cancelled": 0,
        }
        cols = ",".join(f"`{k}`" for k in sle.keys())
        ph = ",".join(["%s"] * len(sle))
        frappe.db.sql(
            f"INSERT INTO `tabStock Ledger Entry` ({cols}) VALUES ({ph})",
            tuple(sle.values()),
        )
        adjusted += 1

    frappe.db.commit()
    return {
        "adjusted": adjusted,
        "skipped_matched": skipped_matched,
        "skipped_no_item": skipped_no_item,
        "skipped_no_wh": skipped_no_wh,
    }
