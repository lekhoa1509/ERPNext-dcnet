# Implementation Plan — Asset Polishing (TSCĐ & CCDC theo TT99/2025)

**Source spec:** `docs/superpowers/specs/2026-04-29-asset-polishing-design.md` (commit `0d9ab59`)
**Branch:** `feat/asset-polishing`
**Worktree:** `.worktrees/vn_accounting-asset-polishing/`
**Plan generated:** 2026-04-29

This plan decomposes the design spec into ordered, file-level tasks with code outlines. Each task lists files touched + exact patterns. Tasks within a phase MAY run in parallel only when they touch disjoint files (noted explicitly). Tasks across phases run sequentially.

---

## Phase 1 — Foundation + TSCĐ Polish

### Task 1.1 — Update VN Chart of Accounts (TK 242 rename)

**Files:**
- `vn_accounting/chart_of_accounts/vn_small_enterprise.json`
- `vn_accounting/chart_of_accounts/vn_large_enterprise.json`

**Outline:**
- Locate `"242"` node. Update `account_name` from `"Chi phí chờ phân bổ"` → `"Chi phí trả trước"`.
- Verify TK 211 group has children 2111-2115 + 213 (per design §7.4). If missing in `vn_small_enterprise.json`, add nodes (large already has them).
- Verify TK 153 exists as group (sub-accounts left to user discretion per TT99).

**Verification:** `grep -q "Chi phí trả trước" vn_accounting/chart_of_accounts/vn_small_enterprise.json` && `bench --site dcnet.localhost migrate` then `frappe.db.get_value("Account", {"account_number":"242", ...}, "account_name")` returns updated name.

---

### Task 1.2 — Property Setter: hide depreciation methods

**File:** `vn_accounting/fixtures/property_setter.json`

**Outline:** Append entry:
```json
{
  "doctype": "Property Setter", "doc_type": "Asset",
  "field_name": "depreciation_method", "property": "options", "property_type": "Text",
  "value": "\nĐường thẳng\nSố dư giảm dần"
}
```

**Verification:** `bench --site dcnet.localhost migrate` then open `/app/asset/new` → dropdown shows 2 options.

---

### Task 1.3 — Translations (vi.csv) — TSCĐ labels

**File:** `vn_accounting/translations/vi.csv` (append, 2-col format)

**Entries (~30):** Per design §7.1 table — Asset, Asset Category, Asset Movement, Asset Repair, Gross Purchase Amount, Asset Owner, Custodian, Available-for-use Date, Depreciation Method, Straight Line, Double Declining Balance, Manual, Total Number of Depreciations, Frequency of Depreciation, Repair Status, Disposal Date, plus all CCDC labels for upcoming Phase 2 DocTypes.

**Verification:** `bench --site dcnet.localhost clear-cache` then frappe._("Asset") returns "Tài sản cố định".

---

### Task 1.4 — Asset Category re-seed (6 categories)

**Files:**
- `vn_accounting/install.py` (add `seed_asset_categories()` function called from `after_install` AND idempotently from `after_migrate`)

**Outline:**
```python
def seed_asset_categories():
    categories = [
        {"asset_category_name": "2111 Nhà cửa, vật kiến trúc", "fixed_asset_account": "211", ...},
        {"asset_category_name": "2112 Máy móc thiết bị", ...},
        {"asset_category_name": "2113 Phương tiện vận tải", ...},
        {"asset_category_name": "2114 Thiết bị dụng cụ quản lý", ...},
        {"asset_category_name": "2115 Cây trồng vật nuôi", ...},
        {"asset_category_name": "213 Tài sản cố định vô hình", ...},
    ]
    for cat in categories:
        if not frappe.db.exists("Asset Category", cat["asset_category_name"]):
            frappe.get_doc({"doctype": "Asset Category", **cat}).insert(ignore_permissions=True)
```

**Note:** Per `frappe-erpnext.md` rules, account_number lookup uses `account_name` LIKE prefix because `create_charts()` leaves `account_number` empty.

---

### Task 1.5 — Custom Fields

**File:** `vn_accounting/fixtures/custom_field.json` (append entries)

**Entries:**
- `Item.is_low_value_asset` (Check, after `is_fixed_asset`)
- `Asset Repair.repair_classification` (Select 3-way: `Chi phí\nSửa chữa lớn vốn hóa\nNâng cấp cải tạo`, default `Chi phí`)
- `Asset Repair.capitalization_je` (Link Journal Entry, depends_on `repair_classification != "Chi phí"`, read_only)
- `Asset Handover.scope` (Select TSCĐ\nCCDC, reqd) — applied to *new* DocType in Phase 3, list here for fixture aggregation
- `Asset Stocktake.scope` (same)

---

### Task 1.6 — Asset Repair extend (validate + on_submit JE routing)

**Files:**
- `vn_accounting/asset/__init__.py` (new)
- `vn_accounting/asset/journal_entry_builder.py` (new — pattern reference: `vn_accounting/treasury/journal_entry_builder.py`)
- `vn_accounting/asset/repair_hooks.py` (new — bind via `doc_events` in `hooks.py`)

**hooks.py changes:**
```python
doc_events = {
    "Asset Repair": {
        "validate": "vn_accounting.asset.repair_hooks.on_validate",
        "on_submit": "vn_accounting.asset.repair_hooks.on_submit",
    },
    ...
}
```

