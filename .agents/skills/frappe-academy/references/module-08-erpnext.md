# Module 8: ERPNext Development

> **Mục tiêu / Objective:** Hiểu kiến trúc ERPNext và xây dựng custom app mở rộng ERPNext.
> **Yêu cầu / Prerequisites:** Module 1-7 (Frappe Framework hoàn chỉnh)
> **Thời lượng / Duration:** ~12 giờ thực hành

---

## L8.1: ERPNext Architecture

### Tổng quan / Overview

ERPNext là ứng dụng quản lý doanh nghiệp toàn diện xây dựng trên Frappe Framework. Hiểu kiến trúc — các Core DocTypes, naming conventions, module structure, và cach ERPNext mở rộng Frappe — là nền tảng để custom và phát triển tính năng mới. ERPNext không phải monolith mà là tập hợp các modules liên kết chặt chẽ qua Links và Controllers.

### Khái niệm chính / Key Concepts

#### 1. Core DocTypes — Xuong song của ERPNext

```
ERPNext co ~700+ DocTypes, nhung chi co ~20 DocTypes cot loi:

=== Master Data (du lieu goc — tao truoc) ===
Company          — Cong ty (multi-company support)
Item             — San pham/Dich vu (core cua moi giao dich)
Customer         — Khach hang (Selling module)
Supplier         — Nha cung cap (Buying module)
Warehouse        — Kho hang (Stock module)
Account          — Tai khoan ke toan (Accounting module)
Cost Center      — Trung tam chi phi
Employee         — Nhan vien (HR module)

=== Transaction DocTypes (giao dich — su dung hang ngay) ===
Sales Order (SO)      — Don dat hang ban
Purchase Order (PO)   — Don dat hang mua
Sales Invoice (SI)    — Hoa don ban hang (tao GL Entry)
Purchase Invoice (PI) — Hoa don mua hang (tao GL Entry)
Delivery Note (DN)    — Phieu giao hang (tao Stock Ledger)
Purchase Receipt (PR) — Phieu nhap kho (tao Stock Ledger)
Stock Entry (SE)      — Xuat/Nhap/Chuyen kho
Payment Entry (PE)    — Phieu thu/chi
Journal Entry (JE)    — But toan tong hop

=== Linking DocTypes (ket noi cac giao dich) ===
GL Entry         — But toan ke toan (tu dong tao tu SI, PI, PE, JE)
Stock Ledger Entry — Nhap xuat kho (tu dong tao tu DN, PR, SE)
```

#### 2. Luong giao dịch chính / Main Transaction Flows

```
=== Luong Ban hang (Selling) ===
Lead → Opportunity → Quotation → Sales Order → Delivery Note → Sales Invoice → Payment Entry
                                      ↓
                                 Material Request → Purchase Order → Purchase Receipt → Purchase Invoice

=== Luong Mua hang (Buying) ===
Material Request → Supplier Quotation → Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry

=== Luong Kho (Stock) ===
Purchase Receipt (nhap) → Stock Entry (chuyen/sx) → Delivery Note (xuat)
     ↓                         ↓                          ↓
Stock Ledger Entry        Stock Ledger Entry        Stock Ledger Entry
     ↓                         ↓                          ↓
GL Entry (perpetual)      GL Entry                   GL Entry

=== Luong Ke toan (Accounting) ===
Sales Invoice → GL Entry → Trial Balance → P&L + Balance Sheet
Purchase Invoice → GL Entry ↗
Payment Entry → GL Entry ↗
Journal Entry → GL Entry ↗
```

#### 3. Naming Conventions

```python
# ERPNext su dùng naming series cho transactions:
# Sales Order:       SO-0001, SO-0002, ...
# Purchase Order:    PO-0001, PO-0002, ...
# Sales Invoice:     SINV-0001, ACC-SINV-0001 (có thể thêm prefix công ty)
# Delivery Note:     DN-0001
# Stock Entry:       STE-0001

# Master data thường dùng ten trực tiếp:
# Item:              "Widget A", "Laptop Dell XPS 15"
# Customer:          "CUST-0001" hoac "Nguyen Van A"
# Warehouse:         "Stores - TM", "Finished Goods - TM" (với company abbr)
# Account:           "1111 - Tien mất VND - TM" (so TK + ten + company abbr)

# Company Abbreviation — Quan trọng!
# Mỗi company có abbreviation (VD: "TM" cho Thang Long TM)
# Warehouses và Accounts deu ket thuc bang " - TM"
# Giup phân biệt data giua các company trong multi-company setup
```

#### 4. Module Structure trong ERPNext

```
erpnext/
  erpnext/
    accounts/           # Ke toan
    assets/             # Tai san co dinh
    buying/             # Mua hang
    crm/                # Quan ly khach hang tiem nang
    hr/                 # Nhan su (da tach thanh app rieng: hrms)
    manufacturing/      # San xuat
    projects/           # Du an
    selling/            # Ban hang
    setup/              # Thiet lap ban dau
    stock/              # Kho hang
    controllers/        # Shared controllers (accounts_controller, stock_controller, ...)
    patches/            # Database patches (migration)
    templates/          # Web templates
    utilities/          # Shared utility functions
```

```python
# Cach ERPNext mở rộng Frappe:

# 1. Ke thua Controller
# ERPNext DocTypes kế thừa từ các base controllers:
from erpnext.controllers.accounts_controller import AccountsController

class SalesInvoice(AccountsController):
    # AccountsController kế thừa từ Document
    # Cung cap: validate_party, validate_currency, make_gl_entries, etc.
    pass

# 2. Hooks — ERPNext dang ky nhiều hooks vao Frappe
# VD: Sau khi submit Sales Invoice → tự động tạo GL Entry + Stock Ledger

# 3. Fixtures — ERPNext cũng cap Country-specific setup
# VD: Chart of Accounts template cho Viết Nam (TT200)
```

