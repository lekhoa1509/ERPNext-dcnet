---
project: apps/vn_accounting
base_branch: main
---

# Tiền Gửi Có Kỳ Hạn & Khoản Vay Ngân Hàng — Design Spec

## 1. Tổng quan

Bổ sung tính năng quản lý **tiền gửi có kỳ hạn** (TK 1281) và **khoản vay ngân hàng** (TK 3411) vào app `vn_accounting`. Tự động sinh lịch trả lãi/trả nợ, tạo nháp Journal Entry hàng kỳ, cảnh báo đáo hạn.

> **Why nằm trong vn_accounting:** Đây là nghiệp vụ kế toán cốt lõi (TK 1281, 3411, 515, 635), sidebar "Ngân hàng" đã có sẵn. vn_banking tập trung vào import sao kê — domain khác.

### Phạm vi

- 2 DocTypes chính: Term Deposit, Bank Loan
- 4 Child DocTypes: Interest Schedule, JE Link (term deposit), Repayment Schedule, JE Link (bank loan)
- 1 Settings section (thêm vào VN Accounting Settings hoặc tạo mới nếu chưa có)
- Scheduled job tạo nháp JE hàng ngày
- Cảnh báo đáo hạn qua Notification Log
- Sidebar items mới trong "Ngân hàng" + "Thiết lập"
- Trang hướng dẫn sử dụng tích hợp trong app

### Ngoài phạm vi

- Trái phiếu (TK 1282), cho vay (TK 1283) — phase 2
- Nợ thuê tài chính (TK 3412) — phase 2
- Báo cáo dòng tiền dự báo — phase 2

## 2. DocType: Term Deposit (Sổ tiền gửi có kỳ hạn)

### 2.1 Fields

| Field | Type | Mô tả | Default |
|-------|------|-------|---------|
| `company` | Link → Company | Công ty | User default |
| `bank` | Link → Bank | Ngân hàng | |
| `bank_account` | Link → Bank Account | TK ngân hàng nguồn (112x) | |
| `deposit_account` | Link → Account | TK hạch toán tiền gửi | Từ Settings |
| `interest_income_account` | Link → Account | TK doanh thu lãi | Từ Settings |
| `deposit_number` | Data | Số sổ tiền gửi (do NH cấp) | |
| `principal_amount` | Currency | Số tiền gốc | |
| `interest_rate` | Percent | Lãi suất %/năm | |
| `interest_type` | Select | Kiểu trả lãi (5 kiểu) | |
| `start_date` | Date | Ngày gửi | |
| `maturity_date` | Date | Ngày đáo hạn | Auto-calc |
| `term_months` | Int | Kỳ hạn (tháng) | |
| `early_withdrawal_rate` | Percent | Lãi suất tất toán trước hạn | |
| `alert_days_before` | Int | Cảnh báo trước X ngày | Từ Settings |
| `status` | Select | Draft/Active/Matured/Settled/Early Settled | Draft |
| `total_interest` | Currency | Tổng lãi dự kiến (read-only, auto-calc) | |
| `interest_schedule` | Table → Term Deposit Interest | Lịch trả lãi | |
| `remarks` | Small Text | Ghi chú | |

### 2.2 Kiểu trả lãi (`interest_type`)

| Giá trị | Mô tả | Lịch trả lãi |
|---------|-------|--------------|
| `End of Term` | Lãi cuối kỳ — 1 lần khi đáo hạn | 1 dòng: maturity_date |
| `Monthly` | Lãi hàng tháng | N dòng: mỗi tháng từ start+1m đến maturity |
| `Quarterly` | Lãi hàng quý | N dòng: mỗi 3 tháng |
| `Prepaid` | Lãi trả trước — khấu trừ vào gốc | 1 dòng: start_date (lãi = gốc × rate × term/12) |
| `Compound` | Lãi nhập gốc — compound mỗi tháng | N dòng: lãi cộng dồn vào principal_at_start |

### 2.3 Công thức tính lãi

**Lãi đơn (End of Term, Monthly, Quarterly, Prepaid):**
```
interest_per_period = principal × (rate/100) × (days_in_period / 365)
```
> **Why 365 không phải 360:** Chuẩn VN (Ngân hàng Nhà nước) dùng actual/365.

**Lãi kép (Compound):**
```
Kỳ 1: interest = principal × (rate/100) × (days/365)
       new_principal = principal + interest
Kỳ 2: interest = new_principal × (rate/100) × (days/365)
       ...
```

### 2.4 Child DocType: Term Deposit Interest

