"""PX / PXHN / PNHN → Stock Entry handler.

Phase D commit 12 + Phase E SCT integration. Misa internal stock vouchers:

| Prefix | Misa name             | ERPNext stock_entry_type | Warehouse fields  |
|--------|-----------------------|--------------------------|-------------------|
| PX     | Phiếu xuất bán        | Material Issue           | s_warehouse only  |
| PXHN   | Phiếu xuất kho nội bộ | Material Transfer        | s_warehouse + t_warehouse |
| PNHN   | Phiếu nhập kho nội bộ | Material Receipt         | t_warehouse only  |

When the SCT (Sổ chi tiết vật tư hàng hóa) file has been parsed for
the current batch, ``context.get_sct_voucher(voucher_no)`` returns the
real item-level breakdown — we emit ONE Stock Entry row per real item
line (with the actual item_code, warehouse, qty, rate). Items and
warehouses that don't yet exist are stub-created via
``_ensure_item_stub`` / ``_ensure_warehouse_for_misa_name``.

Backwards-compat fallback: when no SCT data is loaded (legacy batches
or pure-NKC import), we fall back to the placeholder MISA-MIGRATION-
STOCK Item with a synthesized row built from NKC totals — same
behavior as before the Phase E SCT work.

Per `~/.claude/rules/erpnext-stock-payroll.md`:
- Use `use_serial_batch_fields=1` on every row to skip Serial/Batch
  Bundle creation.
- Company `stock_adjustment_account` must be set; we fall back to first
  Account named like '632*' if absent and short-circuit-fail otherwise.
"""

from __future__ import annotations

from typing import Any

import frappe

from vn_accounting.misa_migration.context import (
    get_active_company as _get_company,
    get_sct_voucher as _get_sct_voucher,
)

from vn_accounting.misa_migration.importers.nkc_handlers.purchase_receipt import (
    _company_default_warehouse,
)
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    _ensure_placeholder_item,
    _ensure_placeholder_stock_item,
)


# Cache resolved warehouse names per (company, misa_name) — avoids
# repeated DB queries during a single Phase 4 run.
_WAREHOUSE_CACHE: dict[tuple[str, str], str] = {}
_ITEM_CACHE: dict[str, str] = {}


def reset_se_perf_caches() -> None:
    """Clear caches between Phase 4 runs (called by orchestrator
    when reset_perf_caches() fires).
    """
    _WAREHOUSE_CACHE.clear()
    _ITEM_CACHE.clear()


