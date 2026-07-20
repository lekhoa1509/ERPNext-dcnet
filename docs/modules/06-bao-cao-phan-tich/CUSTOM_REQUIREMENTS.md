# 06 - Báo cáo Phân tích: Custom Requirements

> Extract từ SPEC_MAPPING.md — chỉ phần cần custom.
> Dùng để plan execution và track tiến độ.

## Custom Fields (thêm vào DocType có sẵn)

| DocType | Field | Type | Mục đích | Spec ref |
|---------|-------|------|----------|----------|
| Item | `custom_launch_date` | Date | Ngày ra mắt sản phẩm (model year) | 6.3.2 |
| Item | `custom_lifecycle_months` | Int | Vòng đời sản phẩm (tháng) | 6.3.2 |
| Item | `custom_is_liquidation` | Check | Đánh dấu hàng thanh lý | 6.3.4 |
| Pricing Rule | `custom_discount_reason` | Select | Lý do giảm giá: Sale Campaign / Thanh lý / Khác | 6.3.4 |

> **Lưu ý:** `custom_launch_date` và `custom_lifecycle_months` có thể đặt trong module 03 (Sản phẩm) nếu hợp lý hơn. Cần phối hợp với team module 03.

## Custom DocTypes (tạo mới)

Không cần tạo DocType mới. Tất cả reports dùng Script Report (không cần DocType riêng).

## Script Reports (Custom Reports)

| # | Report Name | Spec ref | Data Source | Effort |
|---|-------------|----------|-------------|--------|
| 1 | Sản phẩm gần định mức tồn kho | 14.5.3 | Stock Balance + Item.reorder_levels | 1 ngày |
| 2 | Báo cáo Hàng tồn chậm | 6.3.1 | Stock Ageing + Stock Ledger (sales velocity) | 3 ngày |
| 3 | Báo cáo Hàng sắp hết vòng đời | 6.3.2 | Item (custom fields) + Stock Balance | 3 ngày |
| 4 | Báo cáo Điều chuyển hàng | 6.3.3 | Stock Entry (Material Transfer) | 2 ngày |
| 5 | Báo cáo Hàng thanh lý / Sale | 6.3.4 | Pricing Rule + Item + Stock Balance | 3 ngày |

### Chi tiết Report #1: Sản phẩm gần định mức tồn kho

- **Type:** Script Report
- **Module:** Stock (hoặc DCNET Reports)
- **Columns:**
  - Item Code, Item Name, Item Group
  - Warehouse
  - Current Qty, Min Level (Reorder Level)
  - Khoảng cách (Current Qty - Min Level)
  - Status: "Dưới min" (< min) / "Gần min" (< min × 1.2) / "Đủ"
- **Sort:** Khoảng cách ascending (gần min nhất lên đầu)
- **Filters:** Warehouse, Item Group, Status
- **Extend:** Có thể extend Item Shortage Report thay vì tạo mới

### Chi tiết Report #2: Hàng tồn chậm

- **Type:** Script Report
- **Module:** DCNET Reports
- **Columns:**
  - Item Code, Item Name, Item Group, Brand
  - Warehouse, Qty tồn, Value tồn
  - Tuổi tồn (ngày) — từ Stock Ageing
  - Avg bán/tháng — từ Stock Ledger (outward qty / months)
  - Days of Stock = Qty tồn / Avg daily sales
  - Đề xuất: Sale / Điều chuyển / Giữ
- **Business Logic đề xuất:**
  - Tuổi tồn > threshold_days (default 90) AND avg bán < threshold_qty (default 3/tháng) → "Chậm bán"
  - Nếu kho khác có qty < min → "Đề xuất điều chuyển"
  - Nếu không → "Đề xuất sale"
- **Filters:** Warehouse, Item Group, Brand, Tuổi tồn tối thiểu
- **Config:** Threshold values config được (DCNET Settings hoặc report filter)

### Chi tiết Report #3: Hàng sắp hết vòng đời

- **Type:** Script Report
- **Module:** DCNET Reports
- **Columns:**
  - Item Code, Item Name, Item Group, Brand
  - Launch Date, Lifecycle (months), End of Lifecycle Date
  - Còn lại (ngày)
  - Qty tồn (tất cả kho), Value tồn
  - Status: "Khẩn cấp" (≤45 ngày) / "Cảnh báo" (≤60 ngày) / "OK"
- **Filters:** Status filter, Item Group, Brand
- **Dependency:** Custom fields `custom_launch_date` + `custom_lifecycle_months` trên Item
- **Note:** Items chưa có lifecycle data → ẩn khỏi report (chỉ hiện items có data)

### Chi tiết Report #4: Điều chuyển hàng

- **Type:** Script Report
- **Module:** Stock (hoặc DCNET Reports)
- **Columns:**
  - Ngày, Stock Entry ID
  - Từ kho (Source Warehouse), Đến kho (Target Warehouse)
  - Item Code, Item Name, Qty, Value
  - Loại: "Nội bộ" / "Đại lý" (based on target warehouse group)
- **Filters:** Từ ngày - Đến ngày, Source Warehouse, Target Warehouse, Loại
- **Group by:** Period (tuần/tháng), Warehouse pair
- **Chart:** Bar chart — qty điều chuyển theo tháng, stack by loại

### Chi tiết Report #5: Hàng thanh lý / Sale

- **Type:** Script Report
- **Module:** DCNET Reports
- **Columns:**
  - Item Code, Item Name, Item Group, Brand
  - Giá gốc (Standard Selling Price), Giá sale (Pricing Rule price)
  - % giảm, Lý do (Sale Campaign / Thanh lý)
  - Campaign name (từ Promotional Scheme)
  - Qty tồn, Value tồn (at sale price)
  - Qty đã bán trong campaign (nếu có Sales Invoice data)
- **Filters:** Lý do, Item Group, Brand, Campaign
- **Dependency:** Module 12 (Pricing Rule), Sales Invoice data (T4)

## Server Scripts / Hooks

Không cần server script cho module này. Tất cả logic nằm trong Script Reports.

## Client Scripts

Không cần client script cho module này.

## Workflows

Không cần workflow cho module này.

## Tổng effort

| Hạng mục | Số lượng | Effort |
|----------|---------|--------|
| Custom Fields | 4 | 0.5 ngày |
| Script Reports | 5 | 12 ngày |
| Testing | — | 1 ngày |
| **Tổng** | | **~13.5 ngày** |

## Implementation Priority

| # | Report | Priority | Lý do |
|---|--------|----------|-------|
| 1 | 14.5.1 Tồn kho theo kho | P0 | USE — config only |
| 2 | 14.5.2 Giá trị tồn kho | P0 | USE — config only |
| 3 | 14.5.3 Gần định mức | P1 | CFG — extend existing report |
| 4 | 6.3.2 Hết vòng đời | P1 | NEW — ít dependency, custom fields trên Item |
| 5 | 6.3.3 Điều chuyển | P2 | EXT — cần Warehouse data (T4) |
| 6 | 6.3.1 Tồn chậm | P2 | EXT — cần Sales data (T4) |
| 7 | 6.3.4 Thanh lý/Sale | P3 | NEW — cần Pricing Rule + Sales data (T4) |