**repair_hooks.py outline:**
```python
def on_validate(doc, method=None):
    asset_doc = frappe.get_doc("Asset", doc.asset)
    if doc.repair_cost >= 0.10 * (asset_doc.gross_purchase_amount or 0):
        if doc.repair_classification == "Chi phí":
            frappe.msgprint(_("Chi phí sửa chữa ≥ 10% nguyên giá. Cân nhắc vốn hóa."), alert=True)

def on_submit(doc, method=None):
    if doc.repair_classification == "Chi phí":
        return  # ERPNext default JE is correct
    # Vốn hóa flow (Sửa chữa lớn or Nâng cấp)
    je_name = create_capitalization_je(doc)
    frappe.db.set_value("Asset Repair", doc.name, "capitalization_je", je_name)
    asset = frappe.get_doc("Asset", doc.asset)
    asset.gross_purchase_amount = (asset.gross_purchase_amount or 0) + doc.repair_cost
    if doc.repair_classification == "Nâng cấp cải tạo":
        recreate_depreciation_schedule(asset, doc)
    asset.save(ignore_permissions=True)
```

**journal_entry_builder.py outline:**
```python
def create_capitalization_je(repair_doc) -> str:
    """N 241 / C 331 then N 211 (asset CWIP) / C 241 on completion."""
    company = repair_doc.company
    cwip_account = frappe.db.get_value("Account", {"company": company, "account_name": ["like", "241 -%"]})
    asset_account = frappe.get_value("Asset Category",
        frappe.db.get_value("Asset", repair_doc.asset, "asset_category"),
        "fixed_asset_account_in_company", company)
    ...
```

---

### Task 1.7 — Print format: Biên bản sửa chữa TSCĐ

**Files:**
- `vn_accounting/vn_accounting/print_format/asset_repair_report/__init__.py`
- `vn_accounting/vn_accounting/print_format/asset_repair_report/asset_repair_report.json`
- `vn_accounting/vn_accounting/print_format/asset_repair_report/asset_repair_report.html` (Jinja, A4 dọc, Times New Roman 12pt, 3-sign — pattern from `cash_count` print format)

**Reference pattern:** `vn_accounting/vn_accounting/print_format/asset_disposal_report/`.

---

### Task 1.8 — Sidebar reorganization

**File:** `vn_accounting/workspace_sidebar/vn_accounting.json`

**Outline:**
- Locate section header `"label": "TSCĐ & CCDC"` → split into 2 separate sections per design §5.1.
- Section TSCĐ: 9 items (Danh sách, Tạo, Tính khấu hao, Sửa chữa, Bàn giao TSCĐ scope=TSCĐ, Kiểm kê TSCĐ scope=TSCĐ, Thanh lý, Sổ S21-DN, Lịch sử khấu hao).
- Section CCDC: 7 items (Danh sách CCDC, Tạo CCDC, Phân bổ CCDC, Ghi giảm CCDC, Bàn giao CCDC scope=CCDC, Kiểm kê CCDC scope=CCDC, Sổ S22-DN).
- Remove items: Asset Movement, JE-filter Phân bổ CCDC, Fixed Asset Register.
- For Bàn giao/Kiểm kê items use `link_type: "DocType"` + `route_options: {"scope": "TSCĐ"}` — per `frappe-v16-ui.md` route_options patch already in place.

**Verification (per task verification command):**
```python
parents=[i.get('label','') for i in d['items'] if i.get('child')==0]
tscd=[p for p in parents if p.strip()=='TSCĐ']
assert len(tscd)==1 and len(ccdc)==1
```

---

### Task 1.9 — Script Report Sổ S21-DN

**Files:**
- `vn_accounting/vn_accounting/report/s21_dn_so_tscd/__init__.py`
- `vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.json` (`is_standard=1`, `report_type=Script Report`, `ref_doctype=Asset`)
- `vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.py`
- `vn_accounting/vn_accounting/report/s21_dn_so_tscd/s21_dn_so_tscd.js` (filters: from_date, to_date, asset_category, company)

**Columns (per design §6 / §8):** Mã TS, Tên TS, Ngày sử dụng, Nguyên giá, Số kỳ KH, % KH năm, GTKH năm, GTKH luỹ kế, GTCL, Ghi chú.

**Query outline (parameterized SQL, per `frappe.md` security rules):**
```python
def execute(filters=None):
    return get_columns(), get_data(filters)

def get_data(filters):
    return frappe.db.sql("""
        SELECT a.name, a.asset_name, a.available_for_use_date,
               a.gross_purchase_amount, a.total_number_of_depreciations,
               (12.0 / a.total_number_of_depreciations * 100) AS pct_per_year,
               COALESCE(SUM(CASE WHEN ds.schedule_date BETWEEN %(from)s AND %(to)s
                                THEN ds.depreciation_amount ELSE 0 END), 0) AS dep_in_period,
               a.value_after_depreciation AS gtcl,
               a.notes
        FROM `tabAsset` a
        LEFT JOIN `tabDepreciation Schedule` ds ON ds.parent = a.name
        WHERE a.docstatus = 1 AND a.company = %(company)s
        GROUP BY a.name
    """, filters, as_dict=True)
```

---

### Task 1.10 — VN Accounting Settings tab "Phân quyền TSCĐ & CCDC"

**Files:**
- `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json` — add fields per design §9.1:
  - Section break "Mức ngưỡng kiểm soát"
  - `enable_value_thresholds` (Check, default 1)
  - `disposal_threshold` (Currency, default 50000000, depends_on `enable_value_thresholds`)
  - `handover_threshold` (Currency, default 100000000, depends_on `enable_value_thresholds`)
  - `min_asset_value` (Currency, default 30000000) — always-on per TT45/2013
  - Section break "Phạm vi xem theo phòng ban"
  - `scope_by_department` (Check, default 0)
  - `dept_head_sees_subordinate` (Check, default 0, read_only — v2 placeholder)
  - Section break "Bật / Tắt module"
  - `asset_revaluation_enabled` (Check, default 0)
  - Section break "Ma trận phân quyền"
  - `permission_matrix` (Table, options=Asset Permission Rule)
  - Section break "Hoạt động gần đây"
  - `permission_audit_log` (Long Text, read_only) — JSON array, latest 5 displayed via JS

