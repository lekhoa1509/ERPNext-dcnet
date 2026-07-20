# 04 - Danh mục Nhà cung cấp

| Item | Value |
|------|-------|
| **STT** | 04 |
| **Milestone** | T3 (31/03/2026) |
| **Công ty** | TM + NM |
| **Nguồn spec** | ERP_SPECIFICATION.md Section 3.0 + SRS Section 3.4 |
| **ERPNext base** | Buying module (Supplier, Supplier Group, Price List, Item Price, Payment Terms) |
| **Độ phức tạp** | Đơn giản — ERPNext có sẵn ~95% |
| **Status** | Đang làm |

## Tiến độ

- [x] README
- [x] SPEC_MAPPING.md
- [x] CLARIFY.md
- [ ] CUSTOM_REQUIREMENTS.md — Không cần (100% USE/CFG)
- [ ] Mockup — Không cần (dùng UI ERPNext)
- [ ] User Guide

## Tài liệu trong folder

| File | Mô tả |
|------|-------|
| `SPEC_MAPPING.md` | Mapping spec khách hàng -> ERPNext |
| `CLARIFY.md` | Vấn đề cần clarify với khách |

## Tổng hợp nhanh

- **2 features** từ ERP spec (3.0.1 + 3.0.2)
- **Tag**: CFG x2 (chỉ cần config ERPNext, không cần custom code)
- **Effort**: ~2-3 ngày (setup + test)
- **ERPNext DocTypes**: Supplier, Supplier Group, Price List, Item Price, Payment Terms Template

## Liên kết module

| Module | Quan hệ |
|--------|---------|
| 05 - Mua hàng | NCC là master data cho Purchase Order |
| 07 - Kho hàng | NCC liên quan Purchase Receipt |
| 24 - KT Mua hàng | NCC liên quan Accounts Payable |
| 26 - KT Công nợ | Công nợ phải trả NCC |

## Code Reference

> Code thực tế: Không cần custom app — chỉ config ERPNext built-in
> Fixtures (nếu có): `dcnet_apps/dcnet_apps/fixtures/` (Supplier Group, Payment Terms)
