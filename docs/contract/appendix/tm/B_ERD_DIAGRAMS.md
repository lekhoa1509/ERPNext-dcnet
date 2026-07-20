# PHỤ LỤC B - SƠ ĐỒ QUAN HỆ THỰC THỂ (ERD)
# ENTITY RELATIONSHIP DIAGRAMS

> **Tài liệu:** SRS - DCNET Flow
> **Phiên bản:** 1.0.0
> **Ngày tạo:** 03/02/2026

---

## 1. TỔNG QUAN QUAN HỆ GIỮA CÁC MODULES

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          DCNET FLOW - ERD OVERVIEW                               │
└─────────────────────────────────────────────────────────────────────────────────┘

                                    ┌──────────────┐
                                    │    User      │
                                    │ (Nhân viên)  │
                                    └──────┬───────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
             ┌──────────┐           ┌──────────┐           ┌──────────┐
             │   Lead   │──────────►│ Customer │◄──────────│ Supplier │
             └────┬─────┘           └────┬─────┘           └────┬─────┘
                  │                      │                      │
                  │      ┌───────────────┼───────────────┐      │
                  │      │               │               │      │
                  │      ▼               ▼               ▼      │
                  │ ┌─────────┐   ┌──────────┐   ┌──────────┐  │
                  │ │ Fitting │   │  Sales   │   │ Coaching │  │
                  │ │  Order  │   │  Order   │   │  Order   │  │
                  │ └────┬────┘   └────┬─────┘   └────┬─────┘  │
                  │      │             │              │        │
                  │      └──────┬──────┴──────┬───────┘        │
                  │             │             │                │
                  │             ▼             ▼                │
                  │      ┌──────────┐   ┌──────────┐          │
                  │      │ Delivery │   │ Invoice  │          │
                  │      │   Note   │   │          │          │
                  │      └────┬─────┘   └────┬─────┘          │
                  │           │              │                 │
                  │           ▼              ▼                 │
                  │      ┌──────────┐   ┌──────────┐          │
                  │      │ Shipment │   │ Payment  │          │
                  │      └──────────┘   │  Entry   │          │
                  │                     └────┬─────┘          │
                  │                          │                 │
                  │                          ▼                 │
                  │                    ┌──────────┐            │
                  │                    │   GL     │            │
                  │                    │ Entry    │            │
                  │                    └──────────┘            │
                  │                                            │
                  │                                            │
                  │      ┌──────────┐   ┌──────────┐          │
                  └─────►│ Purchase │◄──┤ Purchase │◄─────────┘
                         │  Order   │   │ Receipt  │
                         └────┬─────┘   └──────────┘
                              │
                              ▼
                       ┌──────────┐
                       │  Stock   │◄──────┐
                       │  Entry   │       │
                       └────┬─────┘       │
                            │             │
                            ▼             │
                       ┌──────────┐       │
                       │   Item   │───────┘
                       │(Sản phẩm)│
                       └──────────┘