- `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.py` — extend with:
  ```python
  def on_update(self):
      self._validate_thresholds()
      self._sync_permissions_to_docperm()
      if self.scope_by_department:
          self._apply_dept_user_permissions()
      self._add_audit_log_entry()

  @frappe.whitelist()
  def reset_permission_matrix(): ...
  ```
- `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.js` — add form button "Khôi phục mặc định" → confirm dialog → `frappe.call("vn_accounting...reset_permission_matrix")` → reload. Add audit log HTML render (latest 5 entries).

---

### Task 1.11 — DocType `Asset Permission Rule` (Child)

**Files:**
- `vn_accounting/vn_accounting/doctype/asset_permission_rule/__init__.py`
- `vn_accounting/vn_accounting/doctype/asset_permission_rule/asset_permission_rule.json` (`istable=1`)
- `vn_accounting/vn_accounting/doctype/asset_permission_rule/asset_permission_rule.py` (empty controller)

**Fields:** `enabled` (Check, default 1, in_list_view), `doctype_name` (Link DocType, in_list_view), `role` (Link Role, in_list_view), `read` (Check, in_list_view), `write` (Check, in_list_view), `create` (Check, in_list_view), `submit` (Check), `cancel` (Check), `if_owner` (Check), `is_modified` (Check, hidden, read_only).

---

### Task 1.12 — Default permissions fixture

**File:** `vn_accounting/fixtures/asset_permission_defaults.json` — exact content from design §9.3 (~16 rows; spec calls "≥15").

**Reset method outline (in `vn_accounting_settings.py`):**
```python
@frappe.whitelist()
def reset_permission_matrix():
    settings = frappe.get_single("VN Accounting Settings")
    settings.permission_matrix = []
    defaults = frappe.get_file_json(
        frappe.get_app_path("vn_accounting", "fixtures", "asset_permission_defaults.json"))
    for rule in defaults:
        rule["enabled"] = 1
        settings.append("permission_matrix", rule)
    settings.save()
    return _("Đã khôi phục mặc định")
```

**install.py changes:** in `after_install`, call `reset_permission_matrix()` so fresh sites have defaults loaded. In `after_migrate`, only load if `permission_matrix` empty (per design §10 edge case 16).

---

### Task 1.13 — Phase 1 verification + commit

**Outline:**
- Run `bench --site dcnet.localhost migrate` (sync DocTypes, fixtures).
- Run `bench build --app vn_accounting` (sidebar JS bundle).
- Run `bench --site dcnet.localhost clear-cache` (translation reload).
- Verify each `Phase 1 Foundation` acceptance criterion via console + browser snapshot.
- Commit: `git commit -m "feat(asset-polishing): Phase 1 foundation + TSCĐ polish complete + QA pass"` (after Phase 1 QA Gate completes per task file Sub-task 17).

---

## Phase 2 — CCDC Backbone

### Task 2.1 — DocType `CCDC Category` (Master)

**Files:**
- `vn_accounting/vn_accounting/doctype/ccdc_category/__init__.py`
- `vn_accounting/vn_accounting/doctype/ccdc_category/ccdc_category.json`
- `vn_accounting/vn_accounting/doctype/ccdc_category/ccdc_category.py` (empty NestedSet not needed; flat tree via `is_group`)

**Fields:** `category_name` (Data, reqd, unique), `parent_category_account` (Link Account, filter root_type=Asset + name LIKE 153%), `expense_account_default` (Link Account, filter 627/641/642), `useful_period_default` (Int, in months), `is_group` (Check), `parent_ccdc_category` (Link CCDC Category — for tree view if needed).

---

### Task 2.2 — Seed 5 default CCDC Categories

**File:** `vn_accounting/install.py` — add `seed_ccdc_categories()` per design §7.5; idempotent.

```python
DEFAULT_CCDC_CATEGORIES = [
    {"category_name": "Bàn ghế văn phòng", "useful_period_default": 24},
    {"category_name": "Máy tính, thiết bị IT", "useful_period_default": 24},
    {"category_name": "Dụng cụ sản xuất", "useful_period_default": 12},
    {"category_name": "Đồ bảo hộ", "useful_period_default": 12},
    {"category_name": "Khác", "useful_period_default": 12},
]
```

---

### Task 2.3 — DocType `CCDC Item` (Submittable)

**Files:** standard 4-file pattern.

**Fields per design §4.2 + task spec:**
`item_code` (Link Item, reqd), `item_name` (Data, fetch from Item), `ccdc_category` (Link CCDC Category, reqd), `company` (Link Company, reqd), `location` (Link Location), `custodian` (Link Employee), `cost` (Currency, reqd), `cost_account` (Link Account, default from Category 153), `expense_account` (Link Account, default from Category 627/641/642), `prepayment_account` (Link Account, default 242), `purchase_date` (Date), `available_for_use_date` (Date — required for submit), `useful_period_months` (Int), `allocation_periods` (Int, default useful_period_months), `status` (Select: Mới mua\nĐang sử dụng\nHết phân bổ\nĐã ghi giảm), `purchase_invoice` (Link Purchase Invoice, read_only), `purchase_invoice_item` (Data, hidden), `scope_for_handover` (Hidden, default "CCDC").

**Controller `ccdc_item.py`:**
```python
class CCDCItem(Document):
    def validate(self):
        if (self.cost or 0) <= 0:
            frappe.throw(_("Nguyên giá phải > 0"))
        if (self.useful_period_months or 0) <= 0:
            frappe.throw(_("Số tháng sử dụng phải > 0"))
        if (self.allocation_periods or 0) < 1:
            frappe.throw(_("Số kỳ phân bổ phải ≥ 1"))

    def on_submit(self):
        if not self.available_for_use_date:
            frappe.throw(_("Phải nhập ngày đưa vào sử dụng trước khi submit"))
        from vn_accounting.asset.journal_entry_builder import create_ccdc_putinuse_je
        create_ccdc_putinuse_je(self)  # N 242 / C 153
        from vn_accounting.asset.ccdc_allocation import create_allocation_schedule
        create_allocation_schedule(self)
        self.status = "Đang sử dụng"

    def on_cancel(self):
        # Cancel allocation schedule if not yet allocated
        ...
```

