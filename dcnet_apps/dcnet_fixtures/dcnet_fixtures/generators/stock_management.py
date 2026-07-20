"""
Stock Management Generator for DCNET 3-Year Data

Creates:
1. Opening Stock Entries - khởi tạo tồn kho ban đầu (01/01/2023)
   Đây là bước tiên quyết, phải chạy trước Procurement và Sales.

2. Stock Transfers - điều chuyển hàng giữa kho theo quý:
   Kho Chính HCM → Kho Showroom Hà Nội (để showroom HN có hàng bán từ 2025)

Usage:
    from dcnet_fixtures.dcnet_fixtures.generators.stock_management import (
        generate_opening_stock,
        generate_stock_transfers,
    )
    generate_opening_stock()
    frappe.db.commit()
"""

import frappe
from frappe.utils import getdate, add_days, flt, nowdate
from random import randint, choice, sample, uniform


# =============================================================================
# HELPERS
# =============================================================================

def _get_company():
    return frappe.db.get_single_value("Global Defaults", "default_company") or \
           frappe.db.get_value("Company", {}, "name")


def _get_abbr(company):
    return frappe.db.get_value("Company", company, "abbr")


def _get_stock_account(company, abbr, warehouse_name=None):
    """Get default stock adjustment account"""
    candidates = [
        f"Stock Adjustment - {abbr}",
        f"Temporary Opening - {abbr}",
        f"Opening Balance Equity - {abbr}",
    ]
    for acc in candidates:
        if frappe.db.exists("Account", acc):
            return acc
    # Fallback: any Expense account
    return frappe.db.get_value("Account", {
        "company": company,
        "root_type": "Expense",
        "is_group": 0,
    }, "name")


def _get_actual_qty(item_code, warehouse):
    """Get current stock qty for item in warehouse"""
    qty = frappe.db.get_value("Bin", {
        "item_code": item_code,
        "warehouse": warehouse,
    }, "actual_qty") or 0
    return flt(qty)


# =============================================================================
# OPENING STOCK
# =============================================================================

def generate_opening_stock(opening_date="2023-01-01"):
    """
    Create Stock Entry (Material Receipt) for opening stock on 2023-01-01.

    Each item gets initial stock in each main warehouse proportional to:
    - Kho Chính HCM: 200-500 units (main stock)
    - Kho Showroom Hà Nội: 30-80 units (display stock from 2023 already)
    - Kho Fitting: 10-30 units (fitting equipment only)

    This ensures all warehouses have enough stock for 3 years of sales.
    """
    print("\n[Stock] Generating Opening Stock (2023-01-01)...")

    company = _get_company()
    abbr = _get_abbr(company)
    opening_date = getdate(opening_date)

    items = frappe.get_all("Item",
        filters={"is_stock_item": 1, "disabled": 0},
        fields=["item_code", "item_name", "stock_uom", "standard_rate"]
    )

    if not items:
        print("  ⚠️  No stock items found. Install master data first.")
        return []

    print(f"  Found {len(items)} stock items")

    # Warehouses to stock
    warehouse_configs = [
        {
            "warehouse": f"Kho Chính HCM - {abbr}",
            "qty_range": (200, 500),
            "valuation_mult": 0.60,  # cost price ~60% of standard rate
        },
        {
            "warehouse": f"Kho Showroom Hà Nội - {abbr}",
            "qty_range": (30, 80),
            "valuation_mult": 0.60,
        },
        {
            "warehouse": f"Kho Fitting - {abbr}",
            "qty_range": (5, 20),
            "valuation_mult": 0.60,
        },
    ]

    stock_account = _get_stock_account(company, abbr)
    if not stock_account:
        print("  ⚠️  No stock difference account found.")
        return []

    created = []
    errors = 0

    for wh_cfg in warehouse_configs:
        warehouse = wh_cfg["warehouse"]
        if not frappe.db.exists("Warehouse", warehouse):
            print(f"  ⚠️  Warehouse '{warehouse}' not found, skipping...")
            continue

        print(f"  Creating opening stock for {warehouse}...")

        # Create one big Stock Entry per warehouse with all items
        se_items = []
        for item in items:
            qty = randint(*wh_cfg["qty_range"])
            rate = flt(item.standard_rate) * wh_cfg["valuation_mult"]
            if rate <= 0:
                rate = randint(50_000, 5_000_000)

            se_items.append({
                "item_code": item.item_code,
                "qty": qty,
                "t_warehouse": warehouse,
                "valuation_rate": rate,
                "basic_rate": rate,
            })

        # Split into batches of 50 items to avoid timeout
        batch_size = 50
        for batch_start in range(0, len(se_items), batch_size):
            batch = se_items[batch_start:batch_start + batch_size]
            try:
                se = frappe.get_doc({
                    "doctype": "Stock Entry",
                    "stock_entry_type": "Material Receipt",
                    "set_posting_time": 1,
                    "posting_date": opening_date,
                    "company": company,
                    "remarks": f"Opening stock for {warehouse} - {opening_date}",
                    "items": batch,
                })
                se.flags.ignore_permissions = True
                se.flags.ignore_mandatory = True
                se.insert()
                se.submit()
                created.append(se.name)
                frappe.db.commit()
                print(f"    ✅ Batch {batch_start//batch_size + 1}: {len(batch)} items → {warehouse}")
            except Exception as e:
                errors += 1
                print(f"    ⚠️  Error creating opening stock batch for {warehouse}: {str(e)[:100]}")
                frappe.db.rollback()

    print(f"\n  Opening Stock: {len(created)} stock entries created, {errors} errors")
    return created


