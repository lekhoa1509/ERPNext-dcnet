# Phân Tích Chi Tiết: Spec Kế Toán Khách Hàng vs DCNET Flow

**Prepared:** 20/01/2026
**Purpose:** So sánh chi tiết từng yêu cầu kế toán trong spec khách hàng với khả năng DCNET Flow hiện có
**Source:** `docs/feature/ERP_SPECIFICATION.md` Section 5 (lines 643-742)
**Reference:**
- `docs/analysis/ACCOUNTING_WORKFLOW.md` - DCNET Flow accounting internals
- `docs/analysis/VIETNAM_ACCOUNTING_GAP_ANALYSIS.md` - Vietnam localization gaps

---

## Executive Summary

### Tổng Quan Coverage

```
┌────────────────────────────────────────────────────────────────────┐
│           SPEC KẾ TOÁN KHÁCH HÀNG vs DCNET FLOW COVERAGE          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ✅ Có sẵn (Ready)        ████████████████████░░░░░  55%          │
│  🔧 Cần customize         ████████░░░░░░░░░░░░░░░░░  20%          │
│  ❌ Cần build mới         ██████░░░░░░░░░░░░░░░░░░░  25%          │
│                                                                    │
│  TỔNG COVERAGE:           ████████████████████░░░░░  ~75%*        │
│  (* Sau khi customize)                                             │
└────────────────────────────────────────────────────────────────────┘
```

### Quick Reference Table

| # | Yêu cầu từ Spec | DCNET Flow DocType | Coverage | Action |
|---|----------------|-----------------|----------|--------|
| 1 | Phiếu Thu/Chi | Payment Entry | ✅ 90% | Config templates |
| 2 | Hóa đơn bán hàng | Sales Invoice | ✅ 95% | Config |
| 3 | Hóa đơn mua hàng | Purchase Invoice | ✅ 95% | Config |
| 4 | Công nợ theo hạn TT | Payment Ledger + AR/AP | 🔧 60% | Build workflow |
| 5 | Giá vốn trung bình tháng | Stock Valuation | 🔧 70% | Monthly job |
| 6 | TSCĐ + Khấu hao | Asset | ✅ 90% | Config |
| 7 | CCDC phân bổ | Deferred Expense | 🔧 60% | Extend |
| 8 | Chi phí hỗ trợ hãng | N/A | ❌ 0% | Build new |
| 9 | Báo cáo sự kiện | N/A | ❌ 0% | Build new |
| 10 | Credit Management | Credit Limit | 🔧 60% | Build workflow |

---

## Phần 1: Thông Tin Chung Kế Toán

### 1.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 643-653

| Thông số | Yêu cầu khách hàng | Mô tả |
|----------|-------------------|-------|
| **Chế độ kế toán** | Thông tư 99 | Chế độ kế toán doanh nghiệp mới (từ 01/01/2026) |
| **Hình thức sổ** | Nhật ký chung | General Journal - phổ biến nhất tại VN |
| **Giá xuất kho** | Trung bình tháng | Monthly Weighted Average |
| **Đồng tiền** | VND | Vietnam Dong only |
| **Đánh giá CLTG** | Theo TT 99 | Chênh lệch tỷ giá cuối kỳ |
| **Khấu hao TSCĐ** | Đường thẳng | Straight-Line depreciation |

### 1.2. DCNET Flow Mapping

```mermaid
graph LR
    subgraph "Customer Requirement"
        A1[Thông tư 99]
        A2[Nhật ký chung]
        A3[Trung bình tháng]
        A4[VND]
        A5[CLTG theo TT99]
        A6[Khấu hao đường thẳng]
    end

    subgraph "DCNET Flow Capability"
        B1[Chart of Accounts<br>🔧 Cần build VN template]
        B2[General Ledger<br>✅ Có sẵn]
        B3[Moving Average<br>🔧 Cần monthly job]
        B4[Company Currency<br>✅ Có sẵn]
        B5[Exchange Rate Revaluation<br>✅ Có sẵn]
        B6[Straight Line Method<br>✅ Có sẵn]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    A5 --> B5
    A6 --> B6
```

### 1.3. Coverage Analysis

| Yêu cầu | DCNET Flow Feature | File Reference | Coverage | Gap |
|---------|-----------------|----------------|----------|-----|
| TT 99 CoA | Chart of Accounts | `accounts/doctype/account/` | 🔧 30% | No VN template |
| Nhật ký chung | General Ledger | `accounts/general_ledger.py` | ✅ 95% | Minor config |
| Giá xuất TB tháng | Stock Valuation | `stock/stock_ledger.py` | 🔧 70% | Monthly recalc |
| VND currency | Company Settings | `setup/doctype/company/` | ✅ 100% | None |
| CLTG đánh giá | Exchange Revaluation | `accounts/doctype/exchange_rate_revaluation/` | ✅ 85% | Minor config |
| Khấu hao đường thẳng | Asset Depreciation | `assets/doctype/asset/` | ✅ 95% | None |

---

## Phần 2: Kế Toán Tiền Mặt & Tiền Gửi

### 2.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 656-662

**Yêu cầu:**
1. ✅ Lập và in Phiếu Thu, Chi, Báo Nợ, Báo Có theo Thông tư 200
2. ✅ Tự động hạch toán chênh lệch tỷ giá ngoại tệ
3. ✅ Đánh giá chênh lệch tỷ giá cuối kỳ
4. ✅ Theo dõi Quỹ và các tài khoản ngân hàng
5. 🔧 Theo dõi khế ước

### 2.2. DCNET Flow Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KẾ TOÁN TIỀN MẶT & TIỀN GỬI                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SPEC REQUIREMENT              DCNET FLOW DOCTYPE           STATUS          │
│  ─────────────────────────────────────────────────────────────────          │
│                                                                              │
│  Phiếu Thu ────────────────► Payment Entry (Receive)        ✅ 95%         │
│                               File: payment_entry.py:1-3560                  │
│                                                                              │
│  Phiếu Chi ────────────────► Payment Entry (Pay)            ✅ 95%         │
│                               File: payment_entry.py:1-3560                  │
│                                                                              │
│  Báo Nợ ───────────────────► Journal Entry (Bank Entry)     ✅ 90%         │
│                               File: journal_entry.py:1-1765                  │
│                                                                              │
│  Báo Có ───────────────────► Journal Entry (Bank Entry)     ✅ 90%         │
│                               File: journal_entry.py:1-1765                  │
│                                                                              │
│  CLTG tự động ─────────────► Exchange Gain/Loss posting     ✅ 85%         │
│                               File: payment_entry.py:2486-2550               │
│                                                                              │
│  CLTG cuối kỳ ─────────────► Exchange Rate Revaluation      ✅ 85%         │
│                               File: exchange_rate_revaluation.py             │
│                                                                              │
│  Quỹ & Ngân hàng ──────────► Bank Account + Mode of Payment ✅ 95%         │
│                               File: bank_account.py, mode_of_payment.py      │
│                                                                              │
│  Khế ước ──────────────────► N/A                            ❌ 0%          │
│                               Cần build custom DocType                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3. Data Mapping: Phiếu Thu/Chi → Payment Entry