---

### Task 2.4 — DocType `CCDC Allocation Schedule` (Submittable)

**Fields:** `ccdc_item` (Link CCDC Item, reqd), `start_date` (Date, reqd), `total_amount` (Currency, reqd), `periods` (Int, reqd), `frequency` (Select Monthly), `allocation_entries` (Table → CCDC Allocation Entry), `status` (Select Active\nCompleted\nCancelled).

---

### Task 2.5 — DocType `CCDC Allocation Entry` (Child)

**Fields:** `period_no` (Int, in_list_view), `period_start_date` (Date, in_list_view), `allocation_amount` (Currency, in_list_view), `journal_entry` (Link Journal Entry, read_only, in_list_view), `status` (Select: Pending\nPosted, default Pending), `posted_at` (Datetime, read_only).

---

### Task 2.6 — Allocation logic (`ccdc_allocation.py`)

**File:** `vn_accounting/asset/ccdc_allocation.py`

**Outline:**
```python
def create_allocation_schedule(ccdc_item):
    from frappe.utils import add_months, getdate
    sched = frappe.new_doc("CCDC Allocation Schedule")
    sched.ccdc_item = ccdc_item.name
    sched.start_date = ccdc_item.available_for_use_date
    sched.total_amount = ccdc_item.cost
    sched.periods = ccdc_item.allocation_periods
    sched.frequency = "Monthly"
    n = ccdc_item.allocation_periods
    base_amount = round(ccdc_item.cost / n, 0)
    accumulated = 0
    for i in range(1, n + 1):
        amt = base_amount if i < n else (ccdc_item.cost - accumulated)  # last period absorbs rounding
        accumulated += amt
        sched.append("allocation_entries", {
            "period_no": i,
            "period_start_date": add_months(ccdc_item.available_for_use_date, i - 1),
            "allocation_amount": amt,
            "status": "Pending",
        })
    sched.insert(ignore_permissions=True)
    sched.submit()
    return sched.name


def post_allocation_period(entry_name):
    """Build JE N expense / C 242 and link to entry."""
    ...
```

---

### Task 2.7 — Scheduler hook `allocate_ccdc_monthly`

**Files:**
- `vn_accounting/tasks.py` (new module if not exist) OR `vn_accounting/asset/scheduled.py`
- `vn_accounting/hooks.py` — add to `scheduler_events.daily`:
  ```python
  scheduler_events = {
      "daily": ["vn_accounting.tasks.allocate_ccdc_monthly", ...]
  }
  ```

**Function:**
```python
def allocate_ccdc_monthly():
    today = frappe.utils.getdate()
    pending = frappe.db.sql("""
        SELECT name FROM `tabCCDC Allocation Entry`
        WHERE status='Pending' AND period_start_date <= %s
    """, today, as_dict=True)
    for row in pending:
        try:
            post_allocation_period(row.name)
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"CCDC allocation failed for {row.name}")
            continue
    # Mark CCDC Items where all entries posted
    _close_completed_ccdc_items()
```

---

### Task 2.8 — Hook PI on_submit (auto-create CCDC Item)

**Files:**
- `vn_accounting/asset/pi_hooks.py` (new)
- `vn_accounting/hooks.py` — `doc_events["Purchase Invoice"]["on_submit"]` add new hook (preserve existing).

**Function:**
```python
def on_pi_submit(doc, method=None):
    from vn_accounting.asset.journal_entry_builder import auto_create_ccdc_drafts
    auto_create_ccdc_drafts(doc)


def auto_create_ccdc_drafts(pi_doc):
    for item_row in pi_doc.items:
        if frappe.db.get_value("Item", item_row.item_code, "is_low_value_asset"):
            existing = frappe.db.exists("CCDC Item", {"purchase_invoice": pi_doc.name,
                                                      "purchase_invoice_item": item_row.name})
            if existing:
                continue
            ccdc = frappe.new_doc("CCDC Item")
            ccdc.item_code = item_row.item_code
            ccdc.item_name = item_row.item_name
            ccdc.cost = item_row.amount
            ccdc.purchase_date = pi_doc.posting_date
            ccdc.purchase_invoice = pi_doc.name
            ccdc.purchase_invoice_item = item_row.name
            ccdc.company = pi_doc.company
            ccdc.status = "Mới mua"
            ccdc.insert(ignore_permissions=True)
```

---

### Task 2.9 — DocType `CCDC Writeoff` (Submittable)

**Fields:** `ccdc_item` (Link CCDC Item, reqd, filter docstatus=1 + status != "Đã ghi giảm"), `writeoff_date` (Date, reqd), `writeoff_reason` (Select Mất\nHỏng không sửa được\nHết hạn sử dụng\nKhác), `compensation_amount` (Currency, default 0), `compensation_employee` (Link Employee, depends_on `compensation_amount > 0`), `remaining_242_amount` (Currency, read_only), `remaining_153_amount` (Currency, read_only), `remarks` (Text), `je_242` (Link Journal Entry, read_only), `je_153` (Link Journal Entry, read_only).

