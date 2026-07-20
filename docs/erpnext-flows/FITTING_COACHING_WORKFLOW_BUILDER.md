# Frappe Workflow Builder - Fitting & Coaching

> **Mục đích:** Thiết kế workflow cho 2 module Fitting và Coaching sử dụng Frappe Workflow Builder
> **Nguồn:** FEATURE_SPECIFICATION.md Section 16, 17
> **Ngày:** 29/01/2026

---

## 1. Tổng quan

### 1.1. Frappe Workflow Builder

Frappe Workflow Builder là tính năng **built-in** của Frappe Framework cho phép:
- ✅ Định nghĩa trạng thái và luồng chuyển đổi
- ✅ Visual UI để thiết kế workflow (drag-drop)
- ✅ Phân quyền theo Role ở mỗi trạng thái
- ✅ Điều kiện chuyển trạng thái (Python expression)
- ✅ Tự động hóa (email, webhook, server script)

### 1.2. Áp dụng cho DCNET Flow

| Module | DocType | Số trạng thái | Terminal States |
|--------|---------|---------------|-----------------|
| **Fitting** | Fitting Order | 5 | completed, cancelled |
| **Coaching** | Coaching Order | 8 | completed, cancelled |

---

## 2. FITTING WORKFLOW

### 2.1. Các trạng thái (Workflow States)

> **Nguồn:** FEATURE_SPECIFICATION.md Section 16.1.3

| # | State | Label (VI) | Doc Status | Style | Allow Edit |
|---|-------|------------|------------|-------|------------|
| 1 | `registered` | Mới đăng ký | 0 (Draft) | Primary | Sales User |
| 2 | `confirmed` | Đã xác nhận lịch | 0 (Draft) | Info | Sales User |
| 3 | `in_progress` | Đang thực hiện | 0 (Draft) | Warning | Fitting Technician |
| 4 | `completed` | Hoàn thành | 1 (Submitted) | Success | - |
| 5 | `cancelled` | Hủy | 2 (Cancelled) | Danger | - |

### 2.2. Transitions (Luồng chuyển đổi)

> **Nguồn:** FITTING_STATUS.md - Ma trận chuyển đổi

| # | From State | Action | To State | Allowed Role | Condition |
|---|------------|--------|----------|--------------|-----------|
| 1 | `registered` | Xác nhận lịch | `confirmed` | Sales User | `doc.appointment_at is not None` |
| 2 | `registered` | Hủy đơn | `cancelled` | Sales User, Sales Manager | - |
| 3 | `confirmed` | Bắt đầu fitting | `in_progress` | Fitting Technician | - |
| 4 | `confirmed` | Đổi lịch | `confirmed` | Sales User | - |
| 5 | `confirmed` | Khách không đến | `cancelled` | Sales User | - |
| 6 | `in_progress` | Hoàn thành | `completed` | Fitting Technician | `doc.technical_data is not None` |
| 7 | `in_progress` | Hủy giữa chừng | `cancelled` | Sales Manager | - |

### 2.3. Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FITTING WORKFLOW                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     Xác nhận lịch      ┌──────────────────┐               │
│  │              │  ─────────────────────> │                  │               │
│  │  REGISTERED  │                         │    CONFIRMED     │               │
│  │  (Mới đăng   │  <───────────────────── │  (Đã xác nhận    │               │
│  │    ký)       │      Đổi lịch (loop)    │     lịch)        │               │
│  │              │                         │                  │               │
│  └──────┬───────┘                         └────────┬─────────┘               │
│         │                                          │                         │
│         │ Hủy đơn                                   │ Bắt đầu fitting        │
│         │                                          │                         │
│         │                                          ▼                         │
│         │                                 ┌──────────────────┐               │
│         │                                 │                  │               │
│         │                                 │   IN_PROGRESS    │               │
│         │                                 │  (Đang thực      │               │
│         │                                 │    hiện)         │               │
│         │                                 │                  │               │
│         │                                 └────────┬─────────┘               │
│         │                                          │                         │
│         │               Khách không đến            │ Hoàn thành              │
│         │                      │                   │                         │
│         ▼                      ▼                   ▼                         │
│  ┌──────────────┐     ┌──────────────────────────────────────┐              │
│  │              │     │                                      │              │
│  │  CANCELLED   │     │           COMPLETED                  │              │
│  │   (Hủy)      │     │         (Hoàn thành)                 │              │
│  │              │     │                                      │              │
│  └──────────────┘     └──────────────────────────────────────┘              │
│   [Terminal]                    [Terminal]                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.4. Frappe Workflow Configuration

