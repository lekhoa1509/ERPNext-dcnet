# Module: Tích hợp Vận chuyển (dcnet/shipping)

> **Plugin**: `dcnet/shipping`
>
> **Giai đoạn**: Bàn giao đợt 2
>
> **Ưu tiên**: Trung bình
>
> **Trạng thái câu hỏi**: Chưa xác nhận

---

## Tổng quan yêu cầu (từ Specs)

| Chức năng | Mô tả | Nguồn |
|-----------|-------|-------|
| Danh sách đơn giao vận | Hiển thị, filter theo trạng thái | FEATURE_SPEC |
| Tích hợp Viettel Post | Tạo đơn từ CRM | FEATURE_SPEC |
| Đồng bộ thông tin | Mã, dịch vụ, giá, trạng thái | FEATURE_SPEC |
| Cập nhật tự động | Trạng thái giao vận | FEATURE_SPEC |
| Lịch sử giao vận | Xem lịch sử | FEATURE_SPEC |
| Xử lý đổi/trả | Cập nhật tồn kho | FEATURE_SPEC |

**Đơn vị vận chuyển đề cập:**
- Viettel Post (bắt buộc)
- GHTK (tùy chọn)
- GHN (tùy chọn)

---

## Câu hỏi cần xác nhận

### 1. Scope tích hợp

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 1.1 | Đơn vị vận chuyển cần tích hợp MVP? | ☐ Chỉ Viettel Post | | |
| | | ☐ Viettel Post + GHTK | | |
| | | ☐ Viettel Post + GHTK + GHN | | |
| 1.2 | Nếu nhiều đơn vị, ưu tiên đơn vị nào? | 1. ___ 2. ___ 3. ___ | | Thứ tự build |

---

### 2. Flow nghiệp vụ

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 2.1 | Thời điểm tạo đơn giao vận? | ☐ Tự động sau khi xác nhận đơn hàng | | |
| | | ☐ Nhân viên tạo thủ công | | |
| | | ☐ Tự động sau khi xuất kho | | |
| 2.2 | Ai có quyền tạo đơn giao vận? | ☐ NV bán hàng | | Liên quan phân quyền |
| | | ☐ NV kho | | |
| | | ☐ Cả hai | | |
| 2.3 | Có cho phép chọn loại dịch vụ? | ☐ Mặc định 1 loại | | VD: Standard, Express |
| | | ☐ Cho chọn nhiều loại | | |
| 2.4 | Có cho phép chọn đơn vị VC? | ☐ Cố định 1 đơn vị | | Nếu tích hợp nhiều |
| | | ☐ Cho chọn tại thời điểm tạo | | |

---

### 3. COD - Thu hộ

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 3.1 | Có sử dụng COD (thu hộ)? | ☐ Có | | **Quan trọng** |
| | | ☐ Không | | |
| 3.2 | Tỷ lệ đơn COD ước tính? | ___% | | Để đánh giá độ ưu tiên |
| 3.3 | Flow đối soát COD như thế nào? | ☐ Manual - NV check từng đơn | | |
| | | ☐ Tự động sync từ nhà vận chuyển | | |
| 3.4 | COD tích hợp với công nợ? | ☐ Có - tự động cập nhật | | Liên quan `accounts` |
| | | ☐ Không - track riêng | | |

---

### 4. Phí vận chuyển

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 4.1 | Ai trả phí vận chuyển? | ☐ Khách hàng (luôn luôn) | | |
| | | ☐ Shop (luôn luôn) | | |
| | | ☐ Tùy đơn hàng | | |
| 4.2 | Có cần ước tính phí trước? | ☐ Có - call API tính phí | | Hiển thị khi tạo đơn |
| | | ☐ Không - chỉ biết sau khi tạo | | |
| 4.3 | Phí VC có hiển thị trên đơn hàng? | ☐ Có | | |
| | | ☐ Không | | |
| 4.4 | Có chính sách miễn phí VC? | ☐ Có (đơn từ ___ VNĐ) | | VD: Đơn > 500k free ship |
| | | ☐ Không | | |

---

### 5. Địa điểm gửi hàng

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 5.1 | Gửi hàng từ bao nhiêu địa điểm? | ☐ 1 kho/địa điểm | | |
| | | ☐ Nhiều chi nhánh: ___ điểm | | |
| 5.2 | Cách chọn địa điểm gửi? | ☐ Tự động theo kho xuất | | Nếu multi-location |
| | | ☐ NV chọn thủ công | | |
| 5.3 | Đã có địa chỉ đăng ký với VP? | ☐ Có | | Cần để tích hợp |
| | | ☐ Chưa | | |

---

