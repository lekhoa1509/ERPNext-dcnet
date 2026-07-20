# Thiết kế Extension: Fitting, Coaching, Trade-in trên ERPNext

> **Mục đích:** Giải thích chi tiết cách extend ERPNext Opportunity/Quotation cho các module đặc thù
>
> **Nguồn yêu cầu:** FEATURE_SPECIFICATION.md - Section 16, 17, 18
>
> **Ngày:** 23/01/2026

---

## 1. Tổng quan Kiến trúc

### ERPNext Native Flow

```
Lead ──────────────────────────────────────────────────────────────────┐
  │                                                                    │
  │ make_opportunity()                                                 │
  ▼                                                                    │
Opportunity ───────────────────────────────────────────────────────────┤
  │                                                                    │
  │ make_quotation()                                                   │
  ▼                                                                    │
Quotation ─────────────────────────────────────────────────────────────┤
  │                                                                    │
  │ make_sales_order()  ←── TỰ ĐỘNG TẠO CUSTOMER từ Lead/Prospect      │
  ▼                                                                    │
Sales Order ───────────────────────────────────────────────────────────┤
  │                                                                    │
  │ make_delivery_note() / make_sales_invoice()                        │
  ▼                                                                    │
Delivery Note / Sales Invoice                                          │
  │                                                                    │
  │ make_payment_entry()                                               │
  ▼                                                                    │
Payment Entry ─────────────────────────────────────────────────────────┘
```

### Extension Design cho Fitting/Coaching/Trade-in

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DCNET FLOW EXTENSION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Fitting    │    │   Coaching   │    │   Trade-in   │                   │
│  │   Order      │    │   Order      │    │   Order      │                   │
│  │  (Custom)    │    │  (Custom)    │    │  (Custom)    │                   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                   │
│         │                   │                   │                           │
│         │ Link              │ Link              │ Link                      │
│         ▼                   ▼                   ▼                           │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                     Quotation (ERPNext Native)                   │       │
│  │  • order_type: Sales/Fitting/Coaching/Trade-in                   │       │
│  │  • fitting_order / coaching_order / tradein_order (Link fields)  │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                │                                            │
│                                │ make_sales_order() [Native]                │
│                                ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                   Sales Order (ERPNext Native)                   │       │
│  │  • fitting_order / coaching_order / tradein_order (Link fields)  │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Module Fitting - Chi tiết Thiết kế

### 2.1. Yêu cầu từ Spec (Section 16)

**Nguồn:** FEATURE_SPECIFICATION.md Line 1047-1172

```
Fitting Order:
├── Thông tin khách hàng
├── Lịch hẹn (ngày + giờ)
├── Chi nhánh thực hiện
├── NV Fitting phụ trách
├── Thông số kỹ thuật (20+ fields)
├── Đề xuất nâng cấp
├── Dịch vụ phát sinh (grip, shaft, gậy custom)
└── Trạng thái: Mới → Xác nhận → Đang thực hiện → Hoàn thành → Hủy
```

### 2.2. Thiết kế DocType

#### A. Fitting Order (Custom DocType)

```python
# dcnet_apps/fitting/doctype/fitting_order/fitting_order.py

class FittingOrder(Document):
    # Lifecycle
    def validate(self):
        self.validate_schedule()
        self.calculate_totals()

    def on_submit(self):
        # Nếu có dịch vụ phát sinh → tự động tạo Quotation
        if self.has_services():
            self.create_quotation()

    @frappe.whitelist()
    def create_quotation(self):
        """Tạo Quotation từ dịch vụ phát sinh"""
        from frappe.model.mapper import get_mapped_doc

        quotation = get_mapped_doc(
            "Fitting Order",
            self.name,
            {
                "Fitting Order": {
                    "doctype": "Quotation",
                    "field_map": {
                        "customer": "party_name",
                        "name": "fitting_order",  # Custom link field
                    }
                },
                "Fitting Service Item": {  # Child table
                    "doctype": "Quotation Item",
                    "field_map": {
                        "item_code": "item_code",
                        "qty": "qty",
                        "rate": "rate"
                    }
                }
            }
        )
        quotation.quotation_to = "Customer"
        quotation.order_type = "Fitting"  # Custom field hoặc dùng existing
        quotation.insert()

        # Link ngược
        self.db_set("quotation", quotation.name)

        return quotation.name
```

