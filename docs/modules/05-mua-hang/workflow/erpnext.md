# Luồng Mua hàng ERPNext - Tham khảo kỹ thuật

> **Mục đích:** Tài liệu reference luồng mua hàng chuẩn ERPNext v16.
> Không chứa yêu cầu đặc thù khách hàng. Đối chiếu specs → xem `nhatminh.md`.
> **Satellites:** 04-NCC (Supplier), 24-KT Mua hàng (Accounting), 06-BC Phân tích (Reports)

---

## 1. Tổng quan

### 1.1 Sơ đồ luồng

```
  Material Request → Supplier Quotation → Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry
       (tùy chọn)        (tùy chọn)         (core)           (core)            (core)           (core)
                                                │
                                                ├── Landed Cost Voucher (chi phí mua)
                                                └── Purchase Return / Debit Note (trả hàng)
```

### 1.2 Vai trò

| Role | Quyền chính | DocType |
|------|------------|---------|
| Purchase User | Tạo MR, SQ, PO | Material Request, Supplier Quotation, Purchase Order |
| Purchase Manager | Duyệt PO, cancel | Purchase Order (approve/cancel) |
| Stock User | Nhận hàng, nhập kho | Purchase Receipt |
| Stock Manager | Duyệt nhập kho | Purchase Receipt (approve) |
| Accounts User | Ghi hóa đơn, thanh toán | Purchase Invoice, Payment Entry |
| Accounts Manager | Duyệt thanh toán | Payment Entry, Journal Entry |

### 1.3 Tác động từng DocType

| DocType | Kho (Stock Ledger) | Kế toán (GL Entry) | Submit? |
|---------|:------------------:|:-------------------:|:-------:|
| Material Request | — | — | Có |
| Supplier Quotation | — | — | Có |
| Purchase Order | — | — | Có |
| **Purchase Receipt** | **Có** | Có (Perpetual) | Có |
| **Purchase Invoice** | Tùy chọn | **Có** | Có |
| **Payment Entry** | — | **Có** | Có |
| Landed Cost Voucher | Điều chỉnh giá | **Có** | Có |

---

## 2. Luồng chuẩn & biến thể

### 2.1 Các luồng phổ biến

| # | Luồng | Khi nào dùng |
|---|-------|-------------|
| 1 | MR → SQ → PO → PR → PI → PE | Đầy đủ, nhiều NCC, so sánh giá |
| 2 | PO → PR → PI → PE | Trực tiếp, NCC quen, giá thỏa thuận |
| 3 | PO → PI (✓Update Stock) → PE | Nhận hàng kèm hóa đơn |
| 4 | PI (✓Update Stock) → PE | Mua lẻ, không cần PO |
| 5 | PO → PR → LCV → PI → PE | Nhập khẩu, cần phân bổ chi phí |
| 6 | PI Return (Debit Note) | Trả hàng NCC |

### 2.2 Sơ đồ quyết định

```
Bắt đầu → Cần so sánh giá? ──Có──→ Luồng 1 (MR→SQ→PO)
                              │
                             Không
                              │
                    Nhập khẩu? ──Có──→ Luồng 5 (PO→PR→LCV)
                              │
                             Không
                              │
                    Cần kiểm hàng riêng? ──Có──→ Luồng 2 (PO→PR→PI)
                                           │
                                          Không
                                           │
                                   Cần PO? ──Có──→ Luồng 3 (PO→PI+Stock)
                                              │
                                             Không → Luồng 4 (PI only)
```

---

## 3. Chi tiết DocType

### 3.1 Material Request

```
Material Request
├── Type: Purchase | Material Transfer | Material Issue
├── Required By Date
├── Items: Item Code, Qty, UOM, Warehouse
└── Status: Draft → Submitted → Ordered → Received
```

Tạo từ: Reorder Level (auto) | Manual
Tạo tiếp: Supplier Quotation | Purchase Order

### 3.2 Supplier Quotation

```
Supplier Quotation
├── Supplier
├── Valid Till
├── Items: Item Code, Qty, Rate, Lead Time Days
├── Taxes and Charges
└── Grand Total
```

Tool: **Supplier Quotation Comparison** — so sánh giá giữa NCC

### 3.3 Purchase Order

```
Purchase Order
├── Naming Series: PO-.YYYY.-.#####
├── Supplier, Company, Currency
├── Items: Item Code, Qty, Rate, Warehouse, Expected Delivery Date
│   ├── Received Qty (auto từ PR)
│   ├── Billed Qty (auto từ PI)
│   └── Returned Qty (auto từ Return)
├── Taxes and Charges
├── Payment Terms (child table)
├── Additional Discount
├── Terms and Conditions
└── Status: Draft → To Receive and Bill → To Receive → To Bill → Completed
```

Tạo từ: Material Request | Supplier Quotation | Manual
Tạo tiếp: Purchase Receipt | Purchase Invoice | Payment Entry (advance)

