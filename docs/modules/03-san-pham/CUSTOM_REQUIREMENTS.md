# 03 - Quản lý Sản phẩm: Custom Requirements

> Extract từ SPEC_MAPPING.md — chỉ phần cần custom.
> Dùng để plan execution và track tiến độ.

---

## Custom Fields (thêm vào Item DocType)

| # | Field | Fieldtype | Options | Mục đích | Spec ref | Ghi chú |
|---|-------|-----------|---------|----------|----------|---------|
| 1 | `custom_warranty_months` | Int | — | Thời gian bảo hành (tháng) | 6.6 | Default: 12. Dùng để auto-set warranty_expiry_date trên Serial No |
| 2 | `custom_loyalty_points` | Int | — | Điểm tích cho mỗi SP | 6.4 | ⚠️ Chờ clarify #2.1 — có thể không cần nếu dùng Loyalty Program |
| 3 | `custom_height` | Float | — | Chiều cao (cm) | 6.4 | Không bắt buộc |
| 4 | `custom_length` | Float | — | Chiều dài (cm) | 6.4 | Không bắt buộc |
| 5 | `custom_width` | Float | — | Chiều rộng (cm) | 6.4 | Không bắt buộc |
| 6 | `custom_material` | Data | — | Chất liệu | 6.4 | Không bắt buộc |

> **Lưu ý:** ERPNext đã có sẵn `weight_per_unit` (trọng lượng), `brand` (thương hiệu), `manufacturer_part_no` (SKU nhà SX), `item_barcode` child table (mã vạch). Không cần thêm custom field cho những trường này.

---

## Property Setters (config field hiện có)

| DocType | Field | Property | Value | Mục đích | Spec ref |
|---------|-------|----------|-------|----------|----------|
| Item | brand | reqd | 1 | Bắt buộc chọn thương hiệu | 6.3 |
| Item | item_group | reqd | 1 | Bắt buộc chọn nhóm SP (đã mặc định) | 6.3 |

---

## Client Scripts

| # | DocType | Event | Mục đích | Spec ref |
|---|---------|-------|----------|----------|
| 1 | Item | refresh | Ẩn/hiện custom fields theo Item Group (VD: chiều dài chỉ cho gậy golf) | 6.4 |

---

## Custom Reports (Script Report)

| # | Report | Spec ref | Mô tả | Effort |
|---|--------|----------|--------|--------|
| 1 | Danh sách Sản phẩm (mở rộng) | 6.1 | List SP với filter tồn kho: dưới/vượt định mức, còn/hết hàng. Join Item + Bin (stock) + Reorder Level | 2 ngày |

---

## Data Import Template

| # | Mục đích | Spec ref | Mô tả | Effort |
|---|----------|----------|--------|--------|
| 1 | Template Import SP | 6.4 | File Excel mẫu với columns mapping sang Item fields (bao gồm custom fields). Kèm hướng dẫn | 0.5 ngày |

---

## Hooks / Install Setup

| # | Hook | Trigger | Mục đích | Spec ref |
|---|------|---------|----------|----------|
| 1 | `setup_item_groups()` | after_migrate | Tạo Item Group mặc định cho golf: Gậy golf, Bóng golf, Phụ kiện, Quần áo, Giày, Túi, Khác | 6.2 |
| 2 | `setup_price_list()` | after_migrate | Tạo Price List "Giá bán lẻ" nếu chưa có | 6.1 |

---

## Fixtures cần tạo/cập nhật

| Fixture | File | Ghi chú |
|---------|------|---------|
| Custom Field (Item) | `dcnet_apps/fixtures/custom_field.json` | Thêm 6 fields ở trên |
| Property Setter (Item) | `dcnet_apps/fixtures/property_setter.json` | Config mandatory fields |

---

## Tổng effort

| Hạng mục | Số lượng | Effort |
|----------|---------|--------|
| Custom Fields | 6 | 0.5 ngày |
| Property Setters | 2 | 0.5 ngày |
| Client Script | 1 | 0.5 ngày |
| Custom Report | 1 | 2 ngày |
| Data Import Template | 1 | 0.5 ngày |
| Install hooks | 2 | 0.5 ngày |
| Config & Test | — | 2 ngày |
| **Tổng** | | **6.5 ngày** |
