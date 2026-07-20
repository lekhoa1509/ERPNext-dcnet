# vn_banking v1 — Bank Statement Import & Auto-Match

**Date:** 2026-04-10
**Project:** frappe-bench-dcnet
**Source requirements:** `docs/accounting-requirements/converted/hop-ke-toan-08-04-2026.md` §3 Ngân hàng
**Status:** Design approved, ready for implementation plan

## 1. Goal

Cho kế toán DCNet một công cụ để: (1) upload file sao kê Excel từ ngân hàng VN, (2) tự động khớp từng giao dịch với Sales Invoice / Purchase Invoice đang mở, (3) tạo Payment Entry từ matching result với thao tác tối thiểu, (4) cảnh báo khi thiếu thông tin hoặc chênh lệch số tiền. Mục tiêu UX: kế toán hoàn thành 100 dòng sao kê trong **< 2 phút** không cần đọc docs.

Kiến trúc phải sẵn sàng cho v2: pull trực tiếp từ API ngân hàng (Open Banking), không phải refactor lớn.

## 2. Non-Goals v1

Các hạng mục sau nằm trong §3 yêu cầu gốc nhưng **không làm** trong v1 — tách sub-project riêng:
- **Dự báo dòng tiền** — liên quan tới module Hợp đồng và PAKD đang xây dựng
- **Khế ước vay** — Loan module, scope riêng
- **Tỷ giá hối đoái** — dùng native ERPNext, không custom
- **API pull từ ngân hàng** — scaffold architecture, không implement
- **L4 custom matcher rules (regex trên narration do user tạo)** — scaffold schema, không expose UI
- **L5 ML scoring** — không làm
- **L6 per-Bank-Account rule override** — scaffold schema, không expose UI

## 3. Architecture

### 3.1 Big picture

```
Source (Excel v1, API v2)
        │
        ▼
┌──────────────────┐   fixtures: 7 bank formats
│ BankDataSource   │◄── Bank Statement Format (DocType mapping động)
│ (pluggable)      │
└────────┬─────────┘
         │ NormalizedTransaction[]
         ▼
┌──────────────────┐    lưu file gốc + metadata + list transaction
│ Bank Statement   │    audit trail; source-agnostic
│ Import           │
└────────┬─────────┘
         │ dedupe by (date+amount+ref+narration) hash
         ▼
┌──────────────────┐    ERPNext native DocType + custom fields
│ Bank Transaction │    (bank_statement_import, dedupe_hash,
│                  │     match_confidence, matched_by, ...)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐   rules N → N+A → P+A → M+A → none
│ Match Engine     │   pluggable pipeline (first-hit-wins)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐   Custom Page: Bank Reconcile
│ Review UI        │   upload → table + side panel + bulk actions
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Payment Entry    │   draft default, configurable auto-submit
│ (ERPNext native) │
└──────────────────┘
```

**Principles:**
- Không sửa Frappe/ERPNext core. Tất cả qua custom DocTypes mới, custom fields, custom page, monkey-patches (nếu cần).
- **Source-agnostic ingestion**: layer Source tách khỏi Parser khỏi Match. Engine không biết data đến từ file hay API.
- **Pluggable matcher pipeline**: matcher là Python class implement `BaseMatcher`. Engine đọc thứ tự từ Settings.
- **Progressive disclosure UI**: defaults "just work", Advanced options ẩn sau link.

### 3.2 Source layer (API-ready)

```python
# vn_banking/source/base.py
class BankDataSource(ABC):
    key: str                   # "excel_upload" | "bank_api_vcb" | ...
    label: str
    requires_credentials: bool
    supports_pull: bool        # API có thể tự pull; file thì không

    @abstractmethod
    def fetch(self, bank_account, from_date, to_date, context) -> Iterator[NormalizedTransaction]: ...

    def validate_config(self, bank_account) -> list[str]: ...
```

**v1 implements:** `ExcelFileSource` (đọc file từ `context["file_url"]`, dùng Bank Statement Format để parse).

**v2 future:** `BankApiSource`, `MT940Source`, `CAMT053Source` — không refactor layer downstream.

**Registry DocType `Bank Data Source`** (fixture-seeded):
- `source_key` (unique), `source_label`, `handler_path` (Python dotted path), `requires_credentials`, `supports_pull`, `credential_schema` (JSON)
- v1 ship 1 fixture: `excel_upload`

### 3.3 DocTypes

#### `Bank Statement Format` (fixture, per-bank parser mapping)
- `format_name` (VD: "VCB - Sao kê chi tiết TK")
- `bank` (Link Bank)
- `file_type` (xlsx / xls / csv)
- `sheet_index`, `header_row`, `data_start_row`, `data_end_marker` (regex)
- `col_date`, `col_narration`, `col_debit`, `col_credit`, `col_balance`, `col_ref`, `col_counter_account`
- `date_format`, `decimal_separator`, `thousands_separator`
- `currency` (default VND)
- **Fixtures v1:** VCB, BIDV, Vietinbank, Techcombank, MB, ACB, Sacombank (7 banks)

#### `Bank Statement Import` (parent audit doc — **NOT submittable**, use `status` field)
- `bank_account` (Link), `from_date`, `to_date`
- `source_type` (Link Bank Data Source, default "excel_upload")
- `file` (Attach, optional — required when source_type=excel_upload)
- `file_hash` (Data — metadata only for "last upload this file" display; **NOT used for dedupe**; dedupe is per-transaction via `Bank Transaction.dedupe_hash`)
- `format` (Link Bank Statement Format, auto-detect)
- `triggered_by` (Select: Manual / Scheduled / Webhook — v1 only Manual)
- `api_from_date`, `api_to_date`, `api_page_cursor` (v2 fields, hidden v1)
- `total_rows`, `matched_rows`, `unmatched_rows`, `duplicate_rows`
- `status` (Select: Draft / Parsed / Reviewed / Posted — regular field, not `docstatus`)
- `log` (Long Text — parse errors + warnings)

**Transactions relation:** reverse link via `Bank Transaction.bank_statement_import` — no child table on Import. Query `frappe.get_all("Bank Transaction", filters={"bank_statement_import": import_name})` when needed. This avoids child-row locking issues and keeps Bank Transaction docs independently editable (required for incremental PE creation by user).