#### B. Schema Fitting Order

```json
{
    "doctype": "DocType",
    "name": "Fitting Order",
    "module": "DCNET Fitting",
    "naming_rule": "Expression",
    "autoname": "FIT-.YYYY.-.#####",
    "fields": [
        // === SECTION: Thông tin cơ bản ===
        {"fieldname": "customer", "fieldtype": "Link", "options": "Customer"},
        {"fieldname": "lead", "fieldtype": "Link", "options": "Lead"},
        {"fieldname": "schedule_date", "fieldtype": "Date", "reqd": 1},
        {"fieldname": "schedule_time", "fieldtype": "Time", "reqd": 1},
        {"fieldname": "branch", "fieldtype": "Link", "options": "Branch"},
        {"fieldname": "fitting_staff", "fieldtype": "Link", "options": "User"},
        {"fieldname": "source", "fieldtype": "Select", "options": "\nWebsite\nCửa hàng\nĐiện thoại"},
        {"fieldname": "status", "fieldtype": "Select", "options": "Mới đăng ký\nĐã xác nhận\nĐang thực hiện\nHoàn thành\nHủy"},

        // === SECTION: Thông số kỹ thuật ===
        {"fieldname": "height", "fieldtype": "Float", "label": "Chiều cao (cm)"},
        {"fieldname": "weight", "fieldtype": "Float", "label": "Cân nặng (kg)"},
        {"fieldname": "hand_size", "fieldtype": "Data", "label": "Size tay"},
        {"fieldname": "skill_level", "fieldtype": "Select", "options": "\nNgười mới\nNgười đã chơi\nChuyên nghiệp"},
        {"fieldname": "club_head_speed", "fieldtype": "Float", "label": "Tốc độ đầu gậy"},
        {"fieldname": "ball_speed", "fieldtype": "Float", "label": "Tốc độ bóng"},
        {"fieldname": "swing_shape", "fieldtype": "Data", "label": "Hình swing"},
        {"fieldname": "ball_flight", "fieldtype": "Data", "label": "Đường bóng"},
        {"fieldname": "ball_height", "fieldtype": "Data", "label": "Đường cao bóng"},
        {"fieldname": "iron_distance", "fieldtype": "Float", "label": "Khoảng cách gậy sắt"},
        {"fieldname": "driver_distance", "fieldtype": "Float", "label": "Khoảng cách driver"},
        {"fieldname": "current_clubs_condition", "fieldtype": "Text", "label": "Tình trạng bộ gậy"},
        {"fieldname": "customer_needs", "fieldtype": "Text", "label": "Nhu cầu riêng"},

        // === SECTION: Đề xuất nâng cấp ===
        {"fieldname": "upgrade_recommendations", "fieldtype": "Text Editor"},

        // === SECTION: Dịch vụ phát sinh ===
        {"fieldname": "services", "fieldtype": "Table", "options": "Fitting Service Item"},
        {"fieldname": "total_service_amount", "fieldtype": "Currency"},

        // === SECTION: Link với ERPNext ===
        {"fieldname": "quotation", "fieldtype": "Link", "options": "Quotation", "read_only": 1},
        {"fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "read_only": 1}
    ]
}
```

#### C. Extend Quotation với Custom Field

