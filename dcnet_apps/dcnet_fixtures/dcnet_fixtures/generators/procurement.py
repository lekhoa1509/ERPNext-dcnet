"""
Procurement Cycle Generator for DCNET 3-Year Data

Full buying cycle with 50% YoY growth:
  Purchase Order (Submit)
  → Purchase Receipt (Stock entry, Submit)
    → Purchase Invoice (VAT 10%, Submit)
      → Payment Entry (Submit, 90% of invoices)

Usage:
    from dcnet_fixtures.dcnet_fixtures.generators.procurement import generate_procurement_3y
    generate_procurement_3y()
    frappe.db.commit()
"""

import frappe
from frappe.utils import getdate, add_days, flt, nowdate
from random import randint, choice, sample, random, uniform

from dcnet_fixtures.dcnet_fixtures.generators.foundation import GROWTH_CONFIG, SEASONAL_MULTIPLIERS


# =============================================================================
# HELPERS
# =============================================================================

def _get_company():
    return frappe.db.get_single_value("Global Defaults", "default_company") or \
           frappe.db.get_value("Company", {}, "name")


def _get_abbr(company):
    return frappe.db.get_value("Company", company, "abbr")


def _get_main_warehouse(company, abbr):
    """Return primary inbound warehouse"""
    candidates = [
        f"Kho Chính HCM - {abbr}",
        f"Stores - {abbr}",
        f"Finished Goods - {abbr}",
    ]
    for wh in candidates:
        if frappe.db.exists("Warehouse", wh):
            return wh
    return frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")


def _get_purchase_tax_template(abbr):
    tpl = f"VAT 10% Mua Hàng - {abbr}"
    if frappe.db.exists("Purchase Taxes and Charges Template", tpl):
        return tpl
    # Fallback: existing template
    existing = frappe.db.get_value("Purchase Taxes and Charges Template", {"company": ["!=", ""]}, "name")
    return existing


def _get_bank_account(company, abbr):
    """Get bank/cash account for payment"""
    candidates = [
        f"Bank - {abbr}",
        f"Cash - {abbr}",
        f"Debtors - {abbr}",
    ]
    for acc in candidates:
        if frappe.db.exists("Account", acc):
            return acc
    return frappe.db.get_value("Account", {"company": company, "account_type": ["in", ["Bank", "Cash"]], "is_group": 0}, "name")


def _get_creditors_account(company, abbr):
    candidates = [f"Creditors - {abbr}", f"Accounts Payable - {abbr}"]
    for acc in candidates:
        if frappe.db.exists("Account", acc):
            return acc
    return frappe.db.get_value("Account", {"company": company, "account_type": "Payable", "is_group": 0}, "name")


def _quarter_dates(year, quarter):
    """Return (start_date, end_date) for a given year/quarter"""
    q_starts = {1: f"{year}-01-01", 2: f"{year}-04-01", 3: f"{year}-07-01", 4: f"{year}-10-01"}
    q_ends   = {1: f"{year}-03-31", 2: f"{year}-06-30", 3: f"{year}-09-30", 4: f"{year}-12-31"}
    return getdate(q_starts[quarter]), getdate(q_ends[quarter])


def _random_date(start, end):
    delta = (end - start).days
    return add_days(start, randint(0, max(0, delta)))


def _quarter_po_count(year, quarter):
    cfg = GROWTH_CONFIG.get(year, GROWTH_CONFIG[2023])
    base = cfg["po_per_quarter"]
    seasonal = SEASONAL_MULTIPLIERS[quarter]
    return max(1, int(base * seasonal))


# =============================================================================
# PURCHASE ORDER → RECEIPT → INVOICE → PAYMENT
# =============================================================================

def generate_purchase_order(supplier, items, transaction_date, warehouse, schedule_date, tax_template, company):
    """Create and submit a Purchase Order"""
    cfg = GROWTH_CONFIG.get(transaction_date.year, GROWTH_CONFIG[2023])
    avg_val = cfg["avg_order_value"]

    po_items = []
    num_items = randint(2, min(8, len(items)))
    selected = sample(items, num_items)

    for item in selected:
        qty = randint(5, 50)
        # Cost = avg_order_value * 0.6 ± 30% variance, distributed per item
        rate = max(50_000, int(avg_val * 0.6 / num_items * uniform(0.7, 1.3)))
        po_items.append({
            "item_code": item["item_code"],
            "qty": qty,
            "rate": rate,
            "schedule_date": schedule_date,
            "warehouse": warehouse,
        })

    po = frappe.get_doc({
        "doctype": "Purchase Order",
        "supplier": supplier,
        "transaction_date": transaction_date,
        "schedule_date": schedule_date,
        "company": company,
        "items": po_items,
        "taxes_and_charges": tax_template,
    })
    po.flags.ignore_permissions = True
    po.flags.ignore_mandatory = True
    po.insert()
    po.submit()
    return po


def generate_purchase_receipt(po_doc, receipt_date, partial=False):
    """Create Purchase Receipt from submitted PO"""
    from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
    pr = make_purchase_receipt(po_doc.name)
    # Must set set_posting_time=1 to allow changing posting_date
    pr.set_posting_time = 1
    pr.posting_date = receipt_date

    if partial:
        for item in pr.items:
            item.qty = max(1, int(item.qty * uniform(0.4, 0.9)))
            item.received_qty = item.qty

    pr.flags.ignore_permissions = True
    pr.flags.ignore_mandatory = True
    pr.insert()
    pr.submit()
    return pr


