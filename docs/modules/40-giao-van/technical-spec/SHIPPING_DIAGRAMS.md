# Shipping Module - Diagrams

> **Module:** Quản lý Giao vận (Shipping Management)
>
> **Nguồn:** FEATURE_SPECIFICATION.md Section 9 + Technical Design
>
> **Cập nhật:** 14/01/2026

---

## Mục lục

1. [Sequence Diagrams](#1-sequence-diagrams)
2. [Activity Diagrams](#2-activity-diagrams)
3. [Component Diagrams](#3-component-diagrams)
4. [Deployment Diagram](#4-deployment-diagram)

---

## 1. Sequence Diagrams

### 1.1. Tạo & Book Shipment

```mermaid
sequenceDiagram
    actor User as NV Kho
    participant DN as Delivery Note
    participant Ship as Shipment
    participant API as Viettel Post API
    participant DB as Database

    User->>DN: Mở Delivery Note
    DN->>Ship: Click "Create Shipment"
    Ship->>Ship: Auto fill data từ DN
    User->>Ship: Fill pickup info
    User->>Ship: Click "Submit"
    Ship->>DB: Validate & Save
    DB-->>Ship: Shipment created (status=Submitted)
    Ship-->>User: Success

    User->>Ship: Click "Book with Carrier"
    Ship->>Ship: Validate booking data
    Ship->>API: POST /api/v1/order/create
    Note over Ship,API: Payload: Sender, Receiver,<br/>Product info, COD
    API->>API: Create order
    API-->>Ship: Response: ORDER_ID, AWB_NUMBER
    Ship->>DB: Update awb_number, status=Booked
    DB-->>Ship: Updated
    Ship-->>User: Booked successfully + AWB
```

### 1.2. Tracking Sync (Cron Job)

```mermaid
sequenceDiagram
    participant Cron as Cron Job
    participant Ship as Shipment
    participant DB as Database
    participant API as VP Tracking API
    participant Notify as Notification

    Cron->>DB: Query Shipments (status IN Booked, In Transit)
    DB-->>Cron: List of Shipments

    loop For each Shipment
        Cron->>API: GET /tracking?awb={AWB}
        API-->>Cron: status_code, status_name, update_time

        Cron->>Cron: Map VP status → ERPNext status
        alt Status = 200 (Delivered)
            Cron->>DB: Update status=Delivered
            Cron->>Notify: Gửi notification KH
        else Status = 300/301/302 (Returned)
            Cron->>DB: Update status=Returned
            Cron->>Notify: Alert NV Kho
        else Status = 102/103 (In Transit)
            Cron->>DB: Update tracking_status=In Progress
        end

        Cron->>DB: Update last_sync_time
    end

    Cron->>Cron: Sleep 30 minutes
    Cron->>DB: Next sync cycle
```

### 1.3. Xử lý Hoàn hàng

```mermaid
sequenceDiagram
    participant VP as Viettel Post
    participant Cron as Tracking Cron
    participant Ship as Shipment
    participant Notify as Notification
    actor WH as NV Kho
    participant SE as Stock Entry
    participant DB as Database

    VP->>VP: Đơn hoàn, status = 300
    Cron->>VP: Poll tracking
    VP-->>Cron: status_code=300, return_reason
    Cron->>Ship: Update status=Returned
    Ship->>DB: Save
    Ship->>Notify: Alert NV Kho

    Notify-->>WH: "Shipment XXX đã hoàn"
    WH->>VP: Nhận hàng vật lý
    WH->>Ship: Mở Shipment, xem return_reason
    WH->>SE: Click "Create Stock Entry"
    SE->>SE: Auto fill items từ DN
    WH->>SE: Chọn Target Warehouse
    WH->>SE: Submit
    SE->>DB: Material Receipt created
    DB->>DB: Update inventory
    DB-->>WH: Stock updated successfully
```

---

## 2. Activity Diagrams

### 2.1. Quy trình Giao hàng Hoàn chỉnh

```mermaid
flowchart TB
    START([Nhận Sales Order]) --> CREATE_DN[Tạo Delivery Note]
    CREATE_DN --> SUBMIT_DN[Submit DN]
    SUBMIT_DN --> CREATE_SHIP[Tạo Shipment]

    CREATE_SHIP --> FILL[Fill thông tin pickup/delivery]
    FILL --> VALIDATE{Validation OK?}

    VALIDATE -->|Không| FIX[Sửa lỗi]
    FIX --> FILL

    VALIDATE -->|OK| SUBMIT_SHIP[Submit Shipment]
    SUBMIT_SHIP --> BOOK[Book với Viettel Post]

    BOOK --> API_CALL{API Success?}

    API_CALL -->|Không| RETRY{Retry?}
    RETRY -->|Có| BOOK
    RETRY -->|Không| CANCEL_MANUAL[Cancel/Manual process]
    CANCEL_MANUAL --> END_FAIL([Kết thúc - Fail])

    API_CALL -->|OK| SAVE_AWB[Lưu AWB Number]
    SAVE_AWB --> TRACKING[Tracking tự động 30 phút/lần]

    TRACKING --> CHECK_STATUS{Tracking Status?}

    CHECK_STATUS -->|In Progress| WAIT[Chờ cập nhật]
    WAIT --> TRACKING

    CHECK_STATUS -->|Delivered| DELIVERED[Giao thành công]
    DELIVERED --> NOTIFY_SUCCESS[Thông báo KH]
    NOTIFY_SUCCESS --> FINAL_DELIVERED[Update Delivery Note status]
    FINAL_DELIVERED --> END_SUCCESS([Kết thúc - Success])

    CHECK_STATUS -->|Returned| RETURNED[Hàng hoàn]
    RETURNED --> ALERT_WH[Alert NV Kho]
    ALERT_WH --> RECEIVE_RETURN[NV Kho nhận hàng]
    RECEIVE_RETURN --> CREATE_SE[Tạo Stock Entry]
    CREATE_SE --> UPDATE_INV[Cập nhật tồn kho]
    UPDATE_INV --> END_RETURN([Kết thúc - Returned])

    CHECK_STATUS -->|Lost| HANDLE_LOST[Xử lý thất lạc]
    HANDLE_LOST --> CLAIM[Claim bảo hiểm]
    CLAIM --> END_LOST([Kết thúc - Lost])
```

### 2.2. Quy trình Đối soát COD

```mermaid
flowchart TB
    START([Viettel Post gửi file đối soát]) --> DOWNLOAD[Kế toán download file Excel]

    DOWNLOAD --> OPEN_REPORT[Mở Report COD Pending]
    OPEN_REPORT --> COMPARE[So sánh từng dòng]

    COMPARE --> LOOP{Còn dòng?}

    LOOP -->|Không| DONE[Hoàn thành đối chiếu]

    LOOP -->|Có| NEXT_LINE[Lấy dòng tiếp theo]
    NEXT_LINE --> CHECK_AWB{AWB có trong hệ thống?}

    CHECK_AWB -->|Không| MISMATCH[Ghi nhận lệch]
    MISMATCH --> LOOP

    CHECK_AWB -->|Có| CHECK_AMOUNT{COD Amount khớp?}

    CHECK_AMOUNT -->|Không| INVESTIGATE[Điều tra nguyên nhân]
    INVESTIGATE --> LOOP

    CHECK_AMOUNT -->|Khớp| MARK[Check Shipment.cod_collected]
    MARK --> LOOP

    DONE --> CALC[Tính tổng COD trong kỳ]
    CALC --> CREATE_PE[Tạo Payment Entry]
    CREATE_PE --> SUBMIT_PE[Submit Payment Entry]
    SUBMIT_PE --> UPDATE_FLAG[Update Shipment.cod_remitted]
    UPDATE_FLAG --> END([Kết thúc])
```

---

## 3. Component Diagrams

### 3.1. System Components

```mermaid
flowchart TB
    subgraph "DCNET Core ERPNext"
        subgraph "Stock Module"
            DN[Delivery Note]
            SE[Stock Entry]
            WH[Warehouse]
        end

        subgraph "Selling Module"
            SO[Sales Order]
            CUST[Customer]
        end

        subgraph "Accounts Module"
            SR[Shipping Rule]
            PE[Payment Entry]
        end

        subgraph "Shipping Module - Core"
            SHIP[Shipment DocType]
            SP[Shipment Parcel]
            SDN[Shipment Delivery Note]
        end
    end

    subgraph "dcnet_shipping App Custom"
        API_HANDLER[API Handler]
        TRACKER[Tracking Service]
        WEBHOOK[Webhook Receiver]
        COD_REC[COD Reconciliation]
    end

    subgraph "External Services"
        VP_CREATE[VP Create Order API]
        VP_TRACK[VP Tracking API]
        VP_WEBHOOK[VP Webhook]
    end

    SO --> DN
    DN --> SHIP
    SHIP --> SP
    SHIP --> SDN
    SHIP --> SE

    SHIP --> API_HANDLER
    API_HANDLER --> VP_CREATE
    VP_CREATE -.->|AWB| API_HANDLER

    SHIP --> TRACKER
    TRACKER --> VP_TRACK
    VP_TRACK -.->|Status| TRACKER

    VP_WEBHOOK -.->|Push notification| WEBHOOK
    WEBHOOK --> SHIP

    SHIP --> COD_REC
    COD_REC --> PE

    SHIP --> SR
```

### 3.2. API Integration Architecture

```mermaid
flowchart LR
    subgraph DCNET
        SHIP[Shipment]
        HANDLER[API Handler]
        QUEUE[Task Queue]
    end

    subgraph Cache
        REDIS[(Redis Cache)]
    end

    subgraph VP
        CREATE[Create Order API]
        TRACK[Tracking API]
        WEBHOOK[Webhook Endpoint]
    end

    SHIP -->|Book request| HANDLER
    HANDLER -->|Queue task| QUEUE
    QUEUE -->|Async call| CREATE
    CREATE -.->|Response| QUEUE
    QUEUE -->|Update| SHIP

    SHIP -->|Tracking request| HANDLER
    HANDLER -->|Check cache| REDIS
    REDIS -.->|Hit| HANDLER
    REDIS -.->|Miss| TRACK
    TRACK -.->|Response| HANDLER
    HANDLER -->|Cache 5min| REDIS
    HANDLER -->|Update| SHIP

    WEBHOOK -.->|POST /webhook| HANDLER
    HANDLER -->|Verify signature| HANDLER
    HANDLER -->|Update| SHIP
```

---

## 4. Deployment Diagram

### 4.1. Production Deployment

```mermaid
flowchart TB
    subgraph "User Devices"
        BROWSER[Web Browser]
        MOBILE[Mobile App]
    end

    subgraph "Load Balancer"
        LB[Nginx Load Balancer]
    end

    subgraph "Application Servers"
        APP1[ERPNext Instance 1]
        APP2[ERPNext Instance 2]
    end

    subgraph "Background Workers"
        WORKER1[Worker 1<br/>Tracking Cron]
        WORKER2[Worker 2<br/>Webhook Handler]
    end

    subgraph "Database Layer"
        DB[(MariaDB<br/>Primary)]
        DB_REP[(MariaDB<br/>Replica)]
    end

    subgraph "Cache Layer"
        REDIS[(Redis<br/>Cache/Queue)]
    end

    subgraph "External Services"
        VP[Viettel Post API<br/>https://api.viettelpost.vn]
    end

    BROWSER --> LB
    MOBILE --> LB

    LB --> APP1
    LB --> APP2

    APP1 --> DB
    APP2 --> DB
    APP1 --> REDIS
    APP2 --> REDIS

    DB -.->|Replication| DB_REP

    WORKER1 --> DB
    WORKER2 --> DB
    WORKER1 --> REDIS
    WORKER2 --> REDIS

    WORKER1 -->|Poll tracking| VP
    VP -.->|Webhook| WORKER2

    APP1 -->|Book shipment| VP
    APP2 -->|Book shipment| VP
```

### 4.2. Development Environment

```mermaid
flowchart TB
    subgraph "Developer Machine"
        VSCODE[VS Code]
        CONTAINER[Docker Container<br/>frappe-bench]
    end

    subgraph "Container Services"
        APP[ERPNext Dev]
        DB[(MariaDB)]
        REDIS[(Redis)]
    end

    subgraph "External"
        VP_TEST[Viettel Post<br/>Test Environment]
    end

    VSCODE -->|devcontainer| CONTAINER
    CONTAINER --> APP
    APP --> DB
    APP --> REDIS

    APP -->|Test API| VP_TEST
```

---

## 5. Class Diagrams

### 5.1. Shipment Class Structure

```mermaid
classDiagram
    class Shipment {
        +string name
        +string status
        +string tracking_status
        +string service_provider
        +string awb_number
        +decimal shipment_amount
        +decimal cod_amount
        +datetime pickup_date

        +validate()
        +on_submit()
        +on_cancel()
        +book_with_carrier()
        +update_tracking_status()
        +create_return_stock_entry()
    }

    class ShipmentParcel {
        +string parent
        +float length
        +float width
        +float height
        +float weight
        +int count

        +get_volume()
        +get_weight()
    }

    class ShipmentDeliveryNote {
        +string parent
        +string delivery_note

        +get_items()
        +get_customer()
    }

    class ViettelPostAPI {
        +string api_key
        +string base_url

        +create_order(shipment)
        +track_order(awb_number)
        +cancel_order(order_id)
    }

    class TrackingService {
        +sync_tracking_status()
        +process_webhook(data)
        +map_vp_status_to_erpnext(code)
    }

    Shipment "1" *-- "*" ShipmentParcel
    Shipment "1" *-- "*" ShipmentDeliveryNote
    Shipment --> ViettelPostAPI : uses
    TrackingService --> ViettelPostAPI : calls
    TrackingService --> Shipment : updates
```

---

## 6. Timing Diagrams

### 6.1. Tracking Sync Timeline

```mermaid
gantt
    title Tracking Sync Timeline (1 hour)
    dateFormat HH:mm
    axisFormat %H:%M

    section Cron Job
    Sync Cycle 1      :active, 09:00, 5m
    Sleep             :        09:05, 25m
    Sync Cycle 2      :active, 09:30, 5m
    Sleep             :        09:35, 25m
    Sync Cycle 3      :active, 10:00, 5m

    section API Calls
    Query Shipments   :crit,   09:00, 1m
    Call VP API       :        09:01, 3m
    Update DB         :        09:04, 1m

    section Database
    Read Shipments    :        09:00, 1m
    Write Updates     :        09:04, 1m
```

### 6.2. Order Lifecycle Timeline

```mermaid
gantt
    title Shipment Lifecycle (3 days)
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section Order
    Sales Order       :done,    2026-01-14, 1d
    Delivery Note     :done,    2026-01-15, 1d

    section Shipping
    Create Shipment   :active,  2026-01-15, 1d
    Book with VP      :         2026-01-15, 1d
    In Transit        :         2026-01-16, 2d
    Delivered         :milestone, 2026-01-17, 0d

    section Tracking
    Tracking Start    :         2026-01-15, 3d
    Status Updates    :         2026-01-15, 3d
```

---

**Cập nhật:** 14/01/2026

**Tài liệu liên quan:**
- [SHIPPING_SPEC.md](./SHIPPING_SPEC.md)
- [SHIPPING_STATUS.md](./SHIPPING_STATUS.md)
- [SHIPPING_WORKFLOW.md](./SHIPPING_WORKFLOW.md)
- [SHIPPING_USE_CASE_SPEC.md](./SHIPPING_USE_CASE_SPEC.md)