def bulk_warm_items_from_sct(
    sct_voucher_map: dict[str, dict],
    company: str,
) -> dict[str, int]:
    """PERF (Tier 1.4) — pre-warm _ITEM_CACHE before the voucher loop.

    Walks every SCT voucher's items, collects unique item_codes, runs
    a SINGLE bulk SELECT to populate ``_ITEM_CACHE`` with already-present
    Items (skipping per-row ``frappe.db.exists`` round-trips). Then,
    for the codes still missing, pre-creates them via the existing
    ``_ensure_item_stub`` path — amortizing item creation up-front so
    the voucher loop sees a fully warm cache.

    NOTE on the deviation from the original plan:
        The plan specified ``frappe.db.bulk_insert("Item", rows)`` for
        the missing-Items branch. ``tabItem`` has ~40 NOT NULL columns
        whose set changes between ERPNext versions; building a complete
        raw-column dict is fragile (a single missing required column
        breaks every Phase 4 run on the next bench upgrade). Using
        ``_ensure_item_stub`` per missing item still gives the cache-warm
        win (the dominant cost was the per-row ``exists`` queries, not
        the rare insert) and stays safe across ERPNext upgrades.

    Returns ``{"considered", "already_cached", "found_existing", "created", "failed"}``.
    """
    if not sct_voucher_map:
        return {"considered": 0, "already_cached": 0, "found_existing": 0,
                "created": 0, "failed": 0}

    seen: dict[str, tuple[str | None, str | None, str | None, float]] = {}
    for voucher in sct_voucher_map.values():
        for line in (voucher.get("items") or []):
            code = (line.get("item_code") or "").strip()
            if not code or code in seen:
                continue
            seen[code] = (
                line.get("item_name"),
                line.get("uom") or line.get("primary_uom"),
                line.get("item_group_name") or line.get("item_group"),
                float(line.get("rate") or 0.0),
            )

    considered = len(seen)
    if not considered:
        return {"considered": 0, "already_cached": 0, "found_existing": 0,
                "created": 0, "failed": 0}

    already_cached = sum(1 for code in seen if code in _ITEM_CACHE)
    to_query = [code for code in seen if code not in _ITEM_CACHE]

    # SINGLE bulk SELECT: replaces N per-row frappe.db.exists round-trips.
    # On a typical Phase 4 batch with ~500 unique items this is a >10x
    # round-trip reduction.
    found_existing = 0
    if to_query:
        # Chunk to keep the IN list bounded; mariadb max packet keeps
        # us safe up to ~10k IDs at once but 1k chunks keep logs sane.
        for i in range(0, len(to_query), 1000):
            chunk = to_query[i:i + 1000]
            rows = frappe.db.sql(
                "SELECT name FROM `tabItem` WHERE name IN %(names)s",
                {"names": tuple(chunk)},
            )
            for (name,) in rows:
                _ITEM_CACHE[name] = name
                found_existing += 1

    # Items still missing → create via the established stub path (safe
    # against ERPNext schema drift; cost amortizes upfront so the voucher
    # loop later hits cache only).
    created = 0
    failed = 0
    still_missing = [code for code in to_query if code not in _ITEM_CACHE]
    for code in still_missing:
        item_name, uom, group, rate = seen[code]
        result = _ensure_item_stub(
            item_code=code,
            item_name=item_name,
            uom=uom,
            item_group_name=group,
            rate=rate,
            company=company,
        )
        if result:
            created += 1
        else:
            failed += 1

    # Commit the stub batch in one go so workers re-running the same
    # SCT later (recovery scenarios) hit cached rows.
    try:
        frappe.db.commit()
    except Exception:
        pass

    return {
        "considered": considered,
        "already_cached": already_cached,
        "found_existing": found_existing,
        "created": created,
        "failed": failed,
    }


def _ensure_warehouse_for_misa_name(misa_warehouse: str | None, company: str) -> str | None:
    """Resolve a Misa "Tên kho" / "Mã kho" to a Frappe Warehouse name.

    Strategy (in order):
      1. Cache hit (same company + misa_warehouse).
      2. Exact match on Warehouse.warehouse_name within the Company.
      3. Substring match (case-insensitive) on Warehouse.warehouse_name.
      4. Stub-create a new leaf Warehouse under the Company root.
    Returns None if no Warehouse exists for the Company at all (caller
    falls back to company default).
    """
    if not misa_warehouse:
        return None
    key = (company, misa_warehouse)
    if key in _WAREHOUSE_CACHE:
        return _WAREHOUSE_CACHE[key]

    # Exact match
    name = frappe.db.get_value(
        "Warehouse",
        {"company": company, "warehouse_name": misa_warehouse, "is_group": 0},
        "name",
    )
    if name:
        _WAREHOUSE_CACHE[key] = name
        return name
    # Case-insensitive partial match
    candidates = frappe.db.sql(
        """SELECT name FROM `tabWarehouse`
           WHERE company=%s AND is_group=0 AND disabled=0
             AND LOWER(warehouse_name) LIKE LOWER(%s)
           LIMIT 1""",
        (company, f"%{misa_warehouse}%"),
    )
    if candidates:
        _WAREHOUSE_CACHE[key] = candidates[0][0]
        return candidates[0][0]
    # Stub-create
    try:
        parent = frappe.db.get_value(
            "Warehouse",
            {"company": company, "is_group": 1, "parent_warehouse": ""},
            "name",
        ) or frappe.db.get_value(
            "Warehouse", {"company": company, "is_group": 1}, "name",
        )
        doc = frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": misa_warehouse,
            "company": company,
            "is_group": 0,
            "parent_warehouse": parent,
        })
        doc.flags.ignore_permissions = True
        doc.insert()
        _WAREHOUSE_CACHE[key] = doc.name
        return doc.name
    except Exception as exc:
        frappe.log_error(
            title=f"Misa Warehouse stub failed: {misa_warehouse}",
            message=f"{type(exc).__name__}: {exc}",
        )
        return None