#### Custom fields on `Bank Transaction` (ERPNext native)
- `bank_statement_import` (Link parent)
- `dedupe_hash` (Data — SHA-256 of date+amount+bank_ref+narration)
- `match_confidence` (Select: High / Medium / Low / None)
- `matched_by` (Select: Invoice No / Invoice+Amount / Party+Amount / Name+Amount / Manual / None)
- `suggested_party_type`, `suggested_party`
- `suggested_invoices` (Table — child: `Bank Txn Invoice Suggestion`)
- `difference_amount` (Currency — txn.amount − sum matched invoices)
- `reconcile_notes` (Small Text)

#### Custom fields on `Bank Account` (ERPNext native, v2 scaffold)
- `api_source` (Link Bank Data Source, optional)
- `api_credentials` (Password — Frappe encrypts)
- `api_config_json` (Small Text — endpoints, client_id, extra params)
- `api_last_sync_at` (Datetime)
- `api_last_cursor` (Data — pagination resume)

**Not used v1** — schema pre-allocated so v2 doesn't require DB migrate.

#### `Bank Statement Settings` (Single DocType)

Matching rules section:
- `enable_matcher_invoice_no` (default ON)
- `enable_matcher_invoice_amount` (default ON)
- `enable_matcher_party_amount` (default ON)
- `enable_matcher_name_amount` (default ON, Low confidence)
- `enable_multi_invoice_match` (default ON — only runs after party identified)
- `multi_invoice_max_combinations` (default 5)
- `amount_date_tolerance_days` (default 3)
- `invoice_number_patterns` (Small Text — list regex, one per line. Seed: `ACC-SI-\d{4}-\d+`, `ACC-PI-\d{4}-\d+`, `SI-\d+`, `PINV-\d+`)

Tolerance section:
- `tolerance_type` (Fixed Amount / Percent, default Fixed)
- `tolerance_fixed_amount` (default 1000 VND)
- `tolerance_percent` (default 0.1%)

PE behavior:
- `default_pe_action` (Draft / Submit, default Draft)
- `default_mode_of_payment_credit` (Link Mode of Payment — user sets on install, no hardcoded default; suggest "Wire Transfer" / "Bank Draft")
- `default_mode_of_payment_debit` (Link Mode of Payment — user sets on install)
- `difference_account` (Link Account, optional) — tài khoản hạch toán chênh lệch nhỏ ≤ tolerance vào Deductions của PE. Theo TT99/2025 thường là TK 6415/6425/6427 "Phí ngân hàng". Nếu NULL → chênh lệch ≤ tolerance được ignore (PE không có Deductions row). Xem §14.3.

Match rules child table (L2 reorder / toggle):
- `rules` (Table `Bank Match Rule`): `rule_key` (Link Bank Matcher Type), `enabled`, `priority` (Int — drag to reorder), `confidence_override` (Select), `tolerance_override` (Currency), `bank_account` (Link — L6 scaffold, null=global)

#### `Bank Matcher Type` (fixture registry)
- `matcher_key` (unique), `matcher_label`, `handler_path`, `default_confidence`, `description`
- **Fixtures v1:** `invoice_no`, `invoice_amount`, `party_amount`, `name_amount`

#### `Bank Match Rule` (child table of Settings)

Referenced above.

#### `Bank Txn Invoice Suggestion` (child table of Bank Transaction)
- `invoice_type` (Sales Invoice / Purchase Invoice)
- `invoice_name` (Dynamic Link)
- `outstanding_amount`
- `allocated_amount`
- `selected` (Check)

## 4. Match Engine

### 4.1 Data types & helpers

**ERPNext `Bank Transaction` field mapping** — native fields don't use `amount`/`direction`; helpers bridge the gap:

```python
# vn_banking/match/helpers.py
def get_txn_amount(txn) -> Decimal:
    """Return the absolute transaction amount (credit OR debit)."""
    return Decimal(txn.deposit or 0) or Decimal(txn.withdrawal or 0)

def get_txn_direction(txn) -> str:
    """Return 'credit' (money in) or 'debit' (money out)."""
    return "credit" if (txn.deposit or 0) > 0 else "debit"

def is_txn_matched(txn) -> bool:
    return txn.match_confidence in ("High", "Medium", "Low")

def get_txn_bank_ref(txn) -> str:
    """ERPNext native field name is `reference_number`, not `bank_ref`."""
    return txn.reference_number or ""
```

**Normalized transaction** (pre-persistence, output of Source layer):

```python
# vn_banking/source/base.py
@dataclass
class NormalizedTransaction:
    date: date
    deposit: Decimal             # money in (credit), 0 if debit
    withdrawal: Decimal          # money out (debit), 0 if credit
    description: str             # narration
    reference_number: str        # bank's ref/transaction id
    counter_account_no: str      # other party's bank account (may be empty)
    counter_account_name: str    # other party's name on statement (may be empty)
    raw_row: dict                # original row data for audit
```

**Match interfaces:**

```python
# vn_banking/match/base.py
@dataclass
class InvoiceRef:
    doctype: str
    name: str
    outstanding: Decimal
    allocated: Decimal

@dataclass
class MatchCandidate:
    party_type: str           # "Customer" | "Supplier"
    party: str
    invoices: list[InvoiceRef]
    total_allocated: Decimal
    difference: Decimal
    confidence: str           # "High" | "Medium" | "Low"
    matched_by: str
    explanation: str          # human-readable for side panel

class BaseMatcher(ABC):
    key: str
    label: str
    default_confidence: str

    @abstractmethod
    def applicable(self, txn, ctx) -> bool: ...

    @abstractmethod
    def match(self, txn, ctx) -> list[MatchCandidate]: ...
```

### 4.2 Context object

Built once per import, shared across all matchers to avoid N+1:

```python
class MatchContext:
    direction: "credit" | "debit"
    party_invoice_type: "Sales Invoice" | "Purchase Invoice"
    party_type: "Customer" | "Supplier"
    bank_account: str
    company: str
    posting_date_window: tuple[date, date]   # txn.date ± tolerance_days
    outstanding_invoices: dict[party, list[InvoiceRef]]  # preloaded 1 SQL
    party_by_bank_account: dict[str, str]    # bank_acc_no → party name
    tolerance: Decimal
    settings: BankStatementSettings
```

### 4.3 Matchers

**`InvoiceNoMatcher` (key: invoice_no, default High)**
- Regex extract invoice numbers từ narration using `settings.invoice_number_patterns`
- Lookup each match in `outstanding_invoices`
- Multi-invoice auto-handled: regex tìm được N mã → candidate gom cả N
- Confidence:
  - Tìm ≥1 HĐ outstanding, tổng = txn.amount → High
  - Tổng chênh ≤ tolerance → Medium
  - Không khớp amount → Low
