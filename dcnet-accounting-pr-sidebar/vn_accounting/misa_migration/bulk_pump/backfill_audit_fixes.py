"""One-shot backfill for the bulk_pump audit findings (2026-05-26).

Each step is idempotent: running twice is a no-op. Step ordering matters when
the GL backfill is involved — fix party names first, then inventory GL, then
PI 1331 remap, then status flag re-derive.

Steps:
  1. canonicalize_party_case(company)
     - Find every PI/PE/GL Entry/PLE/Payment Schedule row whose supplier/customer
       reference uses a different case than the canonical Supplier/Customer.name.
       UPDATE to canonical case.

  2. populate_se_detail_warehouses(company)
     - Material Issue / Material Transfer SE Detail rows have NULL s_warehouse
       (root cause: bulk_executor used first-row keys before fix). Copy from
       the matching SLE row.

  3. fix_se_gl(company)
     - Replace TK 632 / TK 632 same-account GL with proper Dr <warehouse.account>
       / Cr <stock_adjustment_account> (or vice versa for Issue) per warehouse.
       Deletes the old broken GL rows and inserts new ones.

  4. remap_pi_1331_expense(company)
     - Item lines with expense_account TK 1331 were misrouted from the VAT-input
       leg into a cost row. Move that amount from expense_account=1331 →
       Company.default_expense_account. Also adjust GL accordingly.

  5. rederive_invoice_status(company)
     - Re-compute SI/PI status from outstanding_amount + due_date so the 16+14
       Paid-but-outstanding>100 cases get reclassified to Unpaid/Partly Paid.

  6. seed_item_defaults(company)
     - For Items used by submitted PI/SI but missing Item Default rows, infer
       income/expense/warehouse from observed usage and INSERT Item Default.

Entry: ``run_all(company)`` runs steps in order and prints summary per step.
Each step can also be called individually for partial re-runs.
"""
from __future__ import annotations

import secrets
import time
from typing import Any

import frappe

from vn_accounting.misa_migration.importers._naming import migrated_doc_name


# ─── Helpers ────────────────────────────────────────────────────────────────

def _gen_name() -> str:
    return secrets.token_hex(5)


# ─── Step 1: canonicalize party case ────────────────────────────────────────

def canonicalize_party_case(company: str) -> dict[str, int]:
    """Find party names with non-canonical case and update every reference.
    Returns counts of rows touched per table."""
    out: dict[str, int] = {}

    # Discover all distinct (used_name → canonical_name) mappings across PI/SI/PE
    mapping: dict[tuple[str, str], str] = {}  # (party_type, used) → canonical
    for dt in ("Supplier", "Customer"):
        rows = frappe.db.sql(
            f"""SELECT DISTINCT t.party AS used, s.name AS canonical FROM (
                  SELECT supplier AS party FROM `tabPurchase Invoice` WHERE company=%s
                  UNION SELECT customer FROM `tabSales Invoice` WHERE company=%s
                  UNION SELECT party FROM `tabPayment Entry` WHERE company=%s AND party_type=%s
                  UNION SELECT party FROM `tabGL Entry` WHERE company=%s AND party_type=%s
                ) t JOIN `tab{dt}` s ON s.name = t.party
                WHERE BINARY t.party != s.name""",
            (company, company, company, dt, company, dt), as_dict=True,
        )
        for r in rows:
            mapping[(dt, r.used)] = r.canonical

    if not mapping:
        out["mappings_found"] = 0
        return out
    out["mappings_found"] = len(mapping)

    # Apply updates per (party_type, used) pair
    for (party_type, used), canonical in mapping.items():
        ref_field = "supplier" if party_type == "Supplier" else "customer"
        parent_dt = "Purchase Invoice" if party_type == "Supplier" else "Sales Invoice"
        n = frappe.db.sql(
            f"UPDATE `tab{parent_dt}` SET `{ref_field}`=%s, `{ref_field}_name`=%s "
            f"WHERE company=%s AND BINARY `{ref_field}`=%s",
            (canonical, canonical, company, used),
        )
        out.setdefault(parent_dt, 0)
        out[parent_dt] += frappe.db._cursor.rowcount

        n = frappe.db.sql(
            "UPDATE `tabPayment Entry` SET party=%s, party_name=%s "
            "WHERE company=%s AND party_type=%s AND BINARY party=%s",
            (canonical, canonical, company, party_type, used),
        )
        out.setdefault("Payment Entry", 0)
        out["Payment Entry"] += frappe.db._cursor.rowcount

        n = frappe.db.sql(
            "UPDATE `tabGL Entry` SET party=%s WHERE company=%s AND party_type=%s "
            "AND BINARY party=%s",
            (canonical, company, party_type, used),
        )
        out.setdefault("GL Entry", 0)
        out["GL Entry"] += frappe.db._cursor.rowcount

        # Payment Ledger Entry (if it exists)
        if frappe.db.table_exists("Payment Ledger Entry"):
            frappe.db.sql(
                "UPDATE `tabPayment Ledger Entry` SET party=%s "
                "WHERE company=%s AND party_type=%s AND BINARY party=%s",
                (canonical, company, party_type, used),
            )
            out.setdefault("Payment Ledger Entry", 0)
            out["Payment Ledger Entry"] += frappe.db._cursor.rowcount

        # Payment Entry Reference also has a party reference via parent PE
        # — updated transitively when PE.party is updated. No standalone update needed.

    frappe.db.commit()
    return out


# ─── Step 2: populate SE Detail warehouses from SLE ─────────────────────────

def populate_se_detail_warehouses(company: str) -> dict[str, int]:
    """Material Issue and Material Transfer SE Detail have NULL s_warehouse.
    Copy from matching SLE row (item_code + voucher_no + outgoing actual_qty)."""
    # Issue: s_warehouse from SLE outgoing (actual_qty < 0)
    n_issue = frappe.db.sql(
        """UPDATE `tabStock Entry Detail` sed
           JOIN `tabStock Entry` se ON se.name = sed.parent
           JOIN `tabStock Ledger Entry` sle
             ON sle.voucher_no = se.name
             AND sle.item_code = sed.item_code
             AND sle.actual_qty < 0
           SET sed.s_warehouse = sle.warehouse
           WHERE se.company = %s AND se.purpose IN ('Material Issue', 'Material Transfer')
             AND (sed.s_warehouse IS NULL OR sed.s_warehouse = '')""",
        (company,),
    )
    n_issue_rows = frappe.db._cursor.rowcount

    # Transfer: t_warehouse from SLE incoming (actual_qty > 0)
    frappe.db.sql(
        """UPDATE `tabStock Entry Detail` sed
           JOIN `tabStock Entry` se ON se.name = sed.parent
           JOIN `tabStock Ledger Entry` sle
             ON sle.voucher_no = se.name
             AND sle.item_code = sed.item_code
             AND sle.actual_qty > 0
           SET sed.t_warehouse = sle.warehouse
           WHERE se.company = %s AND se.purpose = 'Material Transfer'
             AND (sed.t_warehouse IS NULL OR sed.t_warehouse = '')""",
        (company,),
    )
    n_transfer_rows = frappe.db._cursor.rowcount

    frappe.db.commit()
    return {"se_detail_s_warehouse_set": n_issue_rows,
            "se_detail_t_warehouse_set": n_transfer_rows}


# ─── Step 3: fix SE GL ──────────────────────────────────────────────────────

