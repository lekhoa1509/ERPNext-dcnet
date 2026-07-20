# 06 - Báo cáo Phân tích: Spec → ERPNext Mapping

> **Nguồn:** FEATURE_SPECIFICATION.md Section 14.5 + ERP_SPECIFICATION.md Section 6.3
> **ERPNext:** v16 — Stock Module (Reports)
> **Cập nhật:** 17/02/2026

## Quy ước Tags

| Tag | Nghĩa | Action |
|-----|--------|--------|
| `USE` | ERPNext có sẵn, dùng ngay | Config + test |
| `CFG` | ERPNext có, cần config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext có, cần mở rộng | Custom field, client/server script |
| `NEW` | ERPNext không có, cần build | Custom DocType, module mới |
| `REF` | Thuộc module khác | Tham chiếu |

---

## FEAT 14.5. Báo cáo Kho (3 features)

> Nguồn: FEATURE_SPECIFICATION.md Section 14.5

### 14.5.1. Báo cáo tồn kho theo kho

- **Tag:** `USE`
- **Spec yêu cầu:** Báo cáo tồn kho theo kho
- **ERPNext:** Stock Balance Report (`stock/report/stock_balance/`)
- **ERPNext đã có:**
  - Stock Balance report: filter by Warehouse, Item Group, Item Code
  - Hiển thị: Opening Qty, In Qty, Out Qty, Balance Qty, Balance Value
  - Group by Warehouse hoặc Item Group
  - Export Excel/PDF
- **Gap:** Không có gap đáng kể. ERPNext report đáp ứng đủ.
- **Action:**
  1. Config Warehouse tree structure (phụ thuộc module 07)
  2. Config Item Group hierarchy (phụ thuộc module 03)
  3. Test report với sample data
  4. Config permissions (ai được xem kho nào)
- **Effort:** 0.5 ngày
- **Dependency:** Module 07 (Warehouse setup), Module 03 (Item master)

### 14.5.2. Báo cáo giá trị tồn kho của từng kho

- **Tag:** `USE`
- **Spec yêu cầu:** Báo cáo giá trị tồn kho của từng kho
- **ERPNext:** Stock Balance Report + Stock Value Report
- **ERPNext đã có:**
  - Stock Balance report có cột "Balance Value" (= qty × valuation rate)
  - Warehouse Wise Stock Value report (nếu bật Perpetual Inventory)
  - Stock Projected Qty report
  - Valuation method: FIFO hoặc Moving Average (config trong Item/Stock Settings)
- **Gap:** Không có gap đáng kể. Cần đảm bảo Perpetual Inventory được bật.
- **Action:**
  1. Bật Perpetual Inventory trong Stock Settings
  2. Config valuation method (FIFO hoặc Moving Average — phụ thuộc quyết định kế toán)
  3. Test report accuracy với sample data
- **Effort:** 0.5 ngày
- **Dependency:** Module 07 (Stock setup), Kế toán (valuation method decision)
- **⚠️ Clarify:** Phương pháp tính giá vốn — xem CLARIFY.md #1.1

### 14.5.3. Thống kê sản phẩm dưới/gần định mức tồn kho

- **Tag:** `CFG`
- **Spec yêu cầu:** Thống kê các sản phẩm đang dưới và gần định mức tồn kho cùng mức tồn kho hiện tại. Định nghĩa: SP gần định mức = xếp theo SP có mức tồn kho gần với mức MIN trong định mức tồn kho nhất.
- **ERPNext:** Item Shortage Report + Reorder Level (Item DocType)
- **ERPNext đã có:**
  - Item có field `reorder_levels` (child table): Warehouse, Warehouse Reorder Level (MIN), Warehouse Reorder Qty, Material Request Type
  - Item Shortage Report: hiển thị items có qty < reorder level
  - Auto Material Request: tự tạo Material Request khi qty < reorder level
- **Gap:**
  - ERPNext chỉ hiển thị items **đã dưới** min, không sort theo "gần min nhất"
  - Spec muốn: xếp theo khoảng cách (current qty - min), tức SP nào gần min nhất lên trên
  - Cần custom report hoặc extend Item Shortage Report
- **Action:**
  1. Config Reorder Level cho tất cả Items (phụ thuộc data BRAVO)
  2. Tạo Script Report "Sản phẩm gần định mức tồn kho" hoặc extend Item Shortage Report
  3. Report hiển thị: Item, Warehouse, Current Qty, Min Level, Khoảng cách (Qty - Min), Status (Dưới/Gần/Đủ)
  4. Sort by khoảng cách ascending (gần min nhất lên đầu)