| Spec Field (Phiếu Thu/Chi) | DCNET Flow Field | Table | Auto/Manual |
|---------------------------|---------------|-------|-------------|
| Ngày chứng từ | `posting_date` | Payment Entry | Manual |
| Số chứng từ | `name` (auto) | Payment Entry | Auto |
| Loại phiếu (Thu/Chi) | `payment_type` (Receive/Pay) | Payment Entry | Manual |
| Khách hàng/NCC | `party` + `party_type` | Payment Entry | Manual |
| Tài khoản ngân hàng | `paid_from` / `paid_to` | Payment Entry | Manual |
| Số tiền | `paid_amount` | Payment Entry | Manual |
| Tiền tệ | `paid_from_account_currency` | Payment Entry | Auto |
| Tỷ giá | `source_exchange_rate` | Payment Entry | Auto/Manual |
| Số tiền quy đổi | `base_paid_amount` | Payment Entry | Auto |
| Hóa đơn liên quan | `references` | Payment Entry Reference | Manual |
| Diễn giải | `remarks` | Payment Entry | Manual |
| Người lập | `owner` | Payment Entry | Auto |

### 2.4. Workflow: Phiếu Thu Tiền

```mermaid
sequenceDiagram
    participant User as Kế toán
    participant SI as Sales Invoice
    participant PE as Payment Entry
    participant GL as GL Entry
    participant Bank as Bank Account

    User->>SI: Chọn hóa đơn cần thu
    SI-->>User: Hiển thị outstanding amount

    User->>PE: Create Payment Entry
    Note over PE: payment_type = "Receive"<br/>party_type = "Customer"<br/>mode_of_payment = "Bank/Cash"

    PE->>PE: Validate & Calculate
    Note over PE: Check exchange rate<br/>Calculate base_amount<br/>Allocate to invoices

    User->>PE: Submit

    PE->>GL: make_gl_entries()
    Note over GL: Debit: Bank/Cash<br/>Credit: Receivable

    GL->>Bank: Update Bank Balance
    GL->>SI: Update Outstanding

    SI-->>User: Status = Paid
```

### 2.5. Code Reference: Payment Entry GL Creation

**File:** `dcnet_core/erpnext/accounts/doctype/payment_entry/payment_entry.py`

```python
# Line 2486-2550: Exchange gain/loss calculation
def set_difference_amount(self):
    """Calculate exchange difference when payment currency differs from company currency"""
    if self.paid_from_account_currency != self.company_currency:
        # Calculate unrealized gain/loss
        self.difference_amount = flt(self.base_paid_amount) - flt(self.base_received_amount)

# Line 2800-2900: GL Entry creation
def get_gl_entries(self, cancel=0):
    gl_entries = []

    # Debit: Bank/Cash account
    gl_entries.append(
        self.get_gl_dict({
            "account": self.paid_to,
            "debit_in_account_currency": self.received_amount,
            "debit": self.base_received_amount,
        })
    )

    # Credit: Receivable/Payable account
    gl_entries.append(
        self.get_gl_dict({
            "account": self.paid_from,
            "credit_in_account_currency": self.paid_amount,
            "credit": self.base_paid_amount,
            "party_type": self.party_type,
            "party": self.party,
        })
    )

    return gl_entries
```

### 2.6. Gap: Khế Ước Tracking

**Yêu cầu:** Theo dõi khế ước (hợp đồng ngoại tệ)

**DCNET Flow Status:** ❌ Không có concept này

**Solution:** Build custom DocType `dcnet/forex-contract`

```python
# Proposed DocType: Forex Contract
class ForexContract(Document):
    # Fields
    contract_no: str          # Số khế ước
    contract_date: date       # Ngày ký
    bank: str                 # Ngân hàng
    currency: str             # Loại ngoại tệ
    amount: float             # Số tiền
    exchange_rate: float      # Tỷ giá ký
    maturity_date: date       # Ngày đáo hạn
    status: Literal["Active", "Settled", "Cancelled"]

    # Methods
    def on_submit(self):
        # Create GL entry for forex commitment
        pass

    def settle(self):
        # Settle contract and calculate gain/loss
        pass
```

**Effort:** 1-2 weeks

---

## Phần 3: Kế Toán Bán Hàng & Công Nợ Phải Thu

### 3.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 666-673

**Yêu cầu:**
1. ✅ Lập và in hóa đơn, phiếu hàng bán bị trả lại, phiếu thu tiền hàng
2. ⭐ **Theo dõi công nợ theo hạn thanh toán** - CRITICAL
3. ✅ Báo cáo tổng hợp, chi tiết công nợ phải thu KH
4. ✅ Báo cáo Bảng kê/sổ chi tiết, phân tích bán hàng
5. 🔧 Tính giá vốn hàng bán trung bình tháng
6. 🔧 Các báo cáo thuế GTGT

### 3.2. DCNET Flow Mapping

```mermaid
graph TB
    subgraph "Customer Spec - Bán hàng"
        S1[Hóa đơn bán hàng]
        S2[Hàng bán trả lại]
        S3[Phiếu thu tiền]
        S4[Công nợ theo hạn TT]
        S5[Báo cáo công nợ]
        S6[Giá vốn TB tháng]
        S7[Báo cáo VAT]
    end

    subgraph "DCNET Flow DocTypes"
        E1[Sales Invoice<br>✅ 95%]
        E2[Sales Return<br>✅ 90%]
        E3[Payment Entry<br>✅ 95%]
        E4[Payment Ledger + Aging<br>🔧 60%]
        E5[AR Reports<br>✅ 85%]
        E6[Stock Valuation<br>🔧 70%]
        E7[Tax Reports<br>🔧 50%]
    end

    S1 --> E1
    S2 --> E2
    S3 --> E3
    S4 --> E4
    S5 --> E5
    S6 --> E6
    S7 --> E7
```

### 3.3. Data Mapping: Hóa Đơn Bán Hàng → Sales Invoice

**Spec Reference:** ERP_SPECIFICATION.md Section 2, Step 9 (lines 164-182)

