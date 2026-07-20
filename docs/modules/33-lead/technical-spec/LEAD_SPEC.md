# Module Lead - Đặc tả theo Nhật Minh

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 3
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Bàn giao đợt 1
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc

---

## Định nghĩa

> Data cơ hội khách hàng mới có quan tâm mua hàng nhưng chưa có giao dịch thành công

---

## Danh sách Lead

### Hiển thị các cột thông tin:
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

### Tính năng:
- Ẩn/hiện thông tin cột
- Cập nhật tags

### Search/Filter:
- **Tìm kiếm theo:** tên, email
- **Filter theo:**
  - Trạng thái
  - Trạng thái phụ trách (có/chưa NV phụ trách)
  - Thời gian tạo
  - Chi nhánh
  - NV phụ trách
  - Người tạo
  - Độ tuổi
  - Tags

---

## Tạo Lead

### Thông tin cơ bản:
- Mã (auto)
- Ngày nhận
- Tên
- Giới tính
- ĐT
- Email
- Ngày sinh
- Nhân viên phụ trách

### Thông tin nâng cao:
- Trạng thái (VD: chưa nghe máy, đang tư vấn, đang giao hàng, thuê bao, hủy)
- Tags
- Nguồn
- Chi nhánh
- Địa chỉ: Tỉnh thành phố, Quận huyện, Phường xã
- Bảng giá áp dụng
- Sale chăm sóc

### Tính năng bổ sung:
- **Check trùng thông tin** (khi tạo lead)

---

## Import danh sách Lead

| Chức năng | Mô tả |
| --- | --- |
| Import Lead | File excel |

---

## Phân công Lead

> **Lưu ý:** Admin tự phân công Lead thủ công cho nhân viên chăm sóc theo chi nhánh

---

## Xem chi tiết Lead

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

## Cập nhật Lead

- Cập nhật thông tin cơ bản
- Cập nhật tài liệu (Thêm, xóa tài liệu)
- Cập nhật người phụ trách

---

## Xóa Lead

- Xóa lead khỏi hệ thống

---

## Tự động tạo Lead từ nguồn bên ngoài

| Chức năng | Mô tả |
| --- | --- |
| Tự động tạo lead mới từ nhanh_vn | Về với các nguồn đa kênh |

---

## Export danh sách Lead

| Chức năng | Mô tả |
| --- | --- |
| Export Lead | File excel |

---

## Expose API tạo khách hàng

| Chức năng | Mô tả |
| --- | --- |
| Expose API | Xây dựng cổng API cho phép tạo khách hàng mới với nguồn từ hệ thống khác nhằm xác nhận rõ nguồn khách hàng nhận được |

---

## Tổng hợp chức năng Module Lead

| STT | Chức năng | Mô tả |
| --- | --- | --- |
| 1 | Danh sách Lead | Hiển thị, filter, search, ẩn/hiện cột |
| 2 | Tạo Lead | Thông tin cơ bản + nâng cao, check trùng |
| 3 | Import Lead | Import từ file Excel |
| 4 | Xem chi tiết Lead | Thông tin, lịch sử, tài liệu, tư vấn |
| 5 | Cập nhật Lead | Cập nhật thông tin, tài liệu, người phụ trách |
| 6 | Xóa Lead | Xóa khỏi hệ thống |
| 7 | Tự động tạo Lead | Từ nhanh_vn đa kênh |
| 8 | Export Lead | Export ra file Excel |
| 9 | Expose API | API tạo khách hàng từ hệ thống khác |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 3 - Quản lý Lead
**Lưu ý:** Đây là spec GỐC từ Nhật Minh (PHỤ LỤC hợp đồng)
