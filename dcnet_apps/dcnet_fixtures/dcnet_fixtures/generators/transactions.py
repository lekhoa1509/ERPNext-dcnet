"""
Transaction Generators for DCNET Fixtures

Use these generators to create additional transactions programmatically.

Usage in bench console:
    from dcnet_fixtures.generators.transactions import generate_sales_orders
    generate_sales_orders(start_date="2025-04-01", end_date="2025-06-30", count=50)
    frappe.db.commit()
"""

import frappe
from frappe.utils import getdate, add_days, flt
from random import randint, choice, sample
from datetime import datetime


def generate_sales_orders(start_date, end_date, count=50, submit=False):
    """
    Generate random Sales Orders within date range

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        count: Number of Sales Orders to generate
        submit: Whether to submit the orders (default: False, saves as Draft)

    Returns:
        List of created Sales Order names
    """
    # Get available data
    customers = frappe.get_list("Customer", pluck="name")
    items = frappe.get_list("Item",
        filters={"is_sales_item": 1, "item_code": ["like", "GOLF-%"]},
        fields=["item_code", "standard_rate", "stock_uom"]
    )

    if not customers or not items:
        frappe.throw("Please install master data first: dcnet-fixtures install --module master")

    start = getdate(start_date)
    end = getdate(end_date)
    date_range = (end - start).days

    created_orders = []

    for i in range(count):
        # Random date within range
        random_days = randint(0, date_range)
        transaction_date = add_days(start, random_days)
        delivery_date = add_days(transaction_date, randint(3, 10))

        # Random customer
        customer = choice(customers)

        # Random items (1-5 items per order)
        num_items = randint(1, min(5, len(items)))
        selected_items = sample(items, num_items)

        so_items = []
        for item in selected_items:
            qty = randint(1, 5)
            so_items.append({
                "item_code": item.item_code,
                "qty": qty,
                "rate": flt(item.standard_rate or 1000000),
                "delivery_date": delivery_date
            })

        try:
            so = frappe.get_doc({
                "doctype": "Sales Order",
                "customer": customer,
                "transaction_date": transaction_date,
                "delivery_date": delivery_date,
                "items": so_items
            })
            so.flags.ignore_permissions = True
            so.insert()

            if submit:
                so.submit()

            created_orders.append(so.name)
            print(f"Created SO: {so.name} for {customer}")

        except Exception as e:
            print(f"Error creating SO #{i+1}: {str(e)}")
            continue

    return created_orders


def generate_purchase_orders(start_date, end_date, count=30, submit=False):
    """
    Generate random Purchase Orders within date range

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        count: Number of Purchase Orders to generate
        submit: Whether to submit the orders (default: False)

    Returns:
        List of created Purchase Order names
    """
    suppliers = frappe.get_list("Supplier", pluck="name")
    items = frappe.get_list("Item",
        filters={"is_purchase_item": 1, "item_code": ["like", "GOLF-%"]},
        fields=["item_code", "valuation_rate", "stock_uom"]
    )

    if not suppliers or not items:
        frappe.throw("Please install master data first: dcnet-fixtures install --module master")

    start = getdate(start_date)
    end = getdate(end_date)
    date_range = (end - start).days

    created_orders = []

    for i in range(count):
        random_days = randint(0, date_range)
        transaction_date = add_days(start, random_days)
        schedule_date = add_days(transaction_date, randint(7, 21))

        supplier = choice(suppliers)

        num_items = randint(2, 6)
        selected_items = sample(items, min(num_items, len(items)))

        po_items = []
        for item in selected_items:
            qty = randint(5, 30)
            po_items.append({
                "item_code": item.item_code,
                "qty": qty,
                "rate": flt(item.valuation_rate or 500000),
                "schedule_date": schedule_date
            })

        try:
            po = frappe.get_doc({
                "doctype": "Purchase Order",
                "supplier": supplier,
                "transaction_date": transaction_date,
                "schedule_date": schedule_date,
                "items": po_items
            })
            po.flags.ignore_permissions = True
            po.insert()

            if submit:
                po.submit()

            created_orders.append(po.name)
            print(f"Created PO: {po.name} for {supplier}")

        except Exception as e:
            print(f"Error creating PO #{i+1}: {str(e)}")
            continue

    return created_orders