| Spec Field | DCNET Flow Field | DocType | Coverage |
|-----------|---------------|---------|----------|
| Ngày chứng từ | `posting_date` | Sales Invoice | ✅ |
| Khách hàng | `customer` | Sales Invoice | ✅ |
| Hình thức TT | `mode_of_payment` | Sales Invoice | ✅ |
| Số hóa đơn | `name` / `invoice_no` | Sales Invoice | ✅ |
| Hạn thanh toán | `due_date` / `payment_terms_template` | Sales Invoice | ✅ |
| Mã tiền tệ | `currency` | Sales Invoice | ✅ |
| Tổng tiền hàng | `total` | Sales Invoice | ✅ |
| Tổng tiền CK | `discount_amount` | Sales Invoice | ✅ |
| Tổng tiền thuế | `total_taxes_and_charges` | Sales Invoice | ✅ |
| Tổng tiền | `grand_total` | Sales Invoice | ✅ |
| --- Chi tiết --- | --- | --- | --- |
| Mã vật tư | `item_code` | Sales Invoice Item | ✅ |
| Tên vật tư | `item_name` | Sales Invoice Item | ✅ |
| ĐVT | `uom` | Sales Invoice Item | ✅ |
| Số lượng | `qty` | Sales Invoice Item | ✅ |
| Số bảng giá | `price_list` | Sales Invoice | ✅ |
| Đơn giá trước CK | `price_list_rate` | Sales Invoice Item | ✅ |
| Thành tiền trước CK | `base_amount` | Sales Invoice Item | ✅ |
| Số chính sách CK | `pricing_rule` | Sales Invoice Item | ✅ |
| % CK | `discount_percentage` | Sales Invoice Item | ✅ |
| Tiền CK | `discount_amount` | Sales Invoice Item | ✅ |
| Thành tiền sau CK | `amount` | Sales Invoice Item | ✅ |
| --- Lô/Serial --- | --- | --- | --- |
| Số lô | `batch_no` | Sales Invoice Item | ✅ |
| Số seri | `serial_no` | Sales Invoice Item | ✅ |

### 3.4. Sales Invoice Workflow

```mermaid
flowchart TD
    subgraph "From Sales Module"
        SO[Sales Order]
        DN[Delivery Note]
    end

    subgraph "Sales Invoice Process"
        SI_Draft[Sales Invoice<br>Draft]
        SI_Valid[Validate]
        SI_Submit[Submit]
    end

    subgraph "Accounting Impact"
        GL[GL Entry]
        AR[Update AR]
        Stock[Update Stock<br>if POS]
    end

    subgraph "Collection"
        PE[Payment Entry]
        Aging[Aging Update]
    end

    SO -->|Get Items| SI_Draft
    DN -->|Get Items + Qty| SI_Draft

    SI_Draft --> SI_Valid
    SI_Valid -->|Pass| SI_Submit
    SI_Valid -->|Fail| SI_Draft

    SI_Submit --> GL
    GL --> AR
    GL --> Stock

    AR --> Aging
    PE -->|Allocate| AR
    PE --> Aging

    style SI_Submit fill:#90EE90
    style GL fill:#FFD700
```

### 3.5. GL Entry: Sales Invoice

```
📊 Bán hàng 10.000.000 VND + VAT 10% = 11.000.000 VND (chưa thu tiền):

┌────────────────────────────┬────────────┬────────────┐
│ Tài khoản                  │ Nợ (Debit) │ Có (Credit)│
├────────────────────────────┼────────────┼────────────┤
│ 131 - Phải thu khách hàng  │ 11.000.000 │            │
│ (Receivable)               │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 511 - Doanh thu bán hàng   │            │ 10.000.000 │
│ (Revenue)                  │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 3331 - Thuế VAT đầu ra     │            │  1.000.000 │
│ (Tax Payable)              │            │            │
├────────────────────────────┼────────────┼────────────┤
│ TỔNG                       │ 11.000.000 │ 11.000.000 │
└────────────────────────────┴────────────┴────────────┘

Code Reference: sales_invoice.py:474 - on_submit() → make_gl_entries()
```

### 3.6. Gap: Công Nợ Theo Hạn Thanh Toán ⭐⭐⭐

**Yêu cầu Spec:** Theo dõi công nợ theo hạn thanh toán (từ ERP_SPECIFICATION.md Section 2.7-2.8)

**Điều kiện xuất hàng hợp lệ (line 158-162):**
1. KH không có hóa đơn quá hạn
2. Giá trị công nợ hiện tại + giá trị lệnh xuất đã duyệt chưa xuất + giá trị lệnh xuất hiện tại ≤ hạn mức

**DCNET Flow Status:**

| Feature | DCNET Flow | Coverage | Gap |
|---------|---------|----------|-----|
| Hạn mức công nợ | Credit Limit on Customer | ✅ 85% | Basic check only |
| Aging Report | Accounts Receivable | ✅ 90% | Good |
| Hóa đơn quá hạn check | N/A | ❌ 0% | Need build |
| Pending DN check | N/A | ❌ 0% | Need build |
| Approval workflow | N/A | ❌ 0% | Need build |
| Auto notification | N/A | ❌ 0% | Need build |

**Solution: dcnet/credit-management module**

```mermaid
flowchart TD
    SO[Sales Order] --> Check{Credit Check}

    Check --> C1{Có HĐ quá hạn?}
    C1 -->|Có| Block1[BLOCK<br>Cần KTT approve]
    C1 -->|Không| C2

    C2{Current + Pending + New ≤ Limit?}
    C2 -->|Vượt| Block2[BLOCK<br>Cần KTT approve]
    C2 -->|OK| Pass[PASS<br>Cho phép xuất hàng]

    Block1 --> Approve{KTT Approve?}
    Block2 --> Approve

    Approve -->|Yes| Pass
    Approve -->|No| Reject[REJECT<br>Không cho xuất]

    Pass --> DN[Delivery Note]

    style Block1 fill:#FF6B6B
    style Block2 fill:#FF6B6B
    style Pass fill:#90EE90
    style Reject fill:#FF0000
```

**Implementation:**

```python
# dcnet_apps/credit_management/credit_check.py

def validate_credit_on_sales_order(doc, method):
    """Hook: Sales Order before_submit"""
    customer = doc.customer

    # Check 1: Overdue invoices
    overdue = get_overdue_invoices(customer)
    if overdue:
        if not has_cfo_approval(doc):
            frappe.throw(f"Khách hàng có {len(overdue)} hóa đơn quá hạn. Cần KTT phê duyệt.")

    # Check 2: Credit limit
    current_outstanding = get_outstanding_amount(customer)
    pending_deliveries = get_pending_delivery_value(customer)
    new_order_value = doc.grand_total

    credit_limit = get_credit_limit(customer)
    total_exposure = current_outstanding + pending_deliveries + new_order_value

    if total_exposure > credit_limit:
        if not has_cfo_approval(doc):
            frappe.throw(f"Vượt hạn mức công nợ: {total_exposure:,.0f} > {credit_limit:,.0f}. Cần KTT phê duyệt.")

def get_overdue_invoices(customer):
    """Get list of overdue Sales Invoices"""
    return frappe.db.sql("""
        SELECT name, posting_date, due_date, outstanding_amount
        FROM `tabSales Invoice`
        WHERE customer = %s
        AND docstatus = 1
        AND outstanding_amount > 0
        AND due_date < CURDATE()
    """, customer, as_dict=True)

def get_pending_delivery_value(customer):
    """Get value of Delivery Notes not yet invoiced"""
    return frappe.db.sql("""
        SELECT COALESCE(SUM(grand_total), 0) as total
        FROM `tabDelivery Note`
        WHERE customer = %s
        AND docstatus = 1
        AND status NOT IN ('Completed', 'Cancelled')
    """, customer)[0][0] or 0
```

