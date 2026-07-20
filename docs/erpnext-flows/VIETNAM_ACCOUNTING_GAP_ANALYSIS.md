# Phân Tích Nghiệp Vụ Kế Toán Việt Nam vs DCNET Flow (ERPNext v16)

**Prepared:** 20/01/2026
**Purpose:** Gap analysis giữa yêu cầu kế toán VN và khả năng ERPNext hiện tại
**Scope:** Toàn bộ nghiệp vụ kế toán theo VAS + Thông tư 99/2025 + Yêu cầu khách hàng

---

## Executive Summary

### Tổng Quan

**ERPNext v16 có coverage 50-60% cho yêu cầu kế toán Việt Nam:**
- ✅ **Mạnh:** Core accounting (85-95%), AR/AP (80-90%), Fixed Assets (85-90%)
- 🔧 **Cần customize:** Vietnam localization, công nợ tracking, giá vốn trung bình tháng
- ❌ **Thiếu hoàn toàn:** 3 tính năng đặc biệt của Nhật Minh Sport

### Key Findings

| Mảng | ERPNext % | Tình trạng | Effort |
|------|-----------|-----------|--------|
| **Core Accounting** | 85-95% | 🟢 Tốt, cần config | 2-3 weeks |
| **Vietnam Localization** | 30% | 🔧 Cần build CoA + Regional | 3-4 weeks |
| **Công nợ Tracking** | 60% | 🔧 Cần mở rộng aging logic | 3-4 weeks |
| **Tính năng đặc biệt** | 0% | ❌ Cần build 3 modules | 7-10 weeks |
| **TỔNG CỘNG** | **50-60%** | 🟡 Nửa sẵn, nửa build | **15-21 weeks** |

### Critical Gaps

1. **CREDIT_MANAGEMENT** - Công nợ theo hạn thanh toán ⭐⭐⭐
   - ERPNext có AR aging report nhưng thiếu workflow approval
   - Cần: Check credit limit khi tạo SO, cảnh báo quá hạn, approval workflow

2. **Vietnam Chart of Accounts** - Hệ thống tài khoản VN ⭐⭐⭐
   - ERPNext không có template CoA cho VN (60+ countries, không có VN)
   - Cần: Build CoA theo Thông tư 99/2025 (1XX-9XX)

3. **Tính năng đặc biệt** - Chi phí hỗ trợ hãng + Báo cáo sự kiện ⭐⭐
   - ERPNext không có concept này
   - Cần: Build 3 custom modules

---

## Phần 1: Yêu Cầu Kế Toán Việt Nam

### 1.1. Khung Pháp Lý (Legal Framework)

#### Luật & Thông tư chính

| Văn bản | Hiệu lực | Nội dung chính |
|---------|----------|----------------|
| **Luật Kế toán 88/2015/QH13** | 01/01/2017 | Nguyên tắc kế toán, trách nhiệm kế toán trưởng |
| **Thông tư 99/2025/TT-BTC** | 01/01/2026 | Chế độ kế toán doanh nghiệp (thay TT 200/2014) |
| **Thông tư 133/2016/TT-BTC** | 01/01/2017 | Chế độ kế toán SME (tùy chọn) |
| **Thông tư 45/2013/TT-BTC** | - | Quản lý TSCĐ & khấu hao |
| **Thông tư 219/2013/TT-BTC** | - | Thuế GTGT |

#### VAS (Vietnamese Accounting Standards)

**26 chuẩn mực kế toán VN** (VAS 01-26), based on IAS circa 2001-2005:
- VAS 01: General Provisions
- VAS 02: Inventories (FIFO, Weighted Avg - NO LIFO)
- VAS 03: Tangible Fixed Assets
- VAS 10: Foreign Exchange
- VAS 25: Consolidated FS
- VAS 26: Related Parties

**Key Differences vs. IFRS:**
- Rules-based (vs. IFRS principles-based)
- Not updated since 2001-2005
- Land = Intangible Asset (not Tangible)
- Goodwill amortized over 10 years (IFRS: impairment only)

### 1.2. Hệ Thống Tài Khoản (Chart of Accounts)

**Theo Thông tư 99/2025 - Appendix II:**

| Class | Code Range | Loại tài khoản |
|-------|------------|----------------|
| **1XX** | 100-199 | Tài sản (Assets) |
| **2XX** | 200-299 | Nợ phải trả (Liabilities) |
| **3XX** | 300-399 | Vốn chủ sở hữu (Equity) |
| **4XX** | 400-499 | Doanh thu (Revenue) |
| **5XX** | 500-599 | Chi phí (Expenses) |
| **6XX** | 600-699 | Giá vốn sản xuất (Cost of Production) |
| **7XX** | 700-799 | Thu nhập/chi phí khác (Other Income/Expense) |
| **8XX** | 800-899 | Ngoại bảng (Off-Balance Sheet) |
| **9XX** | 900-999 | Quản trị (Management Accounts) |

**Tài khoản đặc thù VN:**
- **111** - Tiền mặt
- **112** - Tiền gửi ngân hàng
- **131** - Phải thu khách hàng
- **133** - Thuế GTGT được khấu trừ (VAT input)
- **3331** - Thuế GTGT phải nộp (VAT output)
- **3387** - Quỹ khen thưởng, phúc lợi (Reward & Welfare Fund)

**New in TT 99/2025:**
- DN có thể tự customize CoA (không cần MoF approval)
- Phải duy trì consistency trong fiscal year

### 1.3. Hình Thức Sổ Kế Toán (Accounting Book Forms)

**3 hình thức chính thức:**

#### Form 1: Nhật ký chung (General Journal) ⭐ Most Popular

**Sổ sách:**
- Sổ Nhật ký chung (General Journal)
- Sổ Nhật ký đặc biệt (Special Journals)
- Sổ Cái (General Ledger)
- Sổ/Thẻ chi tiết (Subsidiary Ledgers)

**Workflow:**
1. Ghi tất cả nghiệp vụ vào Nhật ký chung (chronological)
2. Post vào Special Journals by transaction type
3. Post vào General Ledger by account
4. Maintain detailed subsidiary ledgers

#### Form 2: Nhật ký - Chứng từ (Journal-Voucher)

**10 Journal-Vouchers:**
- JV 1: Cash receipts
- JV 2: Cash payments
- JV 3: Bank deposits
- JV 4: Bank withdrawals
- JV 5: Sales invoices
- JV 6: Purchase invoices
- JV 7-10: Other transactions

#### Form 3: Chứng từ ghi sổ (Document-Based)

**Simplified** - for small enterprises

### 1.4. Chứng Từ Kế Toán (Accounting Documents)

**Theo Thông tư 99/2025 - Mandatory vouchers:**

| Chứng từ | Form | Purpose |
|----------|------|---------|
| **Phiếu Thu** | 01-TT | Cash/Bank receipts |
| **Phiếu Chi** | 02-TT | Cash/Bank payments |
| **Báo Nợ** | - | Debit notes (AR/Bank debits) |
| **Báo Có** | - | Credit notes (AP/Bank credits) |

**Requirements:**
- Sequential numbering
- Digital signatures (for e-documents)
- No deletion (reversal only)
- 10-year retention minimum

### 1.5. Phương Pháp Tính Giá Xuất Kho (Inventory Valuation)

**Allowed methods (per VAS 02):**

| Method | Formula | Use Case |
|--------|---------|----------|
| **FIFO** | First-In, First-Out | Standard practice |
| **Weighted Average** | (Beginning + Purchases) / (Qty Beginning + Qty Purchases) | Smooth price fluctuations |
| **Specific Identification** | Actual cost per item | High-value items (vehicles, machinery) |

