"""Phase 0 Opening Inventory — load Misa OB Inventory rows into ERPNext stock.

Misa OB Inventory file has one row per (item, warehouse) holding stock on the
OB date, with: Mã hàng, Mã kho, Số lượng tồn, Đơn giá, Giá trị tồn.

Output: ONE Material Receipt Stock Entry grouping all items, with N item
rows + N SLE rows. NO GL Entry — accounting is backed by OB Account Balance
(TK 156/152/153 totals are already in the Opening JE). This keeps the stock
ledger aligned to physical reality while letting the GL handle the value
side via the Equity offset.

Warehouse short-codes (KHO, KHOHN, KHODNG, THUHOI...) are resolved through
warehouse_resolver to the suffixed ERPNext Warehouse.name. Items not present
in tabItem are skipped (master must be installed first).
"""
from __future__ import annotations

import json
import secrets
from typing import Any

import frappe
from frappe.utils import getdate, now_datetime

from vn_accounting.misa_migration.bulk_pump import warehouse_resolver


def _gen_name() -> str:
    return secrets.token_hex(5)


def build_opening_inventory(
    batch_name: str,
    company: str,
    ob_date: str,
    posting_user: str = "Administrator",
) -> dict[str, list[dict]] | None:
    """Build SE + SED + SLE rows from Misa OB Inventory file_type."""
    now = frappe.utils.now()
    posting_time = "00:00:00"
    fiscal_year = ob_date[:4] if isinstance(ob_date, str) else str(getdate(ob_date).year)

    rows = frappe.db.sql(
        "SELECT raw_payload FROM `tabMisa Migration Row` "
        "WHERE batch=%s AND file_type='OB Inventory' "
        "AND status NOT IN ('Skipped','Failed','Invalid')",
        (batch_name,), as_dict=True,
    )
    payloads = []
    for r in rows:
        try:
            payloads.append(json.loads(r["raw_payload"] or "{}"))
        except (TypeError, ValueError):
            pass
    if not payloads:
        return None

    # Warm warehouse cache + build a Misa-short-code → ERPNext-name map.
    warehouse_resolver.warm_cache(company)
    wh_map = _build_misa_warehouse_map(company)

    # Item existence cache (skip rows for items not yet imported)
    item_cache: dict[str, str | None] = {}

    def _resolve_item(code: str) -> str | None:
        if code in item_cache:
            return item_cache[code]
        nm = frappe.db.get_value("Item", code, "name")
        item_cache[code] = nm
        return nm

    # Aggregate per (item, warehouse) — sum qty/value across multiple OB
    # lot rows (Misa may export same item in 2 entries with different lots).
    by_pair: dict[tuple[str, str], dict] = {}
    skipped = {"no_item": 0, "no_wh": 0, "no_qty": 0}

    def _to_float(v) -> float:
        """Best-effort numeric coerce. Tong_hop_ton_kho parser sometimes
        keeps the sub-header row ('Số lượng' / 'Giá trị') as a data row;
        coercing those textual values to float raises — return 0."""
        if v is None or v == "":
            return 0.0
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0.0

    for p in payloads:
        item_code = (p.get("Mã hàng") or "").strip()
        misa_wh = (p.get("Mã kho") or "").strip()
        # Two source layouts:
        #   - Misa-native OB Inventory: 'Số lượng tồn' / 'Giá trị tồn'
        #   - "Tong_hop_ton_kho" aggregated workbook: 'Đầu kỳ' (OB qty,
        #     main-header column) + '_col_9' (OB value, third sub-column
        #     under 'Đầu kỳ').
        qty = (
            _to_float(p.get("Số lượng tồn"))
            or _to_float(p.get("Đầu kỳ"))
        )
        value = (
            _to_float(p.get("Giá trị tồn"))
            or _to_float(p.get("_col_9"))
        )
        rate = float(p.get("Đơn giá") or 0) or (value / qty if qty > 0 else 0)
        uom = (p.get("ĐVT") or "Nos").strip()

        if not item_code or not _resolve_item(item_code):
            skipped["no_item"] += 1; continue
        wh_full = wh_map.get(misa_wh) or warehouse_resolver.resolve(misa_wh, company)
        if not wh_full:
            skipped["no_wh"] += 1; continue
        if qty <= 0:
            skipped["no_qty"] += 1; continue

        key = (item_code, wh_full)
        cur = by_pair.get(key) or {"qty": 0.0, "value": 0.0, "uom": uom, "item_code": item_code, "warehouse": wh_full}
        cur["qty"] += qty
        cur["value"] += value
        # Last-write rate (good enough for OB; weighted-avg would be cleaner)
        if qty > 0: cur["rate"] = (cur["rate"] if "rate" in cur else 0) + rate * (qty)
        cur["uom"] = uom
        by_pair[key] = cur

    if not by_pair:
        return None

    voucher_no = f"OB-INV-{batch_name}"
    se_details: list[dict] = []
    sle_rows: list[dict] = []
    total_amount = 0.0
    sle_state: dict[tuple, dict] = {}  # (item, wh) → cumulative

    for idx, ((item_code, wh_full), agg) in enumerate(by_pair.items()):
        qty = agg["qty"]
        value = agg["value"]
        # Re-derive weighted rate
        rate = round(value / qty, 4) if qty > 0 else 0
        uom = agg["uom"]
        if not frappe.db.exists("UOM", uom):
            uom = "Nos"

        # SE Detail (incoming — t_warehouse only). Include `s_warehouse: None`
        # explicitly so the bulk_insert column-union still covers it when this
        # builder runs FIRST and the later Material Issue / Transfer rows
        # depend on the same column being present in the INSERT statement.
        se_details.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "item_code": item_code,
            "item_name": frappe.db.get_value("Item", item_code, "item_name") or item_code,
            "qty": qty, "transfer_qty": qty,
            "uom": uom, "stock_uom": uom, "conversion_factor": 1,
            "s_warehouse": None, "t_warehouse": wh_full,
            "basic_rate": rate, "valuation_rate": rate,
            "basic_amount": value, "amount": value,
            "use_serial_batch_fields": 1,
            "parent": voucher_no,
            "parenttype": "Stock Entry",
            "parentfield": "items",
        })
        total_amount += value

        # SLE row (incoming)
        sle_state[(item_code, wh_full)] = {"qty": qty, "value": value}
        sle_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "item_code": item_code, "warehouse": wh_full,
            "posting_date": ob_date, "posting_time": posting_time,
            "posting_datetime": now_datetime(),
            "voucher_type": "Stock Entry", "voucher_no": voucher_no,
            "actual_qty": qty, "qty_after_transaction": qty,
            "incoming_rate": rate, "outgoing_rate": 0,
            "valuation_rate": rate,
            "stock_value": value, "stock_value_difference": value,
            "stock_uom": uom,
            "company": company, "fiscal_year": fiscal_year,
            "is_cancelled": 0,
        })

    # Stock Entry parent
    se_row = {
        "name": voucher_no,
        "creation": now, "modified": now,
        "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "stock_entry_type": "Material Receipt",
        "purpose": "Material Receipt",
        "posting_date": ob_date, "posting_time": posting_time,
        "set_posting_time": 1,
        "is_opening": "Yes",
        "total_outgoing_value": 0,
        "total_incoming_value": total_amount,
        "value_difference": total_amount,
        "total_amount": total_amount,
        "remarks": "Opening Inventory (bulk_pump)",
        "misa_voucher_no": voucher_no,
    }

    print(f"[opening_inventory] {len(by_pair)} (item,warehouse) pairs, "
          f"total value={total_amount:,.0f} VND. Skipped: "
          f"no_item={skipped['no_item']} no_wh={skipped['no_wh']} "
          f"no_qty={skipped['no_qty']}", flush=True)

    return {
        "Stock Entry": [se_row],
        "Stock Entry Detail": se_details,
        "Stock Ledger Entry": sle_rows,
    }


