# Cash Count (Kiểm Kê Quỹ Tiền Mặt) — Design Spec

**App:** vn_accounting
**Date:** 2026-04-16
**Status:** Approved

---

## 1. Overview

Chức năng kiểm kê quỹ tiền mặt — đối chiếu số dư sổ sách (GL) với tiền mặt thực tế đếm trong két. Khi có chênh lệch, ghi nhận vào TK chờ xử lý (1381/3381) theo chuẩn VAS 2 bước.

**Scope:**
- Kiểm kê định kỳ + đột xuất
- Bảng kê mệnh giá (optional)
- Bút toán ghi nhận chênh lệch (bước 1 VAS)
- In biên bản kiểm kê (Mẫu 08a-TT)
- 3 người ký: Thủ quỹ + Kế toán trưởng + Giám đốc

**Out of scope:** Bước 2 xử lý chênh lệch (bồi thường, chi phí, thu nhập) — JE thủ công do kế toán tự tạo.

---

## 2. Data Model

### 2.1 DocType: Cash Count

**Regular DocType** (không submittable) — dùng status Select field thay vì docstatus.

> **Why:** Submittable lock child table khi docstatus=1, nhưng bước xử lý chênh lệch cần link JE ngược lại vào biên bản sau khi submit. Regular DocType + status field linh hoạt hơn.

| Section | Field | Type | Required | Ghi chú |
|---------|-------|------|----------|---------|
| **Header** | company | Link → Company | Yes | |
| | cash_account | Link → Account | Yes | Filter: account_number LIKE '111%', is_group=0 |
| | count_date | Date | Yes | Default today |
| | count_type | Select | Yes | Periodic / Unscheduled |
| | reason | Small Text | Depends on | Required khi count_type=Unscheduled |
| **Số dư sổ sách** | book_balance | Currency | — | Auto-fetch từ GL, read-only |
| **Kiểm đếm** | show_denomination | Check | — | Default 0 |
| | denominations | Table → Cash Count Denomination | — | Hidden khi show_denomination=0 |
| | actual_amount | Currency | Yes | Auto-sum nếu show_denomination=1, nhập tay nếu 0 |
| **Kết quả** | difference | Currency | — | = actual_amount - book_balance, auto, read-only |
| | difference_type | Select | — | Balanced / Surplus / Deficit, auto |
| **Xử lý chênh lệch** | difference_account | Link → Account | — | Auto-fill từ Settings (3381/1381), cho phép đổi |
| | save_as_default | Check | — | Tick = ghi ngược vào VN Accounting Settings |
| | pending_je | Link → Journal Entry | — | JE ghi nhận bước 1 (1381/3381) |
| | resolution_je | Link → Journal Entry | — | JE xử lý bước 2 (thủ công) |
| | resolution_status | Select | — | Not Applicable / Pending / Resolved, auto |
| **Ký duyệt** | cashier | Link → Employee | Yes | Thủ quỹ |
| | chief_accountant | Link → Employee | Yes | Kế toán trưởng |
| | director | Link → Employee | Yes | Giám đốc |
| | remarks | Text | — | |
| **Status** | status | Select | — | Draft / Counted / Approved / Closed / Pending Resolution / Resolved |

### 2.2 Child DocType: Cash Count Denomination

| Field | Type | Ghi chú |
|-------|------|---------|
| denomination | Int | Mệnh giá (VND, ví dụ 500000) |
| quantity | Int | Số lượng tờ |
| amount | Currency | = denomination × quantity, auto, read-only |

Mệnh giá VND chuẩn (pre-populate khi bật show_denomination): 500.000, 200.000, 100.000, 50.000, 20.000, 10.000, 5.000, 2.000, 1.000.

### 2.3 VN Accounting Settings — Fields mới

| Field | Type | Ghi chú |
|-------|------|---------|
| cash_surplus_account | Link → Account | TK 3381 (thừa quỹ chờ xử lý). Default empty |
| cash_deficit_account | Link → Account | TK 1381 (thiếu quỹ chờ xử lý). Default empty |

---

## 3. Workflow & Business Logic

### 3.1 Status Flow

```
Draft → Counted → Approved → Closed              (difference == 0)
                           → Pending Resolution   (difference != 0, pending_je submitted)
                                → Resolved         (resolution_je submitted)
```

| Chuyển | Ai | Điều kiện |
|--------|-----|-----------|
| Draft → Counted | Accounts User | actual_amount is set (kể cả 0 — két rỗng là hợp lệ), cashier đã chọn |
| Counted → Approved | Accounts Manager | chief_accountant + director đã chọn |
| Approved → Closed | Auto | difference == 0 |
| Approved → Pending Resolution | Auto | difference != 0 AND pending_je submitted |
| Pending Resolution → Resolved | Auto | resolution_je submitted |