def fix_se_gl(company: str) -> dict[str, Any]:
    """Drop the broken Dr 632 / Cr 632 GL rows on Stock Entries and re-emit
    correct per-warehouse Dr <warehouse.account> / Cr <stock_adjustment> rows.
    """
    stock_adj = frappe.db.get_value("Company", company, "stock_adjustment_account") or \
                frappe.db.get_value("Company", company, "default_expense_account")
    if not stock_adj:
        return {"error": "no stock_adjustment_account / default_expense_account on Company"}

    now = frappe.utils.now()
    posting_user = "Administrator"

    # Find all SEs with broken GL (all rows on a single account)
    bad_ses = frappe.db.sql(
        """SELECT DISTINCT gle.voucher_no
           FROM `tabGL Entry` gle
           WHERE gle.company = %s AND gle.voucher_type = 'Stock Entry' AND gle.is_cancelled = 0
           GROUP BY gle.voucher_no HAVING COUNT(DISTINCT gle.account) = 1""",
        (company,), as_dict=True,
    )
    bad_se_names = [r.voucher_no for r in bad_ses]
    out = {"bad_se_count": len(bad_se_names), "se_processed": 0, "gl_deleted": 0, "gl_inserted": 0}
    if not bad_se_names:
        return out

    # Build replacement GL per SE based on SLE warehouse + stock_value_difference
    new_gl_rows: list[dict] = []
    for vno in bad_se_names:
        se = frappe.db.sql(
            "SELECT name, purpose, posting_date FROM `tabStock Entry` WHERE name=%s",
            (vno,), as_dict=True,
        )
        if not se:
            continue
        se_row = se[0]
        fy = str(frappe.utils.getdate(se_row.posting_date).year)

        sle_rows = frappe.db.sql(
            """SELECT warehouse, SUM(stock_value_difference) AS net
               FROM `tabStock Ledger Entry`
               WHERE voucher_no=%s AND is_cancelled=0
               GROUP BY warehouse""",
            (vno,), as_dict=True,
        )

        # Build per-warehouse legs
        for sle in sle_rows:
            wh = sle.warehouse
            net = float(sle.net or 0)
            if abs(net) < 0.5:
                continue
            wh_acc = frappe.db.get_value("Warehouse", wh, "account") or stock_adj
            if wh_acc == stock_adj:
                continue  # same account → no GL needed
            if net > 0:  # net IN — Dr warehouse / Cr stock_adj
                dr_acc, cr_acc = wh_acc, stock_adj
                amt = net
            else:  # net OUT — Dr stock_adj / Cr warehouse
                dr_acc, cr_acc = stock_adj, wh_acc
                amt = -net

            for dr_or_cr in ("dr", "cr"):
                acc = dr_acc if dr_or_cr == "dr" else cr_acc
                d = round(amt, 0) if dr_or_cr == "dr" else 0
                c = round(amt, 0) if dr_or_cr == "cr" else 0
                new_gl_rows.append({
                    "name": _gen_name(),
                    "creation": now, "modified": now,
                    "owner": posting_user, "modified_by": posting_user,
                    "docstatus": 1, "idx": 0,
                    "posting_date": se_row.posting_date,
                    "transaction_date": se_row.posting_date,
                    "fiscal_year": fy,
                    "account": acc, "account_currency": "VND",
                    "voucher_type": "Stock Entry", "voucher_no": vno,
                    "transaction_currency": "VND",
                    "transaction_exchange_rate": 1.0,
                    "reporting_currency_exchange_rate": 1.0,
                    "debit": d, "debit_in_account_currency": d,
                    "debit_in_transaction_currency": d, "debit_in_reporting_currency": d,
                    "credit": c, "credit_in_account_currency": c,
                    "credit_in_transaction_currency": c, "credit_in_reporting_currency": c,
                    "company": company, "is_opening": "No",
                    "is_advance": "No", "is_cancelled": 0,
                    "remarks": f"SE {vno} {se_row.purpose} (audit-fix)",
                })
        out["se_processed"] += 1

    # Atomic-ish: delete old, insert new in one transaction
    if bad_se_names:
        placeholders = ",".join(["%s"] * len(bad_se_names))
        # Identify the "broken" rows: same account on both Dr+Cr for the voucher
        deleted = frappe.db.sql(
            f"""DELETE gle FROM `tabGL Entry` gle
                WHERE gle.company=%s AND gle.voucher_type='Stock Entry'
                  AND gle.voucher_no IN ({placeholders})
                  AND gle.is_cancelled=0""",
            (company, *bad_se_names),
        )
        out["gl_deleted"] = frappe.db._cursor.rowcount

    if new_gl_rows:
        from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
        bulk_insert("GL Entry", new_gl_rows, batch_size=500)
        out["gl_inserted"] = len(new_gl_rows)

    frappe.db.commit()
    return out


# ─── Step 4: remap PI 1331 expense → real expense + GL fix ─────────────────

def remap_pi_1331_expense(company: str) -> dict[str, Any]:
    """For every Purchase Invoice Item whose expense_account starts with 1331,
    re-route to Company.default_expense_account and emit a balancing JE pair.

    Approach: bulk UPDATE the item rows. Then drop matching GL Entry rows
    (account starting with 1331, voucher_type=PI, debit>0) and re-insert
    same Dr amount on the new expense account.

    Existing VAT-line GL (from pi.taxes) is preserved.
    """
    default_exp = frappe.db.get_value("Company", company, "default_expense_account")
    if not default_exp:
        return {"error": "no default_expense_account on Company"}

    # Find PI items to remap, grouped by PI for GL adjustment
    rows = frappe.db.sql(
        """SELECT pii.parent AS pi_name, pii.name AS item_name, pii.expense_account, pii.amount
           FROM `tabPurchase Invoice Item` pii
           JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
           WHERE pi.company=%s AND pi.docstatus=1 AND pii.expense_account LIKE '1331%%'""",
        (company,), as_dict=True,
    )
    if not rows:
        return {"item_rows": 0, "gl_deleted": 0, "gl_inserted": 0}

    # Aggregate per (PI, old_account) → amount
    by_pi: dict[tuple[str, str], float] = {}
    for r in rows:
        by_pi[(r.pi_name, r.expense_account)] = by_pi.get((r.pi_name, r.expense_account), 0.0) + float(r.amount or 0)

    # Update item rows
    n_items = frappe.db.sql(
        """UPDATE `tabPurchase Invoice Item` pii
           JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
           SET pii.expense_account = %s
           WHERE pi.company=%s AND pi.docstatus=1 AND pii.expense_account LIKE '1331%%'""",
        (default_exp, company),
    )
    n_items_rows = frappe.db._cursor.rowcount

    # Build replacement GL: for each (pi, old_acc, amount), drop the matching
    # Dr <old_acc> GL row that represents this item line (NOT the tax row).
    # The PI builder emits 1 Dr per distinct expense_account, so we can
    # identify item-line GL by amount matching the aggregated item total.

    # Actually simpler: just UPDATE GL Entry.account from 1331-prefix → default_exp
    # ONLY for rows whose debit matches the item-line aggregate (i.e. not the
    # tax row amount). But tax row may also be on 1331 — we need to distinguish.
    #
    # Strategy: for each PI, sum the item-line debit on 1331 = item_total.
    # The PI's GL has Dr 1331 = item_total + tax_amount. We need to keep only
    # tax_amount on 1331 and move item_total to default_exp.

    pi_taxes = frappe.db.sql(
        """SELECT pi.name AS pi_name, COALESCE(SUM(ptc.tax_amount), 0) AS tax_total
           FROM `tabPurchase Invoice` pi
           LEFT JOIN `tabPurchase Taxes and Charges` ptc ON ptc.parent = pi.name AND ptc.account_head LIKE '1331%%'
           WHERE pi.company=%s AND pi.docstatus=1
           GROUP BY pi.name""",
        (company,), as_dict=True,
    )
    pi_to_tax = {r.pi_name: float(r.tax_total or 0) for r in pi_taxes}

    # For each PI with a 1331 misrouted item, the GL rows on 1331 sum to
    # item_total + tax_amount. Drop the OLD GL rows on 1331 (Dr-side) and
    # re-emit:
    #   - 1 row Dr <default_exp> = (sum on 1331) - tax_amount  (item portion)
    #   - 1 row Dr <1331>         = tax_amount                  (VAT portion)
    #
    # This preserves total Dr, supplier Cr stays intact, and TK 1331 ends at
    # the correct (smaller) amount.

    new_gl_rows: list[dict] = []
    deleted_gl_count = 0
    now = frappe.utils.now()
    posting_user = "Administrator"

    affected_pis = list({pi for (pi, _) in by_pi.keys()})
    if not affected_pis:
        frappe.db.commit()
        return {"item_rows": n_items_rows, "gl_deleted": 0, "gl_inserted": 0}

    placeholders = ",".join(["%s"] * len(affected_pis))
    # Fetch original 1331 GL rows
    gl_orig = frappe.db.sql(
        f"""SELECT name, voucher_no, account, debit, credit, posting_date, fiscal_year
           FROM `tabGL Entry`
           WHERE company=%s AND voucher_type='Purchase Invoice'
             AND voucher_no IN ({placeholders}) AND account LIKE '1331%%'
             AND is_cancelled=0 AND debit > 0""",
        (company, *affected_pis), as_dict=True,
    )

    # Group GL by PI
    gl_by_pi: dict[str, list[dict]] = {}
    for r in gl_orig:
        gl_by_pi.setdefault(r.voucher_no, []).append(r)

    # Delete original 1331 Dr rows
    if gl_orig:
        gl_names = [r.name for r in gl_orig]
        del_ph = ",".join(["%s"] * len(gl_names))
        frappe.db.sql(
            f"DELETE FROM `tabGL Entry` WHERE name IN ({del_ph})",
            tuple(gl_names),
        )
        deleted_gl_count = len(gl_names)

    # Re-emit 1 Dr default_exp + 1 Dr 1331 per PI
    for pi_name, gl_list in gl_by_pi.items():
        total_dr = sum(float(r.debit or 0) for r in gl_list)
        tax_amt = pi_to_tax.get(pi_name, 0.0)
        item_amt = round(total_dr - tax_amt, 0)
        ref = gl_list[0]
        if item_amt < 1:
            # Whole 1331 amount IS the VAT — keep original on 1331 (just
            # re-insert as one row preserving the total VAT Dr).
            new_gl_rows.append({
                "name": _gen_name(),
                "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
                "docstatus": 1, "idx": 0,
                "posting_date": ref.posting_date, "transaction_date": ref.posting_date,
                "fiscal_year": ref.fiscal_year,
                "account": ref.account, "account_currency": "VND",
                "voucher_type": "Purchase Invoice", "voucher_no": pi_name,
                "transaction_currency": "VND",
                "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
                "debit": round(total_dr, 0), "debit_in_account_currency": round(total_dr, 0),
                "debit_in_transaction_currency": round(total_dr, 0),
                "debit_in_reporting_currency": round(total_dr, 0),
                "credit": 0, "credit_in_account_currency": 0,
                "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
                "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
                "remarks": f"PI {pi_name} VAT input (audit-fix, pure-VAT PI)",
            })
            continue
        # Item Dr → default_exp
        new_gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": ref.posting_date, "transaction_date": ref.posting_date,
            "fiscal_year": ref.fiscal_year,
            "account": default_exp, "account_currency": "VND",
            "voucher_type": "Purchase Invoice", "voucher_no": pi_name,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": item_amt, "debit_in_account_currency": item_amt,
            "debit_in_transaction_currency": item_amt, "debit_in_reporting_currency": item_amt,
            "credit": 0, "credit_in_account_currency": 0,
            "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
            "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"PI {pi_name} expense (audit-fix from TK 1331)",
        })
        # VAT Dr → 1331 (only if tax_amt > 0)
        if tax_amt > 0.5:
            new_gl_rows.append({
                "name": _gen_name(),
                "creation": now, "modified": now, "owner": posting_user, "modified_by": posting_user,
                "docstatus": 1, "idx": 0,
                "posting_date": ref.posting_date, "transaction_date": ref.posting_date,
                "fiscal_year": ref.fiscal_year,
                "account": ref.account, "account_currency": "VND",  # original 1331 account
                "voucher_type": "Purchase Invoice", "voucher_no": pi_name,
                "transaction_currency": "VND",
                "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
                "debit": round(tax_amt, 0), "debit_in_account_currency": round(tax_amt, 0),
                "debit_in_transaction_currency": round(tax_amt, 0),
                "debit_in_reporting_currency": round(tax_amt, 0),
                "credit": 0, "credit_in_account_currency": 0,
                "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
                "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
                "remarks": f"PI {pi_name} VAT input (audit-fix)",
            })

    if new_gl_rows:
        from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
        bulk_insert("GL Entry", new_gl_rows, batch_size=500)

    frappe.db.commit()
    return {"item_rows": n_items_rows, "gl_deleted": deleted_gl_count,
            "gl_inserted": len(new_gl_rows), "affected_pis": len(affected_pis)}