- Explanation: `"Tìm thấy [SI-0123] trong nội dung. Số tiền khớp chính xác."`

**`InvoiceAmountMatcher` (key: invoice_amount, default Medium)**
- Chỉ chạy nếu `InvoiceNoMatcher` không ra candidate
- Tìm SI/PI outstanding có `outstanding_amount == txn.amount ± tolerance` (NOT grand_total — chỉ quan tâm phần còn nợ) trong `posting_date_window`
- 1 invoice khớp duy nhất → Medium
- ≥2 invoices khớp cùng số tiền → không emit candidate (avoid false positive)
- Explanation: `"Khớp duy nhất với [SI-0456] theo số tiền còn nợ và ngày."`

**`PartyAmountMatcher` (key: party_amount, default Medium)**
- Lookup party từ `txn.counter_account` trong `party_by_bank_account`
- Nếu không tìm được party → skip
- Tìm outstanding invoices của party có `outstanding_amount == txn.amount ± tolerance` → Medium
- Multi-invoice (nếu `enable_multi_invoice_match=1`):
  - `combinations_sum_match(party_invoices, txn.amount, k ≤ multi_invoice_max_combinations)`
  - Iterate k từ 2 đến max, yield combo đầu tiên có sum ≈ amount
  - Nếu nhiều combo → pick combo có min(k), rồi earliest date
  - Giới hạn k ≤ 5 (C(20,5) = 15504, acceptable)
- Explanation: `"Party [ABC Corp] theo số TK đối ứng. Gợi ý tổ hợp 2 hoá đơn: SI-0100 + SI-0101."`

**`NameAmountMatcher` (key: name_amount, default Low)**
- Chỉ chạy khi 3 matchers trên đều fail
- Fuzzy match party name (rapidfuzz ratio ≥ 80) trên narration
- Nếu 1 party match → tìm outstanding invoices khớp amount → Low
- Explanation: `"Tên 'CTY ABC' gần khớp với [ABC Corp] (confidence 85%). Cần xác nhận thủ công."`

### 4.4 Pipeline execution

```python
def run_match_engine(import_doc):
    ctx = build_context(import_doc)
    rules = get_enabled_rules_in_priority_order()
    transactions = frappe.get_all(
        "Bank Transaction",
        filters={"bank_statement_import": import_doc.name},
        fields=["name"],
    )
    for txn_name in transactions:
        txn = frappe.get_doc("Bank Transaction", txn_name.name)
        direction = get_txn_direction(txn)
        tctx = ctx.for_direction(direction)
        matched = False
        for rule in rules:
            if rule.bank_account and rule.bank_account != import_doc.bank_account:
                continue  # L6: per-bank override (scaffold)
            matcher = instantiate(rule.rule_key, rule.params)
            if not matcher.applicable(txn, tctx):
                continue
            candidates = matcher.match(txn, tctx)
            if candidates:
                best = pick_best(candidates)
                apply_to_txn(txn, best, rule)
                matched = True
                break  # first-hit-wins
        if not matched:
            txn.match_confidence = "None"
        txn.save()
```

### 4.5 Post-match action

Auto PE creation scoped **High only**. Medium/Low never auto-create — always wait for user confirmation regardless of `default_pe_action`:

- `match_confidence=High` → auto-create Payment Entry. Respect `default_pe_action`:
  - `Draft` (default) → PE created with `docstatus=0`
  - `Submit` → PE created with `docstatus=1`
  - Link to txn via `Bank Transaction.payment_entries` child table (native ERPNext field, type "Bank Transaction Payments")
- `match_confidence=Medium|Low` → save `suggested_party` + `suggested_invoices`, DO NOT create PE. User confirms in side panel. (Even if `default_pe_action=Submit`, user review is required for non-High confidence.)
- `match_confidence=None` → no action. User handles manually via side panel dropdowns.

## 5. UI: Bank Reconcile Page

### 5.1 Philosophy

**Sane defaults + progressive disclosure.** 95% of users never open Settings. Everything happens on one screen.

### 5.2 Stack

Frappe desk page + vanilla JS / jQuery. No React/Vue for v1 — follows ERPNext's existing Bank Reconciliation Tool pattern.

### 5.3 File layout

```
vn_banking/vn_banking/page/bank_reconcile/
  bank_reconcile.json            # page definition
  bank_reconcile.js              # entry point
  bank_reconcile.html            # main layout template
  bank_reconcile.css
  components/
    upload_dialog.js
    txn_table.js
    txn_side_panel.js
    bulk_actions_bar.js
    stat_bar.js
```

### 5.4 Layout

```
┌─────────────────────────────────────────────────────────────┐
│ [Bank Account ▼]  [Upload File]  [Filter: Vào/Ra/Tất cả]   │  toolbar
│ Summary: 120 GD · 85 khớp · 20 gợi ý · 15 chưa · chênh 12k │  stat bar
├─────────────────────────────────────────────────────────────┤
│ ● │ Ngày   │ Nội dung          │ Số tiền  │ Party │ Khớp   │
│ 🟢│ 08/04  │ TT HD SI-0123...  │ 12.5M ↓  │ ABC   │ SI-0123│
│ 🟡│ 08/04  │ CTY XYZ thanh...  │ 8.0M ↓   │ XYZ?  │ ? SI   │
│ 🔴│ 08/04  │ NAP TIEN MAT      │ 5.0M ↑   │ —     │ —      │
│ 🟢│ 08/04  │ ... (2 HĐ)        │ 20.0M ↓  │ DEF   │ 2 HĐ   │
├─────────────────────────────────────────────────────────────┤
│ [✓ Tạo PE nháp cho 85 dòng khớp]  [Submit tất cả PE nháp] │  bulk
│            ⚙ Tinh chỉnh match engine  (small link, corner)  │
└─────────────────────────────────────────────────────────────┘
```

### 5.5 Confidence colors

4 confidence levels → 3 main colors + a badge for Low to distinguish:

- 🟢 **High** → PE nháp đã auto-create, tick và bulk submit
- 🟡 **Medium** → có gợi ý chắc chắn, chờ user xác nhận trong side panel
- 🟠 **Low** (fuzzy name match) → hiển thị cùng 🟡 ở eye-level nhưng có badge "Cần xác nhận" màu orange; filter dropdown cho phép show/hide Low riêng
- 🔴 **None** → chưa có gợi ý, user chọn party + invoice manually