```

---

## 2. ERD CHI TIẾT - MODULE CRM

### 2.1. Lead & Customer

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                              LEAD & CUSTOMER ERD                                │
└────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│       LEAD          │          │     LEAD_SOURCE     │
├─────────────────────┤          ├─────────────────────┤
│ PK lead_id          │          │ PK source_id        │
│    lead_code        │◄─────────│    source_name      │
│    lead_name        │   N:1    │    description      │
│    phone            │          └─────────────────────┘
│    email            │
│    status           │          ┌─────────────────────┐
│ FK source_id        │──────────│       BRANCH        │
│ FK branch_id        │◄─────────├─────────────────────┤
│ FK owner_id         │   N:1    │ PK branch_id        │
│    created_date     │          │    branch_name      │
│    last_contact     │          │    address          │
│    tags             │          │    phone            │
└─────────────────────┘          └─────────────────────┘
         │
         │ Convert (1:1)
         ▼
┌─────────────────────┐          ┌─────────────────────┐
│     CUSTOMER        │          │   CUSTOMER_GROUP    │
├─────────────────────┤          ├─────────────────────┤
│ PK customer_id      │◄─────────│ PK group_id         │
│    customer_code    │   N:1    │    group_name       │
│    customer_name    │          │    price_list_id    │
│    customer_type    │          │    discount_rate    │
│    phone            │          └─────────────────────┘
│    email            │
│ FK group_id         │──────────┐
│ FK price_list_id    │          │
│    credit_limit     │          │ ┌─────────────────────┐
│    outstanding_amt  │          │ │   LOYALTY_TIER      │
│    loyalty_points   │◄─────────┼─├─────────────────────┤
│ FK tier_id          │   N:1    │ │ PK tier_id          │
│ FK owner_id         │          │ │    tier_name        │
│    created_date     │          │ │    min_points       │
└─────────────────────┘          │ │    discount_pct     │
         │                       │ └─────────────────────┘
         │ 1:N                   │
         ▼                       │
┌─────────────────────┐          │ ┌─────────────────────┐
│   CUSTOMER_ADDRESS  │          │ │   LOYALTY_HISTORY   │
├─────────────────────┤          │ ├─────────────────────┤
│ PK address_id       │          │ │ PK history_id       │
│ FK customer_id      │          │ │ FK customer_id      │────┘
│    address_type     │          │ │    points           │
│    address_line     │          │ │    type (earn/burn) │
│    city             │          │ │    reference_doc    │
│    district         │          │ │    trans_date       │
│    ward             │          │ └─────────────────────┘
│    is_default       │
└─────────────────────┘
```

### 2.2. Activity & Communication

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          ACTIVITY & COMMUNICATION ERD                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│     ACTIVITY        │          │   ACTIVITY_TYPE     │
├─────────────────────┤          ├─────────────────────┤
│ PK activity_id      │◄─────────│ PK type_id          │
│    subject          │   N:1    │    type_name        │
│    description      │          │    (Call/SMS/Email/ │
│ FK type_id          │──────────│     FB/Zalo)        │
│ FK lead_id (nullable)          └─────────────────────┘
│ FK customer_id (nullable)
│ FK owner_id         │
│    activity_date    │
│    status           │
└─────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│      TICKET         │          │   TICKET_STATUS     │
├─────────────────────┤          ├─────────────────────┤
│ PK ticket_id        │◄─────────│ PK status_id        │
│    ticket_code      │   N:1    │    status_name      │
│    subject          │          │    (New/InProgress/ │
│    description      │          │     Resolved/Closed)│
│ FK customer_id      │──────────└─────────────────────┘
│ FK status_id        │
│ FK assigned_to      │
│    priority         │
│    created_date     │
│    resolved_date    │
└─────────────────────┘
```

---

## 3. ERD CHI TIẾT - MODULE BÁN HÀNG

### 3.1. Sales Order & Invoice

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            SALES ORDER & INVOICE ERD                             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐                    ┌─────────────────────┐
│    SALES_ORDER      │                    │   ORDER_STATUS      │
├─────────────────────┤                    ├─────────────────────┤
│ PK order_id         │◄───────────────────│ PK status_id        │
│    order_code       │        N:1         │    status_name      │
│    order_type       │                    │    (Draft/Confirmed/│
│    (Retail/Wholesale)                    │     Processing/     │
│ FK customer_id      │──────┐             │     Completed/      │
│ FK status_id        │──────┼─────────────│     Cancelled)      │
│ FK price_list_id    │      │             └─────────────────────┘
│ FK branch_id        │      │
│ FK warehouse_id     │      │
│    order_date       │      │
│    delivery_date    │      │
│    subtotal         │      │
│    discount_amount  │      │
│    tax_amount       │      │
│    grand_total      │      │             ┌─────────────────────┐
│    paid_amount      │      │             │     PRICE_LIST      │
│    outstanding      │      │             ├─────────────────────┤
│ FK voucher_id       │      └────────────►│ PK price_list_id    │
│    loyalty_points_used                   │    price_list_name  │
│    created_by       │                    │    currency         │
│    notes            │                    │    valid_from       │
└─────────┬───────────┘                    │    valid_to         │
          │                                │    is_default       │
          │ 1:N                            └─────────────────────┘
          ▼
┌─────────────────────┐                    ┌─────────────────────┐
│  SALES_ORDER_ITEM   │                    │  PRICE_LIST_ITEM    │
├─────────────────────┤                    ├─────────────────────┤
│ PK item_id          │                    │ PK id               │
│ FK order_id         │                    │ FK price_list_id    │
│ FK product_id       │──────┐             │ FK item_id          │
│    qty              │      │             │    rate             │
│    rate             │      │             └─────────────────────┘
│    discount_pct     │      │
│    discount_amt     │      │
│    amount           │      │
│ FK warehouse_id     │      │
└─────────────────────┘      │
                             │
          ┌──────────────────┘
          │
          ▼
┌─────────────────────┐                    ┌─────────────────────┐
│   SALES_INVOICE     │                    │     ITEM            │
├─────────────────────┤                    │   (Sản phẩm)        │
│ PK invoice_id       │                    ├─────────────────────┤
│    invoice_code     │                    │ PK item_id          │
│ FK order_id         │                    │    item_code        │
│ FK customer_id      │                    │    item_name        │
│    invoice_date     │                    │ FK item_group_id    │
│    due_date         │                    │ FK brand_id         │
│    subtotal         │                    │    standard_rate    │
│    discount_amount  │                    │    uom              │
│    tax_amount       │                    │    barcode          │
│    grand_total      │                    │    has_variants     │
│    status           │                    │    has_serial_no    │
│    (Draft/Submitted/│                    │    has_batch_no     │
│     Paid/Cancelled) │                    │    warranty_period  │
└─────────────────────┘                    └─────────────────────┘
```