**Controller `ccdc_writeoff.py`:**
```python
def validate(self):
    self._compute_remaining_amounts()

def on_submit(self):
    from vn_accounting.asset.journal_entry_builder import create_ccdc_writeoff_jes
    create_ccdc_writeoff_jes(self)
    self._cancel_pending_allocation_entries()
    frappe.db.set_value("CCDC Item", self.ccdc_item, "status", "Đã ghi giảm")

def _compute_remaining_amounts(self):
    pending_sum = frappe.db.sql("""
        SELECT COALESCE(SUM(allocation_amount), 0)
        FROM `tabCCDC Allocation Entry` ae
        JOIN `tabCCDC Allocation Schedule` s ON ae.parent = s.name
        WHERE s.ccdc_item = %s AND ae.status = 'Pending'
    """, self.ccdc_item)[0][0]
    self.remaining_242_amount = pending_sum
    # 153 remains only if CCDC never put in use (status == "Mới mua")
    item_status = frappe.db.get_value("CCDC Item", self.ccdc_item, "status")
    if item_status == "Mới mua":
        self.remaining_153_amount = frappe.db.get_value("CCDC Item", self.ccdc_item, "cost")
    else:
        self.remaining_153_amount = 0
```

---

### Task 2.10 — Print format Biên bản ghi giảm CCDC

**Files:** `vn_accounting/vn_accounting/print_format/ccdc_writeoff_report/{__init__.py,*.json,*.html}` — 2-sign template (Bên giữ / Kế toán) per design §6.

---

### Task 2.11 — Sidebar update — enable CCDC links

After Phase 2 DocTypes exist, update sidebar links to point to live CCDC Item / CCDC Allocation Schedule / CCDC Writeoff routes (replace placeholders from Task 1.8).

---

### Task 2.12 — Phase 2 verification + commit

Run all `Phase 2 CCDC Backbone` acceptance criteria. Commit:
`git commit -m "feat(asset-polishing): Phase 2 CCDC backbone complete + QA pass"`.

---

## Phase 3 — Bàn giao + Kiểm kê

### Task 3.1 — DocType `Asset Handover` (Submittable)

**Fields per design §4.3:** `scope` (Select TSCĐ\nCCDC, reqd, fetch_default from `frappe.route_options`), `posting_date` (Date, reqd, default Today), `from_employee`, `from_department`, `to_employee` (reqd), `to_department`, `to_location`, `co_signer_employee`, `handover_items` (Table → Asset Handover Item), `total_asset_value` (Currency, read_only, calc from child), `reason` (Small Text), `remarks` (Text), `before_handover_snapshot` (Long Text JSON, read_only, hidden).

**Controller `asset_handover.py`:**
```python
def validate(self):
    self._validate_scope_match()
    self._calc_total_value()
    self._validate_threshold()
    if self.docstatus == 0:
        self._snapshot_before_state()

def on_submit(self):
    self._update_targets()
    if self.scope == "TSCĐ":
        self._create_movement_shadow()

def on_cancel(self):
    self._revert_from_snapshot()

def _validate_scope_match(self):
    expected = "Asset" if self.scope == "TSCĐ" else "CCDC Item"
    for row in self.handover_items:
        if row.target_doctype != expected:
            frappe.throw(_("Item phải khớp scope {0}").format(self.scope))

def _validate_threshold(self):
    settings = frappe.get_single("VN Accounting Settings")
    if settings.enable_value_thresholds and (self.total_asset_value or 0) >= (settings.handover_threshold or 0):
        if not self.co_signer_employee:
            frappe.throw(_("Tổng giá trị bàn giao ≥ {0}đ — cần đồng ký bởi nhân viên thứ hai").format(settings.handover_threshold))
```

---

### Task 3.2 — DocType `Asset Handover Item` (Child)

**Fields:** `target_doctype` (Link DocType, reqd, filter via JS to Asset/CCDC Item only), `target_name` (Dynamic Link → target_doctype, reqd), `asset_name` (Data, read_only, fetch from target), `book_value` (Currency, read_only, fetch from target), `serial_no` (Data), `remarks` (Small Text).

**JS `asset_handover.js`:**
```js
frappe.ui.form.on('Asset Handover Item', {
    target_doctype(frm, cdt, cdn) {
        const row = frappe.get_doc(cdt, cdn);
        // restrict via parent.scope
    }
});

frappe.ui.form.on('Asset Handover', {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("📋 Sao chép sang phiếu CCDC"), () => duplicate_with_flipped_scope(frm));
        }
    }
});
```

---

### Task 3.3 — Print format Biên bản bàn giao S22-DN

**Files:** `vn_accounting/vn_accounting/print_format/asset_handover_s22_dn/{__init__.py,*.json,*.html}`.

**Jinja branches:** if `doc.scope == "TSCĐ"` render 01-TSCĐ TT99 layout; else S22-DN CCDC layout. 3-sign + co_signer when present.

---

### Task 3.4 — DocType `Asset Stocktake` (Workflow)

**Fields per design §4.4:** `scope`, `stocktake_date`, `location` (reqd), `department`, `stocktake_team_lead`, `storekeeper`, `accountant`, `stocktake_items` (Table), `total_difference_value`, `difference_resolution`, `workflow_state` (managed by Workflow doc).

**Whitelisted button method:**
```python
@frappe.whitelist()
def load_items(stocktake_name):
    self = frappe.get_doc("Asset Stocktake", stocktake_name)
    if self.scope == "TSCĐ":
        rows = frappe.db.get_all("Asset",
            filters={"location": self.location, "status": ["not in", ["Disposed", "Lost"]]},
            fields=["name", "asset_name", "value_after_depreciation"])
        target_dt = "Asset"
    else:
        rows = frappe.db.get_all("CCDC Item",
            filters={"location": self.location, "status": ["!=", "Đã ghi giảm"]},
            fields=["name", "item_name", "cost"])
        target_dt = "CCDC Item"
    self.stocktake_items = []
    for r in rows:
        self.append("stocktake_items", {"target_doctype": target_dt,
                                        "target_name": r.name,
                                        "book_value": r.get("value_after_depreciation") or r.get("cost"),
                                        "physical_status": "Còn nguyên"})
    self.save()
```

---

### Task 3.5 — DocType `Asset Stocktake Item` (Child)

