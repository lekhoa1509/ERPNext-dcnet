"""BH (Bán hàng) → Sales Invoice handler.

Phase D commit 4. Consumes:
  - voucher dict from nkc_parser (party_code, posting_date, legs[])
  - invoice dict from invoice_list_parser kind='BR' (line_items[] with qty/
    rate/net/tax_rate/tax_amount per line)

Joins them by voucher_no (caller's responsibility) and creates one ERPNext
Sales Invoice with:
  - doc.name = Misa Số chứng từ (per spec §15, e.g. "BH20260001")
  - customer = Misa Mã khách hàng (Phase 3 master must already exist)
  - items = one row per bảng kê line item, with per-line income_account
    extracted from the NKC voucher's Cr 511* legs in source order
  - taxes = one row per unique VAT rate group, charge_type="On Net Total"
  - bill_no / bill_date = Misa invoice metadata
"""

from __future__ import annotations

import json
from collections import OrderedDict
from typing import Any

import frappe

from vn_accounting.misa_migration.context import get_active_company as _get_company
from vn_accounting.misa_migration.importers._naming import migrated_doc_name

# Single placeholder Item used for all SI line items. Created lazily per
# Company. Real Item lookup by item_name is too fuzzy for v1; placeholder
# keeps line items legible via description field.
PLACEHOLDER_ITEM_CODE = "MISA-MIGRATION-SVC"
PLACEHOLDER_STOCK_ITEM_CODE = "MISA-MIGRATION-STOCK"
PLACEHOLDER_ITEM_GROUP_FALLBACKS = ("Services", "All Item Groups")

# VAT/output account TK prefix and revenue prefix per VAS chart TT99/2025
_VAT_OUTPUT_PREFIXES = ("3331", "33311", "33312", "33313")
_REVENUE_PREFIXES = ("511", "5111", "5112", "5113", "51131", "51132",
                     "51133", "51134", "51135", "51136", "51137", "51138",
                     "5114", "5117", "5118", "521", "5211", "5212", "5213",
                     # TK 3387 — Doanh thu chưa thực hiện (deferred revenue).
                     # Misa BH cho contract multi-period dùng Cr 3387 (defer)
                     # rồi PBDT recognize qua Dr 3387 / Cr 511x. SI builder
                     # phải pick up 3387 leg cho deferred-rev sales — nếu
                     # không sẽ fall back default 5111 và mất Cr 3387 hoàn
                     # toàn (DCNET test: 955M / batch).
                     "3387")
_RECEIVABLE_PREFIXES = ("131",)


# ----------------------------------------------------------- helpers

def _load_account_mapping() -> dict[str, str]:
    """Load the Misa Account Mapping Single doc's mappings JSON."""
    try:
        doc = frappe.get_single("Misa Account Mapping")
        return json.loads(doc.mappings or "{}")
    except Exception:
        return {}


def _resolve_account(misa_tk: str | None, mapping: dict[str, str],
                     company: str | None) -> str | None:
    """Misa TK → leaf Account.name, COMPANY-VERIFIED (see _account_lookup)."""
    from vn_accounting.misa_migration.importers.nkc_handlers._account_lookup import (
        resolve_account,
    )
    return resolve_account(misa_tk, mapping, company)

