# 05 - Mua hàng: Custom Requirements

> Extract từ SPEC_MAPPING.md — chỉ phần cần custom (EXT/NEW).
> Dùng để plan execution và track tiến độ.

---

## Custom Fields (thêm vào DocType có sẵn)

| DocType | Field | Type | Mục đích | Spec ref |
|---------|-------|------|----------|----------|
| Purchase Order | `custom_ship_mode` | Select (Sea/Air/Express) | Phương thức vận chuyển | 3.1.3 |
| Purchase Order | `custom_confirm_ship_date` | Date | Ngày NCC xác nhận giao | 3.1.3 |
| Purchase Order | `custom_vendor_po_number` | Data | Số PO của hãng (Titleist, FJ) | 3.1.3 |
| Purchase Order | `custom_supplier_status` | Select (Draft/Sent to Supplier/In Transit/Received) | Trạng thái phía NCC | 3.1.5 |
| Purchase Order | `custom_purchase_plan` | Link (Purchase Plan) | Liên kết tới Kế hoạch mua hàng | 3.2.2 |
| Purchase Receipt | `custom_declaration_no` | Data | Số tờ khai hải quan | 3.2.5 |
| Purchase Receipt | `custom_customs_status` | Select | Tình trạng thông quan | 3.2.4 |
| Purchase Receipt | `custom_clearance_date_expected` | Date | Ngày dự kiến thông quan | 3.2.4 |
| Purchase Receipt | `custom_clearance_date_actual` | Date | Ngày thực tế thông quan | 3.2.4 |
| Purchase Receipt | `custom_po_rate` | Currency | Đơn giá PO (để so sánh) | 3.2.5 |

---

## Custom DocTypes (tạo mới)

| DocType | Module | Parent | Spec ref | Effort |
|---------|--------|--------|----------|--------|
| Purchase Plan | DCNET Buying | - | 3.2.1 | 5 ngày |
| Purchase Plan Item | DCNET Buying | Purchase Plan (child) | 3.2.1 | (tính trong Purchase Plan) |
| Delivery Schedule | DCNET Buying | - | 3.2.3 | 5 ngày |
| Delivery Schedule Item | DCNET Buying | Delivery Schedule (child) | 3.2.3 | (tính trong Delivery Schedule) |

### Purchase Plan (Kế hoạch mua hàng)

**Fields chính (parent):**
- `supplier` (Link: Supplier)
- `plan_date` (Date)
- `plan_number` (Data, auto naming)
- `content` (Text)
- `items` (Table: Purchase Plan Item)

**Fields child (Purchase Plan Item):**
- `item_code` (Link: Item)
- `item_name` (Data, fetch)
- `uom` (Link: UOM)
- `purchase_type` (Select: Demo/Purchase)
- `rate` (Currency)
- `family` (Data)
- `year` (Int)
- `category` (Data)
- `sub_category` (Data)
- `shaft` (Data)
- `price` (Currency)
- `qty_month_1` through `qty_month_12` (Int x12)
- `total_qty` (Int, computed)

### Delivery Schedule (Kế hoạch giao hàng)

**Fields chính (parent):**
- `supplier` (Link: Supplier)
- `purchase_order` (Link: Purchase Order)
- `purchase_plan` (Link: Purchase Plan)
- `schedule_date` (Date)
- `created_by` (Link: User)

**Fields child (Delivery Schedule Item):**
- `item_code` (Link: Item)
- `item_name` (Data)
- `vendor_item_name` (Data) — tên hãng gửi, để so sánh
- `po_number` (Data) — PO Number của hãng
- `po_create_date` (Date)
- `buyer_name` (Data)
- `product_type` (Data)
- `product_group` (Data)
- `category` (Data)
- `location` (Data)
- `model` (Data)
- `stastic_factor` (Data)
- `total_unit` (Int)
- `ship_to` (Data)
- `month` (Data)
- `confirm_ship_date` (Date)
- `ship_mode` (Select: Sea/Air/Express)
- `ean` (Data) — barcode
- `upc` (Data) — barcode
- `po_comment` (Text)
- `remark` (Text)

---

## Server Scripts / Hooks

| Hook | Trigger | Mục đích | Spec ref |
|------|---------|----------|----------|
| validate | Purchase Receipt before_submit | Cảnh báo giá nhập khác giá PO | 3.2.5 |
| validate | Delivery Schedule validate | Cảnh báo tên VT chính thức khác vendor_item_name | 3.2.3 |

---

## Client Scripts

| DocType | Event | Mục đích | Spec ref |
|---------|-------|----------|----------|
| Purchase Receipt | form.rate change | So sánh Rate vs custom_po_rate, hiện warning | 3.2.5 |
| Purchase Order | refresh | Hiển thị custom_supplier_status badge | 3.1.5 |
| Item | form load | Bulk image import tool (custom page hoặc dialog) | 3.1.2 |

---

## Workflows

| DocType | States | Mục đích | Spec ref |
|---------|--------|----------|----------|
| Purchase Receipt | Draft → Chờ duyệt → Đã nhập kho | Phê duyệt phiếu nhập | 3.1.16 |
| Purchase Receipt (Return) | Draft (Lệnh) → Approved → Submitted (Phiếu) | 2-step trả hàng NCC | 3.2.7 |
| Payment Entry | Draft → Đề nghị TT → Approved → Submitted | Phê duyệt thanh toán | 3.2.10 |

---

## Custom Reports (Script Report)

| Report | Spec ref | Format | Effort |
|--------|----------|--------|--------|
| BC Giá mua bình quân | 3.1.18 | Item × Supplier × Avg Rate × Period | 2 ngày |
| BC NCC tốt nhất | 3.1.18 | Supplier ranking (giá, giao hàng, chất lượng) | 1 ngày |
| BC So sánh KHMH vs ĐH | 3.2 end | Plan vs PO variance | 1 ngày |

> Lưu ý: Các report này có thể thuộc module 06 (BC Phân tích).

---

## Custom Tools

| Tool | Mục đích | Spec ref | Effort |
|------|----------|----------|--------|
| Bulk Image Import | Chọn folder → match filename vs Item code → attach | 3.1.2 | 3 ngày |

---

## Tổng effort

| Hạng mục | Số lượng | Effort |
|----------|---------|--------|
| Custom Fields | 10 | 2 ngày |
| Custom DocTypes | 2 (+2 child) | 10 ngày |
| Server Scripts | 2 | 1 ngày |
| Client Scripts | 3 | 2 ngày |
| Workflows | 3 | 3 ngày |
| Custom Reports | 3 | 4 ngày |
| Custom Tools | 1 | 3 ngày |
| Testing & QA | - | 3 ngày |
| **Tổng** | | **~28 ngày** |

> **Lưu ý:** 28 ngày là effort 1 người. Với team 2-3 người làm song song, ~12-15 ngày thực tế.
> Giai đoạn T3 chỉ cần core (PO + Purchase Receipt + custom fields). Custom DocTypes (Purchase Plan, Delivery Schedule) có thể để T4.
