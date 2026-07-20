# Đặc tả Use Cases - Module Loyalty

**Dự án:** DCNET Flow - Nhật Minh Sports
**Module:** Loyalty Management
**Phiên bản:** 1.0.0
**Nguồn:** FEATURE_SPECIFICATION.md (Section 4.6)
**Nền tảng:** DCNET Core Loyalty Program (có sẵn)
**Ngày:** 13/01/2026

---

## 1. Yêu cầu từ Spec gốc

| # | Chức năng | Mô tả | Status |
|---|-----------|-------|--------|
| 1 | Quy tắc tính điểm | Công thức tích điểm khi mua hàng | ✅ Có sẵn |
| 2 | Quy tắc lên hạng | Điều kiện xác định hạng thành viên | ✅ Có sẵn |

---

## 2. Danh sách Actors

### 2.1. System Manager

**Mô tả:** Quản trị viên hệ thống

**Quyền hạn:**
- Tạo và cấu hình Loyalty Program
- Cấu hình các hạng (tier) và điều kiện
- Xem tất cả Loyalty Point Entry

---

### 2.2. Accounts Manager / Accounts User

**Mô tả:** Nhân viên kế toán

**Quyền hạn:**
- Xem Loyalty Program
- Xem Loyalty Point Entry

---

### 2.3. System (Tự động)

**Mô tả:** Hệ thống tự động thực hiện

**Chức năng:**
- Tự động tích điểm khi submit Sales Invoice
- Tự động xác định hạng dựa trên tổng chi tiêu

---

## 3. Ma trận Phân quyền (DCNET Core)

| Use Case | System Manager | Accounts Manager | Accounts User |
|----------|----------------|------------------|---------------|
| **UC-01: Cấu hình Loyalty Program** | ✓ | - | - |
| **UC-02: Xem Loyalty Program** | ✓ | ✓ | ✓ |
| **UC-03: Xem Loyalty Point Entry** | ✓ | ✓ | ✓ |
| **UC-04: Tự động tích điểm** | System | System | System |
| **UC-05: Sử dụng điểm tại Invoice** | ✓ | ✓ | ✓ |

---

## 4. Chi tiết Use Cases

### UC-01: Cấu hình Loyalty Program

**ID:** UC-01
**Tên:** Cấu hình Loyalty Program
**Actors:** System Manager

**Mô tả:**
Tạo và cấu hình chương trình Loyalty với các hạng thành viên.

**Precondition:**
- User đã đăng nhập với quyền System Manager

**Main Flow:**
1. User truy cập **Selling > Settings > Loyalty Program**
2. User chọn "New"
3. User điền thông tin:
   - **Loyalty Program Name:** Tên chương trình
   - **Loyalty Program Type:** Multiple Tier Program
   - **From Date:** Ngày bắt đầu
   - **Auto Opt In:** Tự động áp dụng cho tất cả KH
4. User thêm **Collection Rules** (các hạng):

| Tier Name | Minimum Total Spent | Collection Factor |
|-----------|---------------------|-------------------|
| Bronze | 0 | (Hệ số quy đổi) |
| Silver | (Doanh số tối thiểu) | (Hệ số quy đổi) |
| Gold | (Doanh số tối thiểu) | (Hệ số quy đổi) |
| Platinum | (Doanh số tối thiểu) | (Hệ số quy đổi) |

5. User cấu hình Redemption (nếu có):
   - **Conversion Factor:** 1 điểm = X VNĐ
   - **Expiry Duration:** Số ngày hết hạn
6. User lưu

**Postcondition:**
- Loyalty Program được tạo và sẵn sàng sử dụng

**Giải thích thuật ngữ:**
- **Collection Factor (Hệ số quy đổi điểm):** Số tiền cần chi để được 1 điểm. VD: 10,000 = chi 10,000 VNĐ được 1 điểm
- **Minimum Total Spent (Doanh số tối thiểu):** Tổng chi tiêu để vào hạng này
- **Conversion Factor (Tỷ lệ quy đổi):** Giá trị 1 điểm khi sử dụng. VD: 1,000 = 1 điểm = 1,000 VNĐ

---

### UC-02: Xem Loyalty Program

**ID:** UC-02
**Tên:** Xem Loyalty Program
**Actors:** System Manager, Accounts Manager, Accounts User

**Mô tả:**
Xem thông tin cấu hình Loyalty Program.

**Main Flow:**
1. User truy cập **Selling > Settings > Loyalty Program**
2. User xem danh sách các chương trình
3. User chọn một chương trình để xem chi tiết

---

### UC-03: Xem Loyalty Point Entry

