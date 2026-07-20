# 04 - Danh mục NCC: Vấn đề cần Clarify

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

## 1. Bảng giá & Ưu đãi NCC

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 1.1 | "Cơ sở tính KM đầu vào" cụ thể là gì? Chiết khấu % theo doanh số mua? Volume discount? Quà tặng kèm? Hay tất cả? | :orange_circle: High | Quyết định cách config Pricing Rule. Nếu phức tạp cần custom code | Recommend: Config Pricing Rule cho CK% + CK tiền. Quà tặng xử lý manual | ERP spec 3.0.2 |
| 1.2 | Bảng giá NCC cần quản lý theo từng NCC riêng hay theo nhóm NCC/thương hiệu? | :yellow_circle: Medium | Quyết định số lượng Price List cần tạo | Recommend: 1 Price List/NCC (hoặc /thương hiệu nếu NCC đại diện nhiều hãng) | ERP spec 3.0.2 |

---

## 2. Phân loại NCC

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 2.1 | Cấu trúc nhóm NCC cụ thể? VD: Cấp 1 (Nội địa / Quốc tế) → Cấp 2 (Theo hãng: Titleist, Callaway, Ping...) | :yellow_circle: Medium | Setup Supplier Group tree | Recommend: 2 cấp như VD, bổ sung khi cần | SRS 3.4.2 |
| 2.2 | Mã NCC: Tự sinh (SUP-00001) hay theo quy ước riêng (VD: NCC-TL-001)? Hay giữ mã từ BRAVO? | :yellow_circle: Medium | Config Naming Series | Recommend: Tự sinh, thêm custom field `custom_bravo_code` để lưu mã cũ khi migrate | SRS 3.4.2 |

---

## 3. Đánh giá NCC (chỉ TM)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 3.1 | Thăng Long TM có cần tính năng "Đánh giá NCC" (Supplier Scorecard) không? Nếu có, tiêu chí đánh giá là gì? (giao hàng đúng hạn, chất lượng, giá cả, hỗ trợ...) | :yellow_circle: Medium | Quyết định có config Supplier Scorecard hay không | Recommend: Bỏ qua giai đoạn đầu, bổ sung sau khi đã ổn định | SRS TM 3.4.1 |

---

## Thống kê

| Priority | Số lượng |
|----------|----------|
| :orange_circle: High | 1 |
| :yellow_circle: Medium | 3 |
| **Tổng** | **4** |

> **Ghi chú:** Không có Critical — module này có thể triển khai với giá trị mặc định (Recommend).
> Nếu khách hàng không trả lời kịp, dùng Recommend làm default, confirm sau.