### 3.2. Pricing & Discount

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            PRICING & DISCOUNT ERD                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│   PRICING_RULE      │          │    VOUCHER          │
├─────────────────────┤          ├─────────────────────┤
│ PK rule_id          │          │ PK voucher_id       │
│    rule_name        │          │    voucher_code     │
│    apply_on         │          │    voucher_type     │
│    (Item/ItemGroup/ │          │    (Percentage/     │
│     Customer/Group) │          │     Fixed/FreeShip) │
│    applicable_for   │          │    discount_value   │
│    min_qty          │          │    min_order_value  │
│    max_qty          │          │    max_discount     │
│    discount_type    │          │    usage_limit      │
│    discount_pct     │          │    used_count       │
│    discount_amt     │          │    valid_from       │
│    valid_from       │          │    valid_to         │
│    valid_to         │          │    is_active        │
│    priority         │          └─────────────────────┘
│    is_active        │
└─────────────────────┘

┌─────────────────────┐
│   CREDIT_LIMIT      │
├─────────────────────┤
│ PK id               │
│ FK customer_id      │
│    credit_limit     │
│    credit_days      │
│    bypass_approval  │
│    approved_by      │
│    valid_from       │
└─────────────────────┘
```

---

## 4. ERD CHI TIẾT - MODULE MUA HÀNG

### 4.1. Purchase Order & Receipt

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PURCHASE ORDER & RECEIPT ERD                             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐                    ┌─────────────────────┐
│    SUPPLIER         │                    │   SUPPLIER_GROUP    │
├─────────────────────┤                    ├─────────────────────┤
│ PK supplier_id      │◄───────────────────│ PK group_id         │
│    supplier_code    │        N:1         │    group_name       │
│    supplier_name    │                    └─────────────────────┘
│ FK group_id         │──────────────────┐
│    contact_person   │                  │
│    phone            │                  │
│    email            │                  │
│    address          │                  │
│    payment_terms    │                  │
│    credit_days      │                  │
└─────────┬───────────┘                  │
          │                              │
          │ 1:N                          │
          ▼                              │
┌─────────────────────┐                  │
│  PURCHASE_ORDER     │                  │
├─────────────────────┤                  │
│ PK po_id            │                  │
│    po_code          │                  │
│    po_number_vendor │  ◄── PO Number   │
│ FK supplier_id      │──────────────────┘
│    order_date       │
│    required_date    │
│    ship_mode        │
│    (Sea/Air/Express)│
│    confirm_ship_date│
│    status           │
│    (Draft/Submitted/│
│     InTransit/      │
│     PartialReceived/│
│     Completed)      │
│    subtotal         │
│    tax_amount       │
│    grand_total      │
│    paid_amount      │
│    outstanding      │
└─────────┬───────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐                  ┌─────────────────────┐
│  PURCHASE_ORDER_ITEM│                  │  PURCHASE_RECEIPT   │
├─────────────────────┤                  ├─────────────────────┤
│ PK item_id          │                  │ PK receipt_id       │
│ FK po_id            │                  │    receipt_code     │
│ FK product_id       │                  │ FK po_id            │
│    qty              │                  │ FK supplier_id      │
│    received_qty     │                  │ FK warehouse_id     │
│    rate             │                  │    receipt_date     │
│    amount           │                  │    customs_entry_no │
│    ean              │                  │    status           │
│    upc              │                  └─────────┬───────────┘
│    hs_code          │                            │
└─────────────────────┘                            │ 1:N
                                                   ▼
                                        ┌─────────────────────┐
                                        │PURCHASE_RECEIPT_ITEM│
                                        ├─────────────────────┤
                                        │ PK item_id          │
                                        │ FK receipt_id       │
                                        │ FK product_id       │
                                        │    qty              │
                                        │    rate             │
                                        │    batch_no         │
                                        │    serial_no        │
                                        │    amount           │
                                        └─────────────────────┘
```

