# Spec: TSCĐ & CCDC — Hạch toán inline (single-pane)

**Date:** 2026-05-04
**Branch:** `feature/tscd-ccdc-polish` (apps/vn_accounting)
**Author:** Long
**Status:** Draft for eng/design review

---

## 1. Vấn đề & Mục tiêu

### Vấn đề hiện tại
1. **Asset Repair list view** — cột "Thời gian chết" rỗng cho 100% record (ERPNext core chỉ tính `downtime` qua JS hook khi user thay đổi `repair_status` thủ công; demo seeder bypass UI → null).
2. **Nút "Sổ Cái" rỗng** cho repair "Sửa chữa lớn vốn hóa" / "Nâng cấp cải tạo" — vn_accounting tạo JE riêng, GL Entry lưu `voucher_no = JE.name`, nhưng nút lọc bằng `voucher_no = AR.name` → 0 match.
3. **Repair "Chi phí" không có PI** — ERPNext core không post GL (yêu cầu PI hoặc Stock Consumption), vn_accounting cũng không post. Audit trail thiếu.
4. **Bút toán kế toán bị tách rời chứng từ gốc** — kế toán phải mở 2 màn hình (AR/CCDC + JE) để nắm được hạch toán; không sửa TK trước submit được.
5. **Pattern không nhất quán** giữa Repair (1 JE) và CCDC (3 lifecycle events × 5 hàm `create_*_je`) — code khó maintain, UX khó học.

### Mục tiêu
- **1 giao diện duy nhất** cho mỗi lifecycle event: thông tin gốc + bút toán hạch toán hiển thị inline (không tab, không dialog).
- **Kế toán control**: thấy bút toán mặc định trước submit, sửa TK/số tiền nếu cần, có VAT toggle.
- **Linking ổn định**: dùng `Journal Entry Account.reference_type/reference_name` chuẩn ERPNext — không dùng convention naming.
- **"Sổ Cái" button luôn match**: route trực tiếp đến `voucher_no = JE.name` đã lưu.
- **Áp dụng đồng nhất** cho 4 lifecycle events: Asset Repair, CCDC Item (mua), CCDC Allocation Entry (phân bổ kỳ), CCDC Writeoff (ghi giảm).

---

## 2. Quyết định thiết kế (chốt)

| # | Quyết định | Lý do |
|---|---|---|
| D1 | Section Break, không Tab Break, `collapsible=0` | User yêu cầu "1 giao diện không tab" |
| D2 | 1 Child DocType chung `VN Accounting Entry` | Reuse cho 4 events, giảm 4 → 1 schema |
| D3 | Auto-fill mặc định khi đổi classification/event | Kế toán không phải gõ TK quen thuộc |
| D4 | VAT toggle: `has_vat` checkbox + `vat_rate` (default 10%) → tự thêm dòng 1331 | VN convention |
| D5 | Linking: `JE.accounts[i].reference_type/name = AR/CCDC.name` | Native ERPNext mechanism |
| D6 | "Sổ Cái" button override → route `voucher_no = doc.posted_je` | 1-to-1 stable link |
| D7 | Suppress ERPNext core `make_gl_entries()` cho repair | Tránh double-post |
| D8 | Khi có PI trong `invoices` table → ẩn section Hạch toán, dùng core ERPNext | PI tự lo bút toán |
| D9 | Server-side `validate` tự tính `downtime` | Không phụ thuộc JS UI hook |
| D10 | CCDC writeoff: section "Hạch toán ghi giảm" luôn hiển thị inline trên form CCDC Writeoff (không dialog) | Thống nhất pattern với TSCĐ |
| D11 | CCDC Allocation Entry (child row): thêm 2 cột `debit_account`, `credit_account` editable trước khi post | Kế toán sửa TK theo bộ phận trước khi ghi nhận từng kỳ |
| D12 | Backfill 8 demo Asset Repair record + tạo JE còn thiếu | Demo data hiển thị đúng ngay sau merge |
| D13 | Demo seeder ngừng patch `on_submit` skip | Tạo full audit trail thật |

---

## 3. Schema thay đổi

### 3.1. Child DocType MỚI: `VN Accounting Entry`

```
istable: 1
fields:
  - idx (Int)                      # auto từ Frappe
  - account_debit (Link → Account, reqd, in_list_view)
  - account_credit (Link → Account, reqd, in_list_view)
  - amount (Currency, reqd, options: "VND", in_list_view)
  - description (Small Text, in_list_view)
  - is_vat (Check, hidden)         # đánh dấu row VAT để auto-recalc
  - posted_je (Link → Journal Entry, read_only)
                                   # null khi chưa post; sau on_submit
                                   # set bằng JE.name của row tương ứng
                                   # — dùng cho Allocation Entry trong
                                   # CCDC Schedule (multi-period)
```