#### 5. ERPNext Settings quan trọng

```python
# Các DocType settings can biết:

# Stock Settings — Anh huong cach tính gia von
frappe.get_single("Stock Settings")
# .valuation_method = "FIFO" / "Moving Average"
# .auto_insert_price_list_rate_if_missing = 1
# .allow_negative_stock = 0

# Accounts Settings — Anh huong kế toán
frappe.get_single("Accounts Settings")
# .acc_frozen_upto = "2026-01-01"  # Dong số kế toán trước ngày này

# Selling Settings
frappe.get_single("Selling Settings")
# .selling_price_list = "Standard Selling"

# Buying Settings
frappe.get_single("Buying Settings")
# .buying_price_list = "Standard Buying"
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao Warehouse và Account trong ERPNext có company abbreviation (VD: "- TM") ở cuoi ten?</summary>

**Trả lời:** ERPNext hỗ trợ multi-company — nhiều công ty trên 1 site. Abbreviation đảm bảo Warehouse "Stores - TM" của công ty Thang Long TM khác với "Stores - NM" của Nhất Minh Sport. Mỗi giao dịch của company chi thay warehouses/accounts của company do.
</details>

<details>
<summary><strong>Câu 2:</strong> Khi submit Sales Invoice, nhưng gì xảy ra tự động?</summary>

**Trả lời:** (1) GL Entries được tạo: No 131 (Debtors/Cong nó phải thu), Có 5111 (Doanh thu), Có 33311 (VAT đầu ra). (2) Nếu có items linked to warehouse: Stock Ledger Entries tạo để xuất kho + GL cho gia von (No 632, Có 1561). (3) Outstanding amount của Customer được cập nhật. (4) Stock quantity giảm tuong ung.
</details>

**DEEP DIVE:** Xem skill `erpnext` → references/ để hiểu tung module ERPNext chi tiết.

**DEEP DIVE:** Xem skill `erpnext` → references/accounting/ cho kế toán patterns.

---

## L8.2: Custom App trên ERPNext

### Tổng quan / Overview

Custom app trong ERPNext là cach mở rộng chuc nang mà không sửa code ERPNext goc. Ban có thể tạo DocType mới, extend DocType có sẵn, override logic, và thêm fixtures — tất cả trong 1 app riêng để update ERPNext không mất customization. Đây là best practice để phát triển trên ERPNext.

### Khái niệm chính / Key Concepts

#### 1. Tạo Custom App

```bash
# Tạo app mới
cd /workspace/development/frappe-bench
bench new-app dcnet_apps
# → Nhập ten, description, etc.

# Cai đặt app vao site
bench --site flow.local install-app dcnet_apps

# Cấu trúc app
dcnet_apps/
  dcnet_apps/
    __init__.py
    hooks.py            # ⭐ Cau hinh app
    modules.txt         # Danh sach modules
    patches.txt         # Database patches
    dcnet_apps/         # Module mac dinh
      __init__.py
```

#### 2. hooks.py — Diem kết nối với ERPNext

```python
# hooks.py — Các hooks quan trọng cho custom app trên ERPNext

app_name = "dcnet_apps"
app_title = "DCNET Apps"
app_publisher = "DCNET"
app_description = "Custom modules for DCNET Flow"

# === Dependency ===
required_apps = ["frappe", "erpnext"]  # App nay can ERPNext

# === Override DocType Controller ===
override_doctype_class = {
    "Sales Order": "dcnet_apps.overrides.sales_order.CustomSalesOrder",
    "Sales Invoice": "dcnet_apps.overrides.sales_invoice.CustomSalesInvoice",
}

# === Document Events — Hook vao lifecycle của DocType bất kỳ ===
doc_events = {
    "Sales Order": {
        "validate": "dcnet_apps.events.sales_order.validate",
        "on_submit": "dcnet_apps.events.sales_order.on_submit",
        "before_cancel": "dcnet_apps.events.sales_order.before_cancel",
    },
    "Sales Invoice": {
        "on_submit": "dcnet_apps.events.sales_invoice.on_submit",
    },
    # Wildcards — Ap dùng cho TẤT CẢ DocTypes
    "*": {
        "on_update": "dcnet_apps.events.common.log_update",
    }
}

# === Fixtures — Tự động export/import ===
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["dt", "in", [
            "Sales Order", "Sales Invoice", "Customer", "Item"
        ]]]
    },
    {
        "dt": "Property Setter",
        "filters": [["doc_type", "in", [
            "Sales Order", "Sales Invoice"
        ]]]
    },
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
]

# === Scheduled Tasks ===
scheduler_events = {
    "daily": [
        "dcnet_apps.tasks.daily.process_daily_reports"
    ],
    "hourly": [
        "dcnet_apps.tasks.hourly.check_overdue_orders"
    ]
}

# === Jinja ===
jinja = {
    "methods": [
        "dcnet_apps.utils.jinja_methods.get_customer_loyalty_points",
    ]
}

# === Website ===
website_route_rules = [
    {"from_route": "/catalog/<path:app_path>", "to_route": "catalog"},
]
```

#### 3. Override DocType Class

```python
# dcnet_apps/overrides/sales_order.py
import frappe
from frappe import _
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder


class CustomSalesOrder(SalesOrder):
    """Mo rong Sales Order voi logic DCNET."""

    def validate(self):
        # Gọi validate goc của ERPNext trước
        super().validate()

        # Thêm logic custom
        self.validate_dcnet_rules()
        self.calculate_custom_totals()

    def validate_dcnet_rules(self):
        """Kiem tra quy tac kinh doanh DCNET."""
        # VD: Don hang tối thiểu 500,000 VND
        if self.grand_total < 500000:
            frappe.throw(_("Minimum order value is 500,000 VND"))

        # VD: Kiểm tra customer credit limit
        if self.customer:
            credit_limit = frappe.db.get_value("Customer", self.customer, "credit_limit")
            if credit_limit and self.grand_total > credit_limit:
                frappe.throw(_(
                    "Order exceeds customer credit limit of {0}"
                ).format(frappe.format_value(credit_limit, {"fieldtype": "Currency"})))

    def calculate_custom_totals(self):
        """Tinh cac truong custom."""
        for item in self.items:
            if hasattr(item, "custom_discount_amount"):
                item.custom_net_amount = item.amount - (item.custom_discount_amount or 0)

    def on_submit(self):
        """Logic khi submit don hang."""
        super().on_submit()
        # Gửi notification
        self.notify_warehouse()

    def notify_warehouse(self):
        """Gui thong bao cho kho chuan bi hang."""
        warehouse_manager = frappe.db.get_value(
            "Warehouse", self.set_warehouse, "custom_manager"
        )
        if warehouse_manager:
            frappe.sendmail(
                recipients=[warehouse_manager],
                subject=f"New Sales Order: {self.name}",
                message=f"Please prepare items for {self.name}"
            )
```

#### 4. Document Events (không cần override class)

```python
# dcnet_apps/events/sales_order.py
import frappe
from frappe import _


def validate(doc, method):
    """Hook vao validate cua Sales Order.

    Args:
        doc: Document object (Sales Order instance)
        method: Ten method ("validate")

    Khac voi override_doctype_class:
    - Khong can ke thua class
    - Chay SAU validate goc cua ERPNext
    - De dung hon, nhung it control hon
    """
    # Kiểm tra custom field
    if doc.custom_sales_channel == "Online":
        if not doc.custom_delivery_address:
            frappe.throw(_("Delivery address is required for online orders"))

    # Tự động fill custom fields
    if doc.customer:
        doc.custom_customer_segment = frappe.db.get_value(
            "Customer", doc.customer, "custom_segment"
        )


def on_submit(doc, method):
    """Khi submit Sales Order."""
    # Tạo record tracking
    frappe.get_doc({
        "doctype": "DCNET Order Tracking",
        "sales_order": doc.name,
        "status": "Confirmed",
        "timestamp": frappe.utils.now()
    }).insert(ignore_permissions=True)


def before_cancel(doc, method):
    """Truoc khi cancel Sales Order."""
    # Kiểm tra điều kiện custom trước khi cho cancel
    tracking = frappe.db.get_value("DCNET Order Tracking",
        {"sales_order": doc.name}, "status"
    )
    if tracking == "Shipped":
        frappe.throw(_("Cannot cancel order that has been shipped"))
```

#### 5. Extending vs Creating DocTypes

```
+----------------------+--------------------------------+--------------------------------+
| Approach             | Khi nao dung                   | Vi du                          |
+----------------------+--------------------------------+--------------------------------+
| Custom Fields        | Them field vao DocType co san   | custom_channel tren Sales Order|
| (extend)             | Data lien ket chat voi DocType  |                                |
+----------------------+--------------------------------+--------------------------------+
| override_doctype_    | Can thay doi logic goc          | Custom validate, on_submit     |
| class (extend)       | cua DocType co san              | cho Sales Order                |
+----------------------+--------------------------------+--------------------------------+
| doc_events           | Hook vao events ma khong        | Log, notification, tao record  |
| (extend)             | can thay doi logic goc          | phu sau khi submit             |
+----------------------+--------------------------------+--------------------------------+
| New DocType          | Chuc nang moi hoan toan         | DCNET Fitting, DCNET Trade-In  |
| (create)             | ERPNext khong co                |                                |
+----------------------+--------------------------------+--------------------------------+
| Child Table          | Them child vao DocType co san   | Custom items table trong SO    |
| (extend/create)      | hoac tao child table moi        |                                |
+----------------------+--------------------------------+--------------------------------+
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Su khác biết giua <code>override_doctype_class</code> và <code>doc_events</code> trong hooks.py?</summary>

**Trả lời:** `override_doctype_class` THAY THE class goc — bạn kế thừa và có thể override BAT KY method nao, gọi super() để giu logic goc. `doc_events` HOOK vao events — function bạn viết sẽ chạy SAU method goc. Override class mạnh hơn (có thể thay đổi logic trước/trong/sau), doc_events đơn giản hơn (chi thêm logic sau).
</details>

<details>
<summary><strong>Câu 2:</strong> Tại sao nên dùng Custom App thay vì sửa trực tiếp ERPNext code?</summary>

**Trả lời:** (1) Update ERPNext không mất customization (custom app độc lập). (2) Version control riêng — để track changes. (3) Tại su dùng — 1 custom app cho nhiều sites. (4) Clean separation — biết rõ đầu là ERPNext goc, đầu là custom. (5) Rollback để — tat app là quay về ERPNext goc.
</details>

**DEEP DIVE:** Xem skill `erpnext` → references/ext_syntax-customapp/ cho custom app patterns.

**DEEP DIVE:** Xem skill `dcnet_quality` → syntax/erpnext-syntax-hooks/ cho hooks.py best practices.

---

## L8.3: Custom Fields & Property Setter

### Tổng quan / Overview