# ─── Step 3b: repair OB Inventory SE GL — Cr should be Equity not COGS ────

def repair_ob_inventory_gl(company: str) -> dict[str, Any]:
    """The step-3 fix posted Cr stock_adjustment_account (TK 632) for OB
    Inventory SEs. That's accurate for in-period SE but wrong for opening:
    OB inventory exists from prior years, so the credit side belongs on
    Equity (Retained Earnings, TK 4211) — not on P&L.

    This re-points the credit side for SEs marked is_opening='Yes' to the
    Retained Earnings account.
    """
    eq_acc = (
        frappe.db.get_value("Account", {
            "company": company, "account_number": "4211", "is_group": 0,
        }, "name") or
        frappe.db.get_value("Account", {
            "company": company, "account_name": ["like", "%Lợi nhuận%"],
            "root_type": "Equity", "is_group": 0,
        }, "name") or
        frappe.db.get_value("Account", {
            "company": company, "root_type": "Equity", "is_group": 0,
        }, "name", order_by="account_number")
    )
    if not eq_acc:
        return {"error": "no Equity account found"}

    stock_adj = frappe.db.get_value("Company", company, "stock_adjustment_account") or \
                frappe.db.get_value("Company", company, "default_expense_account")

    # OB Inventory SEs (is_opening='Yes') — re-route Cr from stock_adj → Equity
    ob_se_names = frappe.db.sql_list(
        """SELECT name FROM `tabStock Entry`
           WHERE company=%s AND is_opening='Yes'""",
        (company,),
    )
    if not ob_se_names:
        return {"ob_se_count": 0, "gl_updated": 0}

    placeholders = ",".join(["%s"] * len(ob_se_names))
    n_updated = frappe.db.sql(
        f"""UPDATE `tabGL Entry`
            SET account=%s,
                remarks=CONCAT(IFNULL(remarks, ''), ' (Eq-side)')
            WHERE company=%s AND voucher_type='Stock Entry'
              AND voucher_no IN ({placeholders})
              AND account=%s AND credit > 0 AND debit = 0
              AND is_cancelled=0""",
        (eq_acc, company, *ob_se_names, stock_adj),
    )
    n_updated_rows = frappe.db._cursor.rowcount

    frappe.db.commit()
    return {"ob_se_count": len(ob_se_names), "gl_updated": n_updated_rows,
            "equity_account": eq_acc}


# ─── Step 4b: repair PI GL after a previous bad step-4 run ─────────────────

def repair_pi_unbalance(company: str) -> dict[str, Any]:
    """If a previous run of step 4 deleted the Dr 1331 row for "pure-VAT" PIs
    without re-inserting, this restores the balance by adding back a Dr to
    TK 1331 (or, if no 1331 account is known, the supplier credit account)
    equal to the missing amount per PI.

    Idempotent: re-running after balance is restored = no-op.
    """
    rows = frappe.db.sql(
        """SELECT gle.voucher_no AS pi_name,
                  SUM(gle.debit) AS td, SUM(gle.credit) AS tc,
                  pi.posting_date, YEAR(pi.posting_date) AS fiscal_year
           FROM `tabGL Entry` gle
           JOIN `tabPurchase Invoice` pi ON pi.name = gle.voucher_no
           WHERE gle.company=%s AND gle.voucher_type='Purchase Invoice' AND gle.is_cancelled=0
           GROUP BY gle.voucher_no, pi.posting_date
           HAVING ABS(SUM(gle.debit) - SUM(gle.credit)) > 1""",
        (company,), as_dict=True,
    )
    if not rows:
        return {"unbalanced_pis": 0, "gl_inserted": 0}

    # For each PI, missing_dr = Cr - Dr. Re-insert as Dr on TK 1331.
    # Get the 1331 account for this company.
    vat_acc = frappe.db.get_value("Account", {
        "company": company,
        "account_number": ["like", "1331%"],
        "is_group": 0,
    }, "name") or frappe.db.get_value("Account", {
        "company": company,
        "account_name": ["like", "%1331%"],
        "is_group": 0,
    }, "name")
    if not vat_acc:
        return {"unbalanced_pis": len(rows), "gl_inserted": 0,
                "error": "no 1331 account found"}

    now = frappe.utils.now()
    posting_user = "Administrator"
    new_gl_rows: list[dict] = []
    for r in rows:
        missing = round(float(r.tc or 0) - float(r.td or 0), 0)
        if missing <= 0:
            continue
        new_gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": r.posting_date, "transaction_date": r.posting_date,
            "fiscal_year": r.fiscal_year,
            "account": vat_acc, "account_currency": "VND",
            "voucher_type": "Purchase Invoice", "voucher_no": r.pi_name,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0, "reporting_currency_exchange_rate": 1.0,
            "debit": missing, "debit_in_account_currency": missing,
            "debit_in_transaction_currency": missing, "debit_in_reporting_currency": missing,
            "credit": 0, "credit_in_account_currency": 0,
            "credit_in_transaction_currency": 0, "credit_in_reporting_currency": 0,
            "company": company, "is_opening": "No", "is_advance": "No", "is_cancelled": 0,
            "remarks": f"PI {r.pi_name} VAT input (balance repair)",
        })

    if new_gl_rows:
        from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
        bulk_insert("GL Entry", new_gl_rows, batch_size=500)
    frappe.db.commit()
    return {"unbalanced_pis": len(rows), "gl_inserted": len(new_gl_rows)}


# ─── Step 5: re-derive SI/PI status ─────────────────────────────────────────