**Filter Account query** (set trong JS): `is_group=0, company=parent.company, root_type IN ("Asset","Liability","Income","Expense","Equity")`.

### 3.2. Custom Fields thêm vào DocType cha

#### Asset Repair (ERPNext core, dùng Custom Field)
```json
[
  {
    "fieldname": "vn_accounting_section",
    "fieldtype": "Section Break",
    "label": "Hạch toán",
    "insert_after": "actions_performed",
    "collapsible": 0,
    "depends_on": "eval:!doc.invoices || !doc.invoices.length"
  },
  {
    "fieldname": "has_vat",
    "fieldtype": "Check",
    "label": "Có VAT đầu vào",
    "default": "0",
    "insert_after": "vn_accounting_section"
  },
  {
    "fieldname": "vat_rate",
    "fieldtype": "Percent",
    "label": "VAT %",
    "default": "10",
    "depends_on": "has_vat",
    "insert_after": "has_vat"
  },
  {
    "fieldname": "accounting_entries",
    "fieldtype": "Table",
    "label": "Bút toán",
    "options": "VN Accounting Entry",
    "insert_after": "vat_rate"
  },
  {
    "fieldname": "posted_je",
    "fieldtype": "Link",
    "label": "Bút toán đã ghi",
    "options": "Journal Entry",
    "read_only": 1,
    "insert_after": "accounting_entries"
  }
]
```

> Field `capitalization_je` cũ (đã có) → giữ tương thích, alias bằng `posted_je` qua patch (set posted_je = capitalization_je nếu posted_je null).

#### CCDC Item (custom DocType — sửa trực tiếp .json)
Thêm sau `expense_account`:
```
- has_vat (Check, default 0)
- vat_rate (Percent, default 10, depends_on: has_vat)
- accounting_entries (Table → VN Accounting Entry)
- posted_je (Link → Journal Entry, read_only)
```

#### CCDC Writeoff (custom DocType — sửa trực tiếp .json)
Thêm sau `remaining_153_amount`:
```
- accounting_entries (Table → VN Accounting Entry)
- posted_je_242 (Link → Journal Entry, read_only)   # JE clear 242
- posted_je_153 (Link → Journal Entry, read_only)   # JE clear 153
```

#### CCDC Allocation Entry (child row — sửa .json)
Thêm 2 cột:
```
- debit_account (Link → Account, in_list_view, default fetched từ parent ccdc_item.expense_account)
- credit_account (Link → Account, in_list_view, default fetched từ parent ccdc_item.prepayment_account)
```

> Field `journal_entry` cũ giữ nguyên (link đến JE đã post cho kỳ này).

---

## 4. UX layout — single pane

### 4.1. Asset Repair form
```
┌─ Section: Tài sản & Trạng thái ─────────────────────────┐
│  Asset │ Asset Name (read) │ Repair Status              │
│  Failure Date │ Completion Date │ Downtime              │
│  Repair Classification │ Project │ Cost Center          │
└──────────────────────────────────────────────────────────┘

┌─ Section: Chi phí ──────────────────────────────────────┐
│  Repair Cost │ Total Repair Cost                        │
│  Description (text)                                      │
│  Actions Performed (text)                                │
└──────────────────────────────────────────────────────────┘

┌─ Section: Hạch toán (collapsible=0, ẩn nếu có invoices)┐
│  ☐ Có VAT đầu vào    VAT % [10]                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ # │ TK Nợ  │ TK Có  │ Số tiền    │ Diễn giải       │ │
│  ├───┼────────┼────────┼────────────┼──────────────────│ │
│  │ 1 │ 2413   │ 331    │ 18,000,000 │ Vốn hóa SC AC-7 │ │  ← auto-fill
│  │ 2 │ 1331   │ 331    │ 1,800,000  │ VAT 10% SC      │ │  ← khi has_vat=1
│  └────────────────────────────────────────────────────┘ │
│  Tổng Nợ: 19,800,000  Tổng Có: 19,800,000 ✓             │
│  Bút toán đã ghi: ACC-JV-2026-00134 → [View]            │  ← sau submit
└──────────────────────────────────────────────────────────┘

┌─ Section: Stock Items (collapsible=1, mặc định gập) ────┐
│  (chỉ mở khi có vật tư thay thế)                         │
└──────────────────────────────────────────────────────────┘

┌─ Section: Purchase Invoices (collapsible=1, mặc định gập)
│  (chỉ mở khi tham chiếu PI có sẵn)                       │
└──────────────────────────────────────────────────────────┘
```

