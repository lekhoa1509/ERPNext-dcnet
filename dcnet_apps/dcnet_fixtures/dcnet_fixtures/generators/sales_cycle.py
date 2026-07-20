"""
Sales Cycle Generator for DCNET 3-Year Data

Full selling cycle with 50% YoY growth:
  Sales Order (Submit)
  → Delivery Note (Stock exit, Submit) - REQUIRES stock to exist
    → Sales Invoice (VAT 10%, Submit)
      → Payment Entry (Submit, 80-90% of invoices)

IMPORTANT: Run stock_management.setup_all_stock() BEFORE this generator
to ensure warehouses have sufficient inventory.

Usage:
    from dcnet_fixtures.dcnet_fixtures.generators.sales_cycle import generate_sales_3y
    generate_sales_3y()
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


def _get_stock_warehouses(company, abbr):
    """Return warehouses available for outbound stock, in priority order"""
    candidates = [
        f"Kho Chính HCM - {abbr}",
        f"Kho Showroom Hà Nội - {abbr}",
        f"Stores - {abbr}",
        f"Finished Goods - {abbr}",
    ]
    available = [w for w in candidates if frappe.db.exists("Warehouse", w)]
    if not available:
        fallback = frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")
        if fallback:
            available = [fallback]
    return available


def _get_sales_tax_template(abbr):
    candidates = [
        f"VAT 10% Bán Hàng - {abbr}",
        f"Vietnam Tax - {abbr}",
    ]
    for t in candidates:
        if frappe.db.exists("Sales Taxes and Charges Template", t):
            return t
    return frappe.db.get_value("Sales Taxes and Charges Template", {"company": ["!=", ""]}, "name")


def _get_bank_account(company, abbr):
    candidates = [f"Bank - {abbr}", f"Cash - {abbr}"]
    for acc in candidates:
        if frappe.db.exists("Account", acc):
            return acc
    return frappe.db.get_value("Account", {
        "company": company,
        "account_type": ["in", ["Bank", "Cash"]],
        "is_group": 0
    }, "name")


def _quarter_dates(year, quarter):
    q_starts = {1: f"{year}-01-01", 2: f"{year}-04-01", 3: f"{year}-07-01", 4: f"{year}-10-01"}
    q_ends   = {1: f"{year}-03-31", 2: f"{year}-06-30", 3: f"{year}-09-30", 4: f"{year}-12-31"}
    return getdate(q_starts[quarter]), getdate(q_ends[quarter])


def _random_date(start, end):
    delta = (end - start).days
    return add_days(start, randint(0, max(0, delta)))


def _quarter_so_count(year, quarter):
    cfg = GROWTH_CONFIG.get(year, GROWTH_CONFIG[2023])
    base = cfg["so_per_quarter"]
    seasonal = SEASONAL_MULTIPLIERS[quarter]
    return max(1, int(base * seasonal))


def _get_available_qty(item_code, warehouse):
    """Get actual available qty from Bin table"""
    qty = frappe.db.get_value("Bin", {
        "item_code": item_code,
        "warehouse": warehouse,
    }, "actual_qty") or 0
    return flt(qty)


def _find_best_warehouse(item_code, required_qty, warehouses):
    """
    Find the warehouse with enough stock for the given item.
    Returns warehouse_name or None if no warehouse has enough stock.
    """
    for wh in warehouses:
        available = _get_available_qty(item_code, wh)
        if available >= required_qty:
            return wh
    return None


# =============================================================================
# SALES ORDER → DELIVERY → INVOICE → PAYMENT
# =============================================================================

def build_so_items_with_stock_check(items, warehouses, is_b2b, avg_val):
    """
    Build SO line items ensuring each item's warehouse has sufficient stock.
    Returns list of items or empty list if unable to satisfy with available stock.
    """
    num_items = randint(2, min(6, len(items))) if is_b2b else randint(1, min(3, len(items)))
    candidates = sample(items, min(num_items * 3, len(items)))  # Sample more to allow fallback

    so_items = []
    used_items = set()

    for item in candidates:
        if item["item_code"] in used_items:
            continue
        if len(so_items) >= num_items:
            break

        qty = randint(2, 8) if is_b2b else randint(1, 3)

        # Find a warehouse with enough stock for this item+qty
        best_wh = _find_best_warehouse(item["item_code"], qty, warehouses)
        if best_wh is None:
            # Try with qty=1 as fallback
            best_wh = _find_best_warehouse(item["item_code"], 1, warehouses)
            qty = 1

        if best_wh is None:
            continue  # Skip this item, no stock anywhere

        rate = max(100_000, int(avg_val / num_items * uniform(0.8, 1.4)))

        so_items.append({
            "item_code": item["item_code"],
            "qty": qty,
            "rate": rate,
            "delivery_date": None,  # will be set by caller
            "warehouse": best_wh,
        })
        used_items.add(item["item_code"])

    return so_items


def generate_sales_order(customer, items, transaction_date, delivery_date, warehouses, tax_template, company):
    """Create and submit a Sales Order with stock-aware warehouse assignment"""
    cfg = GROWTH_CONFIG.get(transaction_date.year, GROWTH_CONFIG[2023])
    avg_val = cfg["avg_order_value"]
    is_b2b = frappe.db.get_value("Customer", customer, "customer_type") == "Company"
    order_size_mult = uniform(1.8, 3.0) if is_b2b else uniform(0.6, 1.4)
    avg_val_adjusted = avg_val * order_size_mult

    so_items = build_so_items_with_stock_check(items, warehouses, is_b2b, avg_val_adjusted)

    if not so_items:
        raise ValueError("No items with available stock found for this SO")

    # Set delivery_date on each item
    for it in so_items:
        it["delivery_date"] = delivery_date

    so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": customer,
        "transaction_date": transaction_date,
        "delivery_date": delivery_date,
        "company": company,
        "items": so_items,
        "taxes_and_charges": tax_template,
    })
    so.flags.ignore_permissions = True
    so.flags.ignore_mandatory = True
    so.insert()
    so.submit()
    return so


def generate_delivery_note(so_doc, delivery_date, partial=False):
    """
    Create Delivery Note from submitted Sales Order.
    Stock MUST exist - this validates using real stock.
    """
    from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
    dn = make_delivery_note(so_doc.name)
    # Must set set_posting_time=1 to allow changing posting_date (like ticking 'Edit Posting Date and Time')
    dn.set_posting_time = 1
    dn.posting_date = delivery_date

    if partial:
        for item in dn.items:
            # Only reduce qty if there's stock to justify partial delivery
            available = _get_available_qty(item.item_code, item.warehouse)
            max_deliverable = min(item.qty, int(available))
            item.qty = max(1, int(max_deliverable * uniform(0.5, 0.85)))

    dn.flags.ignore_permissions = True
    dn.flags.ignore_mandatory = True
    dn.insert()
    dn.submit()
    return dn


def generate_sales_invoice_from_dn(dn_doc, invoice_date, tax_template):
    """Create Sales Invoice from Delivery Note"""
    from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
    si = make_sales_invoice(dn_doc.name)
    si.posting_date = invoice_date

    # due_date must be >= posting_date
    # For B2B: net 30-45 days; for B2C: same day
    customer_type = frappe.db.get_value("Customer", dn_doc.customer, "customer_type")
    due_offset = randint(15, 45) if customer_type == "Company" else 0
    si.due_date = add_days(invoice_date, due_offset)
    # Safety: ensure due_date is never before posting_date
    if si.due_date < invoice_date:
        si.due_date = invoice_date

    if tax_template:
        si.taxes_and_charges = tax_template

    si.flags.ignore_permissions = True
    si.flags.ignore_mandatory = True
    # Bypass 'Due Date cannot be before Posting Date' validation for historical data
    si.flags.ignore_validate = True
    si.insert()
    # Re-assert due_date after insert (some hooks may reset it)
    if si.due_date < si.posting_date:
        frappe.db.set_value("Sales Invoice", si.name, "due_date", si.posting_date, update_modified=False)
    si.submit()
    return si


def generate_payment_for_sales_invoice(si_doc, payment_date, bank_account_placeholder, company):
    """Create Payment Entry for a submitted Sales Invoice using TT200 accounts"""
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

    pe = get_payment_entry("Sales Invoice", si_doc.name)
    pe.posting_date = payment_date
    pe.reference_no = f"PT-{payment_date.strftime('%Y%m')}-{randint(10000, 99999)}"
    pe.reference_date = payment_date

    # Logic for TT200: > 10M VND must be Bank (1121)
    grand_total = float(si_doc.grand_total)
    
    cash_acc = frappe.db.get_value("Account", {"account_number": "1111", "company": company}, "name")
    bank_acc = frappe.db.get_value("Account", {"account_number": "1121", "company": company}, "name")
    
    if grand_total >= 10_000_000:
        # Business/Large: 95% Bank
        pe.paid_to = bank_acc or bank_account_placeholder
        pe.mode_of_payment = "Wire Transfer"
    else:
        # Small: 60% Cash, 40% Bank
        if random() < 0.6 and cash_acc:
            pe.paid_to = cash_acc
            pe.mode_of_payment = "Cash"
        else:
            pe.paid_to = bank_acc or bank_account_placeholder
            pe.mode_of_payment = "Wire Transfer"

    pe.flags.ignore_permissions = True
    pe.flags.ignore_mandatory = True
    pe.insert()
    pe.submit()
    return pe


# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_sales_3y(years=None, commit_every=10):
    """
    Generate full sales cycle for 3 years (2023-2026 Q1).
    Applies 50% YoY growth via GROWTH_CONFIG.

    PREREQUISITE: Run stock_management.setup_all_stock() first!

    Args:
        years: list of years, default [2023, 2024, 2025, 2026]
        commit_every: commit to DB every N sales orders
    """
    if years is None:
        years = [2023, 2024, 2025, 2026]

    print("\n" + "=" * 60)
    print("DCNET Sales Cycle Generator (3 Years)")
    print("=" * 60)

    company = _get_company()
    abbr = _get_abbr(company)
    warehouses = _get_stock_warehouses(company, abbr)
    tax_template = _get_sales_tax_template(abbr)
    bank_account = _get_bank_account(company, abbr)

    customers = frappe.get_all("Customer", pluck="name")
    items = frappe.get_all("Item",
        filters={"is_sales_item": 1, "disabled": 0},
        fields=["item_code", "item_name"]
    )

    if not customers or not items:
        print("  ⚠️  No customers or items found. Run master data first.")
        return {}

    print(f"  Company: {company} ({abbr})")
    print(f"  Warehouses: {warehouses}")
    print(f"  Tax Template: {tax_template}")
    print(f"  Customers: {len(customers)}, Items: {len(items)}")

    # Check stock exists
    total_bins = frappe.db.count("Bin", {"actual_qty": [">", 0]})
    if total_bins == 0:
        print("  ⚠️  WARNING: No stock found in any warehouse!")
        print("  Please run: bench --site flow.local dcnet-fixtures generate-3y --phase stock")
        print("  Proceeding anyway...")

    summary = {
        "sales_orders": 0,
        "delivery_notes": 0,
        "sales_invoices": 0,
        "payments": 0,
        "errors": 0,
        "skipped_no_stock": 0,
    }

    for year in years:
        quarters = [1, 2, 3, 4] if year < 2026 else [1]
        print(f"\n  Processing year {year}...")

        for quarter in quarters:
            start_date, end_date = _quarter_dates(year, quarter)
            count = _quarter_so_count(year, quarter)
            print(f"    Q{quarter}/{year}: {count} SOs")

            for i in range(count):
                try:
                    today = getdate(nowdate())
                    so_date = _random_date(start_date, min(end_date, today))
                    raw_delivery = add_days(so_date, randint(3, 14))
                    delivery_date = min(raw_delivery, today)

                    customer = choice(customers)

                    so = generate_sales_order(
                        customer=customer,
                        items=items,
                        transaction_date=so_date,
                        delivery_date=delivery_date,
                        warehouses=warehouses,
                        tax_template=tax_template,
                        company=company,
                    )
                    summary["sales_orders"] += 1

                    # Delivery: 85% full, 10% partial, 5% no delivery
                    r = random()
                    if r < 0.95:
                        dn_date = _random_date(so_date, delivery_date)

                        is_partial = (r > 0.85)
                        dn = generate_delivery_note(so, dn_date, partial=is_partial)
                        summary["delivery_notes"] += 1

                        # Invoice from Delivery Note (preferred) or SO
                        invoice_date = min(add_days(dn_date, randint(0, 5)), today)
                        si = generate_sales_invoice_from_dn(dn, invoice_date, tax_template)
                        summary["sales_invoices"] += 1

                        # Payment
                        customer_type = frappe.db.get_value("Customer", customer, "customer_type")
                        pay_prob = 0.85 if customer_type != "Company" else 0.70
                        if random() < pay_prob:
                            if customer_type == "Company":
                                payment_date = min(add_days(invoice_date, randint(7, 45)), today)
                            else:
                                payment_date = min(add_days(invoice_date, randint(0, 7)), today)
                            generate_payment_for_sales_invoice(si, payment_date, bank_account, company)
                            summary["payments"] += 1

                    if (i + 1) % commit_every == 0:
                        frappe.db.commit()

                except ValueError as ve:
                    # No stock available - skip this SO
                    summary["skipped_no_stock"] += 1
                except Exception as e:
                    summary["errors"] += 1
                    print(f"    ⚠️  Error on SO #{i+1} Q{quarter}/{year}: {str(e)[:100]}")
                    frappe.db.rollback()
                    continue

            frappe.db.commit()

    print("\n" + "=" * 60)
    print("Sales Cycle Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("=" * 60)
    return summary
