"""Comprehensive audit of source-data gaps for a Misa Migration Batch.

Reports issues an accountant should review BEFORE trusting the import.
Each category surfaces a different class of "data wrong/missing":

  A. ``stock_entry_no_gl`` — SE moved stock but no GL Entry. Misa source
     may be missing the JE side of the entry.
  B. ``stock_entry_no_nkc`` — SE auto-created (e.g. from SCT) without any
     NKC source row. Origin unclear.
  C. ``nkc_no_target_doc`` — NKC voucher_no has no corresponding posted
     doc (PI/SE/JE/PE/SI). bulk_pump routing skipped this voucher OR
     classified it as a non-transaction.
  D. ``nkc_unbalanced`` — NKC voucher with sum(Phát sinh Nợ) ≠ sum(Phát
     sinh Có). Data quality issue at source.
  E. ``unmapped_tk`` — Distinct TK appearing in NKC but not present as
     Account in COA. Postings to this TK silently fall to a fallback
     account or get skipped.
  F. ``unmapped_party`` — Mã đối tượng in NKC where TK starts with 131
     but no Customer master, OR TK starts with 331 but no Supplier
     master.
  G. ``unmapped_item`` — Mã hàng in BR/MV/SCT not in Item master. Lines
     route to placeholder Item.
  H. ``doc_total_vs_nkc_mismatch`` — Posted doc's grand_total differs
     from NKC voucher's net amount. Indicates PI/SI/PE amount
     extraction bug or NKC has lines bulk_pump didn't include.

Public entry: ``audit_source_data_gaps(batch_name, threshold_amount=1000)``
— whitelisted. Returns a structured summary + sample details (top 20
per category) for accountant review.
"""
from __future__ import annotations

import json
import time
from typing import Any

import frappe


