"""PN (Phiếu nhập kho) → Purchase Invoice with update_stock=1.

Phase D commit 11. Misa PN vouchers credit 331 (supplier payable) and
debit 156* inventory directly — i.e. they're combined invoice + receipt
in one document. ERPNext models this natively via Purchase Invoice with
`update_stock=1`: the PI submits its own Stock Ledger Entries, so a
separate Purchase Receipt doc is unnecessary.

Spec §4 Phase 4 originally wrote "PN → PI + PR (update_stock=1); PR
doc.name = <voucher_no>-PR". Implementation choice: single PI with
update_stock=1 satisfies the spec INTENT (stock + AP posted under one
voucher) without the doc-count overhead of a sibling PR. The PI gets
doc.name = Misa PN voucher_no directly; no -PR doc is created. If a
downstream report demands an explicit Purchase Receipt sibling we can
revisit in Phase E.

Implementation reuses purchase_invoice helpers
(extract_line_expense_accounts, _load_account_mapping, _resolve_account)
+ the SI placeholder Item.
"""

from __future__ import annotations

import json
from typing import Any

import frappe


from vn_accounting.misa_migration.context import (
    get_active_company as _get_company,
)
from vn_accounting.misa_migration.importers import vat_extractor
from vn_accounting.misa_migration.importers.nkc_handlers.purchase_invoice import (
    _PI_INPUT_VAT_PREFIXES,
    _load_account_mapping,
    _resolve_account,
    extract_line_expense_accounts,
)
from vn_accounting.misa_migration.importers.nkc_handlers.sales_invoice import (
    PLACEHOLDER_ITEM_CODE,
    _ensure_placeholder_item,
)
# _ensure_placeholder_stock_item is lazy-imported inside _create_pi_pr_from_pn
# below to avoid the circular import (stock_entry.py imports from here).


def _company_default_warehouse(company: str) -> str | None:
    """Pick a warehouse to receive PN stock into.

    Strategy (order matters — ERPNext's PI controller has a real bug):
      1. First non-group, active, non-disabled Warehouse WITH non-empty
         ``Warehouse.account``.
      2. Any active non-group Warehouse, with ``account`` auto-filled
         to ``Company.default_inventory_account`` if missing.

    Why: ERPNext purchase_invoice.set_expense_account at line 489 does
    ``_inv_dict["account"]`` (no .get()). When the PN's warehouse isn't
    in the inventory_account_map, _inv_dict is empty → KeyError
    crashes the whole insert. Picking a warehouse that has ``account``
    set guarantees the map lookup succeeds.

    DCNET TEST T1/2025 hit this on 484 PN vouchers: the oldest
    Warehouse (returned by the original order_by='creation') happened
    to be KHO VŨNG TÀU which lacked ``account``.
    """
    # First try: any warehouse with explicit account
    wh = frappe.db.sql(
        """SELECT name FROM `tabWarehouse`
           WHERE company=%s AND is_group=0 AND disabled=0
             AND IFNULL(account, '') != ''
           ORDER BY creation LIMIT 1""",
        (company,),
    )
    if wh:
        return wh[0][0]

    # Fallback: pick any warehouse + auto-fill its account from Company
    # default so the ERPNext map lookup still succeeds. Persist the
    # change so subsequent PN vouchers reuse it.
    fallback = frappe.db.get_value(
        "Warehouse", {"company": company, "is_group": 0, "disabled": 0}, "name"
    )
    if fallback:
        default_acct = frappe.db.get_value(
            "Company", company, "default_inventory_account"
        )
        if default_acct:
            frappe.db.set_value(
                "Warehouse", fallback, "account", default_acct,
                update_modified=False,
            )
    return fallback