**Fields:** `target_doctype` (Link DocType), `target_name` (Dynamic Link), `asset_name` (Data, read_only), `book_value` (Currency, read_only), `physical_status` (Select Còn nguyên\nHỏng\nMất, default Còn nguyên), `remarks` (Small Text), `last_stocktake_date` (Date, read_only).

---

### Task 3.6 — Workflow `Asset Stocktake Workflow`

**File:** `vn_accounting/fixtures/workflow.json` (append) OR new fixture file.

**States:** Draft, In Progress, Completed, Approved, Closed, Rejected.
**Transitions** per design §4.4.

**On approve:** wired via Server Script or Document Hook. Recommend wire via `vn_accounting.asset.stocktake_hooks.on_state_change` reading `workflow_state` change in `on_update` of Asset Stocktake.

---

### Task 3.7 — Stocktake on_approve JE generation

**File:** `vn_accounting/asset/stocktake_hooks.py`

```python
def on_update(doc, method=None):
    if doc.workflow_state == "Approved" and (doc.get_doc_before_save() or {}).workflow_state != "Approved":
        process_approval(doc)


def process_approval(doc):
    from vn_accounting.asset.journal_entry_builder import create_stocktake_loss_je
    je_built = []
    for item in doc.stocktake_items:
        if item.physical_status == "Mất":
            je = create_stocktake_loss_je(doc, item)
            je_built.append(je)
            _update_target_status(item, "Lost")
        elif item.physical_status == "Hỏng":
            _update_target_status(item, "Damaged")
        # Còn nguyên: no action
        _set_last_stocktake_date(item, doc.stocktake_date)
```

---

### Task 3.8 — Print format Biên bản kiểm kê

**Files:** `vn_accounting/vn_accounting/print_format/asset_stocktake_report/{__init__.py,*.json,*.html}` — 3-sign (Trưởng đoàn / Thủ kho / Kế toán).

---

### Task 3.9 — Script Report Sổ S22-DN

**Files:** `vn_accounting/vn_accounting/report/s22_dn_theo_doi_tscd_ccdc/{__init__.py,*.json,*.py,*.js}`.

**Filters:** location (Link, optional), department (Link, optional), as_of_date (Date, default today), company (Link, reqd).

**Logic:** Union query over Asset (scope=TSCĐ) + CCDC Item (scope=CCDC) at the location. Group by location.

---

### Task 3.10 — Phase 3 verification + commit

Acceptance per task file Phase 3 Acceptance + Phase 3 QA Gate. Commit:
`git commit -m "feat(asset-polishing): Phase 3 bàn giao + kiểm kê complete + QA pass"`.

---

## Phase 4 — Demo Data + Final Integration QA + Docs

### Task 4.1 — Demo data seed

**File:** new `apps/dcnet_sample/dcnet_sample/asset_polishing_seed.py` OR extend `vn_accounting/setup_demo.py` if dcnet_sample integration unavailable on worktree-only branch.

**Seed:**
- 10 Asset (5 ghi tăng từ PI + 5 backdated, varied categories)
- 20 CCDC Item (10 đang phân bổ + 5 hết phân bổ + 5 đã ghi giảm)
- 5 Asset Handover (3 TSCĐ + 2 CCDC) to different departments
- 1 Asset Stocktake at "Văn phòng Hà Nội", Approved, with 1 Mất + 1 Hỏng

**Pattern:** wrap in `_create_*` helpers, idempotent via `frappe.db.exists` checks.

---

### Task 4.2 — Unit tests Tier 1

**Files:**
- `vn_accounting/tests/__init__.py`
- `vn_accounting/tests/test_ccdc_allocation.py`
- `vn_accounting/tests/test_permission_sync.py`
- `vn_accounting/tests/test_asset_repair.py`
- `vn_accounting/tests/test_stocktake.py`
- `vn_accounting/tests/test_s21_dn.py`

**Run via** `bench --site dcnet.localhost console` + `unittest.TestLoader().loadTestsFromTestCase(...)` (per `frappe-erpnext.md` rule — `bench run-tests` xung đột với sample data).

Coverage target: ≥80% for the 5 modules.

---

### Task 4.3 — Cross-phase integration QA

Capture screenshots `qa-screenshots/phase4-integration/` for full lifecycle TSCĐ + CCDC per task Acceptance. ≥8 PNG.

---

### Task 4.4 — Update CODEBASE.md / FEATURES.md / README.md

**Files:**
- `docs/CODEBASE.md` — list 9 new DocTypes + relationships in Asset section.
- `docs/CODEBASE_DETAIL.md` — 1 line per new file.
- `FEATURES.md` — mark C4.1 / C4.2 / C4.3 Done; add rows for Bàn giao S22-DN, Kiểm kê, Sửa chữa lớn vốn hóa.
- `README.md` — append asset-polishing to feature list if missing.

---

### Task 4.5 — Final commit

`git commit -m "feat(asset-polishing): v1.0 ship — TT99/2025 compliance, full TSCĐ + CCDC lifecycle"`.

---

## File Inventory (new + modified)

**New DocTypes (10):**
1. CCDC Category
2. CCDC Item
3. CCDC Allocation Schedule
4. CCDC Allocation Entry
5. CCDC Writeoff
6. Asset Handover
7. Asset Handover Item
8. Asset Stocktake
9. Asset Stocktake Item
10. Asset Permission Rule (child of VN Accounting Settings)

**New Python modules:**
- `vn_accounting/asset/__init__.py`
- `vn_accounting/asset/journal_entry_builder.py`
- `vn_accounting/asset/repair_hooks.py`
- `vn_accounting/asset/pi_hooks.py`
- `vn_accounting/asset/ccdc_allocation.py`
- `vn_accounting/asset/stocktake_hooks.py`
- `vn_accounting/tasks.py` (or `vn_accounting/asset/scheduled.py`)
- `vn_accounting/tests/test_*.py` × 5

