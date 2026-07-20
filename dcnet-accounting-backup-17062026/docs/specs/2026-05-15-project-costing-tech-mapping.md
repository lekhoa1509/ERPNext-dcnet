# Tech Mapping — Tính giá thành công trình (FB-00605)

**Source:** `2026-05-15-project-costing-business-logic.md` (BL spec v0.4)
**Module location:** `apps/vn_accounting/vn_accounting/project_costing/`
**Implementation strategy:** single-session phases (KHÔNG dùng multi-session runner). 7 phases, 10-13 sessions ước tính, 4-5 PRs cluster `dcnet-cloud/dcnet-accounting`.
**TT99/2025 binding:** chuỗi GL 627 → 154 → 632 cho doanh nghiệp xây lắp / thi công công trình.

> Tài liệu này CHỈ chi tiết kỹ thuật. Phần nghiệp vụ thuần ở BL spec — KHÔNG lặp lại các quyết định nghiệp vụ ở đây.

## Mục lục

1. [Cấu trúc thư mục](#1-cấu-trúc-thư-mục)
2. [DocType schemas](#2-doctype-schemas)
3. [Custom Fields trên DocType ERPNext](#3-custom-fields-trên-doctype-erpnext)
4. [Property Setters](#4-property-setters)
5. [VN Accounting Settings — 4 fields mới](#5-vn-accounting-settings--4-fields-mới)
6. [Hooks (doc_events) + GL engines](#6-hooks-doc_events--gl-engines)
7. [Whitelisted API endpoints](#7-whitelisted-api-endpoints)
8. [Pivot Tool Page (React SPA)](#8-pivot-tool-page-react-spa)
9. [Embedded "Bút toán liên quan" section](#9-embedded-bút-toán-liên-quan-section)
10. [Reports](#10-reports)
11. [Workspace sidebar items](#11-workspace-sidebar-items)
12. [Translations](#12-translations)
13. [Permissions matrix → DocPerm](#13-permissions-matrix--docperm)
14. [Demo data scenarios](#14-demo-data-scenarios)
15. [Test coverage matrix](#15-test-coverage-matrix)
16. [vn_help articles](#16-vn_help-articles)
17. [Implementation order (phases)](#17-implementation-order-phases)
18. [Self-review notes](#18-self-review-notes)

---

## 1. Cấu trúc thư mục

App có 3-level nesting: `apps/vn_accounting/vn_accounting/vn_accounting/` (inner) chứa DocType + Page + Report JSONs theo convention Frappe. `apps/vn_accounting/vn_accounting/` (outer) chứa sub-packages utility code (asset/, landed_cost/, purchase/, treasury/, ...). Phase 1 + sau follow split này.

```
apps/vn_accounting/vn_accounting/                       ← outer
├── project_costing/                                    ← outer sub-package (code only)
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── allocation_engine.py        ← Cost Allocation Run submit/cancel → JE bù
│   │   ├── cogs_engine.py              ← SI on_submit/cancel → JE 632 ↔ 154
│   │   ├── wip_override_engine.py      ← SE/DN/PI/EC on_submit → JE bù WIP override
│   │   ├── close_engine.py             ← Project Costing close → balance check + write-off JE
│   │   ├── pivot_service.py            ← Pivot Tool 4 endpoints
│   │   ├── markup_calc.py              ← 6 markup methods pure functions
│   │   └── je_trace.py                 ← embedded section data fetch
│   └── tests/
│       ├── __init__.py
│       ├── test_allocation_engine.py
│       ├── test_cogs_engine.py
│       ├── test_wip_override_engine.py
│       ├── test_close_engine.py
│       ├── test_markup_calc.py
│       └── test_pivot_service.py
├── vn_accounting/                                      ← inner: DocTypes + Pages + Reports
│   ├── doctype/
│   │   ├── project_costing/
│   │   │   ├── project_costing.json
│   │   │   ├── project_costing.py
│   │   │   ├── project_costing.js
│   │   │   └── test_project_costing.py
│   │   ├── project_costing_stage/
│   │   │   ├── project_costing_stage.json
│   │   │   └── project_costing_stage.py
│   │   ├── cost_allocation_run/
│   │   │   ├── cost_allocation_run.json
│   │   │   ├── cost_allocation_run.py
│   │   │   └── cost_allocation_run.js
│   │   ├── cost_allocation_share/        ← child table
│   │   │   ├── cost_allocation_share.json
│   │   │   └── cost_allocation_share.py
│   │   └── cost_allocation_source/       ← child table
│   │       ├── cost_allocation_source.json
│   │       └── cost_allocation_source.py
│   ├── page/
│   │   └── project_costing_pivot/
│   │       ├── project_costing_pivot.json
│   │       ├── project_costing_pivot.py     ← empty handler shim
│   │       └── project_costing_pivot.js     ← page handler (ES5)
│   └── report/
│       ├── project_cost_collection/         ← Bảng tập hợp chi phí công trình
│       ├── project_invoicing_progress/      ← Bảng tiến độ xuất HĐ
│       └── project_pnl_detailed/            ← P&L 3-nhóm-cột
├── public/js/
│   ├── project_costing_jes_section.bundle.js    ← embedded section trên Project Costing form
│   └── project_costing_pivot.bundle.jsx         ← React SPA → built to dist
├── fixtures/
│   ├── custom_field.json                 ← +N entries (mục §3)
│   ├── property_setter.json              ← +1 entry (mục §4)
│   └── workspace_sidebar.json hoặc workspace_sidebar/vn_accounting.json   ← +3 items (mục §11)
├── translations/vi.csv                   ← +30-40 strings (mục §12)
└── help/portal/cong-trinh/               ← vn_help articles (mục §16)
    ├── cong-trinh-tinh-gia-thanh.md
    ├── stage-markup.md
    ├── pivot-tool.md
    ├── allocation-run.md
    └── close-project.md
```

Hooks.py thay đổi (xem §6 chi tiết): thêm `doc_events` cho 5 DocType ERPNext + 2 DocType mới; thêm `app_include_js`; thêm `permission_query_conditions` cho 3 DocType mới; thêm Property Setter fixture filter.

---

## 2. DocType schemas

### 2.1 Project Costing (parent — không submittable)

| Property | Value |
|---|---|
| `name` | `Project Costing` |
| `module` | `VN Accounting` |
| `autoname` | `field:project` (1:1 với Project, name = project name) |
| `is_submittable` | 0 (không submit; toàn bộ logic gắn vào SI/JE submit) |
| `track_changes` | 1 |
| `track_seen` | 1 |
| `naming_rule` | `By fieldname` |

**Fields:**

| Fieldname | Type | Options | Label | reqd | read_only | Note |
|---|---|---|---|---|---|---|
| `project` | Link | Project | Công trình | 1 | 1 sau khi save | unique, autoname source |
| `project_name` | Data | - | Tên công trình | 0 | 1 | Fetch from Project |
| `customer` | Link | Customer | Khách hàng | 0 | 1 | Fetch from Project |
| `contract` | Link | DCNET Contract | HĐ khung | 0 | 0 | optional — chỉ cho HĐ khung |
| `company` | Link | Company | Công ty | 1 | 0 | |
| `status` | Select | `Đang thi công\nĐã hoàn thành\nĐã hủy` | Trạng thái | 1 | 1 | controller-managed |
| `column_break_1` | Column Break | | | | | |
| `markup_default_method` | Select | (6 markup methods, xem §2.2) | Phương pháp markup mặc định | 0 | 0 | inherited by new stages |
| `closed_on` | Date | - | Ngày đóng | 0 | 1 | set khi close |
| `writeoff_je` | Link | Journal Entry | Bút toán write-off | 0 | 1 | set khi close có dư |
| `section_break_stages` | Section Break | | Giai đoạn | | | |
| `stages_html` | HTML | - | (placeholder) | 0 | 1 | rendered list of Project Costing Stage rows (separate doctype, joined via parent_costing) |
| `section_break_jes` | Section Break | | Bút toán liên quan | | | |
| `jes_section_html` | HTML | - | (placeholder) | 0 | 1 | populated by `project_costing_jes_section.bundle.js` (xem §9) |

**Controller (`project_costing.py`):**

```python
class ProjectCosting(Document):
    def autoname(self):
        self.name = self.project   # 1:1 with Project

    def validate(self):
        self._fetch_project_fields()
        self._validate_status_transition()

    def _fetch_project_fields(self):
        if not self.project_name or not self.customer:
            p = frappe.db.get_value("Project", self.project,
                ["project_name", "customer", "company"], as_dict=True)
            if p:
                self.project_name = p.project_name
                self.customer = p.customer
                self.company = self.company or p.company

    def _validate_status_transition(self):
        # Đang thi công → Đã hoàn thành (via close button)
        # Đang thi công → Đã hủy (via cancel button)
        # Đã hoàn thành → Đang thi công (reopen)
        # No direct edit of status field (read_only)
        pass

    @frappe.whitelist()
    def close(self, writeoff_account=None, writeoff_amount=0, force=False):
        """Triggered by "Đóng công trình" button. See close_engine.close_project()."""
        from vn_accounting.project_costing.services.close_engine import close_project
        return close_project(self, writeoff_account=writeoff_account,
                             writeoff_amount=writeoff_amount, force=force)
```

**JS (`project_costing.js`):**

- Buttons: "Đóng công trình" (khi status = Đang thi công), "Mở lại" (khi status = Đã hoàn thành), "Hủy công trình" (khi status = Đang thi công), "Mở Pivot Tool" (always).
- Sub-render Stages list inside `stages_html` (table layout) with quick actions per stage.

### 2.2 Project Costing Stage (standalone — không submittable)

| Property | Value |
|---|---|
| `name` | `Project Costing Stage` |
| `module` | `VN Accounting` |
| `autoname` | `format:{parent_costing}-S{stage_order:02d}` (vd: `PROJ-XYZ-S01`) |
| `is_submittable` | 0 |
| `track_changes` | 1 |

**Fields:**

| Fieldname | Type | Options | Label | reqd | read_only | depends_on | Note |
|---|---|---|---|---|---|---|---|
| `parent_costing` | Link | Project Costing | Công trình | 1 | 0 | | |
| `stage_order` | Int | - | Thứ tự | 1 | 0 | | for sort |
| `stage_name` | Data | - | Tên giai đoạn | 1 | 0 | | vd "Khảo sát", "Thi công" |
| `column_break_1` | Column Break | | | | | | |
| `expected_invoice_date` | Date | - | Ngày dự kiến xuất HĐ | 0 | 0 | | for "tiến độ xuất HĐ" report |
| `status` | Select | (6 trạng thái, xem dưới) | Trạng thái | 1 | 1 | | engine-managed |
| `section_markup` | Section Break | | Tính giá | | | | |
| `markup_method` | Select | (6 methods, xem dưới) | Phương pháp markup | 1 | 0 | | |
| `markup_value` | Float | - | Giá trị markup | 0 | 0 | | meaning depends on method |
| `column_break_2` | Column Break | | | | | | |
| `planned_amount` | Currency | - | Giá kế hoạch | 0 | 0 | | optional reference |
| `cost_pinned` | Currency | - | Chi phí đã pin | 0 | 1 | | derived (engine) |
| `price_suggested` | Currency | - | Giá đề xuất (theo công thức) | 0 | 1 | | derived |
| `price_override` | Currency | - | Giá KTT chốt | 0 | 0 | | KTT may type any number |
| `override_reason` | Small Text | - | Lý do override | 0 | 0 | | shown if price_override ≠ price_suggested |
| `override_by` | Link | User | Người override | 0 | 1 | | auto-set on price_override change |
| `override_on` | Datetime | - | Thời điểm override | 0 | 1 | | auto-set |
| `section_invoice` | Section Break | | Hóa đơn | | | | |
| `sales_invoice` | Link | Sales Invoice | Hóa đơn liên kết | 0 | 1 | | set when SI draft created |
| `cogs_je` | Link | Journal Entry | Bút toán giá vốn | 0 | 1 | | set on SI submit |

**Status options (6 states):**
- `Dự kiến` (initial)
- `Đang thi công` (cost being pinned)
- `Chờ xuất HĐ` (đủ chi phí, sẵn sàng SI)
- `Đã có SI draft` (sales_invoice set, docstatus=0)
- `Đã xuất HĐ` (sales_invoice docstatus=1)
- `Đã thu tiền` (SI Payment Schedule fully paid — derived, may auto-update)
- `Đã hủy` (parent project cancelled)

**Markup methods (6 options):**

| Code | Label | markup_value meaning |
|---|---|---|
| `coefficient` | Hệ số | hệ số nhân (vd 1.5) |
| `percent_cost` | % trên chi phí | % cộng thêm (vd 30 ⇒ +30%) |
| `fixed_amount` | Số tiền cố định | giá xuất bằng markup_value |
| `from_contract` | Theo HĐ / phụ lục | giá lấy từ DCNET Contract liên kết |
| `percent_contract` | % trên HĐ khung | % của contract value |
| `cost_to_date_uplift` | % trên cost đã phát sinh + uplift | % cộng thêm vào cost_pinned |

**Controller (`project_costing_stage.py`):**

```python
class ProjectCostingStage(Document):
    def validate(self):
        self._calc_price_suggested()
        self._track_override()
        self._lock_when_si_submitted()

    def _calc_price_suggested(self):
        from vn_accounting.project_costing.services.markup_calc import calculate_price
        self.price_suggested = calculate_price(
            method=self.markup_method,
            markup_value=self.markup_value,
            cost_pinned=flt(self.cost_pinned),
            parent_costing=self.parent_costing,
        )

    def _track_override(self):
        if self.has_value_changed("price_override"):
            self.override_by = frappe.session.user
            self.override_on = now_datetime()

    def _lock_when_si_submitted(self):
        if not self.sales_invoice:
            return
        si_docstatus = frappe.db.get_value("Sales Invoice", self.sales_invoice, "docstatus")
        if si_docstatus == 1:
            # Khóa toàn bộ fields trừ status update từ engine
            locked_changed = any(self.has_value_changed(f) for f in
                ["markup_method","markup_value","price_override","stage_name","stage_order"])
            if locked_changed:
                frappe.throw(_("Giai đoạn đã có hóa đơn submitted — không sửa được"))
```

### 2.3 Cost Allocation Run (submittable)

| Property | Value |
|---|---|
| `name` | `Cost Allocation Run` |
| `module` | `VN Accounting` |
| `autoname` | `CAR-.YYYY.-.MM.-.####` (vd `CAR-2026-05-0001`) |
| `is_submittable` | 1 |
| `track_changes` | 1 |

**Fields:**

| Fieldname | Type | Options | Label | reqd | read_only | Note |
|---|---|---|---|---|---|---|
| `run_period_start` | Date | - | Kỳ bắt đầu | 1 | 0 | |
| `run_period_end` | Date | - | Kỳ kết thúc | 1 | 0 | |
| `company` | Link | Company | Công ty | 1 | 0 | |
| `column_break_1` | Column Break | | | | | |
| `posting_date` | Date | - | Ngày hạch toán | 1 | 0 | default = run_period_end |
| `status` | Select | `Draft\nĐã tính\nĐã phân bổ\nĐã hủy` | Trạng thái | 1 | 1 | |
| `section_method` | Section Break | | Phương pháp phân bổ | | | |
| `method` | Select | `Đều\nThủ công` | Phương pháp | 1 | 0 | R10.3 |
| `section_sources` | Section Break | | Nguồn chi phí | | | |
| `source_costs` | Table | Cost Allocation Source | Chứng từ nguồn | 1 | 0 | child table — see §2.5 |
| `total_amount` | Currency | - | Tổng | 0 | 1 | derived from source_costs |
| `section_shares` | Section Break | | Chia ra projects | | | |
| `shares` | Table | Cost Allocation Share | Phân bổ | 1 | 0 | child — see §2.4 |
| `shares_total_percent` | Percent | - | Tổng % | 0 | 1 | validate = 100 |
| `shares_total_amount` | Currency | - | Tổng tiền | 0 | 1 | = total_amount |
| `section_je` | Section Break | | Bút toán | | | |
| `generated_je` | Link | Journal Entry | Bút toán đã sinh | 0 | 1 | set on submit |

**Controller (`cost_allocation_run.py`):**

```python
class CostAllocationRun(Document):
    def validate(self):
        self._recompute_total()
        self._validate_shares()

    def before_submit(self):
        self._validate_period_not_closed()
        self._validate_target_projects_not_invoiced()

    def on_submit(self):
        from vn_accounting.project_costing.services.allocation_engine import post_allocation_je
        post_allocation_je(self)

    def on_cancel(self):
        from vn_accounting.project_costing.services.allocation_engine import cancel_allocation_je
        cancel_allocation_je(self)

    @frappe.whitelist()
    def recompute_shares(self):
        from vn_accounting.project_costing.services.allocation_engine import compute_shares
        return compute_shares(self)
```

### 2.4 Cost Allocation Share (child)

| Fieldname | Type | Options | Label | reqd | in_list_view |
|---|---|---|---|---|---|
| `project` | Link | Project | Công trình | 1 | 1 |
| `project_name` | Data | - | Tên CT | 0 | 1 |
| `percent` | Percent | - | % | 1 | 1 |
| `amount` | Currency | - | Số tiền | 1 | 1 |
| `wip_account` | Link | Account | TK WIP | 0 | 0 |

`wip_account` mặc định null → engine sử dụng Settings `wip_account_project_costing` cho company. Optional override cho từng project (rare).

### 2.5 Cost Allocation Source (child)

| Fieldname | Type | Options | Label | reqd | in_list_view |
|---|---|---|---|---|---|
| `source_doctype` | Select | `Purchase Invoice\nStock Entry\nDelivery Note\nExpense Claim\nSalary Slip\nJournal Entry` | Loại chứng từ | 1 | 1 |
| `source_name` | Dynamic Link | source_doctype | Chứng từ | 1 | 1 |
| `description` | Small Text | - | Mô tả | 0 | 1 |
| `amount` | Currency | - | Số tiền | 1 | 1 |
| `cost_type` | Select | `Trực tiếp\nPhân bổ` | Loại chi phí | 1 | 1 | (must = Phân bổ) |

> **Note:** `Cost Allocation Source` chỉ lưu reference + amount. Allocation Run KHÔNG copy GL từ chứng từ gốc; KTT input/import thủ công, engine post JE riêng (Dr 154 / Cr 627 per share).

---

## 3. Custom Fields trên DocType ERPNext

Tất cả mới có `module = "VN Accounting"`, name format `<Parent>-<fieldname>`. Ship qua `fixtures/custom_field.json`. **Phải có `translatable: 0` cho Link/Select có options Vietnamese-fixed.**

### 3.1 `project_costing_stage` (Link → Project Costing Stage)

Thêm vào các DocType nguồn chi phí (5 entries):

| Parent DocType | insert_after | depends_on |
|---|---|---|
| Purchase Invoice Item | `project` | `eval:doc.project` |
| Stock Entry | `project` | `eval:doc.project` |
| Delivery Note Item | `project` | `eval:doc.project` |
| Expense Claim | `project` | `eval:doc.project` |
| Timesheet Detail | `project` | `eval:doc.project` |
| Sales Invoice | `project` | (no condition — used as link FROM stage to SI) |

Label tất cả: `"Giai đoạn công trình"`. Description: `"Pin chi phí vào 1 giai đoạn cụ thể của công trình. Bỏ trống → vào Common pool của công trình (pin sau qua Pivot Tool)."`

### 3.2 `wip_override_account` (Link → Account)

Thêm vào các DocType chi phí (4 entries):

| Parent DocType | insert_after | depends_on |
|---|---|---|
| Purchase Invoice Item | `project_costing_stage` | `eval:doc.project` |
| Stock Entry | `project_costing_stage` | `eval:doc.purpose=="Material Issue" && doc.project` |
| Delivery Note | `project_costing_stage` | `eval:doc.project` |
| Expense Claim | `project_costing_stage` | `eval:doc.project` |

Label: `"Tài khoản tập hợp chi phí công trình"`. Description: `"Mặc định 154 (WIP công trình). KTT có thể override per chứng từ — sẽ tạo bút toán bù tự động sau submit."`

### 3.3 `cost_type` (Select)

Options: `Trực tiếp\nPhân bổ`. Default `Trực tiếp`. translatable=0.

Thêm vào 4 DocType (same set as wip_override_account):

| Parent DocType | insert_after |
|---|---|
| Purchase Invoice Item | `wip_override_account` |
| Stock Entry | `wip_override_account` |
| Delivery Note | `wip_override_account` |
| Expense Claim | `wip_override_account` |

Label: `"Loại chi phí"`. Description: `"Trực tiếp = phát sinh hoàn toàn cho 1 công trình. Phân bổ = chi phí chung, chia ra nhiều công trình bằng Đợt phân bổ."`

### 3.4 Total Custom Fields = 15 entries

(5 project_costing_stage + 4 wip_override_account + 4 cost_type + 2 cho Sales Invoice + 1 cho Salary Slip Loan/allocation TBD)

> **Note Salary Slip:** Phase 1 chưa hỗ trợ Salary Slip allocation thủ công — chỉ Timesheet. Salary Slip handled via Allocation Run pattern (lương PM gián tiếp). Documented in BL R3.3 nhưng implement Phase 2.

---

## 4. Property Setters

### 4.1 `Journal Entry Account-reference_type-options`

Mở rộng Select options `Journal Entry Account.reference_type`. Ship qua `fixtures/property_setter.json`.

```json
{
  "doctype_or_field": "DocField",
  "doc_type": "Journal Entry Account",
  "field_name": "reference_type",
  "property": "options",
  "property_type": "Text",
  "value": "\nSales Invoice\nPurchase Invoice\nJournal Entry\nSales Order\nPurchase Order\nExpense Claim\nAsset\nLoan\nPayroll Entry\nEmployee Advance\nExchange Rate Revaluation\nInvoice Discounting\nFees\nFull and Final Statement\nPayment Entry\nBank Transaction\nLanded Cost Voucher\nProject Costing\nCost Allocation Run"
}
```

**Migration order trap:** Property Setter MUST exist BEFORE first JE row references `Project Costing` / `Cost Allocation Run`. Patch in `patches.txt` runs BEFORE first seed → safe.

---

## 5. VN Accounting Settings — 4 fields mới

Section mới `project_costing_section` trong existing `VN Accounting Settings`:

```json
{
  "fieldname": "project_costing_section",
  "fieldtype": "Section Break",
  "label": "Giá thành công trình",
  "collapsible": 1
},
{
  "fieldname": "wip_account_project_costing",
  "fieldtype": "Link",
  "options": "Account",
  "label": "Tài khoản tập hợp chi phí công trình (WIP)",
  "description": "Mặc định 154 — Chi phí SXKD dở dang. Áp dụng cho Stock Entry / DN / PI / Expense Claim / Timesheet khi tag công trình."
},
{
  "fieldname": "overhead_collector_account",
  "fieldtype": "Link",
  "options": "Account",
  "label": "Tài khoản gom chi phí gián tiếp (Overhead)",
  "description": "Mặc định 627 — Chi phí sản xuất chung. Áp dụng cho chứng từ cost_type = Phân bổ trước Allocation Run."
},
{
  "fieldname": "column_break_project_costing_1",
  "fieldtype": "Column Break"
},
{
  "fieldname": "cogs_account_project_costing",
  "fieldtype": "Link",
  "options": "Account",
  "label": "Tài khoản giá vốn công trình (COGS)",
  "description": "Mặc định 632 — Giá vốn hàng bán. Recognize khi Stage SI submit."
},
{
  "fieldname": "writeoff_account_project_costing",
  "fieldtype": "Link",
  "options": "Account",
  "label": "Tài khoản write-off khi đóng công trình",
  "description": "Mặc định 642 — Chi phí QLDN. KTT có thể chọn 632 nếu là giá vốn không phân bổ."
}
```

Seed defaults trong `setup/company_defaults.py` (hook `Company.on_update`): after company creation + VN COA loaded, auto-fill 4 fields by `account_number` LIKE `"154 - %"`, `"627 - %"`, `"632 - %"`, `"642 - %"` (per `_settings_default_inventory_account` pattern in lcv_hooks.py). Tất cả idempotent — chỉ set khi field còn trống.

---

## 6. Hooks (doc_events) + GL engines

### 6.1 hooks.py thay đổi

Thêm vào existing `doc_events`:

```python
doc_events = {
    # ... existing ...
    "Stock Entry": {
        "on_submit": "vn_accounting.project_costing.services.wip_override_engine.on_stock_entry_submit",
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_stock_entry_cancel",
    },
    "Delivery Note": {
        "on_submit": "vn_accounting.project_costing.services.wip_override_engine.on_delivery_note_submit",
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_delivery_note_cancel",
    },
    "Purchase Invoice": {
        # ... existing entries (autofill, asset hooks) ...
        "on_submit": [
            "vn_accounting.asset.pi_hooks.on_purchase_invoice_submit",
            "vn_accounting.project_costing.services.wip_override_engine.on_purchase_invoice_submit",
        ],
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_purchase_invoice_cancel",
    },
    "Expense Claim": {
        "on_submit": "vn_accounting.project_costing.services.wip_override_engine.on_expense_claim_submit",
        "on_cancel": "vn_accounting.project_costing.services.wip_override_engine.on_expense_claim_cancel",
    },
    "Sales Invoice": {
        "on_submit": "vn_accounting.project_costing.services.cogs_engine.on_sales_invoice_submit",
        "on_cancel": "vn_accounting.project_costing.services.cogs_engine.on_sales_invoice_cancel",
    },
}
```

`app_include_js` thêm 1 entry: `"project_costing_jes_section.bundle.js"`.

`fixtures` thêm 1 entry cho Property Setter Journal Entry Account-reference_type (`module = VN Accounting`).

**KHÔNG đăng ký `permission_query_conditions`** cho 3 DocType mới ở Phase 1 (xem §13). Admin từng site cấu hình permission qua Role Permission Manager UI. Per-project ACL = Phase 2 deferral D5.

### 6.2 wip_override_engine.py

**Signature pattern (mỗi DocType có 2 funcs `on_<dt>_submit` + `on_<dt>_cancel`):**

```python
import frappe
from frappe.utils import flt

_MARKER_PREFIX = "PROJECT_COSTING"
_TYPE_WIP_OVERRIDE = "WIP_OVERRIDE"

def _marker(source_doctype: str, source_name: str) -> str:
    return f"[{_MARKER_PREFIX}:{source_name}][TYPE:{_TYPE_WIP_OVERRIDE}][SRC:{source_doctype}]"


def on_purchase_invoice_submit(doc, method=None):
    """For each PI Item row with project + wip_override_account → JE bù."""
    if doc.docstatus != 1:
        return
    overrides = _collect_pi_overrides(doc)
    if not overrides:
        return
    _post_wip_override_je(
        company=doc.company,
        posting_date=doc.posting_date,
        source_dt="Purchase Invoice",
        source_name=doc.name,
        overrides=overrides,
    )


def _collect_pi_overrides(doc) -> list[dict]:
    """Returns list of {project, project_costing_stage, amount, override_account, default_account}."""
    settings_default = _get_settings_wip_account(doc.company)
    out = []
    for item in (doc.items or []):
        if not item.project or not item.get("wip_override_account"):
            continue
        override = item.wip_override_account
        if override == settings_default:
            continue   # no-op
        out.append({
            "project": item.project,
            "project_costing_stage": item.get("project_costing_stage"),
            "amount": flt(item.amount),
            "override_account": override,
            "default_account": settings_default,
            "source_row": item.name,
        })
    return out


def _post_wip_override_je(*, company, posting_date, source_dt, source_name, overrides):
    """Build idempotent JE bù: Dr <override> / Cr <default> per override row.

    Aggregates by (default_account, override_account) pair before posting.
    Skips if existing JE found via marker (idempotent re-submit safety).
    """
    if _find_existing_je(source_name):
        return  # idempotent
    # Aggregate
    by_pair = {}
    for o in overrides:
        key = (o["default_account"], o["override_account"], o["project"])
        by_pair[key] = by_pair.get(key, 0) + o["amount"]
    if not by_pair:
        return

    je = frappe.new_doc("Journal Entry")
    je.posting_date = posting_date
    je.company = company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{_marker(source_dt, source_name)} "
        + frappe._("Bù tài khoản WIP công trình từ {0} {1}").format(source_dt, source_name)
    )
    for (default_acc, override_acc, project), amt in by_pair.items():
        je.append("accounts", {
            "account": override_acc,
            "debit_in_account_currency": amt,
            "project": project,
            "reference_type": "Project Costing",
            "reference_name": project,
            "user_remark": frappe._("Tập hợp chi phí công trình {0}").format(project),
        })
        je.append("accounts", {
            "account": default_acc,
            "credit_in_account_currency": amt,
            "reference_type": "Project Costing",
            "reference_name": project,
            "user_remark": frappe._("Đảo TK mặc định").format(),
        })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()


def _find_existing_je(source_name: str, include_cancelled=False) -> str | None:
    marker = f"[{_MARKER_PREFIX}:{source_name}][TYPE:{_TYPE_WIP_OVERRIDE}]"
    filters = {"user_remark": ["like", f"%{marker}%"]}
    if not include_cancelled:
        filters["docstatus"] = 1
    return frappe.db.get_value("Journal Entry", filters, "name")


def on_purchase_invoice_cancel(doc, method=None):
    je_name = _find_existing_je(doc.name)
    if not je_name:
        return
    je = frappe.get_doc("Journal Entry", je_name)
    if je.docstatus == 1:
        je.flags.ignore_permissions = True
        je.cancel()
```

Same pattern for `on_stock_entry_*`, `on_delivery_note_*`, `on_expense_claim_*` — chỉ khác `_collect_<dt>_overrides` shape (row vs main doc; child table vs flat field).

### 6.3 cogs_engine.py

```python
_TYPE_STAGE_COGS = "STAGE_COGS"

def on_sales_invoice_submit(doc, method=None):
    """Recognize COGS Dr 632 / Cr 154 cho stage liên kết.

    Trigger: SI có project_costing_stage (Custom Field on Sales Invoice).
    """
    if doc.docstatus != 1:
        return
    stage_name = doc.get("project_costing_stage")
    if not stage_name:
        return
    stage = frappe.get_doc("Project Costing Stage", stage_name)
    cost = flt(stage.cost_pinned)
    if cost <= 0:
        return  # EC2 — stage cost = 0 không sinh JE
    parent = stage.parent_costing
    settings = _load_settings(doc.company)
    je = _build_cogs_je(
        company=doc.company,
        posting_date=doc.posting_date,
        si_name=doc.name,
        stage_name=stage_name,
        parent_costing=parent,
        project=doc.project,
        amount=cost,
        cogs_account=settings.cogs_account_project_costing,
        wip_account=settings.wip_account_project_costing,
    )
    je.insert(ignore_permissions=True)
    je.submit()
    # Update stage with COGS JE link
    frappe.db.set_value("Project Costing Stage", stage_name,
                       {"cogs_je": je.name, "status": "Đã xuất HĐ"},
                       update_modified=False)
```

`_build_cogs_je` follows LCV pattern: `user_remark` marker `[PROJECT_COSTING:<parent>][TYPE:STAGE_COGS][SI:<si>]`, accounts list, each row carrying `reference_type="Project Costing"`, `reference_name=parent`, `project=<project>`.

`on_sales_invoice_cancel`: find JE by marker → cancel → reset stage status to `Chờ xuất HĐ`, clear `cogs_je`.

### 6.4 allocation_engine.py

```python
_TYPE_ALLOCATION = "ALLOCATION_RUN"

def post_allocation_je(car_doc):
    """Cost Allocation Run on_submit: Dr 154 (per project) / Cr 627."""
    company = car_doc.company
    settings = _load_settings(company)
    by_share = {}
    for share in car_doc.shares:
        wip_acc = share.wip_account or settings.wip_account_project_costing
        amount = flt(share.amount)
        if amount <= 0:
            continue
        key = (wip_acc, share.project)
        by_share[key] = by_share.get(key, 0) + amount

    cr_total = flt(car_doc.total_amount)
    if not by_share or cr_total <= 0:
        return

    je = frappe.new_doc("Journal Entry")
    je.posting_date = car_doc.posting_date
    je.company = company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"[{_MARKER_PREFIX}:{car_doc.name}][TYPE:{_TYPE_ALLOCATION}] "
        + frappe._("Phân bổ chi phí gián tiếp kỳ {0} → {1}").format(
            car_doc.run_period_start, car_doc.run_period_end)
    )
    for (wip_acc, project), amt in by_share.items():
        je.append("accounts", {
            "account": wip_acc,
            "debit_in_account_currency": amt,
            "project": project,
            "reference_type": "Cost Allocation Run",
            "reference_name": car_doc.name,
            "user_remark": frappe._("Phân bổ vào công trình {0}").format(project),
        })
    je.append("accounts", {
        "account": settings.overhead_collector_account,
        "credit_in_account_currency": cr_total,
        "reference_type": "Cost Allocation Run",
        "reference_name": car_doc.name,
        "user_remark": frappe._("Đảo TK gom chi phí gián tiếp").format(),
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()
    frappe.db.set_value("Cost Allocation Run", car_doc.name,
                       {"generated_je": je.name, "status": "Đã phân bổ"},
                       update_modified=False)
```

`cancel_allocation_je`: find via `generated_je` field (already linked) → cancel JE → status `Đã hủy`. Validate `_validate_target_projects_not_invoiced`: for each share, check no stage of that project has submitted SI within `[run_period_start, run_period_end]` — if any, throw with project list (R10.5).

### 6.5 close_engine.py

```python
_TYPE_CLOSE = "CLOSE_WRITEOFF"

@frappe.whitelist()
def close_project(costing_doc, writeoff_account=None, writeoff_amount=0, force=False):
    """Close Project Costing.

    Steps:
      1. Validate all stages have SI submitted OR are 'Đã hủy'.
      2. Compute remaining 154 balance for project.
      3. If balance == 0 → just flip status to "Đã hoàn thành", set closed_on.
      4. If balance > 0 → require writeoff_account + post Dr <writeoff> / Cr 154.
         Default writeoff_account = Settings.writeoff_account_project_costing.
    """
    _validate_all_stages_resolved(costing_doc.name)
    balance = _compute_wip_balance(costing_doc.project, costing_doc.company)
    if abs(balance) < 0.01:
        # Clean close
        frappe.db.set_value("Project Costing", costing_doc.name,
            {"status": "Đã hoàn thành", "closed_on": today()},
            update_modified=False)
        return {"balance": 0, "writeoff_je": None}

    if balance > 0 and not force:
        return {"balance": balance, "needs_decision": True}

    # Build write-off JE
    settings = _load_settings(costing_doc.company)
    wo_acc = writeoff_account or settings.writeoff_account_project_costing
    wip_acc = settings.wip_account_project_costing

    je = frappe.new_doc("Journal Entry")
    je.posting_date = today()
    je.company = costing_doc.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"[{_MARKER_PREFIX}:{costing_doc.name}][TYPE:{_TYPE_CLOSE}] "
        + frappe._("Write-off khi đóng công trình {0}").format(costing_doc.project)
    )
    je.append("accounts", {
        "account": wo_acc,
        "debit_in_account_currency": flt(balance),
        "project": costing_doc.project,
        "reference_type": "Project Costing",
        "reference_name": costing_doc.name,
    })
    je.append("accounts", {
        "account": wip_acc,
        "credit_in_account_currency": flt(balance),
        "project": costing_doc.project,
        "reference_type": "Project Costing",
        "reference_name": costing_doc.name,
    })
    je.flags.ignore_permissions = True
    je.insert()
    je.submit()
    frappe.db.set_value("Project Costing", costing_doc.name,
        {"status": "Đã hoàn thành", "closed_on": today(), "writeoff_je": je.name},
        update_modified=False)
    return {"balance": balance, "writeoff_je": je.name}


def _compute_wip_balance(project: str, company: str) -> float:
    """Return Dr - Cr on WIP account for this project. > 0 = cost còn dư."""
    settings = _load_settings(company)
    rows = frappe.db.sql("""
        SELECT IFNULL(SUM(debit),0) - IFNULL(SUM(credit),0) AS bal
        FROM `tabGL Entry`
        WHERE account=%s AND project=%s AND company=%s AND is_cancelled=0
    """, (settings.wip_account_project_costing, project, company), as_dict=1)
    return flt(rows[0]["bal"]) if rows else 0
```

### 6.6 markup_calc.py — pure functions

```python
def calculate_price(*, method: str, markup_value: float, cost_pinned: float,
                    parent_costing: str | None = None) -> float:
    """6 markup methods. Returns suggested price; None on bad inputs."""
    cost = flt(cost_pinned)
    mv = flt(markup_value)

    if method == "coefficient":
        return cost * mv  # mv = hệ số (vd 1.5)
    if method == "percent_cost":
        return cost * (1 + mv / 100.0)  # mv = % (vd 30 → +30%)
    if method == "fixed_amount":
        return mv
    if method in ("from_contract", "percent_contract"):
        return _resolve_contract_price(method, mv, parent_costing)
    if method == "cost_to_date_uplift":
        return cost * (1 + mv / 100.0)
    return 0


def _resolve_contract_price(method, mv, parent_costing):
    """For from_contract / percent_contract — read contract value from Project Costing.contract → DCNET Contract."""
    if not parent_costing:
        return 0
    contract = frappe.db.get_value("Project Costing", parent_costing, "contract")
    if not contract:
        return 0
    contract_value = flt(frappe.db.get_value("DCNET Contract", contract, "total_value"))
    if method == "from_contract":
        return mv  # KTT input directly
    return contract_value * (mv / 100.0)
```

> **Pure function rule:** No frappe.throw inside `calculate_price`. Bad method → return 0. Validation lives in Stage controller (`validate()`).

---

## 7. Whitelisted API endpoints

`pivot_service.py` — 4 endpoints cho Pivot Tool page:

### 7.1 `get_pivot_data(costing_name: str) -> dict`

Returns:
```json
{
  "costing": {"name": "...", "project": "...", "customer": "...", "status": "..."},
  "stages": [
    {"name": "...", "stage_name": "...", "stage_order": 1, "status": "...",
     "markup_method": "...", "markup_value": ..., "cost_pinned": ...,
     "price_suggested": ..., "price_override": ..., "sales_invoice": ...}
  ],
  "common_pool": [
    {"source_dt": "Purchase Invoice", "source_name": "...", "source_row": "...",
     "amount": ..., "posting_date": "...", "description": "..."},
    ...
  ],
  "pinned": {
    "<stage_name>": [{"source_dt": ..., "source_name": ..., "amount": ...}, ...]
  },
  "settings": {"wip": "...", "overhead": "...", "cogs": "...", "writeoff": "..."}
}
```

Logic:
- `common_pool` = SELECT all chứng từ với `project=<X>` + `project_costing_stage IS NULL` + cost_type='Trực tiếp'.
- `pinned` = SELECT chứng từ với `project_costing_stage` ∈ stage list của project.

### 7.2 `pin_cost_to_stage(source_doctype, source_name, source_row, stage_name, split_amount=None) -> dict`

Updates `project_costing_stage` field on chứng từ row. For child rows (PI Item / SI Item / etc.), updates the child row, not the parent doc.

Split logic:
- If `split_amount` provided AND ≠ row total → reject in Phase 1 (R4.2 requires complete split, but split UI is Phase 2 — simpler implementation: 1 chứng từ row = 1 stage atomic).
- If pin same row to ≥2 stages → reject with R3.6 warning message.

Returns updated stage `cost_pinned` + new `price_suggested` (re-computed).

### 7.3 `recalculate_stage_price(stage_name) -> dict`

Trigger recompute of `price_suggested` after KTT changes markup_method / markup_value / cost moves in. Returns new value.

### 7.4 `generate_stage_si(stage_name) -> dict`

Creates SI draft:
- 1 item line "[project_name] — [stage_name]"
- amount = `price_override` if set, else `price_suggested`
- customer = parent Project Costing.customer
- Custom Field SI.project_costing_stage = stage_name
- docstatus = 0 (draft)
- KTT then opens SI, reviews, submits → triggers cogs_engine.

Returns `{"sales_invoice": "SINV-...", "url": "/app/sales-invoice/SINV-..."}`.

### 7.5 `je_trace.py` — embedded section

`get_project_costing_jes(costing_name: str) -> dict`

Returns:
```json
{
  "groups": [
    {
      "type": "ALLOCATION_RUN",
      "label": "Phân bổ chi phí gián tiếp",
      "rows": [{"je_name": "...", "posting_date": "...", "amount": ..., "ref": "CAR-...", "label": "..."}],
      "total": ...
    },
    {"type": "WIP_OVERRIDE", "label": "Bù tài khoản WIP", "rows": [...], "total": ...},
    {"type": "STAGE_COGS", "label": "Giá vốn theo stage", "rows": [...], "total": ...},
    {"type": "CLOSE_WRITEOFF", "label": "Write-off đóng project", "rows": [...], "total": ...}
  ],
  "wip_balance": ...
}
```

SQL: WHERE `user_remark LIKE '[PROJECT_COSTING:<costing>]%' AND docstatus=1`, GROUP BY type marker `[TYPE:<X>]` parse.

---

## 8. Pivot Tool Page (React SPA)

### 8.1 Page registration

`page/project_costing_pivot/project_costing_pivot.json`:

```json
{
  "doctype": "Page",
  "name": "project-costing-pivot",
  "module": "VN Accounting",
  "title": "Pivot Tool — Tính giá thành",
  "standard": "Yes",
  "roles": [
    {"role": "Project Manager"},
    {"role": "Accounts Manager"}
  ]
}
```

`page/project_costing_pivot/project_costing_pivot.py` — empty handler shim:

```python
import frappe
def get_context(context):
    pass
```

### 8.2 React bundle

`public/js/project_costing_pivot.bundle.jsx`:
- Entry: `window.AppMount = { mount: (container, props) => ReactDOM.render(<PivotApp {...props}/>, container) }`
- esbuild → IIFE.
- Route param: `?costing=<name>`, default to first active Project Costing if absent.

Page handler in JSON-shipped Page (Frappe v16):

```js
// page_js (loaded by page.py as eval'd ES5 — DO NOT use import here)
frappe.pages["project-costing-pivot"].on_page_load = function (wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: __("Tính giá thành công trình"),
    single_column: true,
  });
  const params = new URLSearchParams(window.location.search);
  const costing = params.get("costing");
  if (window.AppMount && window.AppMount.mount) {
    window.AppMount.mount(page.body[0], { costing });
  } else {
    page.body.html(`<div class="text-muted">${__("Đang tải Pivot Tool...")}</div>`);
  }
};
```

(`app_include_js` loads bundle BEFORE page handler → AppMount available at page load.)

### 8.3 UI layout (React component tree)

```
PivotApp
├── Header (Project Costing summary: project name, customer, status, total cost, total stages)
├── StageColumns (horizontal scroll if >4 stages)
│   ├── StageColumn × N
│   │   ├── StageHeader (name, status, markup chip)
│   │   ├── MarkupConfigCard (method dropdown + value input + override input + reason textarea)
│   │   ├── PriceDisplay (suggested / override / diff)
│   │   ├── PinnedCostsList (drag target — bordered area)
│   │   └── ActionBar (recalc / generate SI buttons)
│   └── CommonPoolColumn (rightmost)
│       ├── Header "Common pool (chưa pin)"
│       └── DraggableCostList
└── BalanceFooter (sum of stages vs sum of pinned + common = total)
```

### 8.4 Interaction patterns

| User action | API call | UI update |
|---|---|---|
| Drag cost row from common pool → stage column | `pin_cost_to_stage(source_doctype, source_name, source_row, stage_name)` | optimistic move; revert on error |
| Drag cost row from stage A → stage B | same API (different stage_name) | check stage A not SI-submitted; revert if locked |
| Change markup_method/value/override on stage card | direct save via `frappe.db.set_value` on Project Costing Stage + `recalculate_stage_price` | refetch stage row, update price displays |
| Click "Tạo HĐ draft" on stage | `generate_stage_si(stage_name)` | open new tab to SI form |
| Click "Cảnh báo pin nhiều stage" dialog | client-side check before API call | block + show R3.6 dialog |

### 8.5 Form vs Pivot Tool divergence rule

**Pivot Tool is the ONLY place to modify cost ↔ stage mapping (R4.1).** From PI/SE/DN/EC forms, `project_costing_stage` Custom Field is **read-only after first save** to prevent two-path mutations.

Implementation: client script on each form sets `frm.set_df_property("project_costing_stage", "read_only", 1)` when `frm.doc.docstatus >= 0 && !frm.is_new()`.

---

## 9. Embedded "Bút toán liên quan" section

Pattern y hệt FB-00834 deferred schedule trên PI form. File: `public/js/project_costing_jes_section.bundle.js`.

```js
frappe.ui.form.on("Project Costing", {
  refresh: function (frm) {
    if (frm.is_new()) return;
    render_jes_section(frm);
  },
});

function render_jes_section(frm) {
  // Remove any prior render (idempotent)
  $(frm.layout.wrapper).find(".vn-pc-jes-section").remove();

  // Generation token guard
  frm.__vn_pc_jes_gen = (frm.__vn_pc_jes_gen || 0) + 1;
  const my_gen = frm.__vn_pc_jes_gen;
  const my_doc = frm.doc.name;

  frappe.call({
    method: "vn_accounting.project_costing.services.je_trace.get_project_costing_jes",
    args: { costing_name: frm.doc.name },
    callback: function (r) {
      if (my_gen !== frm.__vn_pc_jes_gen) return;  // stale
      if (frm.doc.name !== my_doc) return;  // navigated away
      const data = r.message || { groups: [], wip_balance: 0 };
      const $details = $(frm.layout.wrapper).find(".tab-pane").first();
      $details.find(".vn-pc-jes-section").remove();
      $details.append(build_section_html(data));
    },
  });
}

function build_section_html(data) {
  // Returns HTML string: 4 collapsible sub-sections (ALLOCATION_RUN /
  // WIP_OVERRIDE / STAGE_COGS / CLOSE_WRITEOFF), each with rows + total,
  // plus footer "Số dư TK 154 hiện tại".
  // Wrapper class form-section + section-head + custom vn-pc-jes-section.
  // ...
}
```

Inject point: `$(frm.layout.wrapper).find(".tab-pane").first().append(...)` — Chi tiết tab (NOT Connections — per frappe-v16-ui.md `frm.dashboard.add_section()` trap).

---

## 10. Reports

### 10.1 Project Cost Collection — Bảng tập hợp chi phí công trình

Path: `report/project_cost_collection/`. Type: Script Report.

**Filters (`project_cost_collection.js`):**

| Filter | Type | reqd | options |
|---|---|---|---|
| company | Link | 1 | Company |
| project | Link | 0 | Project (multi-select) |
| stage | Link | 0 | Project Costing Stage (filtered by project) |
| cost_type | Select | 0 | `\nTrực tiếp\nPhân bổ` |
| from_date | Date | 1 | default = fiscal year start |
| to_date | Date | 1 | default = today |

**Columns:**

| Field | Label | Width | Format |
|---|---|---|---|
| project | Công trình | 150 | Link → Project |
| stage_name | Giai đoạn | 120 | - |
| cost_type | Loại CP | 80 | (with VN icon ✅/⚠️) |
| source_doctype | Loại chứng từ | 120 | - |
| source_name | Chứng từ | 140 | Link → dynamic |
| posting_date | Ngày | 100 | Date |
| description | Diễn giải | 200 | - |
| amount | Số tiền | 130 | Currency |
| markup_method | Markup | 100 | - |
| stage_status | TT giai đoạn | 100 | - |

**Total row:** `add_total_row=0`, manual emit with `amount` sum only.

`execute(filters)`:
- UNION across PI Item / SE / DN Item / EC / Timesheet Detail (per BL R3.3) joined với Project Costing Stage để derive stage_name/status.
- Filter by company, date range, optional project/stage/cost_type.

### 10.2 Project Invoicing Progress — Bảng tiến độ xuất HĐ

Columns: project, stage_name, expected_invoice_date, status, days_to_due (computed: expected - today), price_override, sales_invoice.

Filter: company, project, status, due within N days.

Default sort: days_to_due ascending (overdue first).

`get_indicator(row)`:
- Red: days_to_due < 0 AND status NOT IN ('Đã xuất HĐ', 'Đã thu tiền')
- Yellow: days_to_due ≤ 7 AND status = 'Chờ xuất HĐ'
- Green: status IN ('Đã xuất HĐ', 'Đã thu tiền')
- Gray: default

### 10.3 Project P&L Detailed — Bảng lãi/lỗ chi tiết

Tận dụng `Project Profitability` core report, không monkey-patch. Tạo Script Report mới riêng:

| Field | Label | Format |
|---|---|---|
| project | Công trình | Link |
| revenue | Doanh thu | Currency |
| direct_cost | CP trực tiếp | Currency |
| allocated_cost | CP phân bổ | Currency |
| total_cost | Tổng CP | Currency (= direct + allocated) |
| gross_profit | Lãi gộp | Currency (= revenue - direct) |
| net_profit | Lãi ròng | Currency (= revenue - total) |
| common_pool | Common pool (chưa pin) | Currency |

SQL: GROUP BY project, derive direct_cost from GL Entry WHERE account=154 AND project=X AND voucher_type≠'Cost Allocation Run', allocated_cost FROM `tabJournal Entry` WHERE reference_type='Cost Allocation Run' grouped by project, revenue FROM Sales Invoice submitted.

`add_total_row=1` for revenue/cost/profit cols. Hide gross/net profit on total row (since project mixing average loses meaning) — set `None` manually.

---

## 11. Workspace sidebar items

Modify `workspace_sidebar/vn_accounting.json` — insert items vào "Giá thành" section.

**Phase 1 ships 2 items** (DocType lists chỉ — Report `Project Cost Collection` chưa tồn tại Phase 1, ship Phase 4):
- Công trình & giá thành → Project Costing
- Đợt phân bổ chi phí gián tiếp → Cost Allocation Run (với `route_options={"docstatus":["=",1]}`)

Phase 4 sẽ thêm 3rd item:

Insert AFTER idx 91 (after "Cấu hình phân bổ chi phí mua hàng"), pushing subsequent items down by 3:

```json
{
  "type": "Link",
  "label": "Công trình & giá thành",
  "link_type": "DocType",
  "link_to": "Project Costing"
},
{
  "type": "Link",
  "label": "Đợt phân bổ chi phí gián tiếp",
  "link_type": "DocType",
  "link_to": "Cost Allocation Run",
  "route_options": "{\"docstatus\":[\"=\",1]}"
},
{
  "type": "Link",
  "label": "Bảng tập hợp chi phí công trình",
  "link_type": "Report",
  "link_to": "Project Cost Collection"
}
```

> **JSON edit must use `ensure_ascii=True`** (per programming.md / git-deploy.md) — otherwise 290-line diff. Use bench-side python script + `bench migrate` to apply, NOT manual editor.

Insert in `after_migrate` via `_sync_workspace_sidebar()` similar pattern to FB-00834 deferred section.

---

## 12. Translations

`translations/vi.csv` thêm ~35 strings. Format 2-cột (source,target), CRLF line endings (per `vn_translation` lesson):

| Source | Target |
|---|---|
| Project Costing | Giá thành công trình |
| Project Costing Stage | Giai đoạn công trình |
| Cost Allocation Run | Đợt phân bổ chi phí |
| Cost Allocation Share | Phân bổ cho công trình |
| Cost Allocation Source | Chứng từ nguồn |
| Project | Công trình (CONTEXT-dependent — verify không xung đột với "Dự án" trong vn_translation) |
| Stage | Giai đoạn |
| Stage Order | Thứ tự giai đoạn |
| Markup Method | Phương pháp markup |
| Markup Value | Giá trị markup |
| Coefficient | Hệ số |
| Percent on Cost | % trên chi phí |
| Fixed Amount | Số tiền cố định |
| From Contract | Theo HĐ / phụ lục |
| Percent of Contract | % trên HĐ khung |
| Cost-to-Date Uplift | % trên cost + uplift |
| Suggested Price | Giá đề xuất |
| Override Price | Giá KTT chốt |
| Override Reason | Lý do override |
| Cost Pinned | Chi phí đã pin |
| Common Pool | Common pool (chưa pin) |
| Pivot Tool | Pivot Tool — gán chi phí vào giai đoạn |
| Pin Cost to Stage | Gán chi phí vào giai đoạn |
| Direct Cost | Chi phí trực tiếp |
| Allocated Cost | Chi phí phân bổ |
| Gross Profit | Lãi gộp |
| Net Profit | Lãi ròng |
| WIP Account | Tài khoản tập hợp chi phí |
| Overhead Account | Tài khoản gom chi phí gián tiếp |
| Close Project | Đóng công trình |
| Reopen Project | Mở lại công trình |
| Write-off | Write-off |
| Run Period | Kỳ phân bổ |
| Allocate Equally | Chia đều |
| Manual Allocation | Phân bổ thủ công |

> **CRITICAL:** verify từng key chưa exist trong `vn_translation/translations/vi.csv` trước khi add — nếu conflict, mod vn_translation PR riêng.

---

## 13. Permissions — Native Frappe Role Permission Manager (KHÔNG hardcode)

**Quyết định (Long 2026-05-15):** KHÔNG ship permission matrix trong DocType JSON / fixtures. Để admin từng site tự cấu hình qua **Role Permission Manager UI** native của Frappe (`/app/permission-manager`).

### 13.1 DocType JSON `permissions` — minimal default only

Mỗi DocType mới (Project Costing, Project Costing Stage, Cost Allocation Run, Cost Allocation Share, Cost Allocation Source) ship 1 row duy nhất trong `permissions` array của JSON:

```json
"permissions": [
  {
    "role": "System Manager",
    "read": 1, "write": 1, "create": 1,
    "delete": 1, "submit": 1, "cancel": 1, "amend": 1,
    "report": 1, "export": 1, "import": 1, "share": 1, "print": 1, "email": 1
  }
]
```

Lý do: System Manager luôn cần full access cho bootstrap + troubleshooting. Mọi role khác (Accounts Manager / Project Manager / Sales Manager / Accounts User) → KTT trên site tự thêm qua Role Permission Manager.

### 13.2 KHÔNG ship Custom DocPerm fixtures

- KHÔNG tạo `fixtures/custom_docperm.json`.
- KHÔNG dùng install hook để insert Custom DocPerm rows.

Cảnh báo rule `frappe-doctype-perms.md`: "ANY Custom DocPerm row silently revokes ALL Standard DocPerm". Vì vậy bỏ Custom DocPerm hoàn toàn → Standard DocPerm trong JSON là source of truth → admin override qua UI.

### 13.3 KHÔNG ship `permission_query_conditions` cho Phase 1

Trong `hooks.py` Phase 1 KHÔNG đăng ký `permission_query_conditions` cho 3 DocType mới. Phase 2 có thể thêm nếu cần per-project ACL (vd: PM chỉ thấy project mình assigned), nhưng Phase 1 giữ flat — mọi user có role read sẽ thấy mọi record cùng company (default Frappe behavior).

### 13.4 SI submit & 2-tier approval

Sales Invoice submit controlled hoàn toàn bởi ERPNext core (Accounts Manager + Sales Manager submit by default). Tool này KHÔNG override permission của SI.

2-tier "Hóa đơn > X tr cần GĐ duyệt trước KTT submit" (BL §6.6 R6.6 optional) — Phase 2. Phase 1 không implement; KTT/GĐ đều submit được mặc định.

### 13.5 Tài liệu hướng dẫn cấu hình (Phase 7 vn_help)

Bài help `cong-trinh-tinh-gia-thanh.md` sẽ có section "Cấu hình quyền" hướng dẫn KTT mở Role Permission Manager + add Accounts Manager / Project Manager / Sales Manager với perm phù hợp role mapping ở BL §9.

Mapping suggest (chỉ hướng dẫn, KHÔNG enforced):

| Vai trò DCNET | Frappe stock role suggest | Project Costing | Stage | Allocation Run |
|---|---|---|---|---|
| KTT | Accounts Manager | R/W/C/Delete | R/W/C/Delete | R/W/C/Submit/Cancel |
| PM | Projects Manager (hoặc Project User) | R/W/C | R/W/C | R/W/C |
| GĐ | Sales Manager | R | R | R |
| KTV | Accounts User | R | R | R |
| Thi công / Văn phòng | Employee (default) | — | — | — |

Site admin có thể chọn role mapping khác (vd: dùng custom role "Site KTT" thay Accounts Manager) tùy nhu cầu.

---

## 14. Demo data scenarios

`dcnet_sample/dcnet_sample/data/project_costing_demo.py` — paired setup/teardown.

### 14.1 Customer/Project setup (idempotent — check exists)

Sử dụng existing demo customers (Agribank, CMC, etc.) nếu có. Tạo mới nếu không.

### 14.2 Three project scenarios

**Project A — Kéo cable Agribank Đà Nẵng**
- Type: HĐ khung (linked to existing DCNET Contract)
- Customer: Agribank (existing) hoặc seed mới
- 3 stages:
  - S01 "Tạm ứng 30%": method=`percent_contract`, markup_value=30, contract value=300tr → price=90tr
  - S02 "Thi công + nghiệm thu giữa": method=`cost_to_date_uplift`, markup_value=25 (uplift +25%) → price tùy cost_pinned
  - S03 "Nghiệm thu cuối": method=`from_contract`, markup_value=120000000 (số dư = HĐ - tạm ứng - giữa)
- Costs to pin:
  - PI cable 50m × 200K = 10tr (Trực tiếp, S02)
  - SE switches × 5 = 25tr (Trực tiếp, S02)
  - Timesheet 80h × 200K = 16tr (Trực tiếp, S02)
  - PI thầu phụ kéo 15tr (Trực tiếp, S03)
- Status: S01 đã SI submitted (cost 0 → EC2), S02 đã SI submitted, S03 chờ xuất HĐ.

**Project B — Build IDC CMC Hà Nội**
- Type: stand-alone (không HĐ khung)
- Customer: CMC Telecom
- 4 stages:
  - S01 "Tạm ứng 30%": method=`fixed_amount`, markup_value=150tr → price=150tr
  - S02 "Thi công": method=`percent_cost`, markup_value=40 → price tùy cost_pinned (+40%)
  - S03 "Nghiệm thu": method=`fixed_amount`, markup_value=200tr
  - S04 "Bảo hành 1 năm": method=`fixed_amount`, markup_value=20tr
- Costs (high volume):
  - PI tủ rack 8 × 30tr = 240tr (S02)
  - SE cable + switch + UPS = 80tr (S02)
  - PI thầu lắp đặt 50tr (S02)
  - Timesheet 300h × 250K = 75tr (S02)
- Status: S01 submitted, S02 submitted có write-off (cost > price ⇒ S02 lỗ ~30tr), S03 chờ, S04 dự kiến.

**Project C — Camera shop ABC**
- Type: stand-alone, simple happy path
- Customer: Cửa hàng ABC (seed mới nếu cần)
- 1 stage:
  - S01 "Trọn gói": method=`coefficient`, markup_value=1.6 → price = cost × 1.6
- Costs:
  - PI camera × 4 = 8tr (S01)
  - SE cable + DVR = 5tr (S01)
- Status: S01 submitted, project closed clean (balance = 0).

### 14.3 Allocation Run

**CAR-2026-05-0001** — Cuối tháng 5/2026:
- Source costs (cost_type=Phân bổ):
  - SS Lương PM Tuấn 25tr (Salary Slip seeded với 50% allocated to project work)
  - PI văn phòng phẩm 8tr
  - EC bảo dưỡng xe công ty 3tr
- Method: Đều (equally distributed)
- Shares: Project A + B + C → 12tr / 12tr / 12tr (total 36tr)
- Status: Đã phân bổ → JE generated (Dr 154-A 12tr, Dr 154-B 12tr, Dr 154-C 12tr, Cr 627 36tr).

### 14.4 Markers + idempotency

All demo docs carry `user_remark` marker `[DEMO:project_costing]` so teardown picks up via SQL. Teardown reverse order: Project C close → cancel its writeoff JE if any → … → Customer/Contract/Item references stay (shared demo).

CLI: `bench --site dcnet.localhost execute dcnet_sample.data.project_costing_demo.setup_all` and `teardown_all`.

Hook into existing `setup_all()` / `teardown_all()` in dcnet_sample. UI: 2-tier teardown (UI = transactions only; CLI = full).

---

## 15. Test coverage matrix

| Service | Test file | Pure func / Frappe DB | Coverage |
|---|---|---|---|
| markup_calc | test_markup_calc.py | Pure | 6 methods × 3 inputs each + edge (0 cost, contract null, negative markup) = ~24 tests |
| allocation_engine | test_allocation_engine.py | Frappe DB | Equal split / manual %, sum-100% validation, post JE shape, cancel reverses, period-closed reject, target-invoiced reject |
| cogs_engine | test_cogs_engine.py | Frappe DB | SI submit posts JE 632↔154, SI cancel reverses, stage cost=0 → no JE (EC2), stage status flips |
| wip_override_engine | test_wip_override_engine.py | Frappe DB | PI/SE/DN/EC × override → JE bù; same override = default → skip; idempotent re-submit; cancel reverses |
| close_engine | test_close_engine.py | Frappe DB | Balance 0 clean close; balance >0 needs writeoff; force=true posts writeoff JE; reopen path |
| pivot_service | test_pivot_service.py | Frappe DB | get_pivot_data shape, pin moves project_costing_stage, pin to ≥2 stages rejects, generate_stage_si creates draft |

**TDD applicability (per multi-session.md):** `markup_calc` = pure → TDD mandatory. Engines + pivot_service = DocType + DB → write tests after implementation. Tests run via `<bench-root>/env/bin/python -m unittest apps/vn_accounting/vn_accounting/project_costing/tests/test_<module>`.

> **DCNET bench Python:** 3.14 — must use `env/bin/python` (NOT bare `python`) for verification commands.

---

## 16. vn_help articles

Path: `apps/vn_accounting/vn_accounting/help/portal/cong-trinh/`.

Each `.md` follows `reference_vn_help_authoring_standard.md` format (YAML frontmatter + section folder convention). Articles:

| File | Audience | Mapping |
|---|---|---|
| `cong-trinh-tinh-gia-thanh.md` | KTT/PM | `doctype_mapping: [Project Costing]` |
| `stage-markup.md` | KTT/PM | `doctype_mapping: [Project Costing Stage]`, with detailed 6-method table |
| `pivot-tool.md` | KTT/PM | `page: project-costing-pivot` (custom field in frontmatter) |
| `allocation-run.md` | KTT | `doctype_mapping: [Cost Allocation Run]` |
| `close-project.md` | KTT | Action-based, not DocType-bound |

**Terminology binding (per `feedback_help_terminology_vietnamese.md`):**
- "Phiếu mua hàng" thay "Purchase Invoice"
- "Phiếu xuất kho" thay "Stock Entry"
- "Phiếu giao hàng" thay "Delivery Note"
- "Phiếu hoàn ứng" thay "Expense Claim"
- "Bảng chấm công" thay "Timesheet"
- "Hóa đơn bán hàng" thay "Sales Invoice"
- "Bút toán kế toán" thay "Journal Entry"
- KHÔNG dùng "ERPNext" / "Frappe" trong body.

---

## 17. Implementation order (phases)

| Phase | Sessions | Scope | Deliverable |
|---|---|---|---|
| **1** | 1-2 | DocType skeletons (4) + Settings 4 fields + Custom Fields (15) + Property Setter + sidebar 3 items + basic translations | Branch `feature/project-costing-phase-1-skeleton` → PR dcnet-accounting |
| **2** | 2 | GL engines (4 services) + markup_calc pure funcs + tests (TDD for markup, post-hoc for engines) | Branch `feature/project-costing-phase-2-engines` → PR |
| **3** | 2-3 | Pivot Tool Page (React SPA) + 4 server endpoints + embedded JE section | Branch `feature/project-costing-phase-3-pivot` → PR |
| **4** | 1 | 3 Reports + sidebar Report links + translation polish | Branch `feature/project-costing-phase-4-reports` → PR |
| **5** | 1 | Demo data 3 scenarios + Allocation Run + dcnet_sample integration | Branch `feature/project-costing-demo-data` → PR dcnet-sample |
| **6** | 1-2 | Playwright QA + `/design-qa` + fixes | (in-place commits + amend PR if needed) |
| **7** | 1 | vn_help 5 articles + PR tổng kết + FB-00605 marked Resolved | Branch `feature/project-costing-vn-help` → PR |

**Branch strategy:** mỗi phase 1 branch off `dcnet-cloud/develop`, PR riêng. KHÔNG 1 PR khổng lồ. Reviewer dễ + rollback nhanh.

**Per-phase gate:**
- Phase 1 must pass: `python3 -m py_compile` all .py files; `bench migrate` clean on dcnet.localhost; `frappe.get_meta("Project Costing")` returns valid doc.
- Phase 2 must pass: All unit tests green + manual smoke test (submit PI tag project + override → verify JE bù).
- Phase 3 must pass: Pivot Tool loads in browser; drag-drop pins cost; SI draft generation works end-to-end.
- Phase 4 must pass: 3 reports return data; sidebar items navigate correctly.
- Phase 5 must pass: 3 projects + Allocation Run live on dcnet.localhost, all JEs traceable in embedded section.
- Phase 6 must pass: 0 console errors on Pivot Tool + Project Costing form; design QA report with all severity-2+ items fixed.
- Phase 7 must pass: All 5 help articles render in `/help/cong-trinh/...`; FB-00605 status flipped Resolved.

---

## 18. Self-review notes

### 18.1 Spec coverage check (BL → tech mapping)

| BL section | Tech mapping section | Coverage |
|---|---|---|
| §1 Mục đích | §6 GL engines + §10 Reports | ✅ |
| §2 Vòng đời | §2.1 Project Costing.status transitions + §6.5 close_engine | ✅ |
| §3 Quy tắc nhập chi phí | §3 Custom Fields + §8.5 read-only on forms | ✅ |
| §3.5 PI tag pattern | §7.2 `pin_cost_to_stage` reject logic | ✅ |
| §3.6 Warning pin nhiều stage | §8.4 client-side dialog | ✅ |
| §4 Pivot Tool | §8 React SPA + §7 endpoints | ✅ |
| §5 Markup 6 methods | §2.2 Stage fields + §6.6 markup_calc | ✅ |
| §6 Xuất hóa đơn | §7.4 `generate_stage_si` + §6.3 cogs_engine | ✅ |
| §7 Đóng/hủy | §6.5 close_engine | ✅ |
| §8 Báo cáo | §10 (3 reports) | ✅ |
| §9 Phân quyền | §13 DocPerm matrix | ✅ |
| §10 Trực tiếp vs phân bổ | §3.3 cost_type CF + §6.4 allocation_engine | ✅ |
| §10.2 Allocation Run | §2.3 DocType + §6.4 engine | ✅ |
| §10.3 P&L 3 nhóm cột | §10.3 Project P&L Detailed report | ✅ |
| §11 TT99/2025 GL chain | §6.2-§6.5 all engines respect chain 627→154→632 | ✅ |
| §12 Override TK WIP | §3.2 CF + §6.2 wip_override_engine | ✅ |
| §13 JE traceability | §4 Property Setter + §6 marker pattern + §9 embedded section | ✅ |
| §14 Edge cases EC1-EC7 | §15 test matrix | ✅ |
| §15 Settings 4 fields | §5 | ✅ |

### 18.2 Type consistency

- `Project Costing` (parent) ↔ `parent_costing` field on stages — naming aligned.
- `markup_method` Select 6 options consistent across DocType JSON + `markup_calc.py` + translations.
- `cost_type` 2 options `Trực tiếp\nPhân bổ` consistent across CF + Allocation Source child + reports.
- JE marker format `[PROJECT_COSTING:<name>][TYPE:<X>]` consistent in wip_override_engine / cogs_engine / allocation_engine / close_engine.
- `reference_type` Select options Property Setter includes both `Project Costing` AND `Cost Allocation Run` — both consumed in `je_trace.py`.

### 18.3 Edge cases mapping (BL §14 → tech)

| EC | BL ref | Tech impl |
|---|---|---|
| EC1 cancel SI sau COGS | §6.5 R6.5 | `cogs_engine.on_sales_invoice_cancel` reverses + resets stage status |
| EC2 stage cost = 0 | §11.2 | `cogs_engine.on_sales_invoice_submit` early return when `cost <= 0` |
| EC3 PCV-closed period | §6.4 | `allocation_engine.before_submit._validate_period_not_closed` checks PCV exists for company in period |
| EC4 chỉ cost phân bổ, không direct | §10.2 | cogs_engine handles cost_pinned from allocated shares (R10.4) |
| EC5 KTT để trống `wip_override_account` | §6.2 | engine falls back to Settings default, no warning post-submit (form-level warning Phase 2) |
| EC6 backdated cost sau stage submitted | §3 R3.4 | Stage controller validates `_lock_when_si_submitted` — chứng từ row reject (R4.3 "khóa") |
| EC7 cancel project mid-stream | §6.4 | Project Costing.status "Đã hủy" — submitted SI stage giữ nguyên, others unpin (cron or manual) |

### 18.4 Phase 2 deferrals — explicit list

Mọi item dưới đây CHỦ ĐỘNG defer khỏi Phase 1, có lý do cụ thể. Phase 2 = sprint riêng sau Phase 1-7 ship + dùng thật ≥1 tháng + thu feedback từ KTT.

#### D1. Stage status `Đã thu tiền` — derive runtime, không DB update

- **Hiện trạng Phase 1:** Project Costing Stage có 6 status enum (Dự kiến / Đang thi công / Chờ xuất HĐ / Đã có SI draft / Đã xuất HĐ / Đã hủy). `Đã thu tiền` KHÔNG enum, KHÔNG cập nhật vào field `status`.
- **Hiển thị Phase 1:** UI Pivot Tool + form render label động đọc runtime từ `Sales Invoice.outstanding_amount == 0`. Code-level: helper `get_stage_display_status(stage)` trả về `"Đã thu tiền"` khi SI fully paid.
- **Phase 2 trigger:** nếu KTT cần filter/sort/report theo "Đã thu tiền" → thêm cron sync `hourly_long` cập nhật field `status` từ Payment Entry. Hoặc thêm field riêng `payment_status` (Select Open/Partial/Paid) derived khác `status`.
- **Lý do defer:** complexity của cron sync + race condition giữa SI cancel ↔ PE cancel ↔ status field. Phase 1 đủ với label hiển thị.

#### D2. Drag-drop reordering Project Costing Stage

- **Hiện trạng Phase 1:** KTT/PM edit field `stage_order` (Int) thủ công, sort tăng dần. Có thể thêm 2 button "↑" "↓" trên stage card trong form rendering (cheap).
- **Phase 2:** drag-and-drop UI trong Pivot Tool — kéo stage column sang trái/phải đổi order. React DnD library.
- **Lý do defer:** UX nice-to-have, không block nghiệp vụ. KTT điền stage_order khi tạo stage là OK; rare khi cần đổi sau.

#### D3. Cost split 1 chứng từ row → ≥2 stages

- **BL ref:** R4.2 nói "1 chi phí có thể chia ra ≥1 giai đoạn. Tổng các phần chia phải = nguyên giá."
- **Hiện trạng Phase 1:** API `pin_cost_to_stage` reject nếu `split_amount < row.amount`. 1 chứng từ row = 1 stage atomic. KTT muốn split → phải sửa chứng từ gốc (vd: tách PI Item thành 2 row, mỗi row gắn 1 stage).
- **Phase 2:** thêm DocType `Pinned Cost Split` (child) lưu mapping `(source_row, stage_name, portion_amount)`. API `pin_cost_to_stage` accept `split_amount`. Engine gom theo `Pinned Cost Split` thay vì đọc field `project_costing_stage` trên row gốc.
- **Lý do defer:** schema + UX phức tạp. Đa số use case Phase 1 không cần split (PI/SE thường cho 1 stage; SE có thể tách trước khi xuất kho).

#### D4. Allocation Run scheduler auto

- **BL ref:** R10.2 explicitly "KTT tạo **manual** (không scheduler tự động)."
- **Decision Phase 1 + Phase 2:** KHÔNG schedule. Manual mãi mãi (per Long quyết định). Mỗi cuối tháng KTT mở Cost Allocation Run, chọn source costs, chọn method, duyệt.
- **Lý do hard NO scheduler:** scheduler runs mỗi tháng — nếu KTT chưa input source costs (PIs/Slips/ECs chưa được tag `cost_type=Phân bổ`), JE sinh ra sai. Tốt hơn manual có review.

#### D5. Per-project ACL (Project Manager chỉ thấy project mình assigned)

- **Hiện trạng Phase 1:** flat — mọi user có read role thấy mọi Project Costing cùng company. KHÔNG register `permission_query_conditions`.
- **Phase 2 trigger:** nếu DCNET có ≥2 PM independent, không muốn PM-A thấy project của PM-B → thêm `permission_query_conditions` join qua `tabProject` permission (ERPNext core có built-in per-project ACL trên Project).
- **Lý do defer:** Phase 1 DCNET 1-2 PM, share visibility OK.

#### D6. Salary Slip allocation source (lương khoán phân bổ %)

- **BL ref:** R3.3 list Salary Slip allocation thủ công là 1 nguồn chi phí.
- **Hiện trạng Phase 1:** KHÔNG hỗ trợ direct Salary Slip → project. Lương kỹ sư on-site (direct) đi qua Timesheet (hours × rate), tag project. Lương PM (gián tiếp) đi qua Cost Allocation Run (KTT add Salary Slip vào source_costs của Allocation Run, chọn cost_type=Phân bổ).
- **Phase 2 trigger:** nếu KTT muốn direct allocate (vd: 60% lương Slip A → Project X, 40% → Project Y) không qua Allocation Run → thêm child table `Salary Slip Project Allocation` trên Salary Slip với rows `(project, percent, amount)`, hook on_submit sinh JE Dr 154-project / Cr 334 per share.
- **Lý do defer:** Allocation Run pattern đã cover use case lương PM gián tiếp đủ. Direct % allocation phức tạp hơn cần UX riêng.

#### D7. 2-tier SI submit workflow (Hóa đơn > X tr cần GĐ duyệt)

- **BL ref:** R6.6 — explicitly optional, default tắt.
- **Hiện trạng Phase 1:** KTT + GĐ đều submit SI mặc định, không workflow.
- **Phase 2:** thêm field `enable_si_two_tier_approval` (Check) + `si_two_tier_threshold` (Currency) vào VN Accounting Settings. Implement qua Frappe Workflow trên Sales Invoice với 2 state (`Draft` → `Pending GĐ Approval` ≥ threshold → `Submitted`). Helper Workflow assignment notification.
- **Lý do defer:** ít công ty cần. Bật khi customer thực sự yêu cầu.

#### D8. Vượt công suất 627 (TT99/2025)

- **BL ref:** §11.5 — TT99 quy định CP cố định 627 vượt công suất bình thường → Dr 632 thẳng, không qua 154.
- **Hiện trạng Phase 1:** toàn bộ 627 phân bổ qua 154 (giả định service company khó định lượng công suất).
- **Phase 2 trigger:** nếu công ty bắt đầu định lượng công suất (vd: số tiếng kỹ sư khả dụng/tháng) + muốn tách "vượt công suất" → thêm field "Phần vượt công suất" trên Cost Allocation Run, engine tách thành 2 JE: 1 JE Dr 154 / Cr 627 (trong công suất), 1 JE Dr 632 / Cr 627 (vượt công suất).
- **Lý do defer:** TT99 quy định nhưng compliance audit ít kiểm tra. Phase 1 đơn giản hóa OK.

#### D9. Workspace dashboard mới cho "Giá thành công trình"

- **Hiện trạng Phase 1:** chỉ 3 sidebar items trong Giá thành section (Project Costing list / Allocation Run list / Cost Collection report). KHÔNG có dedicated workspace page với charts.
- **Phase 2:** thêm Frappe Workspace `Giá thành công trình` với:
  - Number Cards: "Project đang thi công", "WIP balance toàn công ty", "SI chưa xuất tháng này"
  - Charts: P&L per project (bar), Cost composition (donut), Stage status (stacked)
  - Shortcuts tới Project Costing list filtered by status
- **Lý do defer:** mới có data ý nghĩa sau ≥1 tháng dùng thật. Workspace empty đầu tiên trông tệ.

### 18.5 Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| ERPNext upgrade breaks JE bù 2-layer | Low | Pattern stable (LCV uses it 2026-Q1+, no breakage to date). Marker-based idempotency safe. |
| Pivot Tool React bundle size | Low | esbuild IIFE; if >50KB, lazy-load. |
| `tabGL Entry.project` column may not be reliable for all sources | Medium | Verify in Phase 2 — if `project` column not set by ERPNext for some sources (vd JE manual), add custom column or join through reference_name. |
| Cross-company filter on `Project Costing` | Low | Project.company is reqd in ERPNext core — filter works out of box. |
| `vn_translation` conflict with new strings | Medium | Verify each key against vn_translation/vi.csv at translation phase. Update vn_translation if conflict. |
| Demo data project naming collision với existing 6 projects | Low | Prefix all demo projects with `[DEMO]` for easy filter. |

### 18.6 Verification commands (per phase)

**Phase 1:**
```bash
# Syntax check all new .py files
find apps/vn_accounting/vn_accounting/project_costing -name "*.py" -exec python3 -m py_compile {} \;
# DocType installable
bench --site dcnet.localhost migrate
bench --site dcnet.localhost execute frappe.client.get_list --kwargs '{"doctype":"DocType","filters":[["name","like","Project Costing%"]],"fields":["name"]}'
# Settings has 4 new fields
bench --site dcnet.localhost execute frappe.client.get_value --kwargs '{"doctype":"VN Accounting Settings","fieldname":"wip_account_project_costing"}'
```

**Phase 2:**
```bash
cd /home/long/long/frappe-bench-dcnet
env/bin/python -m unittest apps.vn_accounting.vn_accounting.project_costing.tests.test_markup_calc -v
env/bin/python -m unittest apps.vn_accounting.vn_accounting.project_costing.tests.test_allocation_engine -v
# ... others
```

**Phase 3 (live):**
- Navigate to `/app/project-costing-pivot?costing=<demo>` — verify React shell loads, 0 console errors.
- Drag-drop cost row → stage column → verify backend update.

**Phase 6 (full):**
- `/design-qa` skill on `/app/project-costing/<demo>` + Pivot Tool — fix all severity-2+.
- Playwright walks: project A end-to-end (create → pin → markup → SI draft → submit → close).

---

## Tham chiếu

- BL spec: `apps/vn_accounting/docs/specs/2026-05-15-project-costing-business-logic.md`
- LCV JE-bù pattern (mẫu): `apps/vn_accounting/vn_accounting/landed_cost/lcv_hooks.py`
- Deferred schedule embedded section (mẫu UI): `apps/vn_accounting/vn_accounting/public/js/process_deferred_accounting.bundle.js`
- vn_help authoring: `~/.claude/memory/reference_vn_help_authoring_standard.md`
- TT99/2025 GL chain xây lắp: `~/.claude/rules/erpnext-accounting.md` (section "TT99/2025 doanh nghiệp xây lắp")
- Multi-session NOT used — per Long's decision 2026-05-15.