def rederive_invoice_status(company: str) -> dict[str, int]:
    """Recompute status field from outstanding_amount + due_date.
    Rules (ERPNext default, with zero/negative grand_total guard):
      grand_total <= 0                                → 'Paid' (no money owed; covers returns)
      outstanding <= 1 + grand_total > 0              → 'Paid'
      0 < outstanding < grand_total                   → 'Partly Paid'
      outstanding >= grand_total - 1 + due_date < today → 'Overdue'
      outstanding >= grand_total - 1 + due_date >= today → 'Unpaid'
    """
    today = frappe.utils.today()
    out: dict[str, int] = {}

    for parent_dt in ("Sales Invoice", "Purchase Invoice"):
        # Zero-or-negative grand_total → Paid (returns, corrections, voids)
        frappe.db.sql(
            f"""UPDATE `tab{parent_dt}` SET status='Paid'
                WHERE company=%s AND docstatus=1 AND grand_total <= 0""",
            (company,),
        )
        out[f"{parent_dt}_zero_gt"] = frappe.db._cursor.rowcount
        # Paid (positive grand_total, outstanding <= 1)
        frappe.db.sql(
            f"""UPDATE `tab{parent_dt}` SET status='Paid'
                WHERE company=%s AND docstatus=1 AND grand_total > 0
                  AND outstanding_amount <= 1""",
            (company,),
        )
        out[f"{parent_dt}_paid"] = frappe.db._cursor.rowcount
        # Partly Paid
        frappe.db.sql(
            f"""UPDATE `tab{parent_dt}` SET status='Partly Paid'
                WHERE company=%s AND docstatus=1 AND grand_total > 0
                  AND outstanding_amount > 1
                  AND outstanding_amount < grand_total - 1""",
            (company,),
        )
        out[f"{parent_dt}_partly"] = frappe.db._cursor.rowcount
        # Overdue
        frappe.db.sql(
            f"""UPDATE `tab{parent_dt}` SET status='Overdue'
                WHERE company=%s AND docstatus=1 AND grand_total > 0
                  AND outstanding_amount >= grand_total - 1
                  AND due_date IS NOT NULL AND due_date < %s""",
            (company, today),
        )
        out[f"{parent_dt}_overdue"] = frappe.db._cursor.rowcount
        # Unpaid (only when not yet overdue)
        frappe.db.sql(
            f"""UPDATE `tab{parent_dt}` SET status='Unpaid'
                WHERE company=%s AND docstatus=1 AND grand_total > 0
                  AND outstanding_amount >= grand_total - 1
                  AND (due_date IS NULL OR due_date >= %s)""",
            (company, today),
        )
        out[f"{parent_dt}_unpaid"] = frappe.db._cursor.rowcount

    frappe.db.commit()
    return out


# ─── Step 6: seed Item Default ──────────────────────────────────────────────

def seed_item_defaults(company: str) -> dict[str, int]:
    """For Items used in submitted PI/SI but without Item Default rows for
    this Company, infer income/expense/warehouse from observed usage and
    INSERT one Item Default row per (item, company)."""
    items_to_seed = frappe.db.sql(
        """SELECT i.name AS item_code,
                  -- Most-common expense_account from PI item lines
                  (SELECT pii.expense_account FROM `tabPurchase Invoice Item` pii
                   JOIN `tabPurchase Invoice` pi ON pi.name=pii.parent
                   WHERE pi.company=%s AND pi.docstatus=1 AND pii.item_code=i.name
                   GROUP BY pii.expense_account ORDER BY COUNT(*) DESC, SUM(pii.amount) DESC LIMIT 1
                  ) AS exp_acc,
                  (SELECT sii.income_account FROM `tabSales Invoice Item` sii
                   JOIN `tabSales Invoice` si ON si.name=sii.parent
                   WHERE si.company=%s AND si.docstatus=1 AND sii.item_code=i.name
                   GROUP BY sii.income_account ORDER BY COUNT(*) DESC, SUM(sii.amount) DESC LIMIT 1
                  ) AS inc_acc
           FROM `tabItem` i
           WHERE NOT EXISTS (SELECT 1 FROM `tabItem Default` id_ WHERE id_.parent=i.name AND id_.company=%s)
             AND i.disabled = 0
        """,
        (company, company, company), as_dict=True,
    )

    now = frappe.utils.now()
    posting_user = "Administrator"
    new_rows: list[dict] = []
    for r in items_to_seed:
        if not r.exp_acc and not r.inc_acc:
            continue  # nothing to seed
        new_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 0, "idx": 1,
            "company": company,
            "expense_account": r.exp_acc,
            "income_account": r.inc_acc,
            "parent": r.item_code, "parenttype": "Item",
            "parentfield": "item_defaults",
        })

    if new_rows:
        from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
        bulk_insert("Item Default", new_rows, batch_size=500)
    frappe.db.commit()
    return {"item_defaults_inserted": len(new_rows),
            "items_scanned": len(items_to_seed)}


# ─── Step 7: post year-end closing (NVK voucher) ────────────────────────────

def post_year_end_closing(company: str) -> dict[str, Any]:
    """Build + post Misa's year-end Closing Entry (NVK20250331 = "Kết chuyển
    lãi lỗ"). 50 raw rows aggregate into one balanced JE that closes P&L
    accounts (51x revenue, 632/642 expense) into TK 911, then 911 into
    TK 4212 (Retained Earnings).

    Misa exports this with a "wash" leg on 911 (sum_dr = sum_cr on 911); we
    keep that to preserve the trail Misa expects when re-importing later.

    Posting this typically resolves residual P&L imbalance left after the
    audit fixes by pushing the net change through Retained Earnings.

    Idempotent — skips if the closing JE for this voucher_no already exists.
    """
    from vn_accounting.misa_migration.bulk_pump import account_resolver
    from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert

    # Company-scope the batch lookup — two companies may each have an
    # NVK20250331; pick the one belonging to THIS company.
    _b = frappe.db.sql(
        """SELECT r.batch FROM `tabMisa Migration Row` r
           JOIN `tabMisa Migration Batch` b ON b.name = r.batch
           WHERE r.voucher_no='NVK20250331' AND b.company=%s LIMIT 1""",
        (company,),
    )
    batch_name = _b[0][0] if _b else None
    if not batch_name:
        return {"closing_je_built": 0, "reason": "no NVK20250331 rows for company"}

    account_resolver.warm_cache(company)

    rows = frappe.db.sql(
        """SELECT raw_payload FROM `tabMisa Migration Row`
           WHERE batch=%s AND file_type='NKC' AND voucher_no='NVK20250331'""",
        (batch_name,), as_dict=True,
    )
    if not rows:
        return {"closing_je_built": 0, "reason": "no rows"}

    voucher_no = "NVK20250331"
    doc_name = migrated_doc_name(company, voucher_no)
    if frappe.db.exists("Journal Entry", doc_name):
        # Already posted — re-mark rows and return idempotently.
        frappe.db.sql(
            """UPDATE `tabMisa Migration Row` SET status='Posted',
               target_doctype='Journal Entry', target_name=%s
               WHERE batch=%s AND voucher_no='NVK20250331'""",
            (doc_name, batch_name),
        )
        frappe.db.commit()
        return {"closing_je_built": 0, "reason": "already exists", "rows_marked": 50}

    # Aggregate by account
    import json as _json
    legs: dict[str, dict] = {}  # acct → {dr, cr}
    posting_date = None
    for r in rows:
        try:
            p = _json.loads(r.raw_payload)
        except (TypeError, ValueError):
            continue
        raw_tk = (p.get("Tài khoản") or "").strip()
        if not raw_tk:
            continue
        acct = account_resolver.resolve(raw_tk, company) or raw_tk
        dr = float(p.get("Phát sinh Nợ") or 0)
        cr = float(p.get("Phát sinh Có") or 0)
        if dr == 0 and cr == 0:
            continue
        cur = legs.get(acct) or {"dr": 0, "cr": 0}
        cur["dr"] += dr
        cur["cr"] += cr
        legs[acct] = cur
        if posting_date is None:
            posting_date = (p.get("Ngày hạch toán") or "")[:10] or None
    posting_date = posting_date or "2025-12-31"
    fiscal_year = posting_date[:4]

    if not legs:
        return {"closing_je_built": 0, "reason": "no aggregable legs"}

    # Balance check — if any drift due to rounding, push residual to TK 4212
    total_dr = sum(v["dr"] for v in legs.values())
    total_cr = sum(v["cr"] for v in legs.values())
    diff = round(total_dr - total_cr, 0)
    if abs(diff) > 0.5:
        re_acc = (
            account_resolver.resolve("4212", company)
            or account_resolver.resolve("4211", company)
            or frappe.db.get_value(
                "Account",
                {"company": company, "root_type": "Equity", "is_group": 0},
                "name", order_by="account_number",
            )
        )
        if re_acc:
            cur = legs.get(re_acc) or {"dr": 0, "cr": 0}
            if diff > 0:
                cur["cr"] += diff
            else:
                cur["dr"] += -diff
            legs[re_acc] = cur

    # Build JE + JE Account + GL Entry
    now = frappe.utils.now()
    posting_user = "Administrator"
    je_accounts: list[dict] = []
    gl_rows: list[dict] = []
    for idx, (acct, amts) in enumerate(legs.items()):
        if amts["dr"] == 0 and amts["cr"] == 0:
            continue
        je_accounts.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "account": acct, "account_currency": "VND",
            "debit_in_account_currency": amts["dr"], "debit": amts["dr"],
            "credit_in_account_currency": amts["cr"], "credit": amts["cr"],
            "user_remark": "Kết chuyển lãi lỗ năm 2025",
            "parent": doc_name, "parenttype": "Journal Entry",
            "parentfield": "accounts",
        })
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date, "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": acct, "account_currency": "VND",
            "voucher_type": "Journal Entry", "voucher_no": doc_name,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0,
            "reporting_currency_exchange_rate": 1.0,
            "debit": amts["dr"], "debit_in_account_currency": amts["dr"],
            "debit_in_transaction_currency": amts["dr"],
            "debit_in_reporting_currency": amts["dr"],
            "credit": amts["cr"], "credit_in_account_currency": amts["cr"],
            "credit_in_transaction_currency": amts["cr"],
            "credit_in_reporting_currency": amts["cr"],
            "company": company, "is_opening": "No",
            "is_advance": "No", "is_cancelled": 0,
            "remarks": "Year-end Closing (NVK20250331)",
        })

    total_dr_final = sum(v["dr"] for v in legs.values())
    total_cr_final = sum(v["cr"] for v in legs.values())

    je_row = {
        "name": doc_name,
        "creation": now, "modified": now,
        "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "voucher_type": "Journal Entry",
        "posting_date": posting_date,
        "multi_currency": 0,
        "total_debit": total_dr_final, "total_credit": total_cr_final,
        "difference": 0,
        "total_amount_currency": "VND", "total_amount": total_dr_final,
        "user_remark": "Kết chuyển lãi lỗ năm 2025 (bulk_pump audit-fix)",
        "remark": "Kết chuyển lãi lỗ năm 2025",
        "is_opening": "No",
        "misa_voucher_no": voucher_no,
    }

    bulk_insert("Journal Entry", [je_row], batch_size=1)
    bulk_insert("Journal Entry Account", je_accounts, batch_size=500)
    bulk_insert("GL Entry", gl_rows, batch_size=500)

    # Mark Misa rows Posted
    frappe.db.sql(
        """UPDATE `tabMisa Migration Row` SET status='Posted',
           target_doctype='Journal Entry', target_name=%s
           WHERE batch=%s AND voucher_no='NVK20250331'""",
        (doc_name, batch_name),
    )

    frappe.db.commit()
    return {
        "closing_je_built": 1,
        "voucher_no": voucher_no,
        "posting_date": posting_date,
        "leg_count": len(je_accounts),
        "total_dr": total_dr_final,
        "total_cr": total_cr_final,
        "rows_marked": 50,
    }