def _ensure_item_stub(
    item_code: str,
    item_name: str | None,
    uom: str | None,
    item_group_name: str | None,
    rate: float,
    company: str,
) -> str | None:
    """Resolve / stub-create a Misa Item code as a Frappe Item.

    Strategy:
      1. Cache hit on item_code.
      2. Existing Item with same name.
      3. Stub-create with stock_uom + valuation rate + sane defaults.

    Returns the Item.name (== item_code) or None on failure.
    """
    if not item_code:
        return None
    cached = _ITEM_CACHE.get(item_code)
    if cached:
        return cached
    if frappe.db.exists("Item", item_code):
        # Stock Entries require is_stock_item=1. Some Items were created
        # earlier as services/non-stock by other modules; upgrade them
        # in-place when SE needs them as stock.
        is_stock = frappe.db.get_value("Item", item_code, "is_stock_item")
        if not is_stock:
            frappe.db.set_value("Item", item_code, "is_stock_item", 1,
                                update_modified=False)
        _ITEM_CACHE[item_code] = item_code
        return item_code
    # Resolve UOM — must exist in tabUOM. Fallback chain: provided →
    # primary uom from SCT → "Nos" → first UOM in system.
    resolved_uom = uom or "Nos"
    if not frappe.db.exists("UOM", resolved_uom):
        if frappe.db.exists("UOM", "Nos"):
            resolved_uom = "Nos"
        else:
            resolved_uom = frappe.db.get_value("UOM", {}, "name") or "Nos"
            if not frappe.db.exists("UOM", resolved_uom):
                # Create "Nos" as last resort
                try:
                    frappe.get_doc({
                        "doctype": "UOM", "uom_name": "Nos",
                    }).insert(ignore_permissions=True)
                    resolved_uom = "Nos"
                except Exception:
                    return None
    # Resolve Item Group — must exist. Fallback: "All Item Groups"
    resolved_group = item_group_name or "All Item Groups"
    if not frappe.db.exists("Item Group", resolved_group):
        resolved_group = "All Item Groups"
        if not frappe.db.exists("Item Group", resolved_group):
            resolved_group = frappe.db.get_value(
                "Item Group", {"is_group": 0}, "name",
            ) or "All Item Groups"
    try:
        doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": (item_name or item_code)[:140],
            "stock_uom": resolved_uom,
            "item_group": resolved_group,
            "is_stock_item": 1,
            "include_item_in_manufacturing": 0,
            "valuation_rate": float(rate) if rate else 0.0,
        })
        doc.flags.ignore_permissions = True
        doc.insert(set_name=item_code)
        _ITEM_CACHE[item_code] = doc.name
        return doc.name
    except Exception as exc:
        frappe.log_error(
            title=f"Misa Item stub failed: {item_code}",
            message=f"{type(exc).__name__}: {exc}",
        )
        return None


# Prefix → (stock_entry_type, needs_source, needs_target)
_SE_TYPE_BY_PREFIX: dict[str, tuple[str, bool, bool]] = {
    "PX":   ("Material Issue",    True,  False),
    "PXHN": ("Material Transfer", True,  True),
    "PNHN": ("Material Receipt",  False, True),
}


def _alt_warehouse_for_transfer(
    company: str, primary: str | None,
) -> str | None:
    """Pick a second warehouse different from `primary` (for Material Transfer).

    Returns None if only one warehouse exists — caller must short-circuit.
    """
    if not primary:
        return None
    candidates = frappe.db.get_all(
        "Warehouse",
        filters={"company": company, "is_group": 0, "disabled": 0},
        fields=["name"],
        order_by="creation",
        limit=10,
    )
    for w in candidates:
        if w["name"] != primary:
            return w["name"]
    return None


def _ensure_stock_adjustment_account(company: str) -> str | None:
    """Return Company.stock_adjustment_account, falling back to TK 632.

    On first call may set the company field if absent (saves repeated
    fallback lookups across many SEs).
    """
    acct = frappe.db.get_value("Company", company, "stock_adjustment_account")
    if acct:
        return acct
    candidate = frappe.db.get_value(
        "Account",
        {"company": company, "account_number": "632", "is_group": 0},
        "name",
    )
    if not candidate:
        return None
    frappe.db.set_value(
        "Company", company, "stock_adjustment_account", candidate,
        update_modified=False,
    )
    return candidate