### 4.2. CCDC Item form
```
┌─ Section: Thông tin CCDC ───────────────────────────────┐
│  Item Code │ Item Name │ CCDC Category │ Status         │
│  Cost │ Purchase Date │ Available For Use Date          │
│  Useful Period (months) │ Allocation Periods            │
│  Location │ Custodian                                    │
└──────────────────────────────────────────────────────────┘

┌─ Section: Tài khoản hạch toán mặc định ─────────────────┐
│  Cost Account (153) │ Prepayment Account (242)           │
│  Expense Account (6413)                                  │
└──────────────────────────────────────────────────────────┘

┌─ Section: Hạch toán mua (collapsible=0) ────────────────┐
│  ☐ Có VAT đầu vào    VAT % [10]                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ # │ TK Nợ  │ TK Có  │ Số tiền    │ Diễn giải       │ │
│  ├───┼────────┼────────┼────────────┼──────────────────│ │
│  │ 1 │ 242    │ 153    │ 12,000,000 │ Mua CCDC X      │ │  ← auto
│  └────────────────────────────────────────────────────┘ │
│  Bút toán mua: ACC-JV-2026-00210 → [View]              │
└──────────────────────────────────────────────────────────┘
```

### 4.3. CCDC Allocation Schedule form
Schedule không cần section Hạch toán riêng — TK phân bổ nằm trong từng row của child table `Allocation Entries`:
```
┌─ Section: Lịch phân bổ ─────────────────────────────────┐
│  CCDC Item │ Start Date │ Total Amount │ Periods │ Frequency
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ # │ Date  │ Amount │ TK Nợ │ TK Có │ JE     │ Status │ │
│  ├───┼───────┼────────┼───────┼───────┼────────┼────────│ │
│  │ 1 │ 31/01 │ 1.0tr  │ 6413  │ 242   │ JV-134 │ Posted │ │
│  │ 2 │ 28/02 │ 1.0tr  │ 6413  │ 242   │        │ Pending│ │
│  └────────────────────────────────────────────────────┘ │
│  [Ghi nhận kỳ tiếp theo]   [Ghi nhận tất cả kỳ đến hôm nay]
└──────────────────────────────────────────────────────────┘
```

### 4.4. CCDC Writeoff form
```
┌─ Section: Thông tin ghi giảm ───────────────────────────┐
│  CCDC Item │ Item Name (read)                           │
│  Writeoff Date │ Writeoff Reason                        │
│  Compensation Amount │ Compensation Employee            │
│  Remarks                                                 │
└──────────────────────────────────────────────────────────┘

┌─ Section: Số dư còn lại (auto-tính) ────────────────────┐
│  Remaining 242 Amount: 4,000,000                         │
│  Remaining 153 Amount: 0                                 │
└──────────────────────────────────────────────────────────┘

┌─ Section: Hạch toán ghi giảm (collapsible=0) ───────────┐
│  ┌────────────────────────────────────────────────────┐ │
│  │ # │ TK Nợ  │ TK Có  │ Số tiền   │ Diễn giải        │ │
│  ├───┼────────┼────────┼───────────┼──────────────────│ │
│  │ 1 │ 6413   │ 242    │ 4,000,000 │ Xóa số dư 242   │ │ ← auto
│  └────────────────────────────────────────────────────┘ │
│  (Nếu compensation > 0, thêm row D 1388 / C 711 hoặc 642)│
│  Bút toán đã ghi: JE 242 → [View]   JE 153 → [View]    │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Auto-fill rules (helper `default_entries()`)

### 5.1. Asset Repair
Trigger: `repair_classification` change OR `repair_cost` change OR `has_vat`/`vat_rate` change.

| Classification | Row 1 (chính) | Row 2 (VAT, nếu has_vat) |
|---|---|---|
| Chi phí | D **6427** / C **111** / amount = repair_cost | D **1331** / C **111** / amount = repair_cost × vat_rate% |
| Sửa chữa lớn vốn hóa | D **2413** / C **331** / amount = repair_cost | D **1331** / C **331** / amount = repair_cost × vat_rate% |
| Nâng cấp cải tạo | D **2412** / C **331** / amount = repair_cost | D **1331** / C **331** / amount = repair_cost × vat_rate% |

> Khi đã có row do user sửa (`description` thay đổi từ default) → KHÔNG ghi đè. Detect qua flag `_user_edited` trên row, hoặc so giá trị description với template default.

### 5.2. CCDC Item (mua)
Trigger: `cost` change OR doc init.
```
Row 1: D = prepayment_account or 242 / C = cost_account or 153 / amount = cost
Row 2 (has_vat): D 1331 / C cost_account / amount = cost × vat_rate%
```

### 5.3. CCDC Allocation Entry default accounts
Trigger: tạo schedule.
```
debit_account = parent.ccdc_item.expense_account or 6413
credit_account = parent.ccdc_item.prepayment_account or 242
```

### 5.4. CCDC Writeoff
Trigger: `ccdc_item` selected OR `compensation_amount` change.
```
Row 1 (luôn có): D = expense_account or 6413 / C = prepayment_account or 242 / amount = remaining_242_amount
Row 2 (nếu remaining_153 > 0): D 632 / C cost_account or 153 / amount = remaining_153
Row 3 (nếu compensation > 0): D 1388 (nhân viên) / C 711 (thu nhập khác) / amount = compensation_amount
```

---

## 6. Posting flow

### 6.1. Helper module
File: `vn_accounting/utils/accounting_posting.py`

```python
def post_je_from_entries(
    entries: list[dict],          # [{account_debit, account_credit, amount, description}, ...]
    company: str,
    posting_date,
    user_remark: str,
    ref_doctype: str,
    ref_name: str,
    submit: bool = True,
    cost_center: str | None = None,
) -> str:
    """Build a single Journal Entry from N entry rows.

    Each entry row → 2 JE accounts (1 debit + 1 credit).
    All accounts get reference_type=ref_doctype, reference_name=ref_name
    so GL Entry inherits against_voucher correctly.
    Returns JE.name.
    """
    # Validate balance
    total_debit = sum(e['amount'] for e in entries)
    # (each row is balanced by construction: same amount D+C)

    je_accounts = []
    for e in entries:
        je_accounts.append({
            "account": e['account_debit'],
            "debit_in_account_currency": e['amount'],
            "cost_center": cost_center,
            "reference_type": ref_doctype,
            "reference_name": ref_name,
            "user_remark": e.get('description'),
        })
        je_accounts.append({
            "account": e['account_credit'],
            "credit_in_account_currency": e['amount'],
            "cost_center": cost_center,
            "reference_type": ref_doctype,
            "reference_name": ref_name,
            "user_remark": e.get('description'),
        })

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Journal Entry",
        "company": company,
        "posting_date": posting_date,
        "user_remark": user_remark,
        "accounts": je_accounts,
    })
    je.flags.ignore_permissions = True
    je.insert()
    if submit:
        je.submit()
    return je.name