Custom Fields thêm truong mọi vao DocType có sẵn mà không cần sửa code goc. Property Setter thay đổi properties của fields có sẵn (VD: đổi label, ẩn field, thay đổi options). Ca hai có thể tạo qua UI hoặc qua fixtures (JSON) để deploy tự động. Đây là công cụ chính để customize ERPNext mà không cần tạo DocType mới.

### Khái niệm chính / Key Concepts

#### 1. Custom Fields qua UI

```
Duong dan: Setup → Customize → Custom Field
Hoac: Customize Form → chon DocType → Add Row

Cac thong tin can nhap:
- Document Type: DocType muon them field (VD: "Sales Order")
- Label: Ten hien thi (VD: "Sales Channel")
- Fieldname: Tu dong tao tu label, bat dau bang "custom_" (VD: "custom_sales_channel")
- Fieldtype: Data, Link, Select, Currency, Check, etc.
- Insert After: Dat sau field nao
- Options: Cho Select (danh sach options) hoac Link (DocType reference)
```

#### 2. Custom Fields qua Fixtures (JSON)

```json
// dcnet_apps/dcnet_apps/fixtures/custom_field.json
[
    {
        "doctype": "Custom Field",
        "dt": "Sales Order",
        "fieldname": "custom_sales_channel",
        "label": "Sales Channel",
        "fieldtype": "Select",
        "options": "\nOnline\nIn-Store\nPhone\nPartner",
        "insert_after": "customer_name",
        "reqd": 0,
        "in_list_view": 1,
        "in_standard_filter": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Sales Order",
        "fieldname": "custom_delivery_address",
        "label": "Delivery Address",
        "fieldtype": "Small Text",
        "insert_after": "custom_sales_channel",
        "depends_on": "eval:doc.custom_sales_channel=='Online'",
        "mandatory_depends_on": "eval:doc.custom_sales_channel=='Online'"
    },
    {
        "doctype": "Custom Field",
        "dt": "Sales Order",
        "fieldname": "custom_section_dcnet",
        "label": "DCNET Info",
        "fieldtype": "Section Break",
        "insert_after": "terms",
        "collapsible": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Sales Order",
        "fieldname": "custom_internal_notes",
        "label": "Internal Notes",
        "fieldtype": "Text Editor",
        "insert_after": "custom_section_dcnet",
        "permlevel": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_segment",
        "label": "Customer Segment",
        "fieldtype": "Select",
        "options": "\nRegular\nVIP\nWholesale\nPartner",
        "insert_after": "customer_group"
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_loyalty_points",
        "label": "Loyalty Points",
        "fieldtype": "Int",
        "insert_after": "custom_segment",
        "read_only": 1,
        "bold": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Item",
        "fieldname": "custom_brand_origin",
        "label": "Brand Origin",
        "fieldtype": "Data",
        "insert_after": "brand"
    }
]
```

```python
# hooks.py — Dang ky fixtures
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["dt", "in", ["Sales Order", "Customer", "Item"]]]
    }
]
```

#### 3. Property Setter

```json
// dcnet_apps/dcnet_apps/fixtures/property_setter.json
[
    {
        "doctype": "Property Setter",
        "doc_type": "Sales Order",
        "field_name": "naming_series",
        "property": "options",
        "value": "SO-.YYYY.-\nDCNET-SO-.YYYY.-",
        "property_type": "Text"
    },
    {
        "doctype": "Property Setter",
        "doc_type": "Sales Order",
        "field_name": "customer_name",
        "property": "in_list_view",
        "value": "1",
        "property_type": "Check"
    },
    {
        "doctype": "Property Setter",
        "doc_type": "Sales Order",
        "field_name": "territory",
        "property": "hidden",
        "value": "1",
        "property_type": "Check"
    },
    {
        "doctype": "Property Setter",
        "doc_type": "Sales Invoice",
        "field_name": "payment_terms_template",
        "property": "default",
        "value": "Net 30",
        "property_type": "Text"
    }
]
```

#### 4. Thêm Custom Fields bang Code

```python
# Cach 1: frappe.custom — Tạo qua code (thường dùng trong patches)
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Sales Order": [
        {
            "fieldname": "custom_sales_channel",
            "label": "Sales Channel",
            "fieldtype": "Select",
            "options": "\nOnline\nIn-Store\nPhone",
            "insert_after": "customer_name"
        }
    ],
    "Customer": [
        {
            "fieldname": "custom_segment",
            "label": "Customer Segment",
            "fieldtype": "Select",
            "options": "\nRegular\nVIP\nWholesale",
            "insert_after": "customer_group"
        }
    ]
}

create_custom_fields(custom_fields, update=True)

# Cach 2: Truc tiep
if not frappe.db.exists("Custom Field", {"dt": "Sales Order", "fieldname": "custom_sales_channel"}):
    frappe.get_doc({
        "doctype": "Custom Field",
        "dt": "Sales Order",
        "fieldname": "custom_sales_channel",
        "label": "Sales Channel",
        "fieldtype": "Select",
        "options": "\nOnline\nIn-Store",
        "insert_after": "customer_name"
    }).insert()
```

#### 5. Quy tac quan trọng / Important Rules

