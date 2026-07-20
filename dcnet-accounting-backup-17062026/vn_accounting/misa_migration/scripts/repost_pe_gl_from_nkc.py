"""Re-post Payment Entry GL Entries from Misa NKC source.

Misa NKC frequently splits a single UNC voucher into N sub-legs (e.g.,
one UNC paying 3 different TNCN sub-amounts to TK 3335 in a single
banking transaction). The PE builder consolidates these into a single
PE.references row, losing the per-leg GL detail.

This script re-derives the correct GL for each PE from NKC by reading
all legs and rebuilding the GL pair (party-account Dr/Cr + bank Cr/Dr).

For each Payment Entry whose ``voucher_no`` matches a Misa ``Số chứng từ``:
  1. Read NKC rows for that voucher.
  2. Dedupe mirrors (keep only the leg where Phát sinh != 0 with a
     bank/cash TK on the bank side).
  3. DELETE existing GL Entries for that voucher_no + INSERT correct ones.

Idempotent: re-running rewrites GL to match source.

Public entry: ``repost_pe_gl_from_nkc(company, batch_name)``.
"""
from __future__ import annotations

import json
import secrets
from typing import Any

import frappe


BANK_PREFIXES = ("111", "112")


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


def _classify_pair(tk: str, tkdu: str) -> tuple[str, str] | None:
    """Identify which TK is the bank side and which is the party/expense side.

    Returns (bank_tk, party_tk) or None if pair doesn't include a bank.
    """
    tk_is_bank = any(tk.startswith(p) for p in BANK_PREFIXES)
    tkdu_is_bank = any(tkdu.startswith(p) for p in BANK_PREFIXES)
    if tk_is_bank and not tkdu_is_bank:
        return tk, tkdu
    if tkdu_is_bank and not tk_is_bank:
        return tkdu, tk
    return None