**Simplification alternative nếu design team thấy phức tạp:** collapse Low vào cùng 🟡 Medium, chỉ differentiate bằng text "(fuzzy)" cạnh tên party. Quyết định cuối trong T16.

### 5.6 Side panel (click row)

```
┌─ Side Panel ─────────────────┐
│ Giao dịch #42                │
│ Nội dung: "TT HD SI-0123..." │
│ Số tiền: 12.500.000đ Vào     │
│ Ngày: 08/04/2026             │
│                              │
│ ▸ Vì sao hệ thống gợi ý vậy? │  expand → full explanation
│   Khớp theo: Số HĐ trong nội │
│   dung. Độ tin cậy: Cao.     │
│                              │
│ Customer:  [ABC Corp    ▼]   │  filter SI khi đổi customer
│ Hoá đơn:   [SI-0123     ▼]   │
│ Chênh lệch: 0đ ✓             │
│                              │
│ [Tạo PE nháp] [Tạo & Submit] │
│ [Bỏ qua dòng này]            │
└──────────────────────────────┘
```

### 5.7 Bulk actions

- **"Tạo PE nháp cho N dòng khớp cao"** — batch tạo PE draft cho tất cả dòng 🟢
- **"Submit tất cả PE nháp"** — submit all draft PE đã tạo
- Progress bar via Frappe realtime socket for batches > 50

### 5.8 Empty state / error state

- Upload sai format → hiện tên format detected + dropdown chọn format khác
- 0 GD khớp → gợi ý kiểm tra số TK trong Bank Account master
- Parse error → show error log in expandable panel

### 5.9 Settings UI (hidden link, power user)

Accessible via small link `⚙ Tinh chỉnh match engine` at page top-right, opens Bank Statement Settings in new tab.

**Tab "Cơ bản"** (default view):
- Tolerance: "Chấp nhận chênh lệch đến: [1.000] đ"
- Khoảng ngày kiểm tra: "[3] ngày"
- Tạo PE mặc định: [Nháp ▼]

**Tab "Nâng cao"** (accordion "Hiện tuỳ chọn chuyên gia"):
- Toggle matchers với drag-to-reorder priority
- Per-matcher params override
- "Test on last import" preview button — runs current config against last import, shows diff
- Regex patterns textarea (seeded)

### 5.10 Re-run match after Settings change

Settings mở ở tab mới nên Bank Reconcile page cần biết khi user đã save Settings:
- Bank Reconcile có nút "🔄 Chạy lại match engine" hiện trên toolbar khi có import đang mở
- Khi user save Bank Statement Settings, Frappe fires `doc_update` event → Bank Reconcile JS listen qua `frappe.realtime.on('bank_statement_settings_updated')` → show yellow banner "Settings đã đổi — Chạy lại match?" với nút re-run
- Click re-run → call `trigger_rematch(import_name)` API → background job → stats + table refresh via realtime

Thêm API endpoint vào §7: `trigger_rematch(import_name)` → re-runs match engine on existing import without re-parsing file.

## 6. Warnings & Validation

Per requirement §3 "Cảnh báo thiếu thông tin / chênh lệch":

- **Thiếu party**: row 🔴, empty suggested_party, warning icon
- **Chênh lệch > tolerance**: row 🟡, warning icon, `difference_amount` hiển thị
- **Thiếu số HĐ trong narration**: downgrade confidence từ High → Medium (có thể)
- **Dedupe hit**: row bị skip khi ingestion, hiển thị trong stat bar "X duplicate skipped"
- **Parse errors**: log trong `Bank Statement Import.log`, hiển thị expandable trong UI

## 7. API Endpoints

All in `vn_banking/api/reconcile.py`, `@frappe.whitelist()`:

- `trigger_import(bank_account, source_type, file_url=None, from_date=None, to_date=None)` → source-agnostic entry point. Returns `import_name`. Background job if rows > 200.
- `get_import_transactions(import_name, direction_filter="all")` → list GD + candidates
- `get_suggestions(transaction_name)` → recompute candidates (used when user changes party in side panel)
- `get_customer_invoices(customer, from_date, to_date)` → list SI outstanding for dropdown
- `get_supplier_invoices(supplier, from_date, to_date)` → same for PI
- `create_payment_entry(transaction_name, party_type, party, invoices, mode_of_payment, submit=False)` → create PE linked to Bank Transaction
- `bulk_create_pe(import_name, only_high_confidence=True, submit=False)`
- `dismiss_transaction(transaction_name)` → mark as skipped
- `explain_match(transaction_name)` → return explanation string
- `test_matching_on_last_import(settings_override_json)` → dry-run new settings on last import, return diff
- `trigger_rematch(import_name)` → re-run match engine on existing import (no re-parse); used after Settings change

## 8. Background jobs & scheduler (v2 scaffold)

In `hooks.py`:

```python
# v2 scaffold — uncomment when API sources implemented
# scheduler_events = {
#     "hourly": ["vn_banking.tasks.sync_all_api_banks"],
# }
```

`vn_banking/tasks.py:sync_all_api_banks()` stub with `raise NotImplementedError` + docstring.

`vn_banking/api/webhook.py:receive_bank_push()` stub for bank push notifications.

## 9. File layout

```
apps/vn_banking/
├── pyproject.toml
├── README.md
├── .gitignore
├── vn_banking/
│   ├── __init__.py                          # __version__ = "0.0.1"
│   ├── hooks.py
│   ├── modules.txt                          # "VN Banking"
│   ├── patches.txt                          # empty but required
│   ├── config/
│   │   └── desktop.py
│   ├── fixtures/
│   │   ├── bank_statement_format.json       # 7 banks
│   │   ├── bank_matcher_type.json           # 4 matchers
│   │   ├── bank_data_source.json            # excel_upload
│   │   └── custom_field.json                # Bank Transaction + Bank Account extensions
│   ├── vn_banking/
│   │   ├── doctype/
│   │   │   ├── bank_statement_format/
│   │   │   ├── bank_statement_import/
│   │   │   ├── bank_statement_settings/
│   │   │   ├── bank_match_rule/             # child
│   │   │   ├── bank_matcher_type/
│   │   │   ├── bank_data_source/
│   │   │   └── bank_txn_invoice_suggestion/ # child
│   │   └── page/
│   │       └── bank_reconcile/
│   ├── source/
│   │   ├── __init__.py
│   │   ├── base.py                          # BankDataSource ABC
│   │   └── excel.py                         # ExcelFileSource
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── base.py                          # openpyxl + xlrd fallback
│   │   ├── normalizer.py                    # date/amount parse, dedupe hash
│   │   └── detect.py                        # auto-detect format from file
│   ├── match/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── engine.py
│   │   ├── context.py
│   │   ├── invoice_no.py
│   │   ├── invoice_amount.py
│   │   ├── party_amount.py
│   │   ├── name_amount.py
│   │   └── combinations.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── reconcile.py
│   │   └── webhook.py                       # v2 stub
│   ├── tasks.py                             # v2 stub
│   ├── install.py                           # after_install: seed defaults
│   └── tests/
│       ├── fixtures/                        # sample bank Excel files
│       ├── test_parser_vcb.py
│       ├── test_parser_bidv.py
│       ├── test_parser_all_formats.py
│       ├── test_source_excel.py
│       ├── test_matcher_invoice_no.py
│       ├── test_matcher_party_amount.py
│       ├── test_matcher_combinations.py
│       ├── test_engine_pipeline.py
│       ├── test_dedupe.py
│       └── test_reconcile_api.py
```