```

### 6.2. Integration per event

| Event | Hook | Action |
|---|---|---|
| Asset Repair `on_submit` | replace existing | Đọc `accounting_entries`, gọi `post_je_from_entries(...)`, lưu `posted_je`. **Suppress** `make_gl_entries()` của ERPNext core bằng monkey-patch trong module init OR set flag để `on_submit` ERPNext không chạy (xem 6.3). |
| Asset Repair `on_cancel` | new | Cancel JE liên kết qua `posted_je` |
| CCDC Item `on_submit` | replace `create_ccdc_purchase_je` | Như trên |
| CCDC Allocation Entry "Post period" | trong API/whitelisted method | Đọc `debit_account/credit_account/allocation_amount` của row đó, gọi helper, lưu `journal_entry` của row |
| CCDC Writeoff `on_submit` | replace `create_ccdc_writeoff_je` | 1-3 row trong child table → có thể tạo 1 JE duy nhất hoặc 2 JE riêng (242 + 153). Đề xuất: **1 JE duy nhất** với N rows (tổng cân bằng). Lưu vào `posted_je_242` (single field nếu chỉ 1 JE — rename → `posted_je`) |

### 6.3. Suppress ERPNext core GL cho Asset Repair

ERPNext `AssetRepair.on_submit` gọi `self.make_gl_entries()` (line 210). Cách suppress sạch nhất:

```python
# vn_accounting/asset/repair_hooks.py
import erpnext.assets.doctype.asset_repair.asset_repair as ar_mod

_original_make_gl = ar_mod.AssetRepair.make_gl_entries

def patched_make_gl(self, cancel=False):
    """Skip core GL when vn_accounting handles posting via accounting_entries.
    Only fall through to core when no accounting_entries (e.g., legacy data).
    """
    if getattr(self, 'accounting_entries', None) and self.accounting_entries:
        return  # vn_accounting posts via on_submit hook
    return _original_make_gl(self, cancel=cancel)

ar_mod.AssetRepair.make_gl_entries = patched_make_gl
```

Áp dụng patch trong `vn_accounting/__init__.py` (chạy 1 lần khi app load).

> **Why monkey-patch:** ERPNext không expose hook để override; doc_events không ngăn `make_gl_entries` chạy.

---

## 7. Server-side downtime auto-fill

```python
# vn_accounting/asset/repair_hooks.py
def on_validate(doc, method):
    # ... existing 10% warning ...
    if doc.failure_date and doc.completion_date and not doc.downtime:
        from erpnext.assets.doctype.asset_repair.asset_repair import get_downtime
        hrs = get_downtime(doc.failure_date, doc.completion_date)
        if hrs:
            doc.downtime = f"{hrs} Hrs"