---

## 5. ERD CHI TIẾT - MODULE KHO

### 5.1. Warehouse & Stock

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            WAREHOUSE & STOCK ERD                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│    WAREHOUSE        │          │   WAREHOUSE_TYPE    │
├─────────────────────┤          ├─────────────────────┤
│ PK warehouse_id     │◄─────────│ PK type_id          │
│    warehouse_code   │   N:1    │    type_name        │
│    warehouse_name   │          │    (Main/Consignment│
│ FK type_id          │──────────│     /Transit)       │
│ FK branch_id        │          └─────────────────────┘
│    address          │
│    contact_person   │
│    phone            │
└─────────┬───────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐          ┌─────────────────────┐
│       BIN           │          │    STOCK_ENTRY      │
│ (Vị trí trong kho)  │          ├─────────────────────┤
├─────────────────────┤          │ PK entry_id         │
│ PK bin_id           │          │    entry_type       │
│ FK warehouse_id     │          │    (Receive/Issue/  │
│    bin_code         │          │     Transfer/Adjust)│
│    bin_name         │          │ FK warehouse_id     │
│    capacity         │          │    posting_date     │
└─────────────────────┘          │ FK reference_doctype│
                                 │ FK reference_name   │
                                 │    status           │
                                 │    (Draft/Submitted/│
                                 │     Cancelled)      │
                                 └─────────┬───────────┘
                                           │
                                           │ 1:N
                                           ▼
                                 ┌─────────────────────┐
                                 │  STOCK_ENTRY_ITEM   │
                                 ├─────────────────────┤
                                 │ PK item_id          │
                                 │ FK entry_id         │
                                 │ FK product_id       │
                                 │    qty              │
                                 │    rate             │
                                 │    amount           │
                                 │ FK source_warehouse │
                                 │ FK target_warehouse │
                                 │    batch_no         │
                                 │    serial_no        │
                                 └─────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│       BATCH         │          │     SERIAL_NO       │
