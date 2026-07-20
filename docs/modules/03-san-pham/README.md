# 03 - Quản lý Sản phẩm

| Item | Value |
|------|-------|
| **STT** | 03 |
| **Milestone** | T3 (31/03/2026) |
| **Công ty** | TM + NM |
| **Nguồn spec** | FEATURE_SPECIFICATION.md Section 6 |
| **ERPNext base** | Item, Item Group, Brand, Item Price, Data Import/Export |
| **Status** | Đang làm docs |

## 6 Features (từ spec)

| # | Feature | Tag | Approach |
|---|---------|-----|----------|
| 6.1 | Danh sách Sản phẩm | `CFG` | Item List View + config columns + custom filter tồn kho |
| 6.2 | Quản lý Danh mục SP | `USE` | Item Group (tree hierarchy) |
| 6.3 | Tạo Sản phẩm | `CFG` | Item form + config required fields |
| 6.4 | Import Sản phẩm | `EXT` | Data Import + custom fields (tích điểm, kích thước) |
| 6.5 | Export Sản phẩm | `USE` | Data Export (built-in) |
| 6.6 | Chi tiết SP + Bảo hành | `EXT` | Item detail + custom warranty field |

**Tổng:** USE: 2 | CFG: 2 | EXT: 2

## Approach

Sử dụng ERPNext Item module (~90% có sẵn). Custom thêm:
- Custom fields cho thuộc tính vật lý, tích điểm, bảo hành
- Config list view columns + filters
- Data Import template có hỗ trợ custom fields

## Tiến độ

- [x] README
- [x] SPEC_MAPPING.md
- [x] CLARIFY.md
- [x] CUSTOM_REQUIREMENTS.md
- [ ] Mockup (nếu cần)
- [ ] User Guide

## Tài liệu trong folder

| File | Mô tả |
|------|-------|
| `SPEC_MAPPING.md` | ⭐ Mapping spec khách hàng → ERPNext (6 features) |
| `CLARIFY.md` | Vấn đề cần clarify với khách (4 items) |
| `CUSTOM_REQUIREMENTS.md` | Custom fields + scripts cần làm |

## Dependencies

| Module | Quan hệ | Ảnh hưởng |
|--------|---------|-----------|
| 02-dashboard (T3) | Top 20 SP chart | Dashboard dùng Item data |
| 04-nha-cung-cap (T3) | Supplier → Item | NCC cung cấp SP |
| 05-mua-hang (T3) | Purchase Order → Item | Mua hàng tạo tồn kho |
| 07-kho-hang (T4) | Stock Entry → Item | Quản lý tồn kho |
| 12-ban-hang (T4) | Sales Invoice → Item | Bán hàng |

## Code Reference

> Code thực tế: `dcnet_apps/dcnet_apps/`

| Component | Location |
|-----------|----------|
| Item barcode JS | `dcnet_apps/public/js/item_barcode.js` |
| Barcode management | `dcnet_apps/barcode_management/` |
| Custom fields | `dcnet_apps/fixtures/custom_field.json` |