## 10. Task Breakdown

S = ≤1h, M = 2-4h, L = 4-8h.

| # | Task | Effort | Depends |
|---|---|---|---|
| T1 | App scaffold (pyproject, hooks, modules, patches, __init__, dual-remote setup) | S | — |
| T2 | DocTypes core: Format, Import, Settings, MatchRule, MatcherType, DataSource, InvoiceSuggestion child | M | T1 |
| T3 | Custom fields: Bank Transaction + Bank Account (fixture) | S | T1 |
| T4 | `BankDataSource` interface + `NormalizedTransaction` + Parser base + normalizer + dedupe hash | M | T1 |
| T5 | `ExcelFileSource` implementation + auto-detect | M | T4 |
| T6 | 7 bank format fixtures + sample test files | L | T5, T2 |
| T7 | Match engine: BaseMatcher, Context, Engine, pipeline runner | M | T2 |
| T8 | `InvoiceNoMatcher` + tests | M | T7 |
| T9 | `InvoiceAmountMatcher` + tests | S | T7 |
| T10 | `PartyAmountMatcher` + combinations + tests | M | T7 |
| T11 | `NameAmountMatcher` + tests (rapidfuzz dep) | S | T7 |
| T12 | `trigger_import` API + background job + realtime progress | M | T4-T7 |
| T13 | Reconcile API endpoints (get/suggest/create_pe/bulk/dismiss/explain) | M | T12 |
| T14 | Custom page scaffold + routing + CSS | M | T2 |
| T15 | Upload dialog + progress UI + realtime socket | M | T14, T12 |
| T16 | Transaction table + confidence colors + filter Vào/Ra/Tất cả | M | T14, T13 |
| T17 | Side panel: explanation + party/invoice dropdowns + create PE | L | T16, T13 |
| T18 | Bulk actions bar + bulk create PE | M | T16, T13 |
| T19 | Stats bar + empty/error states | S | T16 |
| T20 | Settings UI: tab Cơ bản + tab Nâng cao (toggle + drag reorder) | M | T2, T7 |
| T21 | "Test on last import" preview button | M | T20, T12 |
| T22 | Workspace sidebar integration + module icon | S | T14 |
| T23 | v2 stubs: `sync_all_api_banks`, webhook, commented scheduler hook | S | T1 |
| T24 | End-to-end QA with sample files (all 7 banks) + console error cleanup | M | all |
| T25 | README + usage docs + settings reference | S | all |

**Total: 25 tasks, foundation (T1-T13) parallelizable with UI (T14-T21) once API contract is set.**

## 11. Acceptance Criteria v1

- [ ] Upload sao kê VCB thật → parse ra đúng số dòng giao dịch, decimals + dates correct
- [ ] All 7 bank format fixtures parse cleanly on sample files (test passes)
- [ ] Match engine nhận ra ≥80% GD có số HĐ rõ trong narration (với fixture test data)
- [ ] Multi-invoice: upload file có 1 GD = 3 SI → gợi ý đúng combo khi party identified
- [ ] Dedupe: upload lại cùng file → 0 GD mới tạo ra
- [ ] Tạo PE từ UI single row → PE tồn tại, link đúng SI, mode_of_payment set, reference_no set, posting_date = txn.date
- [ ] Bulk "tạo PE nháp cho N dòng khớp cao" → N PE draft xuất hiện
- [ ] Submit tất cả PE nháp **thuộc import đang mở** → outstanding_amount của các SI liên quan giảm đúng (không ảnh hưởng PE draft của import khác)
- [ ] Settings tab Cơ bản: đổi tolerance → test preview → kết quả cập nhật
- [ ] Settings tab Nâng cao: tắt `NameAmountMatcher` → GD match Low biến mất khỏi kết quả khi re-run
- [ ] Side panel explanation hiển thị đúng matcher đã trúng + lý do
- [ ] Không console error trong toàn bộ flow (upload → submit)
- [ ] `BankDataSource` interface exists + 1 implementation (Excel) + 1 fixture (excel_upload)
- [ ] v2 scaffold: `Bank Account` has api_* custom fields; `tasks.py` and `webhook.py` stubs exist; scheduler hook commented; docstrings explain future use
- [ ] Both git remotes pushed: `goldrag1/vn_banking` + `dcnet-cloud/dcnet-banking`

## 12. Out of Scope (explicit)

- Dự báo dòng tiền (sub-project riêng, liên quan Contract + PAKD modules)
- Khế ước vay / Loan tracking
- Tỷ giá hối đoái (dùng ERPNext native)
- `BankApiSource` implementation (v2 — only scaffold v1)
- Custom regex matchers user-defined via UI (L4)
- ML-based confidence scoring (L5)
- Per-bank-account rule override UI (L6 — schema only)
- Mobile UI (desk-only v1)
- Multi-currency statement in single file (v1 assumes single currency per import, default VND)

## 13. Operational Details

### 13.1 Dependencies

`pyproject.toml`:
- `frappe>=16.0.0`
- `erpnext>=16.0.0` (needs Bank Transaction, Bank Account, Payment Entry, Sales/Purchase Invoice)
- `openpyxl` (xlsx parsing — already in Frappe)
- `xlrd>=2.0` (xls legacy — add to requirements)
- `rapidfuzz>=3.0` (fuzzy name matching — add to requirements)

### 13.2 Permissions