```

Hook đã được register; chỉ thêm logic.

---

## 8. "Sổ Cái" button override

File: `vn_accounting/public/js/asset_repair.bundle.js` (mới)

```js
frappe.ui.form.on("Asset Repair", {
  refresh(frm) {
    // Remove core button "View → Accounting Ledger" + add ours
    if (frm.doc.docstatus > 0 && frm.doc.posted_je) {
      frm.remove_custom_button(__("Accounting Ledger"), __("View"));
      frm.add_custom_button(__("Sổ Cái"), () => {
        frappe.route_options = {
          voucher_no: frm.doc.posted_je,
          from_date: frm.doc.completion_date,
          to_date: frappe.datetime.now_date(),
          company: frm.doc.company,
        };
        frappe.set_route("query-report", "General Ledger");
      }, __("Xem"));
    }
  }
});
```

Tương tự cho CCDC Item, CCDC Writeoff, CCDC Allocation Schedule.

Đăng ký bundle trong `hooks.py`:
```python
doctype_js = {
    "Asset Repair": "public/js/asset_repair.bundle.js",
    "CCDC Item": "public/js/ccdc_item.bundle.js",
    "CCDC Writeoff": "public/js/ccdc_writeoff.bundle.js",
    "CCDC Allocation Schedule": "public/js/ccdc_allocation_schedule.bundle.js",
}
```

---

## 9. Auto-fill JS implementation

Pattern chung trong mỗi `.bundle.js`:

```js
// asset_repair.bundle.js
const DEFAULTS_BY_CLASSIFICATION = {
  "Chi phí":              { debit: "6427", credit: "111", desc_template: "Chi phí sửa chữa {asset}" },
  "Sửa chữa lớn vốn hóa": { debit: "2413", credit: "331", desc_template: "Vốn hóa SC {asset}" },
  "Nâng cấp cải tạo":     { debit: "2412", credit: "331", desc_template: "Nâng cấp {asset}" },
};

async function lookup_account_by_number(company, number) {
  const r = await frappe.db.get_value("Account",
    {company, account_number: number, is_group: 0}, "name");
  return r.message?.name;
}

async function rebuild_entries(frm) {
  if (!frm.doc.repair_classification || !frm.doc.repair_cost) return;
  const def = DEFAULTS_BY_CLASSIFICATION[frm.doc.repair_classification];
  if (!def) return;

  const debit_acc = await lookup_account_by_number(frm.doc.company, def.debit);
  const credit_acc = await lookup_account_by_number(frm.doc.company, def.credit);

  // Don't rebuild if user has manually edited (heuristic: check description doesn't match template)
  const is_user_edited = (frm.doc.accounting_entries || []).some(r =>
    r.description && !r.description.startsWith(def.desc_template.split(' ')[0])
  );
  if (is_user_edited) return;

  frm.clear_table("accounting_entries");
  frm.add_child("accounting_entries", {
    account_debit: debit_acc, account_credit: credit_acc,
    amount: frm.doc.repair_cost,
    description: def.desc_template.replace("{asset}", frm.doc.asset_name || frm.doc.asset),
  });

  if (frm.doc.has_vat && frm.doc.vat_rate) {
    const tk_1331 = await lookup_account_by_number(frm.doc.company, "1331");
    frm.add_child("accounting_entries", {
      account_debit: tk_1331, account_credit: credit_acc,
      amount: (frm.doc.repair_cost * frm.doc.vat_rate / 100),
      description: `VAT ${frm.doc.vat_rate}% — ${frm.doc.repair_classification}`,
      is_vat: 1,
    });
  }
  frm.refresh_field("accounting_entries");
}

frappe.ui.form.on("Asset Repair", {
  repair_classification: rebuild_entries,
  repair_cost: rebuild_entries,
  has_vat: rebuild_entries,
  vat_rate: rebuild_entries,
});
```

---

## 10. Validate (server-side)

### 10.1. Asset Repair
```python
# vn_accounting/asset/repair_hooks.py — extend on_validate
def on_validate(doc, method):
    # ... existing checks ...
    if not doc.invoices and (doc.repair_cost or 0) > 0:
        if not doc.accounting_entries:
            frappe.throw(_("Bút toán không được trống. Vui lòng chọn loại sửa chữa để auto-fill."))
        total = sum((e.amount or 0) for e in doc.accounting_entries)
        expected = doc.repair_cost + (doc.repair_cost * (doc.vat_rate or 0) / 100 if doc.has_vat else 0)
        if abs(total - expected) > 1:
            frappe.throw(_("Tổng bút toán ({0}) không khớp chi phí + VAT ({1})").format(total, expected))