```python
# dcnet_apps/fitting/setup.py

def after_install():
    # Add custom field to Quotation
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    create_custom_fields({
        "Quotation": [
            {
                "fieldname": "fitting_order",
                "label": "Fitting Order",
                "fieldtype": "Link",
                "options": "Fitting Order",
                "insert_after": "opportunity"
            }
        ],
        "Sales Order": [
            {
                "fieldname": "fitting_order",
                "label": "Fitting Order",
                "fieldtype": "Link",
                "options": "Fitting Order",
                "insert_after": "quotation"
            }
        ]
    })
```

### 2.3. Flow hoàn chỉnh

```
                                    ┌─────────────────┐
Website/CRM ──────────────────────▶ │  Fitting Order  │
                                    │   (Custom)      │
                                    └────────┬────────┘
                                             │
               ┌─────────────────────────────┼─────────────────────────────┐
               │                             │                             │
               ▼                             ▼                             ▼
      ┌────────────────┐          ┌────────────────┐           ┌────────────────┐
      │ Không phát sinh│          │ Có dịch vụ     │           │ Chỉ lưu thông  │
      │ Sales Order    │          │ phát sinh      │           │ số kỹ thuật    │
      └────────────────┘          └───────┬────────┘           └────────────────┘
                                          │
                                          │ create_quotation()
                                          ▼
                                 ┌────────────────────┐
                                 │    Quotation       │
                                 │ fitting_order=FIT-X│
                                 │ order_type=Fitting │
                                 └─────────┬──────────┘
                                           │
                                           │ make_sales_order() [Native ERPNext]
                                           ▼
                                 ┌────────────────────┐
                                 │   Sales Order      │
                                 │ fitting_order=FIT-X│
                                 └─────────┬──────────┘
                                           │
                                           │ [Native ERPNext Flow]
                                           ▼
                                 ┌────────────────────┐
                                 │ Delivery / Invoice │
                                 └────────────────────┘
```

---

## 3. Module Coaching - Chi tiết Thiết kế

### 3.1. Yêu cầu từ Spec (Section 17)

**Nguồn:** FEATURE_SPECIFICATION.md Line 1175-1355

```
Coaching Order:
├── Hồ sơ học viên (thông tin cá nhân, trình độ, mục tiêu)
├── Gói huấn luyện (8 buổi cơ bản, 12 buổi nâng cao...)
├── HLV phụ trách
├── Sân tập
├── Lịch học & Điểm danh (Coaching Session)
├── Bài test đầu vào
├── Tiến độ học tập (kỹ năng swing, putting...)
├── Công nợ học phí
└── Trạng thái: Mới → Test → Tư vấn → Thanh toán → Đang học → Hoàn thành
```

### 3.2. Thiết kế DocType

#### A. Coaching Order (Custom DocType)

```python
# dcnet_apps/coaching/doctype/coaching_order/coaching_order.py

class CoachingOrder(Document):
    def validate(self):
        self.validate_package()
        self.calculate_fees()

    def on_submit(self):
        # Tự động tạo Coaching Sessions dựa trên gói học
        self.create_sessions()
        # Tạo Quotation cho học phí
        self.create_quotation()

    @frappe.whitelist()
    def create_quotation(self):
        """Tạo Quotation cho học phí"""
        quotation = frappe.new_doc("Quotation")
        quotation.quotation_to = "Customer"
        quotation.party_name = self.customer
        quotation.order_type = "Coaching"  # hoặc dùng field riêng
        quotation.coaching_order = self.name  # Custom link field

        # Add gói học như 1 item
        quotation.append("items", {
            "item_code": self.package,  # Link to Item doctype
            "qty": 1,
            "rate": self.package_price,
            "description": f"Gói {self.package_name} - {self.total_sessions} buổi"
        })

        # Add phụ kiện phát sinh nếu có
        for item in self.additional_items:
            quotation.append("items", {
                "item_code": item.item_code,
                "qty": item.qty,
                "rate": item.rate
            })

        quotation.insert()
        self.db_set("quotation", quotation.name)
        return quotation.name

    def create_sessions(self):
        """Tạo các buổi học dựa trên gói"""
        package = frappe.get_doc("Coaching Package", self.package)

        for i in range(package.total_sessions):
            session = frappe.new_doc("Coaching Session")
            session.coaching_order = self.name
            session.session_number = i + 1
            session.student = self.customer
            session.coach = self.coach
            session.status = "Scheduled"
            session.insert()
```

