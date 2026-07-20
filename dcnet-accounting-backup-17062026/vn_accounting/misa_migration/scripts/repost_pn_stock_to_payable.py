"""Repost Stock Entry GL with proper Dr/Cr derived from NKC source.

Background:
  bulk_pump's orchestrator routes Misa goods-movement vouchers to Stock
  Entry. The SE generic GL pattern is ``Dr <inventory> / Cr <stock_adj>``
  (receipt) or ``Dr <stock_adj> / Cr <inventory>`` (issue). For Misa
  vouchers this is WRONG because:
    - ``PN`` / ``PNHN`` / ``MH`` (receipt of purchased goods) — NKC posts
      ``Dr <inventory> / Cr 331 <supplier>`` (+ optional Dr 1331 VAT).
      Default SE GL routes Cr to stock_adjustment → 331 balance
      artificially short (~1.25B on Jan 2026 / DCNET TEST).
    - ``PX`` / ``PXHN`` (issue for consumption) — NKC posts
      ``Dr 632x/642x <expense> / Cr <inventory>``. Default SE GL routes
      Dr to stock_adjustment → COGS / opex understated, 156 over.

This script post-processes after bulk_pump:
  1. Scan Stock Entry rows for the company.
  2. For each, look up NKC source legs by voucher_no.
  3. Net the legs (NKC stores mirrored entries — cancel them out).
  4. DELETE existing SE GL for this voucher and INSERT correct legs
     using NKC's actual TKs + parties.

Idempotent: re-running with same NKC produces the same GL set. SEs
without NKC counter-entries are left untouched.

Public entries:
  - ``repost_se_gl_from_nkc(company, batch_name=None, only_with_payable=False)``
    Generic: handles all SE types with NKC source.
  - ``repost_pn_stock_to_payable(...)`` — backward-compat alias that
    sets ``only_with_payable=True`` (original PN-focused mode).
"""
from __future__ import annotations

import json
import secrets
import time
from typing import Any

import frappe


# Prefixes that bulk_pump routes to Stock Entry. PN/PNHN/MH/PNN =
# purchase-receipt class (Cr 331). PX/PXHN/PXK/PXDNG = issue/consumption
# class (Dr 632x/642x). Internal-transfer prefixes (CTNB) typically have
# no money impact in NKC; we only process vouchers with non-empty NKC.
PN_PREFIXES = ("PN", "PNHN", "MH", "PNN")  # receipt
PX_PREFIXES = ("PX", "PXHN", "PXK", "PXDNG")  # issue
SE_PREFIXES = PN_PREFIXES + PX_PREFIXES
VND = "VND"


def _gen_name() -> str:
    return secrets.token_hex(10)


