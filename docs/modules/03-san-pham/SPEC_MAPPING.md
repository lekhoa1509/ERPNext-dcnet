# 03 - Quản lý Sản phẩm: Spec → ERPNext Mapping

> **Nguồn:** FEATURE_SPECIFICATION.md Section 6
> **ERPNext:** v16 — Stock Module (Item, Item Group, Brand, Item Price)
> **Cập nhật:** 16/02/2026

## Quy ước Tags

| Tag | Nghĩa | Action |
|-----|--------|--------|
| `USE` | ERPNext có sẵn, dùng ngay | Config + test |
| `CFG` | ERPNext có, cần config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext có, cần mở rộng | Custom field, client/server script |
| `NEW` | ERPNext không có, cần build | Custom DocType, module mới |
| `REF` | Thuộc module khác | Tham chiếu |

---

## 6. Quản lý Sản phẩm (6 features)

### 6.1. Danh sách Sản phẩm

- **Tag:** `CFG`
- **Spec yêu cầu:** Hiển thị: Mã SP, SKU, Tên SP, Trạng thái (đang/ngừng KD), ĐVT, Nhóm SP, Thương hiệu, Giá bán lẻ. Ẩn/hiện cột. Search theo mã, SKU, tên. Filter theo nhóm SP, tồn kho (dưới/vượt định mức, còn/hết hàng), thương hiệu, trạng thái.
- **ERPNext:** Item DocType → List View
- **ERPNext đã có:**
  - Item List View với columns: item_code, item_name, item_group, brand, stock_uom, disabled
  - Search: item_code, item_name (standard)
  - Filter: item_group, brand, disabled (standard)
  - Ẩn/hiện cột: List Settings (standard)
- **Gap:**
  - "SKU" — ERPNext dùng `item_code` hoặc `manufacturer_part_no`. Nếu cần field riêng → custom field
  - "Giá bán lẻ" — không hiển thị trực tiếp trên list, cần lấy từ Item Price (Price List)
  - "Filter tồn kho theo định mức" — ERPNext không có filter dưới/vượt định mức trên Item List. Cần custom report hoặc client script
- **Action:**
  - Config List View columns (thêm brand, stock_uom)
  - Thêm virtual column "Giá bán lẻ" hoặc custom field mirror
  - Custom report "Danh sách Sản phẩm" với filter tồn kho theo định mức
- **Effort:** 2 ngày
- **⚠️ Clarify:** CLARIFY.md #1.1 (SKU vs Mã SP)

### 6.2. Quản lý Danh mục Sản phẩm

- **Tag:** `USE`
- **Spec yêu cầu:** Danh sách danh mục SP, chi tiết danh mục, tạo/cập nhật/xóa danh mục.
- **ERPNext:** Item Group DocType
- **ERPNext đã có:**
  - Item Group: tree hierarchy (parent-child)
  - CRUD đầy đủ: tạo, sửa, xóa
  - Tree view + list view
  - Default item group tự tạo khi setup
- **Gap:** Không có gap
- **Action:** Tạo Item Group theo cấu trúc sản phẩm golf (Gậy, Bóng, Phụ kiện, Quần áo, Giày...)
- **Effort:** 0.5 ngày

### 6.3. Tạo Sản phẩm

- **Tag:** `CFG`
- **Spec yêu cầu:** Tạo một sản phẩm (single product creation).
- **ERPNext:** Item DocType form
- **ERPNext đã có:**
  - Item form với đầy đủ fields: item_code, item_name, item_group, brand, stock_uom, description, image, weight_per_unit, has_variants, is_stock_item, disabled...
  - Barcode child table (multiple barcodes per item)
  - Default warehouse, default supplier
  - Item template + variant system
- **Gap:**
  - Cần config required fields theo yêu cầu (item_code, item_name, item_group, brand bắt buộc)
  - Custom fields cần thêm: tích điểm, kích thước, bảo hành
- **Action:**
  - Config mandatory fields via Property Setter
  - Thêm custom fields (xem CUSTOM_REQUIREMENTS.md)
  - Setup Item Naming: by Item Code (manual) hoặc auto-naming
- **Effort:** 1 ngày
- **Dependency:** Custom fields từ 6.4 và 6.6

### 6.4. Import Sản phẩm

