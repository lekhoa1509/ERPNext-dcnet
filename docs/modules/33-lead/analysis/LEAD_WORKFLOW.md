# Module Lead - Đặc tả Workflow & ERD

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 3 - Quản lý Lead
> **Lưu ý:** Đây là đặc tả YÊU CẦU, code phải làm theo đặc tả này

---

## 1. Định nghĩa

> Data cơ hội khách hàng mới có quan tâm mua hàng nhưng chưa có giao dịch thành công

---

## 2. Danh sách Lead

### 2.1. Hiển thị các cột thông tin

Theo spec yêu cầu hiển thị:
- Mã khách hàng
- Tên
- ĐT
- Trạng thái (có thể chuyển tại DS)
- Email
- Tags (có thể thêm tại DS)
- Thời gian tạo
- Ngày nhận lead
- Liên hệ lần cuối
- Tổng số tương tác
- Người tạo
- Nguồn lead
- Chi nhánh
- Địa chỉ
- Giới tính

### 2.2. Tính năng

- Ẩn/hiện thông tin cột
- Cập nhật tags

### 2.3. Search/Filter

**Tìm kiếm theo:**
- Tên
- Email

**Filter theo:**
- Trạng thái
- Trạng thái phụ trách (có/chưa NV phụ trách)
- Thời gian tạo
- Chi nhánh
- NV phụ trách
- Người tạo
- Độ tuổi
- Tags

---

## 3. Tạo Lead

### 3.1. Thông tin cơ bản

- Mã (auto)
- Ngày nhận
- Tên
- Giới tính
- ĐT
- Email
- Ngày sinh
- Nhân viên phụ trách

### 3.2. Thông tin nâng cao

- Trạng thái (VD: chưa nghe máy, đang tư vấn, đang giao hàng, thuê bao, hủy)
- Tags
- Nguồn
- Chi nhánh
- Địa chỉ: Tỉnh thành phố, Quận huyện, Phường xã
- Bảng giá áp dụng
- Sale chăm sóc

---

## 4. Phân công Lead

> **Lưu ý:** Admin tự phân công Lead thủ công cho nhân viên chăm sóc theo chi nhánh

---

## 5. Xem chi tiết Lead

Theo spec yêu cầu hiển thị:

- Xem các thông tin cơ bản
- Lịch sử giao dịch
- Hàng hóa đã mua
- Tài liệu đi kèm
- Bình luận gắn với hoạt động (gọi, sms, email, FB, Zalo)
- **Lịch sử tư vấn:**
  - Sản phẩm đã tư vấn
  - Nhân viên tư vấn
  - Ngày tháng tư vấn
  - Nội dung tư vấn
- **Action:** Tạo đơn hàng (Khi tạo đơn hàng, Lead tự động chuyển thành Khách hàng)

---

## 6. Cập nhật Lead

Theo spec yêu cầu:

- Cập nhật thông tin cơ bản
- Cập nhật tài liệu (Thêm, xóa tài liệu)
- Cập nhật người phụ trách

---

## 7. Import danh sách Lead

Theo spec yêu cầu:

| Chức năng | Mô tả |
| --- | --- |
| Import Lead | File excel |

**Quy trình:**
1. User chọn "Import Lead"
2. Upload file Excel theo template
3. Hệ thống validate dữ liệu
4. **Check trùng thông tin** (theo SĐT/Email)
5. Preview kết quả
6. Xác nhận import
7. Tạo Lead mới

---

## 8. Export danh sách Lead

Theo spec yêu cầu:

| Chức năng | Mô tả |
| --- | --- |
| Export Lead | File excel |

**Quy trình:**
1. User truy cập "Danh sách Lead"
2. Áp dụng filter (nếu cần)
3. Chọn "Export Lead"
4. Hệ thống xuất file Excel
5. Tải file về máy

---

## 9. Tự động tạo Lead từ nhanh_vn

Theo spec yêu cầu:

| Chức năng | Mô tả |
| --- | --- |
| Tự động tạo lead mới từ nhanh_vn | Về với các nguồn đa kênh |