@frappe.whitelist()
def repost_pe_gl_from_nkc(company: str, batch_name: str) -> dict[str, Any]:
    """Rewrite Payment Entry GL Entries from Misa NKC source.

    Args:
      company: Company.name
      batch_name: Misa Migration Batch

    Returns:
      Summary dict.
    """
    if not company:
        frappe.throw(frappe._("Phải chọn Company."))
    if not batch_name:
        frappe.throw(frappe._("Phải chọn batch."))

    # All PE voucher_nos in DB (UNC% / TT% / CTHM% patterns from Misa)
    pe_vouchers = frappe.db.sql_list(
        """SELECT DISTINCT voucher_no FROM `tabGL Entry`
           WHERE company=%s AND voucher_type='Payment Entry' AND is_cancelled=0
        """,
        (company,),
    )

    # Group NKC rows by Số chứng từ
    nkc_by_voucher: dict[str, list[dict]] = {}
    nkc_rows = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC'
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
            nkc_by_voucher.setdefault(sct, []).append(p)

    reposted = 0
    skipped = 0
    unmatched = 0
    errors: list[str] = []

    for pe_name in pe_vouchers:
        nkc = nkc_by_voucher.get(pe_name)
        if not nkc:
            unmatched += 1
            continue

        # Extract net legs: dedupe mirrors. Take only rows where the
        # TK side is the bank (Cr movement = bank pays out, Dr = bank receives)
        # OR if not bank, ensure we don't double-count via mirror pair.
        # Strategy: for each row, classify the (TK, TKDU) pair; keep one row
        # per (party_tk, amount, sign).
        seen: set = set()
        legs: list[tuple[str, str, float, float]] = []
        # Each leg: (bank_tk, party_tk, dr_on_bank, cr_on_bank)
        for p in nkc:
            tk = str(p.get("Tài khoản") or "").strip()
            tkdu = str(p.get("TK đối ứng") or "").strip()
            try:
                dr = float(p.get("Phát sinh Nợ") or 0)
                cr = float(p.get("Phát sinh Có") or 0)
            except Exception:
                continue
            classified = _classify_pair(tk, tkdu)
            if not classified:
                continue
            bank_tk, party_tk = classified
            # If TK is bank: Dr means money in, Cr means money out
            # If TKDU is bank: invert (because this row is the party perspective)
            if tk == bank_tk:
                bank_dr = dr
                bank_cr = cr
            else:
                # tkdu is bank, this row is from party perspective:
                # party Dr means bank Cr (bank pays out for the party)
                bank_dr = cr  # because party Cr means money received → bank Dr inverse
                bank_cr = dr
            # Dedupe key: (bank_tk, party_tk, bank_dr, bank_cr, description)
            desc_part = str(p.get("Diễn giải") or "")[:60]
            key = (bank_tk, party_tk, round(bank_dr, 2), round(bank_cr, 2), desc_part)
            if key in seen:
                continue
            seen.add(key)
            if bank_dr + bank_cr == 0:
                continue
            legs.append((bank_tk, party_tk, bank_dr, bank_cr))

        if not legs:
            skipped += 1
            continue

        # Resolve existing PE metadata
        meta_row = frappe.db.sql(
            """SELECT posting_date, fiscal_year, party_type, party,
                      against_voucher_type, against_voucher
               FROM `tabGL Entry` WHERE voucher_no=%s AND company=%s
                                  AND voucher_type='Payment Entry' AND is_cancelled=0
               LIMIT 1""",
            (pe_name, company),
            as_dict=True,
        )
        if not meta_row:
            skipped += 1
            continue
        meta = meta_row[0]

        # Resolve all account names upfront
        accts: dict[str, str | None] = {}
        for bank_tk, party_tk, _, _ in legs:
            if bank_tk not in accts:
                accts[bank_tk] = _resolve_account(bank_tk, company)
            if party_tk not in accts:
                accts[party_tk] = _resolve_account(party_tk, company)
        missing = [tk for tk, nm in accts.items() if not nm]
        if missing:
            errors.append(f"{pe_name}: cannot resolve TK(s) {missing}")
            skipped += 1
            continue

        # Build new GL: for each leg, 2 entries (bank + party)
        now = frappe.utils.now()
        # Delete existing GL
        frappe.db.sql(
            """DELETE FROM `tabGL Entry`
               WHERE voucher_no=%s AND voucher_type='Payment Entry'
                     AND company=%s""",
            (pe_name, company),
        )
        for bank_tk, party_tk, bank_dr, bank_cr in legs:
            # Bank side
            _insert_gl(
                accts[bank_tk], bank_dr, bank_cr,
                pe_name, meta, company, now,
            )
            # Party side: inverse
            _insert_gl(
                accts[party_tk], bank_cr, bank_dr,
                pe_name, meta, company, now,
            )
        reposted += 1

    frappe.db.commit()
    return {
        "reposted": reposted,
        "skipped": skipped,
        "unmatched_no_nkc": unmatched,
        "errors": errors[:50],
    }


def _insert_gl(account: str, dr: float, cr: float, voucher_no: str,
               meta: dict, company: str, now: str) -> None:
    row = {
        "name": _gen_name(),
        "creation": now, "modified": now,
        "owner": "Administrator", "modified_by": "Administrator",
        "docstatus": 1, "idx": 0,
        "posting_date": meta["posting_date"],
        "transaction_date": meta["posting_date"],
        "fiscal_year": meta.get("fiscal_year") or "2026",
        "account": account, "account_currency": "VND",
        "voucher_type": "Payment Entry", "voucher_no": voucher_no,
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
        "remarks": f"PE {voucher_no} re-routed from NKC source",
    }
    cols = ",".join(f"`{k}`" for k in row.keys())
    ph = ",".join(["%s"] * len(row))
    frappe.db.sql(
        f"INSERT INTO `tabGL Entry` ({cols}) VALUES ({ph})",
        tuple(row.values()),
    )