### 6. In phiếu giao hàng

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 6.1 | Có cần in phiếu từ CRM? | ☐ Có - in từ CRM | | |
| | | ☐ Không - lên portal nhà VC in | | |
| 6.2 | Nếu in từ CRM, template nào? | ☐ Mẫu chuẩn Viettel Post | | |
| | | ☐ Mẫu custom theo yêu cầu | | |
| 6.3 | Có in kèm hóa đơn bán hàng? | ☐ Có | | |
| | | ☐ Không | | |

---

### 7. Thông báo cho khách hàng

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 7.1 | Gửi thông báo khi tạo vận đơn? | ☐ Có | | Mã vận đơn, link tracking |
| | | ☐ Không | | |
| 7.2 | Gửi thông báo khi cập nhật TT? | ☐ Có | | Đang giao, Đã giao... |
| | | ☐ Không | | |
| 7.3 | Kênh gửi thông báo? | ☐ Zalo OA | | Chọn nhiều |
| | | ☐ SMS | | |
| | | ☐ Email | | |
| 7.4 | Có template tin nhắn sẵn? | ☐ Có (cung cấp sau) | | |
| | | ☐ DCNET đề xuất | | |

---

### 8. Đơn hàng đặc biệt

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 8.1 | Đơn Fitting có cần giao hàng? | ☐ Có (phụ kiện phát sinh) | | |
| | | ☐ Không | | |
| 8.2 | Đơn Coaching có cần giao hàng? | ☐ Có (tài liệu, dụng cụ) | | |
| | | ☐ Không | | |
| 8.3 | Đơn thu cũ đổi mới - lấy hàng cũ? | ☐ Có - cần giao vận ngược | | Shipper lấy hàng cũ về |
| | | ☐ Không - khách tự mang | | |
| 8.4 | Đơn bảo hành - giao trả hàng? | ☐ Có | | Sau khi sửa xong |
| | | ☐ Không - khách tự lấy | | |

---

### 9. Xử lý hoàn/trả

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 9.1 | Khi đơn hoàn, xử lý như thế nào? | ☐ Tự động cập nhật tồn kho | | |
| | | ☐ Manual - NV xác nhận | | |
| 9.2 | Có tạo phiếu nhập kho tự động? | ☐ Có | | |
| | | ☐ Không | | |
| 9.3 | Có ghi nhận lý do hoàn? | ☐ Có | | Để phân tích |
| | | ☐ Không | | |

---

### 10. API & Tài khoản

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 10.1 | Đã có tài khoản Viettel Post? | ☐ Có | | |
| | | ☐ Chưa - cần đăng ký | | |
| 10.2 | Loại tài khoản VP? | ☐ Cá nhân | | |
| | | ☐ Doanh nghiệp | | |
| 10.3 | API Token/Credentials? | *(Nhận sau khi confirm)* | | Bảo mật |
| 10.4 | Nếu có GHTK - đã có TK? | ☐ Có ☐ Chưa ☐ N/A | | |
| 10.5 | Nếu có GHN - đã có TK? | ☐ Có ☐ Chưa ☐ N/A | | |

---

### 11. Báo cáo vận chuyển

| # | Câu hỏi | Lựa chọn | Trả lời | Ghi chú |
|---|---------|----------|---------|---------|
| 11.1 | Cần báo cáo gì về vận chuyển? | ☐ Số đơn giao thành công | | Chọn nhiều |
| | | ☐ Số đơn hoàn/trả | | |
| | | ☐ Tổng phí vận chuyển | | |
| | | ☐ Thời gian giao trung bình | | |
| | | ☐ Tỷ lệ giao thành công | | |
| 11.2 | Báo cáo theo chiều nào? | ☐ Theo thời gian | | |
| | | ☐ Theo nhà vận chuyển | | |
| | | ☐ Theo chi nhánh | | |

---

## Tóm tắt độ ưu tiên câu hỏi

| Mức độ | Câu hỏi | Lý do |
|--------|---------|-------|
| **Cao** | 1.1, 2.1, 3.1, 4.1, 10.1 | Ảnh hưởng scope và kiến trúc |
| **TB** | 2.2, 3.3, 5.1, 7.1, 8.3 | Ảnh hưởng flow nghiệp vụ |
| **Thấp** | 6.x, 11.x | Có thể làm sau |

---

## Ghi chú từ buổi họp

<!-- Điền sau khi họp -->

| Ngày | Người confirm | Nội dung |
|------|---------------|----------|
| | | |

---

## Liên quan

- [KICKOFF_QUESTIONS.md](../KICKOFF_QUESTIONS.md) - Tổng hợp câu hỏi
- [FEATURE_SPECIFICATION.md](../../feature/FEATURE_SPECIFICATION.md) - Đặc tả chức năng
- [ERPNEXT_COVERAGE_ANALYSIS.md](../../feature/ERPNEXT_COVERAGE_ANALYSIS.md) - ERPNext coverage analysis

---

*Cập nhật: 2025-12-08*
