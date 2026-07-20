"""Post-INSERT derivation: rebuild Bin + Payment Ledger Entry from raw rows.

Bin = per-item-warehouse aggregate of SLE (actual_qty, valuation_rate, stock_value).
Payment Ledger Entry = mirror of GL Entry for party_type rows (Customer/Supplier).

Run AFTER all bulk_insert calls land — these consume the inserted SLE/GL rows.
"""
from __future__ import annotations

import secrets
import time

import frappe


def _gen_name() -> str:
    return secrets.token_hex(5)


def rebuild_bin_for_company(company: str) -> tuple[int, float]:
    """Drop + recompute tabBin from tabStock Ledger Entry for this Company.

    Idempotent: handles re-runs and orphan Bin rows from prior runs (where
    Bin.warehouse no longer maps to tabWarehouse). Strategy:
      1. DELETE Bin rows whose warehouse appears in this company's SLE,
         regardless of whether the warehouse still exists in tabWarehouse.
      2. INSERT ... ON DUPLICATE KEY UPDATE on the deterministic MD5 name,
         so any straggler row not caught by DELETE is updated in place.
    """
    t0 = time.time()
    # Wider DELETE: by warehouse set FROM SLE (catches orphans whose
    # warehouse name doesn't currently join to tabWarehouse).
    frappe.db.sql(
        """DELETE FROM `tabBin` WHERE warehouse IN
           (SELECT DISTINCT warehouse FROM `tabStock Ledger Entry`
            WHERE company=%s)""",
        (company,),
    )
    frappe.db.sql(
        """
        INSERT INTO `tabBin` (name, creation, modified, modified_by, owner, docstatus, idx,
                              item_code, warehouse, actual_qty, valuation_rate, stock_value, stock_uom)
        SELECT
            SUBSTRING(MD5(CONCAT(item_code, '|', warehouse)), 1, 10),
            NOW(), NOW(), 'Administrator', 'Administrator', 0, 0,
            item_code, warehouse,
            SUM(actual_qty),
            CASE WHEN SUM(actual_qty) > 0 THEN SUM(stock_value_difference) / SUM(actual_qty) ELSE 0 END,
            SUM(stock_value_difference),
            MAX(stock_uom)
        FROM `tabStock Ledger Entry`
        WHERE company=%s AND is_cancelled=0
        GROUP BY item_code, warehouse
        ON DUPLICATE KEY UPDATE
            actual_qty=VALUES(actual_qty),
            valuation_rate=VALUES(valuation_rate),
            stock_value=VALUES(stock_value),
            stock_uom=VALUES(stock_uom),
            modified=NOW()
        """,
        (company,),
    )
    frappe.db.commit()
    n_inserted = frappe.db.sql(
        """SELECT COUNT(*) FROM `tabBin`
           WHERE warehouse IN (SELECT DISTINCT warehouse FROM `tabStock Ledger Entry`
                               WHERE company=%s)""",
        (company,),
    )[0][0]
    return n_inserted, time.time() - t0