#### B. Supporting DocTypes

```
Coaching Module:
├── Coaching Order (Main)
├── Coaching Package (Master - Gói học)
├── Coaching Session (Buổi học)
├── Coaching Test (Bài test đầu vào)
├── Coach (HLV - extend Employee)
├── Golf Course (Sân tập)
└── Coaching Progress (Tiến độ kỹ năng)
```

#### C. Liên kết với Quotation/Sales Order

```python
# dcnet_apps/coaching/setup.py

def after_install():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    create_custom_fields({
        "Quotation": [
            {
                "fieldname": "coaching_order",
                "label": "Coaching Order",
                "fieldtype": "Link",
                "options": "Coaching Order",
                "insert_after": "fitting_order"
            }
        ],
        "Sales Order": [
            {
                "fieldname": "coaching_order",
                "label": "Coaching Order",
                "fieldtype": "Link",
                "options": "Coaching Order",
                "insert_after": "fitting_order"
            }
        ]
    })
```

### 3.3. Flow hoàn chỉnh

```
Website/CRM ─────────────────────────────────────────────────────────────────┐
                                                                              │
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐      │
    │ Coaching Test   │────▶│ Coaching Order  │◀────│ Coaching Package│      │
    │ (Bài test)      │     │   (Đơn học)     │     │ (Gói học)       │      │
    └─────────────────┘     └────────┬────────┘     └─────────────────┘      │
                                     │                                        │
           ┌─────────────────────────┼─────────────────────────┐              │
           │                         │                         │              │
           ▼                         ▼                         ▼              │
  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐      │
  │Coaching Session │      │   Quotation     │      │Coaching Progress│      │
  │ (Buổi học)      │      │ (Học phí)       │      │ (Tiến độ)       │      │
  │ × N buổi        │      └────────┬────────┘      └─────────────────┘      │
  └─────────────────┘               │                                         │
                                    │ make_sales_order() [Native]             │
                                    ▼                                         │
                          ┌─────────────────┐                                 │
                          │  Sales Order    │                                 │
                          │ (Thanh toán)    │                                 │
                          └────────┬────────┘                                 │
                                   │                                          │
                    ┌──────────────┼──────────────┐                           │
                    ▼              ▼              ▼                           │
              ┌──────────┐  ┌──────────┐  ┌──────────┐                        │
              │Trọn gói  │  │Đặt cọc   │  │Theo buổi │                        │
              │(100%)    │  │(X%)      │  │          │                        │
              └──────────┘  └──────────┘  └──────────┘                        │
                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Module Trade-in - Chi tiết Thiết kế

### 4.1. Yêu cầu từ Spec (Section 18)

**Nguồn:** FEATURE_SPECIFICATION.md Line 1357-1507

```
Trade-in Order:
├── Thông tin SP cũ (tên, thương hiệu, tình trạng, giá thu, ảnh)
├── Thông tin SP mới (chọn từ danh sách, giá bán)
├── Voucher (nếu có)
├── Công thức: Chênh lệch = Giá mới - Giá thu cũ - Voucher
├── Trạng thái: Mới → Kiểm tra → Định giá → KH xác nhận → Xử lý → Hoàn thành
└── Tích hợp Kho: Nhập SP cũ vào kho "Hàng thu cũ", Xuất SP mới
```

### 4.2. Thiết kế DocType

#### A. Trade-in Order (Custom DocType)

```python
# dcnet_apps/tradein/doctype/tradein_order/tradein_order.py