@frappe.whitelist()
def audit_source_data_gaps(
    batch_name: str,
    threshold_amount: float = 1000.0,
) -> dict[str, Any]:
    """Run all audit categories. Returns structured findings."""
    if not batch_name:
        frappe.throw(frappe._("Phải chọn batch."))
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        frappe.throw(frappe._("Batch không có Company."))

    t0 = time.time()
    out: dict[str, Any] = {
        "batch_name": batch_name,
        "company": company,
        "threshold_amount": threshold_amount,
        "categories": {},
    }

    # ─── A & B: Stock Entry without GL / without NKC ─────────────────
    se_rows = frappe.db.sql(
        "SELECT name, posting_date, total_amount FROM `tabStock Entry` WHERE company=%s",
        (company,), as_dict=True,
    )
    a_no_gl: list[dict] = []
    b_no_nkc: list[dict] = []
    for se in se_rows:
        n_gl = frappe.db.sql(
            "SELECT COUNT(*) FROM `tabGL Entry` WHERE voucher_type='Stock Entry' AND voucher_no=%s AND is_cancelled=0",
            (se["name"],),
        )[0][0]
        n_nkc = frappe.db.sql(
            """SELECT COUNT(*) FROM `tabMisa Migration Row`
               WHERE batch=%s AND file_type='NKC'
               AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))=%s""",
            (batch_name, se["name"]),
        )[0][0]
        if n_gl == 0:
            a_no_gl.append({
                "voucher_no": se["name"],
                "posting_date": str(se["posting_date"]),
                "total_amount": float(se["total_amount"] or 0),
                "nkc_legs_count": n_nkc,
            })
        if n_nkc == 0 and not se["name"].startswith("OB-"):
            b_no_nkc.append({
                "voucher_no": se["name"],
                "posting_date": str(se["posting_date"]),
                "total_amount": float(se["total_amount"] or 0),
            })
    out["categories"]["A_stock_entry_no_gl"] = {
        "count": len(a_no_gl),
        "total_amount": round(sum(x["total_amount"] for x in a_no_gl), 0),
        "samples": sorted(a_no_gl, key=lambda x: -x["total_amount"])[:20],
        "hint": "SE moved stock but no GL. Either internal-transfer (OK) "
                "or source NKC missing the JE side. Re-run "
                "`repost_se_gl_from_nkc` first; remaining items need accountant review.",
    }
    out["categories"]["B_stock_entry_no_nkc"] = {
        "count": len(b_no_nkc),
        "total_amount": round(sum(x["total_amount"] for x in b_no_nkc), 0),
        "samples": sorted(b_no_nkc, key=lambda x: -x["total_amount"])[:20],
        "hint": "SE has no NKC source — auto-created from SCT or elsewhere. "
                "Confirm origin with accountant.",
    }

    # ─── C: NKC voucher with no target doc ───────────────────────────
    orphans = frappe.db.sql(
        """SELECT DISTINCT JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) AS vno
           FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
           AND (target_doctype IS NULL OR target_doctype = '')""",
        (batch_name,), pluck=True,
    )
    c_no_doc: list[dict] = []
    for vno in orphans:
        if not vno:
            continue
        # Compute voucher net amount
        amt = frappe.db.sql(
            """SELECT
                 SUM(CAST(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Phát sinh Nợ"')) AS DECIMAL(20,2))) AS dr,
                 MIN(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Ngày hạch toán"'))) AS pd
               FROM `tabMisa Migration Row`
               WHERE batch=%s AND file_type='NKC'
               AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))=%s""",
            (batch_name, vno), as_dict=True,
        )[0]
        net = float(amt.get("dr") or 0)
        if net < threshold_amount:
            continue
        c_no_doc.append({
            "voucher_no": vno,
            "posting_date": str(amt.get("pd") or "")[:10],
            "total_dr": net,
        })
    out["categories"]["C_nkc_no_target_doc"] = {
        "count": len(c_no_doc),
        "total_amount": round(sum(x["total_dr"] for x in c_no_doc), 0),
        "samples": sorted(c_no_doc, key=lambda x: -x["total_dr"])[:20],
        "hint": "NKC voucher exists in source but bulk_pump didn't create "
                "a target doc. Either prefix routing missed it, or it's "
                "a closing-rule/internal entry classified as non-transaction.",
    }

    # ─── D: NKC voucher unbalanced ──────────────────────────────────
    unb = frappe.db.sql(
        """SELECT JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) AS vno,
                  SUM(CAST(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Phát sinh Nợ"')) AS DECIMAL(20,2))) AS dr,
                  SUM(CAST(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Phát sinh Có"')) AS DECIMAL(20,2))) AS cr
           FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
           GROUP BY vno
           HAVING ABS(dr - cr) > %s""",
        (batch_name, threshold_amount), as_dict=True,
    )
    out["categories"]["D_nkc_unbalanced"] = {
        "count": len(unb),
        "samples": sorted(
            [{"voucher_no": x["vno"], "dr": float(x["dr"] or 0),
              "cr": float(x["cr"] or 0), "diff": float(x["dr"] or 0) - float(x["cr"] or 0)}
             for x in unb if x["vno"]],
            key=lambda x: -abs(x["diff"]),
        )[:20],
        "hint": "NKC voucher where Σ Dr ≠ Σ Cr. Misa export integrity issue. "
                "Confirm with accountant whether voucher needs manual correction.",
    }

    # ─── E: Unmapped TK ─────────────────────────────────────────────
    tks_in_nkc = frappe.db.sql(
        """SELECT DISTINCT JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Tài khoản"')) AS tk
           FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'""",
        (batch_name,), pluck=True,
    )
    unmapped_tks: list[dict] = []
    for tk in tks_in_nkc:
        if not tk or not tk[0].isdigit():
            continue
        exists = frappe.db.get_value(
            "Account", {"account_number": tk, "company": company}, "name",
        )
        if not exists:
            # Count NKC rows referencing this TK
            n = frappe.db.sql(
                """SELECT COUNT(*) FROM `tabMisa Migration Row`
                   WHERE batch=%s AND file_type='NKC'
                   AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Tài khoản"'))=%s""",
                (batch_name, tk),
            )[0][0]
            unmapped_tks.append({"tk": tk, "nkc_rows": n})
    out["categories"]["E_unmapped_tk"] = {
        "count": len(unmapped_tks),
        "samples": sorted(unmapped_tks, key=lambda x: -x["nkc_rows"])[:20],
        "hint": "NKC posts to this TK but no Account exists. Bulk_pump's "
                "account_resolver falls back to closest parent or expense "
                "default — silent routing. Add these TKs to COA.",
    }

    # ─── F: Unmapped party (Customer/Supplier) ──────────────────────
    parties = frappe.db.sql(
        """SELECT JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Tài khoản"')) AS tk,
                  JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Mã đối tượng"')) AS code,
                  JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Tên đối tượng"')) AS name,
                  COUNT(*) AS n
           FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
           AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Mã đối tượng"')) IS NOT NULL
           AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Mã đối tượng"')) != ''
           GROUP BY tk, code, name""",
        (batch_name,), as_dict=True,
    )
    unmapped_parties: list[dict] = []
    for p in parties:
        code = (p["code"] or "").strip()
        tk = (p["tk"] or "").strip()
        if not code:
            continue
        if tk.startswith("131") and not frappe.db.exists("Customer", code):
            unmapped_parties.append({"role": "Customer", "code": code, "name": p["name"], "tk": tk, "nkc_rows": p["n"]})
        elif tk.startswith("331") and not frappe.db.exists("Supplier", code):
            unmapped_parties.append({"role": "Supplier", "code": code, "name": p["name"], "tk": tk, "nkc_rows": p["n"]})
    out["categories"]["F_unmapped_party"] = {
        "count": len(unmapped_parties),
        "samples": sorted(unmapped_parties, key=lambda x: -x["nkc_rows"])[:20],
        "hint": "NKC references party_code via TK 131/331 but no Customer/"
                "Supplier exists. Re-run derive_masters_for_batch.",
    }

    # ─── G: Unmapped Item (in BR/MV/SCT) ─────────────────────────────
    item_rows = frappe.db.sql(
        """SELECT JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Mã hàng"')) AS code,
                  JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Tên hàng"')) AS name,
                  COUNT(*) AS n
           FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type IN ('Bang ke BR','Bang ke MV','SCT','OB Inventory')
           AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Mã hàng"')) IS NOT NULL
           AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Mã hàng"')) != ''
           GROUP BY code, name""",
        (batch_name,), as_dict=True,
    )
    unmapped_items: list[dict] = []
    for r in item_rows:
        code = (r["code"] or "").strip()
        if not code:
            continue
        sanitized = code.replace("<", "-").replace(">", "-") if ("<" in code or ">" in code) else code
        if not frappe.db.exists("Item", sanitized):
            unmapped_items.append({"code": code, "name": r["name"], "rows": r["n"]})
    out["categories"]["G_unmapped_item"] = {
        "count": len(unmapped_items),
        "samples": sorted(unmapped_items, key=lambda x: -x["rows"])[:20],
        "hint": "Item code in BR/MV/SCT/OB Inventory not in Item master. "
                "Re-run derive_masters_for_batch.",
    }

    # ─── H: Doc total vs NKC voucher sum mismatch ────────────────────
    # For each posted PI/SI/PE/SE, compare doc.grand_total/total_amount
    # vs NKC voucher's Σ Phát sinh Nợ.
    mismatches: list[dict] = []
    for dt, total_col in [
        ("Purchase Invoice", "grand_total"),
        ("Sales Invoice", "grand_total"),
        ("Payment Entry", "paid_amount"),
        ("Stock Entry", "total_amount"),
        ("Journal Entry", "total_debit"),
    ]:
        docs = frappe.db.sql(
            f"SELECT name, `{total_col}` AS amt, posting_date FROM `tab{dt}` WHERE company=%s",
            (company,), as_dict=True,
        )
        for d in docs:
            doc_amt = float(d["amt"] or 0)
            nkc_dr = frappe.db.sql(
                """SELECT SUM(CAST(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Phát sinh Nợ"')) AS DECIMAL(20,2)))
                   FROM `tabMisa Migration Row`
                   WHERE batch=%s AND file_type='NKC'
                   AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))=%s""",
                (batch_name, d["name"]),
            )[0][0]
            nkc_amt = float(nkc_dr or 0)
            if nkc_amt == 0:
                continue  # no NKC source — covered by category B
            diff = nkc_amt - doc_amt
            if abs(diff) > threshold_amount:
                mismatches.append({
                    "doctype": dt,
                    "name": d["name"],
                    "posting_date": str(d["posting_date"]),
                    "doc_total": doc_amt,
                    "nkc_sum_dr": nkc_amt,
                    "diff": diff,
                })
    out["categories"]["H_doc_total_vs_nkc_mismatch"] = {
        "count": len(mismatches),
        "samples": sorted(mismatches, key=lambda x: -abs(x["diff"]))[:30],
        "hint": "Posted doc's total differs from NKC voucher's Σ Phát sinh Nợ. "
                "Most common cause: PI/SI line items built with rate=0 because "
                "the BR/MV register lacked line amounts (service vouchers like "
                "MDV2). Need to extract amount from NKC instead of register.",
    }

    out["elapsed_seconds"] = round(time.time() - t0, 2)
    out["summary"] = {k: v["count"] for k, v in out["categories"].items()}
    return out