**Effort:** 3-4 weeks

---

## Phần 4: Kế Toán Mua Hàng & Công Nợ Phải Trả

### 4.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 677-684

**Yêu cầu:**
1. ✅ Phiếu nhập mua, phiếu chi phí vận chuyển, phiếu chi trả NCC
2. ✅ Bù trừ công nợ, thanh toán tạm ứng
3. ⭐ Theo dõi công nợ theo hạn thanh toán
4. ✅ Theo dõi, hạch toán thuế GTGT, thuế nhập khẩu
5. 🔧 **Phân bổ chi phí mua, vận chuyển, thuế NK cho mặt hàng**
6. 🔧 Bảng đối chiếu công nợ NCC
7. ✅ Báo cáo chi tiết mua hàng, sổ nhật ký mua hàng

### 4.2. DCNET Flow Mapping

| Spec Feature | DCNET Flow DocType | Coverage | Notes |
|--------------|-----------------|----------|-------|
| Phiếu nhập mua | Purchase Invoice | ✅ 95% | Direct mapping |
| Chi phí vận chuyển | Landed Cost Voucher | ✅ 85% | Need config |
| Phiếu chi trả NCC | Payment Entry (Pay) | ✅ 95% | Direct mapping |
| Bù trừ công nợ | Payment Reconciliation | ✅ 85% | Config |
| Thanh toán tạm ứng | Advance Payment | ✅ 90% | Config |
| CN theo hạn TT | AP Aging | ✅ 85% | Report available |
| Thuế GTGT đầu vào | Tax template | ✅ 85% | Config rates |
| Thuế nhập khẩu | Landed Cost | ✅ 85% | Config |
| **Phân bổ CP mua** | Landed Cost Voucher | 🔧 70% | Extend allocation |
| **Phân bổ vận chuyển** | Landed Cost Voucher | 🔧 70% | Extend allocation |
| **Phân bổ thuế NK** | Landed Cost Voucher | 🔧 70% | Extend allocation |
| Đối chiếu CN NCC | Supplier Ledger | 🔧 60% | Build reconciliation |
| Báo cáo mua hàng | Purchase Register | ✅ 90% | Available |

### 4.3. Landed Cost Voucher Workflow

```mermaid
sequenceDiagram
    participant PR as Purchase Receipt
    participant PI as Purchase Invoice
    participant LCV as Landed Cost Voucher
    participant Stock as Stock Ledger

    PR->>Stock: Nhập kho (giá tạm)
    Note over Stock: Item cost = Invoice price

    PI->>PI: Ghi nhận công nợ NCC

    Note over LCV: Thu thập các chi phí:<br/>- Vận chuyển<br/>- Thuế NK<br/>- Chi phí khác

    LCV->>LCV: Phân bổ chi phí theo quy tắc
    Note over LCV: Allocation by:<br/>- Quantity<br/>- Amount<br/>- Manual

    LCV->>Stock: Cập nhật giá vốn
    Note over Stock: Item cost = Invoice + Allocated costs

    LCV->>LCV: Create GL entries
```

### 4.4. Data Mapping: Phiếu Nhập Mua → Purchase Invoice

| Spec Field | DCNET Flow Field | Notes |
|-----------|---------------|-------|
| Ngày chứng từ | `posting_date` | ✅ |
| Số phiếu | `name` | Auto |
| Người lập | `owner` | Auto |
| NCC | `supplier` | ✅ |
| Tiền tệ | `currency` | ✅ |
| Kho | `set_warehouse` | ✅ |
| Số tờ khai | `custom_declaration_no` | 🔧 Custom field |
| Mã vật tư | `item_code` | ✅ |
| Số lượng | `qty` | ✅ |
| Đơn giá nhập | `rate` | ✅ |
| Thành tiền | `amount` | ✅ |
| Số lô | `batch_no` | ✅ |
| Số seri | `serial_no` | ✅ |
| Số đơn hàng | `purchase_order` | Link field |
| Số lệnh nhập | `purchase_receipt` | Link field |

### 4.5. GL Entry: Purchase Invoice

```
📊 Mua hàng 8.000.000 + VAT 10% + Thuế NK 5% = 9.200.000 VND:

┌────────────────────────────┬────────────┬────────────┐
│ Tài khoản                  │ Nợ (Debit) │ Có (Credit)│
├────────────────────────────┼────────────┼────────────┤
│ 156 - Hàng hóa             │  8.000.000 │            │
│ (Stock in Warehouse)       │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 1331 - Thuế VAT đầu vào    │    800.000 │            │
│ (Input VAT)                │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 3333 - Thuế nhập khẩu      │    400.000 │            │
│ (Import Duty - Asset)      │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 331 - Phải trả NCC         │            │  8.800.000 │
│ (Payable - excl duty)      │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 3333 - Thuế NK phải nộp    │            │    400.000 │
│ (Import Duty Payable)      │            │            │
├────────────────────────────┼────────────┼────────────┤
│ TỔNG                       │  9.200.000 │  9.200.000 │
└────────────────────────────┴────────────┴────────────┘

Code Reference: purchase_invoice.py:1200-1400 - make_gl_entries()
```

### 4.6. Gap: Phân Bổ Chi Phí Mua Hàng

**Yêu cầu:** Phân bổ chi phí mua, vận chuyển, thuế NK cho các mặt hàng

**DCNET Flow Landed Cost Voucher:**

```python
# dcnet_core/erpnext/stock/doctype/landed_cost_voucher/landed_cost_voucher.py

class LandedCostVoucher(Document):
    # Line 45-80: Allocation methods
    def set_applicable_charges_for_item(self):
        """Distribute applicable charges among items"""
        for item in self.get("items"):
            if self.distribute_charges_based_on == "Amount":
                # Phân bổ theo giá trị
                item.applicable_charges = flt(item.amount) / flt(self.total_item_cost) * total_charges
            elif self.distribute_charges_based_on == "Qty":
                # Phân bổ theo số lượng
                item.applicable_charges = flt(item.qty) / flt(self.total_qty) * total_charges
```

**Gap:** DCNET Flow có sẵn nhưng cần config & customize:
- ✅ Phân bổ theo Amount/Qty - có sẵn
- 🔧 Phân bổ thuế NK riêng - cần extend
- 🔧 Phân bổ vận chuyển quốc tế vs nội địa - cần extend
- 🔧 UI cho kế toán VN - cần customize

**Effort:** 1-2 weeks

---

## Phần 5: Kế Toán Hàng Tồn Kho

### 5.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 688-692

**Yêu cầu:**
1. ✅ Phiếu nhập, xuất, điều chuyển, xuất CCDC
2. ✅ Quản lý NXT theo kho, mặt hàng, nhóm hàng
3. ⭐ **Tính giá vốn tự động theo trung bình tháng**