class TradeinOrder(Document):
    def validate(self):
        self.calculate_difference()

    def calculate_difference(self):
        """Tính chênh lệch: Giá mới - Giá cũ - Voucher"""
        self.difference = (
            flt(self.new_item_price)
            - flt(self.old_item_trade_value)
            - flt(self.voucher_amount)
        )

        if self.difference > 0:
            self.customer_pays = self.difference
            self.customer_receives = 0
        else:
            self.customer_pays = 0
            self.customer_receives = abs(self.difference)

    def on_submit(self):
        self.create_quotation()

    @frappe.whitelist()
    def create_quotation(self):
        """
        Tạo Quotation với 2 dòng:
        1. SP mới (positive)
        2. SP cũ thu lại (negative hoặc discount)
        """
        quotation = frappe.new_doc("Quotation")
        quotation.quotation_to = "Customer"
        quotation.party_name = self.customer
        quotation.order_type = "Trade-in"
        quotation.tradein_order = self.name

        # Item mới
        quotation.append("items", {
            "item_code": self.new_item_code,
            "qty": 1,
            "rate": self.new_item_price,
            "description": f"SP mới: {self.new_item_name}"
        })

        # Giá trị SP cũ (như discount)
        quotation.discount_amount = self.old_item_trade_value + flt(self.voucher_amount)

        quotation.insert()
        self.db_set("quotation", quotation.name)
        return quotation.name

    @frappe.whitelist()
    def complete_trade(self):
        """Hoàn thành giao dịch - tạo Stock Entry"""
        # 1. Nhập SP cũ vào kho "Hàng thu cũ"
        se_receipt = frappe.new_doc("Stock Entry")
        se_receipt.stock_entry_type = "Material Receipt"
        se_receipt.append("items", {
            "item_code": self.old_item_code or self.create_old_item(),
            "qty": 1,
            "t_warehouse": "Hàng thu cũ - COMP",  # Configurable
            "basic_rate": self.old_item_trade_value
        })
        se_receipt.tradein_order = self.name
        se_receipt.insert()
        se_receipt.submit()

        # 2. Sales Order → Delivery Note sẽ xuất SP mới (native flow)

        self.db_set("stock_entry_receipt", se_receipt.name)