**ID:** UC-03
**Tên:** Xem Loyalty Point Entry
**Actors:** System Manager, Accounts Manager, Accounts User

**Mô tả:**
Xem lịch sử giao dịch điểm của khách hàng.

**Main Flow:**
1. User truy cập **Accounts > Loyalty Point Entry**
2. Hệ thống hiển thị danh sách với các cột:
   - Customer
   - Loyalty Program
   - Loyalty Program Tier
   - Loyalty Points
   - Purchase Amount
   - Invoice
   - Posting Date
   - Expiry Date
3. User có thể filter theo:
   - Customer
   - Loyalty Program
   - Posting Date

---

### UC-04: Tự động tích điểm

**ID:** UC-04
**Tên:** Tự động tích điểm
**Actors:** System

**Mô tả:**
Hệ thống tự động tích điểm khi submit Sales Invoice.

**Precondition:**
- Customer có `loyalty_program` được gán
- Sales Invoice được submit

**Main Flow:**
1. User submit Sales Invoice
2. System lấy Customer và Loyalty Program
3. System tính `total_spent` của Customer
4. System xác định tier dựa trên `min_spent`:
   - So sánh total_spent với min_spent của từng tier
   - Gán tier cao nhất đạt điều kiện
5. System tính điểm:
   ```
   ĐIỂM = Invoice Amount ÷ Collection Factor của tier
   ```
6. System tạo Loyalty Point Entry:
   - loyalty_program
   - loyalty_program_tier
   - customer
   - invoice
   - loyalty_points
   - purchase_amount
   - expiry_date (nếu có expiry_duration)
   - posting_date

**Postcondition:**
- Loyalty Point Entry được tạo
- Điểm được cộng cho Customer

---

### UC-05: Sử dụng điểm tại Invoice

**ID:** UC-05
**Tên:** Sử dụng điểm tại Invoice
**Actors:** System Manager, Accounts Manager, Accounts User

**Mô tả:**
Cho phép sử dụng điểm để giảm giá trên Sales Invoice.

**Precondition:**
- Customer có điểm khả dụng
- Loyalty Program có conversion_factor

**Main Flow:**
1. User tạo Sales Invoice
2. User nhập số điểm muốn dùng vào field `Loyalty Points`
3. System tính giá trị giảm:
   ```
   Loyalty Amount = Loyalty Points × Conversion Factor
   ```
4. System áp dụng giảm giá vào Invoice
5. User submit Invoice
6. System tạo Loyalty Point Entry với điểm âm (-)

**Postcondition:**
- Invoice được giảm giá
- Điểm được trừ từ Customer

---

## 5. Tổng hợp chức năng DCNET Core

| # | Chức năng | DocType | Có sẵn |
|---|-----------|---------|--------|
| 1 | Cấu hình chương trình | Loyalty Program | ✅ |
| 2 | Cấu hình hạng & điều kiện | Loyalty Program Collection | ✅ |
| 3 | Lịch sử giao dịch điểm | Loyalty Point Entry | ✅ |
| 4 | Tự động tích điểm | Sales Invoice hook | ✅ |
| 5 | Sử dụng điểm giảm giá | Sales Invoice | ✅ |
| 6 | Điểm hết hạn | expiry_duration | ✅ |
| 7 | Gán Loyalty cho Customer | Customer.loyalty_program | ✅ |
| 8 | Auto opt-in | auto_opt_in | ✅ |

---

## 6. Câu hỏi cần xác nhận

| # | Câu hỏi | Ảnh hưởng |
|---|---------|-----------|
| 1 | Hệ số quy đổi điểm cho từng hạng? (Bao nhiêu VNĐ = 1 điểm) | collection_factor |
| 2 | Doanh số tối thiểu cho từng hạng? | min_spent |
| 3 | Có cho dùng điểm đổi giảm giá? | conversion_factor |
| 4 | 1 điểm = bao nhiêu VNĐ? | conversion_factor |
| 5 | Điểm có hết hạn không? Sau bao lâu? | expiry_duration |
| 6 | Áp dụng tự động cho tất cả KH? | auto_opt_in |

---

## 7. Tham khảo

**Tài liệu liên quan:**
- [LOYALTY_SPEC.md](./LOYALTY_SPEC.md) - Đặc tả chức năng
- [LOYALTY_WORKFLOW.md](./LOYALTY_WORKFLOW.md) - Workflow và ERD
- [LOYALTY_STATUS.md](./LOYALTY_STATUS.md) - Trạng thái và hạng

---

**Nguồn:** FEATURE_SPECIFICATION.md Section 4.6
**Nền tảng:** DCNET Core Loyalty Program
**Cập nhật:** 13/01/2026