```
1. Ten custom field PHAI bat dau bang "custom_"
   ✅ custom_sales_channel
   ❌ sales_channel (se conflict voi ERPNext updates)

2. Custom field KHONG duoc trung ten voi field co san
   Kiem tra truoc: frappe.get_meta("Sales Order").has_field("fieldname")

3. Dung "depends_on" de an/hien fields theo dieu kien
   depends_on: "eval:doc.custom_sales_channel=='Online'"

4. Dung "mandatory_depends_on" thay vi "reqd" cho conditional mandatory
   mandatory_depends_on: "eval:doc.custom_sales_channel=='Online'"

5. Custom fields tu Child Table:
   dt = "Sales Order Item" (KHONG phai "Sales Order")
   insert_after = field name trong child table

6. Export fixtures sau khi tao qua UI:
   bench --site flow.local export-fixtures --app dcnet_apps
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao custom field name PHẢI bắt đầu bang <code>custom_</code>?</summary>

**Trả lời:** Để tránh trung ten với fields có sẵn của ERPNext. Khi ERPNext update, ho có thể thêm fields mới. Nếu custom field trung ten → conflict. Prefix `custom_` là convention đảm bảo namespace separation. Frappe 16 bắt buộc convention này.
</details>

<details>
<summary><strong>Câu 2:</strong> Su khác biết giua Custom Field và Property Setter?</summary>

**Trả lời:** Custom Field THEM field MOI vao DocType (VD: thêm "Sales Channel" vao Sales Order). Property Setter THAY DOI THUOC TINH của field CO SAN (VD: ẩn field "Territory", đổi default của "Payment Terms"). Dùng Custom Field cho data mới, Property Setter cho tính chính data cu.
</details>

**DEEP DIVE:** Xem skill `dcnet_quality` → syntax/erpnext-syntax-customapp/ cho custom field patterns.

**DEEP DIVE:** Xem skill `erpnext` → references/ext_syntax-customapp/ cho ERPNext custom app conventions.

---

## L8.4: Integration Patterns

### Tổng quan / Overview

Frappe/ERPNext hỗ trợ nhiều kieu tích hợp: Webhooks (gửi data ra ngoài), Connected App (OAuth2 với hệ thống ngoài), Email integration, và background jobs. Hiểu các pattern này giúp kết nối ERPNext với e-commerce, logistics, accounting software, và các hệ thống ngoài khác.

### Khái niệm chính / Key Concepts

#### 1. Webhooks (Outgoing)

```
Webhooks gui HTTP request khi co su kien trong ERPNext.

Thiet lap qua UI:
1. Setup → Webhooks → New
2. Chon DocType (VD: "Sales Order")
3. Chon Event (VD: "on_submit")
4. Nhap URL endpoint ngoai
5. Chon method (POST/PUT)
6. Map fields can gui

Webhook JSON format:
{
    "webhook_doctype": "Sales Order",
    "webhook_docevent": "on_submit",
    "request_url": "https://external-api.com/webhook/orders",
    "request_method": "POST",
    "webhook_headers": [
        {"key": "Authorization", "value": "Bearer xxx"},
        {"key": "Content-Type", "value": "application/json"}
    ],
    "webhook_data": [
        {"fieldname": "name", "key": "order_id"},
        {"fieldname": "customer", "key": "customer_name"},
        {"fieldname": "grand_total", "key": "total_amount"}
    ]
}
```

#### 2. Custom Webhook trong Code

```python
# Gửi data ra hệ thống ngoài khi có su kien
# dcnet_apps/integrations/external_sync.py

import frappe
import requests
from frappe import _


def sync_order_to_external(doc, method):
    """Hook: Dong bo Sales Order sang he thong ngoai.

    Dang ky trong hooks.py:
    doc_events = {
        "Sales Order": {
            "on_submit": "dcnet_apps.integrations.external_sync.sync_order_to_external"
        }
    }
    """
    settings = frappe.get_single("DCNET Integration Settings")
    if not settings.enable_sync:
        return

    payload = {
        "order_id": doc.name,
        "customer": doc.customer_name,
        "items": [
            {"item": item.item_code, "qty": item.qty, "rate": item.rate}
            for item in doc.items
        ],
        "total": doc.grand_total,
        "currency": doc.currency
    }

    try:
        response = requests.post(
            settings.api_url + "/orders",
            json=payload,
            headers={"Authorization": f"Bearer {settings.api_key}"},
            timeout=30
        )
        response.raise_for_status()

        # Lưu kết quả sync
        frappe.db.set_value("Sales Order", doc.name,
            "custom_sync_status", "Synced"
        )

    except requests.RequestException as e:
        frappe.log_error(
            title=f"Sync failed for {doc.name}",
            message=str(e)
        )
        frappe.db.set_value("Sales Order", doc.name,
            "custom_sync_status", "Failed"
        )


# Retry failed syncs — Scheduled task
def retry_failed_syncs():
    """Chay hang gio de retry cac sync that bai.

    scheduler_events = {
        "hourly": ["dcnet_apps.integrations.external_sync.retry_failed_syncs"]
    }
    """
    failed_orders = frappe.db.get_all("Sales Order",
        filters={"custom_sync_status": "Failed", "docstatus": 1},
        limit=50
    )
    for order in failed_orders:
        doc = frappe.get_doc("Sales Order", order.name)
        sync_order_to_external(doc, None)
```

#### 3. Background Jobs

```python
import frappe
from frappe.utils.background_jobs import enqueue


def submit_heavy_order(order_name):
    """Xu ly don hang nang (nhieu items) trong background."""
    enqueue(
        method="dcnet_apps.tasks.process_order.process_order_background",
        queue="long",           # short (5m), default (5m), long (24h)
        timeout=600,            # 10 phut
        is_async=True,
        order_name=order_name
    )
    frappe.msgprint("Order is being processed in background")


def process_order_background(order_name):
    """Chay trong background worker."""
    doc = frappe.get_doc("Sales Order", order_name)

    for item in doc.items:
        # Xử lý nang (VD: kiểm tra tồn kho, tính gia, etc.)
        process_item(item)

    doc.custom_processing_status = "Completed"
    doc.save()
    frappe.db.commit()  # Can commit trong background job

    # Gửi notification khi xong
    frappe.publish_realtime(
        event="order_processed",
        message={"order": order_name, "status": "completed"},
        user=doc.owner
    )


