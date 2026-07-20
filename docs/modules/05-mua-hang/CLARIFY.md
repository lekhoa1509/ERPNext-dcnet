# 05 - Mua hàng: Vấn đề cần Clarify

> **Ngày tạo:** 17/02/2026
> **Trạng thái:** Chờ khách hàng xác nhận

---

## Quy ước

| Icon | Ý nghĩa |
|------|---------|
| :red_circle: | **Critical** — Block triển khai, cần trả lời trước khi code |
| :orange_circle: | **High** — Ảnh hưởng thiết kế, cần trả lời trước Sprint |
| :yellow_circle: | **Medium** — Có thể dùng giá trị mặc định, confirm sau |
| :green_circle: | **Resolved** — Đã có câu trả lời |

---

## 1. Features đặc thù

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 1.1 | Quy tắc đặt tên file ảnh để import hàng loạt? VD: `{item_code}.jpg` hay `{model}_{sku}.jpg`? Có nhiều ảnh / 1 SP không? | :yellow_circle: Medium | Quyết định logic match file → Item | Recommend: `{item_code}.jpg` (1 ảnh chính / SP) | 3.1.2 |
| 1.2 | "Nhập hàng theo mã vạch" — quét barcode để thêm Item vào phiếu nhập, hay quét từng serial number khi nhập kho? | :orange_circle: High | Nếu quét serial → cần client script phức tạp hơn | Recommend: Quét Item barcode để add row, serial nhập manual hoặc batch | 3.1.10 |
| 1.3 | "Vòng đời SP" — là thời hạn hết hạn (shelf life, VD: kem chống nắng 2 năm) hay là chu kỳ kinh doanh (VD: model gậy 2024 → ngừng bán 2026)? | :orange_circle: High | Quyết định dùng `shelf_life_in_days` hay `end_of_life` trên Item | Recommend: Product lifecycle (end_of_life), không phải shelf life | 3.1.11 |

---

## 2. Workflow & Trạng thái

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 2.1 | Trạng thái PO "Đã gửi NCC" và "Đang giao" — dùng Workflow ERPNext (phức tạp, cần role assignment) hay dùng custom field Select (đơn giản, user tự cập nhật)? | :orange_circle: High | Workflow = chắc chắn nhưng phức tạp. Custom field = linh hoạt hơn | Recommend: Custom field `custom_supplier_status` (Select) — đơn giản, đủ dùng | 3.1.5 |
| 2.2 | Phiếu nhập (Purchase Receipt) "Chờ duyệt" — ai là người duyệt? Duyệt tất cả hay chỉ duyệt khi vượt ngưỡng giá trị (VD: >100 triệu)? | :red_circle: Critical | Quyết định Workflow design | Recommend: Workflow: Draft → Chờ duyệt (TP Kho) → Đã nhập (KT). Tất cả phiếu nhập đều cần duyệt. | 3.1.16 |

---

## 3. Custom DocTypes vs Extend ERPNext

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 3.1 | "Kế hoạch mua hàng" (3.2.1) — màn hình có nhiều trường đặc thù (Family, Year, Category, Shaft, SL tháng 1-12). Tạo custom DocType mới hay dùng Material Request + custom fields? | :red_circle: Critical | Quyết định kiến trúc: 1 DocType mới ~5 ngày vs extend MR ~3 ngày | Recommend: Custom DocType "Purchase Plan" — MR không phù hợp với format này | 3.2.1 |
| 3.2 | "Lệnh nhập hàng" (3.2.4) — document riêng trước Purchase Receipt hay extend Purchase Receipt với workflow? | :orange_circle: High | DocType riêng = thêm 1 bước, phức tạp hơn. Extend PR = đơn giản hơn | Recommend: Extend Purchase Receipt (custom fields + workflow). Không cần DocType riêng. | 3.2.4 |
| 3.3 | "Trả lại NCC" — spec mô tả 2 bước (Lệnh xuất trả → Phiếu xuất trả). ERPNext gộp 1 bước (Return). Có cần tách 2 bước (approval trước khi xuất kho)? | :orange_circle: High | 2 bước = thêm Workflow trên Return. 1 bước = dùng ERPNext standard | Recommend: Workflow trên Purchase Receipt Return: Draft (Lệnh) → Approved → Submitted (Phiếu) | 3.2.7 |
| 3.4 | "Đề nghị thanh toán" (3.2.10) — document phê duyệt riêng trước Payment Entry, hay Workflow trên Payment Entry (Draft → Đề nghị → Approved → Paid)? | :orange_circle: High | DocType riêng = thêm 1 layer. Workflow = đơn giản hơn | Recommend: Workflow trên Payment Entry. Nếu khách cần print format riêng cho "Đề nghị TT" → tạo Print Format. | 3.2.10 |

---

## 4. Kế hoạch giao hàng

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 4.1 | "Kế hoạch giao hàng" (3.2.3) có rất nhiều trường đặc thù (PO Number, Vendor name, Ship mode, EAN, UPC, Stastic factor...). Đây có phải format nhập từ Excel của hãng (Titleist/FootJoy) không? | :red_circle: Critical | Quyết định DocType schema. Nếu import từ Excel → cần Data Import template match. | Recommend: Custom DocType "Delivery Schedule" với data import từ Excel hãng. | 3.2.3 |
| 4.2 | Tính năng "Cảnh báo tên VT chính thức khác tên trên danh mục" (3.2.3) — tên VT trên hệ thống vs tên hãng gửi. Compare bằng gì? Exact match hay fuzzy? | :yellow_circle: Medium | Client script comparison logic | Recommend: So sánh `item_name` vs trường `vendor_item_name`. Alert khi khác. | 3.2.3 |

---

## 5. Import Process (từ IMPORT_PROCESS_SPECIFICATION)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 5.1 | Legacy analysis (import-management/) đã thiết kế 5 custom DocTypes (Import Schedule, Pre-Order, Shipment Tracking, Customs Clearance, Goods Receipt Check). Có áp dụng không hay simplify? | :orange_circle: High | 5 DocTypes = rất nhiều effort (~15 ngày). Simplify = ít hơn nhưng mất detail. | Recommend: Giai đoạn đầu chỉ làm 2 DocTypes core (Purchase Plan + Delivery Schedule). Shipment/Customs/Pre-Order để phase sau. | IMPORT_PROCESS |
| 5.2 | Pre-Order từ đại lý cấp 1 — có cần tính năng này trong T3 không? (Đại lý gửi pre-order, TLTM review, BLD approve) | :yellow_circle: Medium | Nếu có → thêm 1 DocType + Workflow. Nếu không → skip. | Recommend: Skip T3. Đại lý dùng Excel gửi pre-order. Làm sau khi ổn định. | IMPORT_PROCESS |
| 5.3 | Shipment Tracking + Customs Clearance — có cần tracking chi tiết (state machine với 7 trạng thái) trong T3 hay chỉ cần basic (custom fields trên PO)? | :yellow_circle: Medium | Full tracking = 2 DocTypes mới. Basic = custom fields trên PO. | Recommend: Basic — custom fields trên PO (ship_status, customs_status). Full tracking làm T4 hoặc sau. | IMPORT_PROCESS |

---

## Thống kê

| Priority | Số lượng |
|----------|----------|
| :red_circle: Critical | 3 |
| :orange_circle: High | 6 |
| :yellow_circle: Medium | 4 |
| **Tổng** | **13** |

> **Ghi chú:** 3 Critical items (2.2, 3.1, 4.1) cần trả lời trước khi bắt đầu code.
> Các High items ảnh hưởng thiết kế nhưng có Recommend để dùng default.