| Field | Type | Mô tả |
|-------|------|-------|
| `due_date` | Date | Ngày trả lãi |
| `interest_amount` | Currency | Số tiền lãi kỳ này |
| `principal_at_start` | Currency | Gốc đầu kỳ (cho Compound) |
| `status` | Select | Pending / Draft Created / Booked |
| `journal_entry` | Link → Journal Entry | JE đã tạo |

### 2.5 Workflow

```
Draft → [Submit] → Active → [Maturity date] → Matured → [Settle] → Settled
                       ↘ [Early Settle] → Early Settled
```

- **Submit (Draft → Active):** Tạo JE gửi tiền (Nợ 1281 / Có 112x). Sinh interest_schedule.
- **Matured:** Status tự chuyển khi today >= maturity_date (via scheduled job).
- **Settle:** Nút "Tất toán" trên form → tạo draft JE (Nợ 112x / Có 1281 + 515 nếu còn lãi cuối kỳ).
- **Early Settle:** Nút "Tất toán trước hạn" → nhập ngày tất toán → tính lãi theo early_withdrawal_rate → tạo draft JE.
- **Tái tục:** Nút "Tái tục" trên form khi status=Matured → tạo Term Deposit mới với principal = old principal + accumulated interest (nếu Compound/End of Term).

### Khi nào khác?

- **Tất toán trước hạn:** Lãi thực nhận = gốc × early_withdrawal_rate × actual_days/365. Các kỳ lãi đã Booked trước đó vẫn giữ nguyên — chênh lệch (nếu lãi đã trả > lãi tất toán sớm) sẽ là bút toán điều chỉnh.
- **Lãi trả trước (Prepaid):** Gốc thực gửi = principal_amount - prepaid_interest. JE gửi tiền: Nợ 1281 (principal_amount) / Có 112x (principal_amount - interest) / Có 515 (interest).
- **Maturity rơi vào ngày nghỉ:** Scheduled job vẫn tạo draft đúng due_date. Kế toán tự điều chỉnh posting_date khi submit.

## 3. DocType: Bank Loan (Khoản vay ngân hàng)

### 3.1 Fields

| Field | Type | Mô tả | Default |
|-------|------|-------|---------|
| `company` | Link → Company | | User default |
| `bank` | Link → Bank | Ngân hàng cho vay | |
| `bank_account` | Link → Bank Account | TK nhận tiền vay (112x) | |
| `loan_account` | Link → Account | TK nợ vay | Từ Settings |
| `interest_expense_account` | Link → Account | TK chi phí lãi vay | Từ Settings |
| `loan_number` | Data | Số hợp đồng vay | |
| `loan_amount` | Currency | Số tiền vay | |
| `outstanding_amount` | Currency | Dư nợ hiện tại (auto-calc) | |
| `interest_rate` | Percent | Lãi suất %/năm | |
| `rate_type` | Select | Cố định / Thả nổi | Cố định |
| `repayment_type` | Select | Kiểu trả nợ (2 kiểu) | |
| `repayment_frequency` | Select | Hàng tháng / Hàng quý | Hàng tháng |
| `start_date` | Date | Ngày giải ngân | |
| `maturity_date` | Date | Ngày đáo hạn | |
| `alert_days_before` | Int | Cảnh báo trước X ngày | Từ Settings |
| `status` | Select | Draft/Active/Matured/Settled | Draft |
| `total_interest` | Currency | Tổng lãi dự kiến (read-only) | |
| `total_repayment` | Currency | Tổng trả (gốc+lãi, read-only) | |
| `repayment_schedule` | Table → Bank Loan Repayment | Lịch trả nợ | |
| `remarks` | Small Text | Ghi chú | |

### 3.2 Kiểu trả nợ (`repayment_type`)

**Trả lãi hàng kỳ + gốc cuối kỳ (`Interest Only`):**
```
Mỗi kỳ: interest = outstanding × (rate/100) × (days/365)
         principal = 0 (trừ kỳ cuối = toàn bộ gốc)
```

**Trả đều gốc + lãi (`EMI` — Equal Monthly Installment):**
```
monthly_rate = rate / 100 / 12
EMI = loan_amount × monthly_rate / (1 - (1 + monthly_rate)^(-n))
Mỗi kỳ: interest = outstanding × monthly_rate
         principal = EMI - interest
         outstanding -= principal
```

### 3.3 Child DocType: Bank Loan Repayment