def generate_purchase_invoice(po_doc, invoice_date, tax_template, pr_doc=None):
    """Create Purchase Invoice from submitted PO (or PR if available)"""
    from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_invoice
    pi = make_purchase_invoice(po_doc.name)
    pi.posting_date = invoice_date
    pi.bill_date = invoice_date
    pi.bill_no = f"INV-{invoice_date.strftime('%Y%m')}-{randint(10000, 99999)}"
    if tax_template:
        pi.taxes_and_charges = tax_template
    # Ensure bill_date is not after posting_date
    if pi.bill_date and pi.posting_date and pi.bill_date > pi.posting_date:
        pi.bill_date = pi.posting_date

    pi.flags.ignore_permissions = True
    pi.flags.ignore_mandatory = True
    pi.flags.ignore_validate = True
    pi.insert()
    pi.submit()
    return pi


def generate_payment_for_invoice(pi_doc, payment_date, bank_account_placeholder, company, abbr):
    """Create Payment Entry for a submitted Purchase Invoice using TT200 accounts"""
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

    pe = get_payment_entry("Purchase Invoice", pi_doc.name)
    pe.posting_date = payment_date
    pe.reference_no = f"TT-{payment_date.strftime('%Y%m')}-{randint(10000, 99999)}"
    pe.reference_date = payment_date

    # TT200: > 20M must be Bank (Law on Tax Administration)
    grand_total = float(pi_doc.grand_total)
    
    cash_acc = frappe.db.get_value("Account", {"account_number": "1111", "company": company}, "name")
    bank_acc = frappe.db.get_value("Account", {"account_number": "1121", "company": company}, "name")

    if grand_total >= 20_000_000:
        pe.paid_from = bank_acc or bank_account_placeholder
        pe.mode_of_payment = "Wire Transfer"
    else:
        # Small supply: 40% Cash, 60% Bank
        if random() < 0.4 and cash_acc:
            pe.paid_from = cash_acc
            pe.mode_of_payment = "Cash"
        else:
            pe.paid_from = bank_acc or bank_account_placeholder
            pe.mode_of_payment = "Wire Transfer"

    pe.flags.ignore_permissions = True
    pe.flags.ignore_mandatory = True
    pe.insert()
    pe.submit()
    return pe


# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_procurement_3y(years=None, commit_every=10):
    """
    Generate full procurement cycle for 3 years (2023-2026 Q1).
    Applies 50% YoY growth via GROWTH_CONFIG.

    Args:
        years: list of years to generate, default [2023, 2024, 2025, 2026]
        commit_every: commit to DB every N purchase orders
    """
    if years is None:
        years = [2023, 2024, 2025, 2026]

    print("\n" + "=" * 60)
    print("DCNET Procurement Cycle Generator (3 Years)")
    print("=" * 60)

    company = _get_company()
    abbr = _get_abbr(company)
    warehouse = _get_main_warehouse(company, abbr)
    tax_template = _get_purchase_tax_template(abbr)
    bank_account = _get_bank_account(company, abbr)

    suppliers = frappe.get_all("Supplier", pluck="name")
    items = frappe.get_all("Item",
        filters={"is_purchase_item": 1, "disabled": 0},
        fields=["item_code", "item_name"]
    )

    if not suppliers or not items:
        print("  ⚠️  No suppliers or items found. Run master data first.")
        return {}

    print(f"  Company: {company} ({abbr})")
    print(f"  Warehouse: {warehouse}")
    print(f"  Tax Template: {tax_template}")
    print(f"  Suppliers: {len(suppliers)}, Items: {len(items)}")

    summary = {"purchase_orders": 0, "purchase_receipts": 0, "purchase_invoices": 0, "payments": 0, "errors": 0}

    for year in years:
        quarters = [1, 2, 3, 4] if year < 2026 else [1]  # Only Q1 for 2026
        print(f"\n  Processing year {year}...")

        for quarter in quarters:
            start_date, end_date = _quarter_dates(year, quarter)
            count = _quarter_po_count(year, quarter)
            print(f"    Q{quarter}/{year}: {count} POs")

            for i in range(count):
                try:
                    # PO date within quarter
                    po_date = _random_date(start_date, end_date)
                    schedule_date = add_days(po_date, randint(14, 45))

                    supplier = choice(suppliers)

                    po = generate_purchase_order(
                        supplier=supplier,
                        items=items,
                        transaction_date=po_date,
                        warehouse=warehouse,
                        schedule_date=schedule_date,
                        tax_template=tax_template,
                        company=company,
                    )
                    summary["purchase_orders"] += 1

                    # Receipt: 80% full, 15% partial, 5% no receipt (cancelled/pending)
                    r = random()
                    if r < 0.95:  # 95% get a receipt
                        today = getdate(nowdate())
                        receipt_date = min(add_days(po_date, randint(3, 20)), today)
                        is_partial = (r > 0.80)
                        pr = generate_purchase_receipt(po, receipt_date, partial=is_partial)
                        summary["purchase_receipts"] += 1

                        # Invoice: capped at today
                        invoice_date = min(add_days(receipt_date, randint(1, 7)), today)
                        pi = generate_purchase_invoice(po, invoice_date, tax_template, pr_doc=pr)
                        summary["purchase_invoices"] += 1

                        # Payment: 90% of invoices get paid
                        if random() < 0.90:
                            payment_date = min(add_days(invoice_date, randint(1, 30)), today)
                            generate_payment_for_invoice(pi, payment_date, bank_account, company, abbr)
                            summary["payments"] += 1

                    if (i + 1) % commit_every == 0:
                        frappe.db.commit()

                except Exception as e:
                    summary["errors"] += 1
                    print(f"    ⚠️  Error on PO #{i+1} Q{quarter}/{year}: {str(e)[:80]}")
                    frappe.db.rollback()
                    continue

            frappe.db.commit()

    print("\n" + "=" * 60)
    print("Procurement Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("=" * 60)
    return summary
