# DCNET Dashboard - Tracking

> Cập nhật: 2026-02-13

## Cấu trúc file

```
dcnet_dashboard/
├── __init__.py
├── api.py                                          # 3 whitelist methods (dummy data)
├── number_card/
│   ├── total_revenue/total_revenue.json            # Custom → api.get_total_revenue
│   ├── wholesale_revenue/wholesale_revenue.json    # Custom → api.get_wholesale_revenue
│   └── retail_revenue/retail_revenue.json          # Custom → api.get_retail_revenue
├── dashboard_chart/
│   ├── revenue_by_customer_source/...json           # Report chart, Bar
│   ├── revenue_by_order_source/...json              # Report chart, Bar
│   └── top_products_by_revenue/...json              # Report chart, Bar
├── report/
│   ├── revenue_by_customer_source/ (.py .js .json)  # Script Report
│   ├── revenue_by_order_source/    (.py .js .json)  # Script Report
│   └── top_products_by_revenue/    (.py .js .json)  # Script Report
└── workspace/
    └── dashboard/dashboard.json                     # Workspace layout
```

## Workspace Layout

| ID | Type | Nội dung | Col |
|----|------|----------|-----|
| hd01 | header | **Tổng quan doanh số** | 12 |
| nc01 | number_card | Total Revenue | 4 |
| nc02 | number_card | Wholesale Revenue | 4 |
| nc03 | number_card | Retail Revenue | 4 |
| sp01 | spacer | | 12 |
| hd02 | header | **Phân tích doanh số** | 12 |
| ch01 | chart | Revenue by Customer Source | 6 |
| ch02 | chart | Revenue by Order Source | 6 |
| sp02 | spacer | | 12 |
| ch03 | chart | Top Products by Revenue | 12 |
| sp03 | spacer | | 12 |
| hd04 | header | **Module sắp ra mắt** | 12 |
| pa01 | paragraph | Trade-in (T4 - 30/04/2026) | 12 |
| pa02 | paragraph | Fitting (T6 - 30/06/2026) | 12 |
| pa03 | paragraph | Coaching (T6 - 30/06/2026, Thăng Long TM) | 12 |

### Sidebar links

3 report links (không có Card Break):

- Doanh so theo nguon KH → Revenue by Customer Source
- Doanh so theo nguon don → Revenue by Order Source
- Top 20 SP ban chay → Top Products by Revenue

## Number Cards

Type `Custom`, gọi API trả dummy data. `show_full_number=1` để hiện đủ số.

| Card | API method | Giá trị giả |
|------|-----------|-------------|
| Total Revenue | `dcnet_apps.dcnet_dashboard.api.get_total_revenue` | 2,847,500,000 |
| Wholesale Revenue | `dcnet_apps.dcnet_dashboard.api.get_wholesale_revenue` | 1,923,000,000 |
| Retail Revenue | `dcnet_apps.dcnet_dashboard.api.get_retail_revenue` | 924,500,000 |

### Lưu ý khi tạo Number Card JSON mới

- **Bắt buộc:** `"filters_json": "[]"` — dù là Custom type (tránh null.length TypeError)
- **Bắt buộc:** `"show_full_number": 1` — tránh abbreviation (2,85 B)
- API trả `{"value": number, "fieldtype": "Currency"}` — system tự format VND

## Dashboard Charts

Type `Report`, `use_report_chart=1`, chart type `Bar`.

| Chart | Report | Filters cố định |
|-------|--------|-----------------|
| Revenue by Customer Source | Revenue by Customer Source | from_date: 2026-01-01, to_date: 2026-12-31 |
| Revenue by Order Source | Revenue by Order Source | from_date: 2026-01-01, to_date: 2026-12-31 |
| Top Products by Revenue | Top Products by Revenue | from_date: 2026-01-01, to_date: 2026-12-31, limit: 20 |

Dynamic filter chung: `company = frappe.defaults.get_user_default("Company")`

### Lưu ý khi tạo Dashboard Chart JSON mới

- **Bắt buộc:** `"color": "#4472C4"` — dù dùng `use_report_chart` (tránh invalid color error)

## Reports

3 Script Reports, `ref_doctype: Sales Invoice`. Roles: Sales Manager, Sales User, Accounts User.

| Report | Columns | Filters | Dummy data fallback |
|--------|---------|---------|---------------------|
| Revenue by Customer Source | source, revenue | company, from_date, to_date | 6 nguồn KH (Website, Facebook, Giới thiệu, Walk-in, Zalo, Không rõ) |
| Revenue by Order Source | order_source, revenue | company, from_date, to_date | 5 nguồn đơn (Online, Tại cửa hàng, Điện thoại, Email, Không rõ) |
| Top Products by Revenue | item_code, item_name, qty, revenue | company, from_date, to_date, limit | 10 sản phẩm golf |

Dummy data chỉ trả về khi query thật trả rỗng (không có Sales Invoice submitted).

## VND Currency Format (Global)

Cấu hình tại `install.py` → `setup_currency_format()`, chạy tự động mỗi `bench migrate`.

### Mong muốn: `2.847.500.000đ`