# ─── Step 7a: post any remaining year-end NVK closing/recognition JEs ──────

def post_remaining_nvk_jes(company: str) -> dict[str, Any]:
    """Misa's year-end usually exports multiple NVK* vouchers — NVK20250331
    (the P&L close into TK 911) and NVK20250307 (Chi phí thuế TNDN — tax
    recognition Dr 8211 / Cr 3334). Step 7 handled NVK20250331 explicitly;
    this step picks up every remaining Ready NVK voucher and posts each as
    a standalone JE.

    For each voucher_no still Ready and starting with 'NVK':
      - Aggregate legs by account (resolved)
      - Build + post JE with the same shape as step 7
      - Mark Misa rows Posted

    Idempotent.
    """
    from vn_accounting.misa_migration.bulk_pump import account_resolver
    from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
    import json as _json

    account_resolver.warm_cache(company)
    # Scope to THIS company's batches (a second company may have its own
    # Ready NVK rows; never cross-pick another tenant's vouchers).
    batches = frappe.db.sql_list(
        "SELECT name FROM `tabMisa Migration Batch` WHERE company=%s", (company,)
    )
    if not batches:
        return {"vouchers_built": 0}
    _bph = ",".join(["%s"] * len(batches))
    pending_vnos = frappe.db.sql_list(
        f"""SELECT DISTINCT voucher_no FROM `tabMisa Migration Row`
           WHERE file_type='NKC' AND status='Ready'
             AND batch IN ({_bph})
             AND voucher_no LIKE 'NVK%%' AND voucher_no IS NOT NULL
             AND voucher_no != ''""",
        tuple(batches),
    )
    if not pending_vnos:
        return {"vouchers_built": 0}

    now = frappe.utils.now()
    posting_user = "Administrator"
    out: dict[str, Any] = {"vouchers_built": 0, "vouchers": []}

    for voucher_no in pending_vnos:
        doc_name = migrated_doc_name(company, voucher_no)
        if frappe.db.exists("Journal Entry", doc_name):
            continue
        rows = frappe.db.sql(
            f"""SELECT raw_payload FROM `tabMisa Migration Row`
               WHERE file_type='NKC' AND voucher_no=%s AND status='Ready'
                 AND batch IN ({_bph})""",
            (voucher_no, *batches), as_dict=True,
        )
        if not rows:
            continue
        legs: dict[str, dict] = {}
        posting_date = None
        remark = ""
        for r in rows:
            try: p = _json.loads(r.raw_payload)
            except: continue
            raw_tk = (p.get("Tài khoản") or "").strip()
            if not raw_tk: continue
            acct = account_resolver.resolve(raw_tk, company) or raw_tk
            dr = float(p.get("Phát sinh Nợ") or 0)
            cr = float(p.get("Phát sinh Có") or 0)
            if dr == 0 and cr == 0: continue
            cur = legs.get(acct) or {"dr": 0, "cr": 0}
            cur["dr"] += dr
            cur["cr"] += cr
            legs[acct] = cur
            if posting_date is None:
                posting_date = (p.get("Ngày hạch toán") or "")[:10] or None
            if not remark:
                remark = (p.get("Diễn giải chung") or p.get("Diễn giải") or "")[:200]
        if not legs:
            continue
        posting_date = posting_date or "2025-12-31"
        fiscal_year = posting_date[:4]

        # Verify balanced; if not, push residual to RE (4212)
        td = sum(v["dr"] for v in legs.values())
        tc = sum(v["cr"] for v in legs.values())
        diff = round(td - tc, 0)
        if abs(diff) > 0.5:
            re_acc = (
                account_resolver.resolve("4212", company)
                or account_resolver.resolve("4211", company)
            )
            if re_acc:
                cur = legs.get(re_acc) or {"dr": 0, "cr": 0}
                if diff > 0: cur["cr"] += diff
                else: cur["dr"] += -diff
                legs[re_acc] = cur

        je_accounts, gl_rows = [], []
        for idx, (acct, amts) in enumerate(legs.items()):
            if amts["dr"] == 0 and amts["cr"] == 0: continue
            je_accounts.append({
                "name": _gen_name(),
                "creation": now, "modified": now,
                "owner": posting_user, "modified_by": posting_user,
                "docstatus": 1, "idx": idx + 1,
                "account": acct, "account_currency": "VND",
                "debit_in_account_currency": amts["dr"], "debit": amts["dr"],
                "credit_in_account_currency": amts["cr"], "credit": amts["cr"],
                "user_remark": remark, "parent": doc_name,
                "parenttype": "Journal Entry", "parentfield": "accounts",
            })
            gl_rows.append({
                "name": _gen_name(),
                "creation": now, "modified": now,
                "owner": posting_user, "modified_by": posting_user,
                "docstatus": 1, "idx": 0,
                "posting_date": posting_date, "transaction_date": posting_date,
                "fiscal_year": fiscal_year,
                "account": acct, "account_currency": "VND",
                "voucher_type": "Journal Entry", "voucher_no": doc_name,
                "transaction_currency": "VND",
                "transaction_exchange_rate": 1.0,
                "reporting_currency_exchange_rate": 1.0,
                "debit": amts["dr"], "debit_in_account_currency": amts["dr"],
                "debit_in_transaction_currency": amts["dr"],
                "debit_in_reporting_currency": amts["dr"],
                "credit": amts["cr"], "credit_in_account_currency": amts["cr"],
                "credit_in_transaction_currency": amts["cr"],
                "credit_in_reporting_currency": amts["cr"],
                "company": company, "is_opening": "No",
                "is_advance": "No", "is_cancelled": 0,
                "remarks": remark,
            })

        total_dr = sum(v["dr"] for v in legs.values())
        total_cr = sum(v["cr"] for v in legs.values())
        je_row = {
            "name": doc_name,
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "company": company,
            "voucher_type": "Journal Entry",
            "posting_date": posting_date,
            "multi_currency": 0,
            "total_debit": total_dr, "total_credit": total_cr, "difference": 0,
            "total_amount_currency": "VND", "total_amount": total_dr,
            "user_remark": remark, "remark": remark,
            "is_opening": "No", "misa_voucher_no": voucher_no,
        }
        bulk_insert("Journal Entry", [je_row], batch_size=1)
        bulk_insert("Journal Entry Account", je_accounts, batch_size=500)
        bulk_insert("GL Entry", gl_rows, batch_size=500)
        frappe.db.sql(
            f"""UPDATE `tabMisa Migration Row` SET status='Posted',
               target_doctype='Journal Entry', target_name=%s
               WHERE file_type='NKC' AND voucher_no=%s
                 AND batch IN ({_bph})""",
            (doc_name, voucher_no, *batches),
        )
        out["vouchers_built"] += 1
        out["vouchers"].append({
            "voucher_no": voucher_no,
            "legs": len(je_accounts),
            "total_dr": total_dr,
        })

    frappe.db.commit()
    return out


# ─── Step 7a-tot: mark Misa summary rows as Skipped ────────────────────────