def generate_invoices_from_orders(doctype="Sales Order", limit=None, submit_invoice=False):
    """
    Generate invoices from submitted orders

    Args:
        doctype: "Sales Order" or "Purchase Order"
        limit: Max number of orders to process (None = all)
        submit_invoice: Whether to submit invoices

    Returns:
        List of created invoice names
    """
    from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
    from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_invoice

    filters = {"docstatus": 1, "per_billed": ["<", 100]}
    orders = frappe.get_list(doctype, filters=filters, pluck="name", limit=limit)

    created_invoices = []

    for order_name in orders:
        try:
            if doctype == "Sales Order":
                invoice = make_sales_invoice(order_name)
            else:
                invoice = make_purchase_invoice(order_name)

            invoice.flags.ignore_permissions = True
            invoice.insert()

            if submit_invoice:
                invoice.submit()

            created_invoices.append(invoice.name)
            print(f"Created invoice: {invoice.name} from {order_name}")

        except Exception as e:
            print(f"Error creating invoice from {order_name}: {str(e)}")
            continue

    return created_invoices


def generate_payments_from_invoices(doctype="Sales Invoice", limit=None, submit_payment=False):
    """
    Generate payments from submitted invoices

    Args:
        doctype: "Sales Invoice" or "Purchase Invoice"
        limit: Max number of invoices to process
        submit_payment: Whether to submit payments

    Returns:
        List of created payment names
    """
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

    filters = {"docstatus": 1, "outstanding_amount": [">", 0]}
    invoices = frappe.get_list(doctype, filters=filters, pluck="name", limit=limit)

    created_payments = []

    for invoice_name in invoices:
        try:
            payment = get_payment_entry(doctype, invoice_name)
            payment.flags.ignore_permissions = True
            payment.reference_no = f"PAY-{invoice_name}"
            payment.insert()

            if submit_payment:
                payment.submit()

            created_payments.append(payment.name)
            print(f"Created payment: {payment.name} for {invoice_name}")

        except Exception as e:
            print(f"Error creating payment for {invoice_name}: {str(e)}")
            continue

    return created_payments


def generate_full_cycle(start_date, end_date, so_count=50, po_count=30, submit_all=False):
    """
    Generate full transaction cycle: PO → Receipt → SO → Delivery → Invoice → Payment

    Args:
        start_date: Start date
        end_date: End date
        so_count: Number of Sales Orders
        po_count: Number of Purchase Orders
        submit_all: Submit all documents (creates GL entries)

    Returns:
        Summary dict of created documents
    """
    print("=" * 60)
    print("Generating Full Transaction Cycle")
    print("=" * 60)

    summary = {
        "purchase_orders": [],
        "sales_orders": [],
        "sales_invoices": [],
        "purchase_invoices": [],
        "payments": []
    }

    # Step 1: Create Purchase Orders
    print("\n[1/5] Creating Purchase Orders...")
    summary["purchase_orders"] = generate_purchase_orders(
        start_date, end_date, po_count, submit=submit_all
    )

    # Step 2: Create Sales Orders
    print("\n[2/5] Creating Sales Orders...")
    summary["sales_orders"] = generate_sales_orders(
        start_date, end_date, so_count, submit=submit_all
    )

    if submit_all:
        frappe.db.commit()

        # Step 3: Create Invoices
        print("\n[3/5] Creating Sales Invoices...")
        summary["sales_invoices"] = generate_invoices_from_orders(
            "Sales Order", submit_invoice=submit_all
        )

        print("\n[4/5] Creating Purchase Invoices...")
        summary["purchase_invoices"] = generate_invoices_from_orders(
            "Purchase Order", submit_invoice=submit_all
        )

        frappe.db.commit()

        # Step 4: Create Payments (partial - 70% of invoices)
        print("\n[5/5] Creating Payments...")
        si_limit = int(len(summary["sales_invoices"]) * 0.7)
        pi_limit = int(len(summary["purchase_invoices"]) * 0.7)

        si_payments = generate_payments_from_invoices(
            "Sales Invoice", limit=si_limit, submit_payment=submit_all
        )
        pi_payments = generate_payments_from_invoices(
            "Purchase Invoice", limit=pi_limit, submit_payment=submit_all
        )

        summary["payments"] = si_payments + pi_payments

    frappe.db.commit()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Purchase Orders: {len(summary['purchase_orders'])}")
    print(f"  Sales Orders: {len(summary['sales_orders'])}")
    print(f"  Sales Invoices: {len(summary['sales_invoices'])}")
    print(f"  Purchase Invoices: {len(summary['purchase_invoices'])}")
    print(f"  Payments: {len(summary['payments'])}")
    print("=" * 60)

    return summary