**File: `fitting_order_workflow.json`**

```json
{
  "workflow_name": "Fitting Order Workflow",
  "document_type": "Fitting Order",
  "is_active": 1,
  "override_status": 0,
  "send_email_alert": 1,
  "workflow_state_field": "workflow_state",

  "states": [
    {
      "state": "Mới đăng ký",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "style": "Primary"
    },
    {
      "state": "Đã xác nhận lịch",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "style": "Info"
    },
    {
      "state": "Đang thực hiện",
      "doc_status": "0",
      "allow_edit": "Fitting Technician",
      "style": "Warning"
    },
    {
      "state": "Hoàn thành",
      "doc_status": "1",
      "style": "Success",
      "is_optional_state": 0
    },
    {
      "state": "Hủy",
      "doc_status": "2",
      "style": "Danger"
    }
  ],

  "transitions": [
    {
      "state": "Mới đăng ký",
      "action": "Xác nhận lịch",
      "next_state": "Đã xác nhận lịch",
      "allowed": "Sales User",
      "condition": "doc.appointment_at"
    },
    {
      "state": "Mới đăng ký",
      "action": "Hủy đơn",
      "next_state": "Hủy",
      "allowed": "Sales User"
    },
    {
      "state": "Đã xác nhận lịch",
      "action": "Bắt đầu fitting",
      "next_state": "Đang thực hiện",
      "allowed": "Fitting Technician"
    },
    {
      "state": "Đã xác nhận lịch",
      "action": "Đổi lịch",
      "next_state": "Đã xác nhận lịch",
      "allowed": "Sales User"
    },
    {
      "state": "Đã xác nhận lịch",
      "action": "Khách không đến",
      "next_state": "Hủy",
      "allowed": "Sales User"
    },
    {
      "state": "Đang thực hiện",
      "action": "Hoàn thành",
      "next_state": "Hoàn thành",
      "allowed": "Fitting Technician"
    },
    {
      "state": "Đang thực hiện",
      "action": "Hủy giữa chừng",
      "next_state": "Hủy",
      "allowed": "Sales Manager"
    }
  ]
}
```

### 2.5. Roles cần thiết cho Fitting

| Role | Mô tả | Quyền |
|------|-------|-------|
| **Sales User** | Nhân viên Sale | Tạo đơn, xác nhận lịch, hủy |
| **Sales Manager** | Quản lý Sale | Duyệt hủy giữa chừng |
| **Fitting Technician** | NV Kỹ thuật Fitting | Thực hiện fitting, nhập thông số |

---

## 3. COACHING WORKFLOW

### 3.1. Các trạng thái (Workflow States)

> **Nguồn:** FEATURE_SPECIFICATION.md Section 17.1.3

| # | State | Label (VI) | Doc Status | Style | Allow Edit |
|---|-------|------------|------------|-------|------------|
| 1 | `new` | Mới | 0 (Draft) | Primary | Sales User |
| 2 | `tested` | Đã test | 0 (Draft) | Info | Coach |
| 3 | `consulted` | Đã tư vấn | 0 (Draft) | Info | Sales User |
| 4 | `paid` | Đã thanh toán | 0 (Draft) | Success | Sales User |
| 5 | `in_progress` | Đang học | 0 (Draft) | Warning | Coach |
| 6 | `paused` | Tạm dừng | 0 (Draft) | Secondary | Sales User |
| 7 | `completed` | Hoàn thành | 1 (Submitted) | Success | - |
| 8 | `cancelled` | Hủy | 2 (Cancelled) | Danger | - |

### 3.2. Transitions (Luồng chuyển đổi)

> **Nguồn:** COACHING_STATUS.md - Transition Matrix