# =============================================================================
# QUARTERLY RESTOCKING (procurement supplement)
# =============================================================================

def generate_quarterly_restock(year, quarter, warehouse=None):
    """
    Create a quarterly restock Stock Entry (Material Receipt) to ensure
    sufficient inventory for sales. This supplements PO→PR flow.

    Used when procurement receipts are insufficient for sales volume.
    """
    company = _get_company()
    abbr = _get_abbr(company)

    if warehouse is None:
        warehouse = f"Kho Chính HCM - {abbr}"
        if not frappe.db.exists("Warehouse", warehouse):
            warehouse = frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")

    q_dates = {
        1: f"{year}-01-15",
        2: f"{year}-04-15",
        3: f"{year}-07-15",
        4: f"{year}-10-15",
    }
    posting_date = getdate(q_dates[quarter])
    today = getdate(nowdate())
    posting_date = min(posting_date, today)

    items = frappe.get_all("Item",
        filters={"is_stock_item": 1, "disabled": 0},
        fields=["item_code", "standard_rate"]
    )

    if not items:
        return None

    stock_account = _get_stock_account(company, abbr)
    se_items = []
    for item in items:
        qty = randint(50, 150)
        rate = flt(item.standard_rate) * 0.60
        if rate <= 0:
            rate = randint(50_000, 2_000_000)
        se_items.append({
            "item_code": item.item_code,
            "qty": qty,
            "t_warehouse": warehouse,
            "valuation_rate": rate,
            "basic_rate": rate,
        })

    try:
        se = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "set_posting_time": 1,
            "posting_date": posting_date,
            "company": company,
            "remarks": f"Quarterly restock Q{quarter}/{year}",
            "items": se_items,
        })
        se.flags.ignore_permissions = True
        se.flags.ignore_mandatory = True
        se.insert()
        se.submit()
        return se.name
    except Exception as e:
        frappe.db.rollback()
        print(f"    ⚠️  Quarterly restock error Q{quarter}/{year}: {str(e)[:80]}")
        return None


# =============================================================================
# STOCK TRANSFERS
# =============================================================================

