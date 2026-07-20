# 06 - Báo cáo Phân tích: Vấn đề cần Clarify

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

## 1. Tồn kho & Định giá (liên quan FEAT 14.5)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 1.1 | Phương pháp tính giá vốn: Moving Average hay FIFO? (ERPNext không hỗ trợ "trung bình tháng" như BRAVO) | :orange_circle: High | 14.5.2 Giá trị tồn kho — ảnh hưởng valuation rate | Recommend: Moving Average (gần nhất với trung bình, ERPNext hỗ trợ tốt) | ERP_SPECIFICATION.md + COA_ANALYSIS.md |
| 1.2 | Reorder Level (mức MIN) data lấy từ đâu? BRAVO có sẵn hay cần setup mới? | :yellow_circle: Medium | 14.5.3 SP gần định mức — cần MIN level cho mỗi Item-Warehouse | Recommend: Setup mới, import từ Excel template | FEAT 14.5 |

---

## 2. Phân tích hàng hóa (liên quan ERP 6.3)

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 2.1 | Tiêu chí "hàng bán chậm" cụ thể? Bao nhiêu ngày tồn kho + bao nhiêu đơn bán/tháng được coi là "chậm"? | :red_circle: Critical | 6.3.1 — Business logic xác định hàng chậm | Recommend: Config được (mặc định: >90 ngày tồn + <3 bán/tháng). Khách có thể tùy chỉnh ngưỡng. | ERP 6.3.1 |
| 2.2 | "Vòng đời sản phẩm" = lifecycle do nhà sản xuất công bố (model year) hay tự định nghĩa theo kinh nghiệm kinh doanh? | :red_circle: Critical | 6.3.2 — Cần biết ai nhập data vòng đời, lấy từ đâu | Recommend: Custom field trên Item, nhập thủ công (launch_date + lifecycle_months). NCC cung cấp info. | ERP 6.3.2 |
| 2.3 | "Đại lý" trong "điều chuyển cho đại lý": đại lý là khách hàng (Customer) hay kho con (child Warehouse)? | :orange_circle: High | 6.3.3 — Ảnh hưởng cách track: Stock Entry (warehouse) hay Delivery Note (customer) | Recommend: Đại lý = child Warehouse (thuộc Warehouse Group "Đại lý"). Dùng Material Transfer giữa kho. | ERP 6.3.3 |
| 2.4 | Phân biệt "sale" và "thanh lý" cụ thể? Sale = giảm giá tạm thời (campaign)? Thanh lý = giảm giá vĩnh viễn (ngừng kinh doanh)? | :orange_circle: High | 6.3.4 — Cần tag lý do giảm giá trên Pricing Rule | Recommend: Sale = Pricing Rule có thời hạn (valid_from → valid_upto). Thanh lý = đánh dấu Item `custom_is_liquidation = 1`. | ERP 6.3.4 |
| 2.5 | Mốc cảnh báo "60 ngày" và "45 ngày" có cần config được không, hay fix cứng? | :yellow_circle: Medium | 6.3.2 — UI filter hay hardcode | Recommend: Config được qua DCNET Settings. Mặc định 60 + 45. | ERP 6.3.2 |

---

## 3. Delivery & Scope

| # | Câu hỏi | Priority | Ảnh hưởng | Trả lời | Nguồn |
|---|---------|----------|-----------|---------|-------|
| 3.1 | Module 06 bàn giao T3 nhưng nhiều reports cần data từ T4 (Stock, Sales). Bàn giao T3 chỉ cần framework + sample data, hay cần reports chạy được với data thật? | :orange_circle: High | Timeline — nếu cần data thật thì phải dời sang T4 | Recommend: T3 bàn giao framework (report structure + UI) + test với sample data. T4 activate khi có Stock/Sales data. | TIMELINE_2026.md |
| 3.2 | Report overlap giữa module 06 và module 08 "BC Kho" (T4): FEAT 14.5.1 "tồn kho theo kho" có trùng với ERP 6.1.2 "tồn kho theo kho" không? | :yellow_circle: Medium | Có thể trùng report → cần phân ranh | Recommend: Module 06 = phân tích (so sánh, xu hướng, cảnh báo). Module 08 = listing/tổng hợp (nhập-xuất-tồn). | source-mapping.md |

---

## Thống kê

| Priority | Số lượng |
|----------|----------|
| :red_circle: Critical | 2 |
| :orange_circle: High | 3 |
| :yellow_circle: Medium | 2 |
| **Tổng** | **7** |