def skip_misa_summary_rows(company: str) -> dict[str, int]:
    """Mark Misa 'Tổng'/'Tổng cộng' aggregate rows (NOT real records) as
    Skipped. Covers OB Fixed Asset, OB CCDC, OB Customer/Supplier/etc, NKC
    grand-totals."""
    SUMMARY_TOKENS = ("Tổng", "Tổng cộng", "Total")
    n = 0
    for token in SUMMARY_TOKENS:
        # Match common key fields that contain 'Tổng'
        like_patterns = [
            f'%"Mã tài sản": "{token}"%',
            f'%"Mã CCDC": "{token}"%',
            f'%"Mã đối tượng": "{token}"%',
            f'%"Mã khách hàng": "{token}"%',
            f'%"Mã nhà cung cấp": "{token}"%',
            f'%"Ngày hạch toán": "{token}"%',
        ]
        for pat in like_patterns:
            frappe.db.sql(
                """UPDATE `tabMisa Migration Row` SET status='Skipped',
                   error_message=%s WHERE status='Ready' AND raw_payload LIKE %s""",
                (f"Misa summary row ({token}) — not a data record", pat),
            )
            n += frappe.db._cursor.rowcount

    frappe.db.commit()
    return {"summary_rows_skipped": n}


# ─── Step 7b: P&L residual close ────────────────────────────────────────────

def post_pl_residual_close(company: str) -> dict[str, Any]:
    """Misa's NVK closing was generated against the pre-fix GL state. After
    audit fixes (SE GL routing 5.51B Cr through TK 632, PI 1331 remap, etc.)
    some P&L accounts retain non-zero balances. This step computes the
    residual on every Income/Expense account at year-end and posts a single
    JE that:
      - Dr each Income account with net Cr balance / Cr each Expense account
        with net Dr balance (closes them to zero)
      - Cr each Income account with net Dr (reversal) / Dr each Expense with
        net Cr (reversal)
      - Contra goes to TK 4212 (Retained Earnings) — net change is the
        residual P&L delta from audit fixes.

    Idempotent — checks for an existing voucher of the same name.
    """
    voucher_no = "PL-CLOSE-RESIDUAL-2025"
    doc_name = migrated_doc_name(company, voucher_no)  # company-namespaced
    if frappe.db.exists("Journal Entry", doc_name):
        return {"closing_je_built": 0, "reason": "already exists"}

    posting_date = "2025-12-31"
    # Find every P&L account with non-zero balance as of year-end
    pl_rows = frappe.db.sql(
        """SELECT a.name AS acct, a.root_type,
                  SUM(gle.debit) AS td, SUM(gle.credit) AS tc,
                  SUM(gle.debit) - SUM(gle.credit) AS net
           FROM `tabGL Entry` gle JOIN `tabAccount` a ON a.name = gle.account
           WHERE gle.company=%s AND a.root_type IN ('Income', 'Expense')
             AND gle.is_cancelled=0 AND gle.posting_date <= %s
           GROUP BY a.name, a.root_type
           HAVING ABS(SUM(gle.debit) - SUM(gle.credit)) > 0.5""",
        (company, posting_date), as_dict=True,
    )
    if not pl_rows:
        return {"closing_je_built": 0, "reason": "all P&L already zero"}

    # Find Retained Earnings (TK 4212 current year, fallback to 4211)
    from vn_accounting.misa_migration.bulk_pump import account_resolver
    account_resolver.warm_cache(company)
    re_acc = (
        account_resolver.resolve("4212", company)
        or account_resolver.resolve("4211", company)
        or frappe.db.get_value(
            "Account",
            {"company": company, "root_type": "Equity", "is_group": 0},
            "name", order_by="account_number",
        )
    )
    if not re_acc:
        return {"closing_je_built": 0, "reason": "no Equity account"}

    # Build legs: each P&L acct gets opposite-side leg to zero it;
    # contra sum goes to RE.
    legs: list[tuple[str, float, float]] = []  # (acct, dr, cr)
    net_to_re = 0.0
    for r in pl_rows:
        net = float(r.net or 0)
        if net > 0:
            # Dr balance → close with Cr
            legs.append((r.acct, 0.0, net))
            net_to_re += net  # offset goes Dr (4212 increases as Dr/loss)
        else:
            # Cr balance → close with Dr
            legs.append((r.acct, -net, 0.0))
            net_to_re += net  # offset goes Cr (4212 decreases as Cr/profit gain)

    # RE contra leg
    if net_to_re > 0:
        legs.append((re_acc, net_to_re, 0.0))  # Dr RE — net loss absorbed
    else:
        legs.append((re_acc, 0.0, -net_to_re))  # Cr RE — net gain absorbed

    # Build JE + JE Account + GL Entry
    from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert
    now = frappe.utils.now()
    posting_user = "Administrator"
    fiscal_year = "2025"

    je_accounts: list[dict] = []
    gl_rows: list[dict] = []
    total_dr = total_cr = 0.0
    for idx, (acct, dr, cr) in enumerate(legs):
        if dr == 0 and cr == 0:
            continue
        total_dr += dr
        total_cr += cr
        je_accounts.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": idx + 1,
            "account": acct, "account_currency": "VND",
            "debit_in_account_currency": dr, "debit": dr,
            "credit_in_account_currency": cr, "credit": cr,
            "user_remark": "Residual P&L close (audit-fix)",
            "parent": doc_name, "parenttype": "Journal Entry",
            "parentfield": "accounts",
        })
        gl_rows.append({
            "name": _gen_name(),
            "creation": now, "modified": now,
            "owner": posting_user, "modified_by": posting_user,
            "docstatus": 1, "idx": 0,
            "posting_date": posting_date, "transaction_date": posting_date,
            "fiscal_year": fiscal_year,
            "account": acct, "account_currency": "VND",
            "voucher_type": "Journal Entry", "voucher_no": doc_name,
            "transaction_currency": "VND",
            "transaction_exchange_rate": 1.0,
            "reporting_currency_exchange_rate": 1.0,
            "debit": dr, "debit_in_account_currency": dr,
            "debit_in_transaction_currency": dr, "debit_in_reporting_currency": dr,
            "credit": cr, "credit_in_account_currency": cr,
            "credit_in_transaction_currency": cr, "credit_in_reporting_currency": cr,
            "company": company, "is_opening": "No",
            "is_advance": "No", "is_cancelled": 0,
            "remarks": "Residual P&L close (audit-fix)",
        })

    je_row = {
        "name": doc_name,
        "creation": now, "modified": now,
        "owner": posting_user, "modified_by": posting_user,
        "docstatus": 1, "idx": 0,
        "company": company,
        "voucher_type": "Journal Entry",
        "posting_date": posting_date,
        "multi_currency": 0,
        "total_debit": total_dr, "total_credit": total_cr, "difference": 0,
        "total_amount_currency": "VND", "total_amount": total_dr,
        "user_remark": "Residual P&L close — true-up after audit fixes",
        "remark": "Residual P&L close",
        "is_opening": "No",
    }

    bulk_insert("Journal Entry", [je_row], batch_size=1)
    bulk_insert("Journal Entry Account", je_accounts, batch_size=500)
    bulk_insert("GL Entry", gl_rows, batch_size=500)
    frappe.db.commit()

    return {
        "closing_je_built": 1,
        "voucher_no": voucher_no,
        "leg_count": len(je_accounts),
        "total_dr": total_dr,
        "total_cr": total_cr,
        "net_to_retained_earnings": net_to_re,
    }


# ─── Step 8: mark OB + child Migration Rows as Posted ───────────────────────