- **Effort:** 1 ngày (0.5 config + 0.5 custom report)
- **Dependency:** Module 03 (Item), Module 07 (Warehouse + Reorder Level)

---

## ERP 6.3. Báo cáo Phân tích (4 features)

> Nguồn: ERP_SPECIFICATION.md Section 6.3

### 6.3.1. Báo cáo hàng tồn chậm

- **Tag:** `EXT`
- **Spec yêu cầu:** Hàng bán chậm + Đề xuất sale / điều chuyển
- **ERPNext:** Stock Ageing Report (`stock/report/stock_ageing/`)
- **ERPNext đã có:**
  - Stock Ageing report: hiển thị tuổi tồn kho (số ngày tồn) theo Item + Warehouse
  - Cột: Item, Warehouse, Batch, Age (days), Qty, Value
  - Filter by Warehouse, Item Group, range (0-30, 30-60, 60-90, >90 days)
- **Gap:**
  - ERPNext không có khái niệm "bán chậm" — chỉ có "tuổi tồn kho"
  - Thiếu: so sánh tốc độ bán vs tồn kho để xác định hàng chậm
  - Thiếu: cột "Đề xuất" (sale / điều chuyển) — cần business logic
  - Cần kết hợp Stock Ageing + Sales Analytics để tính "chậm bán"
- **Action:**
  1. Tạo Script Report "Báo cáo Hàng tồn chậm" (extend Stock Ageing)
  2. Logic: so sánh avg daily sales (từ Stock Ledger) vs current qty → tính "days of stock"
  3. Thêm cột: Avg Daily Sales, Days of Stock, Suggestion (Sale/Điều chuyển/Giữ)
  4. Business rule đề xuất: >90 ngày tồn + <X bán/tháng → "Đề xuất sale"; có kho khác qty thấp → "Điều chuyển"
  5. Filter: Warehouse, Item Group, tuổi tồn tối thiểu
- **Effort:** 3 ngày (1 ngày logic + 1 ngày report + 1 ngày test)
- **Dependency:** Module 07 (Stock Ledger data), Module 12 (Sales data cho avg daily sales — T4)
- **⚠️ Clarify:** Tiêu chí "bán chậm" cụ thể — xem CLARIFY.md #2.1

### 6.3.2. Báo cáo hàng sắp hết vòng đời

- **Tag:** `NEW`
- **Spec yêu cầu:** Hàng sắp hết vòng đời — còn 60 ngày + còn 45 ngày
- **ERPNext:** Không có built-in. ERPNext không có khái niệm "vòng đời sản phẩm" (product lifecycle).
- **ERPNext đã có:**
  - Item có field `end_of_life` (date) — nhưng ít được dùng, chỉ disable Item khi hết hạn
  - Batch có field `expiry_date` — cho hàng có hạn sử dụng (thực phẩm, thuốc)
  - Không có report "sắp hết vòng đời"
- **Gap:**
  - ERPNext `end_of_life` là end of ITEM (ngừng kinh doanh), khác với "vòng đời sản phẩm" (lifecycle = từ lúc ra mắt đến khi ngừng)
  - Spec cần: track launch date + lifecycle duration → tính ngày hết vòng đời
  - Cần alert: "còn 60 ngày" và "còn 45 ngày"
  - Áp dụng cho ngành golf: model club/giày thường có lifecycle 1-2 năm
- **Action:**
  1. Custom fields trên Item: `custom_launch_date` (Date), `custom_lifecycle_months` (Int)
  2. Computed: `end_of_lifecycle = launch_date + lifecycle_months`
  3. Tạo Script Report "Hàng sắp hết vòng đời"
  4. Filter: còn ≤60 ngày (cảnh báo), còn ≤45 ngày (khẩn cấp)
  5. Cột: Item, Launch Date, Lifecycle (months), End Date, Còn lại (ngày), Qty tồn, Value tồn, Status
  6. Có thể tái sử dụng field `end_of_life` của ERPNext hoặc dùng custom field riêng
- **Effort:** 3 ngày (1 ngày custom field + 1 ngày report + 1 ngày test)
- **Dependency:** Module 03 (Item — custom fields)
- **⚠️ Clarify:** "Vòng đời" = lifecycle nhà sản xuất (model year) hay tự định nghĩa? — xem CLARIFY.md #2.2

### 6.3.3. Báo cáo hàng điều chuyển

