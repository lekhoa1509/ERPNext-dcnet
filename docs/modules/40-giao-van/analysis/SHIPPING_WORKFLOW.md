# Shipping Workflow & ERD

> **Module:** Quản lý Giao vận (Shipping Management)
>
> **Nguồn:** FEATURE_SPECIFICATION.md Section 9 + ERPNext Analysis
>
> **Cập nhật:** 14/01/2026

---

## Mục lục

1. [Entity Relationship Diagram](#1-entity-relationship-diagram)
2. [Workflow Diagrams](#2-workflow-diagrams)
3. [State Diagrams](#3-state-diagrams)
4. [Data Flow](#4-data-flow)

---

## 1. Entity Relationship Diagram

### 1.1. ERD - Shipping Module

```mermaid
erDiagram
    SALES_ORDER ||--o{ DELIVERY_NOTE : creates
    DELIVERY_NOTE ||--o{ SHIPMENT : creates
    SHIPMENT ||--o{ SHIPMENT_DELIVERY_NOTE : contains
    SHIPMENT ||--o{ SHIPMENT_PARCEL : contains
    SHIPMENT ||--o| STOCK_ENTRY : triggers_return
    SHIPMENT }o--|| CUSTOMER : ships_to
    SHIPMENT }o--|| WAREHOUSE : ships_from
    SHIPMENT }o--|| SHIPPING_RULE : applies

    SALES_ORDER {
        string name PK
        string customer FK
        decimal grand_total
        string status
    }

    DELIVERY_NOTE {
        string name PK
        string sales_order FK
        string customer FK
        string shipping_address FK
        decimal grand_total
        string status
    }

    SHIPMENT {
        string name PK
        string status
        string tracking_status
        string service_provider
        string awb_number
        string viettel_order_id
        decimal shipment_amount
        decimal cod_amount
        datetime pickup_date
        datetime last_sync_time
    }

    SHIPMENT_DELIVERY_NOTE {
        string parent FK
        string delivery_note FK
    }

    SHIPMENT_PARCEL {
        string parent FK
        float length
        float width
        float height
        float weight
        int count
    }

    SHIPPING_RULE {
        string name PK
        string calculate_based_on
        decimal shipping_amount
    }

    CUSTOMER {
        string name PK
        string customer_name
        string primary_address FK
    }

    WAREHOUSE {
        string name PK
        string warehouse_name
        string address FK
    }

    STOCK_ENTRY {
        string name PK
        string entry_type
        string shipment FK
        datetime posting_date
    }
```

**Nguồn:** ERPNext Shipment Schema

---

## 2. Workflow Diagrams

### 2.1. Workflow Tổng quan

```mermaid
flowchart TB
    START([Bắt đầu]) --> SO[Sales Order]
    SO --> DN[Delivery Note]
    DN --> SHIP[Shipment]

    SHIP --> CHECK_STATUS{Status?}

    CHECK_STATUS -->|Submit| BOOK[Book với Viettel Post]
    BOOK --> GET_AWB[Nhận AWB Number]
    GET_AWB --> TRACK[Tracking tự động]

    TRACK --> CHECK_TRACK{Tracking Status?}

    CHECK_TRACK -->|In Progress| WAIT[Chờ cập nhật]
    WAIT --> TRACK

    CHECK_TRACK -->|Delivered| SUCCESS[Giao thành công]
    SUCCESS --> END1([Kết thúc])

    CHECK_TRACK -->|Returned| RETURN[Xử lý hoàn]
    RETURN --> STOCK[Nhập kho]
    STOCK --> END2([Kết thúc])

    CHECK_TRACK -->|Lost| LOST[Xử lý thất lạc]
    LOST --> END3([Kết thúc])
```

### 2.2. Workflow Chi tiết - Tạo & Book Shipment

```mermaid
flowchart TB
    START([NV Kho mở Delivery Note]) --> CHECK_DN{DN đã submit?}

    CHECK_DN -->|Không| ERROR1[Báo lỗi]
    ERROR1 --> END1([Kết thúc])

    CHECK_DN -->|Có| CREATE[Click Create Shipment]
    CREATE --> FILL[Điền thông tin pickup]
    FILL --> VALIDATE{Validation OK?}

    VALIDATE -->|Không| FIX[Fix lỗi]
    FIX --> FILL

    VALIDATE -->|OK| SUBMIT[Submit Shipment]
    SUBMIT --> STATUS1[Status = Submitted]

    STATUS1 --> BOOK_BTN[Click Book with Carrier]
    BOOK_BTN --> CALL_API[Call VP API]

    CALL_API --> API_RESP{API Response?}

    API_RESP -->|Error| RETRY{Retry?}
    RETRY -->|Có| CALL_API
    RETRY -->|Không| END2([Kết thúc])

    API_RESP -->|Success| SAVE_AWB[Lưu AWB Number]
    SAVE_AWB --> STATUS2[Status = Booked]
    STATUS2 --> END3([Sẵn sàng tracking])
```

### 2.3. Workflow Tracking Tự động

```mermaid
flowchart TB
    START([Cron job 30 phút]) --> QUERY[Query Shipment<br/>status IN Booked In Transit]

    QUERY --> LOOP{Có Shipment?}

    LOOP -->|Không| SLEEP[Chờ 30 phút]
    SLEEP --> START

    LOOP -->|Có| NEXT[Lấy Shipment tiếp theo]
    NEXT --> API[Call VP Tracking API]

    API --> RESP{Response?}

    RESP -->|Error| LOG_ERR[Log error]
    LOG_ERR --> MORE{Còn Shipment?}

    RESP -->|Success| PARSE[Parse status code]
    PARSE --> MAP[Map VP status → ERPNext status]
    MAP --> UPDATE[Update Shipment]
    UPDATE --> CHECK_FINAL{Status final?}

    CHECK_FINAL -->|Delivered| NOTIFY1[Gửi notification]
    NOTIFY1 --> MORE

    CHECK_FINAL -->|Returned| NOTIFY2[Gửi alert NV Kho]
    NOTIFY2 --> MORE

    CHECK_FINAL -->|Khác| MORE

    MORE -->|Có| NEXT
    MORE -->|Không| SLEEP
```

### 2.4. Workflow Xử lý Hoàn hàng

```mermaid
flowchart TB
    START([Shipment status = Returned]) --> ALERT[Gửi alert cho NV Kho]

    ALERT --> RECEIVE[NV Kho nhận hàng vật lý]
    RECEIVE --> INSPECT{Kiểm tra<br/>tình trạng}

    INSPECT -->|Nguyên seal| OK[Hàng OK]
    INSPECT -->|Hư hỏng| DAMAGE[Ghi nhận hư hỏng]

    OK --> CREATE_SE[Tạo Stock Entry<br/>Material Receipt]
    DAMAGE --> CREATE_SE

    CREATE_SE --> FILL_SE[Fill items từ DN]
    FILL_SE --> TARGET[Target Warehouse = Kho ban đầu]

    TARGET --> SUBMIT_SE{Submit OK?}

    SUBMIT_SE -->|Error| FIX[Fix lỗi]
    FIX --> SUBMIT_SE

    SUBMIT_SE -->|OK| UPDATE_INV[Cập nhật tồn kho]
    UPDATE_INV --> LINK[Link SE với Shipment]
    LINK --> COMPLETE[Hoàn tất]
    COMPLETE --> END([Kết thúc])
```

---

## 3. State Diagrams

### 3.1. Shipment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> DRAFT

    DRAFT --> SUBMITTED: Submit
    DRAFT --> CANCELLED: Cancel

    SUBMITTED --> BOOKED: Book API Success
    SUBMITTED --> CANCELLED: Cancel

    BOOKED --> IN_TRANSIT: VP Update 102/103
    BOOKED --> CANCELLED: Cancel Before Pickup

    IN_TRANSIT --> DELIVERED: VP Update 200
    IN_TRANSIT --> RETURNED: VP Update 300/301/302
    IN_TRANSIT --> LOST: VP Update 400

    DELIVERED --> [*]
    RETURNED --> [*]
    LOST --> [*]
    CANCELLED --> [*]

    DRAFT: Draft<br/>Chưa submit
    SUBMITTED: Submitted<br/>Chờ book
    BOOKED: Booked<br/>Đã tạo vận đơn VP
    IN_TRANSIT: In Transit<br/>Đang vận chuyển
    DELIVERED: Delivered<br/>Giao thành công
    RETURNED: Returned<br/>Hoàn trả
    LOST: Lost<br/>Thất lạc
    CANCELLED: Cancelled<br/>Đã hủy
```

### 3.2. COD Payment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> CREATED

    CREATED --> DELIVERED: Shipment giao thành công

    DELIVERED --> COLLECTED: VP thu tiền thành công
    COLLECTED --> RECONCILED: Đối soát xác nhận
    RECONCILED --> REMITTED: VP chuyển tiền về

    CREATED --> CANCELLED: Shipment hủy
    DELIVERED --> FAILED: Thu tiền thất bại

    REMITTED --> [*]
    CANCELLED --> [*]
    FAILED --> [*]

    CREATED: Created<br/>COD đã tạo
    DELIVERED: Delivered<br/>Đã giao chờ thu
    COLLECTED: Collected<br/>VP đã thu tiền
    RECONCILED: Reconciled<br/>Đã đối soát
    REMITTED: Remitted<br/>Đã nhận tiền
    CANCELLED: Cancelled<br/>COD hủy
    FAILED: Failed<br/>Thu tiền thất bại
```

---

## 4. Data Flow

### 4.1. Data Flow - Book Shipment

```mermaid
flowchart LR
    subgraph DCNET[DCNET Flow]
        DN[Delivery Note]
        SHIP[Shipment]
        DB[(Database)]
    end

    subgraph VP[Viettel Post]
        API[VP API]
        VPDB[(VP Database)]
    end

    DN -->|1. Create| SHIP
    SHIP -->|2. Fill data| SHIP
    SHIP -->|3. Submit| DB
    SHIP -->|4. Book API Request| API
    API -->|5. Create Order| VPDB
    VPDB -->|6. Generate AWB| API
    API -->|7. Response AWB| SHIP
    SHIP -->|8. Save AWB| DB
```

### 4.2. Data Flow - Tracking Sync

```mermaid
flowchart LR
    subgraph DCNET[DCNET Flow]
        CRON[Cron Job]
        SHIP[Shipment]
        DB[(Database)]
    end

    subgraph VP[Viettel Post]
        TRACK_API[Tracking API]
        VPDB[(VP Database)]
    end

    CRON -->|1. Query| DB
    DB -->|2. Shipment list| CRON
    CRON -->|3. For each AWB| TRACK_API
    TRACK_API -->|4. Query| VPDB
    VPDB -->|5. Status| TRACK_API
    TRACK_API -->|6. Response| CRON
    CRON -->|7. Parse & Map| CRON
    CRON -->|8. Update| DB
    DB -->|9. Notify| SHIP
```

### 4.3. Data Flow - COD Reconciliation

```mermaid
flowchart LR
    subgraph VP[Viettel Post]
        VPDB[(VP Database)]
        FILE[Excel File]
    end

    subgraph DCNET[DCNET Flow]
        ACC[Kế toán]
        SHIP[Shipment]
        PE[Payment Entry]
        DB[(Database)]
    end

    VPDB -->|1. Export| FILE
    FILE -->|2. Download| ACC
    ACC -->|3. So sánh AWB| DB
    DB -->|4. Shipment list| ACC
    ACC -->|5. Match COD| ACC
    ACC -->|6. Update flags| SHIP
    SHIP -->|7. cod_collected = true| DB
    ACC -->|8. Tạo Payment| PE
    PE -->|9. Save| DB
```

---

## 5. Integration Points

### 5.1. Upstream Integration

```mermaid
flowchart TB
    subgraph CRM
        SO[Sales Order]
    end

    subgraph Stock
        DN[Delivery Note]
        SE[Stock Entry]
    end

    subgraph Shipping
        SHIP[Shipment]
    end

    SO -->|Create| DN
    DN -->|Create| SHIP
    SHIP -->|Return trigger| SE
```

### 5.2. External Integration

```mermaid
flowchart LR
    subgraph DCNET
        SHIP[Shipment]
    end

    subgraph "Viettel Post"
        CREATE[Create Order API]
        TRACK[Tracking API]
        WEBHOOK[Webhook]
    end

    SHIP -->|Book| CREATE
    CREATE -->|AWB| SHIP

    SHIP -->|Poll every 30min| TRACK
    TRACK -->|Status update| SHIP

    WEBHOOK -.->|Real-time update<br/>Phase 2| SHIP
```

---

## 6. UI Mockups

### 6.1. Shipment List View

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Shipment List                                         [+ New] [Filter]  │
├─────────────────────────────────────────────────────────────────────────┤
│ ☑ Name         Customer      Status      AWB Number     Tracking       │
├─────────────────────────────────────────────────────────────────────────┤
│ ☐ SHIPMENT-001 Nguyen Van A  🟡 Booked   VTP123456789  -              │
│ ☐ SHIPMENT-002 Tran Thi B    🟣 In Transit VTP987654321 In Progress    │
│ ☐ SHIPMENT-003 Le Van C      🟢 Delivered VTP456789123  Delivered      │
│ ☐ SHIPMENT-004 Pham Thi D    🟠 Returned  VTP789123456  Returned       │
└─────────────────────────────────────────────────────────────────────────┘

Filters:
┌──────────────────────────────────┐
│ Status:     [All ▾]              │
│ Date Range: [Last 7 days ▾]     │
│ Customer:   [                 ]  │
│ AWB:        [                 ]  │
│             [Apply Filter]       │
└──────────────────────────────────┘
```

### 6.2. Shipment Form View

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Shipment SHIPMENT-001                          [Book] [Submit] [Cancel] │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: 🟡 Submitted                    AWB: VTP123456789               │
│                                                                          │
│ ┌─ Pickup From ────────────────┐  ┌─ Delivery To ─────────────────┐   │
│ │ Type: Company                 │  │ Type: Customer                 │   │
│ │ Company: Nhat Minh Sport      │  │ Customer: Nguyen Van A         │   │
│ │ Address: 123 ABC, HN          │  │ Address: 456 XYZ, HCMC         │   │
│ │ Date: 2026-01-15              │  │ Contact: 0901234567            │   │
│ │ Time: 08:00 - 17:00           │  │                                │   │
│ └───────────────────────────────┘  └────────────────────────────────┘   │
│                                                                          │
│ ┌─ Parcels ──────────────────────────────────────────────────────────┐  │
│ │ Parcel | L(cm) | W(cm) | H(cm) | Weight(kg) | Count | [+ Add]     │  │
│ │ ─────────────────────────────────────────────────────────────────  │  │
│ │   1    |  30   |  20   |  10   |    1.5     |   2   | [Remove]   │  │
│ │                                                                     │  │
│ │ Total Weight: 3.0 kg                                               │  │
│ └─────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│ ┌─ Shipment Details ──────────────────────────────────────────────────┐ │
│ │ Service Provider:  Viettel Post                                     │ │
│ │ Carrier Service:   Standard                                         │ │
│ │ Value of Goods:    500,000 VNĐ                                      │ │
│ │ Shipment Amount:   30,000 VNĐ                                       │ │
│ │ COD Amount:        0 VNĐ                                            │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│ ┌─ Tracking ──────────────────────────────────────────────────────────┐ │
│ │ Status: In Progress                                                  │ │
│ │ Info:   Đang giao hàng                                               │ │
│ │ URL:    https://viettelpost.vn/track/VTP123456789                    │ │
│ │ Last Sync: 2026-01-14 15:30:00                                       │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Cập nhật:** 14/01/2026

**Tài liệu liên quan:**
- [SHIPPING_SPEC.md](./SHIPPING_SPEC.md)
- [SHIPPING_STATUS.md](./SHIPPING_STATUS.md)
- [SHIPPING_DIAGRAMS.md](./SHIPPING_DIAGRAMS.md)
