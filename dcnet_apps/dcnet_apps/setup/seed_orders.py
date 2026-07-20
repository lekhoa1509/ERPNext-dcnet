import datetime
import random
import frappe


def run():
    # ── Fetch real master data ─────────────────────────────────────
    customers = frappe.get_list(
        "Customer",
        fields=["name", "customer_name"],
        filters=[["disabled", "=", 0]],
        limit=30,
    )
    if not customers:
        print("ERROR: No customers found. Run dcnet-fixtures generate --module customers first.")
        return

    items = frappe.get_list(
        "Item",
        fields=["name", "item_name", "stock_uom"],
        filters=[["disabled", "=", 0]],
        limit=50,
    )
    if not items:
        print("ERROR: No items found. Run dcnet-fixtures generate --module master first.")
        return

    # Ensure items are marked as sales items (required by SO validation)
    item_names = [i.name for i in items]
    frappe.db.set_value(
        "Item", {"name": ["in", item_names], "is_sales_item": 0},
        "is_sales_item", 1,
    )
    frappe.db.commit()
    print(f"  [setup] Enabled is_sales_item on up to {len(item_names)} items")

    company = frappe.defaults.get_global_default("company")
    if not company:
        co_list = frappe.get_list("Company", limit=1)
        company = co_list[0].name if co_list else None
    if not company:
        print("ERROR: No company configured.")
        return

    price_list = (
        frappe.db.get_value("Price List", {"selling": 1, "enabled": 1}, "name")
        or "Standard Selling"
    )

    # ── Seed data pools ────────────────────────────────────────────
    revenue_statuses = ["Bản nhập", "Bản nhập", "Bản nhập", "Đã ghi", "Đã ghi", "Hủy"]
    exec_statuses = ["Chưa thực hiện", "Đang thực hiện", "Hoàn thành"]
    titles = [
        "Cung cấp dịch vụ Internet Leased Line",
        "Hợp đồng kết nối MPLS VPN",
        "Dịch vụ Cloud Server và lưu trữ",
        "Cung cấp thiết bị mạng và cài đặt",
        "Dịch vụ bảo trì hệ thống mạng",
        "Kết nối Fiber quang nội địa",
        "Hợp đồng cung cấp IP Transit",
        "Dịch vụ Colocation tại IDC",
        "Tư vấn và triển khai hạ tầng IT",
        "Cung cấp giải pháp bảo mật mạng",
    ]

    today = datetime.date.today()
    created = []

    for i in range(10):
        customer = random.choice(customers)
        picked_items = random.sample(items, random.randint(1, min(3, len(items))))

        # Contract duration: 12, 24, or 36 months
        duration = random.choice([12, 24, 36])
        # Random date in past 6 months
        days_ago = random.randint(7, 180)
        order_date = today - datetime.timedelta(days=days_ago)
        order_date_str = order_date.strftime("%Y-%m-%d")
        delivery_date_str = (order_date + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        expiry_str = (order_date + datetime.timedelta(days=duration * 30)).strftime("%Y-%m-%d")
        rev_date_str = (order_date + datetime.timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")

        # Build items — rate in VND (5M–200M range for services)
        so_items = []
        for item in picked_items:
            rate = random.choice([5, 8, 10, 15, 20, 30, 50, 80, 100, 150, 200]) * 1_000_000
            so_items.append({
                "item_code": item.name,
                "item_name": item.item_name,
                "qty": duration,
                "uom": item.stock_uom or "Tháng",
                "rate": rate,
            })

        rev_status = random.choice(revenue_statuses)
        exec_status = random.choice(exec_statuses)
        title = titles[i]

        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": customer.name,
            "title": title,
            "transaction_date": order_date_str,
            "delivery_date": delivery_date_str,
            "selling_price_list": price_list,
            "company": company,
            "currency": "VND",
            "conversion_rate": 1,
            "items": so_items,
            "custom_contract_duration": duration,
            "custom_contract_expiry": expiry_str,
            "custom_revenue_status": rev_status,
            "custom_revenue_recognition_date": rev_date_str,
            "custom_execution_status": exec_status,
        })
        so.flags.ignore_permissions = True
        so.flags.ignore_mandatory = True
        so.insert()

        # Submit a few so we get variety in delivery_status
        if rev_status == "Đã ghi" and random.random() < 0.7:
            so.submit()

        created.append(so.name)
        total = sum(i["qty"] * i["rate"] for i in so_items)
        print(f"  {so.name}  |  {customer.customer_name[:30]:<30}  |  {rev_status:<14}  |  {total:>15,.0f} VND")

    frappe.db.commit()
    print(f"\n✓ Đã tạo {len(created)} đơn hàng: {', '.join(created)}")