# Scheduled background tasks (hooks.py)
# scheduler_events = {
#     "daily": ["dcnet_apps.tasks.daily.cleanup_old_logs"],
#     "hourly": ["dcnet_apps.tasks.hourly.check_stock_alerts"],
#     "weekly": ["dcnet_apps.tasks.weekly.generate_reports"],
#     "monthly": ["dcnet_apps.tasks.monthly.archive_old_data"],
#     "cron": {
#         "0 9 * * 1": ["dcnet_apps.tasks.weekly.monday_morning_report"]
#     }
# }
```

#### 4. Connected App (OAuth2)

```python
# Ket nơi với hệ thống ngoài qua OAuth2
# Setup qua UI: Setup → Connected App → New

# Su dùng trong code:
def get_external_data():
    """Lay data tu he thong ngoai da ket noi OAuth2."""
    connected_app = frappe.get_doc("Connected App", "External ERP")
    token = connected_app.get_access_token()

    response = requests.get(
        "https://external-erp.com/api/customers",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()
```

#### 5. Email Integration

```python
# Gửi email tự động
def send_order_confirmation(order_name):
    """Gui email xac nhan don hang."""
    doc = frappe.get_doc("Sales Order", order_name)

    frappe.sendmail(
        recipients=[doc.contact_email],
        subject=f"Order Confirmation: {doc.name}",
        template="order_confirmation",  # Email template name
        args={
            "doc": doc,
            "customer_name": doc.customer_name,
            "items": doc.items,
            "total": doc.grand_total
        },
        header=["Order Confirmation", "green"]
    )


# Nhận email và tự động tạo document
# Setup: Email Account → check "Enable Incoming"
# hooks.py:
# email_append_to = {
#     "Sales Order": "customer_email",
#     "Issue": "raised_by"
# }
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Khi nào nên dùng Webhook (UI) vs Custom code (doc_events)?</summary>

**Trả lời:** Webhook (UI): Khi chi can gửi data đơn giản (POST JSON) toi 1 URL khi có event. Không can code, user/admin có thể thiết lập. Custom code: Khi can logic phức tạp — transform data, xử lý response, retry, update status. Doc_events linh hoạt hon, nhưng can developer.
</details>

<details>
<summary><strong>Câu 2:</strong> Tại sao can <code>frappe.db.commit()</code> trong background job mà không cần trong web request?</summary>

**Trả lời:** Web request được Frappe tự động commit khi ket thuc thành cong. Background job chạy độc lập (worker process khác), Frappe KHÔNG tự động commit. Nếu không gọi `commit()`, dữ liệu sẽ bi mất khi worker ket thuc. Đây là lỗi thường gap khi bắt đầu viết background jobs.
</details>

**DEEP DIVE:** Xem skill `frappe` → references/integration/ để hiểu thêm về Frappe integration patterns.

**DEEP DIVE:** Xem skill `dcnet_quality` → impl/erpnext-impl-scheduler/ cho scheduled task patterns.

---

## L8.5: Capstone Project — Equipment Rental Module

### Tổng quan / Overview

Du ẩn tong ket: Xây dựng module "Equipment Rental" trên ERPNext, ap dùng tất cả kiến thức từ Module 1-8. Module cho phép quản lý cho thue thiet bi — từ tạo Equipment, Rental Order với workflow, custom fields trên Customer, đến dashboard và báo cáo. Cuối cùng, validate code bang `dcnet_quality` skill.

### Yêu cầu / Requirements

```
Module: Equipment Rental
Mo ta: Quan ly cho thue thiet bi (may khoan, may cat, may han, etc.)

Chuc nang:
1. Equipment DocType — Linked to ERPNext Item
2. Rental Order — Voi workflow (Draft → Submitted → Active → Returned → Cancelled)
3. Custom Fields tren Customer — Loai khach hang thue, so lan thue
4. Dashboard — Number cards, charts
5. Validation — Code quality check

DocTypes can tao:
- Equipment (master data)
- Rental Order (transaction)
- Rental Order Item (child table)
```

### Bài tập / Exercise

#### Phần 1: Equipment DocType

```json
// equipment.json
{
    "doctype": "DocType",
    "name": "Equipment",
    "module": "Equipment Rental",
    "naming_rule": "Expression (old style)",
    "autoname": "EQ-.#####",
    "fields": [
        {"fieldname": "item_code", "label": "Item", "fieldtype": "Link",
         "options": "Item", "reqd": 1, "in_list_view": 1},
        {"fieldname": "equipment_name", "label": "Equipment Name",
         "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
        {"fieldname": "serial_no", "label": "Serial No",
         "fieldtype": "Data", "unique": 1},
        {"fieldname": "status", "label": "Status", "fieldtype": "Select",
         "options": "\nAvailable\nRented\nMaintenance\nRetired",
         "default": "Available", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "daily_rate", "label": "Daily Rate", "fieldtype": "Currency",
         "reqd": 1, "in_list_view": 1},
        {"fieldname": "section_details", "fieldtype": "Section Break"},
        {"fieldname": "description", "label": "Description", "fieldtype": "Text Editor"},
        {"fieldname": "column_break_1", "fieldtype": "Column Break"},
        {"fieldname": "image", "label": "Image", "fieldtype": "Attach Image"},
        {"fieldname": "last_maintenance_date", "label": "Last Maintenance",
         "fieldtype": "Date", "read_only": 1}
    ],
    "permissions": [
        {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Stock Manager", "read": 1, "write": 1, "create": 1}
    ]
}
```

```python
# equipment.py — Controller
import frappe
from frappe import _
from frappe.model.document import Document


class Equipment(Document):
    def validate(self):
        self.validate_item()
        self.validate_daily_rate()

    def validate_item(self):
        """Kiem tra Item ton tai va la loai phu hop."""
        if self.item_code:
            item_type = frappe.db.get_value("Item", self.item_code, "item_group")
            # Có thể kiểm tra item group nếu can

    def validate_daily_rate(self):
        """Daily rate phai > 0."""
        if self.daily_rate and self.daily_rate <= 0:
            frappe.throw(_("Daily rate must be greater than 0"))

    def before_save(self):
        """Fetch ten tu Item neu chua co."""
        if self.item_code and not self.equipment_name:
            self.equipment_name = frappe.db.get_value("Item", self.item_code, "item_name")
```

#### Phần 2: Rental Order với Workflow

```python
# rental_order.py
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, date_diff, add_days, getdate


class RentalOrder(Document):
    def validate(self):
        self.validate_dates()
        self.validate_equipment_available()
        self.calculate_totals()

    def validate_dates(self):
        """Start date phai truoc end date."""
        if self.start_date and self.end_date:
            if getdate(self.end_date) < getdate(self.start_date):
                frappe.throw(_("End Date cannot be before Start Date"))

    def validate_equipment_available(self):
        """Kiem tra thiet bi con kha dung."""
        for item in self.items:
            status = frappe.db.get_value("Equipment", item.equipment, "status")
            if status != "Available" and not self.flags.is_return:
                frappe.throw(_(
                    "Equipment {0} is not available (Status: {1})"
                ).format(item.equipment, status))

    def calculate_totals(self):
        """Tinh tong tien thue."""
        self.total_amount = 0
        rental_days = date_diff(self.end_date, self.start_date) + 1

        for item in self.items:
            daily_rate = frappe.db.get_value("Equipment", item.equipment, "daily_rate")
            item.daily_rate = daily_rate or 0
            item.rental_days = rental_days
            item.amount = item.daily_rate * rental_days * item.quantity
            self.total_amount += item.amount

    def on_submit(self):
        """Khi submit → cap nhat trang thai thiet bi."""
        self.update_equipment_status("Rented")

    def on_cancel(self):
        """Khi cancel → tra lai trang thai."""
        self.update_equipment_status("Available")

    def update_equipment_status(self, status):
        """Cap nhat trang thai cua tat ca thiet bi trong order."""
        for item in self.items:
            frappe.db.set_value("Equipment", item.equipment, "status", status)

    @frappe.whitelist()
    def mark_returned(self):
        """Danh dau da tra thiet bi."""
        self.flags.is_return = True
        self.return_date = today()

        # Tinh phat nếu tra tre
        if getdate(self.return_date) > getdate(self.end_date):
            overdue_days = date_diff(self.return_date, self.end_date)
            self.overdue_days = overdue_days
            self.overdue_penalty = overdue_days * self.total_amount / \
                (date_diff(self.end_date, self.start_date) + 1) * 1.5  # 150% gia/ngay

        self.rental_status = "Returned"
        self.update_equipment_status("Available")
        self.save()

        return {"message": _("Equipment returned successfully")}
```

```python
# Workflow definition — tạo qua fixtures hoặc UI
# fixtures/workflow.json
workflow_data = {
    "doctype": "Workflow",
    "name": "Rental Order Workflow",
    "document_type": "Rental Order",
    "is_active": 1,
    "workflow_state_field": "rental_status",
    "states": [
        {"state": "Draft", "style": ""},
        {"state": "Confirmed", "style": "Primary", "doc_status": "1"},
        {"state": "Active", "style": "Success"},
        {"state": "Returned", "style": "Success"},
        {"state": "Cancelled", "style": "Danger", "doc_status": "2"}
    ],
    "transitions": [
        {"state": "Draft", "action": "Confirm", "next_state": "Confirmed",
         "allowed": "Stock Manager"},
        {"state": "Confirmed", "action": "Activate", "next_state": "Active",
         "allowed": "Stock Manager"},
        {"state": "Active", "action": "Return", "next_state": "Returned",
         "allowed": "Stock Manager"},
        {"state": "Confirmed", "action": "Cancel", "next_state": "Cancelled",
         "allowed": "Stock Manager"},
    ]
}
```

#### Phần 3: Custom Fields trên Customer

```json
// fixtures/custom_field.json — Thêm fields vao Customer
[
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_rental_section",
        "label": "Rental Information",
        "fieldtype": "Section Break",
        "insert_after": "default_currency",
        "collapsible": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_rental_tier",
        "label": "Rental Tier",
        "fieldtype": "Select",
        "options": "\nStandard\nPremium\nEnterprise",
        "insert_after": "custom_rental_section"
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_total_rentals",
        "label": "Total Rentals",
        "fieldtype": "Int",
        "insert_after": "custom_rental_tier",
        "read_only": 1
    },
    {
        "doctype": "Custom Field",
        "dt": "Customer",
        "fieldname": "custom_rental_discount",
        "label": "Rental Discount %",
        "fieldtype": "Percent",
        "insert_after": "custom_total_rentals",
        "depends_on": "eval:doc.custom_rental_tier=='Enterprise'"
    }
]
```

#### Phần 4: Dashboard

```python
# api.py — Endpoints cho Number Cards và Charts

@frappe.whitelist()
def get_total_equipment():
    count = frappe.db.count("Equipment")
    return {"value": count, "fieldtype": "Int"}


@frappe.whitelist()
def get_active_rentals():
    count = frappe.db.count("Rental Order",
        filters={"rental_status": "Active", "docstatus": 1}
    )
    return {"value": count, "fieldtype": "Int"}


@frappe.whitelist()
def get_monthly_revenue():
    """Doanh thu thang hien tai."""
    from frappe.utils import get_first_day, get_last_day

    first_day = get_first_day(today())
    last_day = get_last_day(today())

    result = frappe.db.sql("""
        SELECT COALESCE(SUM(total_amount), 0) as revenue
        FROM `tabRental Order`
        WHERE docstatus = 1
            AND start_date BETWEEN %s AND %s
    """, (first_day, last_day), as_dict=True)

    return {
        "value": result[0].revenue if result else 0,
        "fieldtype": "Currency"
    }
```

```python
# report/rental_summary/rental_summary.py — Script Report
import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"label": _("Equipment"), "fieldname": "equipment", "fieldtype": "Link",
         "options": "Equipment", "width": 150},
        {"label": _("Name"), "fieldname": "equipment_name", "fieldtype": "Data", "width": 200},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Times Rented"), "fieldname": "times_rented", "fieldtype": "Int", "width": 110},
        {"label": _("Total Revenue"), "fieldname": "total_revenue",
         "fieldtype": "Currency", "width": 130},
        {"label": _("Avg Days/Rental"), "fieldname": "avg_days", "fieldtype": "Float", "width": 120},
    ]

    data = frappe.db.sql("""
        SELECT
            e.name as equipment,
            e.equipment_name,
            e.status,
            COUNT(roi.name) as times_rented,
            COALESCE(SUM(roi.amount), 0) as total_revenue,
            COALESCE(AVG(roi.rental_days), 0) as avg_days
        FROM `tabEquipment` e
        LEFT JOIN `tabRental Order Item` roi ON roi.equipment = e.name
        LEFT JOIN `tabRental Order` ro ON ro.name = roi.parent AND ro.docstatus = 1
        GROUP BY e.name
        ORDER BY total_revenue DESC
    """, as_dict=True)

    chart = None
    if data:
        top_10 = [d for d in data if d.total_revenue > 0][:10]
        if top_10:
            chart = {
                "data": {
                    "labels": [d.equipment_name for d in top_10],
                    "datasets": [{"name": _("Revenue"), "values": [d.total_revenue for d in top_10]}]
                },
                "type": "bar"
            }

    return columns, data, None, chart
```

#### Phần 5: Validate Code với dcnet_quality

```
Sau khi hoan thanh code, su dung dcnet_quality skill de validate:

1. Kiem tra Controller patterns:
   - validate() co goi super() khong? (neu ke thua)
   - on_update khong modify fields truc tiep? (dung frappe.db.set_value)
   - Khong import trong Server Script?

2. Kiem tra hooks.py:
   - doc_events format dung?
   - fixtures filter dung format?
   - required_apps co "erpnext"?

3. Kiem tra Client Scripts:
   - Khong dung frappe.db.* trong client?
   - Dung frappe.call() de goi API?

4. Kiem tra Permissions:
   - Moi DocType co permission rules?
   - Sensitive fields co permlevel > 0?

5. Kiem tra Whitelisted Methods:
   - @frappe.whitelist() cho moi API?
   - Validate input parameters?
   - Error handling dung cach?
```

### Checklist hoàn thành / Completion Checklist

```
[ ] Equipment DocType tao va hoat dong
[ ] Rental Order DocType voi child table
[ ] Workflow: Draft → Confirmed → Active → Returned
[ ] Custom Fields tren Customer (3 fields)
[ ] 3 Number Cards (Total Equipment, Active Rentals, Monthly Revenue)
[ ] 1 Script Report (Rental Summary)
[ ] Workspace chua tat ca components
[ ] Code validate — khong co CRITICAL issues
[ ] 5 test cases pass
[ ] Sample data script chay thanh cong
```

### Mini Quiz

<details>
<summary><strong>Câu 1:</strong> Tại sao Equipment DocType link toi Item thay vì tạo độc lập?</summary>

**Trả lời:** Link toi ERPNext Item để tan dùng: (1) Inventory management — theo đổi tồn kho. (2) Pricing — su dùng Price List có sẵn. (3) Reporting — báo cáo chung với Stock reports. (4) Valuation — tính giá trị tại san. Đây là nguyen tac "Extend ERPNext, don't reinvent".
</details>

<details>
<summary><strong>Câu 2:</strong> Trong Rental Order, tại sao dùng <code>frappe.db.set_value</code> để cập nhật Equipment status thay vì <code>equipment.save()</code>?</summary>

**Trả lời:** `set_value` cập nhật trực tiếp DB, nhanh và không trigger Equipment controller hooks. Trong trường hợp này, chi can thay đổi 1 field (status) và không cần chạy validation logic của Equipment. Nếu dùng `save()`, nó sẽ chạy full lifecycle của Equipment — không cần thiet và chậm hơn. Nhưng NEU Equipment có logic trong `on_update` can chạy, thi phải dùng `save()`.
</details>

<details>
<summary><strong>Câu 3:</strong> Nếu mượn tính phat tre han tự động mọi ngày, dùng gi?</summary>

**Trả lời:** Dùng `scheduler_events` trong hooks.py với `"daily"` schedule. Tạo function kiểm tra tất cả Rental Orders có `rental_status = "Active"` và `end_date < today()`, tính phat và gửi notification. Background scheduler chạy dùng 1 lần/ngày, phù hợp cho logic này.
</details>

**DEEP DIVE:** Xem skill `erpnext` → references/ cho ERPNext module patterns thuc te (Selling, Buying, Stock, Accounting).

**DEEP DIVE:** Xem skill `dcnet_quality` → agents/erpnext-code-validator/ để validate code tự động.

**DEEP DIVE:** Xem skill `dcnet_quality` → impl/ cho implementation patterns cho tung loai component.
