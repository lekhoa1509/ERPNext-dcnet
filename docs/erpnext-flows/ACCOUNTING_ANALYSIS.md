# ACCOUNTING MODULE ANALYSIS

> **Module**: `webkul/accounts`
> **Source**: `/Users/vovanduc/Code/dcnet/flow_crm/plugins/webkul/accounts`
> **Status**: ✅ Có sẵn trong Aureus ERP
> **Version**: Verified from source code

---

## 📋 Tổng quan

Module Accounting là **nền tảng kế toán** của Aureus ERP, quản lý:
- Hóa đơn bán/mua (Invoice/Bill)
- Thanh toán (Payment)
- Đối soát ngân hàng (Bank Reconciliation)
- Công nợ (Accounts Receivable/Payable)
- Thuế (Tax Management)
- Báo cáo tài chính

---

## 1️⃣ 18 ACCOUNT TYPES - Hệ thống Tài khoản

> **Source**: `src/Enums/AccountType.php`

### 📊 6 loại ASSETS (Tài sản)

| Account Type | Code | Mô tả | Ví dụ thực tế |
|-------------|------|-------|---------------|
| `ASSET_RECEIVABLE` | `asset_receivable` | Công nợ phải thu | Khách mua chưa trả tiền |
| `ASSET_CASH` | `asset_cash` | Tiền mặt | Tiền trong két, két nhỏ |
| `ASSET_CURRENT` | `asset_current` | Tài sản ngắn hạn | Hàng tồn kho |
| `ASSET_NON_CURRENT` | `asset_non_current` | Tài sản dài hạn | Đầu tư tài chính |
| `ASSET_PREPAYMENTS` | `asset_prepayments` | Trả trước | Trả trước tiền thuê |
| `ASSET_FIXED` | `asset_fixed` | Tài sản cố định | Nhà, xe, máy móc |

**Workflow thực tế:**
```
Bán hàng 10tr (chưa thu):
Nợ: ASSET_RECEIVABLE   +10,000,000  (Khách nợ tăng)
Có: INCOME              -10,000,000  (Doanh thu tăng)

Thu tiền mặt:
Nợ: ASSET_CASH          +10,000,000  (Tiền mặt tăng)
Có: ASSET_RECEIVABLE    -10,000,000  (Khách nợ giảm)
```

### 💳 4 loại LIABILITIES (Nợ phải trả)

| Account Type | Code | Mô tả | Ví dụ thực tế |
|-------------|------|-------|---------------|
| `LIABILITY_PAYABLE` | `liability_payable` | Công nợ phải trả | Nợ nhà cung cấp |
| `LIABILITY_CREDIT_CARD` | `liability_credit_card` | Nợ thẻ tín dụng | Quẹt thẻ chưa trả |
| `LIABILITY_CURRENT` | `liability_current` | Nợ ngắn hạn | Vay ngân hàng < 1 năm |
| `LIABILITY_NON_CURRENT` | `liability_non_current` | Nợ dài hạn | Vay ngân hàng > 1 năm |

**Workflow thực tế:**
```
Mua hàng 50tr (chưa trả NCC):
Nợ: ASSET_CURRENT       +50,000,000  (Hàng tồn kho tăng)
Có: LIABILITY_PAYABLE   -50,000,000  (Nợ NCC tăng)

Trả tiền NCC:
Nợ: LIABILITY_PAYABLE   +50,000,000  (Nợ NCC giảm)
Có: ASSET_CASH          -50,000,000  (Tiền mặt giảm)
```

### 💰 2 loại EQUITY (Vốn chủ sở hữu)

| Account Type | Code | Mô tả |
|-------------|------|-------|
| `EQUITY` | `equity` | Vốn góp |
| `EQUITY_UNAFFECTED` | `equity_unaffected` | Lợi nhuận giữ lại |

### 📈 2 loại INCOME (Thu nhập)

| Account Type | Code | Mô tả |
|-------------|------|-------|
| `INCOME` | `income` | Doanh thu bán hàng |
| `INCOME_OTHER` | `income_other` | Thu nhập khác (lãi tiền gửi, lãi tỷ giá) |

### 📉 3 loại EXPENSE (Chi phí)

| Account Type | Code | Mô tả |
|-------------|------|-------|
| `EXPENSE` | `expense` | Chi phí hoạt động (lương, điện, nước) |
| `EXPENSE_DEPRECIATION` | `expense_depreciation` | Khấu hao tài sản cố định |
| `EXPENSE_DIRECT_COST` | `expense_direct_cost` | Giá vốn hàng bán |

