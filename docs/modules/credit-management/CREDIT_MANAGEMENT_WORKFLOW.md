# Module Credit Management - Workflow & Data Flow

> **Phiên bản**: v1.0
> **Ngày cập nhật**: 2026-01-14
> **Nguồn**: ERP_SPECIFICATION.md Section 2.6-2.8

---

## 📊 Tổng quan Workflow

### Business Process Overview

```mermaid
graph LR
    A[Manager<br/>Set Credit Limit] --> B[NVKD<br/>Tạo Lệnh xuất]
    B --> C{System<br/>Credit Check}
    C -->|Pass| D[Approved<br/>Sẵn sàng xuất]
    C -->|Fail| E[Pending Override<br/>Cần duyệt]
    E --> F{Kế toán trưởng<br/>Review}
    F -->|Approve| D
    F -->|Reject| G[Rejected<br/>Từ chối]
    D --> H[Kho<br/>Xuất hàng]
    H --> I[Fulfilled<br/>Hoàn thành]
    G --> J[End]
    I --> J
```

### Key Components

| Component | Mô tả | Owner |
|-----------|-------|-------|
| **Credit Limit** | Hạn mức tín dụng cho KH | Manager |
| **Credit Check** | Kiểm tra tự động khi tạo lệnh xuất | System |
| **Override Approval** | Phê duyệt ngoại lệ | Kế toán trưởng |
| **Credit Reservation** | Giữ hạn mức khi approved | System |

---

## 🔄 Workflow Chi tiết

### Workflow 1: Cập nhật Hạn mức công nợ

**Nguồn:** ERP_SPECIFICATION.md line 137-150

```mermaid
sequenceDiagram
    actor Manager
    participant UI as Credit Limit UI
    participant System
    participant DB as Database

    Manager->>UI: Vào "Hạn mức công nợ"
    UI->>System: Get customer list
    System->>DB: SELECT customers
    DB-->>System: Customer data
    System-->>UI: Show list

    Manager->>UI: Click "Tạo mới"
    UI-->>Manager: Show form

    Manager->>UI: Fill form:<br/>- Customer<br/>- Credit limit<br/>- Effective date<br/>- Attachment
    Manager->>UI: Click "Lưu"

    UI->>System: Validate & Save

    alt Valid
        System->>DB: INSERT credit_limit
        DB-->>System: Success
        System-->>UI: "✅ Cập nhật thành công"
        UI-->>Manager: Show success message
    else Invalid
        System-->>UI: "❌ Lỗi: [reason]"
        UI-->>Manager: Show error
    end
```

**Input:**
- Mã khách hàng
- Giá trị hạn mức (VND)
- Ngày áp dụng
- Tài khoản công nợ
- File đính kèm (optional)

**Output:**
- Credit limit record created
- Áp dụng cho tất cả lệnh xuất từ ngày hiệu lực

**Business Rules:**
- Hạn mức phải > 0
- Một KH chỉ có 1 hạn mức active tại 1 thời điểm
- Hạn mức mới override hạn mức cũ (theo effective_date)

---

### Workflow 2: Tạo Lệnh xuất hàng với Credit Check

**Nguồn:** ERP_SPECIFICATION.md line 110-134, 152-162

#### Step 1: Tạo lệnh xuất

```mermaid
sequenceDiagram
    actor NVKD
    participant UI as Sales Order UI
    participant System
    participant CreditEngine as Credit Check Engine
    participant DB as Database

    NVKD->>UI: Vào "Đơn hàng" → "Tạo lệnh xuất"
    UI->>System: Load order data
    System->>DB: Get order details
    DB-->>System: Order data
    System-->>UI: Pre-fill form

    par Load Credit Info
        UI->>System: Get credit info (customer_id)
        System->>DB: Get credit data:<br/>- Credit limit<br/>- Current debt<br/>- Pending orders
        DB-->>System: Credit data
        System-->>UI: Display credit panel
    end

    Note over UI: Credit Info Panel shows:<br/>- Hạn mức: 500M<br/>- Công nợ: 350M<br/>- Pending: 100M<br/>- Available: 50M

    NVKD->>UI: Review & edit items
    NVKD->>UI: Click "Lưu"

    UI->>System: Submit order
    System->>CreditEngine: check_credit(customer, order_value)
```