> **Why:** Không dùng Frappe Workflow DocType — 4 trạng thái đơn giản, code trong controller gọn hơn.

### 3.2 Tính book_balance

Server-side pure function:

```python
@frappe.whitelist()
def get_book_balance(cash_account, count_date, company):
    """SUM(debit) - SUM(credit) from GL Entry
    where account=cash_account, posting_date <= count_date, is_cancelled=0"""
```

Tái sử dụng `report_utils.get_opening_balance()` (truyền to_date = count_date + 1 day).

**Trigger:** Client-side `frappe.call` khi cash_account hoặc count_date thay đổi + button "Refresh Balance". Server `validate()` cũng recalc để đảm bảo consistency.

### 3.3 Auto-fill difference_account

Khi `difference_type` thay đổi:
- Surplus → fill từ Settings.cash_surplus_account (3381)
- Deficit → fill từ Settings.cash_deficit_account (1381)
- Balanced → clear

Khi `save_as_default` = 1 và save → ghi ngược difference_account vào Settings field tương ứng.

### 3.4 Bút toán chênh lệch — Bước 1 (Button "Record Difference")

Button chỉ hiện khi status=Approved AND difference != 0.

| Trường hợp | Nợ | Có |
|---|---|---|
| Thiếu (actual < book) | difference_account (1381) | cash_account (111x) |
| Thừa (actual > book) | cash_account (111x) | difference_account (3381) |

- Tạo **Draft** JE (không auto-submit — bút toán tiền cần kiểm tra)
- Link vào `pending_je`
- Remark: `"Cash count #{name} — {Deficit/Surplus} {amount}"`
- Cost center từ company default

### 3.5 Bước 2 — Xử lý chênh lệch (Button "Resolve Difference")

Button hiện khi `pending_je` đã submit AND `resolution_status == Pending`.

User chọn `resolution_type` (Select trên form):

**Khi thiếu quỹ (1381 cần tất toán):**

| Lý do | Nợ | Có | Giải thích |
|-------|-----|-----|------------|
| Employee Compensation | 1388 (Phải thu khác — nhân viên) | 1381 | Thủ quỹ bồi thường |
| Management Expense | 6425 (Chi phí bằng tiền khác) | 1381 | Tính vào chi phí quản lý |

**Khi thừa quỹ (3381 cần tất toán):**

| Lý do | Nợ | Có | Giải thích |
|-------|-----|-----|------------|
| Return to Owner | 3381 | 111 (cash_account) | Trả lại cho đối tượng |
| Other Income | 3381 | 711 (Thu nhập khác) | Ghi nhận thu nhập |

- Tạo **Draft** JE, link vào `resolution_je`
- Remark: `"Cash count #{name} — Resolution: {resolution_type}"`
- Khi `resolution_je` submit → `resolution_status` = Resolved → status = Resolved

**Data model bổ sung:**

| Field | Type | Ghi chú |
|-------|------|---------|
| resolution_type | Select | Employee Compensation / Management Expense / Return to Owner / Other Income |
| resolution_target_account | Link → Account | Auto-fill theo resolution_type, cho phép đổi |

**Settings bổ sung (VN Accounting Settings):**

| Field | Type | Default | Ghi chú |
|-------|------|---------|---------|
| employee_receivable_account | Link → Account | 1388 | TK phải thu nhân viên |
| management_expense_account | Link → Account | 6425 | TK chi phí bằng tiền khác |
| other_income_account | Link → Account | 711 | TK thu nhập khác |

Các TK này cũng hỗ trợ `save_as_default` pattern — user chọn lần đầu, tick lưu mặc định.

> **Why:** Bước 2 có mẫu cố định (chỉ 4 kịch bản). Template hoá giảm sai sót và đảm bảo audit trail đầy đủ — lý do xử lý gắn liền biên bản kiểm kê, không nằm rời rạc trong JE.

### 3.6 Edge Cases

1. **Kiểm kê cùng ngày có giao dịch chưa ghi sổ** — book_balance chỉ tính GL Entry đã post. Draft JE không ảnh hưởng. Kế toán phải đảm bảo sổ cập nhật trước kiểm kê.
2. **Công ty có nhiều quỹ tiền mặt** (nhiều TK 111x) — mỗi Cash Count chọn 1 cash_account. Kiểm kê toàn bộ = nhiều Cash Count cùng ngày.
3. **Kiểm kê đột xuất khi thay đổi thủ quỹ** — count_type=Unscheduled, reason="Bàn giao thủ quỹ". Không cần logic đặc biệt.

---

## 4. Print Format — Biên Bản Kiểm Kê Quỹ (Mẫu 08a-TT)