- **Tag:** `EXT`
- **Spec yêu cầu:** Import từ Excel: Mã hàng, Mã vạch, Tên SP, Nhóm SP (chọn/tạo mới), Thương hiệu (chọn/tạo mới), Giá bán, Trọng lượng, Tích điểm, Thêm thuộc tính, ĐVT, Thuộc tính thêm (chiều cao, dài, rộng, chất liệu), Mô tả.
- **ERPNext:** Data Import tool
- **ERPNext đã có:**
  - Data Import: CSV/Excel upload cho Item DocType
  - Auto-create linked records (Item Group, Brand) nếu chưa có
  - Mapping columns → fields
  - Bulk insert + bulk update modes
  - Progress tracking + error log
- **Gap:**
  - "Tích điểm" — ERPNext Loyalty Program tính điểm theo amount, không theo item. Nếu cần điểm per item → custom field `custom_loyalty_points` (Int)
  - "Thuộc tính thêm (chiều cao, dài, rộng, chất liệu)" — ERPNext chỉ có `weight_per_unit`. Dimensions không có sẵn → custom fields
  - "Giá bán" — cần import vào Item Price (Price List), không phải Item trực tiếp
- **Action:**
  - Thêm custom fields trên Item: `custom_loyalty_points`, `custom_height`, `custom_length`, `custom_width`, `custom_material`
  - Config Data Import template có custom fields
  - Tạo hướng dẫn import (template Excel mẫu)
  - Giá bán: import riêng vào Item Price hoặc dùng hook after_import
- **Effort:** 3 ngày
- **⚠️ Clarify:** CLARIFY.md #2.1 (Tích điểm per item hay per amount?)

### 6.5. Export Sản phẩm

- **Tag:** `USE`
- **Spec yêu cầu:** Export sản phẩm ra file Excel.
- **ERPNext:** Data Export
- **ERPNext đã có:**
  - Data Export: chọn DocType → chọn fields → download Excel/CSV
  - Filter trước khi export
  - Export bao gồm cả custom fields
  - Report Builder cũng hỗ trợ export
- **Gap:** Không có gap
- **Action:** Test Data Export với Item DocType, đảm bảo custom fields xuất được
- **Effort:** 0.5 ngày

### 6.6. Xem chi tiết Sản phẩm

- **Tag:** `EXT`
- **Spec yêu cầu:** Xem chi tiết SP. Thông tin bảo hành: thời gian bảo hành 1 năm với tất cả sản phẩm (gậy golf, shaft).
- **ERPNext:** Item form (detail view)
- **ERPNext đã có:**
  - Item form hiển thị tất cả thông tin chi tiết
  - Image, description, specifications
  - Stock levels per warehouse (Dashboard)
  - Price list, supplier info, accounting defaults
  - Warranty Claim DocType (xử lý yêu cầu bảo hành)
- **Gap:**
  - Item không có field `warranty_period` trực tiếp
  - ERPNext Warranty Claim cần biết thời gian bảo hành nhưng lấy từ Serial No (warranty_expiry_date), không từ Item
  - Cần custom field `custom_warranty_months` trên Item để set warranty mặc định
- **Action:**
  - Thêm custom field `custom_warranty_months` (Int, default 12) trên Item
  - Client Script: auto-set warranty_expiry_date khi tạo Serial No (= ngày bán + warranty_months)
- **Effort:** 1.5 ngày

---

## Tổng hợp

| Tag | Số feature | Effort |
|-----|-----------|--------|
| `USE` | 2 (6.2, 6.5) | 1 ngày |
| `CFG` | 2 (6.1, 6.3) | 3 ngày |
| `EXT` | 2 (6.4, 6.6) | 4.5 ngày |
| **Tổng** | **6** | **8.5 ngày** |

## ERPNext DocTypes liên quan

| DocType | Vai trò | Dùng cho feature |
|---------|---------|-----------------|
| Item | Master data sản phẩm | 6.1, 6.3, 6.4, 6.5, 6.6 |
| Item Group | Phân loại sản phẩm (tree) | 6.2 |
| Brand | Thương hiệu | 6.1, 6.3, 6.4 |
| Item Price | Giá bán theo Price List | 6.1, 6.4 |
| Item Barcode | Mã vạch (child table) | 6.4 |
| Item Attribute | Thuộc tính variant | 6.3, 6.4 |
| Data Import | Import Excel | 6.4 |
| Serial No | Serial tracking + bảo hành | 6.6 |
| Warranty Claim | Xử lý yêu cầu bảo hành | 6.6 |