```

### 10.2. CCDC Item / Writeoff: tương tự, validate tổng amount = `cost` (Item) hoặc = `remaining_242 + remaining_153 + compensation` (Writeoff).

### 10.3. CCDC Allocation Entry: validate `debit_account` + `credit_account` non-empty trước khi post.

---

## 11. Migration & Backfill

### 11.1. Patch order (`patches.txt`):
```
vn_accounting.patches.v0_5_0.create_vn_accounting_entry_doctype
vn_accounting.patches.v0_5_0.add_custom_fields_for_inline_accounting
vn_accounting.patches.v0_5_0.backfill_asset_repair_downtime
vn_accounting.patches.v0_5_0.backfill_asset_repair_je
vn_accounting.patches.v0_5_0.alias_capitalization_je_to_posted_je
```

### 11.2. Backfill `downtime`
```python
# patches/v0_5_0/backfill_asset_repair_downtime.py
import frappe
from erpnext.assets.doctype.asset_repair.asset_repair import get_downtime

def execute():
    rows = frappe.db.sql("""
        SELECT name, failure_date, completion_date FROM `tabAsset Repair`
        WHERE (downtime IS NULL OR downtime='') AND failure_date IS NOT NULL AND completion_date IS NOT NULL
    """, as_dict=True)
    for r in rows:
        hrs = get_downtime(r.failure_date, r.completion_date)
        if hrs:
            frappe.db.set_value("Asset Repair", r.name, "downtime", f"{hrs} Hrs", update_modified=False)
    frappe.db.commit()
```

### 11.3. Backfill missing JE cho 4 record vốn hóa
```python
# patches/v0_5_0/backfill_asset_repair_je.py
import frappe
def execute():
    rows = frappe.get_all("Asset Repair",
        filters={"docstatus": 1, "capitalization_je": ("is", "not set"),
                 "repair_classification": ("in", ["Sửa chữa lớn vốn hóa", "Nâng cấp cải tạo"])},
        fields=["name", "repair_classification", "repair_cost", "completion_date", "company", "asset", "asset_name"]
    )
    for r in rows:
        # Build minimal accounting_entries (1 row) and post
        # ... uses post_je_from_entries helper
        pass
```

> Backfill chạy sau khi schema mới + fixtures cài đặt xong. Nếu data đã có thì backfill no-op.

---

## 12. Demo seeder updates

### 12.1. `dcnet_sample/data/assets.py` — ngừng patch `on_submit`
```python
# DELETE these lines:
# original_on_submit = repair_hooks.on_submit
# repair_hooks.on_submit = lambda doc, method: None
# ...
# repair_hooks.on_submit = original_on_submit
```

Thay vào: trước `repair.submit()`, set `repair.has_vat = 1` (hoặc 0 tùy data) — JS auto-fill không chạy trong context Python, phải gọi server-side helper:

```python
from vn_accounting.utils.accounting_posting import build_default_entries

repair.accounting_entries = []
for entry in build_default_entries("Asset Repair", repair.repair_classification,
                                    repair.repair_cost, has_vat=False, company=COMPANY):
    repair.append("accounting_entries", entry)
```

### 12.2. CCDC seeder (nếu có) — pattern tương tự.

---

## 13. Test plan

### 13.1. Unit tests (Python — `bench console + unittest`)

| Test file | Coverage |
|---|---|
| `test_repair_default_entries.py` | `build_default_entries("Asset Repair", classification, cost, has_vat)` returns đúng accounts cho 3 × 2 = 6 case |
| `test_post_je_from_entries.py` | Post JE → balance check + reference_type/name set đúng |
| `test_repair_validate_balance.py` | `on_validate` throw khi tổng != cost + VAT |
| `test_repair_on_submit_creates_je.py` | Submit AR → posted_je set + JE submitted + GL Entry exists |
| `test_repair_on_cancel_cancels_je.py` | Cancel AR → JE cancelled |
| `test_repair_invoices_skips_section.py` | AR có invoices → core ERPNext path, accounting_entries unused |
| `test_ccdc_item_purchase_je.py` | CCDC Item submit → JE D 242/C 153 đúng |
| `test_ccdc_allocation_post_period.py` | Post period 1 → JE D 6413/C 242 + entry status=Posted |
| `test_ccdc_writeoff_je.py` | Writeoff → JE clear 242 + 153 + compensation |
| `test_downtime_auto_fill.py` | validate fills downtime when both dates set |

### 13.2. Integration / live QA (Playwright MCP)

| Scenario | Expected |
|---|---|
| Tạo AR mới "Chi phí" → submit | Bút toán inline auto-fill D 6427/C 111; submit OK; nút Sổ Cái mở GL có data |
| Tạo AR "Sửa chữa lớn vốn hóa" + VAT 10% | 2 rows (chính + 1331); tổng cân bằng |
| Sửa TK trong row trước submit | Submit → JE dùng TK đã sửa |
| Cancel AR | JE cũng cancel, GL Entry là_cancelled=1 |
| Tạo CCDC Item → submit | JE D 242/C 153 đúng cost |
| Tạo Allocation Schedule + post period 1 | JE D 6413/C 242; entry status=Posted; còn lại Pending |
| Tạo Writeoff cho CCDC còn 4tr 242 | Auto-fill 1 row D 6413/C 242 4tr; submit → JE OK |
| List view Asset Repair | Cột "Thời gian chết" hiển thị (sau backfill) |

### 13.3. Backfill verification
```bash
bench --site dcnet.localhost mariadb -N -B -e "
  SELECT COUNT(*) FROM \`tabAsset Repair\` WHERE downtime IS NULL AND failure_date IS NOT NULL AND completion_date IS NOT NULL
"
# expect: 0

bench --site dcnet.localhost mariadb -N -B -e "
  SELECT COUNT(*) FROM \`tabAsset Repair\` WHERE docstatus=1 AND repair_classification IN ('Sửa chữa lớn vốn hóa','Nâng cấp cải tạo') AND capitalization_je IS NULL
"
# expect: 0
```