**New print formats (5):**
- asset_repair_report
- ccdc_writeoff_report
- asset_handover_s22_dn
- asset_stocktake_report
- (asset_disposal_report exists — reuse)

**New Script Reports (2):**
- s21_dn_so_tscd
- s22_dn_theo_doi_tscd_ccdc

**Modified files:**
- `vn_accounting/chart_of_accounts/vn_small_enterprise.json`, `vn_large_enterprise.json` (TK 242 rename + verify 211 group)
- `vn_accounting/translations/vi.csv` (~30+50 entries)
- `vn_accounting/fixtures/property_setter.json` (Asset.depreciation_method)
- `vn_accounting/fixtures/custom_field.json` (5 entries)
- `vn_accounting/fixtures/asset_permission_defaults.json` (NEW, ~16 rows)
- `vn_accounting/fixtures/workflow.json` (Asset Stocktake Workflow)
- `vn_accounting/workspace_sidebar/vn_accounting.json` (split TSCĐ & CCDC into 2 sections, +CCDC links)
- `vn_accounting/install.py` (add asset_category re-seed + ccdc_category seed + permission defaults loader)
- `vn_accounting/hooks.py` (doc_events PI + Asset Repair + scheduler_events daily)
- `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.{json,py,js}` (extend)
- `docs/CODEBASE.md`, `docs/CODEBASE_DETAIL.md`, `FEATURES.md`, `README.md`

---

## Self-Review Notes

### 1. Spec coverage check

Walked every section of design spec → confirmed mapping to plan tasks:

| Spec section | Plan task(s) |
|---|---|
| §1 Mục tiêu | All phases |
| §2 Bối cảnh TT99 | Task 1.1 (TK 242), Task 1.4 (re-seed) |
| §3.1-3.2 Architecture / DocType inventory | Phase 2 + 3 (10 DocTypes) |
| §3.3 Account routing | Task 1.6 (Asset Repair JE), Task 2.3/2.6/2.9 (CCDC), Task 3.7 (Stocktake) |
| §3.4 Dynamic Link | Tasks 3.2, 3.5 |
| §4.1 TSCĐ Lifecycle | Phase 1 (Repair) + Phase 3 (Handover, Stocktake), Asset Disposal already exists |
| §4.2 CCDC Lifecycle | Phase 2 entirely |
| §4.3 Asset Handover | Task 3.1, 3.2, 3.3 |
| §4.4 Stocktake | Tasks 3.4-3.8 |
| §4.5 Asset Repair | Task 1.6, 1.7 |
| §5 Sidebar | Tasks 1.8 + 2.11 |
| §6 Print formats | 9 print formats — Asset Disposal exists; build 5 (Repair, Writeoff, Handover/S22-DN, Stocktake, Asset Ghi tăng 01-TSCĐ deferred since `Asset` ghi tăng print is informational; spec lists 9 formats but design §6 row 9 says "Biên bản giao nhận TSCĐ" which is essentially Asset Handover (TSCĐ) — already covered by `asset_handover_s22_dn` Jinja-branched). **Initial scan flagged this as missing — see fix below.** |
| §7.1-7.5 i18n + categories | Tasks 1.3, 1.4, 2.2, 1.2 |
| §8 TT99 compliance items | Tasks 1.1, 1.9 (S21), 3.9 (S22), 1.4, 2.2, 1.2; "Theo sản lượng" → out-of-scope per §13 |
| §9 Settings tab | Tasks 1.10, 1.11, 1.12 |
| §10 Edge cases | Distributed across tasks (snapshot in 3.1, idempotent in 4.1, threshold flag-gated in 3.1, etc.) |
| §11 Phasing | Mirrored 1:1 |
| §12 Testing | Task 4.2 (Tier 1); Tier 2/3 are QA Gates per task file |
| §13 Out of scope | Honored (no plan tasks for revaluation, units of production, dept hierarchy v2, BĐS đầu tư) |
| §14 References | N/A (informational) |

### 2. Placeholder scan

- No TBD/TODO entries in plan tasks except those explicitly marked Out-of-Scope per design §13:
  - Asset Value Adjustment (Settings flag default off)
  - "Theo sản lượng" depreciation method (README note)
  - "Trưởng phòng xem cấp con" (read_only field placeholder)
- Found minor `...` in code outline placeholders (CCDC Item `on_cancel`, JE builder `create_capitalization_je` account lookup) — these are intentional outline-level abbreviations. Implementation must fill them; not a TBD.

### 3. Type consistency

DocType names cross-checked with task spec, design spec, and Verification Commands:

| Name in plan | Name in task file | Name in design spec | OK? |
|---|---|---|---|
| CCDC Item | CCDC Item | CCDC Item | ✓ |
| CCDC Category | CCDC Category | CCDC Category | ✓ |
| CCDC Allocation Schedule | CCDC Allocation Schedule | CCDC Allocation Schedule | ✓ |
| CCDC Allocation Entry | CCDC Allocation Entry | CCDC Allocation Entry | ✓ |
| CCDC Writeoff | CCDC Writeoff | CCDC Writeoff | ✓ |
| Asset Handover | Asset Handover | Asset Handover | ✓ |
| Asset Handover Item | Asset Handover Item | Asset Handover Item | ✓ |
| Asset Stocktake | Asset Stocktake | Asset Stocktake | ✓ |
| Asset Stocktake Item | Asset Stocktake Item | Asset Stocktake Item | ✓ |
| Asset Permission Rule | Asset Permission Rule | Asset Permission Rule | ✓ |

Account numbers consistent: 242, 211, 153, 214x, 627/641/642, 1381, 3381, 241, 632, 811, 711, 412 — match TT99 numbering used in design §3.3.

Field names cross-checked between Handover Item and Stocktake Item per Dynamic Link pattern in §3.4: both use `target_doctype` + `target_name`. ✓