| Setting | Giá trị | Ở đâu |
|---------|---------|-------|
| VND `symbol` | `đ` | Currency DocType |
| VND `symbol_on_right` | `1` | Currency DocType |
| VND `number_format` | `#.###` (no decimal) | Currency DocType |
| System `use_number_format_from_currency` | `1` | System Settings |
| System `currency_precision` | `0` | System Settings |

### Cách hoạt động

```
bench migrate → after_migrate() → setup_currency_format()
  ├── UPDATE Currency SET symbol="đ", symbol_on_right=1, number_format="#.###"
  └── UPDATE System Settings SET use_number_format_from_currency=1, currency_precision="0"
```

### Cho team / module mới

Chỉ cần `git pull` + `bench migrate` → VND format tự đúng.
Code mới dùng `fieldtype: "Currency"` — KHÔNG format thủ công.

### Trạng thái hiện tại

- [x] VND symbol "đ" suffix — OK
- [x] Dấu `.` ngăn hàng nghìn — OK
- [ ] Bỏ `,00` decimal — **ĐANG FIX** (đã set `currency_precision=0` nhưng cần verify)

**Root cause `,00`:** Frappe `formatters.js:135` defaults precision=2 khi `currency_precision` empty:
```js
precision = cint(docfield.precision || frappe.boot.sysdefaults.currency_precision || 2);
```
Fix: set `currency_precision="0"` trong System Settings. Nếu vẫn còn `,00` sau migrate + hard refresh, cần kiểm tra bootinfo cache hoặc override precision ở level khác.

## Bugs đã fix

### 1. Label mismatch — number cards & charts không render

**Triệu chứng:** Workspace hiện headers nhưng number cards và charts trống.

**Nguyên nhân:** `block.js:9-13` lookup widget bằng `obj.label == __(block_name)`. Workspace JSON có Vietnamese labels trong `number_cards`/`charts` tables (VD: `"Doanh so"`) nhưng content JSON dùng English names (VD: `"Total Revenue"`). Lookup fail im lặng → render div rỗng.

**Fix:** Đổi labels trong `number_cards`/`charts` tables cho khớp với `number_card_name`/`chart_name`.

**Bài học:** Trong Frappe Workspace, labels của child tables (`Workspace Number Card`, `Workspace Chart`) **PHẢI match** với name dùng trong content JSON blocks.

### 2. Number Card không sync sau migrate

**Triệu chứng:** Đổi `type` từ `Document Type` sang `Custom` trong JSON nhưng DB vẫn giữ giá trị cũ.

**Nguyên nhân:** Frappe sync fixtures dựa trên `modified` timestamp. Nếu timestamp không thay đổi → skip sync.

**Fix:** Bump `modified` timestamp (VD: `2026-03-01` → `2026-03-02`).

**Bài học:** Khi thay đổi nội dung fixtures JSON, luôn bump `modified` để Frappe nhận biết cần sync lại.

### 3. Number Card TypeError + Chart invalid color

**Triệu chứng:** Console errors: `Cannot read properties of null (reading 'length')` tại `dashboard_utils.js:238` và `"" is not a valid color` tại `BaseChart.js:78`.

**Nguyên nhân:** Number Card JSON thiếu `filters_json` → `cleanup_filters()` nhận `null` → `.length` crash. Dashboard Chart JSON thiếu `color` → `BaseChart` nhận empty string.

**Fix:** Thêm `"filters_json": "[]"` vào 3 number cards, `"color": "#4472C4"` vào 3 dashboard charts.

**Bài học:** Custom type Number Cards vẫn cần `filters_json` (empty array string `"[]"`). Dashboard Charts cần `color` field dù dùng `use_report_chart`.

### 4. VND format — abbreviated + sai symbol + decimal

**Triệu chứng:** Number Cards hiện `VND 2,85 B` (abbreviated) hoặc `VND 2.847.500.000,00` (sai format).

**Nguyên nhân (3 lớp):**
1. VND Currency thiếu `symbol` → fallback "VND", `symbol_on_right=0` → prefix
2. Number Card widget dùng `shorten_number()` → abbreviation "2,85 B"
3. `formatters.js:135` defaults `precision=2` khi `currency_precision` empty → `,00`

**Fix (global — install.py):**
1. VND Currency: `symbol="đ"`, `symbol_on_right=1`, `number_format="#.###"`
2. System Settings: `use_number_format_from_currency=1`, `currency_precision="0"`
3. Number Card JSONs: `show_full_number=1` (skip abbreviation)
4. API trả numeric `{value: number, fieldtype: "Currency"}` (system tự format)

**Frappe source references:**
- `number_card_widget.js` → `set_formatted_number()` → `show_full_number` skips `shorten_number()`
- `number_format.js:179` → `get_number_format(currency)` checks `use_number_format_from_currency`
- `number_format.js:148` → `symbol_on_right` support in `format_currency()`
- `formatters.js:135` → `currency_precision || 2` default precision

**Bài học:**
- Frappe Currency DocType có `symbol_on_right` field → dùng cho đ suffix
- `use_number_format_from_currency` → Currency fields dùng format riêng từ Currency doc
- `currency_precision` trong System Settings PHẢI set explicit (empty → default 2)
- Number Card `show_full_number` → skip `shorten_number()`, hiện đủ số
- KHÔNG format thủ công trong API — để system xử lý