| # | From State | Action | To State | Allowed Role | Condition |
|---|------------|--------|----------|--------------|-----------|
| 1 | `new` | Làm test đầu vào | `tested` | Coach | - |
| 2 | `new` | Khách hủy | `cancelled` | Sales User | - |
| 3 | `tested` | Tư vấn gói | `consulted` | Sales User | `doc.test_result is not None` |
| 4 | `tested` | Không phù hợp | `cancelled` | Sales Manager | - |
| 5 | `consulted` | Đăng ký & Thanh toán | `paid` | Sales User | `doc.package_id is not None` |
| 6 | `consulted` | Khách từ chối | `cancelled` | Sales User | - |
| 7 | `paid` | Bắt đầu khóa học | `in_progress` | Coach | `doc.sessions_created == 1` |
| 8 | `in_progress` | Xin nghỉ tạm | `paused` | Sales User, Coach | - |
| 9 | `in_progress` | Hoàn thành khóa | `completed` | Coach | `doc.completed_sessions == doc.total_sessions` |
| 10 | `paused` | Học tiếp | `in_progress` | Sales User | - |
| 11 | `paused` | Hủy (quá hạn) | `cancelled` | Sales Manager | - |

### 3.3. Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COACHING WORKFLOW                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐   Làm test    ┌──────────┐   Tư vấn    ┌──────────┐          │
│  │          │ ────────────> │          │ ──────────> │          │          │
│  │   NEW    │               │  TESTED  │             │CONSULTED │          │
│  │  (Mới)   │               │ (Đã test)│             │(Đã tư vấn)│          │
│  │          │               │          │             │          │          │
│  └────┬─────┘               └────┬─────┘             └────┬─────┘          │
│       │                          │                        │                 │
│       │ Khách hủy                │ Không phù hợp          │ Đăng ký &       │
│       │                          │                        │ Thanh toán      │
│       │                          │                        │                 │
│       │                          │                        ▼                 │
│       │                          │                   ┌──────────┐          │
│       │                          │                   │          │          │
│       │                          │                   │   PAID   │          │
│       │                          │                   │(Đã thanh │          │
│       │                          │                   │   toán)  │          │
│       │                          │                   │          │          │
│       │                          │                   └────┬─────┘          │
│       │                          │                        │                 │
│       │                          │                        │ Bắt đầu         │
│       │                          │                        │ khóa học        │
│       │                          │                        ▼                 │
│       │                          │                   ┌──────────┐          │
│       │                          │       Xin nghỉ    │          │  Hoàn    │
│       │                          │    ┌────────────> │IN_PROGRESS│  thành   │
│       │                          │    │              │(Đang học)│ ────────>│
│       │                          │    │              │          │          │
│       │                          │    │              └────┬─────┘          │
│       │                          │    │                   │                 │
│       │                          │    │                   │ Xin nghỉ tạm    │
│       │                          │    │                   ▼                 │
│       │                          │    │              ┌──────────┐          │
│       │                          │    │  Học tiếp    │          │          │
│       │                          │    └───────────── │  PAUSED  │          │
│       │                          │                   │(Tạm dừng)│          │
│       │                          │                   │          │          │
│       │                          │                   └────┬─────┘          │
│       │                          │                        │                 │
│       │         Khách từ chối    │     Hủy (quá hạn)      │                 │
│       │              │           │          │             │                 │
│       ▼              ▼           ▼          ▼             │                 │
│  ┌──────────────────────────────────────────────────┐    │                 │
│  │                                                  │    │                 │
│  │                   CANCELLED                      │<───┘                 │
│  │                    (Hủy)                         │                      │
│  │                                                  │                      │
│  └──────────────────────────────────────────────────┘                      │
│   [Terminal]                                                                │
│                                                                              │
│                                              ┌──────────────────────────┐   │
│                                              │                          │   │
│                                              │       COMPLETED          │   │
│                                              │     (Hoàn thành)         │   │
│                                              │                          │   │
│                                              └──────────────────────────┘   │
│                                               [Terminal]                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.4. Frappe Workflow Configuration

**File: `coaching_order_workflow.json`**