### 4. Self-fixes applied inline

- **Print format count:** initial pass undercounted print formats. Spec §6 lists 9; with Asset Disposal existing, building 4 print formats covers the gap if `Asset Handover` Jinja branches handle both TSCĐ and CCDC layouts (saves 1 file). Stocktake similarly is 1 format (Jinja branches); Repair = 1; Writeoff = 1. Final count: 4 new print formats. Verification commands list 4 (`asset_handover_s22_dn`, `asset_stocktake_report`, `ccdc_writeoff_report`, `asset_repair_report`) — matches. The 9th in design §6 row "Biên bản giao nhận TSCĐ" (01-TSCĐ form) is rendered by Asset Handover (TSCĐ scope) per the Jinja branch — no separate format needed. Plan adjusted: File Inventory now lists 4 new print formats, not 5. (Corrected during self-review.)
- **Permission defaults row count:** design §9.3 fixture shows 16 rows; spec acceptance says ≥15. Plan adopts ≥15 minimum, target 16 to match design. Verification command checks `>=15`.
- **Threshold flag gating:** design §9.5 distinguishes 2 flag-gated (thanh lý, bàn giao) vs 1 always-on (ghi tăng TSCĐ). Plan Task 3.1 reflects this — only handover threshold + flag check.
- **Asset Movement bóng:** design §3.2 says hide Asset Movement from sidebar but keep DocType native. Plan Task 3.1 `_create_movement_shadow()` confirms shadow record creation on TSCĐ handover for ERPNext audit; cancel uses `before_handover_snapshot`, not Asset Movement (per edge case 17).
- **Scheduler frequency:** spec §11 Sprint 2 says "scheduler chạy đầu tháng 5". Plan uses `daily` scheduler that filters `period_start_date <= today` — handles gaps if site offline on the 1st. Idempotent via `status=Pending` filter.
- **Live testing dance:** worktree → apps/ sync per `git-deploy.md` rule "Worktree ↔ Bench-Apps Deployment Dance" — plan does NOT bake this into Verification Commands (those must be assertion-only per `multi-session.md` rule 13). Live test commands belong in `## Live Testing Procedure` of task file, not plan.

### 5. Risks and unknowns

- **Workflow on_approve hook timing:** Frappe Workflow state changes do NOT trigger document `on_submit` automatically when the doc is already submitted. Task 3.7 wires via `on_update` checking `workflow_state` delta. If this fails in practice, fallback is Server Script attached to Workflow Action.
- **CCDC scheduler idempotency:** if scheduler runs twice in same day, `_close_completed_ccdc_items()` sets status only once (idempotent). `post_allocation_period` checks entry.status before posting — idempotent.
- **Permission Matrix conflict with Standard DocPerm:** edge case 14 — Custom DocPerm wins per Frappe behavior. Plan does NOT delete Standard DocPerm rows; only manages Custom rows for the 9 affected DocTypes per design §9.4.
- **Print format Jinja branch:** spec §6 promises one Asset Handover print format renders both TSCĐ (01-TSCĐ TT99) and CCDC (S22-DN) layouts. Implementation must keep `if doc.scope == "TSCĐ"` branch clean.

### 6. Phase ordering rationale

Phase 1 must complete first because:
- TK 242 rename precedes any JE that posts to 242.
- Settings + permission_matrix + sync logic precedes any DocType creation that needs Custom DocPerm rules.
- Sidebar reorg with placeholders allows Phase 2/3 to add live links incrementally.

Phase 2 must complete before Phase 3 because:
- Asset Handover and Stocktake rely on `CCDC Item` existing (Dynamic Link target).
- Stocktake `Tải danh sách` queries CCDC Item.

Phase 4 must complete last because:
- Demo data spans all phases.
- Cross-phase integration QA tests full lifecycle.
- Docs reflect final shipping state.

### 7. Time estimate sanity check

Task file budget: 20 hours, 40 sessions.
- Phase 1: 13 sub-tasks ≈ 5 sessions impl + 3 QA = 8 sessions.
- Phase 2: 12 sub-tasks ≈ 6 sessions impl + 2 QA = 8 sessions.
- Phase 3: 10 sub-tasks ≈ 6 sessions impl + 4 QA = 10 sessions.
- Phase 4: 5 tasks ≈ 4 sessions.
- Plan (Phase 0): 1 session (this one).
- **Total: ~31 sessions, well within 40-session safety limit.**

---

## Cross-cutting Conventions

**File size:** Per `programming.md`, target ≤500 lines, hard limit 800. JE builder + allocation + stocktake hooks should stay <500 each by splitting if needed.

**Naming:** English internal names. Vietnamese only in `label` JSON fields and `vi.csv` translation pairs. (`frappe.md` "Vietnamese App Naming")

**Security:** All SQL parameterized with `%s` + values dict (`frappe.md` SQL Injection rule). No f-string SQL. All API endpoints `@frappe.whitelist()` with explicit permission checks.

**Cache invalidation:** Use `frappe.get_doc(...).save()` for cacheable DocTypes per `frappe-spa.md` rule. After any sidebar JSON edit run `bench build --app vn_accounting`.

**Worktree dance:** All commits made IN the worktree (`.worktrees/vn_accounting-asset-polishing/`). Sync apps/ via `git -C apps/vn_accounting checkout --detach feat/asset-polishing` before bench build.

**Backdated docs:** When generators/seeds create historical Asset/Handover/Stocktake docs, set `doc.set_posting_time = 1` BEFORE `doc.posting_date` (per `frappe-erpnext.md` rule).

**Fixtures auto-export:** After modifying Custom Fields / Property Setters / Workflow via Desk, run `bench --site dcnet.localhost export-fixtures` to refresh `fixtures/*.json`. Better: edit fixture JSON directly and `bench --site dcnet.localhost migrate`.