├─────────────────────┤          ├─────────────────────┤
│ PK batch_id         │          │ PK serial_id        │
│ FK item_id          │          │ FK item_id          │
│    batch_no         │          │    serial_no        │
│    expiry_date      │          │ FK warehouse_id     │
│    manufacturing_dt │          │    status           │
│    qty              │          │    (Active/Sold/    │
└─────────────────────┘          │     Warranty)       │
                                 │ FK customer_id      │
                                 │    purchase_date    │
                                 │    warranty_expiry  │
                                 └─────────────────────┘
```

### 5.2. Stock Ledger & Reservation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         STOCK LEDGER & RESERVATION ERD                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│   STOCK_LEDGER      │          │  STOCK_RESERVED     │
├─────────────────────┤          ├─────────────────────┤
│ PK ledger_id        │          │ PK reservation_id   │
│ FK item_id          │          │ FK item_id          │
│ FK warehouse_id     │          │ FK warehouse_id     │
│ FK batch_no         │          │ FK sales_order_id   │
│    posting_date     │          │    qty_reserved     │
│    actual_qty       │          │    reserved_date    │
│    qty_after_trans  │          │    status           │
│    incoming_rate    │          │    (Reserved/       │
│    outgoing_rate    │          │     Released/       │
│    valuation_rate   │          │     Delivered)      │
│    stock_value      │          └─────────────────────┘
│ FK voucher_type     │
│ FK voucher_no       │
└─────────────────────┘

┌─────────────────────┐
│    BIN_STOCK        │
├─────────────────────┤
│ PK id               │
│ FK warehouse_id     │
│ FK bin_id           │
│ FK item_id          │
│    actual_qty       │
│    reserved_qty     │
│    available_qty    │
└─────────────────────┘
```

---

## 6. ERD CHI TIẾT - MODULE DỊCH VỤ GOLF

### 6.1. Fitting

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               FITTING ERD                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│   FITTING_ORDER     │          │  FITTING_STATUS     │
├─────────────────────┤          ├─────────────────────┤
│ PK fitting_id       │◄─────────│ PK status_id        │
│    fitting_code     │   N:1    │    status_name      │
│ FK customer_id      │──────────│    (New/Confirmed/  │
│ FK status_id        │          │     InProgress/     │
│    appointment_date │          │     Completed/      │
│    appointment_time │          │     Cancelled)      │
│ FK branch_id        │          └─────────────────────┘
│ FK fitter_id        │
│    source           │
│    (Website/Store/  │
│     Phone)          │
│ FK sales_order_id   │  ◄── Link to Sales Order
│    notes            │
└─────────┬───────────┘
          │
          │ 1:1
          ▼