#### Step 2: Credit Check Logic

```mermaid
flowchart TD
    Start([Credit Check Start]) --> GetData[Load Customer Data]

    GetData --> Check1{Có hóa đơn<br/>quá hạn?}

    Check1 -->|Có| OverdueFound[Found overdue invoices]
    Check1 -->|Không| Check2{Vượt<br/>hạn mức?}

    OverdueFound --> CalcOverdue[Calculate:<br/>- Số lượng HĐ quá hạn<br/>- Tổng giá trị quá hạn<br/>- Số ngày quá hạn TB]
    CalcOverdue --> BuildResult1[Build result:<br/>status = pending_override<br/>reason = overdue]
    BuildResult1 --> ReturnFail[Return FAIL]

    Check2 -->|Có| CalcExposure[Calculate:<br/>total_exposure =<br/>current_debt +<br/>pending_orders +<br/>order_value]
    CalcExposure --> CompareLimit{total_exposure ><br/>credit_limit?}

    CompareLimit -->|Yes| BuildResult2[Build result:<br/>status = pending_override<br/>reason = exceed_limit<br/>exceed_amount]
    BuildResult2 --> ReturnFail

    CompareLimit -->|No| Check2
    Check2 -->|Không| CalcAvailable[Calculate:<br/>available_credit =<br/>credit_limit -<br/>total_exposure]
    CalcAvailable --> BuildResult3[Build result:<br/>status = approved<br/>available_credit]
    BuildResult3 --> ReturnPass[Return PASS]

    ReturnPass --> End([Credit Check End])
    ReturnFail --> End

    style Check1 fill:#fff4e6
    style Check2 fill:#fff4e6
    style ReturnPass fill:#d4edda
    style ReturnFail fill:#f8d7da
```