```json
{
  "workflow_name": "Coaching Order Workflow",
  "document_type": "Coaching Order",
  "is_active": 1,
  "override_status": 0,
  "send_email_alert": 1,
  "workflow_state_field": "workflow_state",

  "states": [
    {
      "state": "Mới",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "style": "Primary"
    },
    {
      "state": "Đã test",
      "doc_status": "0",
      "allow_edit": "Coach",
      "style": "Info"
    },
    {
      "state": "Đã tư vấn",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "style": "Info"
    },
    {
      "state": "Đã thanh toán",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "style": "Success"
    },
    {
      "state": "Đang học",
      "doc_status": "0",
      "allow_edit": "Coach",
      "style": "Warning"
    },
    {
      "state": "Tạm dừng",
      "doc_status": "0",
      "allow_edit": "Sales User",
      "style": "Secondary"
    },
    {
      "state": "Hoàn thành",
      "doc_status": "1",
      "style": "Success"
    },
    {
      "state": "Hủy",
      "doc_status": "2",
      "style": "Danger"
    }
  ],

  "transitions": [
    {
      "state": "Mới",
      "action": "Làm test đầu vào",
      "next_state": "Đã test",
      "allowed": "Coach"
    },
    {
      "state": "Mới",
      "action": "Khách hủy",
      "next_state": "Hủy",
      "allowed": "Sales User"
    },
    {
      "state": "Đã test",
      "action": "Tư vấn gói",
      "next_state": "Đã tư vấn",
      "allowed": "Sales User",
      "condition": "doc.test_result"
    },
    {
      "state": "Đã test",
      "action": "Không phù hợp",
      "next_state": "Hủy",
      "allowed": "Sales Manager"
    },
    {
      "state": "Đã tư vấn",
      "action": "Đăng ký & Thanh toán",
      "next_state": "Đã thanh toán",
      "allowed": "Sales User",
      "condition": "doc.package"
    },
    {
      "state": "Đã tư vấn",
      "action": "Khách từ chối",
      "next_state": "Hủy",
      "allowed": "Sales User"
    },
    {
      "state": "Đã thanh toán",
      "action": "Bắt đầu khóa học",
      "next_state": "Đang học",
      "allowed": "Coach"
    },
    {
      "state": "Đang học",
      "action": "Xin nghỉ tạm",
      "next_state": "Tạm dừng",
      "allowed": "Sales User,Coach"
    },
    {
      "state": "Đang học",
      "action": "Hoàn thành khóa",
      "next_state": "Hoàn thành",
      "allowed": "Coach",
      "condition": "doc.completed_sessions == doc.total_sessions"
    },
    {
      "state": "Tạm dừng",
      "action": "Học tiếp",
      "next_state": "Đang học",
      "allowed": "Sales User"
    },
    {
      "state": "Tạm dừng",
      "action": "Hủy (quá hạn)",
      "next_state": "Hủy",
      "allowed": "Sales Manager"
    }
  ]
}
```

### 3.5. Roles cần thiết cho Coaching

| Role | Mô tả | Quyền |
|------|-------|-------|
| **Sales User** | Nhân viên Sale | Tạo đơn, tư vấn, thanh toán |
| **Sales Manager** | Quản lý Sale | Duyệt hủy, xử lý ngoại lệ |
| **Coach** | Huấn luyện viên | Test, dạy học, điểm danh |

---

## 4. Triển khai Workflow

### 4.1. Bước 1: Tạo Workflow States

**Đường dẫn:** Setup > Workflow > Workflow State

| State Name (VI) | Style |
|-----------------|-------|
| Mới đăng ký | Primary |
| Đã xác nhận lịch | Info |
| Đang thực hiện | Warning |
| Hoàn thành | Success |
| Hủy | Danger |
| Mới | Primary |
| Đã test | Info |
| Đã tư vấn | Info |
| Đã thanh toán | Success |
| Đang học | Warning |
| Tạm dừng | Secondary |

### 4.2. Bước 2: Tạo Workflow Actions

**Đường dẫn:** Setup > Workflow > Workflow Action Master

**Fitting:**
- Xác nhận lịch
- Hủy đơn
- Bắt đầu fitting
- Đổi lịch
- Khách không đến
- Hoàn thành
- Hủy giữa chừng

**Coaching:**
- Làm test đầu vào
- Khách hủy
- Tư vấn gói
- Không phù hợp
- Đăng ký & Thanh toán
- Khách từ chối
- Bắt đầu khóa học
- Xin nghỉ tạm
- Hoàn thành khóa
- Học tiếp
- Hủy (quá hạn)

### 4.3. Bước 3: Tạo Workflow

**Đường dẫn:** Setup > Workflow > Workflow

1. **New Workflow** > Fitting Order Workflow
   - Document Type: Fitting Order
   - Is Active: Yes
   - Thêm States và Transitions như config ở trên

2. **New Workflow** > Coaching Order Workflow
   - Document Type: Coaching Order
   - Is Active: Yes
   - Thêm States và Transitions như config ở trên