| Field | Type | Mô tả |
|-------|------|-------|
| `due_date` | Date | Ngày trả |
| `principal_amount` | Currency | Gốc trả kỳ này |
| `interest_amount` | Currency | Lãi trả kỳ này |
| `total_amount` | Currency | Tổng trả (gốc+lãi) |
| `outstanding_after` | Currency | Dư nợ sau trả |
| `status` | Select | Pending / Draft Created / Booked |
| `journal_entry` | Link → Journal Entry | JE đã tạo |

### 3.4 Workflow

```
Draft → [Submit] → Active → [All repaid] → Settled
                       ↘ [Early Settle] → Settled
```

- **Submit (Draft → Active):** Tạo JE giải ngân (Nợ 112x / Có 3411). Sinh repayment_schedule.
- **Trả kỳ:** Scheduled job tạo draft JE (Nợ 3411+635 / Có 112x). Khi JE submitted → update outstanding_amount.
- **Early Settle:** Nút "Tất toán trước hạn" → tính lãi pro-rata đến ngày tất toán + gốc còn lại → draft JE.
- **Cập nhật lãi suất (thả nổi):** Nút "Cập nhật lãi suất" → nhập rate mới + ngày hiệu lực → regenerate lịch từ kỳ tiếp theo (kỳ đã Booked không đổi).

### Khi nào khác?

- **Trả nợ trước 1 kỳ:** Kế toán có thể submit JE sớm hơn due_date. Status dòng chuyển Booked, scheduled job bỏ qua.
- **Thay đổi lãi suất giữa kỳ (thả nổi):** Regenerate từ kỳ chưa Booked đầu tiên. Kỳ đã Booked giữ nguyên số liệu.
- **Giải ngân nhiều đợt:** Mỗi đợt giải ngân = 1 Bank Loan riêng. Không hỗ trợ partial disbursement trên cùng 1 record (tránh phức tạp hoá schedule).

## 4. Settings

Thêm Section "Ngân hàng — Tiền gửi & Vay" vào VN Accounting Settings (Single DocType). Nếu chưa tồn tại → tạo mới.

| Field | Label | Type | Default |
|-------|-------|------|---------|
| `default_deposit_account` | TK tiền gửi có kỳ hạn | Link → Account | Account matching "1281%" |
| `default_interest_income_account` | TK doanh thu lãi tiền gửi | Link → Account | Account matching "515%" |
| `default_loan_account` | TK nợ vay | Link → Account | Account matching "3411%" |
| `default_interest_expense_account` | TK chi phí lãi vay | Link → Account | Account matching "635%" |
| `deposit_alert_days` | Cảnh báo đáo hạn tiền gửi (ngày) | Int | 7 |
| `loan_alert_days` | Cảnh báo đáo hạn vay (ngày) | Int | 7 |

> **Why Settings thay vì hardcode:** Mỗi công ty có thể dùng sub-account khác (VD: 1281.01 cho VCB, 1281.02 cho BIDV). Kế toán cấu hình 1 lần, mỗi sổ/khoản vay kế thừa mặc định nhưng cho phép override trên form.

Sidebar "Thiết lập" thêm item link tới Settings.

## 5. Automation

### 5.1 Scheduled Job (daily)

Hook trong `hooks.py`:
```python
scheduler_events = {
    "daily": [
        "vn_accounting.treasury.scheduled.process_treasury_schedules"
    ]
}
```

Logic:
1. Quét `Term Deposit` (status=Active): mỗi Interest Schedule row có `due_date <= today` và `status=Pending` → tạo draft JE
2. Quét `Bank Loan` (status=Active): mỗi Repayment Schedule row có `due_date <= today` và `status=Pending` → tạo draft JE
3. Quét đáo hạn: Term Deposit có `maturity_date <= today` và `status=Active` → chuyển status → Matured + tạo draft JE tất toán (nếu kiểu lãi cuối kỳ, kèm lãi)
4. Cảnh báo: records có `maturity_date - alert_days_before <= today` và chưa có alert → tạo Notification Log

### 5.2 Bút toán tự động