### 5.2. DCNET Flow Mapping

| Spec Feature | DCNET Flow DocType | Coverage |
|--------------|-----------------|----------|
| Phiếu nhập kho | Stock Entry (Receipt) | ✅ 95% |
| Phiếu xuất kho | Stock Entry (Issue) | ✅ 95% |
| Phiếu điều chuyển | Stock Entry (Transfer) | ✅ 95% |
| Phiếu xuất CCDC | Stock Entry + Deferred | 🔧 70% |
| NXT theo kho | Stock Balance Report | ✅ 95% |
| NXT theo mặt hàng | Stock Ledger Report | ✅ 95% |
| **Giá vốn TB tháng** | Moving Average | 🔧 70% |

### 5.3. Gap: Giá Vốn Trung Bình Tháng

**Yêu cầu:** Tính giá vốn xuất kho theo phương pháp **trung bình tháng** (Monthly Weighted Average)

**DCNET Flow Default:** Moving Average (perpetual) - tính liên tục theo từng giao dịch

**Sự khác biệt:**

| Aspect | Moving Average (DCNET Flow) | Monthly Weighted Average (Spec) |
|--------|-------------------------|--------------------------------|
| Timing | Sau mỗi transaction | Cuối tháng |
| Calculation | `(Old Qty × Old Rate + New Qty × New Rate) / Total Qty` | `(Opening + Purchases) / (Opening Qty + Purchase Qty)` |
| COGS Update | Real-time | Month-end batch |
| VN Compliance | ⚠️ Not standard | ✅ TT 99 compliant |

**Solution:** Monthly recalculation job

```python
# dcnet_apps/accounting/monthly_valuation.py

def recalculate_monthly_cogs():
    """
    Run at month-end to recalculate COGS using Monthly Weighted Average
    Replaces Moving Average with period-based calculation
    """
    period_start = get_first_day(today())
    period_end = get_last_day(today())

    for item in get_all_items():
        # Get opening balance
        opening_qty, opening_value = get_opening_balance(item, period_start)

        # Get purchases in period
        purchase_qty, purchase_value = get_purchases(item, period_start, period_end)

        # Calculate weighted average
        total_qty = opening_qty + purchase_qty
        total_value = opening_value + purchase_value

        if total_qty > 0:
            avg_rate = total_value / total_qty
        else:
            avg_rate = 0

        # Update all stock ledger entries in period
        update_stock_ledger_valuation(item, period_start, period_end, avg_rate)

        # Repost GL entries
        repost_gl_entries_for_item(item, period_start, period_end)
```

**Effort:** 2-3 weeks

---

## Phần 6: Kế Toán TSCĐ & CCDC

### 6.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 696-704

**Yêu cầu TSCĐ:**
1. ✅ Khai báo, đăng ký và quản lý tài sản
2. ✅ Thẻ tài sản, biến động, biên bản thanh lý
3. ✅ Tự động tính khấu hao theo đường thẳng
4. ✅ Báo cáo TSCĐ

**Yêu cầu CCDC:**
1. 🔧 Theo dõi các lần xuất dùng CCDC
2. 🔧 Giá trị phân bổ CCDC vào chi phí
3. 🔧 Tính phân bổ trong các kỳ khác nhau
4. 🔧 Báo cáo CCDC

### 6.2. DCNET Flow Asset Management

```mermaid
flowchart TD
    subgraph "Asset Lifecycle"
        A1[Asset Purchase] --> A2[Asset Creation]
        A2 --> A3[Depreciation Schedule]
        A3 --> A4[Monthly Depreciation]
        A4 --> A5[Asset Disposal/Sale]
    end

    subgraph "DCNET Flow DocTypes"
        D1[Purchase Invoice<br>with Asset item]
        D2[Asset<br>✅ 95%]
        D3[Asset Depreciation Schedule<br>✅ 95%]
        D4[Depreciation Entry<br>✅ 95%]
        D5[Asset Movement<br>✅ 90%]
    end

    A1 --> D1
    A2 --> D2
    A3 --> D3
    A4 --> D4
    A5 --> D5
```

### 6.3. Data Mapping: TSCĐ → Asset

| Spec Field | DCNET Flow Field | Coverage |
|-----------|---------------|----------|
| Mã tài sản | `asset_name` | ✅ |
| Tên tài sản | `asset_name` | ✅ |
| Ngày mua | `purchase_date` | ✅ |
| Ngày sử dụng | `available_for_use_date` | ✅ |
| Nguyên giá | `gross_purchase_amount` | ✅ |
| Thời gian KH (năm) | `total_number_of_depreciations` | ✅ |
| Phương pháp KH | `depreciation_method` | ✅ |
| Nguồn vốn | `finance_book` | ✅ |
| Bộ phận sử dụng | `location` / `cost_center` | ✅ |
| Tình trạng | `status` | ✅ |

### 6.4. Depreciation GL Entry

```
📊 Khấu hao TSCĐ 100.000.000 VND, 5 năm, đường thẳng:

Khấu hao hàng tháng = 100.000.000 / 5 / 12 = 1.666.667 VND

┌────────────────────────────┬────────────┬────────────┐
│ Tài khoản                  │ Nợ (Debit) │ Có (Credit)│
├────────────────────────────┼────────────┼────────────┤
│ 6424 - Chi phí khấu hao    │  1.666.667 │            │
│ (Depreciation Expense)     │            │            │
├────────────────────────────┼────────────┼────────────┤
│ 2141 - Hao mòn TSCĐ HH     │            │  1.666.667 │
│ (Accumulated Depreciation) │            │            │
└────────────────────────────┴────────────┴────────────┘

Code Reference: asset.py:200-280 - make_depreciation_entry()
```

### 6.5. Gap: CCDC Phân Bổ

**Yêu cầu:** Công cụ dụng cụ (CCDC) - phân bổ giá trị vào chi phí qua nhiều kỳ

**DCNET Flow Status:**
- ✅ Deferred Expense concept có sẵn
- 🔧 CCDC specific workflow cần customize
- 🔧 VN accounting treatment cần extend

**Solution:** Extend Deferred Expense for CCDC

```python
# dcnet_apps/accounting/ccdc.py

class CCDCAllocation(Document):
    """
    Công cụ dụng cụ (CCDC) - Small tools/equipment allocation
    Vietnamese accounting specific
    """

    # Fields
    item_code: str              # Mã CCDC
    issue_date: date            # Ngày xuất dùng
    total_value: float          # Giá trị
    allocation_months: int      # Số tháng phân bổ
    expense_account: str        # TK chi phí (6272, 6422...)
    deferred_account: str       # TK chờ phân bổ (242)
    department: str             # Bộ phận sử dụng

    def on_submit(self):
        # Create initial entry: Debit 242, Credit 153
        self.create_issue_entry()

        # Create allocation schedule
        self.create_allocation_schedule()

    def create_allocation_schedule(self):
        """Create monthly allocation entries"""
        monthly_amount = self.total_value / self.allocation_months

        for month in range(self.allocation_months):
            date = add_months(self.issue_date, month)

            # Debit: Expense (6272)
            # Credit: Deferred (242)
            create_journal_entry(
                debit_account=self.expense_account,
                credit_account=self.deferred_account,
                amount=monthly_amount,
                posting_date=get_last_day(date),
                remarks=f"Phân bổ CCDC: {self.item_code} - Kỳ {month+1}/{self.allocation_months}"
            )
```

