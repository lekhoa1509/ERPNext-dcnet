# Module Fitting - Đặc tả theo Nhật Minh

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.1, 5.2.2, 5.4, 5.5, 14.2
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Bàn giao đợt 1
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc

---

## Định nghĩa

> Dịch vụ đo thông số kỹ thuật cá nhân để tư vấn và customize gậy golf phù hợp với từng khách hàng

---

## Danh sách Đơn hàng Fitting

> **Nguồn:** Section 5.1 - Danh sách Đơn hàng

### Loại danh sách:
- Đơn fitting (tách riêng với đơn vật dụng)

### Hiển thị các cột thông tin:
- Mã đơn hàng (tự động)
- Khách hàng
- Trạng thái đơn hàng (chưa xử lý, đang xuất kho, đã xuất kho, đang vận chuyển, hoàn thành, hoàn trả, hủy)
- Giá trị đơn hàng
- Nguồn đơn hàng
- Thời gian tạo đơn
- Thời gian duyệt
- Đã trả
- Còn nợ
- Chi nhánh bán
- Kho xử lý
- Ghi chú
- Ghi chú nội bộ

### Tính năng:
- Ẩn/hiện thông tin cột
- Cập nhật tags

### Search/Filter:
- **Tìm kiếm theo:** tên, email
- **Filter theo:**
  - Chi nhánh
  - Thời gian
  - Trạng thái đơn
  - Tags khách hàng
  - Nguồn đơn hàng

---

## Tạo đơn hàng Fitting

> **Nguồn:** Section 5.2.2 - Tạo đơn hàng Fitting

### Quy trình:
- Đăng ký fitting qua website → đẩy thông tin vào CRM
- Tạo lịch fitting
- Ghi lại thông tin sau khi fitting:
  - Đề xuất nâng cấp
  - Nhân viên phụ trách
  - Phụ kiện phát sinh từ buổi fitting

### Thông tin kỹ thuật:
- Thời gian
- Tên tuổi
- Chiều cao
- Cân nặng
- Kích thước size tay
- Cấp độ (người mới, người đã chơi)
- Tốc độ đầu gậy
- Tốc độ bóng
- Hình swing
- Đường bóng
- Đường cao bóng
- Khoảng cách của bóng gậy sắt
- Khoảng cách của bóng gậy driver
- Tình trạng bộ gậy của khách
- Nhu cầu riêng của KH (Note)

---

## Xem chi tiết đơn Fitting

> **Nguồn:** Section 5.4 - Xem chi tiết Đơn hàng

### Thông tin hiển thị:
- Theo dõi lịch sử fitting khách hàng
- Khách fitting → phát sinh các dịch vụ khác:
  - Mua thêm grip
  - Lắp shaft
  - Đặt gậy theo thông số đặc biệt
  - Mua combo fitting + gậy
- CRM sẽ gắn dịch vụ + sản phẩm đó vào hồ sơ khách hàng để theo dõi toàn diện

---

## Cập nhật đơn Fitting

> **Nguồn:** Section 5.5 - Cập nhật Đơn hàng

### Chức năng:
- Cập nhật đơn Fitting (dịch vụ phát sinh)

---

## Báo cáo Fitting

> **Nguồn:** Section 14.2 - Báo cáo theo module

### Các loại báo cáo:
- Doanh thu phát sinh từ fitting
- Tổng số buổi fitting trong tháng
- Số lượng khách đến thực hiện fitting
- Báo cáo linh kiện sử dụng trong fitting
- Báo cáo nhân viên thực hiện (doanh thu, tỉ lệ tư vấn thành công)

---

## Tổng hợp chức năng Module Fitting

| STT | Chức năng | Mô tả |
| --- | --- | --- |
| 1 | Danh sách Đơn Fitting | Hiển thị, filter, search, ẩn/hiện cột |
| 2 | Tạo đơn Fitting | Đăng ký từ website, tạo lịch, ghi thông số kỹ thuật |
| 3 | Xem chi tiết Fitting | Lịch sử fitting, dịch vụ phát sinh (grip, shaft, custom, combo) |
| 4 | Cập nhật Fitting | Cập nhật dịch vụ phát sinh |
| 5 | Báo cáo Fitting | Doanh thu, số buổi, số khách, linh kiện sử dụng, báo cáo NV |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5 - Quản lý Đơn hàng (Fitting)
**Lưu ý:** Đây là spec GỐC từ Nhật Minh (PHỤ LỤC hợp đồng)