def _build_misa_warehouse_map(company: str) -> dict[str, str]:
    """Map Misa-style short warehouse codes (KHO, KHOHN, THUHOI...) to ERPNext
    Warehouse.name. Uses heuristic matching against the warehouse name's
    first word or last word."""
    out: dict[str, str] = {}
    wh_rows = frappe.db.sql(
        "SELECT name FROM `tabWarehouse` WHERE company=%s", (company,), as_dict=True)
    # Common Misa short → keyword mappings
    keyword_map = {
        "KHO": "CÔNG TY", "KHOCT": "CÔNG TY",
        "KHOHN": "HÀ NỘI", "KHN": "HÀ NỘI",
        "KHODNG": "ĐÀ NẴNG", "KDN": "ĐÀ NẴNG",
        "KHOHCM": "CÔNG TY",
        "KHOBD": "BÌNH DƯƠNG",
        "KHOVT": "VŨNG TÀU",
        "THUHOI": "THU HỒI",
        "KHOCC": "CÔNG CỤ",
        "KHOTP": "THÀNH PHẨM",
        "KHONOC": "NOC",
        "KHONVL": "NGUYÊN VẬT LIỆU",
        "KHOKHD": "VẬT TƯ KHĐ",
    }
    for short, keyword in keyword_map.items():
        for r in wh_rows:
            if keyword in r["name"]:
                out[short] = r["name"]
                break
    # Direct passthrough for already-suffixed names
    for r in wh_rows:
        out[r["name"]] = r["name"]
    return out