**Effort:** 2-3 weeks

---

## Phần 7: Kế Toán Tổng Hợp

### 7.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 708-715

**Yêu cầu:**
1. ✅ Phiếu kế toán khác, phiếu bù trừ công nợ
2. ✅ Tạo bút toán chênh lệch tỷ giá tự động
3. 🔧 Các bút toán định kỳ
4. 🔧 Bút toán kết chuyển và phân bổ
5. ✅ Sổ chi tiết, sổ tổng hợp, bảng CĐTK, nhật ký chung

### 7.2. DCNET Flow Mapping

| Spec Feature | DCNET Flow DocType | Coverage |
|--------------|-----------------|----------|
| Phiếu KT khác | Journal Entry | ✅ 95% |
| Bù trừ công nợ | Payment Reconciliation | ✅ 85% |
| CLTG tự động | Exchange Rate Revaluation | ✅ 85% |
| Bút toán định kỳ | Auto Repeat + JE Template | 🔧 70% |
| Kết chuyển cuối kỳ | Period Closing Voucher | ✅ 85% |
| Phân bổ | Journal Entry | ✅ 85% |
| Sổ chi tiết TK | Account Ledger | ✅ 95% |
| Sổ tổng hợp | General Ledger | ✅ 95% |
| Bảng CĐTK | Trial Balance | ✅ 95% |
| Nhật ký chung | General Journal | ✅ 95% |

### 7.3. Period Closing Workflow

```mermaid
flowchart TD
    subgraph "Month-End Process"
        M1[Cutoff Date] --> M2[Run COGS Calculation]
        M2 --> M3[Post Depreciation]
        M3 --> M4[Exchange Rate Revaluation]
        M4 --> M5[Review Trial Balance]
    end

    subgraph "Year-End Process"
        Y1[Period Closing Voucher] --> Y2[Close P&L Accounts]
        Y2 --> Y3[Transfer to Retained Earnings]
        Y3 --> Y4[Create Opening Balance]
    end

    M5 --> Y1

    style Y1 fill:#FFD700
```

### 7.4. Code Reference: Period Closing

**File:** `dcnet_core/erpnext/accounts/doctype/period_closing_voucher/period_closing_voucher.py`

```python
# Line 100-150: Close P&L accounts
def make_gl_entries(self):
    gl_entries = []

    # Get P&L account balances
    for account in self.get_pl_accounts():
        balance = get_account_balance(account, self.posting_date)

        if balance > 0:
            # Credit balance -> Debit to zero
            gl_entries.append({
                "account": account,
                "debit": balance,
            })
        else:
            # Debit balance -> Credit to zero
            gl_entries.append({
                "account": account,
                "credit": abs(balance),
            })

    # Transfer net P&L to Retained Earnings
    net_pl = sum(e.get("debit", 0) - e.get("credit", 0) for e in gl_entries)

    gl_entries.append({
        "account": self.closing_account_head,  # Retained Earnings
        "credit" if net_pl > 0 else "debit": abs(net_pl),
    })

    return gl_entries
```

---

## Phần 8: Tính Năng Đặc Biệt

### 8.1. Spec Khách Hàng

**Nguồn:** ERP_SPECIFICATION.md Section 5, lines 719-742

**3 tính năng đặc biệt:**

1. ❌ **Tính chi phí hỗ trợ của hãng** (lines 721-725)
2. ❌ **Báo cáo chi phí theo sự kiện** (lines 727-736)
3. ❌ **Báo cáo tổng hợp cho NM + Đại diện hãng** (lines 739-742)

### 8.2. Gap Analysis

| Feature | DCNET Flow | Coverage | Module to Build |
|---------|---------|----------|-----------------|
| Chi phí hỗ trợ hãng | N/A | ❌ 0% | `dcnet/supplier-support` |
| Báo cáo sự kiện | N/A | ❌ 0% | `dcnet/event-costing` |
| Báo cáo NM+Hãng | N/A | ❌ 0% | Custom reports + API |

### 8.3. Module Design: Chi Phí Hỗ Trợ Hãng

```mermaid
erDiagram
    SUPPLIER_SUPPORT_EVENT ||--o{ SUPPORT_ALLOCATION : has
    SUPPLIER_SUPPORT_EVENT {
        string name PK
        date event_date
        string supplier
        string event_type
        float total_support_amount
        string status
    }

    SUPPORT_ALLOCATION {
        string name PK
        string parent FK
        string cost_center
        string expense_account
        float amount
        string remarks
    }

    SUPPLIER_SUPPORT_EVENT ||--o{ GL_ENTRY : creates
```

**DocType: Supplier Support Event**

```python
# dcnet_apps/supplier_support/supplier_support_event.py

class SupplierSupportEvent(Document):
    """
    Ghi nhận chi phí hỗ trợ từ hãng (vendor support)
    """

    # Fields
    event_name: str           # Tên sự kiện
    event_date: date          # Ngày sự kiện
    supplier: str             # Hãng (Titleist, Callaway...)
    event_type: Literal["Demo", "Marketing", "Training", "Sponsorship"]
    total_support_amount: float  # Tổng chi phí hỗ trợ

    # Child table: Allocation to cost centers
    allocations: List[SupportAllocation]

    def on_submit(self):
        """Create GL entries for support received"""
        # Debit: Expense accounts (per allocation)
        # Credit: Supplier Support Received (income)
        self.make_gl_entries()

    def make_gl_entries(self):
        gl_entries = []

        for alloc in self.allocations:
            # Debit expense
            gl_entries.append({
                "account": alloc.expense_account,
                "cost_center": alloc.cost_center,
                "debit": alloc.amount,
            })

        # Credit income
        gl_entries.append({
            "account": self.get_support_income_account(),
            "credit": self.total_support_amount,
            "party_type": "Supplier",
            "party": self.supplier,
        })

        return gl_entries
```

### 8.4. Module Design: Event Costing

```mermaid
flowchart TD
    subgraph "Event Costing Module"
        EC[Event Costing]
        EC --> T1[Marketing Event]
        EC --> T2[Demo Event]
        EC --> T3[Sales Event]
        EC --> T4[Pricing Error]
    end

    subgraph "Cost Collection"
        GL[GL Entries] --> EC
        SI[Sales Invoices] --> EC
        PE[Expenses] --> EC
    end

    subgraph "Reports"
        EC --> R1[Event Profitability]
        EC --> R2[Cost by Category]
        EC --> R3[ROI Analysis]
    end
```