- **Tag:** `EXT`
- **Spec yêu cầu:** Điều chuyển giữa các kho + Điều chuyển cho đại lý
- **ERPNext:** Stock Entry (Material Transfer) + Stock Entry report
- **ERPNext đã có:**
  - Stock Entry với purpose "Material Transfer": chuyển hàng giữa 2 warehouse
  - Stock Entry với purpose "Material Transfer for Manufacture": chuyển cho sản xuất
  - Stock Entry List/Report: filter by purpose, source/target warehouse
  - Delivery Note có thể dùng cho "điều chuyển cho đại lý" (ship to dealer)
- **Gap:**
  - Không có report **tổng hợp** điều chuyển (summary by period, by warehouse pair)
  - "Điều chuyển cho đại lý" — đại lý là Customer hay Warehouse con? Cần clarify
  - Thiếu: phân tách "điều chuyển nội bộ" vs "điều chuyển đại lý"
- **Action:**
  1. Tạo Script Report "Báo cáo Điều chuyển hàng"
  2. Data source: Stock Entry where purpose = "Material Transfer"
  3. Group by: period (tuần/tháng), source warehouse → target warehouse
  4. Cột: Thời gian, Từ kho, Đến kho, Item, Qty, Value, Loại (Nội bộ/Đại lý)
  5. Phân loại: nếu target warehouse thuộc "Đại lý" group → tag "Điều chuyển đại lý"
  6. Summary: tổng qty + value theo chiều (kho A → kho B)
- **Effort:** 2 ngày (1 ngày report + 1 ngày test)
- **Dependency:** Module 07 (Warehouse hierarchy), Module 15 (Chi nhánh/Đại lý — T4)
- **⚠️ Clarify:** Đại lý là Customer hay Warehouse con? — xem CLARIFY.md #2.3

### 6.3.4. Báo cáo hàng thanh lý / sale

- **Tag:** `NEW`
- **Spec yêu cầu:** Sale campaign + Thanh lý
- **ERPNext:** Pricing Rule (discount campaigns) + không có thanh lý concept
- **ERPNext đã có:**
  - Pricing Rule: set discount % hoặc giá đặc biệt theo thời gian, item group, customer group
  - Promotional Scheme: gom nhiều Pricing Rule thành 1 chương trình
  - Item có field `is_sales_item`, `is_stock_item`
  - Không có concept "thanh lý" (liquidation)
- **Gap:**
  - ERPNext không track "hàng sale" vs "hàng thanh lý" một cách riêng biệt
  - Pricing Rule chỉ quản lý giá, không track lý do (sale campaign vs thanh lý)
  - Thiếu report: tổng hàng đang sale, tổng hàng thanh lý, hiệu quả campaign
  - Cần custom field/tag để phân loại lý do giảm giá
- **Action:**
  1. Custom field trên Pricing Rule hoặc Item: `custom_discount_reason` (Select: Sale Campaign / Thanh lý / Khác)
  2. Tạo Script Report "Báo cáo Hàng thanh lý / Sale"
  3. Data source: Items có Pricing Rule active + Stock Balance
  4. Cột: Item, Giá gốc, Giá sale, % giảm, Lý do (Sale/Thanh lý), Qty tồn, Campaign name
  5. Summary: tổng hàng sale (qty + value), tổng hàng thanh lý (qty + value)
  6. Nếu có Sales Invoice data (T4): thêm cột "Đã bán trong campaign"
- **Effort:** 3 ngày (1 ngày custom field + 1.5 ngày report + 0.5 ngày test)
- **Dependency:** Module 12 (Pricing Rule setup — T4), Module 03 (Item)
- **⚠️ Clarify:** Phân biệt "sale" vs "thanh lý" cụ thể? — xem CLARIFY.md #2.4

---

## Tổng hợp

| Tag | Số feature | Effort |
|-----|-----------|--------|
| `USE` | 2 | 1 ngày |
| `CFG` | 1 | 1 ngày |
| `EXT` | 2 | 5 ngày |
| `NEW` | 2 | 6 ngày |
| **Tổng** | **7** | **~13 ngày** |

## Dependencies tổng hợp

| Module | Features ảnh hưởng | Ghi chú |
|--------|-------------------|---------|
| 03 - Sản phẩm (T3) | Tất cả | Item master, Item Group, custom fields |
| 07 - Kho hàng (T4) | 14.5.1, 14.5.2, 14.5.3, 6.3.1, 6.3.3 | Warehouse, Stock Entry, Stock Ledger |
| 12 - Bán hàng (T4) | 6.3.1 | Sales data cho avg daily sales |
| 15 - Chi nhánh (T4) | 6.3.3 | Đại lý/Chi nhánh hierarchy |

> **Lưu ý:** Module 06 thuộc T3 nhưng nhiều reports cần data từ T4 modules. Trong T3 có thể build report framework + test với sample data. Reports hoạt động đầy đủ khi T4 modules done.
