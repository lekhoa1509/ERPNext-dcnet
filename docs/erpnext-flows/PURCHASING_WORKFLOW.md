# PURCHASING WORKFLOW - Luồng Mua hàng & Nhập hàng ERPNext

> **Nguồn:** ERP_SPECIFICATION.md Section 3 | IMPORT_PROCESS_SPECIFICATION.md | COA_ANALYSIS.md
> **Module:** 05-mua-hang | **Bàn giao:** T3 (31/03/2026)
> **Áp dụng:** Thăng Long TM + Nhật Minh Sport (2 site riêng, code chung)

---

## Mục lục

1. [Tổng quan luồng mua hàng](#1-tổng-quan-luồng-mua-hàng)
2. [ERPNext Standard Flow](#2-erpnext-standard-flow)
3. [DCNET Custom Flow (10 bước theo spec)](#3-dcnet-custom-flow-10-bước-theo-spec)
4. [Chi tiết từng DocType](#4-chi-tiết-từng-doctype)
5. [Trạng thái & Workflow](#5-trạng-thái--workflow)
6. [GL Entry - Bút toán kế toán](#6-gl-entry---bút-toán-kế-toán)
7. [Các luồng rút gọn](#7-các-luồng-rút-gọn)
8. [Batch, Serial, Barcode](#8-batch-serial-barcode)
9. [Trả hàng NCC (Debit Note)](#9-trả-hàng-ncc-debit-note)
10. [Landed Cost - Chi phí mua hàng](#10-landed-cost---chi-phí-mua-hàng)
11. [Thanh toán NCC](#11-thanh-toán-ncc)
12. [Báo cáo mua hàng](#12-báo-cáo-mua-hàng)
13. [Đặc thù ngành Golf (Thăng Long TM)](#13-đặc-thù-ngành-golf-thăng-long-tm)
14. [Phụ thuộc giữa các Module](#14-phụ-thuộc-giữa-các-module)
15. [Custom DocType bổ sung](#15-custom-doctype-bổ-sung)
16. [Quyền & Phân quyền](#16-quyền--phân-quyền)
17. [Checklist triển khai](#17-checklist-triển-khai)

---

## 1. Tổng quan luồng mua hàng

### 1.1 Sơ đồ tổng thể

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         LUỒNG MUA HÀNG ERPNEXT - DCNET FLOW                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Material   │───▶│   Supplier   │───▶│   Purchase   │───▶│   Purchase   │       │
│  │   Request    │    │   Quotation  │    │   Order      │    │   Receipt    │       │
│  │  (Yêu cầu)  │    │  (Báo giá)   │    │  (Đặt hàng)  │    │  (Nhập kho)  │       │
│  └──────────────┘    └──────────────┘    └──────┬───────┘    └──────┬───────┘       │
│         │                    │                   │                   │               │
│         │ Không bắt buộc     │ Không bắt buộc    │                   │               │
│         │                    │                   │                   │               │
│         └────────────────────┴───────────────────┘                   │               │
│                                                                      │               │
│                                                    ┌─────────────────┘               │
│                                                    │                                 │
│                                                    ▼                                 │
│                                            ┌──────────────┐    ┌──────────────┐     │
│                                            │   Purchase   │───▶│   Payment    │     │
│                                            │   Invoice    │    │   Entry      │     │
│                                            │  (Hóa đơn)   │    │  (Thanh toán)│     │
│                                            └──────┬───────┘    └──────────────┘     │
│                                                    │                                 │
│                                                    ▼                                 │
│                                            ┌──────────────┐                         │
│                                            │  GL Entry    │                         │
│                                            │  (Sổ cái)    │                         │
│                                            └──────────────┘                         │
│                                                                                     │
│  ── Bắt buộc    ─ ─ Tùy chọn                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Vai trò tham gia

| Vai trò | Trách nhiệm | DocType chính |
|---------|-------------|---------------|
| **BP Mua hàng** (Purchase User) | Lập kế hoạch, tạo PO, theo dõi giao hàng | Material Request, PO |
| **Kho** (Stock User) | Nhận hàng, kiểm đếm, nhập kho | Purchase Receipt |
| **Kế toán** (Accounts User) | Ghi nhận hóa đơn, thanh toán, đối chiếu | Purchase Invoice, Payment Entry |
| **Quản lý** (Purchase Manager) | Duyệt PO, duyệt thanh toán | PO approval, Payment approval |

### 1.3 Tóm tắt DocType và tác động

| DocType | Tác động Kho | Tác động Kế toán | Submit? |
|---------|:------------:|:-----------------:|:-------:|
| Material Request | Không | Không | Có |
| Supplier Quotation | Không | Không | Có |
| **Purchase Order** | Không | Không | Có |
| **Purchase Receipt** | **Có** (Stock Ledger) | **Có** (GL nếu Perpetual) | Có |
| **Purchase Invoice** | Tùy chọn | **Có** (GL Entry) | Có |
| **Payment Entry** | Không | **Có** (GL Entry) | Có |
| Landed Cost Voucher | **Có** (điều chỉnh giá) | **Có** (GL Entry) | Có |

---

## 2. ERPNext Standard Flow

### 2.1 Luồng đầy đủ (Full Flow)

```
Material Request (MR)
    │
    │  [Get Items From → Material Request]
    ▼
Supplier Quotation (SQ)
    │
    │  [Create → Purchase Order]
    ▼
Purchase Order (PO)
    │
    ├──────────────────────────────┐
    │  [Create → Purchase Receipt] │  [Create → Purchase Invoice]
    ▼                              ▼
Purchase Receipt (PR)         Purchase Invoice (PI)
    │                              │
    │  [Create → Purchase Invoice] │  (nếu tick "Update Stock"
    ▼                              │   → tự nhập kho luôn)
Purchase Invoice (PI)              │
    │                              │
    ├──────────────────────────────┘
    │  [Create → Payment Entry]
    ▼
Payment Entry (PE)
    │
    ▼
GL Entry (tự động)
```

### 2.2 Trạng thái tự động của Purchase Order

```
Purchase Order States:
┌────────┐    Submit    ┌─────────────────┐
│ Draft  │─────────────▶│  To Receive     │
└────────┘              │  and Bill       │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
            ┌───────────┐ ┌──────────┐ ┌──────────┐
            │To Receive │ │ To Bill  │ │Completed │
            │           │ │          │ │          │
            │(đã có PI, │ │(đã có PR,│ │(đã nhận  │
            │ chưa PR)  │ │ chưa PI) │ │ + đã PI) │
            └───────────┘ └──────────┘ └──────────┘

Các trạng thái phụ:
- Closed: Đóng PO (không nhận thêm)
- On Hold: Tạm giữ
- Cancelled: Hủy
```

### 2.3 Mối quan hệ giữa các DocType

```
Material Request ──────────────────────────────────────┐
    │                                                   │
    │ 1:N (1 MR → nhiều SQ)                            │
    ▼                                                   │
Supplier Quotation ────────────────────────────┐        │
    │                                           │        │
    │ N:1 (nhiều SQ → 1 PO tốt nhất)           │        │
    ▼                                           │        │
Purchase Order ◀────────────────────────────────┘────────┘
    │
    │ 1:N (1 PO → nhiều PR nếu nhận từng đợt)
    ▼
Purchase Receipt
    │
    │ N:1 (nhiều PR → 1 PI) hoặc 1:1
    ▼
Purchase Invoice
    │
    │ 1:N (1 PI → nhiều PE nếu trả góp)
    ▼
Payment Entry
```

---

## 3. DCNET Custom Flow (10 bước theo spec)

> **Nguồn:** ERP_SPECIFICATION.md Section 3.2

### 3.1 Sơ đồ 10 bước

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    DCNET FLOW - 10 BƯỚC MUA HÀNG (THEO SPEC KHÁCH HÀNG)           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  BP MUA HÀNG                        BP KẾ TOÁN / KHO                               │
│  ──────────                         ──────────────                                  │
│                                                                                     │
│  ┌──────────────────┐                                                               │
│  │ B1. Kế hoạch     │  Lập KH mua hàng tháng/năm                                  │
│  │     mua hàng     │  theo NCC, sản phẩm                                          │
│  └────────┬─────────┘                                                               │
│           │                                                                         │
│           ▼                                                                         │
│  ┌──────────────────┐                                                               │
│  │ B2. Đơn hàng mua │  Tạo PO, điều khoản TT,                                     │
│  │     / HĐ mua     │  điều kiện giao hàng                                         │
│  └────────┬─────────┘                                                               │
│           │                                                                         │
│           ▼                                                                         │
│  ┌──────────────────┐                                                               │
│  │ B3. Kế hoạch     │  Lịch giao: Mã PO, ngày,                                    │
│  │     giao hàng    │  người mua, SP, vận chuyển                                   │
│  └────────┬─────────┘                                                               │
│           │                                                                         │
│           ▼                                                                         │
│  ┌──────────────────┐                                                               │
│  │ B4. Đề nghị      │  Kho nhận, thông quan,                                       │
│  │     nhập hàng    │  ngày dự kiến/thực tế                                        │
│  └────────┬─────────┘                                                               │
│           │                                                                         │
│           ├─────────────────────────────────────▶ ┌──────────────────┐              │
│           │                                       │ B5. Phiếu nhập   │              │
│           │                                       │     mua/nhập khẩu│              │
│           │                                       │ So sánh giá PO   │              │
│           │                                       └────────┬─────────┘              │
│           │                                                │                        │
│           ▼                                                │                        │
│  ┌──────────────────┐                                      │                        │
│  │ B6. Chi phí      │  Vận chuyển, bốc dỡ                 │                        │
│  │     mua hàng     │  → phân bổ vào giá vốn              │                        │
│  └────────┬─────────┘                                      │                        │
│           │                                                │                        │
│           ▼                                                │                        │
│  ┌──────────────────┐                                      │                        │
│  │ B7. Lệnh xuất    │  Hàng lỗi → lập lệnh trả           │                        │
│  │     trả lại NCC  │  (chờ duyệt)                        │                        │
│  └────────┬─────────┘                                      │                        │
│           │                                                │                        │
│           ├─────────────────────────────────────▶ ┌──────────────────┐              │
│           │                                       │ B8. Phiếu xuất   │              │
│           │                                       │     trả NCC      │              │
│           │                                       │ Giảm kho + nợ    │              │
│           │                                       └────────┬─────────┘              │
│           │                                                │                        │
│           ▼                                                │                        │
│  ┌──────────────────┐                                      │                        │
│  │ B9. Xác nhận     │◀─────────────────────────────────────┘                        │
│  │     công nợ      │  Đối chiếu NCC                                               │
│  └────────┬─────────┘                                                               │
│           │                                                                         │
│           ▼                                                                         │
│  ┌──────────────────┐                                                               │
│  │ B10. Đề nghị     │  Ngày, số, NCC, số tiền,                                     │
│  │      thanh toán  │  phương thức TT                                               │
│  └──────────────────┘                                                               │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Mapping 10 bước → ERPNext DocType

| Bước | Tên | ERPNext DocType | Tag | Ghi chú |
|:----:|-----|----------------|:---:|---------|
| B1 | Kế hoạch mua hàng | **Purchase Plan** (Custom) | `NEW` | DocType mới, KH theo tháng/năm |
| B2 | Đơn hàng mua / HĐ mua | **Purchase Order** | `USE` | + custom fields |
| B3 | Kế hoạch giao hàng | **Delivery Schedule** (Custom) | `NEW` | DocType mới, track vận chuyển |
| B4 | Đề nghị nhập hàng | Purchase Order + custom fields | `EXT` | Thêm field thông quan, ngày dự kiến |
| B5 | Phiếu nhập mua/NK | **Purchase Receipt** | `USE` | + Workflow duyệt 3 bước |
| B6 | Chi phí mua hàng | **Landed Cost Voucher** | `USE` | Phân bổ CP vận chuyển, bốc dỡ |
| B7 | Lệnh xuất trả NCC | **Purchase Return** (Return Order) | `EXT` | Workflow 2 bước (lệnh → duyệt) |
| B8 | Phiếu xuất trả NCC | **Debit Note** (PI return) | `USE` | Tự động giảm kho + công nợ |
| B9 | Xác nhận công nợ | **Supplier Ledger** + Report | `CFG` | Đối chiếu công nợ |
| B10 | Đề nghị thanh toán | **Payment Entry** | `USE` | + Workflow duyệt 4 bước |

---

## 4. Chi tiết từng DocType

### 4.1 Material Request (Yêu cầu mua hàng)

**Mục đích:** Bộ phận kho hoặc sản xuất yêu cầu bổ sung hàng hóa.

```
Material Request
├── Type: Purchase (mua hàng) | Material Transfer | Material Issue
├── Required By Date
├── Items:
│   ├── Item Code
│   ├── Qty
│   ├── Warehouse (kho cần nhận)
│   ├── UOM
│   └── Description
└── Status: Draft → Submitted → Ordered (khi đã tạo PO) → Received
```

**Tạo từ:** Reorder Level tự động | Manual | BOM (sản xuất)
**Tạo tiếp:** Supplier Quotation | Purchase Order

### 4.2 Supplier Quotation (Báo giá NCC)

**Mục đích:** Thu thập và so sánh giá từ nhiều NCC.

```
Supplier Quotation
├── Supplier
├── Quotation To: Material Request
├── Valid Till (ngày hết hạn báo giá)
├── Items:
│   ├── Item Code
│   ├── Qty
│   ├── Rate (giá NCC báo)
│   ├── Amount
│   └── Lead Time Days (thời gian giao)
├── Taxes and Charges
└── Grand Total
```

**So sánh giá:** Buying → Supplier Quotation → Tool "Supplier Quotation Comparison"

### 4.3 Purchase Order (Đơn hàng mua)

**Mục đích:** Xác nhận đặt hàng với NCC — là DocType trung tâm của luồng mua hàng.

```
Purchase Order
├── Supplier
├── Company
├── Order Type: Purchase | Maintenance | Subcontracting
├── Supplier Address / Contact
├── Currency / Exchange Rate
│
├── Items (child table):
│   ├── Item Code / Item Name
│   ├── Qty / Received Qty / Returned Qty / Billed Qty
│   ├── UOM / Stock UOM / Conversion Factor
│   ├── Rate / Amount
│   ├── Warehouse (kho nhận)
│   ├── Expected Delivery Date
│   ├── Batch No (nếu batch tracking)
│   └── BOM (nếu subcontracting)
│
├── Taxes and Charges (child table):
│   ├── Charge Type: On Net Total | On Previous Row Total
│   ├── Account Head (TK thuế/phí: 1331, 3333...)
│   ├── Rate / Amount
│   └── Tax Amount
│
├── Payment Terms (child table):
│   ├── Payment Term
│   ├── Due Date
│   ├── Invoice Portion %
│   └── Payment Amount
│
├── DCNET Custom Fields: ──────────────────────
│   ├── vendor_po_number (Mã PO NCC)
│   ├── ship_mode (Phương thức vận chuyển: Sea/Air/Road)
│   ├── customs_declaration_no (Số tờ khai HQ)
│   ├── expected_clearance_date (Ngày thông quan dự kiến)
│   ├── actual_clearance_date (Ngày thông quan thực tế)
│   └── supplier_status (Trạng thái NCC: Confirmed/Rejected/Partial)
│
├── Discount: Additional Discount % or Amount
├── Grand Total / Rounded Total
├── Terms and Conditions (template)
├── Print Heading
│
└── Status: Draft → Submitted → To Receive and Bill
                                → To Receive
                                → To Bill
                                → Completed
                                → Closed / Cancelled
```

**Tạo từ:** Material Request | Supplier Quotation | Manual
**Tạo tiếp:** Purchase Receipt | Purchase Invoice | Payment Entry

### 4.4 Purchase Receipt (Phiếu nhập kho)

**Mục đích:** Ghi nhận hàng nhập kho thực tế. **Đây là DocType tạo Stock Ledger Entry.**

```
Purchase Receipt
├── Supplier
├── Posting Date / Time
├── Supplier Delivery Note (số phiếu giao NCC)
│
├── Items (child table):
│   ├── Item Code / Item Name
│   ├── Qty (accepted) / Rejected Qty
│   ├── Rate / Amount
│   ├── Warehouse (kho nhận)
│   ├── Rejected Warehouse (kho hàng lỗi)
│   ├── Batch No (tạo mới hoặc chọn)
│   ├── Serial No (danh sách serial, 1 dòng/serial)
│   ├── Quality Inspection (nếu có)
│   ├── Purchase Order (liên kết PO)
│   └── Purchase Order Item (liên kết dòng PO)
│
├── Taxes and Charges
├── Additional Costs (landed cost sơ bộ)
│
├── DCNET Custom Fields: ──────────────────────
│   ├── receipt_approval_status: Draft | Pending Approval | Received
│   └── inspector_name (Người kiểm hàng)
│
└── Status: Draft → To Bill → Completed → Cancelled
            (+ Custom Workflow: Draft → Chờ duyệt → Đã nhập kho)
```

**Tác động khi Submit:**

```
Stock Ledger Entry:
  ┌──────────────────────────────────────────┐
  │ Item: GOLF-CLUB-001                      │
  │ Warehouse: Kho Chính - TM                │
  │ Actual Qty: +10                          │
  │ Incoming Rate: 5,000,000 VND             │
  │ Valuation Rate: recalculated             │
  │ Stock Value: updated                     │
  └──────────────────────────────────────────┘

GL Entry (Perpetual Inventory):
  ┌──────────────────────────────────────────┐
  │ Nợ 1561 (Hàng hóa)      50,000,000      │
  │ Có 331  (Phải trả NCC)  50,000,000      │
  └──────────────────────────────────────────┘
```

### 4.5 Purchase Invoice (Hóa đơn mua hàng)

**Mục đích:** Ghi nhận hóa đơn từ NCC. Tạo bút toán công nợ + thuế.

```
Purchase Invoice
├── Supplier
├── Bill No (số hóa đơn NCC)
├── Bill Date
├── Due Date
├── Is Return: ☐ (tick = Debit Note / trả hàng)
├── Update Stock: ☐ (tick = nhập kho luôn, không cần PR riêng)
│
├── Items (child table):
│   ├── Item Code / Item Name
│   ├── Qty / Rate / Amount
│   ├── Expense Account (TK chi phí: 1561 / 632...)
│   ├── Purchase Receipt (liên kết PR)
│   ├── Purchase Order (liên kết PO)
│   ├── Warehouse (nếu Update Stock = ☑)
│   ├── Batch No / Serial No (nếu Update Stock = ☑)
│   └── Deferred Expense Account (chi phí trả trước)
│
├── Taxes and Charges (child table):
│   ├── Account Head: 1331 (VAT đầu vào)
│   ├── Rate: 10%
│   └── Tax Amount: auto-calculated
│
├── Payment Schedule (child table):
│   ├── Due Date
│   ├── Invoice Portion %
│   └── Payment Amount
│
├── Advances (child table):
│   └── Liên kết Payment Entry đã trả trước
│
└── Status: Draft → Submitted → Paid / Overdue / Unpaid
                               → Cancelled
                               → Debit Note Issued (nếu trả hàng)
```

**Tác động khi Submit:**

```
GL Entry:
  ┌──────────────────────────────────────────────────────┐
  │ Nợ 1561  (Hàng hóa)           45,000,000            │
  │ Nợ 1331  (VAT đầu vào 10%)     5,000,000            │
  │ Có 331   (Phải trả NCC)       50,000,000            │
  └──────────────────────────────────────────────────────┘

  Nếu Update Stock = ☑ → thêm Stock Ledger Entry (như PR)
```

### 4.6 Payment Entry (Thanh toán)

**Mục đích:** Ghi nhận thanh toán cho NCC.

```
Payment Entry
├── Payment Type: Pay (chi tiền)
├── Party Type: Supplier
├── Party: [Supplier Name]
├── Paid From: 1111 (Tiền mặt) hoặc 1121 (Ngân hàng)
├── Paid To: 331 (Phải trả NCC)
├── Paid Amount / Received Amount
├── Mode of Payment: Cash | Wire Transfer | Check
│
├── References (child table):
│   ├── Reference Type: Purchase Invoice
│   ├── Reference Name: PI-2026-00001
│   ├── Total Amount
│   ├── Outstanding Amount
│   └── Allocated Amount (số tiền thanh toán cho PI này)
│
├── Deductions (child table):
│   ├── Account: (chiết khấu thanh toán, CK được hưởng)
│   └── Amount
│
├── DCNET Custom Workflow: ──────────────────────
│   ├── Draft (BP Mua hàng tạo)
│   ├── Đề nghị TT (chờ KT duyệt)
│   ├── Approved (KT đã duyệt)
│   └── Submitted / Paid (đã thực hiện)
│
└── Status: Draft → Submitted → Cancelled
```

**Tác động khi Submit:**

```
GL Entry:
  ┌──────────────────────────────────────────────────────┐
  │ Nợ 331   (Phải trả NCC)       50,000,000            │
  │ Có 1121  (Tiền gửi NH)        50,000,000            │
  └──────────────────────────────────────────────────────┘

  → Outstanding Amount trên Purchase Invoice giảm về 0
  → PI status chuyển thành "Paid"
```

---

## 5. Trạng thái & Workflow

### 5.1 Purchase Receipt - Workflow duyệt 3 bước (DCNET Custom)

```
                     ┌──────────────────────────────────┐
                     │    PURCHASE RECEIPT WORKFLOW      │
                     │         (DCNET Custom)            │
                     └──────────────────────────────────┘

┌─────────┐    Tạo phiếu    ┌──────────────┐    KT/QL duyệt    ┌──────────────┐
│  Draft  │───────────────▶│  Chờ duyệt   │──────────────────▶│  Đã nhập kho │
│         │  (BP Mua hàng)  │  (Pending    │  (Accounts User)  │  (Received)  │
│         │                 │   Approval)  │                   │              │
└─────────┘                 └──────┬───────┘                   └──────────────┘
                                   │                                  │
                                   │ Từ chối                          │ Submit
                                   ▼                                  ▼
                            ┌──────────────┐                  ┌──────────────┐
                            │  Rejected    │                  │ Stock Ledger │
                            │              │                  │ + GL Entry   │
                            └──────────────┘                  └──────────────┘

Quyền:
- Purchase User: Tạo, sửa Draft
- Stock User: Xem, xác nhận kiểm hàng
- Accounts User: Duyệt / Từ chối
- Purchase Manager: Duyệt / Từ chối / Hủy
```

### 5.2 Payment Entry - Workflow duyệt 4 bước (DCNET Custom)

```
                     ┌──────────────────────────────────┐
                     │    PAYMENT ENTRY WORKFLOW        │
                     │         (DCNET Custom)            │
                     └──────────────────────────────────┘

┌─────────┐    Tạo đề nghị   ┌──────────────┐    KT duyệt    ┌──────────────┐
│  Draft  │────────────────▶│  Đề nghị TT  │──────────────▶│  Approved    │
│         │  (BP Mua hàng)   │  (Payment    │  (Accounts    │              │
│         │                  │   Request)   │   Manager)    │              │
└─────────┘                  └──────┬───────┘               └──────┬───────┘
                                    │                              │
                                    │ Từ chối                      │ Submit
                                    ▼                              ▼
                             ┌──────────────┐              ┌──────────────┐
                             │  Rejected    │              │  Submitted   │
                             │              │              │  (Paid)      │
                             └──────────────┘              └──────────────┘
```

### 5.3 Return - Workflow 2 bước (DCNET Custom)

```
                     ┌──────────────────────────────────┐
                     │    PURCHASE RETURN WORKFLOW       │
                     │         (DCNET Custom)            │
                     └──────────────────────────────────┘

┌─────────┐    Tạo lệnh trả   ┌──────────────┐    QL duyệt    ┌──────────────┐
│  Draft  │───────────────────▶│  Chờ duyệt   │──────────────▶│  Approved    │
│ (Lệnh  │  (BP Mua hàng)     │  Return Order │  (Purchase    │              │
│  xuất)  │                    │               │   Manager)    │              │
└─────────┘                    └───────────────┘               └──────┬───────┘
                                                                      │
                                                            Submit Debit Note
                                                                      │
                                                                      ▼
                                                               ┌──────────────┐
                                                               │  Debit Note  │
                                                               │  (PI Return) │
                                                               │  + PR Return │
                                                               └──────────────┘
```

---

## 6. GL Entry - Bút toán kế toán

### 6.1 Tổng hợp bút toán theo từng bước

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        BÚT TOÁN KẾ TOÁN - MUA HÀNG                            │
├──────────────────┬──────────────────────────────────────────────────────────────┤
│                  │                                                              │
│  PURCHASE        │  Nợ 1561 (Hàng hóa)              50,000,000                │
│  RECEIPT         │  Có 331  (Phải trả NCC)           50,000,000                │
│  (Nhập kho)      │  → Stock Ledger: +10 units @ 5,000,000                     │
│                  │                                                              │
├──────────────────┼──────────────────────────────────────────────────────────────┤
│                  │                                                              │
│  PURCHASE        │  Nợ 1561 (Hàng hóa)              45,454,545                │
│  INVOICE         │  Nợ 1331 (VAT đầu vào 10%)        4,545,455                │
│  (Hóa đơn)       │  Có 331  (Phải trả NCC)           50,000,000                │
│                  │                                                              │
│  ⚠️ Lưu ý:      │  Nếu đã có PR → PI chỉ ghi nhận thuế, điều chỉnh          │
│                  │  Nếu PI tick "Update Stock" → gộp cả 2 bút toán           │
│                  │                                                              │
├──────────────────┼──────────────────────────────────────────────────────────────┤
│                  │                                                              │
│  LANDED COST     │  Nợ 1561 (Tăng giá vốn hàng)      2,000,000                │
│  VOUCHER         │  Có 1562 (CP thu mua) hoặc         2,000,000                │
│  (Chi phí mua)   │  Có 331  (nếu NCC vận chuyển)                              │
│                  │  → Stock Ledger: điều chỉnh valuation rate                  │
│                  │                                                              │
├──────────────────┼──────────────────────────────────────────────────────────────┤
│                  │                                                              │
│  PAYMENT         │  Nợ 331  (Phải trả NCC)           50,000,000                │
│  ENTRY           │  Có 1121 (Tiền gửi NH)            50,000,000                │
│  (Thanh toán)    │  hoặc Có 1111 (Tiền mặt)                                   │
│                  │                                                              │
├──────────────────┼──────────────────────────────────────────────────────────────┤
│                  │                                                              │
│  DEBIT NOTE      │  Nợ 331  (Giảm công nợ NCC)       10,000,000                │
│  (Trả hàng)      │  Có 1561 (Giảm hàng tồn)          10,000,000                │
│                  │  → Stock Ledger: -2 units                                   │
│                  │                                                              │
└──────────────────┴──────────────────────────────────────────────────────────────┘
```

### 6.2 Tài khoản liên quan

| TK | Tên | Account Type | Vai trò |
|----|-----|:------------:|---------|
| **1111** | Tiền mặt | Cash | Thanh toán tiền mặt |
| **1121** | Tiền gửi ngân hàng | Bank | Thanh toán chuyển khoản |
| **1331** | Thuế GTGT đầu vào | Tax | VAT được khấu trừ |
| **1561** | Giá mua hàng hóa | Stock | Giá trị hàng nhập kho |
| **1562** | CP thu mua hàng hóa | Expenses Included In Asset Valuation | Vận chuyển, bốc dỡ |
| **331** | Phải trả người bán | Payable | Công nợ NCC |
| **3333** | Thuế NK | Tax | Thuế nhập khẩu (nếu có) |

### 6.3 Ví dụ End-to-End

```
Ví dụ: Mua 10 gậy golf Driver từ NCC Titleist, giá 5,000,000/cái, VAT 10%
       Vận chuyển 2,000,000, thanh toán chuyển khoản sau 30 ngày

═══════════════════════════════════════════════════════════════════

BƯỚC 1: Purchase Receipt (nhận hàng vào kho)
─────────────────────────────────────────────
  Nợ 1561    50,000,000    (10 x 5,000,000)
  Có 331     50,000,000
  → Stock: +10 Driver @ 5,000,000/cái

BƯỚC 2: Landed Cost Voucher (phân bổ CP vận chuyển)
────────────────────────────────────────────────────
  Nợ 1561     2,000,000    (phân bổ đều 200,000/cái)
  Có 1562     2,000,000
  → Stock: 10 Driver @ 5,200,000/cái (đã cộng CP)

BƯỚC 3: Purchase Invoice (ghi nhận hóa đơn + VAT)
──────────────────────────────────────────────────
  Nợ 1561    45,454,545    ← điều chỉnh (vì PR đã ghi 50tr)
  Nợ 1331     5,000,000    (VAT 10% = 50,000,000 x 10%)
  Có 331      50,454,545   ← cân đối
  ⚠️ Thực tế ERPNext tự điều chỉnh khi PI liên kết PR

  Tổng công nợ NCC (331): 50,000,000 (PR) + 5,000,000 (VAT) = 55,000,000

BƯỚC 4: Payment Entry (thanh toán sau 30 ngày)
──────────────────────────────────────────────
  Nợ 331     55,000,000
  Có 1121    55,000,000
  → Outstanding = 0, PI status = "Paid"

═══════════════════════════════════════════════════════════════════
TỔNG KẾT CUỐI:
  Kho: +10 Driver, giá vốn 5,200,000/cái (đã gồm CP vận chuyển)
  Công nợ NCC: 0 (đã thanh toán hết)
  VAT đầu vào: 5,000,000 (khấu trừ kỳ thuế)
  Bank: -55,000,000
═══════════════════════════════════════════════════════════════════
```

---

## 7. Các luồng rút gọn

### 7.1 Tổng hợp các luồng

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          CÁC LUỒNG MUA HÀNG                                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  LUỒNG 1: ĐẦY ĐỦ (có kế hoạch, nhiều NCC)                                    │
│  MR → SQ → PO → PR → PI → PE                                                   │
│  Khi nào: Mua lô lớn, cần so sánh giá, nhiều NCC                              │
│                                                                                  │
│  LUỒNG 2: MUA TRỰC TIẾP (biết NCC, biết giá)                                  │
│  PO → PR → PI → PE                                                              │
│  Khi nào: NCC quen, giá đã thỏa thuận, hàng golf theo mùa                     │
│                                                                                  │
│  LUỒNG 3: MUA NHẬN NGAY (hóa đơn cùng lúc nhận hàng)                          │
│  PO → PI (✓ Update Stock) → PE                                                  │
│  Khi nào: Hàng giao kèm HĐ, không cần kiểm riêng                             │
│                                                                                  │
│  LUỒNG 4: MUA LẺ (không cần PO)                                                │
│  PI (✓ Update Stock) → PE                                                        │
│  Khi nào: Mua văn phòng phẩm, vật tư nhỏ                                      │
│                                                                                  │
│  LUỒNG 5: NHẬP KHẨU (có thông quan)                                            │
│  Purchase Plan → PO (+customs fields) → Delivery Schedule                       │
│  → PR (+QC) → Landed Cost → PI → PE                                            │
│  Khi nào: Hàng golf nhập khẩu từ nước ngoài (Titleist, Callaway...)           │
│                                                                                  │
│  LUỒNG 6: TRẢ HÀNG NCC                                                         │
│  Return Order (draft) → Approve → Debit Note (PI return) + PR return            │
│  Khi nào: Hàng lỗi, sai model, thiếu                                          │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Sơ đồ quyết định chọn luồng

```
                        Bắt đầu mua hàng
                              │
                              ▼
                    ┌─────────────────┐
                    │ Cần so sánh giá │
                    │ nhiều NCC?      │
                    └────────┬────────┘
                        Có   │   Không
                    ┌────────┘────────┐
                    ▼                 ▼
              Luồng 1 (MR→SQ)  ┌─────────────────┐
                               │ Giá trị lớn hoặc │
                               │ hàng nhập khẩu?   │
                               └────────┬──────────┘
                                   Có   │   Không
                               ┌────────┘────────┐
                               ▼                 ▼
                        ┌───────────┐    ┌─────────────────┐
                        │ Có thông  │    │ Hàng giao kèm   │
                        │ quan?     │    │ hóa đơn?         │
                        └─────┬─────┘    └────────┬────────┘
                         Có   │Không        Có    │  Không
                         │    │             │     │
                         ▼    ▼             ▼     ▼
                      Luồng 5 Luồng 2   Luồng 3  ┌──────────┐
                      (NK)    (TT)       (PI+Stock)│ Giá trị  │
                                                   │ nhỏ?     │
                                                   └────┬─────┘
                                                    Có  │Không
                                                    │   │
                                                    ▼   ▼
                                                 Luồng 4 Luồng 2
                                                 (PI only)(PO→PR→PI)
```

---

## 8. Batch, Serial, Barcode

### 8.1 Batch Tracking (Nhập hàng theo lô)

```
Cấu hình Item:
  Item → Has Batch No: ☑
  Item → Create New Batch: ☑ (tự tạo batch mới khi nhập)
  Item → Batch Number Series: BATCH-.YYYY.-.####

Khi tạo Purchase Receipt:
  ┌──────────────────────────────────────────────────┐
  │ Item: GOLF-CLUB-DRIVER-TSi3                      │
  │ Qty: 50                                          │
  │ Batch No: BATCH-2026-0042 (tự tạo hoặc chọn)    │
  │ Warehouse: Kho Chính                             │
  └──────────────────────────────────────────────────┘

Thông tin batch:
  ┌──────────────────────────────────────────────────┐
  │ Batch ID: BATCH-2026-0042                        │
  │ Item: GOLF-CLUB-DRIVER-TSi3                      │
  │ Batch Qty: 50                                    │
  │ Manufacturing Date: 2026-01-15                   │
  │ Expiry Date: (nếu có)                            │
  │ Reference Document: PR-2026-00123                │
  │ Supplier: Titleist Japan                         │
  └──────────────────────────────────────────────────┘

Truy xuất:
  Stock → Stock Balance → filter by Batch No
  Bán hàng: chọn Batch khi tạo Delivery Note
```

### 8.2 Serial Number Tracking (Nhập hàng theo serial)

```
Cấu hình Item:
  Item → Has Serial No: ☑
  Item → Serial No Series: SN-.YYYY.-.######

Khi tạo Purchase Receipt:
  ┌──────────────────────────────────────────────────┐
  │ Item: GOLF-CLUB-DRIVER-TSi3                      │
  │ Qty: 3                                           │
  │ Serial No:                                       │
  │   SN-2026-000101                                 │
  │   SN-2026-000102                                 │
  │   SN-2026-000103                                 │
  │ (mỗi serial 1 dòng, qty = số dòng serial)       │
  └──────────────────────────────────────────────────┘

Mỗi Serial No là 1 DocType riêng:
  ┌──────────────────────────────────────────────────┐
  │ Serial No: SN-2026-000101                        │
  │ Item: GOLF-CLUB-DRIVER-TSi3                      │
  │ Status: Active                                   │
  │ Warehouse: Kho Chính                             │
  │ Purchase Document: PR-2026-00123                 │
  │ Purchase Date: 2026-03-15                        │
  │ Supplier: Titleist Japan                         │
  │ Delivery Document: (khi bán)                     │
  │ Customer: (khi bán)                              │
  └──────────────────────────────────────────────────┘
```

### 8.3 Barcode (Mã vạch)

```
Cấu hình Item:
  Item → Barcodes (child table):
  ┌──────────────────────────────────────────────────┐
  │ Barcode: 4549821346271                           │
  │ Barcode Type: EAN                                │
  │                                                  │
  │ Barcode: 012345678905                            │
  │ Barcode Type: UPC-A                              │
  └──────────────────────────────────────────────────┘

Scan khi nhập hàng (Purchase Receipt):
  1. Click nút "Scan Barcode" trên form
  2. Quét mã vạch bằng máy quét / camera
  3. Hệ thống tự động:
     - Tìm Item có barcode tương ứng
     - Thêm dòng vào Items table
     - Set Qty = 1 (quét lần nữa → tăng qty)
  4. Xác nhận và submit

Flow scan:
  ┌────────────┐    Scan    ┌────────────┐    Match    ┌────────────┐
  │  Barcode   │──────────▶│  Lookup    │───────────▶│  Add Item  │
  │  Scanner   │           │  Item by   │            │  to PR     │
  │            │           │  Barcode   │            │  (qty +1)  │
  └────────────┘           └────────────┘            └────────────┘
```

### 8.4 Kết hợp Batch + Serial + Barcode

```
Ví dụ: Nhập 3 gậy Driver Titleist TSi3

Item Config:
  Has Batch No: ☑
  Has Serial No: ☑
  Barcodes: EAN 4549821346271

Purchase Receipt:
  ┌──────────────────────────────────────────────────┐
  │ Item: GOLF-DRIVER-TSi3                           │
  │ Qty: 3                                           │
  │ Batch: BATCH-2026-0042                           │
  │ Serial No:                                       │
  │   TSi3-2026-001                                  │
  │   TSi3-2026-002                                  │
  │   TSi3-2026-003                                  │
  │ Barcode: 4549821346271 (dùng khi scan)           │
  │ Warehouse: Kho Chính - TM                        │
  │ Rate: 15,000,000                                 │
  └──────────────────────────────────────────────────┘

Kết quả:
  - 1 Batch record (BATCH-2026-0042) → 3 items
  - 3 Serial No records (TSi3-2026-001/002/003)
  - Mỗi serial thuộc batch BATCH-2026-0042
  - Scan barcode 4549821346271 khi bán → chọn serial cụ thể
```

---

## 9. Trả hàng NCC (Debit Note)

### 9.1 Sơ đồ luồng trả hàng

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    LUỒNG TRẢ HÀNG NCC (PURCHASE RETURN)                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────┐                                                           │
│  │ Phát hiện hàng   │  Hàng lỗi, sai model, thiếu, hết hạn...                │
│  │ cần trả          │                                                           │
│  └────────┬─────────┘                                                           │
│           │                                                                     │
│           ▼                                                                     │
│  ┌──────────────────┐                                                           │
│  │ B7. Lệnh xuất    │  BP Mua hàng tạo                                        │
│  │ trả lại NCC      │  Chọn Purchase Receipt gốc                              │
│  │ (Return Order)   │  Chọn items + qty cần trả                               │
│  └────────┬─────────┘                                                           │
│           │                                                                     │
│           ▼                                                                     │
│  ┌──────────────────┐                                                           │
│  │ Purchase Manager │  Kiểm tra lý do, xác nhận                               │
│  │ Duyệt            │                                                           │
│  └────────┬─────────┘                                                           │
│           │                                                                     │
│      ┌────┴────┐                                                                │
│      ▼         ▼                                                                │
│  ┌────────┐ ┌────────────────────────────────────────┐                          │
│  │Rejected│ │  B8. Tạo Debit Note (PI return)        │                          │
│  └────────┘ │  Purchase Invoice → Is Return: ☑       │                          │
│             │  Against Purchase Invoice: PI-xxx       │                          │
│             │  Items → Qty: ÂM (-2)                   │                          │
│             └─────────────────────┬──────────────────┘                          │
│                                   │                                              │
│                                   │ Submit                                       │
│                                   ▼                                              │
│             ┌──────────────────────────────────────────┐                         │
│             │  Tác động:                                │                         │
│             │  1. Stock Ledger: -2 items từ kho         │                         │
│             │  2. GL: Nợ 331, Có 1561 (đảo bút toán)  │                         │
│             │  3. Outstanding NCC giảm                  │                         │
│             └──────────────────────────────────────────┘                         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Cách tạo Debit Note trong ERPNext

```
Cách 1: Từ Purchase Invoice
  Purchase Invoice → Menu → Make Return / Debit Note
  → Tự tạo PI mới với Is Return = ☑, qty ÂM

Cách 2: Từ Purchase Receipt
  Purchase Receipt → Menu → Make Return
  → Tự tạo PR mới với Is Return = ☑, qty ÂM
  → Sau đó tạo Debit Note từ PR return này

Cách 3: Manual
  Tạo Purchase Invoice mới
  → Tick "Is Return"
  → Chọn "Against Purchase Invoice"
  → Nhập items với qty ÂM
```

### 9.3 GL Entry khi trả hàng

```
Debit Note (Purchase Invoice Return):
  ┌──────────────────────────────────────────────────────┐
  │ Nợ 331   (Phải trả NCC)       -10,000,000           │
  │ Có 1561  (Hàng hóa)           -10,000,000           │
  │                                                      │
  │ Hoặc viết theo chiều đảo:                            │
  │ Nợ 331   (Giảm công nợ NCC)    10,000,000           │
  │ Có 1561  (Giảm giá trị kho)    10,000,000           │
  └──────────────────────────────────────────────────────┘

Stock Ledger:
  ┌──────────────────────────────────────────────────────┐
  │ Item: GOLF-DRIVER-TSi3                               │
  │ Actual Qty: -2                                       │
  │ Warehouse: Kho Chính → (hoặc Kho trả hàng)         │
  └──────────────────────────────────────────────────────┘
```

---

## 10. Landed Cost - Chi phí mua hàng

### 10.1 Khái niệm

Landed Cost = Tổng chi phí để hàng hóa "đến được kho", bao gồm:
- Giá mua (purchase price)
- Vận chuyển (freight/shipping)
- Bốc dỡ (loading/unloading)
- Bảo hiểm (insurance)
- Thuế nhập khẩu (customs duty)
- Phí thông quan (customs clearance fee)
- Các phí khác

### 10.2 Luồng Landed Cost Voucher

```
┌──────────────────────────────────────────────────────────────────┐
│                  LANDED COST VOUCHER FLOW                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Bước 1: Tạo Purchase Receipt (nhập kho giá gốc)               │
│  ──────────────────────────────────────                          │
│  PR-001: 10 Driver @ 5,000,000 = 50,000,000                    │
│                                                                  │
│  Bước 2: Nhận hóa đơn chi phí vận chuyển                       │
│  ──────────────────────────────────────                          │
│  HĐ vận chuyển: 3,000,000                                      │
│  HĐ bốc dỡ: 500,000                                            │
│  Thuế NK: 2,500,000                                             │
│  Tổng Landed Cost: 6,000,000                                    │
│                                                                  │
│  Bước 3: Tạo Landed Cost Voucher                                │
│  ──────────────────────────────────────                          │
│  ┌────────────────────────────────────────────────────┐          │
│  │ Landed Cost Voucher                                 │          │
│  │                                                     │          │
│  │ Purchase Receipts:                                  │          │
│  │   PR-001 (10 Driver, 50,000,000)                   │          │
│  │                                                     │          │
│  │ Taxes and Charges:                                  │          │
│  │   Vận chuyển  │ 1562 │ 3,000,000                   │          │
│  │   Bốc dỡ     │ 1562 │   500,000                   │          │
│  │   Thuế NK     │ 3333 │ 2,500,000                   │          │
│  │                                                     │          │
│  │ Distribute By: Qty (hoặc Amount hoặc Manual)       │          │
│  └────────────────────────────────────────────────────┘          │
│                                                                  │
│  Bước 4: Submit → Điều chỉnh giá vốn                           │
│  ──────────────────────────────────────                          │
│  Trước: 10 Driver @ 5,000,000/cái                               │
│  Landed Cost: 6,000,000 / 10 = 600,000/cái                      │
│  Sau:   10 Driver @ 5,600,000/cái                               │
│                                                                  │
│  GL Entry:                                                       │
│  Nợ 1561  6,000,000 (tăng giá vốn hàng)                        │
│  Có 1562  3,500,000 (CP vận chuyển + bốc dỡ)                   │
│  Có 3333  2,500,000 (thuế NK)                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.3 Phương thức phân bổ

| Phương thức | Mô tả | Khi nào dùng |
|------------|-------|-------------|
| **By Qty** | Chia đều theo số lượng | Items cùng loại, kích thước tương đương |
| **By Amount** | Chia theo tỷ lệ giá trị | Items khác giá trị, khác loại |
| **Manual** | Nhập tay cho từng item | Biết chính xác chi phí từng item |

---

## 11. Thanh toán NCC

### 11.1 Các hình thức thanh toán

```
┌─────────────────────────────────────────────────────────────────┐
│                   PHƯƠNG THỨC THANH TOÁN                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. THANH TOÁN NGAY (Cash on Delivery)                          │
│     PO → PR → PI → PE (ngay khi nhận hóa đơn)                  │
│     TK: Nợ 331, Có 1111                                        │
│                                                                  │
│  2. CHUYỂN KHOẢN (Bank Transfer)                                │
│     PO → PR → PI → PE (theo payment terms)                     │
│     TK: Nợ 331, Có 1121                                        │
│                                                                  │
│  3. TRẢ GÓP / THEO KỲ (Credit Terms)                          │
│     PO → PR → PI → PE1 (50%) → PE2 (30%) → PE3 (20%)         │
│     Payment Schedule trên PI                                    │
│                                                                  │
│  4. ỨNG TRƯỚC (Advance Payment)                                │
│     PE (ứng trước) → PO → PR → PI (trừ ứng trước)            │
│     TK ứng: Nợ 331 (Advance), Có 1121                         │
│     Khi nhận PI: tự trừ advance, chỉ thanh toán phần còn lại  │
│                                                                  │
│  5. THANH TOÁN BÙ TRỪ (Netting)                                │
│     NCC vừa bán vừa mua                                        │
│     Journal Entry: Nợ 331 (giảm nợ NCC), Có 131 (giảm nợ KH) │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 11.2 Payment Terms (Điều khoản thanh toán)

```
Ví dụ: Payment Term "30-70 trong 60 ngày"
  ┌──────────────────────────────────────────────────────┐
  │ Payment Terms Template: NCC-30-70                    │
  │                                                      │
  │ Row 1:                                               │
  │   Invoice Portion: 30%                               │
  │   Due Date Based On: Day(s) after invoice date       │
  │   Credit Days: 0 (thanh toán ngay)                  │
  │                                                      │
  │ Row 2:                                               │
  │   Invoice Portion: 70%                               │
  │   Due Date Based On: Day(s) after invoice date       │
  │   Credit Days: 60                                    │
  │                                                      │
  │ Khi tạo PI 100,000,000:                             │
  │   Due 1: 30,000,000 - ngày hóa đơn                 │
  │   Due 2: 70,000,000 - 60 ngày sau                   │
  └──────────────────────────────────────────────────────┘
```

### 11.3 Advance Payment (Ứng trước)

```
Luồng ứng trước:
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  1. Tạo Payment Entry (trước khi có PI)                │
  │     Payment Type: Pay                                   │
  │     Party: Supplier ABC                                 │
  │     Amount: 20,000,000                                  │
  │     ⚠️ KHÔNG chọn Reference (chưa có PI)               │
  │                                                         │
  │  GL: Nợ 331 (Advance)  20,000,000                      │
  │      Có 1121            20,000,000                      │
  │                                                         │
  │  2. Sau đó tạo Purchase Invoice 50,000,000             │
  │     → Section "Advance Payments"                        │
  │     → Tự hiện PE ứng trước: 20,000,000                 │
  │     → Tick để trừ advance                               │
  │     → Outstanding còn: 30,000,000                       │
  │                                                         │
  │  3. Thanh toán phần còn lại                             │
  │     PE: 30,000,000 → Reference: PI                     │
  │     → Outstanding = 0                                   │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

---

## 12. Báo cáo mua hàng

### 12.1 Báo cáo ERPNext có sẵn

| Báo cáo | Đường dẫn | Mô tả |
|---------|----------|-------|
| Purchase Analytics | Buying → Reports | Phân tích theo NCC/Item/nhóm, theo kỳ |
| Purchase Order Analysis | Buying → Reports | PO theo trạng thái, NCC, thời gian |
| Supplier-Wise Sales Analytics | Buying → Reports | Phân tích mua theo NCC |
| Items To Be Requested | Buying → Reports | Items dưới reorder level |
| Requested Items To Order | Buying → Reports | MR chưa tạo PO |
| Purchase Order Items To Receive | Buying → Reports | PO đã đặt chưa nhận |
| Purchase Invoice Trends | Buying → Reports | Xu hướng PI theo thời gian |
| Accounts Payable | Accounts → Reports | Công nợ NCC, aging |
| Accounts Payable Summary | Accounts → Reports | Tổng hợp công nợ theo NCC |

### 12.2 Báo cáo DCNET Custom (cần build)

| Báo cáo | Mô tả | Loại |
|---------|-------|:----:|
| **Giá mua bình quân** | Giá TB theo item, NCC, kỳ | Script Report |
| **NCC tốt nhất** | Xếp hạng NCC theo giá, giao hàng đúng hẹn, chất lượng | Script Report |
| **So sánh KH mua vs Thực tế** | Purchase Plan vs PO, % hoàn thành | Script Report |
| **Lịch sử mua theo Item** | Tất cả PO/PR/PI cho 1 item, timeline | Script Report |
| **Chi phí mua hàng chi tiết** | Landed Cost breakdown theo item, lô | Script Report |

---

## 13. Đặc thù ngành Golf (Thăng Long TM)

### 13.1 Lịch đặt hàng theo mùa

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    LỊCH ĐẶT HÀNG - THĂNG LONG TM                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  THÁNG │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │ 10 │ 11 │ 12 │        │
│  ──────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤        │
│  Clubs │████│████│    │    │    │    │    │    │████│████│    │    │ MOQ 10  │
│  (new) │SHIP│SHIP│    │    │    │    │    │    │ĐẶT │ĐẶT │    │    │ 3th trước│
│  ──────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤        │
│  Soft  │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ ĐH │ Monthly│
│  goods │    │    │    │    │    │    │    │    │    │    │    │    │ trước 5th│
│  ──────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤        │
│  JP    │    │    │    │    │    │████│████│    │    │    │████│████│ 2x/năm │
│  Aparel│    │    │    │    │    │S/S │S/S │    │    │    │F/W │F/W │ SS & FW│
│  ──────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤        │
│  Putter│    │    │    │    │    │    │    │    │    │████│    │    │ Annual │
│  Wedge │    │    │    │    │    │    │    │    │    │████│    │    │ 3th trước│
│                                                                                 │
│  ████ = Thời điểm đặt hàng / nhận hàng                                        │
│  ĐH  = Đặt hàng                                                               │
│  S/S = Spring/Summer, F/W = Fall/Winter                                        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 13.2 Quy trình nội bộ Thăng Long TM (9 bước)

```
┌────────────────────────────────────────────────────────────────────────────┐
│             QUY TRÌNH MUA HÀNG NỘI BỘ - THĂNG LONG TM                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. Theo dõi lịch đặt hàng của hãng                                      │
│     └─ Lịch cố định (fixed) + đặt hàng đặc biệt (special)              │
│                                                                            │
│  2. Khám phá & trải nghiệm SP mới (hàng năm)                            │
│     └─ GĐ Kinh doanh + 6 bộ phận đánh giá                              │
│                                                                            │
│  3. Nhận Order Form từ hãng                                               │
│     ├─ Thu thập pre-order từ đại lý                                      │
│     ├─ Tổng hợp đơn đặt hàng                                            │
│     └─ GĐ duyệt pre-order                                               │
│                     │                                                     │
│                     ▼ ERPNext: Purchase Plan (Custom DocType)             │
│                                                                            │
│  4. Xác nhận đơn hàng                                                     │
│     ├─ Gửi PO cho NCC                                                    │
│     └─ NCC xác nhận / từ chối / điều chỉnh                              │
│                     │                                                     │
│                     ▼ ERPNext: Purchase Order (supplier_status field)     │
│                                                                            │
│  5. Kế hoạch giao hàng                                                    │
│     ├─ NCC gửi lịch giao (1 tháng trước)                                │
│     ├─ TM tạo PO (cho kế toán)                                          │
│     └─ Phản hồi NCC trong 5 ngày                                        │
│                     │                                                     │
│                     ▼ ERPNext: Delivery Schedule (Custom DocType)         │
│                                                                            │
│  6. Vận chuyển & theo dõi                                                 │
│     ├─ Phối hợp forwarder (Sea/Air)                                      │
│     ├─ Cập nhật hàng tuần cho các BP                                     │
│     └─ Báo cáo BLĐ                                                      │
│                     │                                                     │
│                     ▼ ERPNext: PO custom fields (ship_mode, customs)      │
│                                                                            │
│  7. Nhận hàng & kiểm tra (1 ngày)                                        │
│     ├─ Kiểm đếm số lượng                                                │
│     ├─ Kiểm tra chất lượng                                               │
│     └─ So sánh với PO                                                    │
│                     │                                                     │
│                     ▼ ERPNext: Purchase Receipt + QC Inspection           │
│                                                                            │
│  8. Ghi nhận & xử lý chênh lệch                                          │
│     ├─ Đúng → nhập kho                                                   │
│     ├─ Thừa → liên hệ NCC                                               │
│     └─ Thiếu/lỗi → tạo Return Order                                     │
│                     │                                                     │
│                     ▼ ERPNext: Purchase Receipt submit + Debit Note       │
│                                                                            │
│  9. Tính giá vốn & báo cáo                                               │
│     ├─ Phân bổ chi phí vận chuyển (Landed Cost)                          │
│     ├─ Tính giá vốn bình quân                                            │
│     └─ Báo cáo mua hàng kỳ                                              │
│                     │                                                     │
│                     ▼ ERPNext: Landed Cost Voucher + Reports             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 13.3 Nhập khẩu (Import) - Luồng đặc biệt

```
Luồng nhập khẩu hàng golf:
  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  Purchase Plan                                                   │
  │    └─ Lên KH theo mùa, MOQ, lịch hãng                          │
  │         │                                                        │
  │         ▼                                                        │
  │  Purchase Order                                                  │
  │    ├─ vendor_po_number: PO# từ hãng                             │
  │    ├─ ship_mode: Sea / Air                                      │
  │    ├─ Currency: USD / JPY                                        │
  │    └─ Exchange Rate: tỷ giá ngày đặt                            │
  │         │                                                        │
  │         ▼                                                        │
  │  Delivery Schedule (Custom)                                      │
  │    ├─ Confirm Date (NCC xác nhận)                               │
  │    ├─ Ship Date (ngày xuất)                                     │
  │    ├─ ETA (ngày dự kiến đến)                                    │
  │    ├─ Forwarder Info                                             │
  │    └─ Customs Declaration No                                     │
  │         │                                                        │
  │         ▼                                                        │
  │  Thông quan                                                      │
  │    ├─ Expected Clearance Date                                    │
  │    ├─ Actual Clearance Date                                      │
  │    └─ Thuế NK (3333)                                             │
  │         │                                                        │
  │         ▼                                                        │
  │  Purchase Receipt                                                │
  │    ├─ Kiểm đếm (1 ngày)                                        │
  │    ├─ Batch No (theo lô nhập)                                   │
  │    ├─ Serial No (từng sản phẩm)                                 │
  │    └─ So sánh giá PR vs PO                                      │
  │         │                                                        │
  │         ▼                                                        │
  │  Landed Cost Voucher                                             │
  │    ├─ Vận chuyển quốc tế (sea/air freight)                      │
  │    ├─ Phí thông quan                                             │
  │    ├─ Vận chuyển nội địa                                        │
  │    ├─ Bốc dỡ                                                    │
  │    └─ Bảo hiểm                                                   │
  │         │                                                        │
  │         ▼                                                        │
  │  Purchase Invoice                                                │
  │    ├─ Bill No: Số HĐ NCC nước ngoài                            │
  │    ├─ Currency: USD/JPY                                          │
  │    ├─ Exchange Rate: tỷ giá ngày HĐ                            │
  │    └─ VAT: theo quy định NK                                     │
  │         │                                                        │
  │         ▼                                                        │
  │  Payment Entry                                                   │
  │    ├─ T/T (Telegraphic Transfer)                                │
  │    ├─ L/C (Letter of Credit)                                    │
  │    └─ Exchange Rate: tỷ giá ngày thanh toán                     │
  │         │                                                        │
  │  ⚠️ Chênh lệch tỷ giá:                                        │
  │    Nợ/Có 635 (CP tài chính) nếu tỷ giá TT ≠ tỷ giá HĐ       │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

---

## 14. Phụ thuộc giữa các Module

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    PHỤ THUỘC MODULE - MUA HÀNG                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                          ┌─────────────────┐                                   │
│                          │ 03. Sản phẩm    │ ◀── Item master, variant,         │
│                          │     (Item)      │     batch/serial config            │
│                          └────────┬────────┘                                   │
│                                   │                                             │
│                                   ▼                                             │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐          │
│  │ 04. NCC         │────▶│ 05. MUA HÀNG   │────▶│ 07. Kho         │          │
│  │     (Supplier)  │     │    (BUYING)     │     │     (Stock)     │          │
│  │ Master data,    │     │                 │     │ Warehouse,      │          │
│  │ Payment Terms,  │     │ PO → PR → PI   │     │ Stock Ledger    │          │
│  │ Price List      │     │ → PE            │     │                 │          │
│  └─────────────────┘     └────────┬────────┘     └─────────────────┘          │
│                                   │                                             │
│                          ┌────────┴────────┐                                   │
│                          │                 │                                    │
│                          ▼                 ▼                                    │
│                 ┌─────────────────┐ ┌─────────────────┐                        │
│                 │ 24. KT Mua hàng│ │ 26. KT Công nợ  │                        │
│                 │ GL Entry,      │ │ AP Aging,        │                        │
│                 │ Trial Balance  │ │ Supplier Statement│                       │
│                 └────────┬───────┘ └────────┬─────────┘                        │
│                          │                  │                                   │
│                          ▼                  ▼                                   │
│                 ┌──────────────────────────────────────┐                        │
│                 │ 30. KT Tổng hợp                      │                        │
│                 │ Financial Reports, Closing            │                        │
│                 └──────────────────────────────────────┘                        │
│                                                                                 │
│  Module liên quan khác:                                                        │
│  ├─ 06. BC Phân tích: Báo cáo mua hàng                                       │
│  ├─ 09. Đơn hàng: SO → PO (liên kết bán-mua)                                │
│  ├─ 15. Trade-in: Nhập hàng cũ (1565)                                        │
│  └─ 22. KT Tiền: Payment Entry (cash/bank)                                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 15. Custom DocType bổ sung

### 15.1 Purchase Plan (Kế hoạch mua hàng) — NEW

```
Purchase Plan
├── plan_name
├── year: 2026
├── supplier
├── status: Draft | Submitted | Closed
│
├── Items (child table - Purchase Plan Item):
│   ├── item_code
│   ├── item_name
│   ├── item_group (Family/Category)
│   ├── current_stock (auto-fetch)
│   ├── jan_qty, feb_qty, ..., dec_qty (12 cột tháng)
│   ├── total_qty (auto-sum)
│   ├── estimated_rate
│   └── estimated_amount
│
├── Total: tổng giá trị KH
│
└── Actions:
    └── Get Items → Purchase Order (tạo PO từ KH tháng hiện tại)
```

### 15.2 Delivery Schedule (Kế hoạch giao hàng) — NEW

```
Delivery Schedule
├── schedule_name
├── supplier
├── purchase_order (link PO)
├── vendor_po_number
│
├── ship_mode: Sea | Air | Road
├── forwarder_name
├── forwarder_contact
│
├── Dates:
│   ├── confirm_date (NCC xác nhận)
│   ├── ship_date (ngày xuất hàng)
│   ├── eta_date (dự kiến đến)
│   ├── actual_arrival_date (thực tế đến)
│   ├── expected_clearance_date
│   └── actual_clearance_date
│
├── customs_declaration_no
├── status: Pending | In Transit | Arrived | Cleared | Received
│
├── Items (child table):
│   ├── item_code
│   ├── qty_ordered (trên PO)
│   ├── qty_shipping (đợt này)
│   ├── ean_code
│   └── upc_code
│
└── Attachments: packing list, bill of lading, customs docs
```

---

## 16. Quyền & Phân quyền

### 16.1 Ma trận quyền

```
┌──────────────────────┬────────┬────────┬────────┬────────┬────────┐
│ DocType              │Purchase│Purchase│Stock   │Accounts│Accounts│
│                      │User    │Manager │User    │User    │Manager │
├──────────────────────┼────────┼────────┼────────┼────────┼────────┤
│ Material Request     │ CRUD   │ CRUD+A │   R    │   R    │   R    │
│ Supplier Quotation   │ CRUD   │ CRUD+A │        │   R    │   R    │
│ Purchase Order       │ CRU    │ CRUD+A │   R    │   R    │   R    │
│ Purchase Receipt     │  CR    │  CR    │ CRUD   │  R+A   │ CRUD+A │
│ Purchase Invoice     │   R    │   R    │   R    │ CRUD   │ CRUD+A │
│ Payment Entry        │  CR    │  CR    │        │ CRU    │ CRUD+A │
│ Landed Cost Voucher  │   R    │  CR    │        │ CRUD   │ CRUD+A │
│ Purchase Plan (NEW)  │ CRUD   │ CRUD+A │   R    │   R    │   R    │
│ Delivery Schedule    │ CRUD   │ CRUD+A │   R    │   R    │   R    │
├──────────────────────┼────────┼────────┼────────┼────────┼────────┤
│ C=Create R=Read      │        │        │        │        │        │
│ U=Update D=Delete    │        │        │        │        │        │
│ A=Amend/Cancel       │        │        │        │        │        │
└──────────────────────┴────────┴────────┴────────┴────────┴────────┘
```

### 16.2 Approval Rules

| Hành động | Ai duyệt | Điều kiện |
|-----------|----------|-----------|
| PO > 50,000,000 VND | Purchase Manager | Grand Total > threshold |
| Purchase Receipt | Accounts User/Manager | Tất cả phiếu nhập |
| Return Order | Purchase Manager | Tất cả lệnh trả |
| Payment Entry | Accounts Manager | Tất cả thanh toán |
| Landed Cost > 10,000,000 | Accounts Manager | Amount > threshold |

---

## 17. Checklist triển khai

### Phase T3 (31/03/2026) — Core

- [ ] **Setup cơ bản**
  - [ ] Supplier master data (module 04)
  - [ ] Item master với batch/serial config (module 03)
  - [ ] Warehouse setup (module 07)
  - [ ] Price List NCC
  - [ ] Payment Terms templates
  - [ ] Tax template (VAT 10%)

- [ ] **Purchase Order**
  - [ ] Custom fields: vendor_po_number, ship_mode, supplier_status
  - [ ] Custom fields: customs_declaration_no, expected/actual_clearance_date
  - [ ] Naming series: PO-.YYYY.-.#####
  - [ ] Print format tiếng Việt

- [ ] **Purchase Receipt**
  - [ ] Workflow 3 bước (Draft → Chờ duyệt → Đã nhập kho)
  - [ ] Custom field: receipt_approval_status, inspector_name
  - [ ] Barcode scan integration
  - [ ] Client script: so sánh giá PR vs PO (cảnh báo chênh lệch)

- [ ] **Purchase Invoice**
  - [ ] Tax template VAT 10% (TK 1331)
  - [ ] Link PR ↔ PI
  - [ ] Naming series: PI-.YYYY.-.#####

- [ ] **Payment Entry**
  - [ ] Workflow 4 bước (Draft → Đề nghị TT → Approved → Paid)
  - [ ] Link PI ↔ PE

- [ ] **Landed Cost Voucher**
  - [ ] Config TK 1562 (CP thu mua)
  - [ ] Template chi phí thường gặp

- [ ] **Trả hàng (Debit Note)**
  - [ ] Workflow 2 bước cho Return Order
  - [ ] Test luồng trả hàng end-to-end

- [ ] **Báo cáo cơ bản**
  - [ ] Purchase Order Analysis
  - [ ] Accounts Payable
  - [ ] PO Items To Receive

### Phase T4+ — Advanced

- [ ] **Purchase Plan** (Custom DocType)
  - [ ] DocType definition + child table
  - [ ] 12 cột tháng
  - [ ] Action: Get Items → PO
  - [ ] Report: KH vs Thực tế

- [ ] **Delivery Schedule** (Custom DocType)
  - [ ] DocType definition + child table
  - [ ] Status tracking (Pending → In Transit → Cleared → Received)
  - [ ] Import từ Excel NCC

- [ ] **Báo cáo nâng cao**
  - [ ] Giá mua bình quân
  - [ ] NCC tốt nhất
  - [ ] So sánh KH mua vs đơn hàng
  - [ ] Chi phí mua hàng chi tiết

- [ ] **Bulk Image Import Tool**
  - [ ] Upload multiple images
  - [ ] Auto-match by naming convention

---

## Appendix A: ERPNext Settings liên quan

```python
# Buying Settings (Setup → Buying Settings)
{
    "supp_master_name": "Supplier Name",      # Đặt tên NCC theo
    "buying_price_list": "Standard Buying",    # Bảng giá mua mặc định
    "maintain_same_rate": 1,                   # Giữ giá giống PO→PR→PI
    "allow_multiple_items": 1,                 # Cho phép trùng item trên PO
    "po_required": "Yes",                      # Bắt buộc PO trước PI
    "pr_required": "Yes",                      # Bắt buộc PR trước PI
}

# Stock Settings (Setup → Stock Settings)
{
    "valuation_method": "FIFO",                # Hoặc "Moving Average"
    "auto_insert_price_list_rate_if_missing": 1,
    "allow_negative_stock": 0,                 # KHÔNG cho phép tồn âm
    "show_barcode_field": 1,                   # Hiện field barcode
}

# Accounts Settings
{
    "acc_frozen_upto": "",                     # Đóng sổ đến ngày
    "determine_address_tax_category_from": "Billing Address",
}
```

## Appendix B: API Endpoints

```
# Purchase Order
GET    /api/resource/Purchase Order?filters=[["status","=","To Receive and Bill"]]
POST   /api/resource/Purchase Order
GET    /api/resource/Purchase Order/{name}
PUT    /api/resource/Purchase Order/{name}

# Purchase Receipt
POST   /api/method/erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt
       Body: {"source_name": "PO-2026-00001"}

# Purchase Invoice
POST   /api/method/erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice
       Body: {"source_name": "PO-2026-00001"}

# Payment Entry
POST   /api/method/erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry
       Body: {"dt": "Purchase Invoice", "dn": "PI-2026-00001"}

# Landed Cost
POST   /api/resource/Landed Cost Voucher

# Reports
GET    /api/method/frappe.client.get_list?doctype=Purchase Order&fields=["name","supplier","grand_total","status"]
```

---

> **Last Updated:** 16/03/2026
> **Nguồn specs:** ERP_SPECIFICATION.md Section 3 | IMPORT_PROCESS_SPECIFICATION.md | COA_ANALYSIS.md
> **Module docs:** docs/modules/05-mua-hang/
