# 06 - Báo cáo Phân tích

| Item | Value |
|------|-------|
| **STT** | 06 |
| **Milestone** | T3 (31/03/2026) |
| **Công ty** | TM + NM |
| **Nguồn spec** | FEATURE_SPECIFICATION.md Section 14.5 + ERP_SPECIFICATION.md Section 6.3 |
| **ERPNext base** | Stock module (Stock Balance, Stock Ageing, Item Shortage Report) |
| **Độ phức tạp** | Trung bình — ERPNext có ~40% reports sẵn, cần custom 60% |
| **Status** | Đang làm |

## Tổng quan

Module "Báo cáo Phân tích" tập trung vào các báo cáo **phân tích tồn kho và sản phẩm**. Scope gộp từ 2 nguồn spec:

- **FEAT 14.5** (3 features): BC tồn kho theo kho, giá trị tồn kho, SP gần min
- **ERP 6.3** (4 features): Hàng chậm, vòng đời, điều chuyển, thanh lý/sale

> **Lưu ý scope:** FEAT 14.1-14.4 (Doanh số, Đơn hàng, KH, NV) đã tách sang T4 modules 18-22. ERP 6.1, 6.2, 6.4 thuộc module 31 (T5).

## Approach

| Tag | Số feature | Effort |
|-----|-----------|--------|
| USE | 2 | 1 ngày |
| CFG | 1 | 1 ngày |
| EXT | 2 | 5 ngày |
| NEW | 2 | 6 ngày |
| **Tổng** | **7** | **~13 ngày** |

## Tiến độ

- [x] README
- [x] SPEC_MAPPING.md
- [x] CLARIFY.md
- [x] CUSTOM_REQUIREMENTS.md
- [ ] Mockup (không cần — reports dùng ERPNext Report Builder UI)
- [ ] User Guide

## Tài liệu trong folder

| File | Mô tả |
|------|-------|
| `SPEC_MAPPING.md` | Mapping spec khách hàng → ERPNext |
| `CLARIFY.md` | Vấn đề cần clarify với khách |
| `CUSTOM_REQUIREMENTS.md` | Tổng hợp phần cần custom |

## Dependencies

| Module | Quan hệ | Ghi chú |
|--------|---------|---------|
| 03 - Sản phẩm | Input | Item master data, Item Group, attributes |
| 07 - Kho hàng (T4) | Input | Warehouse, Stock Entry, Stock Ledger |
| 05 - Mua hàng | Input | Purchase Receipt → Stock Ledger |
| 08 - BC Kho (T4) | Liên quan | Overlap một phần BC tồn kho |
| 31 - BC Tổng hợp (T5) | Liên quan | ERP 6.1, 6.2, 6.4 thuộc module 31 |

## Lưu ý quan trọng

- **T3 chưa có Stock module** (STT 07, T4) → reports trong T3 sẽ build framework/template, data thực tế có đầy đủ khi module 07 done
- Reports phân tích cần **Item master** (module 03) + **Reorder Level** config
- Hàng "vòng đời" cần custom field trên Item (launch date, lifecycle months)

## Code Reference

> Code thực tế: `dcnet_apps/dcnet_apps/dcnet_reports/` (hoặc tích hợp vào module stock reports)
