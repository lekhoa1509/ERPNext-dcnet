"""
Tạo nhanh N đơn hàng bán ngẫu nhiên từ dữ liệu khách hàng + vật tư hiện có.

Gọi:
  bench --site flow.local execute 'dcnet_apps.dcnet_apps.quick_so.run'
  bench --site flow.local execute 'dcnet_apps.dcnet_apps.quick_so.run' --kwargs '{"count": 20}'
"""

import frappe
from frappe.utils import getdate, add_days, nowdate, flt
from random import choice, randint, sample, uniform, random as rnd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_company():
    return (
        frappe.db.get_single_value("Global Defaults", "default_company")
        or frappe.db.get_value("Company", {}, "name")
    )


def _get_abbr(company):
    return frappe.db.get_value("Company", company, "abbr")


def _get_warehouses(company, abbr):
    """Lấy các kho thực sự có tồn kho, ưu tiên kho chính."""
    rows = frappe.db.sql(
        """
        SELECT b.warehouse
        FROM `tabBin` b
        JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE b.actual_qty > 0
          AND w.company = %s
          AND w.is_group = 0
        GROUP BY b.warehouse
        ORDER BY SUM(b.actual_qty) DESC
        LIMIT 5
        """,
        company,
        as_dict=True,
    )
    return [r.warehouse for r in rows] if rows else []


def _get_tax_template(abbr):
    candidates = [f"VAT 10% Bán Hàng - {abbr}", f"Vietnam Tax - {abbr}"]
    for t in candidates:
        if frappe.db.exists("Sales Taxes and Charges Template", t):
            return t
    return frappe.db.get_value(
        "Sales Taxes and Charges Template", {"company": ["!=", ""]}, "name"
    )


def _available_qty(item_code, warehouse):
    return flt(
        frappe.db.get_value(
            "Bin", {"item_code": item_code, "warehouse": warehouse}, "actual_qty"
        )
        or 0
    )


def _find_warehouse(item_code, qty, warehouses):
    for wh in warehouses:
        if _available_qty(item_code, wh) >= qty:
            return wh
    return None


def _build_items(items, warehouses, is_b2b, avg_val):
    num = randint(2, min(6, len(items))) if is_b2b else randint(1, min(3, len(items)))
    candidates = sample(items, min(num * 3, len(items)))
    so_items = []
    used = set()
    for item in candidates:
        if len(so_items) >= num:
            break
        if item["item_code"] in used:
            continue
        qty = randint(2, 8) if is_b2b else randint(1, 3)
        wh = _find_warehouse(item["item_code"], qty, warehouses)
        if wh is None:
            wh = _find_warehouse(item["item_code"], 1, warehouses)
            qty = 1
        if wh is None:
            continue
        rate = max(100_000, int(avg_val / num * uniform(0.8, 1.4)))
        so_items.append(
            {"item_code": item["item_code"], "qty": qty, "rate": rate, "warehouse": wh}
        )
        used.add(item["item_code"])
    return so_items


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(count=20):
    company = _get_company()
    abbr = _get_abbr(company)
    warehouses = _get_warehouses(company, abbr)
    tax_template = _get_tax_template(abbr)

    customers = frappe.get_all("Customer", pluck="name")
    items = frappe.get_all(
        "Item",
        filters={"is_sales_item": 1, "disabled": 0},
        fields=["item_code", "item_name"],
    )

    print(f"\nCompany   : {company} ({abbr})")
    print(f"Warehouses: {warehouses}")
    print(f"Tax       : {tax_template}")
    print(f"Customers : {len(customers)}, Items: {len(items)}")
    print(f"Bins có tồn kho: {frappe.db.count('Bin', {'actual_qty': ['>', 0]})}")
    print(f"\nĐang tạo {count} Đơn hàng bán...\n")

    today = getdate(nowdate())
    avg_val = 5_000_000  # ~5 triệu VND mỗi SO

    created = []
    skipped = 0
    attempts = 0

    while len(created) < count and attempts < count * 4:
        attempts += 1
        so_date = add_days(today, -randint(1, 60))
        delivery_date = min(add_days(so_date, randint(3, 14)), today)
        customer = choice(customers)
        is_b2b = frappe.db.get_value("Customer", customer, "customer_type") == "Company"
        avg = avg_val * (uniform(1.8, 3.0) if is_b2b else uniform(0.6, 1.4))

        so_items = _build_items(items, warehouses, is_b2b, avg)
        if not so_items:
            skipped += 1
            continue

        for it in so_items:
            it["delivery_date"] = delivery_date

        try:
            so = frappe.get_doc(
                {
                    "doctype": "Sales Order",
                    "customer": customer,
                    "transaction_date": so_date,
                    "delivery_date": delivery_date,
                    "company": company,
                    "items": so_items,
                    "taxes_and_charges": tax_template,
                }
            )
            so.flags.ignore_permissions = True
            so.flags.ignore_mandatory = True
            so.insert()
            so.submit()
            frappe.db.commit()

            created.append(so.name)
            print(
                f"  [{len(created):2d}] {so.name}"
                f"  |  {customer[:28]}"
                f"  |  {so_date}"
                f"  |  {len(so.items)} SP"
                f"  |  {so.grand_total:,.0f} VND"
            )

        except Exception as e:
            skipped += 1
            frappe.db.rollback()
            print(f"       SKIP attempt {attempts}: {str(e)[:100]}")

    print(f"\n✅ Xong: {len(created)}/{count} SO đã tạo, {skipped} bỏ qua.")
    return created