### 4.4. Bước 4: Sử dụng Workflow Builder (Visual)

**Đường dẫn:** `/app/workflow-builder/{workflow_name}`

1. Mở Workflow Builder
2. Drag-drop các State nodes
3. Kết nối các transitions
4. Configure điều kiện và roles
5. Save

---

## 5. Automation với Workflow

### 5.1. Email Notifications

**Fitting - Nhắc lịch hẹn:**

```python
# Workflow Transition: confirmed
# Send Email Alert: Yes

# Email Template: Fitting Appointment Reminder
Subject: [DCNET Flow] Xác nhận lịch hẹn Fitting - {{ doc.code }}

Kính gửi {{ doc.customer_name }},

Chúng tôi xác nhận lịch hẹn Fitting của bạn:
- Mã đơn: {{ doc.code }}
- Thời gian: {{ doc.appointment_at }}
- Chi nhánh: {{ doc.branch }}
- NV phụ trách: {{ doc.fitter_name }}

Vui lòng đến đúng giờ. Nếu cần đổi lịch, vui lòng liên hệ hotline.

Trân trọng,
DCNET Flow Team
```

**Coaching - Nhắc buổi học:**

```python
# Server Script: Before Save
# Trigger: scheduled_at - 1 day

Subject: [DCNET Flow] Nhắc lịch học Golf - {{ doc.code }}

Kính gửi {{ doc.student_name }},

Bạn có buổi học Golf vào ngày mai:
- Khóa học: {{ doc.package_name }}
- Buổi thứ: {{ doc.current_session }}/{{ doc.total_sessions }}
- Thời gian: {{ doc.next_session_at }}
- HLV: {{ doc.coach_name }}
- Sân tập: {{ doc.golf_course }}

Trân trọng,
DCNET Flow Team
```

### 5.2. Automation Tasks

**Fitting - Tự động tạo từ Website:**

```python
# hooks.py
doc_events = {
    "Fitting Order": {
        "after_insert": "dcnet_apps.fitting.auto_notify_sale"
    }
}

# fitting.py
def auto_notify_sale(doc, method):
    if doc.source == "website":
        # Gửi notification cho Sale team
        frappe.publish_realtime(
            event="new_fitting_order",
            message={"fitting_id": doc.name, "customer": doc.customer_name},
            user=doc.assigned_sale or "Sales User"
        )
```

**Coaching - Tự động hoàn thành:**

```python
# hooks.py
doc_events = {
    "Coaching Session": {
        "on_update": "dcnet_apps.coaching.check_course_completion"
    }
}

# coaching.py
def check_course_completion(doc, method):
    if doc.status == "completed":
        coaching_order = frappe.get_doc("Coaching Order", doc.coaching_order)
        completed = frappe.db.count("Coaching Session", {
            "coaching_order": doc.coaching_order,
            "status": "completed"
        })

        if completed >= coaching_order.total_sessions:
            # Tự động suggest hoàn thành
            frappe.msgprint(
                f"Học viên đã hoàn thành {completed}/{coaching_order.total_sessions} buổi. "
                "Vui lòng click 'Hoàn thành khóa' để kết thúc."
            )
```

---

## 6. UI Preview - Workflow trên Form

### 6.1. Fitting Order Form

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Fitting Order: FIT-20260129-001                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Status: [🔵 Mới đăng ký]                                                   │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                                   │
│  │ Xác nhận lịch   │  │    Hủy đơn      │                                   │
│  └─────────────────┘  └─────────────────┘                                   │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Khách hàng: Nguyễn Văn A                                                   │
│  SĐT: 0912345678                                                            │
│  Lịch hẹn: 30/01/2026 14:00                                                 │
│  Chi nhánh: Showroom Hà Nội                                                 │
│  NV Fitting: Trần Văn B                                                     │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  📋 Workflow History:                                                        │
│  • 29/01/2026 10:00 - Tạo đơn từ Website (Admin)                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2. Coaching Order Form

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Coaching Order: COACH-20260129-001                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Status: [🟠 Đang học]                     Progress: ████████░░ 8/10 buổi   │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                                   │
│  │  Xin nghỉ tạm   │  │  Hoàn thành khóa │ (disabled - chưa đủ buổi)       │
│  └─────────────────┘  └─────────────────┘                                   │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Học viên: Lê Thị C                                                         │
│  Gói học: 10 buổi cơ bản                                                    │
│  HLV: Nguyễn Văn D                                                          │
│  Sân tập: Sân Golf ABC                                                      │
│  Học phí: 15,000,000 VND (Đã TT: 15,000,000)                               │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  📋 Workflow History:                                                        │
│  • 29/01/2026 - Đang học (Coach: Nguyễn Văn D)                             │
│  • 25/01/2026 - Đã thanh toán (Sales: Trần Thị E)                          │
│  • 24/01/2026 - Đã tư vấn (Sales: Trần Thị E)                              │
│  • 23/01/2026 - Đã test (Coach: Nguyễn Văn D)                              │
│  • 22/01/2026 - Tạo đơn mới (Sales: Trần Thị E)                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Lợi ích khi sử dụng Workflow Builder