def generate_stock_transfers(years=None):
    """
    Create quarterly stock transfers:
    - Kho Chính HCM → Kho Showroom Hà Nội (from 2025, HN showroom opens)
    - Kho Chính HCM → Kho Fitting (fitting equipment)
    """
    if years is None:
        years = [2023, 2024, 2025, 2026]

    print("\n[Stock] Generating Stock Transfers...")

    company = _get_company()
    abbr = _get_abbr(company)
    src_warehouse = f"Kho Chính HCM - {abbr}"
    hn_warehouse = f"Kho Showroom Hà Nội - {abbr}"
    fitting_warehouse = f"Kho Fitting - {abbr}"

    if not frappe.db.exists("Warehouse", src_warehouse):
        print(f"  ⚠️  Source warehouse '{src_warehouse}' not found.")
        return []

    items = frappe.get_all("Item",
        filters={"is_stock_item": 1, "disabled": 0},
        fields=["item_code", "item_name"]
    )

    created = []
    today = getdate(nowdate())

    for year in years:
        quarters = [1, 2, 3, 4] if year < 2026 else [1]

        for quarter in quarters:
            q_dates = {1: f"{year}-03-20", 2: f"{year}-06-20", 3: f"{year}-09-20", 4: f"{year}-12-20"}
            transfer_date = min(getdate(q_dates[quarter]), today)

            # Transfer to HN showroom (from 2023, small amount; from 2025, larger)
            if frappe.db.exists("Warehouse", hn_warehouse):
                hn_qty_range = (5, 20) if year < 2025 else (15, 40)
                # Pick 15-30 items to transfer
                selected_items = sample(items, min(25, len(items)))
                hn_items = []
                for item in selected_items:
                    qty = randint(*hn_qty_range)
                    # Check available stock first
                    available = _get_actual_qty(item.item_code, src_warehouse)
                    if available >= qty:
                        hn_items.append({
                            "item_code": item.item_code,
                            "qty": qty,
                            "s_warehouse": src_warehouse,
                            "t_warehouse": hn_warehouse,
                        })

                if hn_items:
                    try:
                        se = frappe.get_doc({
                            "doctype": "Stock Entry",
                            "stock_entry_type": "Material Transfer",
                            "set_posting_time": 1,
                            "posting_date": transfer_date,
                            "company": company,
                            "remarks": f"Điều chuyển HCM → Hà Nội Q{quarter}/{year}",
                            "items": hn_items,
                        })
                        se.flags.ignore_permissions = True
                        se.flags.ignore_mandatory = True
                        se.insert()
                        se.submit()
                        created.append(se.name)
                        frappe.db.commit()
                    except Exception as e:
                        frappe.db.rollback()
                        print(f"    ⚠️  Transfer error Q{quarter}/{year} HCM→HN: {str(e)[:80]}")

            # Transfer to Fitting warehouse each quarter
            if frappe.db.exists("Warehouse", fitting_warehouse):
                fitting_items_selected = sample(items, min(10, len(items)))
                fitting_items = []
                for item in fitting_items_selected:
                    qty = randint(2, 8)
                    available = _get_actual_qty(item.item_code, src_warehouse)
                    if available >= qty:
                        fitting_items.append({
                            "item_code": item.item_code,
                            "qty": qty,
                            "s_warehouse": src_warehouse,
                            "t_warehouse": fitting_warehouse,
                        })

                if fitting_items:
                    try:
                        se = frappe.get_doc({
                            "doctype": "Stock Entry",
                            "stock_entry_type": "Material Transfer",
                            "set_posting_time": 1,
                            "posting_date": transfer_date,
                            "company": company,
                            "remarks": f"Điều chuyển vào Kho Fitting Q{quarter}/{year}",
                            "items": fitting_items,
                        })
                        se.flags.ignore_permissions = True
                        se.flags.ignore_mandatory = True
                        se.insert()
                        se.submit()
                        created.append(se.name)
                        frappe.db.commit()
                    except Exception as e:
                        frappe.db.rollback()

    print(f"  Created {len(created)} stock transfer entries")
    return created


# =============================================================================
# MAIN
# =============================================================================

def setup_all_stock(years=None):
    """Run opening stock + transfers. Call before sales cycle."""
    if years is None:
        years = [2023, 2024, 2025, 2026]

    print("\n" + "=" * 60)
    print("DCNET Stock Setup")
    print("=" * 60)

    # 1. Opening stock on 2023-01-01
    opening = generate_opening_stock("2023-01-01")
    frappe.db.commit()

    # 2. Quarterly restocks (to top up in each quarter)
    print("\n[Stock] Generating quarterly restocks...")
    restock_count = 0
    for year in years:
        quarters = [1, 2, 3, 4] if year < 2026 else [1]
        for quarter in quarters:
            name = generate_quarterly_restock(year, quarter)
            if name:
                restock_count += 1
                frappe.db.commit()
    print(f"  Created {restock_count} quarterly restock entries")

    # 3. Transfers to other warehouses
    transfers = generate_stock_transfers(years)
    frappe.db.commit()

    print(f"\n✅ Stock setup complete!")
    print(f"  Opening entries: {len(opening)}")
    print(f"  Restocks: {restock_count}")
    print(f"  Transfers: {len(transfers)}")
    return {
        "opening": opening,
        "restocks": restock_count,
        "transfers": transfers,
    }