def _nkc_legs_for_voucher(batch_name: str, voucher_no: str) -> list[dict]:
    """Return parsed legs from NKC rows for one voucher_no.

    Each leg: {account: TK, debit: float, credit: float, party_code: str,
               party_name: str, line_idx: int}.
    NKC stores both sides of double-entry (mirrored). We keep both.
    """
    rows = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
           AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) = %s
           ORDER BY row_index""",
        (batch_name, voucher_no), as_dict=True,
    )
    legs: list[dict] = []
    for idx, r in enumerate(rows):
        try:
            p = json.loads(r["raw_payload"] or "{}")
        except (TypeError, ValueError):
            continue
        legs.append({
            "account": str(p.get("Tài khoản") or "").strip(),
            "counter_account": str(p.get("TK đối ứng") or "").strip(),
            "debit": float(p.get("Phát sinh Nợ") or 0),
            "credit": float(p.get("Phát sinh Có") or 0),
            "party_code": str(p.get("Mã đối tượng") or "").strip(),
            "party_name": str(p.get("Tên đối tượng") or "").strip(),
            "description": str(p.get("Diễn giải") or "").strip()[:140],
        })
    return legs


def _resolve_account(tk: str, company: str) -> str | None:
    if not tk:
        return None
    # Direct lookup by account_number
    nm = frappe.db.get_value("Account", {"account_number": tk, "company": company}, "name")
    if nm:
        return nm
    # Try as parent if leaf form (e.g. 1121.21 → look for 1121.21)
    return None


def _resolve_party(party_code: str, party_type_hint: str | None = None) -> tuple[str | None, str | None]:
    """Return (party_type, party_name). Try Supplier first for PN, then Customer."""
    if not party_code:
        return (None, None)
    # PN is purchase → most likely Supplier
    if frappe.db.exists("Supplier", party_code):
        return ("Supplier", party_code)
    if frappe.db.exists("Customer", party_code):
        return ("Customer", party_code)
    return (None, None)


def _build_gl_row(
    *, account: str, debit: float, credit: float, voucher_no: str,
    voucher_type: str, posting_date, fiscal_year: str, company: str,
    party_type: str | None, party: str | None, remarks: str,
    now, owner: str,
) -> dict:
    return {
        "name": _gen_name(),
        "creation": now, "modified": now, "owner": owner, "modified_by": owner,
        "docstatus": 1, "idx": 0,
        "posting_date": posting_date, "transaction_date": posting_date,
        "fiscal_year": fiscal_year,
        "account": account, "account_currency": VND,
        "voucher_type": voucher_type, "voucher_no": voucher_no,
        "transaction_currency": VND,
        "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
        "debit": round(debit, 0), "debit_in_account_currency": round(debit, 0),
        "debit_in_transaction_currency": round(debit, 0),
        "debit_in_reporting_currency": round(debit, 0),
        "credit": round(credit, 0), "credit_in_account_currency": round(credit, 0),
        "credit_in_transaction_currency": round(credit, 0),
        "credit_in_reporting_currency": round(credit, 0),
        "party_type": party_type, "party": party,
        "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
        "remarks": remarks[:240],
    }


@frappe.whitelist()
def repost_se_gl_from_nkc(
    company: str,
    batch_name: str | None = None,
    only_with_payable: bool = False,
) -> dict[str, Any]:
    """Repost SE GL by re-deriving from NKC source legs.

    Args:
      company: Target company.
      batch_name: If set, scope to one Misa Migration Batch. Default:
                  latest batch for the company.
      only_with_payable: If True, only repost vouchers whose NKC has a
                         331/338 Cr leg (original PN-focused mode).
                         Default False = process ALL PN+PX SEs with NKC
                         (both receipt + issue side).

    Returns:
      Summary dict — vouchers_processed / gl_deleted / gl_inserted /
      voucher-by-voucher details (truncated).
    """
    t0 = time.time()
    co_doc = frappe.get_doc("Company", company)
    stock_adj = co_doc.stock_adjustment_account
    if not stock_adj:
        frappe.throw("Company has no stock_adjustment_account — cannot diff.")

    # Find SE for prefixes bulk_pump routes through SE builder.
    # Double %% per memory rule "frappe.db.sql LIKE pattern needs %%".
    prefix_clauses = " OR ".join(f"name LIKE '{p}%%'" for p in SE_PREFIXES)
    se_rows = frappe.db.sql(
        f"""SELECT name, posting_date, total_amount, owner
            FROM `tabStock Entry`
            WHERE company=%s AND ({prefix_clauses})""",
        (company,), as_dict=True,
    )
    # Derive fiscal_year from posting_date (Stock Entry has no fiscal_year col)
    for s in se_rows:
        pd = s.get("posting_date")
        s["fiscal_year"] = str(pd.year) if pd else "2026"
    if not se_rows:
        return {"company": company, "vouchers_found": 0, "elapsed_seconds": round(time.time() - t0, 2)}

    # If batch_name scoped, intersect with batch's voucher_no list
    if batch_name:
        batch_vnos = set(frappe.db.sql_list(
            """SELECT DISTINCT JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))
               FROM `tabMisa Migration Row`
               WHERE batch=%s AND file_type='NKC'""",
            (batch_name,),
        ))
        se_rows = [s for s in se_rows if s["name"] in batch_vnos]
    else:
        # Need a batch to read NKC from — pick the latest batch for company
        batch_name = frappe.db.get_value(
            "Misa Migration Batch", {"company": company},
            "name", order_by="creation desc",
        )
        if not batch_name:
            return {"company": company, "vouchers_found": len(se_rows),
                    "error": "no Misa Migration Batch found", "elapsed_seconds": round(time.time() - t0, 2)}

    processed = 0
    gl_deleted = gl_inserted = 0
    details: list[dict] = []
    now = frappe.utils.now()

    for se in se_rows:
        vno = se["name"]
        legs = _nkc_legs_for_voucher(batch_name, vno)
        if not legs:
            continue

        # Group legs by (account, side) and aggregate. NKC includes mirrored
        # entries (Dr X/Cr Y plus Dr Y/Cr X); we want each leg ONCE.
        # Strategy: only keep one direction per voucher_no — use the leg
        # where credit > 0 for the counter-party (331/152x/etc.), and the
        # leg where debit > 0 for the asset side (156x/1331/etc.). That's
        # the natural "first half" of each double-entry.
        leg_totals: dict[str, dict] = {}  # tk → {dr, cr, party_code, party_name}
        for leg in legs:
            tk = leg["account"]
            if not tk:
                continue
            cur = leg_totals.setdefault(tk, {"dr": 0.0, "cr": 0.0, "party_code": "", "party_name": ""})
            cur["dr"] += leg["debit"]
            cur["cr"] += leg["credit"]
            if not cur["party_code"] and leg["party_code"]:
                cur["party_code"] = leg["party_code"]
                cur["party_name"] = leg["party_name"]

        # Net per TK (Dr - Cr to dedupe mirrored entries; if mirror present
        # both sides cancel; otherwise we get the actual net).
        # Asset-side TKs (156/152/1331) take Dr; payable/expense-side
        # (331/338/335/6xx/642) take Cr when mirrored.
        ASSET_PREFIXES = ("156", "152", "153", "155", "157", "1331", "133", "211", "242", "141")
        CREDIT_PREFIXES = ("331", "338", "335", "334", "333", "1388")
        net_legs: list[dict] = []
        for tk, t in leg_totals.items():
            net = t["dr"] - t["cr"]
            if abs(net) < 0.005:
                # mirrored — split based on account semantics
                if tk.startswith(ASSET_PREFIXES):
                    net_legs.append({"account": tk, "debit": t["dr"], "credit": 0,
                                     "party_code": "", "party_name": ""})
                elif tk.startswith(CREDIT_PREFIXES) or tk.startswith(("6", "8")):
                    net_legs.append({"account": tk, "debit": 0, "credit": t["cr"],
                                     "party_code": t["party_code"], "party_name": t["party_name"]})
                elif tk.startswith(("5", "7")):
                    # Revenue/Other income: Cr side primary
                    net_legs.append({"account": tk, "debit": 0, "credit": t["cr"],
                                     "party_code": t["party_code"], "party_name": t["party_name"]})
                else:
                    # Unclassified — keep the dominant side
                    if t["dr"] >= t["cr"]:
                        net_legs.append({"account": tk, "debit": t["dr"], "credit": 0,
                                         "party_code": t["party_code"], "party_name": t["party_name"]})
                    else:
                        net_legs.append({"account": tk, "debit": 0, "credit": t["cr"],
                                         "party_code": t["party_code"], "party_name": t["party_name"]})
            elif net > 0:
                net_legs.append({"account": tk, "debit": net, "credit": 0,
                                 "party_code": t["party_code"], "party_name": t["party_name"]})
            else:
                net_legs.append({"account": tk, "debit": 0, "credit": -net,
                                 "party_code": t["party_code"], "party_name": t["party_name"]})

        if not net_legs:
            continue

        # Optional filter — only process vouchers with a payable Cr leg.
        # Default OFF so PX (issue) vouchers also get reposted (their NKC
        # has Cr <inventory> + Dr 632x/642x, no payable involved).
        if only_with_payable:
            has_payable = any(
                l["account"].startswith(("331", "338", "335")) and l["credit"] > 0
                for l in net_legs
            )
            if not has_payable:
                continue

        # DELETE existing SE GL for this voucher (we'll rebuild from NKC).
        # SE-builder created entries: Dr <inventory_account> / Cr <stock_adjustment>.
        n_del = frappe.db.sql(
            "DELETE FROM `tabGL Entry` WHERE voucher_type='Stock Entry' AND voucher_no=%s",
            (vno,),
        )
        gl_deleted += int(frappe.db._cursor.rowcount or 0)

        # INSERT GL legs derived from NKC
        new_gl_rows: list[dict] = []
        for leg in net_legs:
            acc_name = _resolve_account(leg["account"], company)
            if not acc_name:
                continue
            party_type = party = None
            if leg["account"].startswith(("331",)) and leg["party_code"]:
                pt, pn = _resolve_party(leg["party_code"])
                party_type, party = pt, pn
            new_gl_rows.append(_build_gl_row(
                account=acc_name,
                debit=leg["debit"], credit=leg["credit"],
                voucher_no=vno, voucher_type="Stock Entry",
                posting_date=se["posting_date"],
                fiscal_year=se["fiscal_year"] or "2026",
                company=company,
                party_type=party_type, party=party,
                remarks=f"PN repost: {leg['party_name'] or leg['account']}",
                now=now, owner=se["owner"] or "Administrator",
            ))

        for row in new_gl_rows:
            cols = ",".join(f"`{k}`" for k in row.keys())
            placeholders = ",".join(["%s"] * len(row))
            frappe.db.sql(
                f"INSERT INTO `tabGL Entry` ({cols}) VALUES ({placeholders})",
                tuple(row.values()),
            )
            gl_inserted += 1

        processed += 1
        if len(details) < 10:  # sample first 10 vouchers
            details.append({
                "voucher_no": vno,
                "legs": [{"acc": l["account"], "dr": l["debit"], "cr": l["credit"],
                          "party": l["party_code"]} for l in net_legs],
            })

    frappe.db.commit()
    return {
        "company": company,
        "batch_name": batch_name,
        "only_with_payable": only_with_payable,
        "vouchers_found": len(se_rows),
        "vouchers_processed": processed,
        "gl_deleted": gl_deleted,
        "gl_inserted": gl_inserted,
        "elapsed_seconds": round(time.time() - t0, 2),
        "samples": details,
    }


@frappe.whitelist()
def repost_pn_stock_to_payable(
    company: str,
    batch_name: str | None = None,
) -> dict[str, Any]:
    """Backward-compat alias — calls ``repost_se_gl_from_nkc`` with
    ``only_with_payable=True`` (PN-focused original behaviour).
    """
    return repost_se_gl_from_nkc(company, batch_name=batch_name, only_with_payable=True)