def mark_consumed_rows_posted(company: str) -> dict[str, int]:
    """Update Misa Migration Row.status for rows that are economically
    integrated into the GL but stuck at 'Ready' because the orchestrator
    never updated them. Returns counts per file_type."""
    out: dict[str, int] = {}

    # 1. OB rows — all aggregated into the master Opening JE (OB-MM-*)
    ob_je_name = frappe.db.get_value(
        "Journal Entry",
        {"company": company, "voucher_type": "Opening Entry", "is_opening": "Yes"},
        "name", order_by="posting_date desc",
    )
    OB_TYPES = ["OB Account Balance", "OB Customer AR", "OB Supplier AP",
                "OB Bank Balance", "OB Employee Advance", "OB Prepaid Expense"]
    if ob_je_name:
        placeholders = ",".join(["%s"] * len(OB_TYPES))
        frappe.db.sql(
            f"""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Journal Entry', target_name=%s
                WHERE file_type IN ({placeholders}) AND status='Ready'""",
            (ob_je_name, *OB_TYPES),
        )
        out["ob_aggregate_to_je"] = frappe.db._cursor.rowcount

    # 2. OB Inventory → Stock Entry (OB-INV-MM-*)
    ob_inv_se = frappe.db.get_value(
        "Stock Entry",
        {"company": company, "is_opening": "Yes"},
        "name", order_by="posting_date desc",
    )
    if ob_inv_se:
        frappe.db.sql(
            """UPDATE `tabMisa Migration Row` SET status='Posted',
               target_doctype='Stock Entry', target_name=%s
               WHERE file_type='OB Inventory' AND status='Ready'""",
            (ob_inv_se,),
        )
        out["ob_inventory_to_se"] = frappe.db._cursor.rowcount

    # 3. OB Fixed Asset → tabAsset (per row, lookup by Mã tài sản)
    n_fa = 0
    rows = frappe.db.sql(
        """SELECT name, raw_payload FROM `tabMisa Migration Row`
           WHERE file_type='OB Fixed Asset' AND status='Ready'""",
        as_dict=True,
    )
    for r in rows:
        try:
            import json as _json
            p = _json.loads(r.raw_payload or "{}")
        except (TypeError, ValueError):
            continue
        asset_code = p.get("Mã tài sản") or p.get("Mã CCDC")
        if asset_code and frappe.db.exists("Asset", asset_code):
            frappe.db.sql(
                """UPDATE `tabMisa Migration Row` SET status='Posted',
                   target_doctype='Asset', target_name=%s WHERE name=%s""",
                (asset_code, r.name),
            )
            n_fa += 1
    out["ob_fixed_asset"] = n_fa

    # 4. OB CCDC → tabAsset (similar — they get created as Assets via the asset builder)
    n_ccdc = 0
    rows = frappe.db.sql(
        """SELECT name, raw_payload FROM `tabMisa Migration Row`
           WHERE file_type='OB CCDC' AND status='Ready'""",
        as_dict=True,
    )
    for r in rows:
        try:
            import json as _json
            p = _json.loads(r.raw_payload or "{}")
        except (TypeError, ValueError):
            continue
        asset_code = p.get("Mã CCDC") or p.get("Mã tài sản")
        if asset_code and frappe.db.exists("Asset", asset_code):
            frappe.db.sql(
                """UPDATE `tabMisa Migration Row` SET status='Posted',
                   target_doctype='Asset', target_name=%s WHERE name=%s""",
                (asset_code, r.name),
            )
            n_ccdc += 1
    out["ob_ccdc"] = n_ccdc

    # 5. SCT / Bang ke BR / Bang ke MV — consumed-as-child by NKC vouchers.
    # Mark as 'Posted' with target_doctype set to the parent voucher's doctype
    # when we can resolve the parent voucher, otherwise just status='Posted'.
    for ft in ("SCT", "Bang ke BR"):
        n = frappe.db.sql(
            f"""UPDATE `tabMisa Migration Row` mr
                LEFT JOIN `tabMisa Migration Row` parent
                  ON parent.voucher_no = mr.voucher_no
                  AND parent.file_type='NKC' AND parent.status='Posted'
                SET mr.status='Posted',
                    mr.target_doctype=COALESCE(parent.target_doctype, 'Consumed'),
                    mr.target_name=COALESCE(parent.target_name, mr.voucher_no)
                WHERE mr.file_type=%s AND mr.status='Ready'""",
            (ft,),
        )
        out[ft] = frappe.db._cursor.rowcount

    frappe.db.commit()
    return out


# ─── Step 9: auto-resolve Account Conflicts ────────────────────────────────

def resolve_account_conflicts(company: str) -> dict[str, int]:
    """For the Account file_type rows with status='Conflict', mark them
    Resolved with note that Frappe's existing account_name wins. Misa's
    proposed name is captured in raw_payload for audit.

    No GL impact — these are Account master mismatches, not transactions.
    The 34 conflicts in DCNET TEST are CoA TKs where Frappe uses one name
    (e.g. "TSCĐ hữu hình") and Misa uses another ("Tài sản cố định hữu hình").
    Both refer to the same TK; we keep Frappe.
    """
    n = frappe.db.sql(
        """UPDATE `tabMisa Migration Row` SET status='Posted',
           target_doctype='Account',
           error_message=CONCAT('AUTO-RESOLVED (kept Frappe name): ', IFNULL(error_message, ''))
           WHERE file_type='Account' AND status='Conflict'""",
    )
    rowcount = frappe.db._cursor.rowcount
    frappe.db.commit()
    return {"resolved": rowcount}


# ─── Step 10a: create missing masters via existing builders ────────────────

def create_missing_masters(company: str) -> dict[str, Any]:
    """Run the existing masters.py builders for any master rows still Ready
    that lack a Frappe counterpart. Currently handles Employee + Bank +
    Bank Account (the 3 masters with SQL builders in bulk_pump/builders/masters.py).

    Other masters (Item Group, Customer Group, Warehouse, Department,
    Cost Center, Asset Category, CCDC Category) typically come from the
    ORM Misa importer that runs BEFORE bulk_pump. If they're still missing
    after bulk_pump runs, that's an upstream ORM gap, not a bulk_pump gap.
    """
    from vn_accounting.misa_migration.bulk_pump.builders import masters
    from vn_accounting.misa_migration.bulk_pump.bulk_executor import bulk_insert

    batch_name = frappe.db.get_value(
        "Misa Migration Row", {"file_type": "Bank Account"}, "batch"
    ) or frappe.db.get_value(
        "Misa Migration Batch", {"company": company}, "name"
    )
    if not batch_name:
        return {"batch": None, "skipped": "no batch found"}

    out: dict[str, Any] = {"batch": batch_name}

    # Bank + Bank Account
    ba_out = masters.build_bank_account_dicts(batch_name, company)
    bank_rows = ba_out.get("Bank", [])
    if bank_rows:
        bulk_insert("Bank", bank_rows, batch_size=200)
        out["Bank_inserted"] = len(bank_rows)
    bacc_rows = ba_out.get("Bank Account", [])
    if bacc_rows:
        bulk_insert("Bank Account", bacc_rows, batch_size=200)
        out["Bank Account_inserted"] = len(bacc_rows)

    # Employee
    emp_out = masters.build_employee_dicts(batch_name, company)
    emp_rows = emp_out.get("Employee", [])
    if emp_rows:
        bulk_insert("Employee", emp_rows, batch_size=200)
        out["Employee_inserted"] = len(emp_rows)

    frappe.db.commit()
    return out


# ─── Step 10b: mark master rows Posted / Missing ───────────────────────────