| Nghiệp vụ | Nợ | Có | Trigger |
|-----------|-----|-----|---------|
| Gửi tiền | deposit_account (1281) | bank_account (112x) | Submit Term Deposit |
| Lãi tiền gửi (định kỳ) | bank_account (112x) | interest_income_account (515) | Scheduled job |
| Lãi tiền gửi (nhập gốc) | deposit_account (1281) | interest_income_account (515) | Scheduled job |
| Lãi tiền gửi (trả trước) | bank_account (112x) | interest_income_account (515) | Submit Term Deposit |
| Tất toán tiền gửi | bank_account (112x) | deposit_account (1281) + interest_income_account (515) | Nút Tất toán / Scheduled job |
| Nhận vay | bank_account (112x) | loan_account (3411) | Submit Bank Loan |
| Trả lãi vay | interest_expense_account (635) | bank_account (112x) | Scheduled job |
| Trả gốc vay | loan_account (3411) | bank_account (112x) | Scheduled job |
| Trả gốc+lãi (EMI) | loan_account (3411) + interest_expense_account (635) | bank_account (112x) | Scheduled job |

Tất cả JE tạo ở trạng thái **Draft**. Kế toán review rồi submit thủ công.

> **Why Draft không auto-submit:** Chứng từ ảnh hưởng sổ cái — kế toán cần kiểm tra số liệu trước khi ghi nhận.

### 5.3 Cảnh báo đáo hạn

- Tạo `frappe.publish_realtime` notification + `Notification Log` cho users có role "Accounts Manager"
- Cảnh báo trước X ngày (cấu hình trong Settings)
- Cảnh báo chỉ tạo 1 lần per record (đánh dấu `alert_sent` flag)

## 6. Sidebar & Navigation

Thêm vào sidebar "Ngân hàng" trong `workspace_sidebar/vn_accounting.json`:

```
Ngân hàng
  ├── Thu ngân hàng          (hiện có)
  ├── Chi ngân hàng          (hiện có)
  ├── Sổ Tài khoản ngân hàng (hiện có)
  ├── Đối soát sao kê        (hiện có)
  ├── Điều chuyển nội bộ     (hiện có)
  ├── Tạo bút toán ngân hàng (hiện có)
  ├── ── (phân cách visual) ──
  ├── Tiền gửi có kỳ hạn     ← MỚI (link_type: DocType, link_to: Term Deposit)
  └── Khoản vay ngân hàng    ← MỚI (link_type: DocType, link_to: Bank Loan)

Thiết lập
  ├── ... (hiện có)
  └── Cài đặt ngân hàng      ← MỚI (link tới VN Accounting Settings)
```

## 7. Hướng dẫn sử dụng — tích hợp trong app

### 7.1 Form-level help

- `introduction` field trên Term Deposit form: *"Nhập thông tin sổ tiền gửi. Hệ thống tự động tính lịch trả lãi và tạo nháp bút toán khi đến hạn."*
- `introduction` field trên Bank Loan form: *"Nhập thông tin khoản vay. Hệ thống tự động tính lịch trả nợ và tạo nháp bút toán hàng kỳ."*
- `description` trên các field quan trọng (interest_type, repayment_type, early_withdrawal_rate...)

### 7.2 Trang hướng dẫn

Frappe Web Page (`/desk/vn-treasury-guide`) chứa:
- Giải thích 5 kiểu trả lãi tiền gửi + ví dụ số
- Giải thích 2 kiểu trả nợ vay + ví dụ số
- Flow sử dụng: tạo → submit → scheduled job → review draft JE → submit JE
- Xử lý đặc biệt: tất toán trước hạn, tái tục, thay đổi lãi suất

> **Why không dùng Wiki/Docs riêng:** Docs bên ngoài out-of-date khi tính năng thay đổi. Hướng dẫn trong app = versioned cùng code.

### 7.3 Translations

Thêm vào `translations/vi.csv`:
```
Term Deposit,Tiền Gửi Có Kỳ Hạn
Bank Loan,Khoản Vay Ngân Hàng
Interest Schedule,Lịch Trả Lãi
Repayment Schedule,Lịch Trả Nợ
```

## 8. Permissions

| Role | Term Deposit | Bank Loan | Settings |
|------|-------------|-----------|----------|
| Accounts User | Read, Create, Write | Read, Create, Write | Read |
| Accounts Manager | Full (incl. Submit, Cancel) | Full (incl. Submit, Cancel) | Read, Write |
| System Manager | Full | Full | Full |

## 9. Testing

### Pure functions (TDD required)
- `calculate_interest_schedule(principal, rate, interest_type, start_date, maturity_date)` — test all 5 types
- `calculate_repayment_schedule(amount, rate, repayment_type, frequency, start_date, maturity_date)` — test both types
- `calculate_early_settlement(deposit/loan, settlement_date)` — test pro-rata calculation

### Integration (verify at end)
- Submit Term Deposit → JE created with correct accounts
- Scheduled job → draft JE created for due items
- Settle → JE with correct amounts
- Settings defaults propagate to new records