┌─────────────────────┐
│ FITTING_MEASUREMENT │
├─────────────────────┤
│ PK measurement_id   │
│ FK fitting_id       │
│    height           │  ◄── cm
│    weight           │  ◄── kg
│    hand_size        │  ◄── S/M/L/XL
│    skill_level      │  ◄── Beginner/Intermediate/Advanced
│    club_head_speed  │  ◄── mph
│    ball_speed       │  ◄── mph
│    swing_type       │  ◄── Draw/Fade/Straight
│    ball_flight      │  ◄── Low/Mid/High
│    iron_distance    │  ◄── yards
│    driver_distance  │  ◄── yards
│    current_club_condition
│    special_needs    │
│    recommendation   │
└─────────────────────┘
```

### 6.2. Coaching

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               COACHING ERD                                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│  COACHING_ORDER     │          │  COACHING_PACKAGE   │
├─────────────────────┤          ├─────────────────────┤
│ PK coaching_id      │◄─────────│ PK package_id       │
│    coaching_code    │   N:1    │    package_name     │
│ FK student_id       │──────────│    package_type     │
│ FK package_id       │          │    (Individual/     │
│ FK coach_id         │          │     Group/          │
│ FK course_id        │          │     Competition)    │
│    start_date       │          │    total_sessions   │
│    status           │          │    session_duration │
│    completed_sessions           │    price            │
│    total_fee        │          │    description      │
│    paid_amount      │          └─────────────────────┘
│    outstanding      │
└─────────┬───────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐          ┌─────────────────────┐
│  COACHING_SESSION   │          │       COACH         │
├─────────────────────┤          ├─────────────────────┤
│ PK session_id       │          │ PK coach_id         │
│ FK coaching_id      │          │ FK employee_id      │
│    session_number   │          │    certificate      │
│    scheduled_date   │          │    experience_years │
│    scheduled_time   │          │    specialization   │
│    actual_start     │          │    rating           │
│    actual_end       │          └─────────────────────┘
│    status           │
│    (Scheduled/      │          ┌─────────────────────┐
│     Completed/      │          │    GOLF_COURSE      │
│     Absent/         │          ├─────────────────────┤
│     Cancelled)      │          │ PK course_id        │
│    content          │          │    course_name      │
│    progress_notes   │          │    address          │
│    homework         │          │    lanes            │
└─────────────────────┘          │    contact_phone    │
                                 │    is_partner       │
                                 └─────────────────────┘

┌─────────────────────┐
│   COACHING_TEST     │
├─────────────────────┤
│ PK test_id          │
│ FK coaching_id      │
│    test_date        │
│ FK coach_id         │
│    skill_level      │
│    test_details     │
│    recommendation   │
└─────────────────────┘
```

### 6.3. Trade-in

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               TRADE-IN ERD                                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│   TRADEIN_ORDER     │          │  TRADEIN_STATUS     │
├─────────────────────┤          ├─────────────────────┤
│ PK tradein_id       │◄─────────│ PK status_id        │
│    tradein_code     │   N:1    │    status_name      │
│ FK customer_id      │──────────│    (New/Inspecting/ │
│ FK status_id        │          │     Quoted/         │
│ FK branch_id        │          │     CustomerConfirm/│
│ FK processed_by     │          │     Processing/     │
│    created_date     │          │     Completed/      │
│ FK old_item_id      │  ◄──     │     Cancelled)      │
│    old_item_name    │     │    └─────────────────────┘
│    old_item_brand   │     │
│    old_item_condition      │    ┌─────────────────────┐
│    (New/Good/Fair/Poor)    │    │  ITEM_CONDITION     │
│    old_item_value   │     │    ├─────────────────────┤
│    old_item_image   │     │    │ PK condition_id     │
│ FK new_item_id      │  ◄──┼────│    condition_name   │
│    new_item_price   │     │    │    discount_factor  │
│ FK voucher_id       │     │    └─────────────────────┘
│    voucher_amount   │     │
│    difference_amount│     │  ◄── = new_price - old_value - voucher
│    payment_status   │     │
│    notes            │     │
└─────────────────────┘     │
                            │
          ┌─────────────────┘
          │
          ▼