### 7.1. Cho Quản lý

| Lợi ích | Mô tả |
|---------|-------|
| **Visibility** | Nhìn thấy trạng thái tất cả đơn |
| **Control** | Kiểm soát ai làm gì ở bước nào |
| **Audit Trail** | Lịch sử đầy đủ mọi thay đổi |
| **Reporting** | Báo cáo theo từng trạng thái |

### 7.2. Cho Nhân viên

| Lợi ích | Mô tả |
|---------|-------|
| **Clarity** | Biết rõ công việc cần làm |
| **Automation** | Hệ thống tự nhắc lịch, gửi email |
| **Error Prevention** | Không thể bỏ qua bước bắt buộc |
| **Mobile** | Làm việc trên điện thoại |

### 7.3. Cho Khách hàng

| Lợi ích | Mô tả |
|---------|-------|
| **Transparency** | Biết đơn đang ở đâu |
| **Notifications** | Nhận nhắc lịch tự động |
| **Consistency** | Trải nghiệm đồng nhất |

---

## 8. Demo cho Khách hàng

### 8.1. Script Demo Fitting

```
1. [Sale] Tạo đơn Fitting mới từ website
   → Hệ thống tự động gửi thông báo cho Sale
   → Status: "Mới đăng ký"

2. [Sale] Click "Xác nhận lịch" sau khi gọi khách
   → Chọn lịch hẹn, phân công NV Fitting
   → Status: "Đã xác nhận lịch"
   → Hệ thống gửi email nhắc lịch cho khách

3. [NV Fitting] Khách đến, click "Bắt đầu fitting"
   → Status: "Đang thực hiện"
   → Mở form nhập thông số kỹ thuật

4. [NV Fitting] Nhập thông số, click "Hoàn thành"
   → Status: "Hoàn thành"
   → Hỏi: Khách có muốn mua grip/shaft không?
   → Nếu có: Tạo Sales Order liên kết
```

### 8.2. Script Demo Coaching

```
1. [Sale] Tạo đơn Coaching cho học viên mới
   → Status: "Mới"

2. [HLV] Thực hiện bài test đầu vào
   → Nhập kết quả test
   → Click "Làm test đầu vào"
   → Status: "Đã test"

3. [Sale] Tư vấn gói học phù hợp
   → Chọn gói: "10 buổi cơ bản"
   → Click "Tư vấn gói"
   → Status: "Đã tư vấn"

4. [Sale] Học viên đồng ý, thanh toán
   → Tạo Order, ghi nhận thanh toán
   → Click "Đăng ký & Thanh toán"
   → Status: "Đã thanh toán"

5. [HLV] Bắt đầu khóa học
   → Tạo 10 buổi học trong hệ thống
   → Click "Bắt đầu khóa học"
   → Status: "Đang học"
   → Hệ thống nhắc lịch từng buổi

6. [HLV] Sau 10 buổi, click "Hoàn thành khóa"
   → Status: "Hoàn thành"
   → Hệ thống gợi ý: Đăng ký khóa tiếp?
```

---

## 9. References

- **Nguồn spec:** FEATURE_SPECIFICATION.md Section 16, 17
- **Status definitions:** FITTING_STATUS.md, COACHING_STATUS.md
- **Frappe Workflow docs:** https://frappeframework.com/docs/user/en/automation/workflow

---

**Ngày tạo:** 29/01/2026
**Người tạo:** DCNET Development Team
**Trạng thái:** Chờ review & phê duyệt từ khách hàng
