"""Reconstruct VN Accounting Entry child rows from already-posted Journal Entry.

Records created before the inline-accounting feature (or via Session-11 manual
backfill) have `posted_je` set but `accounting_entries=[]`. This patch reads
the linked JE's accounts (ordered by idx) and pairs adjacent debit+credit rows
back into child entries — matching the order produced by
`post_je_from_entries()`.

Covers:
  - Asset Repair         (parent.posted_je)
  - CCDC Item            (parent.posted_je)
  - CCDC Writeoff        (parent.posted_je)

Idempotent: skips parents that already have rows.

Caveat: pairing assumes JE rows were appended in [debit, credit, debit, credit, …]
order, which is what `post_je_from_entries` does. JEs created by other means
(manual UI input, third-party scripts) may not pair cleanly — those records
are left untouched and logged as a warning.
"""
from __future__ import annotations

import frappe


_SOURCES = (
    ("Asset Repair", "VN Accounting Entry", "accounting_entries"),
    ("CCDC Item", "VN Accounting Entry", "accounting_entries"),
    ("CCDC Writeoff", "VN Accounting Entry", "accounting_entries"),
)


def _backfill_one(parent_doctype: str, parent_name: str, je_name: str) -> int:
    """Read JE accounts, pair them, write VN Accounting Entry rows. Returns row count."""
    accounts = frappe.db.sql(
        """SELECT account, debit_in_account_currency, credit_in_account_currency,
                  user_remark, party_type, party
           FROM `tabJournal Entry Account`
           WHERE parent = %s
           ORDER BY idx""",
        (je_name,),
        as_dict=True,
    )
    if not accounts or len(accounts) % 2 != 0:
        frappe.log_error(
            f"Cannot pair JE accounts: {je_name} has {len(accounts)} rows (expected even)",
            "v0_5_2 backfill",
        )
        return 0

    rows_created = 0
    for i in range(0, len(accounts), 2):
        d_row = accounts[i]
        c_row = accounts[i + 1]
        # Sanity: first must be debit-leg, second credit-leg
        if not (d_row.debit_in_account_currency and c_row.credit_in_account_currency):
            frappe.log_error(
                f"JE {je_name} row pair {i}/{i+1} not debit→credit; skipping",
                "v0_5_2 backfill",
            )
            continue
        amount = d_row.debit_in_account_currency
        # Heuristic: VAT row has account starting with "1331"
        is_vat = 1 if str(d_row.account or "").startswith("1331") else 0
        # Party_type/party comes from the credit-leg (e.g., TK 331 Payable)
        party_type = c_row.party_type or None
        party = c_row.party or None

        entry = frappe.get_doc({
            "doctype": "VN Accounting Entry",
            "parent": parent_name,
            "parenttype": parent_doctype,
            "parentfield": "accounting_entries",
            "account_debit": d_row.account,
            "account_credit": c_row.account,
            "amount": amount,
            "description": d_row.user_remark or c_row.user_remark or "",
            "is_vat": is_vat,
            "party_type": party_type,
            "party": party,
            "idx": (i // 2) + 1,
        })
        entry.flags.ignore_permissions = True
        entry.insert(ignore_links=True)
        rows_created += 1
    return rows_created


def execute() -> None:
    total_parents = 0
    total_rows = 0
    for parent_doctype, _child_dt, _child_field in _SOURCES:
        if not frappe.db.exists("DocType", parent_doctype):
            continue
        # Find parents with posted_je set + 0 child entries
        rows = frappe.db.sql(
            f"""SELECT p.name, p.posted_je
                FROM `tab{parent_doctype}` p
                LEFT JOIN `tabVN Accounting Entry` ae
                  ON ae.parent = p.name AND ae.parenttype = %s
                WHERE p.posted_je IS NOT NULL
                  AND p.posted_je != ''
                  AND p.docstatus IN (1, 2)
                GROUP BY p.name, p.posted_je
                HAVING COUNT(ae.name) = 0""",
            (parent_doctype,),
            as_dict=True,
        )
        for r in rows:
            if not frappe.db.exists("Journal Entry", r.posted_je):
                continue
            try:
                created = _backfill_one(parent_doctype, r.name, r.posted_je)
                if created:
                    total_parents += 1
                    total_rows += created
            except Exception as exc:
                frappe.log_error(
                    f"v0_5_2 backfill {parent_doctype} {r.name}: {exc}",
                    "v0_5_2 backfill",
                )
    if total_parents:
        frappe.db.commit()
        print(f"v0_5_2: backfilled {total_rows} entries across {total_parents} parents")