def backfill_pe_references_for_company(company: str) -> tuple[int, dict]:
    """FIFO-allocate every PE without references to open SI/PI of the same party.

    Pure SQL/batch — no ORM cancel+amend. Inserts tabPayment Entry Reference
    rows + recomputes PE.total_allocated_amount/unallocated_amount + drains
    SI/PI.outstanding_amount + flips SI/PI.status.

    Returns (n_refs_inserted, summary_dict).
    """
    t0 = time.time()
    summary = {"linked": 0, "no_match": 0, "skipped": 0,
               "elapsed_seconds": 0.0}

    # Eligible PEs: docstatus=1, no existing references, Receive→131 / Pay→331
    pes = frappe.db.sql(
        """SELECT pe.name, pe.party_type, pe.party, pe.paid_amount,
                  pe.payment_type, pe.posting_date, pe.paid_from, pe.paid_to
           FROM `tabPayment Entry` pe
           LEFT JOIN `tabPayment Entry Reference` per ON per.parent=pe.name
           WHERE pe.company=%s AND pe.docstatus=1
             AND per.parent IS NULL
             AND pe.party_type IN ('Customer','Supplier')
             AND pe.party IS NOT NULL AND pe.party != ''
             AND (
                 (pe.payment_type='Pay' AND pe.paid_to LIKE '331%%')
                 OR (pe.payment_type='Receive' AND pe.paid_from LIKE '131%%')
             )""",
        (company,), as_dict=True,
    )
    if not pes:
        summary["elapsed_seconds"] = round(time.time() - t0, 2)
        return 0, summary

    # Preload open invoices per (party_type, party) — single bulk fetch then
    # group in Python instead of N+1 queries per PE.
    si_rows = frappe.db.sql(
        """SELECT name, customer AS party, outstanding_amount, posting_date
           FROM `tabSales Invoice`
           WHERE company=%s AND docstatus=1 AND outstanding_amount > 0
           ORDER BY posting_date ASC, name ASC""",
        (company,), as_dict=True,
    )
    pi_rows = frappe.db.sql(
        """SELECT name, supplier AS party, outstanding_amount, posting_date
           FROM `tabPurchase Invoice`
           WHERE company=%s AND docstatus=1 AND outstanding_amount > 0
           ORDER BY posting_date ASC, name ASC""",
        (company,), as_dict=True,
    )
    open_by_party: dict[tuple, list[dict]] = {}
    for r in si_rows:
        open_by_party.setdefault(("Customer", r["party"]), []).append(
            {"dt": "Sales Invoice", **r})
    for r in pi_rows:
        open_by_party.setdefault(("Supplier", r["party"]), []).append(
            {"dt": "Purchase Invoice", **r})

    # Build all allocation rows + invoice-drain map in memory
    ref_rows: list[dict] = []
    pe_alloc: dict[str, float] = {}      # pe_name → total_allocated
    inv_drain: dict[tuple, float] = {}    # (dt, name) → total taken
    now = frappe.utils.now()

    for pe in pes:
        invs = open_by_party.get((pe["party_type"], pe["party"]))
        if not invs:
            summary["no_match"] += 1
            continue
        remaining = float(pe["paid_amount"] or 0)
        idx = 1
        for inv in invs:
            if remaining <= 0.001:
                break
            avail = float(inv["outstanding_amount"] or 0) - inv_drain.get(
                (inv["dt"], inv["name"]), 0.0)
            if avail <= 0.001:
                continue
            take = min(avail, remaining)
            ref_rows.append({
                "name": secrets.token_hex(5),
                "creation": now, "modified": now,
                "owner": "Administrator", "modified_by": "Administrator",
                "docstatus": 1, "idx": idx,
                "reference_doctype": inv["dt"],
                "reference_name": inv["name"],
                "allocated_amount": take,
                "total_amount": float(inv["outstanding_amount"] or 0),
                "outstanding_amount": avail - take,
                "due_date": inv["posting_date"],
                "exchange_rate": 1.0, "exchange_gain_loss": 0,
                "account": pe["paid_from"] if pe["payment_type"] == "Receive"
                           else pe["paid_to"],
                "account_type": ("Receivable" if pe["payment_type"] == "Receive"
                                 else "Payable"),
                "payment_type": pe["payment_type"],
                "parent": pe["name"],
                "parenttype": "Payment Entry",
                "parentfield": "references",
            })
            inv_drain[(inv["dt"], inv["name"])] = inv_drain.get(
                (inv["dt"], inv["name"]), 0.0) + take
            pe_alloc[pe["name"]] = pe_alloc.get(pe["name"], 0.0) + take
            remaining -= take
            idx += 1
        if pe_alloc.get(pe["name"], 0) > 0:
            summary["linked"] += 1
        else:
            summary["no_match"] += 1

    if ref_rows:
        from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
        bulk_insert("Payment Entry Reference", ref_rows, batch_size=500)

    # Bulk-update PE.total_allocated_amount + unallocated_amount
    for pe_name, alloc in pe_alloc.items():
        frappe.db.sql(
            """UPDATE `tabPayment Entry`
               SET total_allocated_amount=%s, base_total_allocated_amount=%s,
                   unallocated_amount=GREATEST(paid_amount - %s, 0)
               WHERE name=%s""",
            (alloc, alloc, alloc, pe_name),
        )

    # Bulk-drain SI/PI outstanding + flip status
    si_drain = [(name, taken) for (dt, name), taken in inv_drain.items() if dt == "Sales Invoice"]
    pi_drain = [(name, taken) for (dt, name), taken in inv_drain.items() if dt == "Purchase Invoice"]
    for name, taken in si_drain:
        frappe.db.sql(
            """UPDATE `tabSales Invoice`
               SET outstanding_amount=GREATEST(outstanding_amount - %s, 0),
                   status=CASE
                     WHEN outstanding_amount - %s <= 0.01 THEN 'Paid'
                     ELSE 'Partly Paid'
                   END
               WHERE name=%s""", (taken, taken, name),
        )
    for name, taken in pi_drain:
        frappe.db.sql(
            """UPDATE `tabPurchase Invoice`
               SET outstanding_amount=GREATEST(outstanding_amount - %s, 0),
                   status=CASE
                     WHEN outstanding_amount - %s <= 0.01 THEN 'Paid'
                     ELSE 'Partly Paid'
                   END
               WHERE name=%s""", (taken, taken, name),
        )
    frappe.db.commit()

    summary["elapsed_seconds"] = round(time.time() - t0, 2)
    return len(ref_rows), summary


def rebuild_payment_ledger_entry_for_company(company: str) -> tuple[int, float]:
    """Generate tabPayment Ledger Entry from tabGL Entry party rows."""
    t0 = time.time()
    frappe.db.sql(
        "DELETE FROM `tabPayment Ledger Entry` WHERE company=%s", (company,),
    )
    # PLE mirrors GL for Customer/Supplier party rows on Receivable/Payable accounts
    frappe.db.sql(
        """
        INSERT INTO `tabPayment Ledger Entry` (
            name, creation, modified, modified_by, owner, docstatus, idx,
            posting_date, account_type, account, party_type, party,
            voucher_type, voucher_no, against_voucher_type, against_voucher_no,
            amount, amount_in_account_currency, account_currency, company, delinked
        )
        SELECT
            MD5(g.name),
            NOW(), NOW(), 'Administrator', 'Administrator', 0, 0,
            g.posting_date,
            a.account_type,
            g.account, g.party_type, g.party,
            g.voucher_type, g.voucher_no,
            COALESCE(g.against_voucher_type, g.voucher_type),
            COALESCE(g.against_voucher, g.voucher_no),
            (g.debit - g.credit),
            (g.debit_in_account_currency - g.credit_in_account_currency),
            g.account_currency, g.company, 0
        FROM `tabGL Entry` g
        JOIN `tabAccount` a ON a.name = g.account
        WHERE g.company=%s AND g.is_cancelled=0
        AND g.party_type IN ('Customer','Supplier')
        AND a.account_type IN ('Receivable','Payable')
        """,
        (company,),
    )
    frappe.db.commit()
    n = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabPayment Ledger Entry` WHERE company=%s", (company,),
    )[0][0]
    return n, time.time() - t0
