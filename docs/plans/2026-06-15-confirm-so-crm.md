# Confirm: Tính năng "Sinh đơn hàng" từ CRM

**Ngày confirm:** 15/06/2026  
**Người phụ trách:** _(điền tên)_  
**Mục tiêu:** Xác nhận yêu cầu trước khi phát triển form SO trong CRM

---

## 1. Câu hỏi kỹ thuật cần confirm với khách

### ✅ Đã rõ — không cần hỏi

| Vấn đề | Kết luận |
|--------|----------|
| SO tạo từ CRM có vào kế toán không? | **Có.** SO được tạo thật trong ERPNext. Kế toán vào Selling → Sales Order là thấy, submit/giao hàng/xuất hóa đơn bình thường. |
| Có bị mất dữ liệu khi chuyển từ MISA sang ERP? | Không — miễn là các trường được mapping đúng. |

---

## 2. Mapping MISA → ERPNext

### Trường đã có sẵn trong ERPNext (không cần làm gì thêm)

| MISA | ERPNext | Ghi chú |
|------|---------|---------|
| Khách hàng | Customer | ✅ |
| Liên hệ | Contact Person | ✅ |
| Cơ hội | Opportunity | ✅ |
| Số đơn hàng/Hợp đồng | PO No (po_no) | ✅ |
| Ngày đặt hàng | Transaction Date | ✅ |
| Hạn giao hàng | Delivery Date | ✅ |
| Loại đơn hàng | Order Type | ✅ |
| Chiến dịch | Campaign | ✅ |
| Khu vực | Territory | ✅ |
| Chu kỳ/Điều khoản thanh toán | Payment Terms Template | ✅ |
| Báo giá liên kết | Quotation (linked) | ✅ |
| Diễn giải | Title | ✅ |
| Mô tả | Note | ✅ |
| Bảng giá | Selling Price List | ✅ |
| Tiền tệ | Currency | ✅ |
| Thông tin giao hàng (địa chỉ) | Shipping Address | ✅ |
| Thông tin hóa đơn (địa chỉ) | Billing Address / Customer Address | ✅ |

---

### Trường MISA **không có** trong ERPNext — cần xác nhận có dùng không

> Nếu cần → thêm Custom Field vào Sales Order (khoảng 1-2 ngày dev)

| MISA | Ghi chú | **Câu hỏi cần hỏi khách** |
|------|---------|--------------------------|
| Đơn hàng cha | SO tham chiếu SO khác | Có dùng không? Dùng trong trường hợp nào? |
| Thời hạn HĐg (tháng) | Số tháng hợp đồng | Có cần lưu trường này không? |
| Ngày hết hạn hợp đồng | Contract expiry date | Có cần lưu và theo dõi không? |
| Số ngày được nợ | Credit days per order | Hay dùng điều khoản thanh toán thay thế? |
| Tình trạng thực hiện đơn hàng | Khác với Status của SO | Có cần trường riêng hay dùng Status ERPNext? |
| Ngày ghi số (doanh số) | Revenue recognition date | Có theo dõi ngày ghi nhận DT không? |
| Ngày nghiệm thu tính cước | Acceptance date | Áp dụng cho loại hình nào? |
| Hạn sản xuất | Production deadline | Có liên quan đến quy trình sản xuất không? |

---

### Trường có vẻ đặc thù ngành viễn thông — cần xác nhận

> Những trường này trong MISA có thể được thiết kế cho công ty viễn thông  
> Thăng Long TM và Nhật Minh Sport **có thể không cần**

| MISA | Khả năng áp dụng | **Câu hỏi** |
|------|-----------------|------------|
| Điểm lắp đặt A-End | Điểm đầu đường truyền | Có nghiệp vụ này không? |
| Điểm lắp đặt Z-End | Điểm cuối đường truyền | Có nghiệp vụ này không? |
| Khu vực lắp đặt dịch vụ | Địa điểm triển khai dịch vụ | Khác với Khu vực (Territory) thông thường? |

---

## 3. Câu hỏi về luồng nghiệp vụ

| # | Câu hỏi | Lý do cần biết |
|---|---------|---------------|
| 1 | Ai được phép tạo SO từ CRM? Chỉ sale hay cả quản lý? | Phân quyền |
| 2 | Sau khi tạo SO từ CRM, bước tiếp theo là gì? (Cần duyệt? Hay tự động submit?) | ERPNext SO mặc định ở trạng thái Draft — cần submit mới vào kế toán |
| 3 | Sale có cần xem lại SO sau khi tạo không, hay chỉ cần biết tạo thành công? | UX: có cần link "Mở SO" sau khi lưu? |
| 4 | Khi tạo SO từ cơ hội, cơ hội đó có tự động chuyển trạng thái không? (VD: → "Đã tạo đơn") | Automation |
| 5 | Một cơ hội có thể tạo nhiều SO không? | Ảnh hưởng đến hiển thị danh sách SO trong tab Cơ hội |

---

## 4. Kết luận và bước tiếp theo

| Kết quả confirm | Việc cần làm |
|----------------|-------------|
| Trường nào cần thêm (từ bảng mục 2) | Thêm Custom Field vào SO — ~1 ngày |
| Trường nào không cần | Loại khỏi form để gọn gàng |
| Trường viễn thông không áp dụng | Bỏ qua |
| Luồng duyệt SO | Config Workflow nếu cần |

---

*Ghi chú sau buổi confirm:*

> _(Điền kết quả sau khi confirm với khách)_
