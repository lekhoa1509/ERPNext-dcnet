# Module 07 - Kho hàng: Vấn đề cần Clarify

> **Ngày tạo:** 16/02/2026
> **Trạng thái:** Chờ khách hàng xác nhận
> **Người phụ trách:** DCNET Team
> **Ảnh hưởng:** Không thể triển khai một số features nếu chưa clarify

---

## Quy ước

| Icon | Ý nghĩa |
|------|---------|
| :red_circle: | **Critical** — Block triển khai, cần trả lời trước khi code |
| :orange_circle: | **High** — Ảnh hưởng thiết kế, cần trả lời trước Sprint |
| :yellow_circle: | **Medium** — Có thể dùng giá trị mặc định, confirm sau |
| :white_circle: | **Low** — Nice-to-have, không block |
| :green_circle: | **Resolved** — Đã có câu trả lời |

---

## 1. Cấu trúc kho (Warehouse Setup)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 1.1 | Có bao nhiêu kho? Tên cụ thể từng kho? | :red_circle: Critical | Warehouse master setup | | README.md |
| 1.2 | Kho nào cho phép xuất âm (negative stock)? | :orange_circle: High | Stock Settings config | Recommend: KHÔNG | README.md |
| 1.3 | Transit warehouse: 1 kho chung hay mỗi tuyến 1 kho? | :yellow_circle: Medium | Warehouse hierarchy | Recommend: 1 kho Transit chung | STOCK_ACCOUNTING_INTEGRATION.md |
| 1.4 | Kho nào cho phép xuất trực tiếp (không cần PO)? | :yellow_circle: Medium | Workflow config | VD: Kho CCDC xuất thẳng | STOCK_ACCOUNTING_INTEGRATION.md |

---

## 2. Phương pháp tính giá vốn (Valuation)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 2.1 | Phương pháp giá vốn: Trung bình tháng hay Moving Average? | :red_circle: Critical | Valuation method, có thể cần 3-4 tuần custom | Recommend: Moving Average (ERPNext native) | README.md, STOCK_ACCOUNTING_INTEGRATION.md |
| 2.2 | ERP spec ghi "trung bình tháng", SRS ghi "bình quân gia quyền" — chính xác là gì? | :red_circle: Critical | Cùng câu 2.1, conflict giữa 2 tài liệu | | STOCK_MODULE_CONNECTIONS.md |

**Phân tích:**
- ERPNext chỉ hỗ trợ **FIFO** và **Moving Average** (native)
- **Trung bình tháng** cần custom script chạy cuối tháng (thêm 2-3 tuần effort)
- **Moving Average** cho kết quả tương đương, real-time, TT200 chấp nhận
- Xem chi tiết: `analysis/STOCK_ACCOUNTING_INTEGRATION.md` Section 4

---

## 3. Tracking sản phẩm (Batch / Serial)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 3.1 | Sản phẩm nào cần tracking theo lô (Batch)? | :orange_circle: High | Item Master config | | README.md |
| 3.2 | Sản phẩm nào cần tracking theo serial? | :orange_circle: High | Item Master config | | README.md |

**Đề xuất:**

| Loại SP | Batch | Serial | Lý do |
|---------|:-----:|:------:|-------|
| Golf Clubs | Yes | Yes | Giá trị cao, cần track từng cái |
| Golf Balls | Yes | No | Track theo lô, không từng quả |
| Apparel | Yes | No | Track theo lô (size/color) |
| Accessories | Yes | No | Track theo lô |
| Golf Bags | Yes | Yes | Giá trị trung-cao |
| Training Aids | No | No | Giá trị thấp |

---

## 4. Barcode & Tem nhãn

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 4.1 | Barcode format: EAN-13, Code128, hay QR? | :orange_circle: High | Barcode generation logic | | README.md |
| 4.2 | Kích thước tem nhãn? (30x20mm, 50x25mm, ...) | :yellow_circle: Medium | Print template | | README.md |
| 4.3 | Có tích hợp máy scan barcode không? Model nào? | :yellow_circle: Medium | Hardware integration | | README.md |

---

## 5. Kiểm kê (Stock Reconciliation)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 5.1 | Kiểm kê định kỳ hay đột xuất? Tần suất? | :yellow_circle: Medium | Scheduled job, freeze period | | README.md |
| 5.2 | Freeze kho khi kiểm kê cần approval từ ai? | :yellow_circle: Medium | Custom workflow | Propose: Thủ kho chênh lệch nhỏ, GĐ chênh lệch lớn | STOCK_ACCOUNTING_INTEGRATION.md |
| 5.3 | Threshold chênh lệch cần duyệt Giám đốc? | :yellow_circle: Medium | Approval matrix | VD: > 5.000.000 VND | STOCK_ACCOUNTING_INTEGRATION.md |

---

## 6. Phê duyệt (Approval Workflow)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 6.1 | Phê duyệt phiếu xuất: trước hay sau khi submit? | :orange_circle: High | Workflow design | | README.md |

---

## 7. Kế toán kho (Stock Accounting)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 7.1 | Hàng ký gửi dùng TK 1567 hay tạo TK mới? | :orange_circle: High | COA update, Warehouse mapping | TK 1567 có sẵn trong COA v2 | STOCK_ACCOUNTING_INTEGRATION.md |
| 7.2 | Stock Adjustment dùng TK 6329 hay 632? | :orange_circle: High | Default Accounts config | Recommend: 6329 (tách biệt COGS) | STOCK_ACCOUNTING_INTEGRATION.md |
| 7.3 | Trade-in TK 1565 tách riêng — confirm? | :orange_circle: High | Warehouse mapping | Đã tạo trong COA v2 | STOCK_ACCOUNTING_INTEGRATION.md |

---

## 8. Trade-in (Đặc thù DCNET)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 8.1 | Giá SP cũ > giá SP mới → KH có được nhận tiền chênh lệch? | :orange_circle: High | Bút toán, cashflow | | STOCK_ACCOUNTING_INTEGRATION.md |
| 8.2 | SP cũ sau khi thu về xử lý thế nào? (bán lại, thanh lý, trả hãng?) | :orange_circle: High | Workflow, báo cáo | | STOCK_ACCOUNTING_INTEGRATION.md |
| 8.3 | Có cần tạo hóa đơn cho SP cũ không? (ảnh hưởng thuế) | :orange_circle: High | Tax, invoice flow | | STOCK_ACCOUNTING_INTEGRATION.md |

---

## 9. Báo cáo (Reports)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 9.1 | BC nhập xuất tồn: theo format BRAVO cũ hay TT200 mới? | :orange_circle: High | Report development | Recommend: TT200 | STOCK_ACCOUNTING_INTEGRATION.md |

---

## Thống kê

| Priority | Số lượng | Trạng thái |
|----------|----------|-----------|
| :red_circle: Critical | 3 | Chờ |
| :orange_circle: High | 13 | Chờ |
| :yellow_circle: Medium | 6 | Chờ (có recommend) |
| **Tổng** | **22** | **0 resolved** |

---

**Last Updated:** 16/02/2026
