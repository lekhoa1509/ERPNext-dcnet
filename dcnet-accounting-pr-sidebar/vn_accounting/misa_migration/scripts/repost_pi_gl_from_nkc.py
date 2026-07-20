"""Re-post Purchase Invoice GL Entries from Misa NKC source.

Misa NKC for PI vouchers (MDV%/MH%) splits a single invoice into N legs:
each line goes to its own expense/asset TK (6322, 6323, 242, 1331, 156, …).
The PI builder collapses these into single ``expense_account`` per line,
losing the per-line account split — especially the 6xxx (immediate
expense) vs 242 (deferred expense) distinction.

This script rebuilds PI GL from NKC by reading the per-leg account
assignments directly.

For each Purchase Invoice ``voucher_no`` matching a Misa ``Số chứng từ``:
  1. Read NKC rows where ``Tài khoản=331`` AND ``Phát sinh Có > 0``
     (the supplier-payable Cr leg — counter is the expense/asset/VAT TK).
  2. Group by counter-TK → expense split.
  3. DELETE existing GL Entries for that voucher_no + INSERT correct ones.

Public entry: ``repost_pi_gl_from_nkc(company, batch_name)``.
"""
from __future__ import annotations

import json
import secrets
from typing import Any

import frappe


def _gen_name() -> str:
    return secrets.token_hex(10)


def _resolve_account(tk: str, company: str) -> str | None:
    nm = frappe.db.get_value(
        "Account",
        {"account_number": tk, "company": company, "is_group": 0},
        "name",
    )
    if nm:
        return nm
    rows = frappe.db.sql(
        "SELECT name FROM `tabAccount` WHERE company=%s AND is_group=0 "
        "AND (account_number=%s OR account_name LIKE %s) ORDER BY account_number LIMIT 1",
        (company, tk, f"{tk} - %%"),
    )
    return rows[0][0] if rows else None


def _net_legs_from_nkc(rows: list[dict]) -> tuple[dict[str, float], dict[str, float]]:
    """Extract Dr / Cr legs from NKC for a PI voucher.

    Standard PIs have one or more ``TK=331 Cr=X`` rows; each counter-TK
    becomes a Dr leg. Non-standard PIs (e.g. incident reimbursement) have
    no 331 leg — pair Dr legs with their TKDU counter directly.

    Returns ``(dr_legs, cr_legs)`` where each is ``{tk: amount}``.
    """
    # Collect all 331-Cr rows; their TKDUs are the Dr legs
    cr_331_legs: dict[str, float] = {}
    has_331 = False
    for r in rows:
        try:
            p = json.loads(r["raw_payload"])
        except Exception:
            continue
        tk = str(p.get("Tài khoản") or "").strip()
        tkdu = str(p.get("TK đối ứng") or "").strip()
        try:
            cr = float(p.get("Phát sinh Có") or 0)
        except Exception:
            cr = 0
        if tk == "331" and cr > 0 and tkdu:
            has_331 = True
            cr_331_legs[tkdu] = cr_331_legs.get(tkdu, 0.0) + cr
        elif tk == "331" and cr < 0 and tkdu:
            # Hóa đơn điều chỉnh giảm: Misa xuất chân ÂM (Cr 331 −X ≡ Dr 331
            # +X). Trừ vào cùng bucket — tổng Cr 331 của voucher giảm đúng X,
            # chân đối ứng (1331/642x) cũng âm theo ở mirror-pair phía dưới.
            # Trước đây cả voucher âm bị rớt toàn bộ chân → builder GL (thiếu
            # cặp VAT ±2,28M trên 1331↔331, ~15 hóa đơn tập 2025) giữ nguyên.
            has_331 = True
            cr_331_legs[tkdu] = cr_331_legs.get(tkdu, 0.0) + cr

    if has_331:
        # Standard PI: Dr = each counter TK, Cr = 331
        total_cr = sum(cr_331_legs.values())
        return cr_331_legs, {"331": total_cr}

    # Non-standard (no 331 leg): walk all "TK perspective" rows.
    # Pick rows where TK > TKDU alphabetically (canonical perspective)
    # — this picks exactly one of each mirror pair deterministically.
    dr_out: dict[str, float] = {}
    cr_out: dict[str, float] = {}
    for r in rows:
        try:
            p = json.loads(r["raw_payload"])
        except Exception:
            continue
        tk = str(p.get("Tài khoản") or "").strip()
        tkdu = str(p.get("TK đối ứng") or "").strip()
        try:
            dr = float(p.get("Phát sinh Nợ") or 0)
            cr = float(p.get("Phát sinh Có") or 0)
        except Exception:
            continue
        if not tk or not tkdu or (dr == 0 and cr == 0):
            continue
        # Canonical: keep row where TK alphabetically > TKDU
        if tk <= tkdu:
            continue
        # Chân âm (điều chỉnh giảm): Dr −X ≡ Cr +X — normalize trước khi
        # phân nhánh, nếu không cả 2 nhánh dưới đều rớt chân.
        if dr < 0:
            cr, dr = cr - dr, 0.0
        if cr < 0:
            dr, cr = dr - cr, 0.0
        if dr > 0:
            dr_out[tk] = dr_out.get(tk, 0.0) + dr
            cr_out[tkdu] = cr_out.get(tkdu, 0.0) + dr
        elif cr > 0:
            cr_out[tk] = cr_out.get(tk, 0.0) + cr
            dr_out[tkdu] = dr_out.get(tkdu, 0.0) + cr
    return dr_out, cr_out