def create_pi_pr_from_pn(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """PN → Purchase Invoice with update_stock=1.

    Returns target_doctype='Purchase Invoice' (no separate PR doc). The
    'pr_target_name' field is None for v1; reserved for Phase E if a
    sibling PR doc is added.
    """
    voucher_no = voucher.get("voucher_no", "")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}

    if frappe.db.exists("Purchase Invoice", voucher_no):
        return {"status": "skipped", "target_name": voucher_no,
                "target_doctype": "Purchase Invoice",
                "reason": "already_exists"}

    party_code = voucher.get("party_code") or ""
    if not party_code:
        return {"status": "failed",
                "error": f"voucher {voucher_no} missing party_code"}
    # PERF (Tier 1.5): set-lookup vs per-call DB round-trip
    from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache
    if not _party_cache.is_supplier(party_code):
        return {"status": "failed",
                "error": f"Supplier {party_code!r} not found — run Phase 3 first"}

    company = _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    warehouse = _company_default_warehouse(company)
    if not warehouse:
        return {"status": "failed",
                "error": f"No active non-group warehouse on company {company!r}"}

    mapping = _load_account_mapping()

    # Bảng kê MV line items — synthesize 1 line if missing
    line_items: list[dict[str, Any]] = []
    if invoice and invoice.get("line_items"):
        line_items = list(invoice["line_items"])
    else:
        total_dr_inventory = 0.0
        for leg in (voucher.get("legs") or []):
            acct = (leg.get("account") or "").strip()
            debit = leg.get("debit") or 0.0
            if debit > 0 and not any(acct.startswith(p) for p in _PI_INPUT_VAT_PREFIXES):
                total_dr_inventory += debit
        line_items = [{
            "item_name": voucher.get("voucher_remark") or voucher_no,
            "description": voucher.get("voucher_remark") or voucher_no,
            "uom": "Nos",
            "qty": 1.0,
            "rate": total_dr_inventory,
            "net_amount": total_dr_inventory,
            "tax_rate": 0.0,
            "tax_amount": 0.0,
            "tax_account": None,
        }]

    per_line_tk = extract_line_expense_accounts(
        voucher.get("legs") or [], len(line_items)
    )
    per_line_expense_acct: list[str | None] = [
        _resolve_account(tk, mapping, company) for tk in per_line_tk
    ]

    vat_tk = vat_extractor.extract_vat_account(
        voucher.get("legs") or [], side="input"
    )
    vat_account = _resolve_account(vat_tk, mapping, company) if vat_tk else None

    # FIX: PN PI uses update_stock=1 (the entire point of routing PN → PI
    # vs MDV/MH). Without a stock-eligible placeholder, ERPNext skips SLE
    # creation even with update_stock=1, so Dr 1561 GL has no matching
    # SLE → subsequent SE PX has valuation_rate=0 → TK 1561 Cr lost.
    # Use the stock-item placeholder (is_stock_item=1) instead.
    # Lazy import to avoid circular dep (stock_entry → purchase_receipt).
    from vn_accounting.misa_migration.importers.nkc_handlers.stock_entry import (
        _ensure_placeholder_stock_item,
    )
    placeholder_item = _ensure_placeholder_stock_item(company)

    items_payload: list[dict[str, Any]] = []
    for idx, li in enumerate(line_items):
        qty = float(li.get("qty") or 0.0)
        rate = float(li.get("rate") or 0.0)
        net_amount = float(li.get("net_amount") or 0.0)
        if qty <= 0:
            qty = 1.0
            rate = net_amount
        uom = li.get("uom") or "Nos"
        if not frappe.db.exists("UOM", uom):
            uom = "Nos" if frappe.db.exists("UOM", "Nos") else "Unit"
        raw_name = li.get("item_name") or li.get("description") or placeholder_item
        row = {
            "item_code": placeholder_item,
            "item_name": str(raw_name)[:140],  # ERPNext Item Name 140-char cap
            "description": li.get("description") or li.get("item_name") or "",
            "qty": qty,
            "uom": uom,
            "stock_uom": uom,
            "conversion_factor": 1,
            "rate": rate,
            "warehouse": warehouse,  # update_stock=1 requires per-row warehouse
        }
        if per_line_expense_acct[idx]:
            row["expense_account"] = per_line_expense_acct[idx]
        items_payload.append(row)

    taxes_payload = vat_extractor.build_tax_rows(line_items, vat_account)

    posting_date = voucher.get("posting_date") or (
        invoice.get("posting_date") if invoice else None
    )
    bill_no = (invoice or {}).get("invoice_no") or voucher.get("invoice_no")
    bill_date = (invoice or {}).get("invoice_date") or voucher.get("invoice_date")
    supplier_name = (invoice or {}).get("party_name") or voucher.get("party_name")

    payload = {
        "doctype": "Purchase Invoice",
        "supplier": party_code,
        "supplier_name": supplier_name,
        "company": company,
        "posting_date": posting_date,
        "set_posting_time": 1,
        "bill_no": bill_no,
        "bill_date": bill_date,
        "remarks": voucher.get("voucher_remark") or voucher_no,
        "items": items_payload,
        "taxes": taxes_payload,
        "update_stock": 1,
        "supplier_warehouse": warehouse,
        "misa_voucher_no": voucher_no,
    }

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight already validated Supplier / Item /
        # Warehouse / Account links; skip ERPNext's per-row Link check.
        doc.flags.ignore_links = True
        doc.insert(set_name=voucher_no)
        return {
            "status": "created",
            "target_name": doc.name,
            "target_doctype": "Purchase Invoice",
            "update_stock": True,
            "warehouse": warehouse,
            "vat_account": vat_account,
            "line_count": len(items_payload),
            "tax_rows": len(taxes_payload),
            "pr_target_name": None,  # reserved for future sibling PR
        }
    except Exception as exc:
        import traceback
        err = f"{type(exc).__name__}: {exc}"
        # Log full traceback for diagnostics — without this, recurring errors
        # like KeyError('account') give no clue where they originate.
        # Migration Row.error_message keeps the short form for UI rendering.
        frappe.log_error(
            title=f"Misa PN create failed: {voucher_no}",
            message=f"{err}\n\nVoucher legs: {len(voucher.get('legs') or [])}\n\n"
                    f"{traceback.format_exc()}",
        )
        return {"status": "failed", "target_name": None, "error": err}