---

## 14. Edge cases

| Case | Xử lý |
|---|---|
| AR có cả `invoices` lẫn `accounting_entries` | UI: hiển thị warning, ẩn section Hạch toán; server: skip accounting_entries posting, dùng core ERPNext |
| User clear `accounting_entries` thủ công rồi submit | `on_validate` throw nếu cost > 0 và không có invoices |
| `has_vat` toggle qua lại | JS rebuild rows; nếu user đã sửa row VAT thì giữ — heuristic: detect via is_vat flag |
| User đổi `repair_classification` sau khi đã sửa rows | JS hỏi confirm "Ghi đè bút toán mặc định?" → nếu OK rebuild |
| JE submit fail (ví dụ TK chưa cấu hình) | `on_submit` rollback → AR không submit; show frappe.throw với context |
| CCDC Allocation: post 1 kỳ rồi delete CCDC Item | block delete khi có JE tham chiếu (đã có trong logic hiện tại?) |
| CCDC Writeoff khi CCDC Item chưa allocate hết | warn "Còn N kỳ chưa phân bổ. Tiếp tục writeoff?" |
| Multi-currency company | Sprint này chỉ VND; nếu khác → throw "Chưa hỗ trợ multi-currency" |
| TK 6427 không tồn tại trong COA | Fallback theo cây con: 642 → 6427 → 642x; throw nếu không tìm |
| Cost center per row | Inherit từ company.cost_center; nếu doc có project → dùng project.cost_center |
| Bộ phận sản xuất → 6277 thay vì 6427 | User sửa thủ công; KHÔNG auto-detect ở v1 (vNext: Custom Field "Bộ phận" trên AR) |
| Repair_cost = 0 | Block submit ("Chi phí phải > 0") |
| Demo seeder bypass on_submit cũ | Patch v0_5_0 backfill JE cho data có sẵn |

---

## 15. Acceptance criteria

### Functional
- [ ] Asset Repair list view cột "Thời gian chết" hiển thị data cho mọi record (backfill xong + new records auto-fill).
- [ ] Tạo AR "Chi phí" / "Vốn hóa" / "Nâng cấp" — bút toán inline auto-fill đúng TK theo bảng §5.1.
- [ ] Toggle `has_vat` — row 1331 xuất hiện/biến mất, validate cân bằng.
- [ ] AR submit → `posted_je` set, JE submitted với reference_type/name đúng, GL Entry tồn tại.
- [ ] AR cancel → JE cancel.
- [ ] Nút "Sổ Cái" mở GL có data (không rỗng).
- [ ] CCDC Item form: section "Hạch toán mua" hiển thị, auto-fill đúng, submit tạo JE D 242/C 153.
- [ ] CCDC Allocation Schedule form: cột TK Nợ/Có hiển thị editable trong child table, post period tạo JE đúng.
- [ ] CCDC Writeoff form: section "Hạch toán ghi giảm" hiển thị, auto-fill 2-3 row tùy số dư + bồi thường, submit tạo JE.
- [ ] AR có `invoices` (PI) → UI ẩn section Hạch toán, core ERPNext xử lý GL như cũ.

### Quality gates
- [ ] 10/10 unit tests pass.
- [ ] Console errors = 0 trên 4 form (Playwright MCP capture).
- [ ] Migration patches `v0_5_0/*` chạy idempotent (chạy 2 lần không error).
- [ ] Demo data sau seed: tất cả AR có `posted_je` non-null + GL Entry hiển thị.
- [ ] No double-posting: 1 AR submit → đúng 1 JE, đúng số GL Entry rows.
- [ ] Sidebar "Sửa chữa tài sản" / "CCDC" links vẫn hoạt động (regression check).