Jinja HTML Print Format, khổ A4 dọc.

### Layout

```
Đơn vị: {company}                           Mẫu số 08a
Địa chỉ: {company_address}            (Ban hành theo TT200/2014)

         BIÊN BẢN KIỂM KÊ QUỸ TIỀN MẶT
       Ngày {count_date} tháng ... năm ...

Loại kiểm kê: {Định kỳ / Đột xuất}
Lý do: {reason}  (chỉ hiện khi Đột xuất)
Tài khoản quỹ: {cash_account}

I. Số dư theo sổ kế toán: {book_balance}

II. Số kiểm kê thực tế:
┌──────────────┬──────────┬──────────────┐
│  Mệnh giá    │  Số tờ   │  Thành tiền  │
├──────────────┼──────────┼──────────────┤
│  (rows with quantity > 0)               │
├──────────────┼──────────┼──────────────┤
│  Tổng cộng   │          │  {actual}    │
└──────────────┴──────────┴──────────────┘
(bảng mệnh giá: conditional, chỉ hiện khi show_denomination=1)
(nếu không: "Tổng số tiền mặt kiểm kê: {actual_amount}")

III. Chênh lệch:
- Thừa: {surplus_amount hoặc "—"}
- Thiếu: {deficit_amount hoặc "—"}
- Lý do chênh lệch: {remarks}

IV. Kết luận và kiến nghị xử lý:
{remarks hoặc "Quỹ cân bằng, không chênh lệch"}

┌──────────┬────────────────┬──────────┐
│ Giám đốc │ Kế toán trưởng │  Thủ quỹ │
│ (Ký tên) │   (Ký tên)     │ (Ký tên) │
│          │                │          │
│{director}│{chief_acct}    │{cashier} │
└──────────┴────────────────┴──────────┘
```

### Kỹ thuật

- Jinja HTML Print Format (không Standard — cần conditional layout phức tạp)
- `company_address`: lấy từ `frappe.get_doc("Company", doc.company)` — không cần field riêng trên Cash Count
- Số tiền VND format: `{:,.0f}` replace comma→dot (5.000.000)
- Chỉ hiện denomination rows có quantity > 0
- Font: Times New Roman (chuẩn văn bản hành chính VN)
- CSS @media print, margin A4

---

## 5. Permissions

| Role | Read | Write | Create | Delete |
|------|------|-------|--------|--------|
| Accounts User | Yes | Yes (Draft only) | Yes | No |
| Accounts Manager | Yes | Yes | Yes | Yes |

> **Why:** Accounts User = thủ quỹ (tạo, nhập). Accounts Manager = KTT (duyệt, tạo JE, xoá Draft). Giám đốc chỉ ký biên bản in, không cần thao tác hệ thống.

---

## 6. Sidebar Integration

Thêm vào section "Quỹ tiền mặt" trong workspace sidebar, trước "Tạo bút toán tiền mặt":

```
Quỹ tiền mặt
├── Thu tiền mặt          (existing)
├── Chi tiền mặt          (existing)
├── Sổ quỹ tiền mặt      (existing)
├── Kiểm kê quỹ          ← NEW: link_type=DocType, link_to=Cash Count
└── Tạo bút toán tiền mặt (existing)
```

---

## 7. Translations (vi.csv additions)

```csv
Cash Count,Kiểm kê quỹ tiền mặt
Cash Count Denomination,Bảng kê mệnh giá
Periodic,Định kỳ
Unscheduled,Đột xuất
Balanced,Cân bằng
Surplus,Thừa quỹ
Deficit,Thiếu quỹ
Record Difference,Ghi nhận chênh lệch
Refresh Balance,Cập nhật số dư
Book Balance,Số dư sổ sách
Actual Amount,Số tiền thực tế
Show Denomination Detail,Chi tiết mệnh giá
Save as Default Account,Lưu làm tài khoản mặc định
Not Applicable,Không áp dụng
Pending,Chờ xử lý
Resolved,Đã xử lý
Counted,Đã kiểm đếm
Approved,Đã duyệt
Closed,Đóng
Cash Surplus Account,Tài khoản thừa quỹ
Cash Deficit Account,Tài khoản thiếu quỹ
Resolve Difference,Xử lý chênh lệch
Resolution Type,Hình thức xử lý
Employee Compensation,Bồi thường nhân viên
Management Expense,Chi phí quản lý
Return to Owner,Trả lại đối tượng
Other Income,Thu nhập khác
Pending Resolution,Chờ xử lý chênh lệch
Employee Receivable Account,Tài khoản phải thu nhân viên
Management Expense Account,Tài khoản chi phí quản lý
Other Income Account,Tài khoản thu nhập khác
```