### 📋 1 loại OFF_BALANCE (Ngoài bảng cân đối)

| Account Type | Code | Mô tả |
|-------------|------|-------|
| `OFF_BALANCE` | `off_balance` | Tài khoản tạm (suspense account) |

---

## 2️⃣ WORKFLOW CƠ BẢN

> **Source**: `src/Enums/MoveState.php`, `src/Enums/PaymentState.php`

### 📄 Invoice/Bill Workflow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  DRAFT   │────►│ POSTED   │────►│ NOT_PAID │────►│  PAID    │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
    │                 │                 │                 │
    ▼                 ▼                 ▼                 ▼
• Nhập thông tin  • Tính thuế     • Theo dõi       • Đối soát
• Chỉnh sửa tự do • Tạo bút toán  • Ngày hết hạn   • Cập nhật sổ
                  • Sinh số HĐ    • Gửi email
                  • Khóa sửa
```

**States từ source code:**
```php
// MoveState.php
DRAFT  = 'draft'   // Nháp - Chưa hạch toán
POSTED = 'posted'  // Đã hạch toán
CANCEL = 'cancel'  // Hủy

// PaymentState.php
NOT_PAID         = 'not_paid'         // Chưa thanh toán
IN_PAYMENT       = 'in_payment'       // Đang thanh toán
PAID             = 'paid'             // Đã thanh toán đủ
PARTIAL          = 'partial'          // Thanh toán một phần
REVERSED         = 'reversed'         // Đã hoàn lại
BLOCKED          = 'blocked'          // Bị chặn
INVOICING_LEGACY = 'invoicing_legacy' // Di sản
```

### 💰 Payment Workflow

> **Source**: `src/Enums/PaymentType.php`, `src/Models/Payment.php`

```
┌────────────────────┐              ┌────────────────────┐
│  INBOUND Payment   │              │ OUTBOUND Payment   │
│  (Thu tiền)        │              │ (Chi tiền)         │
├────────────────────┤              ├────────────────────┤
│ • Từ khách hàng    │              │ • Trả NCC          │
│ • Thu tiền bán     │              │ • Chi phí          │
│ • Thu công nợ      │              │ • Trả nợ           │
└──────────┬─────────┘              └──────────┬─────────┘
           │                                   │
           └───────────────┬───────────────────┘
                           ▼
                ┌─────────────────────┐
                │  Payment Methods    │
                ├─────────────────────┤
                │ • Cash (Tiền mặt)   │
                │ • Bank (CK)         │
                │ • Card (Thẻ)        │
                │ • QR Code           │
                └──────────┬──────────┘
                           ▼
                ┌─────────────────────┐
                │  Auto Reconcile     │
                │  • Match invoice    │
                │  • Update status    │
                │  • Calculate residual│
                └─────────────────────┘
```

**Payment fields từ source code:**
```php
// Payment.php model
'amount'                          // Số tiền thanh toán
'amount_company_currency_signed'  // Số tiền quy đổi
'payment_type'                    // inbound/outbound
'partner_type'                    // customer/supplier
'is_reconciled'                   // Đã đối soát?
'is_matched'                      // Đã match?
```

---

## 3️⃣ TAX MANAGEMENT - Quản lý Thuế

> **Source**: `src/Models/Tax.php`, `src/Models/TaxGroup.php`, `src/Models/FiscalPosition.php`

### 🧮 Tax Configuration

```php
// Tax.php
Tax: "VAT 10%"
├─ amount: 10                    // Tỷ lệ %
├─ scope: SERVICE/CONSU          // Loại áp dụng
├─ type_tax_use: SALE/PURCHASE   // Bán/Mua
├─ price_include: true/false     // Giá đã gồm thuế?
└─ tax_exigibility: based_on_invoice/based_on_payment
```

### 📊 Tax Group (Nhóm thuế)

```
TaxGroup: "VAT + Environmental Tax"
├─ Tax 1: VAT 10%
├─ Tax 2: Environmental Tax 2%
└─ Total: 12%

Ví dụ: Hóa đơn 100tr
- Base: 100,000,000
- VAT (10%): 10,000,000
- Env Tax (2%): 2,000,000
- Total: 112,000,000
```

### 🌍 Fiscal Position (Vị trí tài chính)

**Ánh xạ thuế theo địa chỉ:**
```
FiscalPosition: "Domestic"
└─ Tax mapping:
   Thuế mặc định (VAT 10%) → VAT 10%