@frappe.whitelist()
def print_audit_report(batch_name: str, threshold_amount: float = 1000.0) -> str:
    """Pretty-print the audit. Returns text for accountant."""
    r = audit_source_data_gaps(batch_name, threshold_amount)
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append(f"SOURCE-DATA GAPS AUDIT — batch {r['batch_name']} — company {r['company']}")
    lines.append("=" * 100)
    lines.append(f"Threshold: > {r['threshold_amount']:,.0f} VND  ·  elapsed: {r['elapsed_seconds']}s")
    lines.append("")
    lines.append("SUMMARY (count by category):")
    for cat, n in r["summary"].items():
        marker = "✗" if n > 0 else "✓"
        lines.append(f"  {marker} {cat:<35s} : {n}")
    lines.append("")
    for cat, info in r["categories"].items():
        if info["count"] == 0:
            continue
        lines.append("─" * 100)
        lines.append(f"[{cat}]  count={info['count']}")
        if "total_amount" in info:
            lines.append(f"  total amount: {info['total_amount']:,.0f}")
        lines.append(f"  HINT: {info['hint']}")
        samples = info.get("samples", [])
        if samples:
            lines.append(f"  TOP {len(samples)} SAMPLES:")
            for s in samples:
                lines.append(f"    {json.dumps(s, default=str, ensure_ascii=False)[:200]}")
        lines.append("")
    return "\n".join(lines)
