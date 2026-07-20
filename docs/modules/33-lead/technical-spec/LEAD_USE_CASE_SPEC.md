# Đặc tả Use Cases - Module Quản lý Lead

**Dự án:** DCNET Flow - Nhật Minh Sports
**Module:** Lead Management
**Phiên bản:** 1.0
**Nguồn:** FEATURE_SPECIFICATION.md (Section 3)
**Ngày:** 06/01/2026

---

## 📋 Mục lục

1. [Định nghĩa Lead](#1-định-nghĩa-lead)
2. [Danh sách Actors và Vai trò](#2-danh-sách-actors-và-vai-trò)
3. [Ma trận Phân quyền](#3-ma-trận-phân-quyền)
4. [Chi tiết Use Cases](#4-chi-tiết-use-cases)
5. [Use Case Diagram](#5-use-case-diagram)

---

## 1. Định nghĩa Lead

> **Định nghĩa từ khách hàng:**
> 
> Data cơ hội khách hàng mới có quan tâm mua hàng nhưng chưa có giao dịch thành công

**Đặc điểm:**
- Chưa phát sinh giao dịch thành công
- Có tiềm năng chuyển đổi thành Khách hàng
- Khi tạo đơn hàng → Tự động chuyển thành Khách hàng

---

## 2. Danh sách Actors và Vai trò

### 2.1. Admin

**Mô tả:** Quản trị viên hệ thống

**Quyền hạn:**
- Xem tất cả Lead
- **Phân công Lead cho nhân viên chăm sóc** (thủ công - không auto)
- Quản lý cấu hình: Tags, Trạng thái, Nguồn khách hàng

---

### 2.2. Nhân viên (Sale/NV phụ trách)

**Mô tả:** Nhân viên chăm sóc Lead

**Quyền hạn:**
- Xem Lead được phân công
- Cập nhật thông tin Lead
- Chuyển trạng thái Lead
- Thêm hoạt động tư vấn
- Tạo đơn hàng từ Lead

**Giới hạn:**
- Chỉ xem Lead được phân công cho mình

---

### 2.3. System (Tự động)

**Mô tả:** Hệ thống tự động thực hiện các tác vụ

**Chức năng:**
- **Tự động chuyển đổi Lead → Customer khi tạo đơn hàng**
- Tạo mã Lead tự động
- Ghi log hoạt động

---

## 3. Ma trận Phân quyền

| Use Case | Admin | Nhân viên | System |
| --- | --- | --- | --- |
| **UC-01: Tạo Lead mới** | ✓ | ✓ | - |
| **UC-02: Xem danh sách Lead** | ✓ (tất cả) | ✓ (của mình) | - |
| **UC-03: Xem chi tiết Lead** | ✓ | ✓ | - |
| **UC-04: Cập nhật thông tin Lead** | ✓ | ✓ | - |
| **UC-05: Cập nhật Tags** | ✓ | ✓ | - |
| **UC-06: Chuyển trạng thái** | ✓ | ✓ | - |
| **UC-07: Thêm lịch sử tư vấn** | ✓ | ✓ | - |
| **UC-08: Cập nhật tài liệu** | ✓ | ✓ | - |
| **UC-09: Phân công Lead** | ✓ | - | - |
| **UC-10: Tạo đơn hàng từ Lead** | ✓ | ✓ | - |
| **UC-11: Tự động chuyển Lead → Customer** | - | - | ✓ |
| **UC-12: Xóa Lead** | ✓ | - | - |
| **UC-13: Import danh sách Lead** | ✓ | ✓ | - |
| **UC-14: Export danh sách Lead** | ✓ | ✓ | - |
| **UC-15: Tự động tạo Lead từ nhanh\_vn** | - | - | ✓ |
| **UC-16: Expose API tạo khách hàng** | - | - | ✓ |

**Chú thích:**
- ✓ = Có quyền thực hiện
- ✓ (của mình) = Chỉ thực hiện trên Lead được phân công
- ✓ (tất cả) = Thực hiện trên tất cả Lead
- - = Không có quyền

---

## 4. Chi tiết Use Cases

### UC-01: Tạo Lead mới

**ID:** UC-01
**Tên:** Tạo Lead mới
**Actors:** Admin, Nhân viên

**Mô tả:**
Nhập thông tin khách hàng tiềm năng mới vào hệ thống.

**Precondition:**
- User đã đăng nhập vào hệ thống

**Main Flow:**
1. User chọn "Tạo Lead mới"
2. Hệ thống hiển thị form nhập thông tin
3. User nhập **Thông tin cơ bản:**
  - Mã (auto)
  - Ngày nhận
  - Tên (bắt buộc)
  - Giới tính
  - Điện thoại (bắt buộc)
  - Email
  - Ngày sinh
  - Nhân viên phụ trách
4. User nhập **Thông tin nâng cao:**
  - Trạng thái (VD: chưa nghe máy, đang tư vấn, đang giao hàng, thuê bao, hủy)
  - Tags
  - Nguồn
  - Chi nhánh
  - Địa chỉ: Tỉnh thành phố, Quận huyện, Phường xã
  - Bảng giá áp dụng
  - Sale chăm sóc
5. User submit form
6. Hệ thống tạo Lead mới với mã tự động
7. Hệ thống lưu thông tin

**Postcondition:**
- Lead mới được tạo trong hệ thống
- Mã Lead được sinh tự động

**Business Rules:**
- Mã Lead tự động sinh
- Tên và Điện thoại là bắt buộc

---

### UC-02: Xem danh sách Lead

**ID:** UC-02
**Tên:** Xem danh sách Lead
**Actors:** Admin, Nhân viên

**Mô tả:**
Hiển thị danh sách Lead trong hệ thống với khả năng lọc, sắp xếp, ẩn/hiện cột.

**Precondition:**
- User đã đăng nhập vào hệ thống

**Main Flow:**
1. User truy cập trang "Danh sách Lead"
2. Hệ thống hiển thị danh sách Lead:
  - **Admin:** Thấy tất cả Lead
  - **Nhân viên:** Chỉ thấy Lead được phân công cho mình
3. Hệ thống hiển thị các cột:
  - Mã khách hàng
  - Tên
  - ĐT
  - Trạng thái (có thể chuyển trực tiếp tại danh sách)
  - Email
  - Tags (có thể thêm trực tiếp tại danh sách)
  - Thời gian tạo
  - Ngày nhận lead
  - Liên hệ lần cuối
  - Tổng số tương tác
  - Người tạo
  - Nguồn lead
  - Chi nhánh
  - Địa chỉ
  - Giới tính

**Tính năng:**
- **Ẩn/hiện thông tin cột:** User có thể tuỳ chỉnh cột hiển thị
- **Cập nhật tags:** Cập nhật tags trực tiếp tại danh sách
- **Chuyển trạng thái:** Chuyển trạng thái trực tiếp tại danh sách

**Search/Filter:**
- **Tìm kiếm theo:** Tên, Email
- **Filter theo:**
  - Trạng thái
  - Trạng thái phụ trách (có/chưa NV phụ trách)
  - Thời gian tạo
  - Chi nhánh
  - NV phụ trách
  - Người tạo
  - Độ tuổi
  - Tags

**Postcondition:**
- Danh sách Lead được hiển thị theo quyền hạn

---

### UC-03: Xem chi tiết Lead

**ID:** UC-03
**Tên:** Xem chi tiết Lead
**Actors:** Admin, Nhân viên

**Mô tả:**
Xem thông tin chi tiết của một Lead cụ thể.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống
- User có quyền xem Lead này

**Main Flow:**
1. User click vào một Lead trong danh sách
2. Hệ thống kiểm tra quyền
3. Hệ thống hiển thị chi tiết Lead:
  - **Thông tin cơ bản**
  - **Lịch sử giao dịch**
  - **Hàng hóa đã mua**
  - **Tài liệu đi kèm**
  - **Bình luận gắn với hoạt động** (gọi, sms, email, FB, Zalo)
  - **Lịch sử tư vấn:**
    - Sản phẩm đã tư vấn
    - Nhân viên tư vấn
    - Ngày tháng tư vấn
    - Nội dung tư vấn

**Actions:**
- **Tạo đơn hàng** (UC-10)

**Postcondition:**
- Chi tiết Lead được hiển thị

---

### UC-04: Cập nhật thông tin Lead

**ID:** UC-04
**Tên:** Cập nhật thông tin Lead
**Actors:** Admin, Nhân viên

**Mô tả:**
Sửa đổi thông tin cơ bản của Lead đã tồn tại.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống
- User có quyền cập nhật Lead này

**Main Flow:**
1. User mở chi tiết Lead
2. User click "Chỉnh sửa thông tin Lead"
3. Hệ thống hiển thị form edit
4. User cập nhật **thông tin cơ bản**:
  - Tên
  - Giới tính
  - ĐT
  - Email
  - Ngày sinh
  - Địa chỉ
  - Chi nhánh
  - Nguồn
  - Bảng giá áp dụng
5. User submit form
6. Hệ thống lưu thay đổi

**Postcondition:**
- Thông tin Lead được cập nhật

**Business Rules:**
- Không cho phép sửa Mã Lead (tự động sinh)

---

### UC-05: Cập nhật Tags

**ID:** UC-05
**Tên:** Cập nhật Tags
**Actors:** Admin, Nhân viên

**Mô tả:**
Thêm hoặc xóa tags cho Lead, có thể thực hiện trực tiếp tại danh sách.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống

**Main Flow:**
1. User chọn Lead cần cập nhật tags
2. User click vào cột "Tags"
3. User thêm/xóa tags
4. Hệ thống lưu thay đổi

**Postcondition:**
- Tags của Lead được cập nhật

**Business Rules:**
- Có thể cập nhật tags trực tiếp tại danh sách Lead
- Tags được quản lý tập trung trong phần "Cài đặt hệ thống"

---

### UC-06: Chuyển trạng thái

**ID:** UC-06
**Tên:** Chuyển trạng thái
**Actors:** Admin, Nhân viên

**Mô tả:**
Thay đổi trạng thái của Lead theo quy trình chăm sóc, có thể thực hiện trực tiếp tại danh sách.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống
- User có quyền cập nhật Lead này

**Main Flow:**
1. User chọn Lead cần chuyển trạng thái
2. User click vào cột "Trạng thái" tại danh sách HOẶC vào chi tiết Lead
3. User chọn trạng thái mới (VD: chưa nghe máy, đang tư vấn, đang giao hàng, thuê bao, hủy)
4. Hệ thống cập nhật trạng thái
5. Hệ thống ghi log thay đổi

**Postcondition:**
- Trạng thái Lead được cập nhật
- Log hoạt động được ghi nhận

**Business Rules:**
- Có thể chuyển trạng thái trực tiếp tại danh sách Lead
- Danh sách trạng thái được quản lý trong "Cài đặt hệ thống → Trạng thái Khách hàng"

---

### UC-07: Thêm lịch sử tư vấn

**ID:** UC-07
**Tên:** Thêm lịch sử tư vấn
**Actors:** Admin, Nhân viên

**Mô tả:**
Ghi lại thông tin tư vấn khách hàng.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống
- User có quyền cập nhật Lead này

**Main Flow:**
1. User mở chi tiết Lead
2. User click tab "Lịch sử tư vấn"
3. User click "Thêm hoạt động tư vấn"
4. User nhập thông tin:
  - **Sản phẩm đã tư vấn**
  - **Nhân viên tư vấn** (auto-fill từ user hiện tại)
  - **Ngày tháng tư vấn**
  - **Nội dung tư vấn**
5. User submit
6. Hệ thống lưu lịch sử tư vấn

**Postcondition:**
- Lịch sử tư vấn được ghi nhận

**Business Rules:**
- Lịch sử tư vấn hiển thị trong tab "Lịch sử tư vấn" tại chi tiết Lead
- Không được xóa lịch sử tư vấn (chỉ xem)

---

### UC-08: Cập nhật tài liệu

**ID:** UC-08
**Tên:** Cập nhật tài liệu
**Actors:** Admin, Nhân viên

**Mô tả:**
Thêm hoặc xóa tài liệu đi kèm cho Lead.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống
- User có quyền cập nhật Lead này

**Main Flow (Thêm tài liệu):**
1. User mở chi tiết Lead
2. User click tab "Tài liệu đi kèm"
3. User click "Thêm tài liệu"
4. User upload file
5. Hệ thống lưu file
6. Hệ thống hiển thị tài liệu trong danh sách

**Main Flow (Xóa tài liệu):**
1. User mở chi tiết Lead
2. User click tab "Tài liệu đi kèm"
3. User chọn tài liệu cần xóa
4. User click "Xóa"
5. Hệ thống xác nhận
6. Hệ thống xóa tài liệu

**Postcondition:**
- Tài liệu được thêm/xóa

---

### UC-09: Phân công Lead

**ID:** UC-09
**Tên:** Phân công Lead
**Actors:** Admin

**Mô tả:**
Admin phân công Lead cho nhân viên chăm sóc (thủ công - không auto).

**Precondition:**
- User đã đăng nhập với quyền Admin
- Lead tồn tại trong hệ thống

**Main Flow:**
1. Admin mở chi tiết Lead
2. Admin click "Cập nhật người phụ trách"
3. Hệ thống hiển thị danh sách nhân viên
4. Admin chọn nhân viên mới
5. Admin submit
6. Hệ thống cập nhật người phụ trách
7. Hệ thống gửi thông báo cho nhân viên mới

**Postcondition:**
- Lead được phân công cho nhân viên mới
- Nhân viên mới nhận được thông báo

**Business Rules:**
- **QUAN TRỌNG:** Admin tự phân công lead cho nhân viên chăm sóc, **không auto chia**
- Chỉ Admin mới có quyền phân công

---

### UC-10: Tạo đơn hàng từ Lead

**ID:** UC-10
**Tên:** Tạo đơn hàng từ Lead
**Actors:** Admin, Nhân viên

**Mô tả:**
Tạo đơn hàng khi Lead quyết định mua hàng.

**Precondition:**
- User đã đăng nhập
- Lead tồn tại trong hệ thống
- User có quyền tạo đơn hàng cho Lead này

**Main Flow:**
1. User mở chi tiết Lead
2. User click **Action: "Tạo đơn hàng"**
3. Hệ thống mở form tạo Order:
  - Pre-fill thông tin từ Lead (Tên, SĐT, Email, Địa chỉ)
4. User nhập thông tin đơn hàng:
  - Nguồn đơn
  - Địa chỉ nhận hàng
  - Thời gian tạo đơn hàng
  - Kho xuất hàng
  - Chọn sản phẩm
  - Phương thức thanh toán
5. User submit form
6. Hệ thống tạo Order
7. **Hệ thống trigger UC-11: Tự động chuyển đổi Lead → Customer**

**Postcondition:**
- Order được tạo thành công
- Lead được chuyển thành Customer (UC-11)

**Business Rules:**
- Form Order pre-fill thông tin từ Lead
- Khi tạo đơn hàng thành công → Lead tự động chuyển thành Khách hàng

---

### UC-11: Tự động chuyển Lead → Customer

**ID:** UC-11
**Tên:** Tự động chuyển đổi Lead → Customer
**Actors:** System

**Mô tả:**
Hệ thống tự động chuyển Lead thành Customer khi tạo đơn hàng thành công.

**Precondition:**
- Order từ Lead được tạo thành công (UC-10)

**Main Flow:**
1. System nhận sự kiện: "Order created from Lead"
2. System kiểm tra Lead chưa có Customer tương ứng
3. System tạo Customer mới:
  - Copy thông tin từ Lead: Tên, ĐT, Email, Địa chỉ, Giới tính, Ngày sinh, Tags, Nguồn, Chi nhánh, Bảng giá áp dụng
  - Link Customer với Lead (reference)
4. System ghi log: "Lead được chuyển đổi thành Customer"

**Postcondition:**
- Customer mới được tạo
- Lead được link với Customer
- Log được ghi nhận

**Alternative Flow:**
- 2a. Nếu Customer đã tồn tại (SĐT/Email trùng):
  - System link Lead với Customer hiện có
  - Không tạo Customer mới

**Business Rules:**
- **Khi tạo đơn hàng, Lead tự động chuyển thành Khách hàng** (theo FEATURE_SPECIFICATION.md)
- Lead record không bị xóa (giữ để tracking)

---

### UC-12: Xóa Lead

**ID:** UC-12
**Tên:** Xóa Lead
**Actors:** Admin

**Mô tả:**
Xóa Lead khỏi hệ thống.

**Precondition:**
- User đã đăng nhập với quyền Admin
- Lead tồn tại trong hệ thống

**Main Flow:**
1. Admin mở danh sách Lead hoặc chi tiết Lead
2. Admin click "Xóa Lead"
3. Hệ thống hiển thị xác nhận: "Bạn có chắc chắn muốn xóa Lead này?"
4. Admin xác nhận
5. Hệ thống xóa Lead

**Postcondition:**
- Lead bị xóa khỏi hệ thống

**Business Rules:**
- Chỉ Admin mới có quyền xóa Lead
- Cần xác nhận trước khi xóa

---

### UC-13: Import danh sách Lead

**ID:** UC-13
**Tên:** Import danh sách Lead
**Actors:** Admin, Nhân viên

**Mô tả:**
Import danh sách Lead từ file Excel vào hệ thống.

**Precondition:**
- User đã đăng nhập vào hệ thống
- File Excel đúng định dạng template

**Main Flow:**
1. User chọn "Import Lead"
2. Hệ thống hiển thị form upload
3. User tải lên file Excel
4. Hệ thống validate file:
  - Kiểm tra định dạng
  - Kiểm tra các cột bắt buộc (Tên, ĐT)
  - **Check trùng thông tin** (theo SĐT/Email)
5. Hệ thống hiển thị preview dữ liệu
6. User xác nhận import
7. Hệ thống tạo các Lead mới
8. Hệ thống báo cáo kết quả (thành công/lỗi)

**Postcondition:**
- Các Lead mới được tạo trong hệ thống
- Các record trùng được báo cáo

**Business Rules:**
- File Excel theo template định sẵn
- Check trùng theo SĐT hoặc Email
- Bỏ qua hoặc cập nhật record trùng (tuỳ cấu hình)

---

### UC-14: Export danh sách Lead

**ID:** UC-14
**Tên:** Export danh sách Lead
**Actors:** Admin, Nhân viên

**Mô tả:**
Xuất danh sách Lead ra file Excel.

**Precondition:**
- User đã đăng nhập vào hệ thống
- Có Lead trong hệ thống

**Main Flow:**
1. User truy cập "Danh sách Lead"
2. User áp dụng filter (nếu cần)
3. User chọn "Export Lead"
4. Hệ thống xuất file Excel:
  - **Admin:** Xuất tất cả Lead (hoặc theo filter)
  - **Nhân viên:** Xuất Lead được phân công (hoặc theo filter)
5. Hệ thống tải file về máy

**Postcondition:**
- File Excel được tải về máy user

**Business Rules:**
- Export theo quyền hạn (Admin: tất cả, NV: của mình)
- Có thể export theo filter đang áp dụng

---

### UC-15: Tự động tạo Lead từ nhanh_vn

**ID:** UC-15
**Tên:** Tự động tạo Lead từ nhanh_vn
**Actors:** System

**Mô tả:**
Hệ thống tự động tạo Lead mới khi có dữ liệu từ nhanh_vn với các nguồn đa kênh.

**Precondition:**
- Tích hợp với nhanh_vn đã được cấu hình
- Có dữ liệu mới từ nhanh_vn

**Main Flow:**
1. System nhận webhook/API call từ nhanh_vn
2. System parse dữ liệu khách hàng
3. System check trùng (SĐT/Email)
4. Nếu không trùng:
  - System tạo Lead mới
  - Gán nguồn theo kênh (Facebook, Zalo, Website...)
5. Nếu trùng:
  - System cập nhật thông tin (nếu cần)
  - Ghi log

**Postcondition:**
- Lead mới được tạo tự động
- Nguồn khách hàng được ghi nhận chính xác

**Business Rules:**
- Tự động tạo từ các nguồn đa kênh qua nhanh_vn
- Check trùng trước khi tạo mới
- Ghi nhận nguồn khách hàng từ kênh gốc

---

### UC-16: Expose API tạo khách hàng

**ID:** UC-16
**Tên:** Expose API tạo khách hàng
**Actors:** System (External System)

**Mô tả:**
Xây dựng cổng API cho phép tạo khách hàng mới với nguồn từ hệ thống khác nhằm xác nhận rõ nguồn khách hàng nhận được.

**Precondition:**
- API đã được cấu hình và bảo mật
- External system có API key/token hợp lệ

**Main Flow:**
1. External system gọi API endpoint `/api/leads`
2. System xác thực request (API key/token)
3. System validate dữ liệu đầu vào:
  - Tên (bắt buộc)
  - ĐT (bắt buộc)
  - Nguồn (bắt buộc - xác định hệ thống gọi)
4. System check trùng
5. System tạo Lead mới
6. System trả về response (success/error)

**Postcondition:**
- Lead mới được tạo
- Nguồn khách hàng được xác nhận từ hệ thống gọi

**API Specification:**
```

POST /api/leads
Headers:
  - Authorization: Bearer {token}
  - Content-Type: application/json

Body:
{
  "name": "string (required)",
  "phone": "string (required)",
  "email": "string",
  "source": "string (required)",
  "tags": ["string"],
  ...
}

Response:
{
  "success": true,
  "lead_id": "string",
  "message": "Lead created successfully"
}
```

**Business Rules:**
- API phải có xác thực
- Nguồn khách hàng là bắt buộc để tracking
- Check trùng trước khi tạo

---

## 5. Use Case Diagram

### 5.1. Sơ đồ Use Case (Text)

```
┌──────────────────────────────────────────────────────────────────────┐
│                      «System» Lead Management                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌────────────────────────┐                                           │
│  │ UC-01: Tạo Lead mới    │◄──────────┐                               │
│  └────────────────────────┘           │                               │
│                                        │                               │
│  ┌────────────────────────────────┐   │                               │
│  │ UC-02: Xem danh sách Lead      │◄──┼──────────┐                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-03: Xem chi tiết Lead       │◄──┼──────────┤                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-04: Cập nhật thông tin Lead │◄──┼──────────┤                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-05: Cập nhật Tags           │◄──┼──────────┤                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-06: Chuyển trạng thái       │◄──┼──────────┤                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-07: Thêm lịch sử tư vấn     │◄──┼──────────┤                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-08: Cập nhật tài liệu       │◄──┼──────────┤                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-09: Phân công Lead          │◄──┼──────────┘                    │
│  └────────────────────────────────┘   │     (Manual - Admin)          │
│                                        │                               │
│  ┌────────────────────────────────┐   │                               │
│  │ UC-10: Tạo đơn hàng từ Lead    │◄──┼──────────┐                    │
│  └────────────────────────────────┘   │          │                    │
│              │                         │          │                    │
│              │ «include»               │          │                    │
│              ▼                         │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-11: Tự động chuyển đổi      │◄──┼──────────┼────────────────────┤
│  │        Lead → Customer          │   │          │                    │
│  └────────────────────────────────┘   │          │                    │
│                                        │          │                    │
│  ┌────────────────────────────────┐   │          │                    │
│  │ UC-12: Xóa Lead                │◄──┼──────────┘                    │
│  └────────────────────────────────┘   │                               │
│                                        │                               │
└────────────────────────────────────────┼───────────────────────────────┘
                                         │
                                         │
            ┌───────────┐                │           ┌────────┐
            │ Nhân viên │────────────────┘           │ System │
            └───────────┘                            └────────┘
                  │
             ┌────────┐
             │ Admin  │
             └────────┘
```

### 5.2. Mối quan hệ Actors và Use Cases

**Admin:**
- UC-01: Tạo Lead mới
- UC-02: Xem danh sách Lead (tất cả)
- UC-03: Xem chi tiết Lead
- UC-04: Cập nhật thông tin Lead
- UC-05: Cập nhật Tags
- UC-06: Chuyển trạng thái
- UC-07: Thêm lịch sử tư vấn
- UC-08: Cập nhật tài liệu
- UC-09: Phân công Lead (thủ công)
- UC-10: Tạo đơn hàng từ Lead
- UC-12: Xóa Lead
- UC-13: Import danh sách Lead
- UC-14: Export danh sách Lead

**Nhân viên:**
- UC-01: Tạo Lead mới
- UC-02: Xem danh sách Lead (của mình)
- UC-03: Xem chi tiết Lead
- UC-04: Cập nhật thông tin Lead
- UC-05: Cập nhật Tags
- UC-06: Chuyển trạng thái
- UC-07: Thêm lịch sử tư vấn
- UC-08: Cập nhật tài liệu
- UC-10: Tạo đơn hàng từ Lead
- UC-13: Import danh sách Lead
- UC-14: Export danh sách Lead

**System:**
- UC-11: Tự động chuyển đổi Lead → Customer
- UC-15: Tự động tạo Lead từ nhanh_vn
- UC-16: Expose API tạo khách hàng

### 5.3. Mối quan hệ Include

- **UC-10 «include» UC-11:**
  - Khi tạo đơn hàng từ Lead (UC-10) thành công
  - Hệ thống tự động kích hoạt chuyển đổi Lead → Customer (UC-11)

---

## 📚 Tham khảo

**Tài liệu liên quan:**
- [FEATURE_SPECIFICATION.md](../../feature/FEATURE_SPECIFICATION.md) - Đặc tả chức năng gốc (Section 3)
- [LEAD_WORKFLOW.md](./LEAD_WORKFLOW.md) - Workflow và ERD
- [LEAD_DIAGRAMS.md](./LEAD_DIAGRAMS.md) - State Machine Diagrams

---

## 📝 Ghi chú quan trọng

1. **Phân công Lead:** Admin tự phân công Lead thủ công cho nhân viên chăm sóc theo chi nhánh (UC-09)

2. **Trạng thái Lead:** Danh sách trạng thái do khách hàng tự định nghĩa trong "Cài đặt hệ thống". Ví dụ từ spec:
  - Chưa nghe máy
  - Đang tư vấn
  - Đang giao hàng
  - Thuê bao
  - Hủy

3. **Tự động chuyển đổi:** Khi tạo đơn hàng từ Lead → Lead tự động chuyển thành Khách hàng (UC-11)

4. **Cập nhật nhanh tại danh sách:**
  - Có thể chuyển trạng thái trực tiếp tại danh sách (UC-06)
  - Có thể cập nhật tags trực tiếp tại danh sách (UC-05)

5. **Lịch sử tư vấn:** Ghi lại chi tiết sản phẩm đã tư vấn, nhân viên tư vấn, ngày tháng, nội dung (UC-07)

---

**Ngày cập nhật:** 06/01/2026
**Người soạn:** DCNET Development Team
**Nguồn:** FEATURE_SPECIFICATION.md v1.2.0 (Section 3)
```