```

#### B. Schema Trade-in Order

```json
{
    "doctype": "DocType",
    "name": "Tradein Order",
    "module": "DCNET Trade-in",
    "naming_rule": "Expression",
    "autoname": "TI-.YYYY.-.#####",
    "fields": [
        // === SECTION: Thông tin khách hàng ===
        {"fieldname": "customer", "fieldtype": "Link", "options": "Customer", "reqd": 1},
        {"fieldname": "branch", "fieldtype": "Link", "options": "Branch"},
        {"fieldname": "staff", "fieldtype": "Link", "options": "User"},

        // === SECTION: SP cũ (Khách trả) ===
        {"fieldname": "section_old_item", "fieldtype": "Section Break", "label": "Sản phẩm cũ"},
        {"fieldname": "old_item_name", "fieldtype": "Data", "label": "Tên SP cũ", "reqd": 1},
        {"fieldname": "old_item_brand", "fieldtype": "Link", "options": "Brand"},
        {"fieldname": "old_item_condition", "fieldtype": "Select", "options": "Mới\nTốt\nTrung bình\nKém"},
        {"fieldname": "old_item_trade_value", "fieldtype": "Currency", "label": "Giá thu SP cũ", "reqd": 1},
        {"fieldname": "old_item_notes", "fieldtype": "Text"},
        {"fieldname": "old_item_images", "fieldtype": "Attach Image"},

        // === SECTION: SP mới (Khách nhận) ===
        {"fieldname": "section_new_item", "fieldtype": "Section Break", "label": "Sản phẩm mới"},
        {"fieldname": "new_item_code", "fieldtype": "Link", "options": "Item", "reqd": 1},
        {"fieldname": "new_item_name", "fieldtype": "Data", "fetch_from": "new_item_code.item_name"},
        {"fieldname": "new_item_price", "fieldtype": "Currency", "reqd": 1},

        // === SECTION: Tính toán ===
        {"fieldname": "section_calculation", "fieldtype": "Section Break", "label": "Thanh toán"},
        {"fieldname": "voucher_code", "fieldtype": "Link", "options": "Coupon Code"},
        {"fieldname": "voucher_amount", "fieldtype": "Currency"},
        {"fieldname": "difference", "fieldtype": "Currency", "read_only": 1, "label": "Chênh lệch"},
        {"fieldname": "customer_pays", "fieldtype": "Currency", "read_only": 1, "label": "KH thanh toán"},
        {"fieldname": "customer_receives", "fieldtype": "Currency", "read_only": 1, "label": "KH nhận lại"},

        // === SECTION: Trạng thái ===
        {"fieldname": "status", "fieldtype": "Select", "options": "Mới tạo\nĐang kiểm tra\nĐã định giá\nKH xác nhận\nĐang xử lý\nHoàn thành\nĐã hủy"},

        // === SECTION: Link với ERPNext ===
        {"fieldname": "quotation", "fieldtype": "Link", "options": "Quotation", "read_only": 1},
        {"fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "read_only": 1},
        {"fieldname": "stock_entry_receipt", "fieldtype": "Link", "options": "Stock Entry", "read_only": 1}
    ]
}
```

### 4.3. Flow hoàn chỉnh

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TRADE-IN FLOW                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Khách mang SP cũ ──────────────────────────────────────────────────────┐   │
│                                                                         │   │
│                    ┌─────────────────────┐                              │   │
│                    │   Tradein Order     │◀─────────────────────────────┘   │
│                    │   (Đơn trade-in)    │                                  │
│                    └──────────┬──────────┘                                  │
│                               │                                             │
│        ┌──────────────────────┼──────────────────────┐                      │
│        │                      │                      │                      │
│        ▼                      ▼                      ▼                      │
│  ┌───────────┐        ┌─────────────┐        ┌─────────────┐               │
│  │Kiểm tra   │───────▶│  Định giá   │───────▶│ KH xác nhận │               │
│  │SP cũ      │        │  SP cũ      │        │             │               │
│  └───────────┘        └─────────────┘        └──────┬──────┘               │
│                                                     │                       │
│                                                     │ create_quotation()    │
│                                                     ▼                       │
│                                            ┌─────────────────┐              │
│                                            │   Quotation     │              │
│                                            │ (Chênh lệch)    │              │
│                                            └────────┬────────┘              │
│                                                     │                       │
│                                                     │ make_sales_order()    │
│                                                     ▼                       │
│                                            ┌─────────────────┐              │
│                                            │  Sales Order    │              │
│                                            └────────┬────────┘              │
│                                                     │                       │
│                    ┌────────────────────────────────┼───────────────────┐   │
│                    │                                │                   │   │
│                    ▼                                ▼                   │   │
│           ┌─────────────────┐              ┌─────────────────┐          │   │
│           │ Stock Entry     │              │ Delivery Note   │          │   │
│           │ (Nhập SP cũ     │              │ (Xuất SP mới    │          │   │
│           │  vào kho)       │              │  cho khách)     │          │   │
│           └─────────────────┘              └─────────────────┘          │   │
│                    │                                │                   │   │
│                    │        Kho "Hàng thu cũ"       │                   │   │
│                    └────────────────────────────────┘                   │   │
│                                                                         │   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Tại sao ERPNext dễ extend hơn Frappe CRM?

### 5.1. Native Functions có sẵn

| Function | ERPNext | Frappe CRM |
|----------|---------|------------|
| `make_quotation()` | ✅ Native | ❌ Không có |
| `make_sales_order()` | ✅ Native | ❌ Không có |
| `make_customer()` | ✅ Native | ⚠️ Cần integration |
| `get_mapped_doc()` | ✅ Support Quotation | ⚠️ Chỉ Lead → Deal |
| Stock Entry integration | ✅ Native | ❌ Không có |
| Price List integration | ✅ Native | ❌ Không có |

### 5.2. Code Example: Tạo Sales Order từ Custom Module

**ERPNext (Native):**
```python
# Chỉ cần 1 dòng code
from erpnext.selling.doctype.quotation.quotation import make_sales_order
so = make_sales_order(quotation_name)
```

**Frappe CRM (Cần custom):**
```python
# Cần viết toàn bộ mapping logic
def create_sales_order_from_deal(deal_name):
    deal = frappe.get_doc("CRM Deal", deal_name)

    # 1. Tạo Customer nếu chưa có
    customer = create_customer_from_organization(deal.organization)

    # 2. Tạo Quotation
    quotation = frappe.new_doc("Quotation")
    quotation.party_name = customer.name
    quotation.quotation_to = "Customer"
    # ... map tất cả fields manually ...
    quotation.insert()

    # 3. Tạo Sales Order từ Quotation
    # ... còn nhiều code nữa ...
```

### 5.3. Tổng kết Effort

| Module | ERPNext CRM | Frappe CRM |
|--------|-------------|------------|
| **Fitting Order** | ~3 ngày | ~7 ngày |
| **Coaching Order** | ~5 ngày | ~12 ngày |
| **Trade-in Order** | ~4 ngày | ~10 ngày |
| **Tổng** | **~12 ngày** | **~29 ngày** |

**Lý do chênh lệch:**
- ERPNext: Reuse native functions (`make_quotation`, `make_sales_order`, Stock Entry)
- Frappe CRM: Phải viết toàn bộ integration với ERPNext Sales/Stock

---

## 6. Cấu trúc App đề xuất

```
dcnet_apps/
├── dcnet_apps/                   # Main module
│   ├── __init__.py
│   ├── hooks.py                  # Custom hooks
│   └── patches/                  # Migration patches
│
├── fitting/                      # Fitting Module
│   ├── doctype/
│   │   ├── fitting_order/
│   │   ├── fitting_service_item/ # Child table
│   │   └── fitting_technical_spec/ # Optional: tách thông số
│   ├── report/
│   │   └── fitting_performance/
│   └── api.py
│
├── coaching/                     # Coaching Module
│   ├── doctype/
│   │   ├── coaching_order/
│   │   ├── coaching_package/     # Master data
│   │   ├── coaching_session/     # Buổi học
│   │   ├── coaching_test/        # Bài test
│   │   ├── coaching_progress/    # Tiến độ
│   │   ├── coach/                # HLV (extend Employee)
│   │   └── golf_course/          # Sân tập
│   ├── report/
│   │   └── coaching_revenue/
│   └── api.py
│
└── tradein/                      # Trade-in Module
    ├── doctype/
    │   ├── tradein_order/
    │   └── tradein_inspection/   # Optional: form kiểm tra
    ├── report/
    │   └── tradein_summary/
    └── api.py
```

---

## 7. Kết luận

**ERPNext CRM là lựa chọn tối ưu** cho Fitting/Coaching/Trade-in vì:

1. **Native Integration**: `make_quotation()`, `make_sales_order()` có sẵn
2. **Stock Management**: Trade-in cần Stock Entry - ERPNext có native
3. **Price List**: Fitting/Coaching cần bảng giá - ERPNext có native
4. **Customer 360**: Tất cả lịch sử giao dịch tập trung vào Customer doctype
5. **Effort**: 12 ngày vs 29 ngày (tiết kiệm ~60% effort)

---

**© 2026 DCNET Corporation**

**Tham khảo:**
- `docs/feature/FEATURE_SPECIFICATION.md` - Section 16, 17, 18
- `dcnet_core/erpnext/selling/doctype/quotation/quotation.py` - ERPNext Quotation
- `dcnet_core/erpnext/crm/doctype/opportunity/opportunity.py` - ERPNext Opportunity