**PROHIBITED:** ❌ LIFO (Last-In, First-Out) - not allowed in Vietnam

**Customer Requirement:** **Trung bình tháng** (Monthly Weighted Average)

### 1.6. Phương Pháp Khấu Hao TSCĐ (Fixed Asset Depreciation)

**Allowed methods (per TT 45/2013):**

#### Method 1: Đường thẳng (Straight-Line) ⭐ Customer requirement

```
Annual Rate (%) = 1 / Useful Life × 100
Annual Depreciation = Original Cost × Rate
```

**Example:** Asset 100M, 5 years → 20%/year → 20M/year

#### Method 2: Số dư giảm dần (Declining Balance)

**Accelerated depreciation** - higher in early years

**Factors:**
- ≤ 4 years: 1.5x
- 4-6 years: 2.0x
- > 6 years: 2.5x

#### Method 3: Theo sản lượng (Units of Production)

Based on actual usage (km, units produced, etc.)

**Minimum Useful Life (per TT 45):**
- Buildings: 5-50 years
- Machinery: 5-20 years
- Vehicles: 6-10 years
- Computers: 3-5 years

### 1.7. Thuế GTGT (VAT - Value Added Tax)

**4 mức thuế suất:**

| Rate | Applied to |
|------|-----------|
| **0%** | Exports, duty-free, international transport |
| **5%** | Essential goods (agriculture, medical, education, water) |
| **8%** | Temporary reduction (Jul 2025 - Dec 2026) - normally 10% items |
| **10%** | Standard rate (all other goods/services) |

**Input VAT Deduction Rules:**

**20 Million VND Rule:** ⭐ CRITICAL
- Purchases ≥ 20M VND (incl. VAT) → Must have **bank transfer proof**
- Cash payments ≥ 20M → **NO VAT deduction allowed**