def _build_rows_from_sct(
    sct_voucher: dict[str, Any],
    stock_entry_type: str,
    company: str,
    primary_wh: str,
    fallback_target_wh: str | None,
) -> list[dict[str, Any]]:
    """Build SE item rows from real SCT item lines for a voucher.

    For Material Issue (PX): one row per line with qty_out > 0,
        s_warehouse = resolved Misa warehouse name, no t_warehouse.

    For Material Receipt (PNHN / PN): one row per line with qty_in > 0,
        t_warehouse = resolved warehouse name, no s_warehouse.

    For Material Transfer (PXHN / CK02): SCT emits TWO lines per item
        (one with qty_out > 0 at source, one with qty_in > 0 at target).
        We PAIR by item_code: each pair → one row with both s_/t_warehouse.
        Unpaired lines (only qty_out OR only qty_in for an item) fall
        through as their respective single-warehouse type.
    """
    lines = sct_voucher.get("lines") or []

    if stock_entry_type == "Material Issue":
        rows = []
        for ln in lines:
            qty = float(ln.get("qty_out") or 0.0)
            if qty <= 0:
                continue
            item_code = _ensure_item_stub(
                ln.get("item_code"), ln.get("item_name"),
                ln.get("uom"), ln.get("item_group_name"),
                ln.get("rate") or 0.0, company,
            )
            if not item_code:
                continue
            s_wh = _ensure_warehouse_for_misa_name(
                ln.get("warehouse_name") or ln.get("warehouse_code"),
                company,
            ) or primary_wh
            rate = float(ln.get("rate") or 0.0)
            rows.append({
                "item_code": item_code,
                "qty": qty,
                "uom": ln.get("uom") or "Nos",
                "stock_uom": ln.get("uom") or "Nos",
                "conversion_factor": 1,
                "use_serial_batch_fields": 1,
                "allow_zero_valuation_rate": 1,
                "basic_rate": rate if rate > 0 else 1.0,
                "s_warehouse": s_wh,
                "description": ln.get("item_name") or item_code,
            })
        return rows

    if stock_entry_type == "Material Receipt":
        rows = []
        for ln in lines:
            qty = float(ln.get("qty_in") or 0.0)
            if qty <= 0:
                continue
            item_code = _ensure_item_stub(
                ln.get("item_code"), ln.get("item_name"),
                ln.get("uom"), ln.get("item_group_name"),
                ln.get("rate") or 0.0, company,
            )
            if not item_code:
                continue
            t_wh = _ensure_warehouse_for_misa_name(
                ln.get("warehouse_name") or ln.get("warehouse_code"),
                company,
            ) or primary_wh
            rate = float(ln.get("rate") or 0.0)
            rows.append({
                "item_code": item_code,
                "qty": qty,
                "uom": ln.get("uom") or "Nos",
                "stock_uom": ln.get("uom") or "Nos",
                "conversion_factor": 1,
                "use_serial_batch_fields": 1,
                "allow_zero_valuation_rate": 1,
                "basic_rate": rate if rate > 0 else 1.0,
                "t_warehouse": t_wh,
                "description": ln.get("item_name") or item_code,
            })
        return rows

    # Material Transfer — pair source(qty_out) + target(qty_in) per item_code
    sources: dict[str, dict] = {}
    targets: dict[str, dict] = {}
    for ln in lines:
        ic = ln.get("item_code")
        if not ic:
            continue
        if (ln.get("qty_out") or 0) > 0 and ic not in sources:
            sources[ic] = ln
        if (ln.get("qty_in") or 0) > 0 and ic not in targets:
            targets[ic] = ln

    rows = []
    seen = set()
    for ic, src in sources.items():
        tgt = targets.get(ic)
        item_code = _ensure_item_stub(
            ic, src.get("item_name"), src.get("uom"),
            src.get("item_group_name"), src.get("rate") or 0.0, company,
        )
        if not item_code:
            continue
        s_wh = _ensure_warehouse_for_misa_name(
            src.get("warehouse_name") or src.get("warehouse_code"), company,
        ) or primary_wh
        t_wh = _ensure_warehouse_for_misa_name(
            (tgt or {}).get("warehouse_name") or (tgt or {}).get("warehouse_code"),
            company,
        ) or fallback_target_wh or primary_wh
        if t_wh == s_wh and fallback_target_wh and fallback_target_wh != s_wh:
            t_wh = fallback_target_wh
        qty = float(src.get("qty_out") or 0.0)
        rate = float(src.get("rate") or 0.0)
        rows.append({
            "item_code": item_code,
            "qty": qty,
            "uom": src.get("uom") or "Nos",
            "stock_uom": src.get("uom") or "Nos",
            "conversion_factor": 1,
            "use_serial_batch_fields": 1,
            "allow_zero_valuation_rate": 1,
            "basic_rate": rate if rate > 0 else 1.0,
            "s_warehouse": s_wh,
            "t_warehouse": t_wh,
            "description": src.get("item_name") or item_code,
        })
        seen.add(ic)
    # Unpaired target-only items (qty_in with no qty_out) — receipt-style
    for ic, tgt in targets.items():
        if ic in seen:
            continue
        item_code = _ensure_item_stub(
            ic, tgt.get("item_name"), tgt.get("uom"),
            tgt.get("item_group_name"), tgt.get("rate") or 0.0, company,
        )
        if not item_code:
            continue
        t_wh = _ensure_warehouse_for_misa_name(
            tgt.get("warehouse_name") or tgt.get("warehouse_code"),
            company,
        ) or fallback_target_wh or primary_wh
        qty = float(tgt.get("qty_in") or 0.0)
        rate = float(tgt.get("rate") or 0.0)
        rows.append({
            "item_code": item_code,
            "qty": qty,
            "uom": tgt.get("uom") or "Nos",
            "stock_uom": tgt.get("uom") or "Nos",
            "conversion_factor": 1,
            "use_serial_batch_fields": 1,
            "allow_zero_valuation_rate": 1,
            "basic_rate": rate if rate > 0 else 1.0,
            "t_warehouse": t_wh,
            "description": tgt.get("item_name") or item_code,
        })
    return rows