FiscalPosition: "Export"
└─ Tax mapping:
   Thuế mặc định (VAT 10%) → VAT 0%

FiscalPosition: "Hanoi"
└─ Tax mapping:
   + VAT 10%
   + License tax (Thuế môn bài HN)
```

### 💡 Tax Partition (Phân bổ thuế)

> **Source**: `src/Models/TaxPartition.php`

```php
TaxPartition for Invoice
├─ Repartition type: BASE       // Phần gốc
│  └─ Account: None
│
└─ Repartition type: TAX        // Phần thuế
   └─ Account: TAX_PAYABLE      // Tài khoản thuế GTGT phải nộp

Document types:
- INVOICE: Hóa đơn bán
- REFUND: Hoàn trả
```

---

## 4️⃣ PAYMENT TERMS - Điều khoản Thanh toán

> **Source**: `src/Models/PaymentTerm.php`, `src/Enums/DelayType.php`

### 📅 Payment Term Types

| Term | Mô tả | Ví dụ |
|------|-------|-------|
| **Net 30** | Thanh toán sau 30 ngày | Invoice 01/01 → Due 31/01 |
| **2/10 Net 30** | Giảm 2% nếu trả trong 10 ngày | 100tr: Trả trong 10 ngày = 98tr, sau 10 ngày = 100tr |
| **End of Month** | Cuối tháng hiện tại | Invoice 15/01 → Due 31/01 |
| **End of Following Month** | Cuối tháng sau | Invoice 15/01 → Due 28/02 |

### 🧾 Delay Types

```php
// DelayType.php
DAYS_AFTER          // Số ngày sau ngày hóa đơn
DAYS_NEXT_MONTH     // Ngày X tháng sau
DAY_OF_MONTH        // Ngày X trong tháng
LAST_DAY_OF_MONTH   // Ngày cuối tháng
```

**Ví dụ cấu hình:**
```php
PaymentTerm: "2/10 Net 30"
├─ name: "2/10 Net 30"
├─ early_discount: true
├─ discount_percentage: 2
├─ discount_days: 10
└─ PaymentDueTerm:
   ├─ Due term 1: 2% if paid within 10 days
   └─ Due term 2: Full amount after 30 days
```

---

## 5️⃣ BANK RECONCILIATION - Đối soát Ngân hàng

> **Source**: `src/Models/BankStatement.php`, `src/Models/Reconcile.php`

### 🏦 Bank Statement Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Import CSV     │────►│  Auto Matching  │────►│  Review & Adjust│
│  (Sao kê NH)    │     │  (Quy tắc ĐS)   │     │  (Kiểm tra)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
  • File Excel          • By amount            • So sánh
  • Nhập thủ công       • By date              • Xác nhận
  • Số dư đầu/cuối      • By reference         • Tạo bút toán
                        • By partner           • Đánh dấu matched
```

### 🔍 Reconciliation Rules

```php
// Reconcile.php model
Reconcile rules:
├─ match_amount: true              // Khớp theo số tiền
├─ match_date_tolerance: ±3 days   // Sai số ngày
├─ match_label: "INV"              // Khớp theo mô tả
├─ match_partner: true             // Khớp theo khách/NCC
└─ payment_tolerance: 5%           // Sai số cho phép
```

**Matching Process:**
```
Bank Statement Line: +11,000,000 VNĐ (15/01/2025) "INV001"
                              ↓
Auto-match tìm trong hệ thống:
  - Invoice INV001: 11,000,000 VNĐ (14/01/2025) ✓
  - Amount match: 11tr = 11tr ✓
  - Date match: 15/01 vs 14/01 (±3 days) ✓
  - Reference match: "INV001" ✓
                              ↓
Create PartialReconcile/FullReconcile
Update payment_state: NOT_PAID → PAID
```

### 📋 BankStatement Fields

```php
// BankStatement.php
'name'              // Tên sao kê
'reference'         // Số tham chiếu
'date'              // Ngày sao kê
'balance_start'     // Số dư đầu
'balance_end'       // Số dư cuối
'balance_end_real'  // Số dư thực tế
'is_completed'      // Đã hoàn tất?
```

---

## 6️⃣ MULTI-CURRENCY - Đa Tiền Tệ