┌─────────────────────┐
│  TRADEIN_INSPECTION │
├─────────────────────┤
│ PK inspection_id    │
│ FK tradein_id       │
│    inspection_date  │
│ FK inspector_id     │
│    checklist_result │
│    suggested_price  │
│    manager_approved │
│ FK approved_by      │
│    final_price      │
│    images           │
└─────────────────────┘
```

---

## 7. ERD CHI TIẾT - MODULE KẾ TOÁN

### 7.1. General Ledger & Journal

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          GENERAL LEDGER & JOURNAL ERD                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│     ACCOUNT         │          │   ACCOUNT_TYPE      │
├─────────────────────┤          ├─────────────────────┤
│ PK account_id       │◄─────────│ PK type_id          │
│    account_code     │   N:1    │    type_name        │
│    account_name     │          │    (Asset/Liability/│
│ FK type_id          │──────────│     Equity/Income/  │
│ FK parent_account   │          │     Expense)        │
│    is_group         │          └─────────────────────┘
│    balance_type     │
│    (Debit/Credit)   │
└─────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│   JOURNAL_ENTRY     │          │ JOURNAL_ENTRY_ITEM  │
├─────────────────────┤          ├─────────────────────┤
│ PK journal_id       │◄─────────│ PK item_id          │
│    journal_code     │   1:N    │ FK journal_id       │
│    posting_date     │          │ FK account_id       │
│    reference_type   │          │    debit            │
│    reference_name   │          │    credit           │
│    total_debit      │          │ FK party_type       │
│    total_credit     │          │ FK party            │
│    status           │          │    cost_center      │
│    (Draft/Submitted/│          │    remarks          │
│     Cancelled)      │          └─────────────────────┘
│    remarks          │
└─────────────────────┘

┌─────────────────────┐
│    GL_ENTRY         │
├─────────────────────┤
│ PK gl_entry_id      │
│ FK account_id       │
│    posting_date     │
│    debit            │
│    credit           │
│ FK voucher_type     │
│ FK voucher_no       │
│ FK party_type       │
│ FK party            │
│    balance          │
│    against          │
│    cost_center      │
└─────────────────────┘
```

### 7.2. Receivables & Payables

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         RECEIVABLES & PAYABLES ERD                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐          ┌─────────────────────┐
│  PAYMENT_ENTRY      │          │  PAYMENT_TYPE       │
├─────────────────────┤          ├─────────────────────┤
│ PK payment_id       │◄─────────│ PK type_id          │
│    payment_code     │   N:1    │    type_name        │
│ FK type_id          │──────────│    (Receive/Pay/    │
│    party_type       │          │     Internal)       │
│    (Customer/       │          └─────────────────────┘
│     Supplier)       │
│ FK party            │
│    posting_date     │
│    payment_method   │
│    (Cash/Bank/Check)│
│ FK bank_account     │
│    paid_amount      │
│    status           │
│    (Draft/Submitted/│
│     Reconciled)     │
└─────────┬───────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐
│PAYMENT_ENTRY_REF    │
├─────────────────────┤
│ PK ref_id           │
│ FK payment_id       │
│    reference_type   │
│    (Sales Invoice/  │
│     Purchase Invoice)
│    reference_name   │
│    allocated_amount │
└─────────────────────┘

┌─────────────────────┐
│   AGING_REPORT      │
├─────────────────────┤
│    party_type       │
│    party            │
│    current_amount   │  ◄── 0-30 days
│    30_60_amount     │  ◄── 31-60 days
│    60_90_amount     │  ◄── 61-90 days
│    over_90_amount   │  ◄── >90 days
│    total_outstanding│
└─────────────────────┘
```

---

## 8. QUAN HỆ TỔNG HỢP

### 8.1. Summary của các quan hệ chính

| Entity A | Relationship | Entity B | Cardinality |
|----------|--------------|----------|-------------|
| Lead | converts to | Customer | 1:1 |
| Customer | has many | Sales Order | 1:N |
| Customer | belongs to | Customer Group | N:1 |
| Sales Order | contains | Order Items | 1:N |
| Sales Order | creates | Sales Invoice | 1:1 |
| Sales Order | creates | Delivery Note | 1:N |
| Sales Invoice | receives | Payment Entry | 1:N |
| Supplier | has many | Purchase Order | 1:N |
| Purchase Order | contains | PO Items | 1:N |
| Purchase Order | creates | Purchase Receipt | 1:N |
| Item | stored in | Warehouse | N:N |
| Item | has many | Batch | 1:N |
| Item | has many | Serial No | 1:N |
| Fitting Order | creates | Sales Order | 1:1 |
| Coaching Order | contains | Sessions | 1:N |
| Trade-in | creates | Stock Entry | 1:N |

---

**© 2026 DCNET Corporation**