def _ensure_placeholder_item(company: str | None) -> str:
    """Create the placeholder MISA-MIGRATION-SVC Item if not present. Idempotent."""
    if frappe.db.exists("Item", PLACEHOLDER_ITEM_CODE):
        return PLACEHOLDER_ITEM_CODE
    # Resolve a defensible Item Group
    item_group = None
    for cand in PLACEHOLDER_ITEM_GROUP_FALLBACKS:
        if frappe.db.exists("Item Group", cand):
            item_group = cand
            break
    if not item_group:
        # Last resort: pick any group
        item_group = frappe.db.get_value("Item Group", {"is_group": 0}, "name")
    uom = "Nos" if frappe.db.exists("UOM", "Nos") else frappe.db.get_value(
        "UOM", {}, "name"
    )
    doc = frappe.get_doc({
        "doctype": "Item",
        "item_code": PLACEHOLDER_ITEM_CODE,
        "item_name": "Misa Migration — Placeholder Service Item",
        "item_group": item_group,
        "is_stock_item": 0,
        "stock_uom": uom,
        "description": "Placeholder Item used by Misa Migration importer for "
                       "Sales/Purchase Invoice line items. Real Item master "
                       "lookup is too fuzzy in v1; line description carries "
                       "the verbatim Misa Mặt hàng / Diễn giải text.",
    })
    doc.flags.ignore_permissions = True
    doc.insert(set_name=PLACEHOLDER_ITEM_CODE)
    return PLACEHOLDER_ITEM_CODE


def _ensure_placeholder_stock_item(company: str | None) -> str:
    """Stock-tracked placeholder Item for Stock Entry / PN PI with
    update_stock=1.

    Separate from MISA-MIGRATION-SVC because Material Issue / Transfer /
    Receipt Stock Entries require is_stock_item=1 on every line item;
    using the service placeholder fails with "X is not a stock Item".
    """
    if frappe.db.exists("Item", PLACEHOLDER_STOCK_ITEM_CODE):
        return PLACEHOLDER_STOCK_ITEM_CODE
    item_group = None
    for cand in PLACEHOLDER_ITEM_GROUP_FALLBACKS:
        if frappe.db.exists("Item Group", cand):
            item_group = cand
            break
    if not item_group:
        item_group = frappe.db.get_value("Item Group", {"is_group": 0}, "name")
    uom = "Nos" if frappe.db.exists("UOM", "Nos") else frappe.db.get_value(
        "UOM", {}, "name"
    )
    doc = frappe.get_doc({
        "doctype": "Item",
        "item_code": PLACEHOLDER_STOCK_ITEM_CODE,
        "item_name": "Misa Migration — Placeholder Stock Item",
        "item_group": item_group,
        "is_stock_item": 1,
        "stock_uom": uom,
        "description": "Stock-tracked placeholder for Misa Material Issue / "
                       "Transfer / Receipt Stock Entries. Real Item lookup "
                       "deferred to Phase E.",
    })
    doc.flags.ignore_permissions = True
    doc.insert(set_name=PLACEHOLDER_STOCK_ITEM_CODE)
    return PLACEHOLDER_STOCK_ITEM_CODE