Page access + DocType read/write scoped to roles:
- **Accounts User** (default ERPNext role): can access Bank Reconcile page, upload, create draft PE, confirm matches
- **Accounts Manager**: additionally can submit PE, modify Bank Statement Settings
- **System Manager**: full access including Bank Statement Format fixtures, Bank Matcher Type
- **Others**: no access

Set via `permissions` block in each DocType JSON.

### 13.3 Hooks wiring

`hooks.py`:
```python
app_name = "vn_banking"
app_version = "0.0.1"

after_install = "vn_banking.install.after_install"
after_migrate = "vn_banking.install.after_migrate"  # ensures fixture upsert

fixtures = [
    {"dt": "Bank Statement Format"},
    {"dt": "Bank Matcher Type"},
    {"dt": "Bank Data Source"},
    {"dt": "Custom Field", "filters": [["name", "like", "Bank Transaction-%"]]},
    {"dt": "Custom Field", "filters": [["name", "like", "Bank Account-%"]]},
]

# v2 scaffold — commented until API sources implemented
# scheduler_events = {
#     "hourly": ["vn_banking.tasks.sync_all_api_banks"],
# }
```

### 13.4 Test runner

Frappe's native test runner:
```bash
bench --site dcnet.localhost run-tests --app vn_banking
```

Tests inherit from `frappe.tests.utils.FrappeTestCase`. Fixture Excel files in `vn_banking/tests/fixtures/` committed to repo (anonymized real samples or generated mocks).

### 13.5 Workspace integration

New workspace "Banking VN" (or merge into existing "Banking" workspace — decide at T22). Sidebar entry points:
- Link Card → Bank Reconcile page
- Link Card → Bank Statement Import list
- Link Card → Bank Statement Settings (Single)
- Shortcut → "Upload new statement" (opens Bank Reconcile page with upload dialog open)

## 14. Resolved Decisions

### 14.1 Sample Excel files (status: pending collection)
User đang xin sample sao kê thật từ các bank. T6 (bank format fixtures) sẽ:
- Start với VCB + 1 bank khác khi có sample đầu tiên
- Còn lại scaffold với mock generated tests, backfill fixture khi sample về
- Task T6 có thể split thành T6a (VCB + mock generator) và T6b (các bank còn lại, backfill)

### 14.2 Invoice number patterns — flexible config
`invoice_number_patterns` trong Bank Statement Settings là **Small Text, multi-line regex list**, configurable fully by user. Không hardcode pattern theo bất kỳ naming series cụ thể nào.

**Future-proof cho VAT invoice:** DCNet sẽ có thêm mã hoá đơn điện tử VAT (HĐĐT theo TT78/2021 và TT99/2025). Các pattern có thể cùng tồn tại:
- Pattern nội bộ ERPNext: `ACC-SI-\d{4}-\d+`, `SI-\d+`
- Pattern HĐĐT VAT (ví dụ): `\d{2}[A-Z]{3}\d{2}/\d+` (ký hiệu mẫu + số), hoặc `K\d{2}[A-Z]{3}\d{3}/\d{7}`
- User tự thêm/sửa pattern trong Settings, không cần đổi code

`InvoiceNoMatcher` iterates all patterns, collects all matches, lookups in `outstanding_invoices`. Seed fixture pattern v1 bao gồm cả ERPNext naming và placeholder cho HĐĐT với comment giải thích format.

### 14.3 Difference write-off — theo Thông tư 99/2025

Chuẩn kế toán VN theo TT99/2025: chênh lệch nhỏ giữa số thực tế nhận/chi và số trên hoá đơn (thường do phí chuyển khoản, chênh lệch làm tròn) được hạch toán vào **tài khoản chi phí phù hợp** — không phải write-off qua tài khoản đặc biệt.

Thực tế phổ biến:
- **Phí chuyển khoản bị trừ vào thu** (VD: nhận 12.499.500đ thay vì 12.500.000đ) → chênh 500đ hạch toán vào TK **6415 / 6427 / 6425** (chi phí dịch vụ mua ngoài — "Phí ngân hàng"), tuỳ CoA của công ty
- **Chênh lệch làm tròn** → TK **635** (chi phí tài chính khác) hoặc **811** (chi phí khác), ít dùng
- **Chênh lệch lớn** (> tolerance) → không tự động write-off, phải user review

**Implementation v1:**
- Thêm field `difference_account` (Link Account) vào Bank Statement Settings — user chọn tài khoản mặc định để hạch toán chênh lệch nhỏ. Gợi ý default: account có tên chứa "Phí ngân hàng" hoặc TK 6415/6425/6427 trong VN COA, nhưng không hardcode — user chọn khi setup
- Khi tạo PE với difference ≤ tolerance VÀ `difference_account` đã set → PE thêm row trong Deductions child table với `account = difference_account`, `amount = difference`, `cost_center = default`
- Khi `difference_account` NULL → giữ hành vi cũ (ignore difference ≤ tolerance, không hạch toán chênh lệch)
- Difference > tolerance → không auto write-off dù config có; row hiển thị warning 🟡, user quyết định thủ công

**Acceptance criterion bổ sung §11:**
- [ ] Khi `difference_account` set và txn có chênh lệch = 500đ (≤ tolerance), PE được tạo có 1 row Deductions link tới `difference_account` với amount = 500đ
- [ ] Khi `difference_account` NULL, cùng txn → PE có 0 row Deductions, PE.total_allocated_amount khớp txn.amount
- [ ] Khi chênh lệch = 5000đ (> tolerance 1000đ), PE không tự tạo; row hiển thị 🟡 warning "chênh lệch vượt ngưỡng"

## 15. Design Decision Rationales (Trụ cột 2)

Mỗi quyết định kiến trúc non-obvious có giải thích tại sao chọn approach này và đã reject gì.

### 15.1 Dùng Bank Transaction native thay vì custom DocType

> **Why:** ERPNext Bank Reconciliation Tool, Payment Entry reconciliation, và GL Entry posting đều đọc từ `tabBank Transaction`. Custom DocType sẽ cần duplicate toàn bộ linking logic. Custom fields trên native DocType là cách ít xâm phạm nhất.
> **Rejected:** Custom `VN Bank Transaction` DocType — mất tích hợp native, phải viết lại PE linking.

### 15.2 Bank Statement Import NOT submittable, dùng `status` field

