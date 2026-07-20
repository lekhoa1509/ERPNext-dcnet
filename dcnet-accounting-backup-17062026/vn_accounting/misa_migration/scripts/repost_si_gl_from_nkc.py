"""Re-post Sales Invoice GL Entries from Misa NKC source.

Misa source booking model for telecom companies uses DEFERRED revenue
(Dr 131 / Cr 3387) for prepaid services + DIRECT revenue (Dr 131 /
Cr 51131-51136) for monthly recognition. Default ERPNext SI Item routing
puts everything to a single ``income_account`` field — losing the per-line
TK split that the source preserves.

This script re-derives the correct GL for each SI from NKC:

  For each Sales Invoice ``voucher_no`` matching a Misa ``Số chứng từ``:
    1. Read NKC rows whose ``Tài khoản=131`` AND ``Phát sinh Nợ > 0``
       (the authoritative leg — counter is the income/deferred/VAT TK).
    2. Group by counter-TK → revenue split.
    3. DELETE existing GL Entries for that voucher_no + INSERT correct ones.

Idempotent: re-running rewrites GL to match source — safe on repeat.

Public entry: ``repost_si_gl_from_nkc(company, batch_name)`` —
also whitelisted.
"""
from __future__ import annotations

import json
import secrets
from typing import Any

import frappe


def _gen_name() -> str:
    return secrets.token_hex(10)


def _net_legs_from_nkc(rows: list[dict]) -> dict[str, float]:
    """Extract 131-Dr leg counterparties from NKC rows.

    Returns ``{counter_tk: amount}`` where amount is summed Dr on 131.
    """
    out: dict[str, float] = {}
    for r in rows:
        try:
            p = json.loads(r["raw_payload"])
        except Exception:
            continue
        tk = str(p.get("Tài khoản") or "").strip()
        tkdu = str(p.get("TK đối ứng") or "").strip()
        try:
            dr = float(p.get("Phát sinh Nợ") or 0)
        except Exception:
            dr = 0
        if tk == "131" and dr > 0 and tkdu:
            out[tkdu] = out.get(tkdu, 0.0) + dr
    return out


def _resolve_account(tk: str, company: str) -> str | None:
    """Resolve TK code to Account name in company. Try exact first, then prefix."""
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


@frappe.whitelist()
def repost_si_gl_from_nkc(company: str, batch_name: str) -> dict[str, Any]:
    """Rewrite SI GL Entries from Misa NKC source.

    Args:
      company: Company.name
      batch_name: Misa Migration Batch

    Returns:
      Summary dict with reposted / skipped / unmatched counts.
    """
    if not company:
        frappe.throw(frappe._("Phải chọn Company."))
    if not batch_name:
        frappe.throw(frappe._("Phải chọn batch."))

    # Find all NKC rows for SI vouchers (BH%) grouped by voucher
    nkc_by_voucher: dict[str, list[dict]] = {}
    nkc_rows = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
           AND JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')) LIKE 'BH%%'
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
        if not sct:
            continue
        nkc_by_voucher.setdefault(sct, []).append(r)

    # Process each SI in DB
    si_vouchers = frappe.db.sql_list(
        """SELECT DISTINCT voucher_no FROM `tabGL Entry`
           WHERE company=%s AND voucher_type='Sales Invoice' AND is_cancelled=0
        """,
        (company,),
    )

    reposted = 0
    skipped = 0
    unmatched = 0
    errors: list[str] = []
    total_amount = 0.0

    for si_name in si_vouchers:
        nkc = nkc_by_voucher.get(si_name)
        if not nkc:
            unmatched += 1
            continue
        legs = _net_legs_from_nkc(nkc)
        if not legs:
            skipped += 1
            continue

        # Resolve current GL row (one of them) — copy metadata
        meta_row = frappe.db.sql(
            """SELECT posting_date, fiscal_year, party_type, party,
                      against_voucher_type, against_voucher,
                      cost_center, project
               FROM `tabGL Entry` WHERE voucher_no=%s AND company=%s
                                  AND voucher_type='Sales Invoice' AND is_cancelled=0
               LIMIT 1""",
            (si_name, company),
            as_dict=True,
        )
        if not meta_row:
            skipped += 1
            continue
        meta = meta_row[0]

        # Resolve 131 Dr account (customer receivable)
        acct_131 = _resolve_account("131", company)
        if not acct_131:
            errors.append(f"{si_name}: cannot resolve 131")
            skipped += 1
            continue

        # Build new legs: Dr 131 (total) + Cr (each counter TK)
        total_dr = sum(legs.values())
        new_legs: list[tuple[str, float, float]] = []  # (acct, dr, cr)
        new_legs.append((acct_131, total_dr, 0.0))
        for tk, amt in legs.items():
            acct = _resolve_account(tk, company)
            if not acct:
                errors.append(f"{si_name}: cannot resolve TK {tk}")
                break
            new_legs.append((acct, 0.0, amt))
        else:
            # All legs resolved — proceed with overwrite
            now = frappe.utils.now()
            # Delete current GL for this SI
            frappe.db.sql(
                """DELETE FROM `tabGL Entry`
                   WHERE voucher_no=%s AND voucher_type='Sales Invoice'
                         AND company=%s""",
                (si_name, company),
            )
            # Insert new GL
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
                    "voucher_type": "Sales Invoice", "voucher_no": si_name,
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
                    "remarks": f"SI {si_name} re-routed from NKC source",
                }
                cols = ",".join(f"`{k}`" for k in row.keys())
                ph = ",".join(["%s"] * len(row))
                frappe.db.sql(
                    f"INSERT INTO `tabGL Entry` ({cols}) VALUES ({ph})",
                    tuple(row.values()),
                )
            reposted += 1
            total_amount += total_dr
            continue
        # else branch above — broke out due to unresolved TK
        skipped += 1

    frappe.db.commit()
    return {
        "reposted": reposted,
        "skipped": skipped,
        "unmatched_no_nkc": unmatched,
        "total_amount_reposted": total_amount,
        "errors": errors[:50],
    }
