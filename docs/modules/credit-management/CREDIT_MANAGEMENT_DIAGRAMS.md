# Module Credit Management - Diagrams

> **Phiên bản**: v1.0
> **Ngày cập nhật**: 2026-01-14
> **Mục đích**: Tổng hợp tất cả sơ đồ trực quan cho Credit Management

---

## 📊 Table of Contents

1. [Process Flow Diagrams](#1-process-flow-diagrams)
2. [Sequence Diagrams](#2-sequence-diagrams)
3. [State Machine Diagrams](#3-state-machine-diagrams)
4. [Data Flow Diagrams](#4-data-flow-diagrams)
5. [Architecture Diagrams](#5-architecture-diagrams)
6. [UI Mockup Diagrams](#6-ui-mockup-diagrams)

---

## 1. Process Flow Diagrams

### 1.1. High-Level Credit Control Process

```mermaid
graph TB
    Start([Business Start]) --> SetLimit[Manager<br/>Set Credit Limit]
    SetLimit --> CreateOrder[NVKD<br/>Create Sales Order]
    CreateOrder --> AutoCheck{System<br/>Auto Credit Check}

    AutoCheck -->|Pass<br/>✅ No overdue<br/>✅ Within limit| Approved[Status: Approved<br/>Reserve Credit]
    AutoCheck -->|Fail<br/>❌ Has overdue<br/>OR<br/>❌ Exceed limit| PendingOverride[Status: Pending Override<br/>Email to Kế toán trưởng]

    Approved --> WaitShip[Wait for<br/>Warehouse]
    WaitShip --> Ship[Kho<br/>Ship Goods]
    Ship --> Fulfilled[Status: Fulfilled<br/>Release Credit]

    PendingOverride --> Review{Kế toán trưởng<br/>Review}
    Review -->|Approve| Approved
    Review -->|Reject| Rejected[Status: Rejected<br/>Notify NVKD]

    Fulfilled --> CreateInvoice[Create<br/>Sales Invoice]
    CreateInvoice --> UpdateDebt[Update<br/>Current Debt]

    Rejected --> Renegotiate[NVKD<br/>Renegotiate<br/>with Customer]
    Renegotiate --> End([End])

    UpdateDebt --> Payment{Customer<br/>Payment?}
    Payment -->|Yes| ReduceDebt[Reduce<br/>Current Debt]
    Payment -->|No| CheckOverdue{Overdue?}

    ReduceDebt --> End
    CheckOverdue -->|Yes| Alert[Send<br/>Overdue Alert]
    CheckOverdue -->|No| End
    Alert --> End

    style AutoCheck fill:#fff4e6
    style Review fill:#ffe4e4
    style Approved fill:#d4edda
    style Rejected fill:#f8d7da
```

---

### 1.2. Credit Check Decision Tree

```mermaid
flowchart TD
    Start([Start Credit Check]) --> Input[Input:<br/>- Customer ID<br/>- Order Value]

    Input --> GetData[Fetch Data:<br/>1. Credit Limit<br/>2. Current Debt<br/>3. Pending Orders<br/>4. Overdue Invoices]

    GetData --> Q1{Has Credit<br/>Limit?}
    Q1 -->|No| E1[❌ ERROR:<br/>No credit limit set]
    E1 --> Result1[Status: pending_override<br/>Reason: no_credit_limit]

    Q1 -->|Yes| Q2{Has Overdue<br/>Invoices?}
    Q2 -->|Yes| Calc1[Calculate:<br/>- Overdue count<br/>- Overdue amount<br/>- Avg overdue days]
    Calc1 --> Result2[Status: pending_override<br/>Reason: overdue_invoices<br/>+ Details]

    Q2 -->|No| Q3{Exceed<br/>Credit Limit?}
    Q3 -->|Test| CalcExposure[total_exposure =<br/>current_debt +<br/>pending_orders +<br/>order_value]
    CalcExposure --> Compare{total_exposure ><br/>credit_limit?}

    Compare -->|Yes| Calc2[Calculate:<br/>- Exceed amount<br/>- Credit utilization %]
    Calc2 --> Result3[Status: pending_override<br/>Reason: exceed_limit<br/>+ Details]

    Compare -->|No| Calc3[Calculate:<br/>- Available credit<br/>- Credit utilization %]
    Calc3 --> Result4[Status: approved<br/>Reason: pass<br/>+ Available credit]

    Result1 --> End([End])
    Result2 --> End
    Result3 --> End
    Result4 --> End

    style Q1 fill:#e3f2fd
    style Q2 fill:#fff4e6
    style Q3 fill:#fff4e6
    style Result1 fill:#ffebee
    style Result2 fill:#ffebee
    style Result3 fill:#ffebee
    style Result4 fill:#e8f5e9
```

---

## 2. Sequence Diagrams

### 2.1. Normal Flow - Pass Credit Check

```mermaid
sequenceDiagram
    actor NVKD
    participant UI as Sales Order UI
    participant API as Backend API
    participant CreditEngine as Credit Check Engine
    participant DB as Database
    participant Cache

    NVKD->>UI: Navigate to "Tạo lệnh xuất"
    UI->>API: GET /api/sales-order/new?customer_id=123

    par Parallel Data Loading
        API->>DB: Get order data
        DB-->>API: Order details
    and
        API->>Cache: Get credit info (customer_id)
        alt Cache Hit
            Cache-->>API: Cached credit data
        else Cache Miss
            API->>DB: Calculate credit info
            DB-->>API: Fresh credit data
            API->>Cache: Store cache (TTL: 5min)
        end
    end

    API-->>UI: Response with order + credit data
    UI-->>NVKD: Display form + credit panel

    Note over UI: Credit Panel shows:<br/>Hạn mức: 500M<br/>Công nợ: 200M<br/>Pending: 50M<br/>Available: 250M ✅

    NVKD->>UI: Fill form & Click "Lưu"
    UI->>API: POST /api/sales-order<br/>{ customer_id, items, grand_total }

    API->>CreditEngine: check_credit(customer_id, grand_total)

    CreditEngine->>DB: Query overdue invoices
    DB-->>CreditEngine: [] (no overdue)

    CreditEngine->>DB: Query current debt & pending
    DB-->>CreditEngine: current=200M, pending=50M

    CreditEngine->>CreditEngine: Calculate:<br/>total = 200M + 50M + 100M = 350M<br/>limit = 500M<br/>350M < 500M ✅

    CreditEngine-->>API: Result: PASS<br/>{status: approved, available: 150M}

    API->>DB: INSERT sales_order<br/>SET status = 'Approved'
    API->>DB: Reserve credit (log)
    API->>Cache: Invalidate customer credit cache

    DB-->>API: Success

    API-->>UI: 200 OK {order_id, status: approved}
    UI-->>NVKD: Show "✅ Lệnh xuất đã được duyệt"

    Note over NVKD,DB: Order ready for warehouse to ship
```

---

### 2.2. Exception Flow - Fail Credit Check (Overdue)

```mermaid
sequenceDiagram
    actor NVKD
    participant UI
    participant API
    participant CreditEngine
    participant DB
    participant EmailService
    actor KeToanTruong as Kế toán trưởng

    NVKD->>UI: Fill form & Click "Lưu"
    UI->>API: POST /api/sales-order

    API->>CreditEngine: check_credit(customer_id, 100M)

    CreditEngine->>DB: Query overdue invoices
    DB-->>CreditEngine: [INV-001: 20M (15 days),<br/>INV-005: 10M (5 days)]

    CreditEngine->>CreditEngine: Found overdue!<br/>count = 2<br/>total = 30M

    CreditEngine-->>API: Result: FAIL<br/>{<br/>  status: pending_override,<br/>  reason: overdue_invoices,<br/>  overdue_count: 2,<br/>  overdue_amount: 30M<br/>}

    API->>DB: INSERT sales_order<br/>SET status = 'Pending Override'<br/>credit_check_result = JSON

    API->>EmailService: send_override_request_email(<br/>  to: ketoan@nhatminh.com,<br/>  order: SO-2026-001,<br/>  reason: overdue<br/>)

    EmailService->>KeToanTruong: 📧 Subject: [Cần duyệt] Lệnh xuất #SO-2026-001<br/>Body: KH có 2 HĐ quá hạn (30M)

    DB-->>API: Success
    API-->>UI: 200 OK {<br/>  order_id,<br/>  status: pending_override,<br/>  message: "Có hóa đơn quá hạn"<br/>}

    UI-->>NVKD: Show popup:<br/>"⚠️ KHÔNG ĐỦ ĐIỀU KIỆN XUẤT HÀNG<br/><br/>Lý do: Khách hàng có 2 hóa đơn quá hạn<br/>Tổng giá trị: 30,000,000 VND<br/><br/>Đã gửi yêu cầu phê duyệt đến Kế toán trưởng"

    Note over NVKD,KeToanTruong: Order pending approval
```

---

### 2.3. Override Approval Flow

```mermaid
sequenceDiagram
    actor KeToanTruong as Kế toán trưởng
    participant Email
    participant UI as Approval UI
    participant API
    participant DB
    participant NotificationService
    actor NVKD

    Email->>KeToanTruong: 📧 [Cần duyệt] SO-2026-001
    KeToanTruong->>Email: Click link
    Email->>UI: Open approval page

    UI->>API: GET /api/sales-order/pending-override
    API->>DB: SELECT * WHERE status='Pending Override'
    DB-->>API: List of orders
    API-->>UI: Display list

    KeToanTruong->>UI: Click order #SO-2026-001
    UI->>API: GET /api/sales-order/SO-2026-001/details
    API->>DB: Get order + credit_check_result
    DB-->>API: Full details
    API-->>UI: Show popup

    Note over UI: Display:<br/>- Customer: Đại lý ABC<br/>- Reason: Overdue 30M<br/>- Credit details<br/>- Input: reason field

    KeToanTruong->>KeToanTruong: Review & decide

    alt Decision: APPROVE
        KeToanTruong->>UI: Enter reason:<br/>"KH VIP, cam kết TT trong tuần"<br/>Click "Phê duyệt"

        UI->>API: POST /api/sales-order/SO-2026-001/approve<br/>{ reason, approved_by }

        API->>DB: BEGIN TRANSACTION

        API->>DB: UPDATE sales_order SET<br/>status = 'Approved',<br/>override_approved_by = user_id,<br/>override_reason = reason,<br/>override_at = NOW()

        API->>DB: INSERT audit_log

        API->>DB: Reserve credit

        API->>DB: COMMIT

        API->>NotificationService: notify_nvkd(<br/>  order: SO-2026-001,<br/>  status: approved<br/>)

        NotificationService->>NVKD: 🔔 In-app: "✅ Lệnh xuất #SO-2026-001<br/>đã được Kế toán trưởng phê duyệt"

        DB-->>API: Success
        API-->>UI: 200 OK
        UI-->>KeToanTruong: "✅ Đã phê duyệt thành công"

    else Decision: REJECT
        KeToanTruong->>UI: Enter reason:<br/>"Nợ quá hạn quá nhiều,<br/>cần thu nợ trước"<br/>Click "Từ chối"

        UI->>API: POST /api/sales-order/SO-2026-001/reject<br/>{ reason }

        API->>DB: UPDATE sales_order SET<br/>status = 'Rejected',<br/>override_approved_by = user_id,<br/>override_reason = reason

        API->>DB: INSERT audit_log

        API->>NotificationService: notify_nvkd(<br/>  order: SO-2026-001,<br/>  status: rejected,<br/>  reason<br/>)

        NotificationService->>NVKD: 🔔 In-app + Email:<br/>"❌ Lệnh xuất #SO-2026-001 bị từ chối<br/>Lý do: [reason]"

        DB-->>API: Success
        API-->>UI: 200 OK
        UI-->>KeToanTruong: "✅ Đã từ chối"
    end
```

---

## 3. State Machine Diagrams

### 3.1. Sales Order Status State Machine

```mermaid
stateDiagram-v2
    [*] --> draft: User creates order

    draft --> credit_checking: User clicks Save
    draft --> cancelled: User cancels

    credit_checking --> approved: ✅ Pass check<br/>(no overdue + within limit)
    credit_checking --> pending_override: ❌ Fail check<br/>(overdue OR exceed)

    pending_override --> approved: Kế toán trưởng approves
    pending_override --> rejected: Kế toán trưởng rejects

    approved --> fulfilled: Kho ships goods
    approved --> cancelled: User cancels

    fulfilled --> [*]: Complete
    rejected --> [*]: End
    cancelled --> [*]: End

    state credit_checking {
        [*] --> CheckOverdue
        CheckOverdue --> CheckLimit: No overdue
        CheckOverdue --> FailOverdue: Has overdue
        CheckLimit --> Pass: Within limit
        CheckLimit --> FailLimit: Exceed limit
        Pass --> [*]
        FailOverdue --> [*]
        FailLimit --> [*]
    }

    note right of credit_checking
        Automatic validation:
        1. Query overdue invoices
        2. Calculate total exposure
        3. Compare with credit limit
    end note

    note right of pending_override
        Requires manual approval
        from Kế toán trưởng

        Must provide reason
        for audit trail
    end note

    note right of approved
        Credit is reserved
        (counted in pending orders)

        Warehouse can ship
    end note

    note right of fulfilled
        Credit is released
        (no longer pending)

        Invoice created
        → Current debt updated
    end note
```

---

### 3.2. Credit Limit Lifecycle

```mermaid
stateDiagram-v2
    [*] --> draft: Manager creates

    draft --> active: Effective date reached
    draft --> cancelled: Manager cancels

    active --> expired: Expiry date passed
    active --> suspended: Manager suspends<br/>(customer payment issues)
    active --> superseded: New limit created

    suspended --> active: Manager reactivates<br/>(payment received)

    expired --> [*]: End of lifecycle
    cancelled --> [*]: Never activated
    superseded --> [*]: Replaced by new

    note right of active
        Only 1 active limit
        per customer at a time
    end note

    note right of suspended
        Block all new orders
        until reactivated
    end note
```

---

## 4. Data Flow Diagrams

### 4.1. Context Diagram (Level 0)

```mermaid
flowchart TB
    subgraph External["EXTERNAL ENTITIES"]
        Manager[Manager]
        NVKD[NVKD]
        KeToan[Kế toán trưởng]
        Customer[Customer]
        Kho[Warehouse]
    end

    subgraph System["CREDIT MANAGEMENT SYSTEM"]
        CMS[Credit<br/>Management<br/>System]
    end

    subgraph ExternalSystems["EXTERNAL SYSTEMS"]
        ERP[ERPNext Core]
        EmailSys[Email System]
        NotifSys[Notification System]
    end

    Manager -->|Credit limit data| CMS
    NVKD -->|Sales order request| CMS
    KeToan -->|Override decision| CMS
    Customer -.->|Payment| CMS

    CMS -->|Credit check result| NVKD
    CMS -->|Override request| KeToan
    CMS -->|Shipping approval| Kho
    CMS -->|Overdue alert| NVKD

    CMS <-->|Order data| ERP
    CMS <-->|Invoice data| ERP
    CMS -->|Send email| EmailSys
    CMS -->|Send notification| NotifSys

    style CMS fill:#e3f2fd
```

---

### 4.2. Level 1 DFD - Credit Check Process

```mermaid
flowchart LR
    subgraph Actors
        NVKD[NVKD]
    end

    subgraph Processes["PROCESSES"]
        P1[1.0<br/>Validate<br/>Order]
        P2[2.0<br/>Check<br/>Credit]
        P3[3.0<br/>Calculate<br/>Exposure]
        P4[4.0<br/>Make<br/>Decision]
    end

    subgraph DataStores["DATA STORES"]
        D1[(D1:<br/>Credit<br/>Limit)]
        D2[(D2:<br/>Sales<br/>Invoice)]
        D3[(D3:<br/>Sales<br/>Order)]
    end

    NVKD -->|Order request| P1
    P1 -->|Valid order| P2
    P2 -->|Credit query| D1
    D1 -->|Credit limit| P2
    P2 -->|Overdue query| D2
    D2 -->|Invoice list| P2
    P2 -->|Pending query| D3
    D3 -->|Order list| P2

    P2 -->|Credit data| P3
    P3 -->|Exposure calc| P4

    P4 -->|Decision| P1
    P1 -->|Result| NVKD

    style P2 fill:#fff4e6
    style P4 fill:#ffe4e4
```

---

## 5. Architecture Diagrams

### 5.1. System Architecture

```mermaid
flowchart TB
    subgraph Frontend["FRONTEND LAYER"]
        WebUI[Web UI<br/>Frappe Desk]
        API_Client[REST API Client]
    end

    subgraph Backend["BACKEND LAYER"]
        subgraph API["API Layer"]
            REST[REST API<br/>Endpoints]
            Hooks[DocType Hooks]
        end

        subgraph Business["Business Logic Layer"]
            CreditEngine[Credit Check<br/>Engine]
            Calculator[Credit<br/>Calculator]
            Validator[Business Rule<br/>Validator]
        end

        subgraph Data["Data Access Layer"]
            ORM[Frappe ORM]
            CacheLayer[Redis Cache]
        end
    end

    subgraph Database["DATABASE LAYER"]
        MySQL[(MariaDB)]
        Redis[(Redis)]
    end

    subgraph External["EXTERNAL SERVICES"]
        Email[Email Service]
        Notification[Push Notification]
    end

    WebUI <-->|HTTP/HTTPS| REST
    API_Client <-->|REST API| REST

    REST -->|Call| CreditEngine
    Hooks -->|Trigger| CreditEngine

    CreditEngine -->|Use| Calculator
    CreditEngine -->|Use| Validator

    Calculator -->|Query| ORM
    Calculator -->|Cache| CacheLayer
    Validator -->|Query| ORM

    ORM <-->|SQL| MySQL
    CacheLayer <-->|Redis Protocol| Redis

    CreditEngine -.->|Send| Email
    CreditEngine -.->|Send| Notification

    style CreditEngine fill:#fff4e6
    style Calculator fill:#e3f2fd
    style Validator fill:#e8f5e9
```

---

### 5.2. Component Diagram

```mermaid
flowchart TB
    subgraph CreditManagementModule["Credit Management Module"]
        subgraph Controllers
            C1[SalesOrderController]
            C2[CreditLimitController]
            C3[OverrideController]
        end

        subgraph Services
            S1[CreditCheckService]
            S2[CreditCalculationService]
            S3[NotificationService]
            S4[AuditLogService]
        end

        subgraph Repositories
            R1[CreditLimitRepository]
            R2[SalesOrderRepository]
            R3[InvoiceRepository]
        end

        subgraph Models
            M1[CreditLimit]
            M2[SalesOrder]
            M3[CreditCheckResult]
        end
    end

    C1 -->|Use| S1
    C2 -->|Use| S2
    C3 -->|Use| S1
    C3 -->|Use| S4

    S1 -->|Use| S2
    S1 -->|Use| S3
    S1 -->|Use| R1
    S1 -->|Use| R2
    S1 -->|Use| R3

    S2 -->|Use| R1
    S2 -->|Use| R2
    S2 -->|Use| R3

    R1 -->|CRUD| M1
    R2 -->|CRUD| M2
    R3 -.->|Read| Invoice[(Sales Invoice)]

    S1 -->|Create| M3
```

---

## 6. UI Mockup Diagrams

### 6.1. Credit Info Panel (Lệnh xuất hàng)

```
┌─────────────────────────────────────────┐
│ 💳 THÔNG TIN TÍN DỤNG                  │
├─────────────────────────────────────────┤
│                                         │
│ 📊 Hạn mức tín dụng                    │
│ ┌────────────────────────────────────┐ │
│ │   500,000,000 VND                  │ │
│ └────────────────────────────────────┘ │
│                                         │
│ 💰 Công nợ hiện tại                    │
│ ┌────────────────────────────────────┐ │
│ │   350,000,000 VND                  │ │
│ └────────────────────────────────────┘ │
│                                         │
│ 📦 Lệnh xuất chưa xuất                 │
│ ┌────────────────────────────────────┐ │
│ │   100,000,000 VND                  │ │
│ └────────────────────────────────────┘ │
│                                         │
│ 📝 Đơn hiện tại                        │
│ ┌────────────────────────────────────┐ │
│ │    80,000,000 VND                  │ │
│ └────────────────────────────────────┘ │
│                                         │
├─────────────────────────────────────────┤
│ 🔢 Tổng rủi ro tín dụng                │
│ ┌────────────────────────────────────┐ │
│ │   530,000,000 VND  ❌              │ │
│ │   Vượt hạn mức: 30,000,000         │ │
│ └────────────────────────────────────┘ │
│                                         │
│ ⚡ Tín dụng khả dụng                    │
│ ┌────────────────────────────────────┐ │
│ │   -30,000,000 VND  ⚠️              │ │
│ └────────────────────────────────────┘ │
│                                         │
│ 📈 Tỷ lệ sử dụng                       │
│ ┌────────────────────────────────────┐ │
│ │   [████████████░░░] 106%  🔴       │ │
│ └────────────────────────────────────┘ │
│                                         │
├─────────────────────────────────────────┤
│ ⚠️ CẢNH BÁO                            │
│                                         │
│ ❌ Vượt hạn mức 30,000,000 VND         │
│ ⚠️ Cần Kế toán trưởng phê duyệt        │
│                                         │
│ [ 📧 Gửi yêu cầu phê duyệt ]           │
└─────────────────────────────────────────┘
```

---

### 6.2. Override Approval Popup

```
┌──────────────────────────────────────────────┐
│ PHÊ DUYỆT NGOẠI LỆ - LỆNH XUẤT #SO-2026-001│
├──────────────────────────────────────────────┤
│                                              │
│ 👤 Khách hàng: Đại lý ABC (KH-12345)       │
│ 📅 Ngày tạo: 14/01/2026 10:30              │
│ 👨‍💼 NVKD: Nguyễn Văn A                      │
│ 💵 Giá trị đơn: 80,000,000 VND             │
│                                              │
├──────────────────────────────────────────────┤
│ ⚠️ LÝ DO CHẶN                               │
│                                              │
│ ❌ Vượt hạn mức công nợ                     │
│    Vượt: 30,000,000 VND                     │
│                                              │
│ CHI TIẾT TÍN DỤNG:                          │
│ ┌──────────────────────────────────────────┐│
│ │ Hạn mức:            500,000,000 VND     ││
│ │ Công nợ hiện tại:   350,000,000 VND     ││
│ │ Lệnh xuất chưa xuất: 100,000,000 VND    ││
│ │ Đơn hiện tại:        80,000,000 VND     ││
│ │ ─────────────────────────────────────── ││
│ │ Tổng rủi ro:        530,000,000 VND  ❌ ││
│ └──────────────────────────────────────────┘│
│                                              │
│ 📋 Lý do phê duyệt (bắt buộc): *            │
│ ┌──────────────────────────────────────────┐│
│ │                                          ││
│ │  [Nhập lý do phê duyệt...]              ││
│ │                                          ││
│ └──────────────────────────────────────────┘│
│                                              │
│ [ ✅ PHÊ DUYỆT ]  [ ❌ TỪ CHỐI ]           │
│                                              │
└──────────────────────────────────────────────┘
```

---

### 6.3. Aging Report Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│ BÁO CÁO CÔNG NỢ THEO ĐỘ TUỔI (AGING REPORT)                   │
│ Ngày báo cáo: 14/01/2026                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────┬──────────┬─────┬─────┬─────┬─────┬────────────┐  │
│ │ MÃ KH   │ TÊN KH   │0-30 │31-60│61-90│ 90+ │ TỔNG CÔNG  │  │
│ │         │          │     │     │     │     │ NỢ         │  │
│ ├─────────┼──────────┼─────┼─────┼─────┼─────┼────────────┤  │
│ │ KH-001  │ Đại lý A │ 100 │  50 │  20 │  10 │ 180        │  │
│ │         │          │ ███ │ ██  │ █   │ █   │            │  │
│ ├─────────┼──────────┼─────┼─────┼─────┼─────┼────────────┤  │
│ │ KH-002  │ Đại lý B │ 200 │   0 │   0 │   0 │ 200        │  │
│ │         │          │█████│     │     │     │            │  │
│ ├─────────┼──────────┼─────┼─────┼─────┼─────┼────────────┤  │
│ │ KH-003  │ Đại lý C │  50 │ 100 │  80 │  50 │ 280        │  │
│ │         │          │ ██  │ ███ │ ███ │ ██  │ ⚠️         │  │
│ ├─────────┼──────────┼─────┼─────┼─────┼─────┼────────────┤  │
│ │ ...     │ ...      │ ... │ ... │ ... │ ... │ ...        │  │
│ ├─────────┼──────────┼─────┼─────┼─────┼─────┼────────────┤  │
│ │ TỔNG    │          │ 500 │ 150 │  50 │  30 │ 730        │  │
│ └─────────┴──────────┴─────┴─────┴─────┴─────┴────────────┘  │
│                                                                 │
│ BIỂU ĐỒ PHÂN BỐ:                                              │
│                                                                 │
│ 0-30 ngày   (68.5%) ███████████████████████████░░░░░░         │
│ 31-60 ngày  (20.5%) ████████░░░░░░░░░░░░░░░░░░░░░░░░          │
│ 61-90 ngày  ( 6.8%) ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          │
│ 90+ ngày    ( 4.1%) ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          │
│                                                                 │
│ [ 📥 Export Excel ]  [ 📧 Email Report ]                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Summary

### Diagram Count by Category

| Category | Count | Purpose |
|----------|-------|---------|
| **Process Flow** | 2 | Show business process flow |
| **Sequence** | 3 | Show interactions between actors & system |
| **State Machine** | 2 | Show status transitions |
| **Data Flow** | 2 | Show data movement |
| **Architecture** | 2 | Show system components |
| **UI Mockup** | 3 | Show user interface design |
| **TOTAL** | **14 diagrams** | Full visualization coverage |

---

### Key Insights from Diagrams

1. **Credit Check is Central:** All flows converge on credit check logic
2. **2-Stage Validation:** Overdue check → Limit check
3. **Override is Exception:** Normal flow should pass credit check
4. **Audit Trail:** Every decision is logged (state machines show this)
5. **Real-time Updates:** Cache invalidation ensures fresh data

---

**© 2025 DCNET Corporation - Powered by DCNET Cloud**