> **Source**: `src/Models/Move.php` (currency_id field)

### 💱 Currency Workflow

```
Invoice USD:
┌─────────────────────────────────────┐
│ Amount: $1,000                      │
│ Currency: USD                       │
│ Rate: 24,000 VNĐ/$                  │
│ Amount in VNĐ: 24,000,000           │
└─────────────────────────────────────┘
                ↓
Accounting entries (VNĐ):
Nợ: ASSET_RECEIVABLE    +24,000,000
Có: INCOME              -24,000,000
                ↓
Payment received (rate changed):
┌─────────────────────────────────────┐
│ Received: $1,000                    │
│ New rate: 24,100 VNĐ/$              │
│ Actual VNĐ: 24,100,000              │
│ Exchange gain: +100,000 VNĐ         │
└─────────────────────────────────────┘
                ↓
Accounting entries:
Nợ: ASSET_CASH              +24,100,000
Có: ASSET_RECEIVABLE        -24,000,000
Có: INCOME_OTHER (Gain)        -100,000
```

### 📊 Fields from source

```php
// Move.php
'currency_id'                        // Tiền tệ giao dịch
'invoice_currency_rate'              // Tỷ giá
'amount_total'                       // Tổng tiền (currency)
'amount_total_signed'                // Tổng tiền (VNĐ)
'amount_total_in_currency_signed'    // Tổng tiền (có dấu)
```

---

## 7️⃣ CREDIT NOTE / REFUND - Hoàn Trả

> **Source**: `src/Models/MoveReversal.php`, `src/Filament/Resources/CreditNoteResource.php`

### 🔄 Credit Note Workflow

```
Original Invoice: 11,000,000 VNĐ [PAID]
                ↓
Customer returns goods
                ↓
Create Credit Note: -11,000,000 VNĐ
                ↓
MoveReversal (Reverse entries):
  Nợ: INCOME              +10,000,000
  Nợ: LIABILITY (VAT)      +1,000,000
  Có: ASSET_RECEIVABLE    -11,000,000
                ↓
Refund to customer: 11,000,000 VNĐ
  Nợ: ASSET_RECEIVABLE    +11,000,000
  Có: ASSET_CASH          -11,000,000
```

### 📝 MoveReversal Fields

```php
// MoveReversal.php
'reason'           // Lý do hoàn trả
'date'             // Ngày hoàn trả
'move_ids'         // ID hóa đơn gốc
'refund_move_ids'  // ID hóa đơn hoàn trả
```

---

## 8️⃣ MODELS & RELATIONSHIPS

### 📦 33 Models Chính

| Model | Mô tả | Relationships |
|-------|-------|---------------|
| **Account** | Tài khoản kế toán | 1:N → MoveLine |
| **Journal** | Sổ nhật ký | 1:N → Move, Payment |
| **Move** | Bút toán/Hóa đơn | 1:N → MoveLine, Payment |
| **MoveLine** | Chi tiết dòng | N:1 → Move, Account |
| **Payment** | Thanh toán | N:1 → Move, Journal |
| **PaymentMethod** | Phương thức TT | 1:N → PaymentMethodLine |
| **PaymentTerm** | Điều khoản TT | 1:N → PaymentDueTerm |
| **Tax** | Thuế | 1:N → TaxPartition |
| **TaxGroup** | Nhóm thuế | 1:N → Tax |
| **FiscalPosition** | Vị trí tài chính | 1:N → FiscalPositionTax |
| **BankStatement** | Sao kê NH | 1:N → BankStatementLine |
| **Reconcile** | Quy tắc đối soát | - |
| **PartialReconcile** | Đối soát 1 phần | N:1 → FullReconcile |
| **FullReconcile** | Đối soát đủ | 1:N → PartialReconcile |
| **MoveReversal** | Hoàn lại | N:N → Move |

---

## 9️⃣ FILAMENT RESOURCES

### 🖥️ UI Resources (15 resources)

