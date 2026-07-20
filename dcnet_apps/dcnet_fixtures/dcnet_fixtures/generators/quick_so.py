"""
Tạo nhanh 20 đơn hàng bán ngẫu nhiên từ dữ liệu hiện có.
Gọi: bench --site flow.local execute 'dcnet_fixtures.dcnet_fixtures.generators.quick_so.run'
"""

import frappe
from frappe.utils import getdate, add_days, nowdate
from random import choice, randint

from dcnet_fixtures.dcnet_fixtures.generators.sales_cycle import (
    generate_sales_order,
    _get_company,
    _get_abbr,
    _get_stock_warehouses,
    _get_sales_tax_template,
)


def run(count=20):
    company = _get_company()
    abbr = _get_abbr(company)
    warehouses = _get_stock_warehouses(company, abbr)
    tax_template = _get_sales_tax_template(abbr)

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
    print(f"\nCreating {count} Sales Orders...\n")

    today = getdate(nowdate())
    created = []
    skipped = 0
    attempts = 0

    while len(created) < count and attempts < count * 3:
        attempts += 1
        so_date = add_days(today, -randint(1, 60))
        delivery_date = min(add_days(so_date, randint(3, 14)), today)
        customer = choice(customers)

        try:
            so = generate_sales_order(
                customer=customer,
                items=items,
                transaction_date=so_date,
                delivery_date=delivery_date,
                warehouses=warehouses,
                tax_template=tax_template,
                company=company,
            )
            frappe.db.commit()
            created.append(so.name)
            print(
                f"  [{len(created):2d}] {so.name}"
                f"  |  KH: {customer[:30]}"
                f"  |  Ngày: {so_date}"
                f"  |  {len(so.items)} SP"
                f"  |  {so.grand_total:,.0f} VND"
            )

        except ValueError:
            skipped += 1
            frappe.db.rollback()
        except Exception as e:
            skipped += 1
            print(f"       SKIP attempt {attempts}: {str(e)[:120]}")
            frappe.db.rollback()

    print(f"\n✅ Xong: {len(created)}/{count} SO đã tạo, {skipped} bỏ qua (thiếu tồn kho).")
    return created