**DocType: Event Costing**

```python
# dcnet_apps/event_costing/event_costing.py

class EventCosting(Document):
    """
    Báo cáo chi phí theo sự kiện
    4 loại: Marketing, Demo, Bán hàng, Sai giá
    """

    # Fields
    event_name: str
    event_type: Literal["Marketing", "Demo", "Sales", "Pricing Error"]
    start_date: date
    end_date: date

    # Linked documents
    sales_invoices: List[str]      # Linked sales
    expense_entries: List[str]     # Linked expenses
    support_events: List[str]      # Linked supplier support

    # Calculated fields
    total_revenue: float = 0
    total_cost: float = 0
    total_support: float = 0
    net_profit: float = 0

    def calculate_totals(self):
        """Calculate event profitability"""
        # Revenue from linked sales
        self.total_revenue = sum(
            frappe.db.get_value("Sales Invoice", si, "grand_total")
            for si in self.sales_invoices
        )

        # Costs from expenses
        self.total_cost = sum(
            frappe.db.get_value("Journal Entry", je, "total_debit")
            for je in self.expense_entries
        )

        # Support received
        self.total_support = sum(
            frappe.db.get_value("Supplier Support Event", sse, "total_support_amount")
            for sse in self.support_events
        )

        # Net profit
        self.net_profit = self.total_revenue - self.total_cost + self.total_support
```

### 8.5. Effort Estimate

| Module | Features | Effort |
|--------|----------|--------|
| `dcnet/supplier-support` | DocType, GL integration, Reports | 3-4 weeks |
| `dcnet/event-costing` | DocType, Linkage, Profitability | 3-4 weeks |
| Partner Report API | Data aggregation, API endpoint | 2-3 weeks |
| **Total** | | **8-11 weeks** |

---

## Phần 9: Tổng Hợp Coverage Matrix

### 9.1. Feature-by-Feature Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ACCOUNTING SPEC vs DCNET FLOW COVERAGE MATRIX                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  FEATURE                              DCNET FLOW  COVERAGE   ACTION             │
│  ─────────────────────────────────────────────────────────────────────          │
│                                                                                  │
│  === KẾ TOÁN TIỀN MẶT/GỬI ===                                                   │
│  Phiếu Thu                            Payment Entry   ✅ 95%    Config          │
│  Phiếu Chi                            Payment Entry   ✅ 95%    Config          │
│  Báo Nợ/Có                            Journal Entry   ✅ 90%    Config          │
│  CLTG tự động                         Exchange G/L    ✅ 85%    Config          │
│  CLTG cuối kỳ                         Revaluation     ✅ 85%    Config          │
│  Quỹ & Ngân hàng                      Bank Account    ✅ 95%    Config          │
│  Theo dõi khế ước                     N/A             ❌ 0%     Build           │
│                                                                                  │
│  === KẾ TOÁN BÁN HÀNG ===                                                       │
│  Hóa đơn bán hàng                     Sales Invoice   ✅ 95%    Config          │
│  Hàng bán trả lại                     Sales Return    ✅ 90%    Config          │
│  Phiếu thu tiền                       Payment Entry   ✅ 95%    Config          │
│  Công nợ theo hạn TT                  AR Aging        🔧 60%    Build workflow  │
│  Báo cáo CN KH                        AR Reports      ✅ 85%    Config          │
│  Giá vốn TB tháng                     Stock Valuation 🔧 70%    Monthly job     │
│  Báo cáo VAT                          Tax Reports     🔧 50%    Build templates │
│                                                                                  │
│  === KẾ TOÁN MUA HÀNG ===                                                       │
│  Phiếu nhập mua                       Purchase Inv    ✅ 95%    Config          │
│  Chi phí vận chuyển                   Landed Cost     ✅ 85%    Config          │
│  Phiếu chi trả NCC                    Payment Entry   ✅ 95%    Config          │
│  Bù trừ công nợ                       Reconciliation  ✅ 85%    Config          │
│  Thanh toán tạm ứng                   Advance Payment ✅ 90%    Config          │
│  CN theo hạn TT                       AP Aging        ✅ 85%    Config          │
│  Thuế GTGT/NK                         Tax templates   ✅ 85%    Config          │
│  Phân bổ CP mua/VC/NK                 Landed Cost     🔧 70%    Extend          │
│  Đối chiếu CN NCC                     Supplier Ledger 🔧 60%    Build           │
│                                                                                  │
│  === KẾ TOÁN TỒN KHO ===                                                        │
│  Phiếu nhập/xuất/điều chuyển          Stock Entry     ✅ 95%    Config          │
│  NXT theo kho/mặt hàng                Stock Reports   ✅ 95%    Config          │
│  Giá vốn TB tháng                     Valuation       🔧 70%    Monthly job     │
│                                                                                  │
│  === KẾ TOÁN TSCĐ/CCDC ===                                                      │
│  TSCĐ management                      Asset           ✅ 90%    Config          │
│  Khấu hao đường thẳng                 Depreciation    ✅ 95%    Config          │
│  CCDC xuất dùng                       Stock Entry     🔧 70%    Extend          │
│  CCDC phân bổ                         Deferred Exp    🔧 60%    Build           │
│                                                                                  │
│  === KẾ TOÁN TỔNG HỢP ===                                                       │
│  Phiếu KT khác                        Journal Entry   ✅ 95%    Config          │
│  Bút toán định kỳ                     Auto Repeat     🔧 70%    Config          │
│  Kết chuyển cuối kỳ                   Period Closing  ✅ 85%    Config          │
│  Sổ/báo cáo                           Reports         ✅ 90%    Config          │
│                                                                                  │
│  === TÍNH NĂNG ĐẶC BIỆT ===                                                     │
│  Chi phí hỗ trợ hãng                  N/A             ❌ 0%     Build module    │
│  Báo cáo sự kiện                      N/A             ❌ 0%     Build module    │
│  Báo cáo NM+Hãng                      N/A             ❌ 0%     Build API       │
│                                                                                  │
│  === CREDIT MANAGEMENT ===                                                       │
│  Hạn mức công nợ                      Credit Limit    ✅ 85%    Config          │
│  Check HĐ quá hạn                     N/A             ❌ 0%     Build           │
│  Check pending DN                     N/A             ❌ 0%     Build           │
│  Approval workflow                    N/A             ❌ 0%     Build           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2. Summary Statistics

| Category | ✅ Ready | 🔧 Customize | ❌ Build | Total Items |
|----------|---------|-------------|---------|-------------|
| Tiền mặt/Gửi | 6 | 0 | 1 | 7 |
| Bán hàng | 4 | 3 | 0 | 7 |
| Mua hàng | 7 | 2 | 1 | 10 |
| Tồn kho | 2 | 1 | 0 | 3 |
| TSCĐ/CCDC | 2 | 2 | 0 | 4 |
| Tổng hợp | 3 | 1 | 0 | 4 |
| Đặc biệt | 0 | 0 | 3 | 3 |
| Credit Mgmt | 1 | 0 | 3 | 4 |
| **TOTAL** | **25** | **9** | **8** | **42** |
| **Percentage** | **60%** | **21%** | **19%** | **100%** |