def extract_line_income_accounts(
    voucher_legs: list[dict[str, Any]],
    n_line_items: int,
    line_amounts: list[float] | None = None,
) -> list[str | None]:
    """Extract one Misa TK (revenue) string per bảng kê line item, in order.

    BH NKC pattern is 4 legs per invoice line (Dr 131 net, Cr 511X net,
    Dr 131 VAT, Cr 33311 VAT). But some BH have N×items legs (deferred-rev
    splits with VAT) where N varies — chunk-by-index misaligns.

    Algorithm (refined to handle multi-revenue-TK):
      1. Aggregate ALL Cr revenue legs (5xx, 521x, 3387) by TK total.
      2. Single revenue TK → use for ALL items (covers BH20260004 lump
         deferred revenue case: 100 legs / 30 items all Cr 3387).
      3. Multi revenue TK + line_amounts given → greedy assignment by
         largest remaining TK budget; items drain TK budget until next-TK
         wins (covers BH20260192 with Cr 51133 + 51134 + 3387 mix).
      4. Multi-TK without amounts → legacy chunk algo (last-resort).

    Args:
      voucher_legs: NKC voucher legs in source order.
      n_line_items: number of bảng kê line items.
      line_amounts: optional per-item amounts for greedy multi-TK assignment.

    Returns:
      list[str | None] of length n_line_items. Indices = line item positions.
    """
    if not voucher_legs or n_line_items <= 0:
        return [None] * n_line_items

    # Step 1: collect revenue Cr legs by TK
    tk_totals: dict[str, float] = {}
    for leg in voucher_legs:
        acct = (leg.get("account") or "").strip()
        cr = leg.get("credit") or 0.0
        if cr > 0 and any(acct.startswith(p) for p in _REVENUE_PREFIXES):
            tk_totals[acct] = tk_totals.get(acct, 0.0) + float(cr)

    if not tk_totals:
        return [None] * n_line_items

    # Step 2: single revenue TK → easy
    if len(tk_totals) == 1:
        only_tk = next(iter(tk_totals))
        return [only_tk] * n_line_items

    # Step 3: multi-TK with per-line amounts → AMOUNT-MATCH first, greedy fallback.
    #
    # Per-line amount match is dramatically more accurate than greedy budget
    # because Misa NKC typically has exactly 1 Cr revenue leg per MV item
    # (same amount). E.g. BH with 6 items each 5M → 6 Cr 5xxx legs each 5M,
    # one per item. Greedy by "largest remaining budget" disperses items
    # across TKs incorrectly when amounts vary.
    #
    # Algorithm:
    #   For each MV line item amount X:
    #     1. Try unused NKC Cr revenue leg with amount ≈ X (tolerance 1 VND).
    #        If found → use that leg's TK, mark leg consumed.
    #     2. Try unused leg with amount close to X (within 5% tolerance).
    #     3. Fallback: pick TK with largest remaining budget; subtract item amt.
    if line_amounts and len(line_amounts) >= n_line_items:
        # Build mutable leg list (tk, amount, used flag)
        legs_pool: list[list] = []
        for leg in voucher_legs:
            acct = (leg.get("account") or "").strip()
            cr = float(leg.get("credit") or 0.0)
            if cr > 0 and any(acct.startswith(p) for p in _REVENUE_PREFIXES):
                legs_pool.append([acct, cr, False])
        remaining_by_tk: dict[str, float] = dict(tk_totals)
        out: list[str | None] = []
        for idx in range(n_line_items):
            amt = float(line_amounts[idx] or 0)
            matched_tk = None
            # Try exact match (≤ 1 VND tolerance)
            for entry in legs_pool:
                if not entry[2] and abs(entry[1] - amt) <= 1.0:
                    matched_tk = entry[0]
                    entry[2] = True
                    remaining_by_tk[matched_tk] = remaining_by_tk.get(matched_tk, 0) - entry[1]
                    break
            # Try fuzzy match (≤ 5%, min 100 VND)
            if not matched_tk and amt > 0:
                fuzzy_tol = max(100.0, amt * 0.05)
                for entry in legs_pool:
                    if not entry[2] and abs(entry[1] - amt) <= fuzzy_tol:
                        matched_tk = entry[0]
                        entry[2] = True
                        remaining_by_tk[matched_tk] = remaining_by_tk.get(matched_tk, 0) - entry[1]
                        break
            # Fallback: largest remaining budget
            if not matched_tk and remaining_by_tk:
                best = max(remaining_by_tk, key=lambda k: remaining_by_tk[k])
                if remaining_by_tk[best] > 0.5:
                    matched_tk = best
                    remaining_by_tk[best] -= amt
                    if remaining_by_tk[best] <= 0 and len(remaining_by_tk) > 1:
                        del remaining_by_tk[best]
            out.append(matched_tk)
        return out

    # Step 4: legacy chunk algo (multi-TK without amounts)
    out_legacy: list[str | None] = []
    legs_per_line = max(1, len(voucher_legs) // n_line_items)
    for line_idx in range(n_line_items):
        start = line_idx * legs_per_line
        end = start + legs_per_line
        chunk = voucher_legs[start:end]
        revenue_tk = None
        for leg in chunk:
            acct = (leg.get("account") or "").strip()
            credit = leg.get("credit") or 0.0
            if credit > 0 and any(acct.startswith(p) for p in _REVENUE_PREFIXES):
                revenue_tk = acct
                break
        out_legacy.append(revenue_tk)
    return out_legacy


def extract_tax_account(voucher_legs: list[dict[str, Any]]) -> str | None:
    """Find the first Cr 33311 (or 3331*) leg account from NKC. None if absent."""
    for leg in voucher_legs:
        acct = (leg.get("account") or "").strip()
        credit = leg.get("credit") or 0.0
        if credit > 0 and any(acct.startswith(p) for p in _VAT_OUTPUT_PREFIXES):
            return acct
    return None


def _group_line_items_by_tax_rate(
    line_items: list[dict[str, Any]],
) -> "OrderedDict[float, list[dict[str, Any]]]":
    """Group bảng kê line items by tax_rate (preserves first-seen rate order)."""
    groups: OrderedDict[float, list[dict[str, Any]]] = OrderedDict()
    for li in line_items:
        rate = float(li.get("tax_rate") or 0.0)
        groups.setdefault(rate, []).append(li)
    return groups


# ----------------------------------------------------------- main handler

def create_si_from_bh(
    voucher: dict[str, Any],
    invoice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a Sales Invoice doc from BH voucher + matching bảng kê BR invoice.

    Returns result dict with status keys.
    """
    voucher_no = voucher.get("voucher_no")
    if not voucher_no:
        return {"status": "failed", "error": "voucher missing voucher_no"}

    if invoice is None:
        return {"status": "failed",
                "error": f"bảng kê BR invoice not provided for {voucher_no}"}

    # Resolve company from a sensible source: any default Company.
    # In production this comes from Misa Migration Batch.company; for the
    # standalone handler we derive from Customer master.
    party_code = voucher.get("party_code") or ""
    if not party_code:
        return {"status": "failed",
                "error": f"voucher {voucher_no} missing party_code (NKC 'Mã đối tượng')"}
    # PERF (Tier 1.5): set-lookup vs per-call DB round-trip
    from vn_accounting.misa_migration.importers.nkc_handlers import _party_cache
    if not _party_cache.is_customer(party_code):
        return {"status": "failed",
                "error": f"Customer {party_code!r} not found — run Phase 3 first"}

    customer_company = frappe.db.get_value("Customer", party_code, "represents_company")
    company = customer_company or _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    # Company-namespaced doc name so two companies' overlapping Misa voucher
    # numbers don't collide on ERPNext's global doc name. Idempotency skip
    # checks the namespaced name (raw voucher_no kept in misa_voucher_no).
    target_name = migrated_doc_name(company, voucher_no)
    if frappe.db.exists("Sales Invoice", target_name):
        return {"status": "skipped", "target_name": target_name,
                "error": None, "reason": "already_exists"}

    mapping = _load_account_mapping()
    line_items = invoice.get("line_items") or []
    if not line_items:
        return {"status": "failed",
                "error": f"bảng kê BR has 0 line items for {voucher_no}"}

    # Per-line income accounts from NKC, then resolved via mapping
    per_line_tk = extract_line_income_accounts(
        voucher.get("legs") or [], len(line_items)
    )
    per_line_income_acct: list[str | None] = [
        _resolve_account(tk, mapping, company) for tk in per_line_tk
    ]

    # VAT account from NKC's first Cr 33311 leg
    vat_tk = extract_tax_account(voucher.get("legs") or [])
    vat_account = _resolve_account(vat_tk, mapping, company) if vat_tk else None

    placeholder_item = _ensure_placeholder_item(company)
    from vn_accounting.misa_migration.importers.nkc_handlers import _item_cache

    # Build Items child rows
    items_payload: list[dict[str, Any]] = []
    for idx, li in enumerate(line_items):
        qty = float(li.get("qty") or 0.0)
        rate = float(li.get("rate") or 0.0)
        net_amount = float(li.get("net_amount") or 0.0)
        # Misa allows qty=0, net=0 for placeholder rows — keep but skip rate validation
        # ERPNext requires qty > 0 for SI; bump to 1 if 0
        if qty <= 0:
            qty = 1.0
            rate = net_amount  # so amount = qty*rate = net_amount

        uom = li.get("uom") or "Nos"
        if not frappe.db.exists("UOM", uom):
            uom = "Nos" if frappe.db.exists("UOM", "Nos") else "Unit"
        # Fractional qty + placeholder Item (stock_uom='Nos' must_be_whole=1)
        # always fails because SI/PI override row UOM to match Item.stock_uom.
        # Unconditionally collapse to qty=1 + rate*=qty (preserves total).
        if qty != int(qty):
            rate = qty * rate
            qty = 1.0

        # ERPNext Item Name = Data field (140 char cap). Misa item names
        # frequently exceed this for descriptive contracts. Truncate.
        raw_name = li.get("item_name") or li.get("description") or placeholder_item
        # Real Item match by name; fall back to placeholder when no master row.
        matched_code = _item_cache.match_item_code(li.get("item_name"))
        item_code_used = matched_code or placeholder_item
        row = {
            "item_code": item_code_used,
            "item_name": str(raw_name)[:140],
            "description": li.get("description") or li.get("item_name") or "",
            "qty": qty,
            "uom": uom,
            "stock_uom": uom,
            "conversion_factor": 1,
            "rate": rate,
            # ERPNext computes amount = qty * rate; we let it.
        }
        if per_line_income_acct[idx]:
            row["income_account"] = per_line_income_acct[idx]
        items_payload.append(row)

    # Build Taxes child rows — one row per tax_rate group
    tax_groups = _group_line_items_by_tax_rate(line_items)
    taxes_payload: list[dict[str, Any]] = []
    for rate, lis in tax_groups.items():
        if rate == 0.0:
            continue  # ERPNext skips 0% tax rows by convention
        tax_amount_total = sum(float(li.get("tax_amount") or 0.0) for li in lis)
        if not vat_account or tax_amount_total <= 0:
            continue
        taxes_payload.append({
            "charge_type": "On Net Total",
            "account_head": vat_account,
            "description": f"VAT {rate:g}%",
            "rate": rate,
            "included_in_print_rate": 0,
        })

    posting_date = voucher.get("posting_date") or invoice.get("posting_date")
    bill_no = invoice.get("invoice_no") or voucher.get("invoice_no")
    bill_date = invoice.get("invoice_date") or voucher.get("invoice_date")

    payload = {
        "doctype": "Sales Invoice",
        "customer": party_code,
        "company": company,
        "posting_date": posting_date,
        "set_posting_time": 1,
        "bill_no": bill_no,
        "bill_date": bill_date,
        "remarks": voucher.get("voucher_remark") or invoice.get("invoice_no") or "",
        "items": items_payload,
        "taxes": taxes_payload,
        "update_stock": 0,
        # Custom fields
        "misa_voucher_no": voucher_no,
    }

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        # PERF (Tier 1.2): preflight already validated Customer / Account
        # links; skip ERPNext's per-row Link integrity check (~5-10ms/row)
        doc.flags.ignore_links = True
        doc.insert(set_name=target_name)
        return {"status": "created", "target_name": doc.name,
                "target_doctype": "Sales Invoice",
                "vat_account": vat_account,
                "line_count": len(items_payload),
                "tax_rows": len(taxes_payload)}
    except Exception as exc:
        import traceback
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(
            title=f"Misa SI create failed: {voucher_no}",
            message=f"{err}\n\nVoucher legs: {len(voucher.get('legs') or [])}\n\n"
                    f"{traceback.format_exc()}",
        )
        return {"status": "failed", "target_name": None, "error": err}