@frappe.whitelist()

def _voucher_lookup_key(doc_name: str, company: str) -> str:
    """Misa voucher number for a migrated doc.

    Fresh-company runs name docs ``{abbr}-{voucher_no}`` (namespacing, so two
    companies' overlapping Misa numbers don't collide) while NKC rows carry
    the bare ``Số chứng từ``. Strip the abbr prefix when present."""
    import re as _re
    abbr = frappe.get_cached_value("Company", company, "abbr") or ""
    prefix = f"{abbr}-"
    key = doc_name[len(prefix):] if abbr and doc_name.startswith(prefix) else doc_name
    # Amended docs (PE backfill cancel+amend) carry a trailing "-1"/"-2" —
    # the Misa voucher number never does.
    return _re.sub(r"-\d+$", "", key)

def repost_pi_gl_from_nkc(company: str, batch_name: str) -> dict[str, Any]:
    if not company:
        frappe.throw(frappe._("Phải chọn Company."))
    if not batch_name:
        frappe.throw(frappe._("Phải chọn batch."))

    # NKC rows for PI vouchers (MDV%, MH%, NK%)
    nkc_by_voucher: dict[str, list[dict]] = {}
    nkc_rows = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
           AND (JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) LIKE 'MDV%%'
                OR JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) LIKE 'MH%%'
                OR JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) LIKE 'NK%%'
                OR JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) LIKE 'PN%%')
        """,
        (batch_name,),
        as_dict=True,
    )
    for r in nkc_rows:
        try:
            p = json.loads(r["raw_payload"])
        except Exception:
            continue
        sct = str(p.get("Số chứng từ") or "").strip()
        if sct:
            nkc_by_voucher.setdefault(sct, []).append(r)

    pi_vouchers = frappe.db.sql_list(
        """SELECT DISTINCT voucher_no FROM `tabGL Entry`
           WHERE company=%s AND voucher_type='Purchase Invoice' AND is_cancelled=0
        """,
        (company,),
    )
    # ALSO cover submitted PIs with NO GL at all — the handler can build a
    # zero-amount PI when no bảng kê line matches (grand_total=0 → ERPNext
    # writes no GL). Those vouchers' NKC legs (Dr 6xx/1331 / Cr 331) are
    # otherwise lost entirely (194 PIs ≈ 463M trên TK 331, E2E 2026-06-11).
    no_gl = frappe.db.sql_list(
        """SELECT pi.name FROM `tabPurchase Invoice` pi
           LEFT JOIN `tabGL Entry` g
                  ON g.voucher_no = pi.name AND g.is_cancelled = 0
           WHERE pi.company=%s AND pi.docstatus=1 AND g.name IS NULL""",
        (company,),
    )
    pi_vouchers = list(dict.fromkeys(list(pi_vouchers) + list(no_gl)))

    reposted = skipped = unmatched = 0
    errors: list[str] = []

    for pi_name in pi_vouchers:
        nkc = nkc_by_voucher.get(pi_name) or nkc_by_voucher.get(_voucher_lookup_key(pi_name, company))
        if not nkc:
            unmatched += 1
            continue
        dr_legs, cr_legs = _net_legs_from_nkc(nkc)
        if not dr_legs and not cr_legs:
            skipped += 1
            continue
        meta_row = frappe.db.sql(
            """SELECT posting_date, fiscal_year, party_type, party,
                      against_voucher_type, against_voucher,
                      cost_center, project
               FROM `tabGL Entry` WHERE voucher_no=%s AND company=%s
                                  AND voucher_type='Purchase Invoice' AND is_cancelled=0
               LIMIT 1""",
            (pi_name, company), as_dict=True,
        )
        if not meta_row:
            # Zero-GL PI — derive meta from the document itself.
            pid = frappe.db.get_value(
                "Purchase Invoice", pi_name,
                ["posting_date", "supplier", "cost_center", "project"],
                as_dict=True,
            )
            if not pid or not pid.posting_date:
                skipped += 1
                continue
            meta = {
                "posting_date": pid.posting_date,
                "fiscal_year": str(pid.posting_date.year),
                "party_type": "Supplier", "party": pid.supplier,
                "against_voucher_type": "", "against_voucher": "",
                "cost_center": pid.cost_center or "", "project": pid.project or "",
            }
        else:
            meta = meta_row[0]

        new_legs: list[tuple[str, float, float]] = []
        all_resolved = True
        for tk, amt in dr_legs.items():
            acct = _resolve_account(tk, company)
            if not acct:
                errors.append(f"{pi_name}: cannot resolve Dr TK {tk}")
                all_resolved = False
                break
            new_legs.append((acct, amt, 0.0))
        if all_resolved:
            for tk, amt in cr_legs.items():
                acct = _resolve_account(tk, company)
                if not acct:
                    errors.append(f"{pi_name}: cannot resolve Cr TK {tk}")
                    all_resolved = False
                    break
                new_legs.append((acct, 0.0, amt))
        if not all_resolved:
            skipped += 1
            continue

        now = frappe.utils.now()
        frappe.db.sql(
            """DELETE FROM `tabGL Entry`
               WHERE voucher_no=%s AND voucher_type='Purchase Invoice'
                     AND company=%s""",
            (pi_name, company),
        )
        for acct, dr, cr in new_legs:
            row = {
                "name": _gen_name(),
                "creation": now, "modified": now,
                "owner": "Administrator", "modified_by": "Administrator",
                "docstatus": 1, "idx": 0,
                "posting_date": meta["posting_date"],
                "transaction_date": meta["posting_date"],
                "fiscal_year": meta.get("fiscal_year") or "2026",
                "account": acct, "account_currency": "VND",
                "voucher_type": "Purchase Invoice", "voucher_no": pi_name,
                "transaction_currency": "VND",
                "transaction_exchange_rate": 1.0,
                "reporting_currency_exchange_rate": 1.0,
                "debit": dr, "debit_in_account_currency": dr,
                "debit_in_transaction_currency": dr,
                "debit_in_reporting_currency": dr,
                "credit": cr, "credit_in_account_currency": cr,
                "credit_in_transaction_currency": cr,
                "credit_in_reporting_currency": cr,
                "company": company, "is_opening": "No",
                "is_advance": "No", "is_cancelled": 0,
                "party_type": meta.get("party_type") or "",
                "party": meta.get("party") or "",
                "against_voucher_type": meta.get("against_voucher_type") or "",
                "against_voucher": meta.get("against_voucher") or "",
                "cost_center": meta.get("cost_center") or "",
                "project": meta.get("project") or "",
                "remarks": f"PI {pi_name} re-routed from NKC source",
            }
            cols = ",".join(f"`{k}`" for k in row.keys())
            ph = ",".join(["%s"] * len(row))
            frappe.db.sql(
                f"INSERT INTO `tabGL Entry` ({cols}) VALUES ({ph})",
                tuple(row.values()),
            )
        reposted += 1

    frappe.db.commit()
    return {
        "reposted": reposted, "skipped": skipped,
        "unmatched_no_nkc": unmatched, "errors": errors[:50],
    }