**Declaration Frequency:**
- **Monthly:** Revenue > 50B VND/year (deadline: 20th of next month)
- **Quarterly:** Revenue ≤ 50B VND/year (deadline: 30th of next quarter's 1st month)

**Forms:**
- Form 01/GTGT - VAT declaration
- Form 02/GTGT - Input VAT detail

### 1.8. Báo Cáo Tài Chính (Financial Statements)

**4 báo cáo bắt buộc (from 01/01/2026):**

| Report | Form | Old Name |
|--------|------|----------|
| **Báo cáo tình hình tài chính** | B01-DN | Bảng cân đối kế toán (Balance Sheet) |
| **Báo cáo kết quả kinh doanh** | B02-DN | Income Statement (P&L) |
| **Báo cáo lưu chuyển tiền tệ** | B03-DN | Cash Flow Statement |
| **Thuyết minh BCTC** | B09-DN | Notes to Financial Statements |

**Deadline:** March 31 of following year

**Audit Requirement (per NĐ 90/2025):**

Large enterprises must audit if meet **2 of 3 criteria:**
- Employees ≥ 200
- Revenue ≥ 300B VND/year
- Total Assets ≥ 100B VND

---

## Phần 2: Yêu Cầu Khách Hàng (Nhật Minh Sport)

### 2.1. Thông Tin Chung

**From:** `docs/feature/ERP_SPECIFICATION.md` Section 5 (line 643-742)

| Item | Value |
|------|-------|
| **Chế độ kế toán** | Thông tư 99 |
| **Hình thức sổ** | Nhật ký chung |
| **Giá xuất kho** | Trung bình tháng (Monthly Weighted Average) |
| **Đồng tiền** | VND |
| **Đánh giá CLTG** | Theo Thông tư 99 |
| **Khấu hao TSCĐ** | Đường thẳng (Straight-Line) |

### 2.2. Kế Toán Tiền Mặt & Tiền Gửi

**Requirements:**
- ✅ Lập & in Phiếu Thu, Chi, Báo Nợ, Báo Có (theo TT 200/99)
- ✅ Tự động hạch toán chênh lệch tỷ giá ngoại tệ
- ✅ Đánh giá chênh lệch tỷ giá cuối kỳ
- ✅ Theo dõi Quỹ và các tài khoản ngân hàng
- 🔧 Theo dõi **Khế ước** (hợp đồng ngoại tệ) - cần customize

### 2.3. Kế Toán Bán Hàng & Công Nợ Phải Thu

**Requirements:**
- ✅ Lập & in hóa đơn, phiếu hàng bán bị trả lại, phiếu thu tiền
- ⭐ **Theo dõi công nợ theo hạn thanh toán** - CRITICAL
- ✅ Báo cáo tổng hợp, chi tiết công nợ phải thu KH
- ✅ Báo cáo Bảng kê/sổ chi tiết, phân tích bán hàng
- ✅ Tính giá vốn hàng bán trung bình tháng
- ✅ Các báo cáo thuế GTGT

### 2.4. Kế Toán Mua Hàng & Công Nợ Phải Trả

**Requirements:**
- ✅ Lập & in phiếu nhập mua, chi phí vận chuyển, chi trả NCC
- ✅ Phiếu bù trừ công nợ NCC
- ✅ Phiếu thanh toán tạm ứng
- ⭐ **Theo dõi công nợ theo hạn thanh toán** - CRITICAL
- ✅ Theo dõi, hạch toán thuế GTGT, thuế nhập khẩu
- 🔧 **Phân bổ chi phí mua** cho mặt hàng
- 🔧 **Phân bổ chi phí vận chuyển**
- 🔧 **Phân bổ thuế nhập khẩu**
- 🔧 **Bảng đối chiếu công nợ NCC** (reconciliation)
- ✅ Báo cáo chi tiết mua hàng, sổ nhật ký, tổng hợp nhập mua

### 2.5. Kế Toán Hàng Tồn Kho

**Requirements:**
- ✅ Phiếu nhập, xuất, điều chuyển, xuất CCDC
- ✅ Quản lý NXT theo kho, mặt hàng, nhóm hàng
- 🔧 **Tính giá vốn tự động** theo **trung bình tháng**

### 2.6. Kế Toán TSCĐ & CCDC

**TSCĐ Requirements:**
- ✅ Khai báo, quản lý TSCĐ
- ✅ Chi tiết thẻ tài sản, phiếu biến động, biên bản thanh lý
- ✅ Tự động tính & hạch toán khấu hao theo nguồn vốn (straight-line)
- ✅ Báo cáo: Thẻ, sổ, chi tiết, khấu hao, tăng/giảm, tổng hợp, kiểm kê

**CCDC Requirements:**
- 🔧 Theo dõi các lần xuất dùng CCDC
- 🔧 Giá trị phân bổ CCDC vào chi phí
- 🔧 Tính phân bổ giá trị CCDC trong các kỳ khác nhau
- 🔧 Báo cáo: Phân bổ giá trị CCDC, tổng hợp tình hình sử dụng

### 2.7. Kế Toán Tổng Hợp

**Requirements:**
- ✅ Phiếu kế toán khác (manual entry)
- ✅ Phiếu bù trừ công nợ
- ✅ Tạo bút toán chênh lệch tỷ giá tự động
- 🔧 **Các bút toán định kỳ** (recurring)
- 🔧 **Bút toán kết chuyển & phân bổ**
- ✅ Sổ chi tiết tài khoản, sổ tổng hợp
- ✅ Bảng cân đối tài khoản, Nhật ký chung

### 2.8. Tính Năng Đặc Biệt ⭐⭐

#### 2.8.1. Tính Chi Phí Hỗ Trợ Của Hãng

**Purpose:** Ghi nhận & phân bổ chi phí hỗ trợ từ **hãng (vendor)** cho từng sự kiện/chương trình

**Example:**
- Hãng golf cung cấp funding cho:
  - Sự kiện demo gậy mới
  - Marketing event
  - Chương trình training

**Coverage ERPNext:** ❌ 0%
**Status:** CẦN BUILD (`dcnet/supplier-support`)

#### 2.8.2. Báo Cáo Chi Phí Theo Sự Kiện

**Purpose:** Báo cáo chi phí theo khoản mục cho từng sự kiện/vụ việc

**4 loại sự kiện:**
1. **Marketing** - quảng cáo, event marketing
2. **Demo** - sự kiện demo sản phẩm
3. **Bán hàng** - chương trình sale
4. **Sai giá** - xử lý chênh lệch giá

**Calculation:**
```
Chi phí = Tổng chi phí cho sự kiện
Doanh thu = Doanh số từ sự kiện đó
Lợi nhuận = Doanh thu - Chi phí
```

**Coverage ERPNext:** ❌ 0%
**Status:** CẦN BUILD (`dcnet/event-costing`)

#### 2.8.3. Báo Cáo Tổng Hợp cho Nhật Minh + Đại Diện Hãng

**Purpose:** Báo cáo tổng hợp về quản lý hàng hóa

**Đối tượng:**
- Nhật Minh (đại lý cấp 1)
- Đại diện độc quyền hãng tại VN
- Cả 2 bên cùng dùng phần mềm Bravo (hoặc DCNET Flow)

**Nội dung:**
- Nhập/xuất/tồn kho
- Doanh thu/doanh số
- Chi phí hỗ trợ từ hãng
- Chi phí sự kiện
- Báo cáo hiệu suất

**Coverage ERPNext:** ❌ 0%
**Status:** CẦN BUILD (custom report + API sync với vendor)

### 2.9. Quản Lý Công Nợ (CRITICAL)

**From:** `docs/feature/ERP_SPECIFICATION.md` Section 2.7-2.8

#### 2.9.1. Hạn Mức Công Nợ

- Cấu hình **hạn mức công nợ per khách hàng**
- Lưu trữ tài khoản công nợ
- Accrual account tracking

**Coverage ERPNext:** 85% (Credit Limit có sẵn, cần customize)

#### 2.9.2. Kiểm Tra Công Nợ Quá Hạn ⭐⭐⭐

**Báo cáo công nợ quá hạn (aging):**
- 0-30 ngày
- 31-60 ngày
- 61-90 ngày
- 90+ ngày

**Cảnh báo tự động khi:**
- Có hóa đơn quá hạn
- Công nợ vượt hạn mức

**Điều kiện xuất hàng hợp lệ:**
1. KH không có hóa đơn quá hạn
2. Công nợ hiện tại + các lệnh xuất đã duyệt + lệnh xuất hiện tại ≤ hạn mức

**Xử lý ngoại lệ:**
- Nếu vượt 2 điều kiện → **Kế toán trưởng** phải **xác nhận**

**Coverage ERPNext:** ❌ 0% (cần workflow custom)
**Status:** CẦN BUILD (`dcnet/credit-management`)

---

## Phần 3: ERPNext v16 Accounting Capabilities

### 3.1. Core Accounting Features (85-95% Coverage)

**From:** Agent analysis of `dcnet_core/erpnext/accounts/`

#### 3.1.1. Chart of Accounts

**DocType:** Account

**Features:**
- ✅ Hierarchical structure (NestedSet)
- ✅ Account types: Asset, Liability, Income, Expense, Equity
- ✅ 31 sub-types (Bank, Cash, Current Asset, COGS, Tax, Receivable, Payable, etc.)
- ✅ Multi-currency support per account
- ✅ Balance constraint (Debit/Credit enforcement)
- ✅ Account numbers support
- ✅ Freeze account capability
- ✅ Group vs Ledger hierarchy

**Gap:** ❌ No Vietnam CoA template (60+ countries, NO Vietnam)

#### 3.1.2. Journal Entry & GL

**DocTypes:** Journal Entry, GL Entry

**Features:**
- ✅ Multi-currency support
- ✅ 18 voucher types (Journal Entry, Bank Entry, Cash Entry, Opening Entry, etc.)
- ✅ Tax withholding integration
- ✅ Template support for recurring entries
- ✅ Auto-repeat capability
- ✅ Cost center & project allocation
- ✅ Finance book support
- ✅ Accounting dimensions

**Match Vietnam:** ✅ Nhật ký chung (General Journal) - 90% coverage

#### 3.1.3. Period Closing

**DocTypes:** Fiscal Year, Accounting Period, Period Closing Voucher

**Features:**
- ✅ Multi-company fiscal year
- ✅ Intra-year period divisions
- ✅ Automated closing workflow

**Match Vietnam:** ✅ Calendar year (Jan 1 - Dec 31) - 100% coverage

### 3.2. AR/AP Management (80-90% Coverage)

#### 3.2.1. Sales Invoice (AR)

**DocType:** Sales Invoice

**Features:**
- ✅ Item-based invoicing with multi-currency
- ✅ Tax integration (Sales Taxes and Charges)
- ✅ Advance payment allocation
- ✅ Payment schedule (Payment Terms)
- ✅ Customer discount tracking
- ✅ Multi-mode payment support
- ✅ Delivery note linkage

**Match Vietnam:** ✅ Hóa đơn bán hàng - 90% coverage

#### 3.2.2. Purchase Invoice (AP)

**DocType:** Purchase Invoice

**Features:**
- ✅ Supplier-based invoicing
- ✅ GRN linkage
- ✅ Expense account support
- ✅ Advance payment integration

**Match Vietnam:** ✅ Hóa đơn mua hàng - 90% coverage

#### 3.2.3. AR/AP Tracking

**DocTypes:** Payment Terms Template, Party Account

**Reports:**
- ✅ Accounts Receivable (customer aging)
- ✅ Accounts Receivable Summary
- ✅ Accounts Payable (supplier aging)
- ✅ Accounts Payable Summary

**Gap:** 🔧 Aging report có sẵn nhưng thiếu **workflow approval** khi vượt hạn

### 3.3. Payment Management (85-90% Coverage)

#### 3.3.1. Payment Entry

**DocType:** Payment Entry

**Features:**
- ✅ Centralized payment processing
- ✅ Payment modes (Cash, Bank, Credit Card)
- ✅ Multi-currency payment
- ✅ Exchange gain/loss calculation
- ✅ Tax withholding support
- ✅ Bank account selection
- ✅ Clearance date tracking
- ✅ Payment deductions
- ✅ Invoice linking

**Match Vietnam:** ✅ Phiếu Thu/Chi - 90% coverage

#### 3.3.2. Bank & Cash

**DocTypes:** Bank, Bank Account, Bank Reconciliation Tool, Bank Transaction

**Features:**
- ✅ Bank master data
- ✅ Company bank accounts
- ✅ Automated bank reconciliation UI
- ✅ Bank statement import
- ✅ Auto-allocation to invoices
- ✅ Cheque management

**Match Vietnam:** ✅ Quản lý ngân hàng - 90% coverage

**Gap:** 🔧 Thiếu **20M VND rule** (VAT deduction based on payment method)

### 3.4. Tax Management (85% Coverage)

#### 3.4.1. VAT Configuration

**DocTypes:** Sales/Purchase Taxes and Charges Template, Tax Category

**Features:**
- ✅ Multi-rate tax configuration
- ✅ Percentage/fixed amount
- ✅ Accounting head mapping
- ✅ Customer/Supplier group applicability

**Vietnam Tax Setup (Found):**
```json
"Vietnam": {
    "Vietnam Tax": {
        "account_name": "VAT",
        "tax_rate": 10.00
    }
}
```

**Gap:** 🔧 Only 10% configured, missing 0%, 5%, 8%

#### 3.4.2. Tax Withholding (TDS)

**DocTypes:** Tax Withholding Category, Tax Withholding Rate, Tax Withholding Entry

**Features:**
- ✅ TDS category master
- ✅ Threshold amounts
- ✅ TDS calculation & deduction
- ✅ Integration with invoices & payments

**Match Vietnam:** ✅ Applicable for PIT/CIT withholding

### 3.5. Inventory Valuation (70-95% Coverage)

**From:** Agent analysis - ERPNext Inventory module

**Supported Methods:**
- ✅ FIFO (First-In, First-Out)
- ✅ Moving Average (perpetual)
- ❌ NO LIFO (good - aligns with Vietnam)
- 🔧 **Weighted Average Monthly** - cần config

**Gap:** 🔧 ERPNext has **Moving Average** (perpetual), customer wants **Monthly Weighted Average**

**Solution:** Configure monthly job to recalculate COGS at period end

### 3.6. Fixed Asset Management (85-90% Coverage)

#### 3.6.1. Asset Tracking

**DocTypes:** Asset, Asset Category, Asset Depreciation Schedule

**Features:**
- ✅ Asset master data
- ✅ Depreciation Entry posting
- ✅ Asset Disposal entries
- ✅ Depreciation schedule
- ✅ Multiple depreciation methods

**Match Vietnam:** ✅ TSCĐ tracking - 90% coverage

#### 3.6.2. Depreciation Methods

**Supported:**
- ✅ Straight-Line Method (khấu hao đường thẳng)
- ✅ Declining Balance (số dư giảm dần)
- ✅ Manual depreciation

**Match Vietnam:** ✅ Customer requirement (Straight-Line) - 100% coverage

**Gap:** 🔧 CCDC (công cụ dụng cụ) phân bổ - cần extend logic

### 3.7. Cost Accounting (80-90% Coverage)

**DocTypes:** Cost Center, Accounting Dimension

**Features:**
- ✅ Hierarchical cost centers
- ✅ GL entry allocation
- ✅ Budget allocation
- ✅ Custom dimensions (beyond Cost Center/Project)
- ✅ Project-wise profitability

**Match Vietnam:** ✅ Cost tracking - 85% coverage

### 3.8. Financial Reporting (85% Coverage)

#### 3.8.1. Built-in Reports (52 reports total)

**Core Financial Statements:**
- ✅ Balance Sheet (Standard IFRS)
- ✅ Profit and Loss Statement (P&L)
- ✅ Trial Balance (detailed, simple, consolidated)
- ✅ Cash Flow Statement
- ✅ Financial Ratios

**AR/AP Reports:**
- ✅ General Ledger
- ✅ Accounts Receivable/Payable (aging)
- ✅ Customer/Supplier Ledger Summary

**Bank & Cash:**
- ✅ Bank Reconciliation Statement
- ✅ Bank Clearance Summary

**Sales & Purchase:**
- ✅ Sales/Purchase Register
- ✅ Item Wise Sales/Purchase Register
- ✅ Gross Profit Report

**Tax Reports:**
- ✅ Tax Withholding Details

**Gap:** 🔧 Missing **Vietnam-specific reports**:
- ❌ VAT declaration (Tờ khai VAT - Form 01/GTGT)
- ❌ Corporate tax report (Form 03/TNDN)
- ❌ Báo cáo tình hình tài chính (Form B01-DN per TT 99)

### 3.9. Multi-Currency & Exchange Rate (85-90% Coverage)

**DocTypes:** Exchange Rate Revaluation, Currency Exchange Settings

**Features:**
- ✅ Multi-currency invoices
- ✅ Exchange gain/loss posting
- ✅ Unrealized gain/loss on FX accounts
- ✅ Rounding loss allowance
- ✅ Fuzzy matching for reconciliation

**Match Vietnam:** ✅ Chênh lệch tỷ giá - 85% coverage

### 3.10. Advanced Features (70-90% Coverage)

**Available:**
- ✅ Invoice Discounting/Factoring
- ✅ Dunning (Collections)
- ✅ Payment Reconciliation
- ✅ Subscription billing
- ✅ POS Invoice
- ✅ Loyalty Program
- ✅ Deferred Revenue/Expense
- ✅ Budget vs Actual
- ✅ Consolidated Financial Statements

**Match Vietnam:** ✅ Advanced features - 80% coverage

---

## Phần 4: Gap Analysis - ERPNext vs Vietnam Requirements

### 4.1. Summary Table

| Requirement | ERPNext | Coverage | Status | Effort |
|-------------|---------|----------|--------|--------|
| **1. Chart of Accounts VN** | No template | 0% | ❌ Cần build | 2-3 weeks |
| **2. Accounting Book Forms** | General Journal ✅ | 90% | ✅ Tốt | Config only |
| **3. Accounting Documents** | Payment Entry ✅ | 90% | ✅ Tốt | Customize templates |
| **4. Inventory Valuation** | Moving Avg ✅ | 70% | 🔧 Cần config | 1-2 weeks |
| **5. Fixed Asset** | Straight-Line ✅ | 90% | ✅ Tốt | Config only |
| **6. VAT Management** | Multi-rate ✅ | 70% | 🔧 Cần config | 1 week |
| **7. Financial Statements** | IFRS reports ✅ | 70% | 🔧 Cần VN templates | 2-3 weeks |
| **8. Công nợ Tracking** | Aging report ✅ | 60% | 🔧 Cần workflow | 3-4 weeks |
| **9. 20M VND Rule** | No concept | 0% | ❌ Cần build | 1-2 weeks |
| **10. Chi phí hỗ trợ hãng** | No concept | 0% | ❌ Cần build | 3-4 weeks |
| **11. Báo cáo sự kiện** | No concept | 0% | ❌ Cần build | 3-4 weeks |
| **12. Báo cáo NM+Hãng** | No concept | 0% | ❌ Cần build | 2-3 weeks |
| **TỔNG CỘNG** | - | **50-60%** | 🟡 Nửa sẵn | **19-29 weeks** |

### 4.2. Detailed Gap Analysis by Module

#### 4.2.1. Kế Toán Tiền Mặt/Gửi (85-90% Coverage)

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Phiếu Thu/Chi | ✅ Payment Entry | 10% templates | Customize print formats |
| Báo Nợ/Báo Có | ✅ Journal Entry | 10% templates | Customize print formats |
| Chênh lệch tỷ giá | ✅ Exchange Gain/Loss | 5% auto-posting | Configure posting rules |
| Quỹ & Ngân hàng | ✅ Bank Account | 0% | No gap |
| **Theo dõi khế ước** | ❌ No concept | 50% | **Build custom DocType** |

**Effort:** 1-2 weeks (mainly templates + khế ước tracking)

#### 4.2.2. Kế Toán Bán Hàng/CN Thu (60-90% Coverage)

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Hóa đơn bán | ✅ Sales Invoice | 0% | No gap |
| Phiếu hàng trả lại | ✅ Sales Return | 0% | No gap |
| Phiếu thu tiền | ✅ Payment Entry | 0% | No gap |
| **CN theo hạn TT** | ✅ Aging report | 40% workflow | **Build approval workflow** |
| Báo cáo CN KH | ✅ AR reports | 10% | Customize reports |
| Phân tích bán hàng | ✅ Sales Register | 10% | Customize reports |
| Giá vốn TB tháng | 🔧 Moving Avg | 30% | **Monthly job to recalc** |
| Báo cáo VAT | ✅ Tax reports | 30% | **Build Form 01/GTGT** |

**Effort:** 3-4 weeks (CN workflow + VAT forms)

#### 4.2.3. Kế Toán Mua Hàng/CN Trả (60-90% Coverage)

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Phiếu nhập mua | ✅ Purchase Invoice | 0% | No gap |
| Chi phí vận chuyển | ✅ Landed Cost Voucher | 10% | Configure |
| Phiếu chi trả NCC | ✅ Payment Entry | 0% | No gap |
| Bù trừ CN NCC | ✅ Payment Reconciliation | 10% | Customize |
| Thanh toán tạm ứng | ✅ Advance Payment | 0% | No gap |
| **CN theo hạn TT** | ✅ Aging report | 40% workflow | **Build approval workflow** |
| Thuế GTGT, NK | ✅ Tax tracking | 10% | Configure tax heads |
| **Phân bổ CP mua** | 🔧 Landed Cost | 40% | **Extend logic** |
| **Phân bổ vận chuyển** | 🔧 Landed Cost | 40% | **Extend logic** |
| **Phân bổ thuế NK** | 🔧 Landed Cost | 40% | **Extend logic** |
| **Đối chiếu CN NCC** | 🔧 Reconciliation | 30% | **Build detailed view** |
| Báo cáo mua hàng | ✅ Purchase Register | 10% | Customize |

**Effort:** 3-4 weeks (phân bổ logic + đối chiếu CN)

#### 4.2.4. Kế Toán Tồn Kho (70-95% Coverage)

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Phiếu nhập/xuất | ✅ Stock Entry | 0% | No gap |
| Phiếu điều chuyển | ✅ Stock Transfer | 0% | No gap |
| Phiếu xuất CCDC | ✅ Material Issue | 10% | Customize |
| NXT theo kho | ✅ Stock Ledger | 0% | No gap |
| NXT theo mặt hàng | ✅ Stock Balance | 0% | No gap |
| **Giá vốn TB tháng** | 🔧 Moving Avg | 30% | **Monthly recalc job** |

**Effort:** 1-2 weeks (giá vốn monthly)

#### 4.2.5. Kế Toán TSCĐ/CCDC (60-90% Coverage)

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Khai báo TSCĐ | ✅ Asset | 0% | No gap |
| Thẻ tài sản | ✅ Asset card | 0% | No gap |
| Biến động TS | ✅ Asset Movement | 10% | Customize |
| Thanh lý TS | ✅ Asset Disposal | 10% | Customize |
| Khấu hao đường thẳng | ✅ Straight-Line | 0% | No gap |
| Báo cáo TSCĐ | ✅ Asset reports | 10% | Customize |
| **Xuất dùng CCDC** | ❌ No concept | 40% | **Build tracking** |
| **Phân bổ CCDC** | ❌ No concept | 40% | **Extend deferred logic** |
| **Báo cáo CCDC** | ❌ No concept | 40% | **Build reports** |

**Effort:** 2-3 weeks (CCDC phân bổ)

#### 4.2.6. Kế Toán Tổng Hợp (70-90% Coverage)

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Phiếu KT khác | ✅ Journal Entry | 0% | No gap |
| Bù trừ CN | ✅ Payment Reconciliation | 10% | Customize |
| Chênh lệch TG tự động | ✅ Exchange Revaluation | 10% | Configure |
| **Bút toán định kỳ** | 🔧 Auto Repeat | 30% | **Extend templates** |
| **Kết chuyển & phân bổ** | 🔧 Period Closing | 30% | **Build automation** |
| Sổ chi tiết TK | ✅ Account Ledger | 0% | No gap |
| Sổ tổng hợp TK | ✅ General Ledger | 0% | No gap |
| Bảng cân đối TK | ✅ Trial Balance | 0% | No gap |
| Nhật ký chung | ✅ General Journal | 0% | No gap |

**Effort:** 2-3 weeks (recurring entries + period close automation)

#### 4.2.7. Tính Năng Đặc Biệt (0% Coverage) ⭐⭐

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| **Chi phí hỗ trợ hãng** | ❌ No concept | 100% | **Build `dcnet/supplier-support`** |
| **Báo cáo sự kiện** | ❌ No concept | 100% | **Build `dcnet/event-costing`** |
| **Báo cáo NM+Hãng** | ❌ No concept | 100% | **Build custom reports + API** |

**Modules to Build:**

**1. dcnet/supplier-support** (3-4 weeks)
- DocType: Supplier Support Event
- Track vendor funding per event/campaign
- Allocation to cost centers
- Reports: Support by vendor, by event, by period

**2. dcnet/event-costing** (3-4 weeks)
- DocType: Event Costing
- Event types: Marketing, Demo, Sales, Pricing Error
- Cost allocation from GL
- Revenue tracking from Sales
- ROI calculation: Profit = Revenue - Cost
- Reports: Profitability by event type

**3. Partner Report API** (2-3 weeks)
- Custom report aggregation
- API endpoint for vendor access
- Data sync with Bravo (if needed)
- Security: Partner-specific data filtering

**Effort:** 8-11 weeks total

#### 4.2.8. Quản Lý Công Nợ (0-85% Coverage) ⭐⭐⭐

| Feature | ERPNext | Gap | Solution |
|---------|---------|-----|----------|
| Hạn mức CN per KH | ✅ Credit Limit | 15% | Configure + customize |
| **Aging report** | ✅ AR Aging | 0% | No gap |
| **Cảnh báo quá hạn** | ❌ No auto-alert | 100% | **Build notification system** |
| **Check CN khi tạo SO** | 🔧 Basic check | 60% | **Build complex logic** |
| **Approval workflow** | ❌ No workflow | 100% | **Build manager approval** |
| Credit hold flag | ✅ On Hold status | 0% | No gap |

**Module: dcnet/credit-management** (3-4 weeks)

**Features:**
- Enhanced credit limit check:
  - Current outstanding
  - Pending delivery orders (approved but not shipped)
  - Current Sales Order
  - Total ≤ Credit Limit
- Overdue invoice check (any invoice > payment terms → block)
- Manager approval workflow (if exceed conditions)
- Auto-notification:
  - Customer: approaching limit (90%)
  - Sales: customer on hold
  - Finance: overdue invoices
- Dashboard: Credit utilization by customer

**Effort:** 3-4 weeks

---

## Phần 5: Vietnam Localization Status

### 5.1. Current Localization (30% Coverage)

**From:** Agent analysis of `dcnet_core/erpnext/` and `dcnet_apps/`

#### 5.1.1. What's Already Done ✅

**Currency Setup (100%):**
```python
# dcnet_apps/install.py
frappe.db.set_single_value("FCRM Settings", "currency", "VND")
```
- Locks system to VND (single-currency mode)
- Prevents exchange rate API errors

**Fiscal Year Auto-Setup (100%):**
```python
# Auto-creates calendar year (Jan 1 - Dec 31)
```
- Matches Vietnam fiscal year

**Vietnamese Translations (100%):**
- ERPNext: 56,980 lines (vi.po)
- Frappe CRM: 6,875 lines
- Custom Frappe: 32,292 lines
- **Total: 96,147 lines** of Vietnamese UI

**System Language:**
```python
frappe.db.set_single_value("System Settings", "language", "vi")
```

#### 5.1.2. What's Missing ❌

**Chart of Accounts Template (0%):**
- ERPNext has 60+ country templates (AU, SG, TW, TH, etc.)
- **NO Vietnam template**
- Missing: `dcnet_core/erpnext/accounts/doctype/account/chart_of_accounts/vn_standard.json`

**Regional Module (0%):**
- ERPNext has regional modules: US, AU, UAE, IT, ZA, TR
- **NO `erpnext/regional/vietnam/`**
- Missing:
  - VAT Settings DocType
  - E-tax integration
  - Tax authority compliance

**Tax Configuration (30%):**
- Basic config found:
  ```json
  "Vietnam": {
      "Vietnam Tax": {
          "account_name": "VAT",
          "tax_rate": 10.00
      }
  }
  ```
- Missing: 0%, 5%, 8% rates
- Missing: Tax templates for different scenarios

**Financial Reports (0%):**
- No Vietnam-specific report formats
- Missing:
  - Form B01-DN (Financial Position per TT 99)
  - Form B02-DN (Income Statement per TT 99)
  - Form 01/GTGT (VAT Declaration)
  - Form 03/TNDN (Corporate Income Tax)

### 5.2. Localization Build Plan (3-4 weeks)

#### Phase 1: Chart of Accounts (1-2 weeks)

**Build:** `dcnet_apps/accounting/chart_of_accounts/vietnam_standard.json`

**Structure:**
```json
{
  "name": "Vietnam - Standard Chart of Accounts (TT 99/2025)",
  "country": "Vietnam",
  "tree": {
    "100 - TÀI SẢN": {
      "111 - Tiền mặt": {...},
      "112 - Tiền gửi ngân hàng": {...},
      "131 - Phải thu khách hàng": {...},
      "133 - Thuế GTGT được khấu trừ": {...},
      "152 - Nguyên liệu, vật liệu": {...},
      ...
    },
    "200 - NỢ PHẢI TRẢ": {...},
    "300 - VỐN CHỦ SỞ HỮU": {...},
    "400 - DOANH THU": {...},
    "500 - CHI PHÍ": {...}
  }
}
```

**Accounts to include:**
- All standard accounts from TT 99 Appendix II
- Vietnam-specific accounts (138, 244, 3387, 421, etc.)
- Tax accounts (133, 3331, 3334)

#### Phase 2: Regional Module (2-3 weeks)

**Build:** `dcnet_apps/accounting/vietnam/`

**Files:**
```
vietnam/
├── __init__.py
├── setup.py                    # Auto-setup on install
├── utils.py                    # Business logic
├── doctype/
│   ├── vietnam_vat_settings/   # VAT configuration
│   └── vietnam_tax_report/     # Tax report generator
└── report/
    ├── form_01_gtgt/           # VAT Declaration
    └── form_03_tndn/           # CIT Return
```

**setup.py:**
- Auto-create VAT accounts (133, 3331)
- Configure tax templates (0%, 5%, 8%, 10%)
- Set default CoA to Vietnam Standard

**vietnam_vat_settings DocType:**
```python
Fields:
- company
- vat_rate_standard (default: 10%)
- vat_rate_reduced (default: 5%)
- vat_rate_temporary (default: 8%)
- vat_rate_export (default: 0%)
- bank_payment_threshold (default: 20,000,000 VND)
- enable_20m_rule (checkbox)
```

**utils.py - 20M VND Rule:**
```python
def validate_vat_deduction(payment_entry):
    """
    If payment amount >= 20M VND and mode = Cash:
        Do not allow input VAT deduction
    """
    if payment_entry.mode_of_payment == "Cash":
        if payment_entry.paid_amount >= 20000000:
            # Reverse input VAT if exists
            frappe.throw("Cannot claim VAT deduction for cash payments >= 20M VND")
```

#### Phase 3: Financial Reports (1-2 weeks)

**Build:** Vietnam-format financial statements

**Report 1: Form B01-DN (Financial Position)**
- Based on ERPNext Balance Sheet
- Customize groupings per TT 99 format
- Add VN-specific line items

**Report 2: Form B02-DN (Income Statement)**
- Based on ERPNext P&L
- Restructure per TT 99 format

**Report 3: Form 01/GTGT (VAT Declaration)**
- Custom report pulling from GL
- Input VAT (133)
- Output VAT (3331)
- Net VAT payable/refundable

**Report 4: Form 03/TNDN (CIT Return)**
- Accounting profit from P&L
- Tax adjustments table
- Taxable income calculation

---

## Phần 6: Implementation Roadmap

### 6.1. Phase Breakdown

#### **Phase 1: Vietnam Localization (3-4 weeks)**

**Deliverables:**
1. Chart of Accounts Vietnam Standard
2. Regional module `dcnet_apps/accounting/vietnam/`
3. VAT configuration (0%, 5%, 8%, 10%)
4. Basic financial reports (B01, B02)

**Effort:** 1 developer, 3-4 weeks

#### **Phase 2: Core Accounting Extensions (4-5 weeks)**

**Deliverables:**
1. Monthly Weighted Average inventory valuation
2. CCDC (công cụ dụng cụ) phân bổ logic
3. Recurring entry templates
4. Phân bổ chi phí mua/vận chuyển/thuế NK
5. Đối chiếu công nợ NCC enhancements

**Effort:** 1-2 developers, 4-5 weeks

#### **Phase 3: Credit Management (3-4 weeks)** ⭐⭐⭐

**Deliverables:**
1. Enhanced credit limit check (current + pending + new ≤ limit)
2. Overdue invoice check workflow
3. Manager approval workflow
4. Auto-notifications (customer, sales, finance)
5. Credit utilization dashboard

**Module:** `dcnet/credit-management`

**Effort:** 1 developer, 3-4 weeks

#### **Phase 4: Special Features (8-11 weeks)** ⭐⭐

**Deliverables:**
1. `dcnet/supplier-support` - Chi phí hỗ trợ hãng (3-4 weeks)
2. `dcnet/event-costing` - Báo cáo sự kiện (3-4 weeks)
3. Partner Report API - Báo cáo NM+Hãng (2-3 weeks)

**Effort:** 1-2 developers, 8-11 weeks

#### **Phase 5: Tax Compliance (2-3 weeks)**

**Deliverables:**
1. Form 01/GTGT - VAT Declaration
2. Form 03/TNDN - CIT Return
3. 20M VND rule automation (VAT deduction block)
4. Tax deadline reminders

**Effort:** 1 developer, 2-3 weeks

### 6.2. Total Timeline

**Sequential Execution:**
- Phase 1: Weeks 1-4 (Localization)
- Phase 2: Weeks 5-9 (Core Extensions)
- Phase 3: Weeks 10-13 (Credit Management)
- Phase 4: Weeks 14-24 (Special Features)
- Phase 5: Weeks 25-27 (Tax Compliance)

**Total: 27 weeks (~6.5 months)** with 1-2 developers

**Parallel Execution (Recommended):**
- Track 1 (Developer 1): Phase 1 → Phase 2 → Phase 5 (9-12 weeks)
- Track 2 (Developer 2): Phase 3 → Phase 4 (11-15 weeks)

**Total: 15 weeks (~3.5 months)** with 2 developers

### 6.3. Resource Allocation

**Team Composition:**
- **1x Senior Developer** - ERPNext expert, Vietnam accounting knowledge
- **1x Mid Developer** - Python/Frappe framework
- **1x QA** - Testing & validation
- **1x Accountant** - Domain expert for validation

**External Support:**
- Tax consultant (for Form 01/03 validation)
- Audit firm (for compliance review)

---

## Phần 7: Recommendations

### 7.1. Priority Matrix

| Priority | Module | Reason | Effort |
|----------|--------|--------|--------|
| **P0** | Vietnam CoA | Foundation cho tất cả accounting | 1-2 weeks |
| **P0** | VAT Configuration | Legal compliance (0%, 5%, 8%, 10%) | 1 week |
| **P0** | Credit Management | CRITICAL per customer (risk control) | 3-4 weeks |
| **P1** | Monthly Weighted Avg | Customer requirement (giá vốn) | 1-2 weeks |
| **P1** | Financial Reports | Legal compliance (B01, B02) | 2-3 weeks |
| **P1** | Supplier Support | Customer special feature | 3-4 weeks |
| **P2** | Event Costing | Customer special feature | 3-4 weeks |
| **P2** | CCDC Allocation | Nice to have | 2-3 weeks |
| **P2** | Tax Reports | Legal compliance (Form 01, 03) | 2-3 weeks |
| **P3** | Partner API | Nice to have | 2-3 weeks |

### 7.2. Quick Wins (1-2 weeks)

These can be delivered fast for early customer value:

1. **Vietnam CoA Template** (1 week)
   - Build JSON file with standard Vietnam accounts
   - Immediate value: Proper account structure

2. **VAT Multi-Rate Setup** (1 week)
   - Configure 0%, 5%, 8%, 10% tax templates
   - Immediate value: Correct VAT calculation

3. **Print Templates** (1 week)
   - Phiếu Thu/Chi customized to Vietnam format
   - Immediate value: Professional documents

4. **Vietnamese UI** (Already done ✅)
   - 96K+ lines of translations
   - Immediate value: User-friendly interface

### 7.3. Risk Mitigation

**Risk 1: Monthly Weighted Average complexity**
- **Mitigation:** Start with Moving Average (ERPNext default), then enhance with monthly job
- **Fallback:** Use FIFO if weighted average proves too complex

**Risk 2: 20M VND rule enforcement**
- **Mitigation:** Implement as warning first (soft block), then hard block after testing
- **Fallback:** Manual process with training

**Risk 3: Credit Management workflow adoption**
- **Mitigation:** Phase 1 = automated alerts only, Phase 2 = hard blocks with approval
- **Fallback:** Manual credit check by finance team

**Risk 4: Special features (Supplier Support, Event Costing) scope creep**
- **Mitigation:** Define MVP clearly, use agile sprints, weekly demos to customer
- **Fallback:** Defer advanced features to Phase 2

### 7.4. Success Criteria

**MVP Success (Phase 1-2 complete):**
- ✅ Vietnam CoA installed and active
- ✅ VAT 0%, 5%, 8%, 10% configured and tested
- ✅ Sales/Purchase invoices with correct VAT
- ✅ Monthly Weighted Average valuation working
- ✅ Basic financial reports (B01, B02)

**Phase 1 Complete:**
- ✅ All MVP + Credit Management module
- ✅ Credit limit checks on SO creation
- ✅ Overdue invoice blocking
- ✅ Manager approval workflow

**Full Launch:**
- ✅ All special features (Supplier Support, Event Costing)
- ✅ Tax compliance (Form 01/GTGT, 03/TNDN)
- ✅ Partner API for vendor reporting
- ✅ User training completed
- ✅ Accounting team sign-off

---

## Phần 8: Verification & Testing

### 8.1. Unit Testing

**Vietnam CoA:**
- Test account hierarchy (parent-child)
- Validate account types (Asset, Liability, etc.)
- Ensure tax accounts exist (133, 3331, 3334)

**VAT Calculation:**
- Test 0% for exports
- Test 5% for essential goods
- Test 8% for temporary reduction
- Test 10% for standard
- Test Input VAT deduction
- **Test 20M VND rule** (cash payment block)

**Inventory Valuation:**
- Test monthly weighted average calculation
- Compare with manual calculation
- Test period-end closing
- Verify COGS accuracy

**Credit Management:**
- Test credit limit check (current + pending + new)
- Test overdue invoice detection
- Test approval workflow
- Test notifications

### 8.2. Integration Testing

**End-to-End Sales Flow:**
1. Create Customer with credit limit
2. Create Sales Order (check credit)
3. Create Delivery Note
4. Create Sales Invoice (VAT 10%)
5. Create Payment Entry (bank transfer if >= 20M)
6. Verify VAT deduction allowed
7. Check aging report

**End-to-End Purchase Flow:**
1. Create Supplier
2. Create Purchase Order
3. Create Purchase Receipt
4. Create Purchase Invoice (VAT 10% + import duty)
5. Landed Cost Voucher (phân bổ chi phí)
6. Payment Entry (bank transfer if >= 20M)
7. Verify AP aging

**Period-End Close:**
1. Run monthly weighted average job
2. Post depreciation entries
3. Exchange rate revaluation
4. Generate financial statements (B01, B02)
5. Verify Trial Balance balances

### 8.3. User Acceptance Testing (UAT)

**Participants:**
- Chief Accountant (Kế toán trưởng)
- AR/AP Accountants
- Inventory Accountant
- Tax Accountant

**Test Scenarios:**
1. **Daily Operations** (2 weeks)
   - Enter 100+ real transactions
   - Generate invoices, payments, receipts
   - Check accuracy vs. manual calculation

2. **Month-End Close** (1 week)
   - Close period
   - Generate all reports
   - Validate against prior system (Bravo)

3. **Tax Filing** (1 week)
   - Generate Form 01/GTGT
   - Verify VAT amounts
   - Submit test filing

4. **Credit Management** (1 week)
   - Test various credit limit scenarios
   - Trigger overdue workflow
   - Validate notifications

**Sign-off Criteria:**
- 100% of test cases passed
- No P0/P1 bugs
- Performance acceptable (reports < 5 seconds)
- User satisfaction score > 4/5

---

## Phần 9: Summary - Chức Năng Có Thể Đáp Ứng vs Cần Custom

### 9.1. ✅ CÓ THỂ ĐÁP ỨNG NGAY (85-95% coverage)

**Core Accounting:**
- ✅ Double-entry bookkeeping
- ✅ Multi-company accounting
- ✅ General Journal (Nhật ký chung)
- ✅ General Ledger (Sổ Cái)
- ✅ Journal Entry (Phiếu kế toán)
- ✅ Trial Balance (Bảng cân đối tài khoản)
- ✅ Fiscal Year management
- ✅ Period closing

**AR/AP:**
- ✅ Sales Invoice (Hóa đơn bán)
- ✅ Purchase Invoice (Hóa đơn mua)
- ✅ Payment Entry (Phiếu Thu/Chi)
- ✅ Customer/Supplier Ledger
- ✅ Aging Reports (công nợ quá hạn)
- ✅ Payment Terms
- ✅ Credit Limit (basic)

**Bank & Cash:**
- ✅ Bank Account management
- ✅ Bank Reconciliation
- ✅ Bank Statement Import
- ✅ Cheque management
- ✅ Multi-currency support
- ✅ Exchange gain/loss

**Tax:**
- ✅ Multi-rate VAT
- ✅ Tax withholding (TDS)
- ✅ Tax on purchase/sale

**Inventory:**
- ✅ Stock Entry (Phiếu nhập/xuất)
- ✅ Stock Transfer (Điều chuyển)
- ✅ Stock Ledger (NXT theo kho)
- ✅ Stock Balance (NXT theo mặt hàng)
- ✅ FIFO valuation
- ✅ Moving Average valuation

**Fixed Assets:**
- ✅ Asset management (TSCĐ)
- ✅ Asset card (Thẻ tài sản)
- ✅ Straight-Line depreciation
- ✅ Declining Balance depreciation
- ✅ Asset Disposal
- ✅ Asset reports

**Financial Reporting:**
- ✅ Balance Sheet
- ✅ Income Statement (P&L)
- ✅ Cash Flow Statement
- ✅ Trial Balance
- ✅ General Ledger report
- ✅ 52 built-in reports

**Advanced:**
- ✅ Cost Center tracking
- ✅ Project costing
- ✅ Budget vs Actual
- ✅ Deferred Revenue/Expense
- ✅ Consolidated FS

### 9.2. 🔧 CẦN CUSTOMIZE (60-70% coverage, cần config/extend)

**Vietnam Localization:**
- 🔧 Chart of Accounts Vietnam Standard (cần build JSON)
- 🔧 VAT 0%, 5%, 8% configuration (10% đã có)
- 🔧 Financial reports format Vietnam (B01, B02 per TT 99)
- 🔧 Print templates Vietnam (Phiếu Thu/Chi format)

**Accounting Practices:**
- 🔧 Monthly Weighted Average (có Moving Avg, cần monthly job)
- 🔧 CCDC allocation (công cụ dụng cụ phân bổ - extend deferred logic)
- 🔧 Recurring entries enhancement (có basic, cần templates)
- 🔧 Period-end automation (kết chuyển & phân bổ)

**Purchase Cost Allocation:**
- 🔧 Phân bổ chi phí mua (extend Landed Cost)
- 🔧 Phân bổ vận chuyển (extend Landed Cost)
- 🔧 Phân bổ thuế nhập khẩu (extend Landed Cost)

**AP Management:**
- 🔧 Đối chiếu công nợ NCC (extend Reconciliation)
- 🔧 Báo cáo chi tiết theo hạn TT

**Tax Compliance:**
- 🔧 20M VND rule (VAT deduction block on cash)
- 🔧 Form 01/GTGT generation (VAT Declaration)
- 🔧 Form 03/TNDN generation (CIT Return)

**Tracking:**
- 🔧 Theo dõi khế ước (hợp đồng ngoại tệ - build DocType)

### 9.3. ❌ CẦN BUILD MỚI (0% coverage)

**Credit Management Module (CRITICAL):**
- ❌ Enhanced credit limit check (current + pending + new order)
- ❌ Overdue invoice blocking
- ❌ Manager approval workflow for credit exceed
- ❌ Auto-notification system (customer, sales, finance)
- ❌ Credit utilization dashboard

**Special Features (Nhật Minh Sport):**
- ❌ Chi phí hỗ trợ của hãng (Supplier Support Event tracking)
- ❌ Báo cáo chi phí theo sự kiện (Event Costing - Marketing, Demo, Sales, Pricing)
- ❌ Báo cáo tổng hợp cho NM + Đại diện hãng (Partner Report API)

**Regional Module:**
- ❌ `dcnet_apps/accounting/vietnam/` regional module
- ❌ Vietnam VAT Settings DocType
- ❌ Vietnam tax report generators

### 9.4. Coverage Summary by Category

| Category | Coverage | ✅ Ready | 🔧 Customize | ❌ Build | Effort |
|----------|----------|---------|-------------|---------|--------|
| **Core Accounting** | 90% | 90% | 10% | 0% | 1-2 weeks |
| **AR/AP** | 80% | 70% | 20% | 10% | 3-4 weeks |
| **Bank/Cash** | 85% | 80% | 15% | 5% | 1-2 weeks |
| **Tax** | 70% | 40% | 40% | 20% | 2-3 weeks |
| **Inventory** | 75% | 70% | 25% | 5% | 1-2 weeks |
| **Fixed Assets** | 85% | 80% | 15% | 5% | 2-3 weeks |
| **Reporting** | 70% | 60% | 30% | 10% | 2-3 weeks |
| **Vietnam Specific** | 30% | 30% | 40% | 30% | 3-4 weeks |
| **Credit Mgmt** | 60% | 60% | 0% | 40% | 3-4 weeks |
| **Special Features** | 0% | 0% | 0% | 100% | 8-11 weeks |
| **TỔNG CỘNG** | **50-60%** | **55%** | **20%** | **25%** | **27-41 weeks** |

---

## Phần 10: Kết Luận

### 10.1. Đánh Giá Tổng Thể

**ERPNext v16 có khả năng đáp ứng 50-60% yêu cầu kế toán Việt Nam:**

**Điểm mạnh:**
- ✅ Core accounting rất mạnh (85-95%)
- ✅ AR/AP, Bank, Fixed Assets đầy đủ tính năng
- ✅ 52 reports built-in, dễ customize
- ✅ Multi-currency, multi-company
- ✅ Frappe framework linh hoạt, dễ extend

**Điểm yếu:**
- ❌ Không có Vietnam localization (CoA, Tax, Reports)
- ❌ Thiếu Credit Management workflow (critical cho B2B)
- ❌ Không có concept "Special Features" (chi phí hỗ trợ hãng, sự kiện)
- 🔧 Giá vốn trung bình tháng cần customize

### 10.2. Effort Estimate

**Total Implementation:**
- **Sequential:** 27-41 weeks (~6.5-10 months) with 1-2 developers
- **Parallel:** 15-21 weeks (~3.5-5 months) with 2 developers

**Breakdown:**
- Vietnam Localization: 3-4 weeks
- Core Extensions: 4-5 weeks
- Credit Management: 3-4 weeks
- Special Features: 8-11 weeks
- Tax Compliance: 2-3 weeks
- Testing & UAT: 2-4 weeks

### 10.3. Recommended Approach

**Phase 1 (MVP - 8-10 weeks):**
- Vietnam CoA + VAT configuration
- Monthly Weighted Average
- Basic financial reports
- Credit Management module

**Deliverable:** System sẵn sàng cho daily operations, compliance cơ bản

**Phase 2 (Full - additional 8-12 weeks):**
- Special features (Supplier Support, Event Costing)
- Tax reports (Form 01, 03)
- CCDC allocation
- Partner API

**Deliverable:** Hệ thống hoàn chỉnh với tất cả tính năng đặc biệt

### 10.4. Go/No-Go Decision

**GO if:**
- ✅ Customer OK với timeline 4-6 months full implementation
- ✅ Budget cho 2 developers × 4-6 months
- ✅ Có thể sống với MVP (8-10 weeks) cho đến khi Phase 2 xong
- ✅ Team có ERPNext expertise (hoặc willing to learn)

**NO-GO if:**
- ❌ Cần giải pháp instant (< 2 months)
- ❌ Budget limited, không thể afford customization
- ❌ Yêu cầu special features ngay từ đầu (không thể chờ Phase 2)
- ❌ Team không có Python/Frappe skills

### 10.5. Alternative Options

**Nếu NO-GO:**

**Option 1:** Mua Vietnam accounting software (VN-focused)
- **Pros:** Vietnam compliance 100%, instant
- **Cons:** Không integrate với CRM/ERP, vendor lock-in

**Option 2:** Hybrid approach
- Use ERPNext for CRM/Sales/Inventory
- Use separate Vietnam accounting software
- Sync via API
- **Pros:** Best of both worlds
- **Cons:** Integration complexity, 2 systems to maintain

**Option 3:** Delay accounting module
- Deploy Phase 1 CRM only (đã 90% complete)
- Use existing Bravo for accounting (temporary)
- Migrate accounting later (Phase 2)
- **Pros:** Faster time to market for CRM
- **Cons:** Manual data sync, delayed full integration

---

## Next Steps

1. **Customer Decision:**
   - Review this analysis
   - Decide GO/NO-GO for accounting module
   - Confirm timeline & budget

2. **If GO:**
   - Prioritize phases (MVP first or Full?)
   - Allocate resources (2 developers recommended)
   - Schedule kickoff

3. **Proof of Concept (2 weeks):**
   - Build Vietnam CoA template
   - Configure VAT 0%, 5%, 8%, 10%
   - Demo to customer
   - Validate approach

4. **Development Kickoff:**
   - Sprint planning
   - Weekly demos
   - Agile delivery

---

**Document End**

**Prepared by:** Claude Code Analysis
**Date:** 20/01/2026
**Version:** 1.0
**Status:** Draft for Customer Review