### Documentation
- [ ] CHANGELOG.md ghi nhận v0.5.0.
- [ ] CODEBASE_DETAIL.md update file mới: `accounting_posting.py`, child DocType, bundle JS.
- [ ] BUSINESS_LOGIC.md §TSCĐ và §CCDC bổ sung mục "Hạch toán inline".

---

## 16. Out of scope (vNext)

- Bộ phận / Phòng ban → auto-route TK 6427 vs 6277 vs 6417: cần thêm field `department` trên AR.
- Asset Disposal feature (form riêng, đang planned).
- Multi-currency repair (USD/EUR cho công ty FDI).
- Bulk post N CCDC allocation periods qua scheduled task (cron monthly).
- Chuyển CCDC writeoff `posted_je_242`/`posted_je_153` 2 fields → 1 field `posted_je` (nếu chốt 1 JE duy nhất từ đầu).
- Deprecate `capitalization_je` field hoàn toàn (giữ tới v0.6.0 cho compatibility).

---

## 17. Self-review (3-point)

### Spec coverage
- [x] Mọi vấn đề ở §1 có decision ở §2.
- [x] Mọi decision có schema/UX/posting flow chi tiết.
- [x] Mọi event (4 events) có auto-fill rule + posting flow + test.

### Placeholder scan
- [ ] (User scan trước khi approve — chưa có TBD/TODO trong spec này.)

### Type consistency
- [x] Field names nhất quán (`accounting_entries`, `posted_je`, `has_vat`, `vat_rate`).
- [x] Helper signature (`post_je_from_entries`, `build_default_entries`) đồng bộ giữa server + seeder.
- [x] Account number references TT99/2025: 111, 1331, 153, 2412, 2413, 242, 331, 632, 642x, 711, 1388 đều tồn tại trong cả `vn_small_enterprise.json` và `vn_large_enterprise.json` (cần verify khi code).

---

## 18. Phasing trong sprint

| Phase | Scope | Output |
|---|---|---|
| **P1 — Foundation** | Child DocType `VN Accounting Entry`, helper `accounting_posting.py`, default rules `build_default_entries()`, unit tests cho helper | Helpers + tests pass standalone |
| **P2 — Asset Repair** | Custom fields, JS bundle (auto-fill + Sổ Cái override), `on_validate`/`on_submit`/`on_cancel`, monkey-patch core `make_gl_entries`, integration tests | AR e2e working |
| **P3 — CCDC Item + Writeoff** | Schema sửa, JS bundle, `on_submit`/`on_cancel`, integration tests | CCDC mua + writeoff working |
| **P4 — CCDC Allocation Schedule** | Child row `debit_account/credit_account`, post-period whitelisted method, JS bundle | Allocation post per period |
| **P5 — Migration + Backfill** | Patches v0_5_0 (downtime + JE backfill + alias capitalization_je) | Demo data hiển thị đúng |
| **P6 — Demo seeder** | `dcnet_sample/data/assets.py` ngừng skip hook + use helper | Fresh seed → full audit trail |
| **P7 — Design QA + Live QA** | Playwright MCP review 4 forms + console errors | Ship-ready |

Mỗi phase = 1 multi-session phase trong `multi-session/2026-05-04-tscd-ccdc-polish.md`.

---

## 19. Risk & mitigation

| Risk | Mitigation |
|---|---|
| Monkey-patch ERPNext core `make_gl_entries` xung đột với version bump tương lai | Test patch trên cả Frappe v16 hiện tại + tag version cụ thể; có unit test verify patch còn áp dụng |
| User đã dùng `capitalization_je` field cũ → field thứ 2 `posted_je` gây nhầm | Migration alias: `posted_je = capitalization_je` cho data cũ; deprecate `capitalization_je` ở v0.6.0 |
| Custom Field `accounting_entries` Table trên ERPNext core DocType — fixture import có thể conflict với migration ERPNext | Test trên fresh site + site có data cũ; rollback path documented |
| Performance: list view AR/CCDC load chậm vì kéo thêm child rows | List view không hiển thị child table; chỉ form load. OK |
| User đổi default account trong Settings sau khi đã có data | Auto-fill lookup dynamic theo company; existing rows không đổi (intentional — chỉ ảnh hưởng record mới) |

---

**Tổng dòng spec:** ~620 lines.
**Phụ thuộc bên ngoài:** không (tất cả nằm trong vn_accounting + dcnet_sample).
**Compatibility:** Frappe v16, ERPNext v16, VN COA TT99/2025.