### 3.4 Purchase Receipt

```
Purchase Receipt
├── Naming Series: PR-.YYYY.-.#####
├── Supplier, Posting Date/Time
├── Supplier Delivery Note
├── Items: Item Code, Qty, Rejected Qty, Rate
│   ├── Warehouse / Rejected Warehouse
│   ├── Batch No (nếu has_batch_no)
│   ├── Serial No (nếu has_serial_no, 1 dòng/serial)
│   ├── Quality Inspection
│   └── Purchase Order (link)
├── Taxes and Charges
└── Status: Draft → To Bill → Completed
```

**Khi Submit:** Stock Ledger Entry + GL Entry (Perpetual Inventory)

### 3.5 Purchase Invoice

```
Purchase Invoice
├── Naming Series: PI-.YYYY.-.#####
├── Supplier, Bill No, Bill Date, Due Date
├── Is Return: ☐ (tick = Debit Note)
├── Update Stock: ☐ (tick = nhập kho luôn)
├── Items: Item Code, Qty, Rate, Expense Account
│   ├── Purchase Receipt (link)
│   ├── Purchase Order (link)
│   └── Deferred Expense Account
├── Taxes and Charges
├── Payment Schedule
├── Advances (auto-fetch PE ứng trước)
└── Status: Draft → Unpaid → Partially Paid → Paid → Overdue
```

**Khi Submit:** GL Entry (công nợ + thuế). Nếu Update Stock ☑ → thêm Stock Ledger.

### 3.6 Payment Entry

```
Payment Entry
├── Payment Type: Pay
├── Party: Supplier
├── Mode of Payment: Cash | Wire Transfer | Check
├── Paid From: 1111/1121 (Cash/Bank)
├── Paid To: 331 (Payable)
├── References: Purchase Invoice + Allocated Amount
├── Deductions (chiết khấu, phí NH)
└── Status: Draft → Submitted
```

**Khi Submit:** GL Entry (giảm tiền, giảm công nợ) → PI outstanding = 0 → PI status = Paid

---

## 4. Trạng thái tự động

### Purchase Order

```
Draft → Submit → To Receive and Bill
                    ├── To Receive (có PI, chưa PR)
                    ├── To Bill (có PR, chưa PI)
                    └── Completed (có cả PR + PI)
  Trạng thái khác: On Hold | Closed | Cancelled
```

### Purchase Receipt

```
Draft → Submitted → To Bill (chờ PI) → Completed (có PI)
                  → Return (trả hàng)
```

### Purchase Invoice

```
Draft → Submitted → Unpaid → Partially Paid → Paid
                  → Overdue (quá hạn)
                  → Debit Note Issued
```

---

## 5. GL Entry - Bút toán kế toán

### 5.1 Tổng hợp

| Bước | Nợ | Có |
|------|----|----|
| **Purchase Receipt** | 1561 (Hàng hóa) | 331 (Phải trả NCC) |
| **Purchase Invoice** | 1561 + 1331 (VAT) | 331 |
| **Landed Cost** | 1561 (tăng giá vốn) | 1562/331 (CP thu mua) |
| **Payment Entry** | 331 | 1111/1121 (Cash/Bank) |
| **Debit Note** | 331 (giảm CN) | 1561 (giảm kho) |

### 5.2 Ví dụ end-to-end

```
Mua 10 SP @ 5,000,000, VAT 10%, vận chuyển 2,000,000

1. PR:  Nợ 1561  50,000,000  / Có 331   50,000,000  → Stock +10
2. LCV: Nợ 1561   2,000,000  / Có 1562   2,000,000  → Giá vốn 5,200,000/cái
3. PI:  Nợ 1331   5,000,000  / Có 331     5,000,000  → Tổng CN = 55,000,000
4. PE:  Nợ 331   55,000,000  / Có 1121  55,000,000  → CN = 0, Paid

Kết quả: Kho +10 @ 5,200,000 | CN = 0 | VAT 5tr | Bank -55tr
```

### 5.3 Tài khoản liên quan

| TK | Tên | Account Type |
|----|-----|:------------:|
| 1111 | Tiền mặt | Cash |
| 1121 | Tiền gửi NH | Bank |
| 1331 | VAT đầu vào | Tax |
| 1561 | Giá mua hàng hóa | Stock |
| 1562 | CP thu mua | Expenses Included In Asset Valuation |
| 331 | Phải trả NCC | Payable |
| 3333 | Thuế NK | Tax |

---

## 6. Batch, Serial, Barcode

### Batch

```
Item → Has Batch No: ☑ → Create New Batch: ☑
PR: Item + Qty + Batch No (auto hoặc chọn)
Tra cứu: Stock Balance → filter Batch
```

### Serial No