def _create_se(
    voucher: dict[str, Any],
    prefix: str,
) -> dict[str, Any]:
    """Shared Stock Entry creation for PX/PXHN/PNHN.

    Phase E: when an SCT (Sổ chi tiết) lookup matches voucher_no, build
    rows from real item-line data. Otherwise fall back to legacy
    placeholder Item synthesis from NKC totals.
    """
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}

    existing_docstatus = frappe.db.get_value(
        "Stock Entry", voucher_no, "docstatus"
    )
    if existing_docstatus in (0, 1):
        return {"status": "skipped", "target_name": voucher_no,
                "target_doctype": "Stock Entry",
                "reason": "already_exists"}
    if existing_docstatus == 2:
        return {"status": "failed", "target_name": voucher_no,
                "target_doctype": "Stock Entry",
                "error": f"{voucher_no} exists as cancelled (docstatus=2). "
                         "Delete it before re-running migration."}

    spec = _SE_TYPE_BY_PREFIX.get(prefix)
    if not spec:
        return {"status": "failed",
                "error": f"Unknown SE prefix {prefix!r}"}
    stock_entry_type, needs_source, needs_target = spec

    company = _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    stock_adj = _ensure_stock_adjustment_account(company)
    if not stock_adj:
        return {"status": "failed",
                "error": f"Company {company!r} has no stock_adjustment_account "
                         "and TK 632 not found in CoA"}

    primary_wh = _company_default_warehouse(company)
    if not primary_wh:
        return {"status": "failed",
                "error": f"No active warehouse on company {company!r}"}

    # ===== Phase E path: real items from SCT =====
    sct = _get_sct_voucher(voucher_no)
    items_payload: list[dict[str, Any]]
    sct_used = False
    fallback_target_wh = None
    if needs_target and not needs_source:
        # PNHN — target only
        pass
    elif stock_entry_type == "Material Transfer":
        fallback_target_wh = _alt_warehouse_for_transfer(company, primary_wh)

    if sct and sct.get("lines"):
        items_payload = _build_rows_from_sct(
            sct, stock_entry_type, company, primary_wh, fallback_target_wh,
        )
        if items_payload:
            sct_used = True
        else:
            items_payload = []  # will fall through to placeholder

    # ===== Legacy fallback: placeholder item from NKC totals =====
    if not sct_used:
        total_qty_amount = 0.0
        for leg in (voucher.get("legs") or []):
            debit = float(leg.get("debit") or 0.0)
            credit = float(leg.get("credit") or 0.0)
            total_qty_amount += max(debit, credit)
        if total_qty_amount > 0 and len(voucher.get("legs") or []) >= 2:
            total_qty_amount = total_qty_amount / 2
        placeholder_item = _ensure_placeholder_stock_item(company)
        basic_rate = total_qty_amount if total_qty_amount > 0 else 1.0

        source_wh = primary_wh if needs_source else None
        target_wh = primary_wh if needs_target else None
        if stock_entry_type == "Material Transfer":
            if not fallback_target_wh:
                return {"status": "failed",
                        "error": "Material Transfer needs ≥2 warehouses; "
                                 f"company {company!r} has only one"}
            target_wh = fallback_target_wh

        row: dict[str, Any] = {
            "item_code": placeholder_item,
            "qty": 1.0,
            "basic_rate": basic_rate,
            "uom": "Nos",
            "stock_uom": "Nos",
            "conversion_factor": 1,
            "use_serial_batch_fields": 1,
            "allow_zero_valuation_rate": 1,
            "description": voucher.get("voucher_remark") or voucher_no,
        }
        if source_wh:
            row["s_warehouse"] = source_wh
        if target_wh:
            row["t_warehouse"] = target_wh
        items_payload = [row]

    if not items_payload:
        return {"status": "failed",
                "error": f"{voucher_no}: SCT lookup empty + no NKC legs"}

    # Derive payload-level warehouses from items_payload (use first row)
    first_s_wh = next((r.get("s_warehouse") for r in items_payload if r.get("s_warehouse")), None)
    first_t_wh = next((r.get("t_warehouse") for r in items_payload if r.get("t_warehouse")), None)

    payload = {
        "doctype": "Stock Entry",
        "stock_entry_type": stock_entry_type,
        # FIX (Tier 1.2 follow-up): with ignore_links=True, ERPNext's
        # fetch_from='stock_entry_type.purpose' never fires, so
        # validate_warehouse() sees purpose=None and the Material-Receipt
        # branch (which clears item.s_warehouse) is skipped. Set purpose
        # explicitly — for the prefixes we handle, purpose == stock_entry_type.
        "purpose": stock_entry_type,
        "company": company,
        "posting_date": voucher.get("posting_date"),
        "set_posting_time": 1,
        "remarks": voucher.get("voucher_remark") or voucher_no,
        "items": items_payload,
        "misa_voucher_no": voucher_no,
    }
    if needs_source and first_s_wh:
        payload["from_warehouse"] = first_s_wh
    if needs_target and first_t_wh:
        payload["to_warehouse"] = first_t_wh

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight + SCT stub-creator already validated
        # Item / Warehouse links; skip ERPNext's per-row Link integrity
        # check.
        doc.flags.ignore_links = True
        doc.insert(set_name=voucher_no)
        return {
            "status": "created",
            "target_name": doc.name,
            "target_doctype": "Stock Entry",
            "stock_entry_type": stock_entry_type,
            "source_warehouse": first_s_wh,
            "target_warehouse": first_t_wh,
            "prefix_handled": prefix,
            "sct_used": sct_used,
            "line_count": len(items_payload),
        }
    except Exception as exc:
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(title=f"Misa SE create failed: {voucher_no}",
                         message=err)
        return {"status": "failed", "target_name": None, "error": err}


# ----------------------------------------------------------- public entry points

def create_se_from_px(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """PX (Phiếu xuất bán) → Material Issue Stock Entry."""
    return _create_se(voucher, "PX")


def create_se_from_pxhn(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """PXHN (Phiếu xuất kho nội bộ) → Material Transfer Stock Entry."""
    return _create_se(voucher, "PXHN")


def create_se_from_pnhn(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """PNHN (Phiếu nhập kho nội bộ) → Material Receipt Stock Entry."""
    return _create_se(voucher, "PNHN")
