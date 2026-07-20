# Shipping Module - Specification

> **Module:** Quản lý Giao vận (Shipping Management)
>
> **Giai đoạn:** Bàn giao đợt 2
>
> **Nguồn:** FEATURE_SPECIFICATION.md Section 9

---

## Section Mapping Table

| Section | Nội dung | Nguồn | Line | Status |
|---------|----------|-------|------|--------|
| 9.1 | Danh sách Đơn giao vận | FEATURE_SPECIFICATION.md | 803-809 | ✅ |
| 9.2 | Liên kết với đơn vị Viettel Post | FEATURE_SPECIFICATION.md | 810-818 | ✅ |

---

## 1. Tổng quan Module

### 1.1. Định nghĩa

Module quản lý giao vận cho phép:
- Theo dõi đơn giao vận
- Tích hợp với đơn vị vận chuyển (Viettel Post)
- Đồng bộ thông tin vận đơn tự động
- Xử lý trạng thái đổi/trả hàng

**Nguồn:** FEATURE_SPECIFICATION.md Section 9

### 1.2. Vị trí trong hệ thống

```
DCNET Flow
├── CRM (Đợt 1)
│   ├── Lead
│   ├── Customer
│   └── Order
├── ERP (Đợt 2)
│   ├── Warehouse
│   ├── Product
│   └── **Shipping** ← Module này
└── Advanced (Đợt 3)
```

**Nguồn:** FEATURE_SPECIFICATION.md Phân giai đoạn

---

## 2. Chức năng chính

### 2.1. Danh sách Đơn giao vận

**Mô tả:** Hiển thị danh sách các đơn vận chuyển

**Tính năng:**
- Hiển thị danh sách đơn giao vận
- Filter theo trạng thái đơn giao vận

**Nguồn:** FEATURE_SPECIFICATION.md Section 9.1 (Line 803-809)

### 2.2. Tích hợp Viettel Post

**Mô tả:** Kết nối với API Viettel Post để tạo và theo dõi vận đơn

**Tính năng:**
- Cho phép tạo đơn giao vận từ hệ thống CRM sang Viettel Post
- Đồng bộ mã giao vận
- Đồng bộ dịch vụ giao vận
- Đồng bộ giá vận chuyển
- Đồng bộ trạng thái giao vận với Viettel Post

**Xử lý đặc biệt:**
- Đơn ở trạng thái đổi/trả thì cập nhật lại tồn kho

**Nguồn:** FEATURE_SPECIFICATION.md Section 9.2 (Line 810-818)

---

## 3. Đơn vị vận chuyển hỗ trợ

### 3.1. Ưu tiên cao

| Đơn vị | Trạng thái | Ghi chú |
|--------|-----------|---------|
| **Viettel Post** | Bắt buộc | Tích hợp API đầy đủ |

**Nguồn:** FEATURE_SPECIFICATION.md Section 9.2

### 3.2. Tùy chọn (cần xác nhận)

| Đơn vị | Trạng thái | Ghi chú |
|--------|-----------|---------|
| GHTK | Tùy chọn | Cần confirm với khách hàng |
| GHN | Tùy chọn | Cần confirm với khách hàng |

**Nguồn:** SHIPPING_QUESTIONS.md Section 1.1

---

## 4. Tích hợp với Module khác

### 4.1. Dependencies

**Depends on:**
- **Sales Order** - Đơn hàng cần giao
- **Delivery Note** - Phiếu xuất kho
- **Customer** - Thông tin khách hàng, địa chỉ giao hàng
- **Warehouse** - Cập nhật tồn kho khi hoàn/trả

**Nguồn:** FEATURE_SPECIFICATION.md Section 9.2

### 4.2. Đơn hàng đặc biệt

| Loại đơn | Giao hàng | Ghi chú |
|----------|-----------|---------|
| Fitting | Tùy chọn | Phụ kiện phát sinh (nếu có) |
| Coaching | Tùy chọn | Tài liệu, dụng cụ (nếu có) |
| Thu cũ đổi mới | Tùy chọn | Vận chuyển ngược - lấy hàng cũ |
| Bảo hành | Tùy chọn | Giao trả hàng sau sửa |

**Nguồn:** SHIPPING_QUESTIONS.md Section 8

---

## 5. DCNET Core Foundation

### 5.1. ERPNext có sẵn (70% coverage)

**Delivery Note:**
- ✅ Phiếu giao hàng từ Sales Order
- ✅ Địa chỉ giao hàng
- ✅ Shipping Rule (tính phí)
- ✅ Print Format

**Shipment:**
- ✅ Quản lý vận đơn
- ✅ Service Provider field
- ✅ AWB Number (mã vận đơn)
- ✅ Tracking URL
- ✅ Tracking Status
- ✅ Pickup/Delivery information
- ✅ Parcel management

