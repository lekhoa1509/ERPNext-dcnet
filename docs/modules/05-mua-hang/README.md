# 05 - Quản lý Mua hàng

| Item | Value |
|------|-------|
| **STT** | 05 |
| **Milestone** | T3 (31/03/2026) |
| **Công ty** | TM + NM |
| **Nguồn spec** | ERP_SPECIFICATION.md Section 3.1 + 3.2, IMPORT_PROCESS_SPECIFICATION.md, SRS Section 3.5 |
| **ERPNext base** | Buying module (Purchase Order, Purchase Receipt, Purchase Invoice, Landed Cost Voucher, Payment Entry, Pricing Rule) |
| **Độ phức tạp** | Trung bình-khó — có EXT/NEW items |
| **Status** | Đang làm |

## Tiến độ

- [x] README
- [x] SPEC_MAPPING.md
- [x] CLARIFY.md
- [x] CUSTOM_REQUIREMENTS.md
- [x] Mockup (3 screens: Purchase Plan, Delivery Schedule, Bulk Image Import)
- [ ] User Guide

## Tài liệu trong folder

| File | Mô tả |
|------|-------|
| `SPEC_MAPPING.md` | Mapping spec khách hàng -> ERPNext |
| `CLARIFY.md` | Vấn đề cần clarify với khách |
| `CUSTOM_REQUIREMENTS.md` | Tổng hợp phần cần custom (EXT/NEW) |
| `mockup/` | UI mockups: Purchase Plan, Delivery Schedule, Bulk Image Import |

## Tổng hợp nhanh

- **28 entries** từ ERP spec (18 features 3.1 + 10 workflow steps 3.2, có overlap)
- **Tag**: USE 7 | CFG 7 | EXT 9 | NEW 2 | REF 3
- **Effort**: ~20-25 ngày
- **Legacy**: `docs/modules/import-management/` (5 files phân tích cũ, đã thiết kế 5 custom DocTypes)

## Liên kết module

| Module | Quan hệ |
|--------|---------|
| 03 - Sản phẩm | Item master data |
| 04 - NCC | Supplier master data |
| 07 - Kho hàng | Purchase Receipt -> Stock |
| 24 - KT Mua hàng | Purchase Invoice -> GL Entry |
| 26 - KT Công nợ | Accounts Payable |

## Legacy docs (tham khảo)

> Folder `docs/modules/import-management/` chứa 5 files phân tích format cũ:
> - `IMPORT_MANAGEMENT_SPEC.md` — Extract quy trình từ spec gốc
> - `IMPORT_MANAGEMENT_STATUS.md` — Status workflow & state machines (5 custom DocTypes)
> - `IMPORT_MANAGEMENT_WORKFLOW.md` — Workflow diagrams & ERD
> - `IMPORT_MANAGEMENT_USE_CASE_SPEC.md` — 13 use cases & actors
> - `IMPORT_MANAGEMENT_DIAGRAMS.md` — Mermaid diagrams
>
> **Lưu ý:** Legacy thiết kế rất chi tiết (5 DocTypes, state machines) nhưng chưa review với khách.
> SPEC_MAPPING.md là file chính — legacy chỉ để tham khảo.

## Code Reference

> Code thực tế: `dcnet_apps/dcnet_apps/buying/` (chưa tạo)
> ERPNext core: `dcnet_core/erpnext/buying/`