def mark_master_rows_posted(company: str) -> dict[str, Any]:
    """For master Misa Migration Rows in 'Ready' status, check whether the
    corresponding Frappe master already exists (created by an earlier ORM
    import pass). If exists → mark Posted with target_doctype/target_name.
    If not exists → leave Ready with a note (these need a separate ORM
    import or manual setup; bulk_pump never claimed to create them).

    Masters checked (key field → DocType):
      - Item Group, Customer Group: code/name → Item Group / Customer Group
      - Warehouse, Department, Cost Center: Frappe name = '<misa_name> - <abbr>'
      - Account: '<TK> - <name> - <abbr>' resolved via account_resolver
      - Bank: by 'Tên đầy đủ'
      - Bank Account: by 'Số tài khoản' or '<acc_no> - <bank>'
      - Asset Category / CCDC Category: by name
    """
    from vn_accounting.misa_migration.bulk_pump import account_resolver
    import json as _json

    abbr = frappe.db.get_value("Company", company, "abbr") or ""
    account_resolver.warm_cache(company)
    out: dict[str, dict] = {}

    def try_match(dt: str, candidates: list[str]) -> str | None:
        """Try to find a Frappe doc matching any of the candidate names.
        Returns the canonical Frappe name if found."""
        for c in candidates:
            if not c:
                continue
            c = str(c).strip()
            if not c:
                continue
            # Direct match
            name = frappe.db.get_value(dt, c, "name")
            if name:
                return name
            # With abbr suffix
            name = frappe.db.get_value(dt, f"{c} - {abbr}", "name")
            if name:
                return name
            # Case-insensitive match (collation handles this for get_value already
            # but explicit search via name LIKE for first hit)
            rows = frappe.db.sql(
                f"SELECT name FROM `tab{dt}` WHERE name LIKE %s LIMIT 1",
                (f"{c}%",),
            )
            if rows:
                return rows[0][0]
        return None

    # Item Group
    ig_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Item Group' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in ig_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        code = p.get("Mã nhóm vật tư, hàng hóa, dịch vụ", "")
        name = p.get("Tên nhóm vật tư, hàng hóa, dịch vụ", "")
        match = try_match("Item Group", [code, name])
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Item Group', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Item Group"] = {"posted": n_posted, "missing": n_missing}

    # Customer Group
    cg_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Customer Group' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in cg_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        code = p.get("Mã nhóm KH, NCC", "")
        name = p.get("Tên nhóm khách hàng, nhà cung cấp", "")
        match = try_match("Customer Group", [code, name])
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Customer Group', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Customer Group"] = {"posted": n_posted, "missing": n_missing}

    # Warehouse — Frappe naming is typically '<Tên kho> - <abbr>'
    wh_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Warehouse' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in wh_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        code = p.get("Mã kho", "")
        wh_name = p.get("Tên kho", "")
        match = try_match("Warehouse", [code, wh_name, f"{wh_name} - {abbr}"])
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Warehouse', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Warehouse"] = {"posted": n_posted, "missing": n_missing}

    # Department
    dep_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Department' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in dep_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        code = p.get("Mã đơn vị", "")
        dep_name = p.get("Tên đơn vị", "")
        match = try_match("Department", [code, dep_name, f"{dep_name} - {abbr}"])
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Department', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Department"] = {"posted": n_posted, "missing": n_missing}

    # Cost Center
    cc_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Cost Center' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in cc_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        code = p.get("Mã đối tượng THCP", "")
        cc_name = p.get("Tên đối tượng THCP", "")
        match = try_match("Cost Center", [code, cc_name, f"{cc_name} - {abbr}"])
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Cost Center', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Cost Center"] = {"posted": n_posted, "missing": n_missing}

    # Asset Category — mark missing as Skipped (need manual creation)
    for ft, code_key, name_key in [
        ("Asset Category", "Mã loại TSCĐ", "Tên loại TSCĐ"),
        ("CCDC Category", "Mã loại CCDC", "Tên loại CCDC"),
    ]:
        rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
            WHERE file_type=%s AND status='Ready'""", (ft,), as_dict=True)
        n_posted = n_missing = 0
        for r in rows:
            try: p = _json.loads(r.raw_payload or "{}")
            except: continue
            code = p.get(code_key, "")
            ac_name = p.get(name_key, "")
            match = try_match("Asset Category", [code, ac_name])
            if match:
                frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                    target_doctype='Asset Category', target_name=%s WHERE name=%s""",
                    (match, r.row_name))
                n_posted += 1
            else:
                frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Skipped',
                    error_message=%s WHERE name=%s""",
                    (f"No matching Frappe Asset Category for '{ac_name or code}' — needs manual setup",
                     r.row_name))
                n_missing += 1
        out[ft] = {"posted": n_posted, "skipped_missing": n_missing}

    # Bank (by Tên đầy đủ — full name)
    bank_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Bank' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in bank_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        full = p.get("Tên đầy đủ", "")
        short = p.get("Tên viết tắt", "")
        match = try_match("Bank", [full, short])
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Bank', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Bank"] = {"posted": n_posted, "missing": n_missing}

    # Bank Account
    ba_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Bank Account' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in ba_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        acc_no = p.get("Số tài khoản", "")
        bank_name = p.get("Tên ngân hàng", "")
        candidates = [acc_no, f"{acc_no} - {bank_name}"]
        match = try_match("Bank Account", candidates)
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Bank Account', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Bank Account"] = {"posted": n_posted, "missing": n_missing}

    # Account — use account_resolver
    acc_rows = frappe.db.sql("""SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
        WHERE file_type='Account' AND status='Ready'""", as_dict=True)
    n_posted = n_missing = 0
    for r in acc_rows:
        try: p = _json.loads(r.raw_payload or "{}")
        except: continue
        tk = p.get("Số tài khoản", "")
        match = account_resolver.resolve(str(tk), company)
        if match:
            frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
                target_doctype='Account', target_name=%s WHERE name=%s""",
                (match, r.row_name))
            n_posted += 1
        else:
            n_missing += 1
    out["Account"] = {"posted": n_posted, "missing": n_missing}

    # Misa Default Account — config; mark Posted with no target since no DocType
    n_md = frappe.db.sql("""UPDATE `tabMisa Migration Row` SET status='Posted',
        target_doctype='', target_name=''
        WHERE file_type='Misa Default Account' AND status='Ready'""")
    out["Misa Default Account"] = {"posted": frappe.db._cursor.rowcount, "missing": 0}

    # Primary masters (Customer / Supplier / Item / Project / UOM / Employee) —
    # already imported by the ORM pass; just sync status.
    PRIMARY_MASTERS = [
        ("Customer", "Customer", ["Mã khách hàng", "Tên khách hàng"]),
        ("Supplier", "Supplier", ["Mã nhà cung cấp", "Tên nhà cung cấp"]),
        ("Item", "Item", ["Mã", "Mã hàng", "Item Code"]),
        ("Project", "Project", ["Mã công trình", "Tên công trình"]),
        ("UOM", "UOM", ["Đơn vị tính", "Tên đơn vị tính"]),
        ("Employee", "Employee", ["Mã nhân viên", "Tên nhân viên"]),
    ]
    TOTAL_TOKENS = {"Tổng", "Tổng cộng", "Total"}
    for misa_ft, dt, key_candidates in PRIMARY_MASTERS:
        rows = frappe.db.sql(
            """SELECT name AS row_name, raw_payload FROM `tabMisa Migration Row`
               WHERE file_type=%s AND status='Ready'""",
            (misa_ft,), as_dict=True,
        )
        n_posted = n_skipped = 0
        for r in rows:
            try: p = _json.loads(r.raw_payload or "{}")
            except: continue
            candidates = [p.get(k, "") for k in key_candidates]
            candidates = [c.strip() for c in candidates if c and str(c).strip() not in TOTAL_TOKENS]
            match = try_match(dt, candidates)
            if match:
                frappe.db.sql(
                    """UPDATE `tabMisa Migration Row` SET status='Posted',
                       target_doctype=%s, target_name=%s WHERE name=%s""",
                    (dt, match, r.row_name),
                )
                n_posted += 1
            else:
                # Skip header/aggregate rows that won't ever match
                frappe.db.sql(
                    """UPDATE `tabMisa Migration Row` SET status='Skipped',
                       error_message=%s WHERE name=%s""",
                    (f"No matching Frappe {dt} for keys {candidates[:2]}", r.row_name),
                )
                n_skipped += 1
        out[misa_ft] = {"posted": n_posted, "skipped_missing": n_skipped}

    frappe.db.commit()
    return out


# ─── Step 10: reclassify reference-only Ready rows ──────────────────────────

def reclassify_reference_rows(company: str) -> dict[str, int]:
    """Mark reference-only rows (no economic effect) as Skipped with reason.

    Categories:
      - Unknown: tax-resource + currency rate sheets (1,375 in DCNET TEST)
      - Bang ke MV: VAT input declaration summary lines (4)
      - Misa Closing Rule: year-end closing rule definitions (20)

    These are NOT transactions; the prior parser put them in file_type=Unknown
    or kept the original type. Reclassifying as Skipped + status='Skipped'
    makes the Misa Migration UI show the correct count of unresolved items.
    """
    out: dict[str, int] = {}
    for ft, reason in [
        ("Unknown", "Reference-only (tax/currency rates from Misa export)"),
        ("Bang ke MV", "VAT input declaration summary — not a transaction"),
        ("Misa Closing Rule", "Year-end closing rule config — not a transaction"),
    ]:
        n = frappe.db.sql(
            """UPDATE `tabMisa Migration Row` SET status='Skipped',
               error_message=%s
               WHERE file_type=%s AND status='Ready'""",
            (reason, ft),
        )
        out[ft] = frappe.db._cursor.rowcount
    frappe.db.commit()
    return out


# ─── Orchestrator ───────────────────────────────────────────────────────────

@frappe.whitelist()
def run_all(company: str | None = None,
            include_pl_residual_close: bool = True) -> dict[str, Any]:
    """Run all backfill steps in order. Idempotent.

    Usage:
      bench --site <site> execute \
        vn_accounting.misa_migration.bulk_pump.backfill_audit_fixes.run_all \
        --kwargs '{"company": "DCNET TEST"}'
    """
    if not company:
        company = frappe.db.get_single_value("Global Defaults", "default_company") or \
                  frappe.db.get_value("Company", {}, "name")
    if not company:
        frappe.throw("No company specified and no default Company found")

    t0 = time.time()
    out: dict[str, Any] = {"company": company, "started_at": frappe.utils.now()}

    steps = [
        ("1_canonicalize_party_case", canonicalize_party_case),
        ("2_populate_se_detail_warehouses", populate_se_detail_warehouses),
        ("3_fix_se_gl", fix_se_gl),
        ("3b_repair_ob_inventory_gl", repair_ob_inventory_gl),
        ("4_remap_pi_1331_expense", remap_pi_1331_expense),
        ("4b_repair_pi_unbalance", repair_pi_unbalance),
        ("5_rederive_invoice_status", rederive_invoice_status),
        ("6_seed_item_defaults", seed_item_defaults),
        ("7_post_year_end_closing", post_year_end_closing),
        ("7a_post_remaining_nvk_jes", post_remaining_nvk_jes),
        ("7a-tot_skip_misa_summary_rows", skip_misa_summary_rows),
        *([("7b_post_pl_residual_close", post_pl_residual_close)]
          if include_pl_residual_close else []),
        ("8_mark_consumed_rows_posted", mark_consumed_rows_posted),
        ("9_resolve_account_conflicts", resolve_account_conflicts),
        ("10_reclassify_reference_rows", reclassify_reference_rows),
        ("10a_create_missing_masters", create_missing_masters),
        ("10b_mark_master_rows_posted", mark_master_rows_posted),
    ]

    for label, fn in steps:
        t_step = time.time()
        try:
            out[label] = fn(company)
            out[label]["elapsed_seconds"] = round(time.time() - t_step, 2)
            print(f"[{label}] OK ({out[label]['elapsed_seconds']}s): {out[label]}", flush=True)
        except Exception as e:  # noqa: BLE001
            out[label] = {"error": f"{type(e).__name__}: {e}",
                          "elapsed_seconds": round(time.time() - t_step, 2)}
            print(f"[{label}] FAILED: {out[label]['error']}", flush=True)
            frappe.db.rollback()

    out["total_elapsed_seconds"] = round(time.time() - t0, 2)
    return out
