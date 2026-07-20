# Module Thu cũ Đổi mới (Trade-in) - Đặc tả theo Nhật Minh

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.4, 5.4, 5.5
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Bàn giao đợt 1
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc

---

## Định nghĩa

> Chương trình cho phép khách hàng mang sản phẩm cũ (gậy golf) để đổi lấy sản phẩm mới, với việc tính toán giá trị chênh lệch giữa sản phẩm mới và sản phẩm cũ.

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.4 (Line 489-500)

---

## Danh sách Đơn Thu cũ Đổi mới

### Loại danh sách đơn hàng:
- Đơn thu cũ đổi mới (tách riêng với các loại đơn khác)

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1 (Line 393)

### Tính năng (áp dụng chung cho tất cả loại đơn):
- Ẩn/hiện thông tin cột
- Cập nhật tags

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1 (Line 397-399)

### Search/Filter (áp dụng chung):
- **Tìm kiếm theo:** tên, email
- **Filter theo:**
  - Chi nhánh
  - Thời gian
  - Trạng thái đơn
  - Tags khách hàng
  - Nguồn đơn hàng
  - Loại đơn (Lẻ/Sỉ)

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.1 (Line 401-409)

---

## Tạo đơn hàng Thu cũ Đổi mới

### Thông tin:
- Thông tin sản phẩm khách trả lại (gậy cũ)
- Thông tin sản phẩm mới nhận
- Giá trị bù trừ (khách cần trả thêm hoặc nhận lại nếu có)

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.4 (Line 491-494)

### Tính năng:
- Gắn 2 dòng sản phẩm trong cùng một giao dịch
- Cho phép tính giá trị chênh lệch:
  - **Công thức:** Giá gậy mới - Giá thu gậy cũ - Voucher (nếu có) = Số tiền khách thanh toán

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.4 (Line 496-499)

---

## Xem chi tiết đơn Thu cũ Đổi mới

- Xem chi tiết đơn thu cũ đổi mới

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.4 (Line 540)

> ⚠️ **Cần clarify với khách hàng:** Chi tiết hiển thị những thông tin gì? (Thông tin SP cũ, SP mới, giá trị chênh lệch, lịch sử giao dịch...)

---

## Cập nhật đơn Thu cũ Đổi mới

- Cập nhật đơn thu cũ đổi mới

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.5 (Line 553)

> ⚠️ **Cần clarify với khách hàng:** Những trường nào được phép cập nhật? Quy trình duyệt như thế nào?

---

## Tổng hợp chức năng Module Thu cũ Đổi mới

| STT | Chức năng | Mô tả | Nguồn |
| --- | --- | --- | --- |
| 1 | Danh sách đơn Thu cũ Đổi mới | Hiển thị, filter, search | Section 5.1, Line 393 |
| 2 | Tạo đơn Thu cũ Đổi mới | SP cũ + SP mới + Tính chênh lệch | Section 5.2.4, Line 489-500 |
| 3 | Xem chi tiết đơn | Xem thông tin chi tiết | Section 5.4, Line 540 |
| 4 | Cập nhật đơn | Cập nhật thông tin đơn | Section 5.5, Line 553 |

---

## Các điểm cần Clarify với khách hàng

| # | Câu hỏi | Lý do |
|---|---------|-------|
| 1 | Chi tiết thông tin sản phẩm cũ cần thu thập? | Spec chỉ ghi "thông tin sản phẩm khách trả lại" |
| 2 | Tiêu chí định giá sản phẩm cũ? | Cần biết cách xác định "Giá thu gậy cũ" |
| 3 | Quy trình kiểm tra/đánh giá sản phẩm cũ? | Không có trong spec |
| 4 | Trạng thái workflow của đơn Thu cũ Đổi mới? | Không có trong spec |
| 5 | Ai có quyền duyệt giá thu sản phẩm cũ? | Không có trong spec |
| 6 | Có cho phép thu cũ không đổi mới (chỉ bán lại)? | Liên quan Section 5.9 Resell |
| 7 | Sản phẩm cũ sau khi thu về xử lý như thế nào? | Nhập kho? Bán lại? Thanh lý? |
| 8 | Báo cáo nào cần cho chương trình Trade-in? | Không có trong spec |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.4, 5.4, 5.5 - Quản lý Đơn hàng
**Lưu ý:** Đây là spec GỐC từ Nhật Minh (PHỤ LỤC hợp đồng)