**Quy trình:**
1. Nhận dữ liệu từ nhanh_vn (webhook/API)
2. Parse thông tin khách hàng
3. Check trùng (SĐT/Email)
4. Tạo Lead mới (nếu không trùng)
5. Gán nguồn theo kênh (Facebook, Zalo, Website...)

---

## 10. Expose API tạo khách hàng

Theo spec yêu cầu:

| Chức năng | Mô tả |
| --- | --- |
| Expose API | Xây dựng cổng API cho phép tạo khách hàng mới với nguồn từ hệ thống khác nhằm xác nhận rõ nguồn khách hàng nhận được |

**Endpoint:** `POST /api/leads`

**Quy trình:**
1. External system gọi API
2. Xác thực request (API key/token)
3. Validate dữ liệu đầu vào
4. Check trùng
5. Tạo Lead mới
6. Trả về response

---

## 11. Tính năng khác

Theo spec yêu cầu:

- Xóa lead
- Chỉnh sửa thông tin Lead
- **Check trùng thông tin** (khi tạo lead)

---

## 12. ERD - Entity Relationship Diagram

### 12.1. Các thực thể chính

Dựa trên spec, cần có các thực thể:

**Lead** (thực thể chính)
- Mã khách hàng (auto)
- Tên
- ĐT
- Email
- Giới tính
- Ngày sinh
- Địa chỉ (Tỉnh thành phố, Quận huyện, Phường xã)
- Trạng thái
- Tags
- Ngày nhận
- Thời gian tạo
- Liên hệ lần cuối
- Tổng số tương tác
- Người tạo
- Nguồn lead
- Chi nhánh
- Nhân viên phụ trách
- Bảng giá áp dụng
- Sale chăm sóc

**Lịch sử tư vấn** (theo spec Section 5)
- Sản phẩm đã tư vấn
- Nhân viên tư vấn
- Ngày tháng tư vấn
- Nội dung tư vấn
- Link đến Lead

**Tài liệu** (theo spec Section 5, 6)
- Tài liệu đi kèm
- Link đến Lead

**Bình luận hoạt động** (theo spec Section 5)
- Loại hoạt động (gọi, sms, email, FB, Zalo)
- Nội dung
- Link đến Lead

**Lịch sử giao dịch** (theo spec Section 5)
- Link đến Lead
- Thông tin giao dịch

**Hàng hóa đã mua** (theo spec Section 5)
- Link đến Lead
- Sản phẩm

**Tags**
- Tên tag
- Màu sắc

### 12.2. Mối quan hệ

```
Lead --- Nhiều ---> Lịch sử tư vấn
Lead --- Nhiều ---> Tài liệu
Lead --- Nhiều ---> Bình luận hoạt động
Lead --- Nhiều ---> Lịch sử giao dịch
Lead --- Nhiều ---> Hàng hóa đã mua
Lead --- Nhiều ---> Tags (Many-to-Many)
Lead --- 1 -------> Nhân viên phụ trách
Lead --- 1 -------> Người tạo
Lead --- 1 -------> Nguồn lead
Lead --- 1 -------> Chi nhánh
Lead --- 1 -------> Bảng giá
Lead --- 1 -------> Sale chăm sóc
Lead --- 1 -------> Địa chỉ (Tỉnh/TP, Quận/Huyện, Phường/Xã)
```

---

## 13. Business Rules

### 13.1. Phân công Lead

Theo spec:
> Admin tự phân công Lead thủ công cho nhân viên chăm sóc theo chi nhánh

### 13.2. Chuyển đổi Lead sang Khách hàng

Theo spec Section 5:
> Khi tạo đơn hàng, Lead tự động chuyển thành Khách hàng

---

## 14. Trạng thái Lead

Theo spec Section 3.2:
> Trạng thái (VD: chưa nghe máy, đang tư vấn, đang giao hàng, thuê bao, hủy)

**Lưu ý:** Đây là VÍ DỤ, cần xác định đầy đủ các trạng thái cụ thể với stakeholder

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 3 - Quản lý Lead
**Ngày cập nhật:** 2026-01-06
**Trạng thái:** Đặc tả YÊU CẦU - Code phải implement theo đặc tả này