> **Why:** Import là workflow container — user tạo, upload, review, tạo PE dần dần qua nhiều lần. Submittable (docstatus=1) lock child rows và không cho phép edit sau submit. Status field (Draft/Parsed/Reviewed/Posted) linh hoạt hơn cho workflow dài.
> **Rejected:** `is_submittable=1` — child table Bank Transaction bị read-only sau submit, chặn việc user update match/PE từng dòng.

### 15.3 Config-driven parser (Bank Statement Format) thay vì per-bank code

> **Why:** Thêm bank mới = thêm 1 record trong Format DocType (admin làm được), không cần developer viết code + deploy. 4 banks hiện tại khác nhau chỉ ở column position, header row, date format — hoàn toàn config-driven.
> **Rejected:** Per-bank Python parser (bidv.py, mb_bank.py) — code maintenance cao, mỗi bank mới cần dev, không self-service.

### 15.4 Reverse link (Bank Transaction.bank_statement_import) thay vì child table trên Import

> **Why:** Bank Transaction là ERPNext native DocType, cần independently editable (user tạo PE từng dòng, update match). Child table trên Import sẽ lock khi parent saved, và Frappe child tables không hỗ trợ Link tới existing top-level DocType.
> **Rejected:** Child table on Import — Frappe child table yêu cầu dedicated child DocType, không thể reference Bank Transaction trực tiếp.

### 15.5 First-hit-wins matcher pipeline thay vì score aggregation

> **Why:** Kế toán cần kết quả deterministic — cùng giao dịch luôn ra cùng kết quả. Score aggregation (tổng điểm từ nhiều matcher) tạo ra "gray zone" khi 2 candidate cùng score, gây confusion. First-hit-wins với priority rõ ràng = predictable + debuggable.
> **Rejected:** Score aggregation across matchers — non-deterministic khi scores gần nhau, khó explain cho user.

### 15.6 Confidence levels (High/Medium/Low/None) thay vì numeric score

> **Why:** Kế toán không quan tâm "score 73 vs 81" — họ cần biết "tin được hay phải kiểm tra?". 4 mức confidence maps trực tiếp sang UX action: High=auto PE, Medium=review gợi ý, Low=cần xác nhận, None=manual. Numeric score phải thêm threshold config phức tạp.
> **Rejected:** Numeric 0-100 score — cần threshold mapping, khó giải thích cho non-tech user.

### 15.7 Vanilla JS / jQuery thay vì React/Vue

> **Why:** ERPNext Bank Reconciliation Tool dùng Frappe page + vanilla JS. Consistency với codebase ERPNext giúp kế toán quen giao diện. React/Vue cần build toolchain riêng, tăng complexity cho 1 page duy nhất.
> **Rejected:** React SPA — build complexity, CSRF handling, separate state management cho 1 page.

### 15.8 Auto-PE chỉ High confidence

> **Why:** Tạo Payment Entry sai = sai sổ kế toán. High confidence (invoice number khớp chính xác + amount match) là threshold an toàn duy nhất cho auto-create. Medium/Low yêu cầu human judgment — sai invoice link = sai công nợ.
> **Rejected:** Auto-PE cho Medium — risk false positive: cùng số tiền nhưng khác invoice → PE link sai invoice → outstanding sai.

### 15.9 Fuzzy threshold ≥80 (rapidfuzz)

> **Why:** Thử nghiệm trên narration thực tế VN: "CTY TNHH ABC" vs "Công ty TNHH ABC" = ratio ~85. "CTY ABC" vs "ABC Corp" = ratio ~60. Threshold 80 bắt được viết tắt phổ biến VN (CTY/Cty/CÔNG TY) nhưng loại bỏ false positive từ tên ngắn trùng partial.
> **Rejected:** Threshold 70 — quá nhiều false positive từ tên công ty ngắn (3-4 ký tự).

### 15.10 Multi-invoice max k=5 combinations

> **Why:** C(20,5) = 15504 iterations — chạy <100ms trên Python. k=6 → C(20,6) = 38760, vẫn OK nhưng real-world hiếm khi 1 giao dịch thanh toán >5 hoá đơn cùng lúc. k=5 là balance giữa coverage và performance.
> **Rejected:** k=10 — C(20,10) = 184756, slow + unrealistic business scenario.

### 15.11 difference_account trong Settings thay vì hardcode

> **Why:** VN COA có nhiều tài khoản phù hợp (6415/6425/6427/635/811) tuỳ công ty. Hardcode 1 TK = sai cho các COA khác TT99/2025. Settings field cho admin chọn đúng TK của mình.
> **Rejected:** Hardcode TK 6415 — không portable qua các COA template khác.

### 15.12 openpyxl thay vì csv/pandas cho xlsx

> **Why:** Bank statement xlsx files có merged cells (MB Bank), multiple sheets, date formatting (Excel serial dates). openpyxl đã có trong Frappe dependency, xử lý đúng tất cả edge case này. csv.reader không đọc được xlsx. pandas overkill cho row iteration.
> **Rejected:** `pandas.read_excel` — heavier dependency, openpyxl đủ; `csv.reader` — không đọc xlsx.

## 16. Edge Cases — Khi nào khác? (Trụ cột 1+4)

### 16.1 Match Engine

**InvoiceNoMatcher:**
- **Narration có nhiều số HĐ nhưng chỉ một số outstanding:** matcher gom tất cả invoice numbers tìm được, lookup từng cái. Chỉ những invoice có outstanding > 0 được đưa vào candidate. Invoice đã paid bị bỏ qua silently.
- **Cùng invoice number xuất hiện 2 lần trong narration:** regex `findall` trả về list unique matches. Duplicate bị dedupe trước lookup.
- **Invoice number format thay đổi giữa các kỳ (VD: ACC-SI-2025 → ACC-SI-2026):** patterns trong Settings chứa `\d{4}` wildcard, bắt được cả 2 năm. Nếu naming series thay đổi hoàn toàn, admin thêm pattern mới.

**InvoiceAmountMatcher:**
- **Nhiều invoice cùng outstanding amount:** matcher KHÔNG emit candidate — trả về empty list. Tránh false positive. User handle manually qua side panel.
- **Invoice từ company khác (multi-company bench):** `build_context` filter `outstanding_invoices` theo `company` của Bank Account. Chỉ invoice cùng company được xét.
- **Invoice posting_date ngoài tolerance window (VD: hoá đơn 6 tháng trước):** default `amount_date_tolerance_days=3`, invoice ngoài window bị loại. Nếu user cần rộng hơn, tăng tolerance trong Settings.