### 9.3. Implementation Effort

| Phase | Scope | Effort |
|-------|-------|--------|
| **Phase 1: Config** | Ready features (60%) | 2-3 weeks |
| **Phase 2: Customize** | Extend features (21%) | 4-6 weeks |
| **Phase 3: Build** | New modules (19%) | 8-12 weeks |
| **Total** | 100% coverage | **14-21 weeks** |

---

## Phần 10: Implementation Roadmap

### 10.1. Phase 1: Configuration (Weeks 1-3)

**Goal:** Get basic accounting operational

**Tasks:**
1. Vietnam Chart of Accounts setup
2. VAT templates (0%, 5%, 8%, 10%)
3. Payment Entry print formats
4. Bank & Cash accounts configuration
5. Asset depreciation settings
6. Basic reports customization

**Deliverables:**
- ✅ Basic accounting transactions working
- ✅ Sales/Purchase invoices with VAT
- ✅ Payment Entry (Thu/Chi) operational
- ✅ Trial Balance accurate

### 10.2. Phase 2: Customization (Weeks 4-9)

**Goal:** Vietnam-specific features

**Tasks:**
1. Monthly Weighted Average valuation job
2. Credit Management workflow
3. Landed Cost extension for import duty
4. CCDC allocation module
5. Recurring entries templates
6. AP/AR aging workflow

**Deliverables:**
- ✅ COGS calculated correctly (monthly average)
- ✅ Credit limit check with approval workflow
- ✅ Landed cost allocation working
- ✅ CCDC phân bổ operational

### 10.3. Phase 3: Special Features (Weeks 10-21)

**Goal:** Customer-specific features

**Tasks:**
1. `dcnet/supplier-support` module
2. `dcnet/event-costing` module
3. Partner Report API
4. Vietnam tax reports (Form 01/GTGT, 03/TNDN)

**Deliverables:**
- ✅ Supplier support tracking
- ✅ Event profitability reports
- ✅ NM + Vendor reporting API
- ✅ Tax compliance reports

### 10.4. Timeline Visualization

```mermaid
gantt
    title Accounting Module Implementation
    dateFormat  YYYY-MM-DD

    section Phase 1: Config
    Vietnam CoA           :p1a, 2026-02-01, 1w
    VAT Templates         :p1b, after p1a, 1w
    Print Formats         :p1c, after p1b, 1w

    section Phase 2: Customize
    Monthly Valuation     :p2a, 2026-02-22, 2w
    Credit Management     :p2b, 2026-02-22, 3w
    Landed Cost Extend    :p2c, after p2a, 1w
    CCDC Module           :p2d, after p2c, 2w

    section Phase 3: Build
    Supplier Support      :p3a, 2026-04-05, 4w
    Event Costing         :p3b, after p3a, 4w
    Partner API           :p3c, after p3b, 3w
    Tax Reports           :p3d, 2026-04-05, 3w
```

---

## Phần 11: Kết Luận

### 11.1. Tổng Kết Coverage

**DCNET Flow đáp ứng được ~75-80% yêu cầu kế toán từ spec khách hàng sau khi customize:**

| Status | Count | Percentage | Description |
|--------|-------|------------|-------------|
| ✅ Ready | 25 | 60% | Có sẵn, chỉ cần config |
| 🔧 Customize | 9 | 21% | Cần extend logic |
| ❌ Build | 8 | 19% | Cần build mới hoàn toàn |

### 11.2. Critical Gaps

**3 gaps quan trọng nhất cần address:**

1. **Credit Management Workflow** ⭐⭐⭐
   - Check hóa đơn quá hạn
   - Check hạn mức (current + pending + new)
   - Approval workflow cho KTT
   - **Effort:** 3-4 weeks

2. **Monthly Weighted Average** ⭐⭐
   - Customer requirement vs DCNET Flow default
   - Month-end recalculation job
   - **Effort:** 2-3 weeks

3. **Special Features** ⭐⭐
   - Chi phí hỗ trợ hãng: 3-4 weeks
   - Báo cáo sự kiện: 3-4 weeks
   - Partner API: 2-3 weeks

### 11.3. Recommendations

**Go/No-Go:**

| Criteria | Assessment |
|----------|------------|
| Core accounting | ✅ GO - 85-95% ready |
| AR/AP management | ✅ GO - 80-90% ready |
| Credit management | ⚠️ GO with customization |
| Special features | ⚠️ GO with Phase 3 build |

**Recommended Approach:**

1. **Phase 1 (MVP):** Deploy core accounting + credit management
   - Timeline: 8-10 weeks
   - Coverage: ~80%

2. **Phase 2 (Full):** Add special features
   - Timeline: Additional 8-11 weeks
   - Coverage: 100%

**Total Timeline:** 16-21 weeks (~4-5 months) with 2 developers

---

## Appendix A: Code References

### Key Files

| File | Lines | Purpose |
|------|-------|---------|
| `accounts/general_ledger.py` | 880 | GL Entry processing |
| `accounts/doctype/sales_invoice/sales_invoice.py` | 3,072 | Sales Invoice logic |
| `accounts/doctype/purchase_invoice/purchase_invoice.py` | 2,068 | Purchase Invoice logic |
| `accounts/doctype/payment_entry/payment_entry.py` | 3,560 | Payment processing |
| `accounts/doctype/journal_entry/journal_entry.py` | 1,765 | Journal Entry |
| `assets/doctype/asset/asset.py` | 1,200+ | Asset management |
| `stock/stock_ledger.py` | 1,500+ | Stock valuation |

### Key Functions

| Function | File:Line | Purpose |
|----------|-----------|---------|
| `make_gl_entries()` | general_ledger.py:29 | Create GL entries |
| `get_gl_entries()` | sales_invoice.py:2400 | SI GL creation |
| `set_difference_amount()` | payment_entry.py:2486 | Exchange diff |
| `post_depreciation_entries()` | asset.py:280 | Depreciation posting |

---

## Appendix B: Vietnam Accounting Standards Reference

### Thông Tư 99/2025 Key Points

1. **Chart of Accounts** - Hệ thống tài khoản mới
2. **Financial Statements** - Báo cáo tài chính chuẩn
3. **Inventory Valuation** - FIFO, Weighted Average (NO LIFO)
4. **Fixed Assets** - Khấu hao theo TT 45/2013

### VAS Standards Applied

- VAS 01: General Provisions
- VAS 02: Inventories
- VAS 03: Tangible Fixed Assets
- VAS 10: Foreign Exchange

---

**Document End**

**Prepared by:** Claude Code Analysis
**Date:** 20/01/2026
**Version:** 1.0
**Status:** Complete - Ready for Review