**Code Logic:**
```python
def check_credit(customer_id, order_value):
    """
    2 điều kiện bắt buộc (ERP_SPECIFICATION.md line 158-161):
    1. Không có hóa đơn quá hạn
    2. (Current Debt + Pending + Order) ≤ Credit Limit
    """

    # Step 1: Check overdue invoices
    overdue = frappe.db.sql("""
        SELECT name, due_date, outstanding_amount,
               DATEDIFF(CURDATE(), due_date) as overdue_days
        FROM `tabSales Invoice`
        WHERE customer = %s
          AND due_date < CURDATE()
          AND outstanding_amount > 0
          AND docstatus = 1
    """, customer_id, as_dict=True)

    if overdue:
        return {
            "status": "pending_override",
            "reason": "overdue_invoices",
            "overdue_count": len(overdue),
            "overdue_amount": sum(inv.outstanding_amount for inv in overdue),
            "overdue_list": overdue
        }

    # Step 2: Check credit limit
    credit_data = frappe.db.get_value(
        "Credit Limit",
        {"customer": customer_id, "status": "Active"},
        ["credit_limit", "effective_date"],
        as_dict=True
    )

    if not credit_data:
        return {
            "status": "pending_override",
            "reason": "no_credit_limit",
            "message": "Khách hàng chưa có hạn mức tín dụng"
        }

    # Get current debt
    current_debt = frappe.db.sql("""
        SELECT SUM(outstanding_amount) as total
        FROM `tabSales Invoice`
        WHERE customer = %s
          AND docstatus = 1
          AND outstanding_amount > 0
    """, customer_id)[0][0] or 0

    # Get pending orders (approved but not shipped)
    pending_orders = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabSales Order`
        WHERE customer = %s
          AND status = 'Approved'
          AND docstatus = 1
    """, customer_id)[0][0] or 0

    # Calculate total exposure
    total_exposure = current_debt + pending_orders + order_value
    credit_limit = credit_data.credit_limit

    if total_exposure > credit_limit:
        return {
            "status": "pending_override",
            "reason": "exceed_limit",
            "credit_limit": credit_limit,
            "current_debt": current_debt,
            "pending_orders": pending_orders,
            "current_order": order_value,
            "total_exposure": total_exposure,
            "exceed_amount": total_exposure - credit_limit
        }

    # Pass all checks
    available_credit = credit_limit - total_exposure
    return {
        "status": "approved",
        "reason": "pass",
        "available_credit": available_credit,
        "credit_utilization": (total_exposure / credit_limit * 100) if credit_limit > 0 else 0
    }
```

#### Step 3: Handle Check Result

```mermaid
sequenceDiagram
    participant CreditEngine
    participant System
    participant UI
    participant NotificationService
    actor NVKD
    actor KeToanTruong as Kế toán trưởng

    CreditEngine-->>System: Return check result

    alt Result = PASS (approved)
        System->>System: Set status = approved
        System->>System: Reserve credit
        System->>DB: UPDATE sales_order<br/>SET status = 'Approved'
        System-->>UI: Success response
        UI-->>NVKD: Show "✅ Đã duyệt"

    else Result = FAIL (pending_override)
        System->>System: Set status = pending_override
        System->>DB: UPDATE sales_order<br/>SET status = 'Pending Override'<br/>credit_check_result = JSON

        System->>NotificationService: Send email to approver
        NotificationService->>KeToanTruong: 📧 Email:<br/>"Cần phê duyệt lệnh xuất #SO-xxx"

        System-->>UI: Warning response
        UI-->>NVKD: Show popup:<br/>"⚠️ Không đủ điều kiện xuất hàng<br/>Đã gửi yêu cầu phê duyệt"
    end
```

---

### Workflow 3: Override Approval (Phê duyệt ngoại lệ)

**Nguồn:** ERP_SPECIFICATION.md line 158-162

```mermaid
sequenceDiagram
    actor KeToanTruong as Kế toán trưởng
    participant Email
    participant UI as Approval UI
    participant System
    participant DB
    participant NotificationService
    actor NVKD

    Email->>KeToanTruong: 📧 "Cần phê duyệt lệnh xuất #SO-2026"
    KeToanTruong->>Email: Click link

    Email->>UI: Navigate to approval page
    UI->>System: Get pending orders
    System->>DB: SELECT * FROM sales_order<br/>WHERE status = 'Pending Override'
    DB-->>System: Order list
    System-->>UI: Display list

    KeToanTruong->>UI: Click order #SO-2026
    UI->>System: Get order details
    System->>DB: SELECT * with credit_check_result
    DB-->>System: Full details
    System-->>UI: Show popup with:<br/>- Customer info<br/>- Reason (overdue/exceed)<br/>- Credit details<br/>- Input: reason field

    KeToanTruong->>KeToanTruong: Review information

    alt Decision: APPROVE
        KeToanTruong->>UI: Enter reason<br/>Click "Phê duyệt"
        UI->>System: approve_override(order_id, reason)

        System->>DB: UPDATE sales_order SET<br/>status = 'Approved',<br/>override_approved_by = user_id,<br/>override_reason = reason,<br/>override_at = NOW()

        System->>System: Reserve credit
        System->>DB: Log audit trail

        System->>NotificationService: Notify NVKD
        NotificationService->>NVKD: 🔔 "✅ Lệnh xuất #SO-2026 đã được duyệt"

        System-->>UI: Success
        UI-->>KeToanTruong: "✅ Đã phê duyệt"

    else Decision: REJECT
        KeToanTruong->>UI: Enter reason<br/>Click "Từ chối"
        UI->>System: reject_override(order_id, reason)

        System->>DB: UPDATE sales_order SET<br/>status = 'Rejected',<br/>override_approved_by = user_id,<br/>override_reason = reason,<br/>override_at = NOW()

        System->>DB: Log audit trail

        System->>NotificationService: Notify NVKD
        NotificationService->>NVKD: 🔔 "❌ Lệnh xuất #SO-2026 bị từ chối:<br/>[reason]"

        System-->>UI: Success
        UI-->>KeToanTruong: "✅ Đã từ chối"
    end
```

**Business Rules:**
- Chỉ Kế toán trưởng có quyền override
- Bắt buộc nhập lý do (audit trail)
- Mỗi lệnh xuất chỉ được xem xét 1 lần
- Log đầy đủ: who, when, why

---

## 📊 Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    CUSTOMER ||--o{ CREDIT_LIMIT : has
    CUSTOMER ||--o{ SALES_ORDER : places
    CUSTOMER ||--o{ SALES_INVOICE : receives

    SALES_ORDER ||--|| CREDIT_CHECK_RESULT : contains
    SALES_ORDER }o--|| USER : "approved by"

    CREDIT_LIMIT {
        int id PK
        int customer_id FK
        decimal credit_limit
        date effective_date
        date expiry_date
        string account_code
        int approved_by FK
        string attachment
        enum status
        timestamp created_at
    }

    CUSTOMER {
        int id PK
        string customer_code
        string customer_name
        string customer_group
        enum payment_terms
        int payment_period_days
    }

    SALES_ORDER {
        int id PK
        string order_number
        int customer_id FK
        decimal grand_total
        enum status
        json credit_check_result
        int override_approved_by FK
        text override_reason
        timestamp override_at
        timestamp created_at
    }

    SALES_INVOICE {
        int id PK
        string invoice_number
        int customer_id FK
        date invoice_date
        date due_date
        decimal grand_total
        decimal outstanding_amount
        int overdue_days
        enum aging_bucket
    }

    USER {
        int id PK
        string email
        string full_name
        enum role
    }
```

---

## 🔄 State Transition Matrix

| From State | Event | To State | Condition | Actor |
|------------|-------|----------|-----------|-------|
| - | Create | `draft` | Always | NVKD |
| `draft` | Save | `credit_checking` | Always | System |
| `credit_checking` | Pass check | `approved` | No overdue + Within limit | System |
| `credit_checking` | Fail check | `pending_override` | Overdue OR Exceed limit | System |
| `pending_override` | Approve | `approved` | Kế toán trưởng approve | Kế toán trưởng |
| `pending_override` | Reject | `rejected` | Kế toán trưởng reject | Kế toán trưởng |
| `approved` | Ship | `fulfilled` | Kho xuất hàng | Kho |
| `approved` | Cancel | `cancelled` | User cancel | NVKD/Manager |
| `draft` | Cancel | `cancelled` | User cancel | NVKD |

---

## 📈 Data Flow Diagram (Level 1)

```mermaid
flowchart TB
    subgraph Actors
        Manager[Manager]
        NVKD[NVKD]
        KeToan[Kế toán trưởng]
        Kho[Kho]
    end

    subgraph Processes["PROCESSES"]
        P1[1.0<br/>Quản lý<br/>Hạn mức]
        P2[2.0<br/>Tạo & Check<br/>Lệnh xuất]
        P3[3.0<br/>Phê duyệt<br/>Override]
        P4[4.0<br/>Xuất hàng<br/>& Ghi nhận]
    end

    subgraph DataStores["DATA STORES"]
        D1[(D1: Credit Limit)]
        D2[(D2: Sales Order)]
        D3[(D3: Sales Invoice)]
        D4[(D4: Audit Log)]
    end

    Manager -->|Credit limit data| P1
    P1 -->|Store| D1

    NVKD -->|Order request| P2
    D1 -->|Read credit info| P2
    D3 -->|Check overdue| P2
    D2 -->|Check pending| P2
    P2 -->|Save order| D2

    P2 -.->|If fail| P3
    KeToan -->|Decision| P3
    D2 -->|Read order| P3
    P3 -->|Update status| D2
    P3 -->|Log| D4

    P2 -.->|If pass| P4
    P3 -.->|If approved| P4
    Kho -->|Ship confirmation| P4
    D2 -->|Read order| P4
    P4 -->|Update status| D2
    P4 -->|Create invoice| D3

    style P2 fill:#fff4e6
    style P3 fill:#ffe4e4
```

---

## 🎯 Integration Points

### 1. Integration với Đơn hàng bán (Sales Order)

**Trigger:** Khi tạo "Lệnh xuất hàng" từ Sales Order

**Data Flow:**
```
Sales Order → Lệnh xuất hàng
├── Copy: customer_id, items, quantities, prices
├── Trigger: Credit Check
└── Update: Sales Order status based on credit check result
```

**Hook Point:** `before_save` event của Sales Order DocType

---

### 2. Integration với Hóa đơn bán hàng (Sales Invoice)

**Trigger:** Khi tạo Sales Invoice

**Data Flow:**
```
Sales Invoice Created/Paid
├── Update: Current Debt
├── Update: Overdue Status
└── Release: Reserved Credit (if invoice is paid)
```

**Hook Points:**
- `on_submit`: Tăng current debt
- `on_payment`: Giảm current debt, check if overdue cleared

---

### 3. Integration với Phiếu thu tiền (Payment Entry)

**Trigger:** Khi nhận thanh toán từ KH

**Data Flow:**
```
Payment Entry
├── Decrease: Current Debt
├── Clear: Overdue status (if applicable)
└── Recalculate: Available Credit
```

**Hook Point:** `on_submit` event của Payment Entry

---

## 📊 Performance Considerations

### Caching Strategy

```python
# Cache credit info to avoid repeated queries
def get_customer_credit_cached(customer_id):
    cache_key = f"credit_info:{customer_id}"
    cached = frappe.cache().get(cache_key)

    if cached:
        return cached

    # Calculate fresh data
    credit_info = calculate_credit_info(customer_id)

    # Cache for 5 minutes
    frappe.cache().setex(cache_key, 300, credit_info)

    return credit_info

# Invalidate cache when relevant data changes
def invalidate_credit_cache(customer_id):
    cache_key = f"credit_info:{customer_id}"
    frappe.cache().delete(cache_key)
```

**Cache invalidation triggers:**
- Sales Invoice created/updated
- Payment Entry created
- Credit Limit updated
- Sales Order status changed

---

### Database Indexing

```sql
-- Optimize overdue invoice queries
CREATE INDEX idx_invoice_overdue
ON `tabSales Invoice` (customer, due_date, outstanding_amount, docstatus);

-- Optimize pending order queries
CREATE INDEX idx_order_pending
ON `tabSales Order` (customer, status, docstatus);

-- Optimize credit limit lookup
CREATE INDEX idx_credit_limit_active
ON `tabCredit Limit` (customer, status, effective_date);
```

---

## 🔐 Security & Audit

### Audit Trail

**Log these events:**
- Credit limit created/updated
- Credit check performed (pass/fail)
- Override approved/rejected
- Credit reserved/released

**Log format:**
```json
{
  "timestamp": "2026-01-14T10:30:00Z",
  "event_type": "override_approved",
  "user_id": 123,
  "user_email": "ketoan@nhatminh.com",
  "sales_order": "SO-2026-001",
  "customer": "KH-12345",
  "reason": "Khách hàng VIP, có cam kết thanh toán trong tuần",
  "credit_data": {
    "credit_limit": 500000000,
    "total_exposure": 530000000,
    "exceed_amount": 30000000
  }
}
```

### Role-based Access Control

| Action | NVKD | Manager | Kế toán | Kế toán trưởng |
|--------|------|---------|---------|----------------|
| View credit info (own customers) | ✅ | ✅ | ✅ | ✅ |
| View credit info (all customers) | ❌ | ✅ | ✅ | ✅ |
| Create sales order | ✅ | ✅ | ❌ | ✅ |
| Update credit limit | ❌ | ✅ | ❌ | ✅ |
| Override credit check | ❌ | ❌ | ❌ | ✅ |
| View audit log | ❌ | ✅ | ✅ | ✅ |

---

## 📝 Key Takeaways

### 1. Tại sao cần Credit Management?

**Vấn đề:**
- Bán chịu cho đại lý → Rủi ro nợ xấu cao
- Không kiểm soát → Mất vốn, dòng tiền khó khăn

**Giải pháp:**
- Set credit limit
- Auto-check trước khi xuất hàng
- Override workflow cho exceptions

---

### 2. 2 điều kiện xuất hàng

```python
✅ Điều kiện 1: Không có hóa đơn quá hạn
✅ Điều kiện 2: (Current Debt + Pending + Order) ≤ Credit Limit
```

---

### 3. Best Practices

**DO:**
- ✅ Set credit limit cho tất cả khách hàng đại lý
- ✅ Review credit limit định kỳ (quarterly)
- ✅ Monitor aging report hàng tuần
- ✅ Log đầy đủ override decisions

**DON'T:**
- ❌ Skip credit check (ngay cả KH VIP)
- ❌ Override mà không ghi lý do
- ❌ Set credit limit quá cao ban đầu
- ❌ Bỏ qua cảnh báo hóa đơn quá hạn

---

**© 2025 DCNET Corporation - Powered by DCNET Cloud**