```
Item → Has Serial No: ☑ → Serial No Series: SN-.YYYY.-.######
PR: Item + Qty=3 + Serial No: SN-001\nSN-002\nSN-003
Mỗi Serial = 1 DocType (truy xuất nguồn gốc)
```

### Barcode

```
Item → Barcodes: EAN/UPC
PR: nút "Scan Barcode" → quét → auto add item row → quét lần nữa → qty +1
```

---

## 7. Trả hàng (Debit Note)

```
Cách 1: PI → Menu → Make Return → PI mới (Is Return ☑, qty ÂM)
Cách 2: PR → Menu → Make Return → PR mới (qty ÂM) → Debit Note
Cách 3: Manual PI → tick Is Return → Against PI → qty ÂM

GL: Nợ 331 (giảm CN) / Có 1561 (giảm kho)
Stock: Actual Qty giảm
```

---

## 8. Landed Cost Voucher

```
Landed Cost Voucher
├── Purchase Receipts: chọn PR cần phân bổ
├── Taxes and Charges: Vận chuyển, Bốc dỡ, Thuế NK...
├── Distribute By: Qty | Amount | Manual
└── Submit → Điều chỉnh Valuation Rate + GL

Ví dụ: PR 10 items @ 5M + LCV 2M (by Qty) → giá vốn mới 5.2M/cái
```

---

## 9. Thanh toán NCC

| Hình thức | Luồng | GL |
|-----------|-------|----|
| Thanh toán ngay | PI → PE | Nợ 331, Có 1111 |
| Chuyển khoản | PI → PE (theo term) | Nợ 331, Có 1121 |
| Trả nhiều đợt | PI → PE1 → PE2 | Mỗi PE ghi 1 phần |
| Ứng trước | PE → PO → PI (trừ advance) | PE trước, PI auto trừ |
| Bù trừ | Journal Entry | Nợ 331, Có 131 |

### Payment Terms Template

```
VD: "30-70-60days"
  Row 1: 30% | ngày hóa đơn
  Row 2: 70% | 60 ngày sau
```

---

## 10. Pricing Rule (Ưu đãi NCC)

```
Pricing Rule (Buying)
├── Apply On: Item Code | Item Group | Brand
├── Supplier / Supplier Group
├── Valid From / Valid Upto
├── Discount: % | Amount | Fixed Rate
├── Min/Max Qty, Min/Max Amount
├── Free Item: Item + Qty + Rate=0
└── Priority
```

---

## 11. Supplier Master (Module 04)

```
Supplier
├── Supplier Name, Supplier Group (tree)
├── Tax ID, Default Currency
├── Payment Terms Template
├── Contact (child): name, email, phone
├── Address (child): billing, shipping
├── Supplier Scorecard (đánh giá)
└── Dashboard: PO, PR, PI linked

Price List (Buying)
├── Per Supplier/Group
├── Item Price: Item + Rate + valid_from/upto
└── Auto-fetch vào PO
```

---

## 12. Báo cáo có sẵn

| Báo cáo | Mô tả |
|---------|-------|
| Purchase Analytics | Phân tích theo NCC/Item/nhóm, theo kỳ |
| Purchase Order Analysis | PO theo trạng thái, thời gian |
| Purchase Order Items To Receive | PO chưa nhận hàng |
| Purchase Order Items To Receive and Bill | PO chưa nhận + chưa PI |
| Purchase Invoice Trends | Xu hướng PI |
| Accounts Payable | Công nợ NCC chi tiết |
| Accounts Payable Summary | Tổng hợp theo NCC |
| Supplier Ledger Summary | Sổ cái NCC |
| Item-wise Purchase Register | Sổ mua theo item |
| Purchase Register | Sổ mua tổng hợp |
| Stock Balance | Tồn kho theo warehouse/item |
| Stock Ageing | Tuổi tồn kho |

---

## 13. Cấu hình

### Buying Settings

```
supp_master_name: "Supplier Name"
buying_price_list: "Standard Buying"
maintain_same_rate: 1          # Giữ giá PO→PR→PI
po_required: "Yes"             # Bắt buộc PO trước PI
pr_required: "Yes"             # Bắt buộc PR trước PI
```

### Stock Settings

```
valuation_method: "FIFO"       # Hoặc "Moving Average"
allow_negative_stock: 0
show_barcode_field: 1
```

---

## 14. API Endpoints

```
# CRUD
GET/POST   /api/resource/Purchase Order
GET/PUT    /api/resource/Purchase Order/{name}

# Actions
POST /api/method/erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt
POST /api/method/erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice
POST /api/method/erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice
POST /api/method/erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry

# Filters
GET /api/resource/Purchase Order?filters=[["status","=","To Receive and Bill"]]
GET /api/resource/Purchase Invoice?filters=[["outstanding_amount",">",0]]
```

---

> **Last Updated:** 17/03/2026
> **ERPNext Version:** v16