**Shipping Rule:**
- ✅ Tính phí theo Fixed/Net Total/Net Weight
- ✅ Điều kiện theo khoảng giá trị
- ✅ Miễn phí vận chuyển (đơn > X VNĐ)

**Nguồn:** ERPNext v16 Stock Module Analysis

### 5.2. Cần Custom (30%)

**API Integration:**
- ❌ Viettel Post API
- ❌ Auto sync tracking status
- ❌ Webhook notification

**Business Logic:**
- ❌ COD management
- ❌ Auto return handling (hoàn/trả)
- ❌ Customer notification

**Nguồn:** Gap Analysis - Shipping Module

---

## 6. Phạm vi MVP (Đợt 2)

### 6.1. In Scope

**Core Features:**
- ✅ Danh sách đơn giao vận
- ✅ Filter theo trạng thái
- ✅ Tích hợp Viettel Post API
- ✅ Tạo vận đơn từ Delivery Note
- ✅ Sync mã vận đơn (AWB)
- ✅ Sync tracking status (manual polling)
- ✅ Shipping Rule configuration

**Nguồn:** FEATURE_SPECIFICATION.md Section 9 + ERPNext Analysis

### 6.2. Out of Scope (Phase 2)

**Advanced Features:**
- ❌ Auto webhook sync (real-time)
- ❌ Push notification cho khách hàng
- ❌ Auto xử lý hoàn/trả
- ❌ COD reconciliation dashboard
- ❌ Multi-carrier comparison

**Nguồn:** Phase Planning

---

## 7. Câu hỏi cần xác nhận

### 7.1. Ưu tiên cao (bắt buộc trước khi build)

| # | Câu hỏi | Impact |
|---|---------|--------|
| 1 | Đơn vị vận chuyển nào cần tích hợp cho MVP? | Scope & Architecture |
| 2 | Đã có tài khoản Viettel Post? Loại nào? | API Setup |
| 3 | Thời điểm tạo vận đơn? (Auto/Manual) | Workflow |
| 4 | Có sử dụng COD không? Tỷ lệ bao nhiêu? | Business Logic |
| 5 | Ai trả phí vận chuyển? | Shipping Rule Config |

**Nguồn:** SHIPPING_QUESTIONS.md Section A (Priority)

### 7.2. Ưu tiên trung bình (có thể clarify sau)

| # | Câu hỏi | Impact |
|---|---------|--------|
| 6 | Gửi hàng từ bao nhiêu địa điểm? | Multi-location setup |
| 7 | Flow đối soát COD? (Manual/Auto) | Feature complexity |
| 8 | Đơn đặc biệt (Fitting/Coaching) có giao hàng? | Module integration |

**Nguồn:** SHIPPING_QUESTIONS.md Section B-C

---

## 8. Ràng buộc & Quy tắc

### 8.1. Business Rules

**Trạng thái hoàn/trả:**
- Khi đơn ở trạng thái **Hoàn** hoặc **Trả** → Tự động cập nhật tồn kho

**Nguồn:** FEATURE_SPECIFICATION.md Section 9.2 (Line 817)

### 8.2. Technical Constraints

**API Limitations:**
- Viettel Post API rate limit (cần xác nhận)
- Tracking status update frequency

**Data Constraints:**
- Mã vận đơn (AWB) là unique
- Shipment phải link với Delivery Note

**Nguồn:** ERPNext Shipment DocType Constraints

---

## 9. Timeline Estimate

### 9.1. Phase 1 - MVP (15 ngày)

**Custom App: `dcnet_shipping`**
- Viettel Post API integration: 5 ngày
- Auto create Shipment từ Delivery Note: 3 ngày
- Sync AWB & tracking status: 4 ngày
- Shipping Rule configuration: 2 ngày
- Testing & Bug fix: 1 ngày

**Nguồn:** Technical Estimate

### 9.2. Phase 2 - Enhancements (10 ngày)

- Webhook auto sync: 3 ngày
- Customer notification: 3 ngày
- Auto return handling: 2 ngày
- COD reconciliation: 2 ngày

**Nguồn:** Future Enhancement Planning

---

## 10. Acceptance Criteria

### 10.1. Functional

- [ ] User có thể xem danh sách đơn giao vận
- [ ] User có thể filter theo trạng thái
- [ ] System tạo vận đơn Viettel Post thành công
- [ ] Mã vận đơn sync về Shipment
- [ ] Tracking status cập nhật chính xác
- [ ] Phí vận chuyển tính đúng theo Shipping Rule
- [ ] Đơn hoàn/trả cập nhật tồn kho

### 10.2. Non-Functional

- [ ] API response time < 3s
- [ ] Tracking update mỗi 30 phút
- [ ] 99% uptime
- [ ] Audit log đầy đủ

**Nguồn:** Standard Quality Requirements

---

**Cập nhật:** 14/01/2026

**Người tạo:** DCNET Development Team