| Resource | Route | Chức năng |
|----------|-------|-----------|
| **AccountResource** | `/accounts` | CRUD tài khoản |
| **JournalResource** | `/journals` | CRUD sổ nhật ký |
| **InvoiceResource** | `/invoices` | Hóa đơn bán |
| **BillResource** | `/bills` | Hóa đơn mua |
| **PaymentsResource** | `/payments` | Thanh toán |
| **CreditNoteResource** | `/credit-notes` | Ghi có |
| **RefundResource** | `/refunds` | Hoàn trả |
| **TaxResource** | `/taxes` | Quản lý thuế |
| **TaxGroupResource** | `/tax-groups` | Nhóm thuế |
| **PaymentTermResource** | `/payment-terms` | Điều khoản TT |
| **FiscalPositionResource** | `/fiscal-positions` | Vị trí tài chính |
| **CashRoundingResource** | `/cash-roundings` | Làm tròn tiền |
| **BankAccountResource** | `/bank-accounts` | TK ngân hàng |
| **IncoTermResource** | `/incoterms` | INCOTERMS |
| **AccountTagResource** | `/account-tags` | Nhãn tài khoản |

---

## 🔟 TÍCH HỢP VỚI CÁC MODULE KHÁC

```
webkul/accounts
    ├─► webkul/partners (Customer, Supplier, BankAccount)
    ├─► webkul/products (Product, Tax mapping)
    ├─► webkul/inventories (Stock valuation)
    ├─► webkul/sales (Sales Order → Invoice)
    ├─► webkul/purchases (Purchase Order → Bill)
    ├─► webkul/payments (PaymentToken, PaymentTransaction)
    ├─► webkul/chatter (Comments, Activity log)
    └─► webkul/support (Company, Currency, UTM tracking)
```

---

## 📌 TÓM TẮT TÍNH NĂNG CÓ SẴN

### ✅ Core Accounting (100% ready)
- [x] 18 loại tài khoản (Chart of Accounts)
- [x] Workflow: DRAFT → POSTED → PAID
- [x] Automatic journal entries
- [x] Double-entry bookkeeping (Nợ = Có)

### ✅ Invoice & Payment (100% ready)
- [x] Invoice/Bill management
- [x] Payment types: Inbound/Outbound
- [x] Payment methods: Cash/Bank/Card
- [x] Auto reconciliation
- [x] Residual tracking (amount_residual)
- [x] Due date tracking (invoice_date_due)

### ✅ Tax Management (100% ready)
- [x] Tax configuration (%, fixed amount)
- [x] Tax groups (multiple taxes)
- [x] Fiscal positions (tax mapping by location)
- [x] Tax partitions (distribution rules)
- [x] Price include/exclude tax

### ✅ Bank & Reconciliation (100% ready)
- [x] Bank statement import
- [x] Auto-matching rules (amount, date, reference)
- [x] Partial/Full reconciliation
- [x] Manual adjustment

### ✅ Advanced Features (100% ready)
- [x] Multi-currency support
- [x] Payment terms (Net 30, early discount)
- [x] Credit Note/Refund
- [x] Move reversal
- [x] Cash rounding
- [x] INCOTERMS
- [x] Activity tracking (Chatter)
- [x] Email invoices

---

## ⚠️ PENDING - Cần Clarify với Khách hàng

### 🔴 Business Rules
- [ ] **Công nợ đơn Sỉ**: Cho phép nợ? Hạn mức? Điều khoản?
- [ ] **Hạn mức công nợ**: Theo khách hàng? Theo nhóm?
- [ ] **Báo cáo công nợ**: Theo chi nhánh? Theo nhân viên?
- [ ] **Chiết khấu thanh toán**: Áp dụng như thế nào?

### 🟡 Not Available (Cần custom)
- [ ] Automated reminder (Nhắc nợ tự động)
- [ ] Overdue tracking dashboard (Báo cáo quá hạn)
- [ ] Payment planning tool (Kế hoạch thanh toán)
- [ ] Financial reports (Báo cáo: Công nợ, Cash flow, P&L)

---

## 📚 Source Code References

```
/plugins/webkul/accounts/
├── src/
│   ├── Models/              (33 models)
│   ├── Enums/               (25 enums)
│   ├── Filament/Resources/  (15 resources)
│   ├── Mail/                (Email templates)
│   ├── AccountManager.php   (Service class)
│   └── TaxManager.php       (Service class)
├── database/migrations/     (40+ migrations)
└── resources/views/         (Blade templates)
```

**Key Files:**
- Models: `Move.php`, `Payment.php`, `Tax.php`, `BankStatement.php`
- Enums: `AccountType.php`, `MoveState.php`, `PaymentState.php`
- Resources: `InvoiceResource.php`, `BillResource.php`, `PaymentsResource.php`

---

**Last updated**: 2025-12-29
**Verified by**: Claude Code (Source code analysis)