**PartyAmountMatcher:**
- **counter_account_no trống hoặc không nhận dạng được:** matcher skip — `applicable()` return False khi không tìm được party từ `party_by_bank_account`.
- **Nhiều party dùng cùng bank account number:** `party_by_bank_account` chỉ lưu entry mới nhất (last write wins). Edge case hiếm — 2 công ty chung 1 TK ngân hàng. Giải pháp: admin cập nhật Bank Account master.
- **Combination explosion khi tolerance cao:** `max_k=5` hard limit + tolerance filter loại bỏ combos ngoài range trước khi enumerate.

**NameAmountMatcher:**
- **Fuzzy match trả về nhiều party ≥80%:** matcher chỉ lấy top 1 (highest ratio). Nếu 2 party cùng score, lấy alphabetical first — deterministic.
- **Tên party quá ngắn (VD: "ABC"):** partial_ratio trên string ngắn dễ false positive. Confidence luôn Low — user phải xác nhận.

### 16.2 Auto-PE Creation

- **PE creation thất bại (thiếu permission, accounting validation):** `create_payment_entry` wrapped trong try/except, lỗi ghi vào `bulk_create_pe` response `errors` list. Transaction giữ nguyên status, không mất data.
- **Cùng transaction matched 2 lần qua 2 import:** `dedupe_hash` ngăn duplicate Bank Transaction. Nếu cùng file upload 2 lần → 0 new txns. Nếu 2 file khác nhau có cùng giao dịch → cùng hash → skip.
- **User có nhiều Bank Account cùng bank:** `detect_format_and_bank` trả về bank_account=null nếu >1 match, user phải chọn thủ công trong upload dialog.

### 16.3 Dedupe Logic

- **Hash collision (SHA-256):** probability negligible (~1/2^256). Trong phạm vi ngân hàng VN (triệu giao dịch/năm), collision không xảy ra.
- **Re-upload file có 1 dòng khác (sửa lỗi):** dòng mới có hash khác → tạo Bank Transaction mới. Dòng cũ đã dedupe → skip. Kết quả: 1 new txn added. Nếu dòng cũ đã reconciled, new txn duplicate cần user dismiss thủ công.
- **Date format thay đổi nhưng amount/ref giống:** hash input dùng `date.isoformat()` (YYYY-MM-DD) — format-independent. Cùng ngày dù parse từ "08/04/2026" hay "2026-04-08" → cùng hash.

### 16.4 Difference Write-off

- **difference_account bị deactivate/archived:** Frappe validate khi PE insert → throw error "Account XYZ is disabled". PE creation fails, error logged — user cần fix account trong COA.
- **Cost Center required nhưng không set:** PE inherits company default cost_center. Nếu company chưa set default → Frappe validation error. Fix: set company.cost_center trước khi dùng vn_banking.
- **Chênh lệch âm (nhận nhiều hơn hoá đơn):** difference = txn_amount - allocated. Nếu positive → bank fee (chi phí). Nếu negative → overpayment. Cả 2 trường hợp đều vào Deductions nếu ≤ tolerance. User review nếu > tolerance.

### 16.5 Multi-invoice Combo Matching

- **k=2 và k=3 đều sum đúng:** `combinations_sum_match` iterate k từ nhỏ → lớn, return combo đầu tiên (smallest k). k=2 thắng k=3.
- **Combo chứa invoice đã cancelled:** `build_context` chỉ load invoices có `docstatus=1` AND `outstanding_amount > 0`. Cancelled invoices (docstatus=2) không bao giờ vào candidate pool.
- **Rounding difference khi sum nhiều invoice:** `Decimal` arithmetic — no floating point error. Tolerance check dùng `abs(diff) <= tolerance`.

## 17. Dependency Justification (Trụ cột 3)

| Dependency | Why stdlib can't | License | Status |
|---|---|---|---|
| `openpyxl` | xlsx format requires ZIP + XML parsing with merged cell support. Already in Frappe dependency tree — zero additional weight. | MIT | Active (monthly releases) |
| `xlrd>=2.0` | Legacy .xls (BIFF) binary format. Python stdlib has no xls reader. `csv.reader` only handles text CSV, not binary xls. | BSD | Maintained (security fixes) |
| `rapidfuzz>=3.0` | C-optimized fuzzy string matching. `difflib.SequenceMatcher` is 10-50x slower and lacks `partial_ratio` (partial substring matching needed for VN abbreviated names like "CTY" vs "Công ty"). | MIT | Active (weekly releases) |
| `pandas` | Used ONLY for `pd.read_html()` to parse HTML-as-xls (PG Bank exports). `html.parser` + `BeautifulSoup` alone can't parse `<table>` into structured rows with NaN handling. Only imported in `parser/base.py:read_html_rows()`. | BSD-3 | Active |
| `beautifulsoup4` + `lxml` | Backend for `pandas.read_html(flavor="bs4")`. Required by pandas for HTML table parsing. Not used directly. | MIT / BSD | Active |

## 18. Human-AI Responsibility Markers (Trụ cột 6)

Các quyết định sau ảnh hưởng tài chính/quyền truy cập — **PHẢI được người dùng xác nhận**, AI không tự quyết:

- **`[HUMAN CONFIRM]` difference_account** (§14.3, Settings): chọn sai tài khoản hạch toán chênh lệch = sai báo cáo tài chính. Admin/kế toán trưởng phải chọn đúng TK theo COA của công ty.
- **`[HUMAN CONFIRM]` default_pe_action = Submit** (§3.3 Settings): auto-submit PE = ghi sổ kế toán không qua review. Chỉ nên dùng khi kế toán đã tin tưởng match engine sau nhiều tháng vận hành.
- **`[HUMAN CONFIRM]` tolerance_fixed_amount** (§3.3 Settings): ngưỡng chênh lệch quá cao = write-off sai, quá thấp = nhiều dòng cần review thủ công. Default 1000 VND phù hợp cho DCNet nhưng tuỳ quy mô giao dịch.
- **`[HUMAN CONFIRM]` invoice_number_patterns** (§14.2): regex sai = miss match hoặc false match. Kế toán cần verify regex bắt đúng mã HĐ của công ty.
- **`[HUMAN CONFIRM]` Permission matrix** (§13.2): ai được submit PE, ai được access Settings — quyết định bởi quản lý, không phải developer.

## 19. Open Questions (remaining)

*None — all resolved 2026-04-10. Sample files collected 2026-04-10 (4 banks: BIDV, MB Bank, Sacombank, PG Bank).*
