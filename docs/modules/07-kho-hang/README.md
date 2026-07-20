# Module 07 - Kho hàng (Warehouse / Stock Management)

> **STT:** 07
> **Milestone:** T4 (30/04/2026)
> **Công ty:** TM + NM (cả 2)
> **Độ phức tạp:** Cao - Module trung tâm kết nối mọi module khác
> **ERPNext coverage:** ~55-65% native, ~35-45% cần custom

---

## Tổng quan

Module Kho là **trung tâm kết nối** của toàn bộ hệ thống. Mọi giao dịch mua, bán, sản xuất đều đi qua kho và tự động tạo bút toán kế toán (GL Entry) thông qua cơ chế Perpetual Inventory.

### Phạm vi

- 30 features (3 CRM + 25 ERP + 2 Web Sync)
- 10 Critical + 16 High + 4 Medium priority
- Phụ thuộc: Buying, Selling, Accounting, Manufacturing
- Custom lớn nhất: Consignment (4-5 tuần), Barcode (2-3 tuần)

---

## Tài liệu trong folder

### analysis/

| File | Mô tả |
|------|-------|
| `WAREHOUSE_WORKFLOW.md` | Workflow & phân tích nghiệp vụ (có sẵn) |
| `WAREHOUSE_STATUS.md` | Status workflow & state machine (có sẵn) |
| `STOCK_ACCOUNTING_INTEGRATION.md` | ⭐ **Kho ↔ Kế toán** - Perpetual Inventory, GL Entry, COA mapping |
| `STOCK_MODULE_CONNECTIONS.md` | ⭐ **Kho ↔ Tất cả module** - Buying, Selling, Trade-in, Consignment, Import |
| `ERPNEXT_COVERAGE_GAP.md` | ⭐ **Gap Analysis** - ERPNext native vs Custom cần làm |

### technical-spec/

| File | Mô tả |
|------|-------|
| `WAREHOUSE_SPEC.md` | Spec Summary 12 bước (có sẵn) |
| `WAREHOUSE_DIAGRAMS.md` | Diagrams (có sẵn) |
| `WAREHOUSE_USE_CASE_SPEC.md` | Use Cases chi tiết (có sẵn) |

---

## Feature Matrix (30 features)

### Phase 1 CRM (3 features)

| # | Feature ID | Tên | Priority |
|---|-----------|------|:--------:|
| 1 | WH-001 | Danh sách kho | Critical |
| 2 | WH-002 | Tạo kho | High |
| 3 | WH-003 | Xem chi tiết kho (tồn kho) | Critical |

### Phase 2 ERP - Kho (20 features)

| # | Feature ID | Tên | Priority | ERPNext |
|---|-----------|------|:--------:|:-------:|
| 1 | ERP-WH-001 | Tồn kho đầu kỳ | Critical | ✅ Stock Reconciliation |
| 2 | ERP-WH-002 | Phiếu nhập mua | Critical | ✅ Purchase Receipt |
| 3 | ERP-WH-003 | Phiếu nhập khẩu | Critical | ✅ PR + Landed Cost |
| 4 | ERP-WH-004 | Phiếu nhập khác | High | ✅ Stock Entry (Receipt) |
| 5 | ERP-WH-005 | Phiếu xuất bán | Critical | ✅ Delivery Note |
| 6 | ERP-WH-006 | Phiếu xuất khác | High | ✅ Stock Entry (Issue) |
| 7 | ERP-WH-007 | Phiếu điều chuyển | High | ✅ Stock Entry (Transfer) |
| 8 | ERP-WH-008 | Phiếu xuất trả NCC | High | ✅ Purchase Return |
| 9 | ERP-WH-009 | Quản lý lô (Batch) | High | ⚠️ Cần thêm lifecycle alerts |
| 10 | ERP-WH-010 | Quản lý serial | High | ⚠️ Cần custom status |
| 11 | ERP-WH-011 | Quản lý vị trí | High | ❌ Custom |
| 12 | ERP-WH-012 | Reserve stock | Critical | ✅ Stock Reservation Entry |
| 13 | ERP-WH-013 | Gán barcode | High | ❌ Custom |
| 14 | ERP-WH-014 | Tạo tem nhãn | High | ❌ Custom |
| 15 | ERP-WH-015 | In tem hàng loạt | High | ❌ Custom |
| 16 | ERP-WH-016 | Kiểm kê | High | ⚠️ Cần custom freeze + approval |
| 17 | ERP-WH-017 | Xử lý chênh lệch | High | ⚠️ Cần custom approval |
| 18 | ERP-WH-018 | BC tồn kho | Critical | ✅ Stock Balance |
| 19 | ERP-WH-019 | BC giá trị tồn | High | ✅ Stock Ledger |
| 20 | ERP-WH-020 | Cảnh báo tồn | High | ⚠️ Reorder Level + custom |

### Phase 2 ERP - Báo cáo kho (5 features)

| # | Feature ID | Tên | Priority | ERPNext |
|---|-----------|------|:--------:|:-------:|
| 1 | ERP-WH-021 | BC nhập xuất tồn | Critical | ⚠️ Cần custom report |
| 2 | ERP-WH-022 | BC theo lô | High | ✅ Batch-Wise Balance |
| 3 | ERP-WH-023 | BC theo serial | High | ⚠️ Cần custom |
| 4 | ERP-WH-024 | BC theo vị trí | Medium | ❌ Custom |
| 5 | ERP-WH-025 | BC giá nhập XBQ | High | ⚠️ Cần custom |

### Web Sync (2 features)

| # | Feature ID | Tên | Priority |
|---|-----------|------|:--------:|
| 1 | ERP-WEB-003 | Đồng bộ kho | High |
| 2 | ERP-WEB-005 | Đồng bộ tồn kho (real-time) | Critical |

---

## Mối liên hệ với module khác

> Chi tiết: xem `analysis/STOCK_MODULE_CONNECTIONS.md`

```
Buying ──── Purchase Receipt ────▶ STOCK ◀──── Delivery Note ──── Selling
                                    │
                              ┌─────┼─────┐
                              ▼     ▼     ▼
                           SLE    Bin   GL Entry ──▶ ACCOUNTING
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
               Trade-in  Consignment  Import
```

---

## Vấn đề cần clarify

1. Bao nhiêu kho? Tên? Kho nào cho phép xuất âm?
2. Tracking batch hay serial cho sản phẩm nào?
3. Phương pháp giá vốn: Trung bình tháng hay Moving Average?
4. Phê duyệt trước hay sau khi submit?
5. Kiểm kê định kỳ hay đột xuất? Tần suất?
6. Barcode format: EAN-13, Code128, QR?
7. Kích thước tem nhãn?
8. Tích hợp máy scan barcode?

---

**Last Updated:** 16/02/2026
