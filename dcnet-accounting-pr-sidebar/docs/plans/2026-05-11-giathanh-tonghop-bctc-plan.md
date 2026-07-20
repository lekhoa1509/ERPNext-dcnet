# Implementation Plan — Giá thành + Tổng hợp + BCTC (TT99/2025)

**Spec:** `docs/specs/2026-05-11-giathanh-tonghop-bctc.md` (916 lines, 21 decisions chốt)
**Multi-session task file:** `docs/multi-session/giathanh-tonghop-bctc.md`
**Branch:** `feat/giathanh-tonghop-bctc` (created from `develop`)
**Site:** `dcnet.localhost` (port 8001)
**Estimated sessions:** 15–18 (per spec §9)

This plan is *file-level* — each numbered task corresponds to one or more concrete file edits with exact paths. Sub-agents executing this plan should treat the spec as the source of truth and use this plan as the navigator.

---

## P0 — Phase 0: Foundation (THIS SESSION)

| # | Task | File | Status |
|---|------|------|--------|
| P0.1 | Branch `feat/giathanh-tonghop-bctc` from `develop` | git | DONE |
| P0.2 | Scaffold sub-packages with `__init__.py` docstrings | `vn_accounting/{landed_cost,costing,period_closing,financial_reporting}/__init__.py` | DONE |
| P0.3 | Implementation plan (this file) | `docs/plans/2026-05-11-giathanh-tonghop-bctc-plan.md` | DONE |
| P0.4 | Self-review (§3-point checklist below) | inline | DONE |
| P0.5 | Commit + session-last | git + `.multi-session/session-last-giathanh-tonghop-bctc.md` | (in progress) |

---

## P1 — Phase 1: Foundation — 4 Settings DocTypes + BCTC Template Seeding

> **Outcome:** Site `dcnet.localhost` has 4 Settings working with TT99/2025 defaults; Company VN auto-clones BCTC Mapping; rich UI guidance on every field.

### P1.1 — `LCV Allocation Settings` (Single DocType)

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/lcv_allocation_settings/lcv_allocation_settings.json`

Fields per spec §3.1:
- `expense_types` (Table → `LCV Expense Type Setting`)
- `auto_apply_settings_on_new_lcv` (Check, default=1)
- `import_vat_default_deductible_pct` (Float, default=100, reqd=1)

Each field needs rich `description` per UI guidance §12 (see spec line 96).

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/lcv_expense_type_setting/lcv_expense_type_setting.json` — child DocType

Fields:
- `expense_type` (Data, in_list_view=1)
- `expense_type_key` (Data, in_list_view=1, reqd=1, unique-within-parent via validate)
- `default_expense_account` (Link Account, in_list_view=1, get_query filtered by `company` ctx if available)
- `is_import_only` (Check, in_list_view=1)
- `allocation_method` (Select: `Amount`/`Qty`/`Weight`/`Volume`, in_list_view=1)

**Seed file:** `apps/vn_accounting/vn_accounting/fixtures/lcv_allocation_settings_default_expense_types.json`

12 rows per spec table at line 106–119.

**Controller:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/lcv_allocation_settings/lcv_allocation_settings.py`
- `validate()`: unique `expense_type_key` within `expense_types` table
- `validate()`: `0 ≤ import_vat_default_deductible_pct ≤ 100`

### P1.2 — `Manufacturing Costing Settings` (Single DocType)

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/manufacturing_costing_settings/manufacturing_costing_settings.json`

11 fields per spec §3.2 (lines 161-174):
- `direct_material_account` (Link Account, reqd=1, default via lookup 621*)
- `direct_labor_account` (Link Account, reqd=1, default via lookup 622*)
- `manufacturing_overhead_account` (Link Account, reqd=1, default via lookup 627*)
- `work_in_progress_account` (Link Account, reqd=1, default via lookup 154*)
- `finished_goods_account` (Link Account, reqd=1, default via lookup 155*)
- `cost_of_goods_sold_account` (Link Account, reqd=1, default via lookup 632*)
- `cost_object` (Select, options `Item\nWork Order\nProject\nCustomer\nSales Order`, default `Item`)
- `overhead_allocation_basis` (Select, options 6 bases, default `Machine Hours`)
- `wip_valuation_method` (Select, options `Equivalent Production\nDirect Material Only\n50% Conversion Cost`, default `Equivalent Production`)
- `auto_hide_for_small_enterprise` (Check, default=1)
- `transfer_to_finished_goods` (Check, default=1)
- `services_cogs_account` (Link Account, depends_on `eval:!doc.transfer_to_finished_goods`, default via lookup 632*)

Rich `description` per UI guidance (TT99/2025 reference + override hint per field).

**Controller:** `manufacturing_costing_settings.py`
- `validate()`: if `transfer_to_finished_goods=0` → `services_cogs_account` reqd

### P1.3 — Extend `VN Accounting Settings` (existing Single)

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json` — APPEND fields, do NOT regenerate the file.

New fields per spec §3.3 (lines 184-192):
- Section Break "Kết chuyển cuối kỳ" with `description` explaining periodic vs annual closure
- `pnl_account_911` (Link Account, reqd=1, default lookup 911*)
- `retained_earnings_current_year` (Link Account, reqd=1, default lookup 4212*)
- `retained_earnings_prior_year` (Link Account, reqd=1, default lookup 4211*)
- `revenue_accounts_to_close` (Table → `Account List Item`, reqd=1)
- `expense_accounts_to_close_periodic` (Table → `Account List Item`, reqd=1, **excludes 821**)
- `corporate_income_tax_account` (Link Account, reqd=1, default lookup 821*)
- `period_closing_balance_tolerance` (Currency, default=1)

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/account_list_item/account_list_item.json` — child DocType (reusable)

Fields:
- `account` (Link Account, in_list_view=1, reqd=1)
- `note` (Small Text, in_list_view=1)

**Seed:** `after_install` hook seeds:
- `revenue_accounts_to_close` ← TK 511, 512, 515, 711 (per spec line 189)
- `expense_accounts_to_close_periodic` ← TK 632, 635, 641, 642, 811 (per spec line 190)

### P1.4 — `BCTC Mapping` + `BCTC Mapping Template` (new DocTypes)

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/bctc_mapping/bctc_mapping.json`

Fields per spec §3.4 (lines 216-224):
- `company` (Link Company, reqd=1, unique=1)
- `coa_template` (Data, options `vn_large_enterprise\nvn_small_enterprise`, read_only=1 after detect)
- `b01_lines` / `b02_lines` / `b03_lines` (Tables → `BCTC Line`)
- `b09_template_path` (Data, default `[apppath]/templates/b09_dn_template.xlsx`)
- `last_restored_from_default` (Datetime, read_only=1)
- Naming rule: `BCTC Mapping {company}`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/bctc_mapping_template/bctc_mapping_template.json`

Hidden DocType (`hide_toolbar=1`, no Web View). Same Table fields, naming = template key (`vn_large_enterprise_b01` etc.).

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/bctc_line/bctc_line.json` — child DocType

Fields per spec §3.4 (lines 228-239):
- `code` (Data, reqd=1, in_list_view=1, read_only=1)
- `name` (Data, reqd=1, in_list_view=1, read_only=1)
- `section` (Data)
- `value_type` (Select: `closing_debit\nclosing_credit\nperiod_debit\nperiod_credit\nformula`)
- `account_formula` (Long Text)
- `line_formula` (Long Text)
- `display_indent` (Int, default=0)
- `is_subtotal` (Check)
- `sign_multiplier` (Select: `+1\n-1`, default `+1`)
- `note` (Small Text)

**Fixture seeds:**
- `apps/vn_accounting/vn_accounting/fixtures/bctc_template_b01_large.json` — ~50 lines per TT99/2025 Phụ lục IV
- `bctc_template_b01_small.json` — simpler subset for small COA
- `bctc_template_b02_large.json` / `bctc_template_b02_small.json` — ~18 lines
- `bctc_template_b03_large.json` / `bctc_template_b03_small.json` — ~30 lines

Each fixture contains a single `BCTC Mapping Template` doc with seeded child rows.

**Controller:** `bctc_mapping.py`
- 2 buttons via `.js`: "Copy mapping từ Company khác" + "Khôi phục mặc định TT99/2025" (per-line and per-report modes)
- `frappe.whitelist()` methods: `copy_from_company(source_company)` + `restore_from_template(report: b01|b02|b03, line_codes: list|None)`

### P1.5 — Install Hooks Orchestration

**File:** `apps/vn_accounting/vn_accounting/setup/__init__.py` (or `install.py` — check existing first)

Add to `after_install` (per spec §6.1):
```python
seed_lcv_allocation_settings()              # 12 expense types
seed_manufacturing_costing_settings()       # TT99/2025 defaults
seed_period_closing_account_settings()      # 911/4212/lists/821
seed_bctc_mapping_templates()               # 2 templates × 3 reports
```

Each function lives next to its DocType controller for locality.

**File:** `apps/vn_accounting/vn_accounting/hooks.py`

Extend existing `Company.on_update` (per spec §6.2):
```python
"Company": {
    "on_update": [
        # existing handlers...
        "vn_accounting.financial_reporting.bctc_mapping_lifecycle.ensure_bctc_mapping_for_company",
    ],
}
```

**File:** `apps/vn_accounting/vn_accounting/financial_reporting/bctc_mapping_lifecycle.py`

```python
def ensure_bctc_mapping_for_company(doc, method):
    if doc.country != "Vietnam": return
    if frappe.db.exists("BCTC Mapping", {"company": doc.name}): return
    coa_template = _detect_coa_template(doc.name)   # check 621/622/627 presence
    _clone_template_to_company(doc.name, coa_template)
```

### P1.6 — Tests Phase 1

| File | Purpose |
|---|---|
| `apps/vn_accounting/tests/test_settings_seed.py` | All 4 Settings populate after install (use `frappe.test_runner` or manual fixture sync) |
| `apps/vn_accounting/tests/test_bctc_template_clone.py` | Company VN creation auto-clones; large vs small detection |
| `apps/vn_accounting/tests/test_doctype_field_descriptions.py` | Per §8.4 — all reqd=1 + Link/Select/Date/Currency fields have descriptions ≥10 chars |

Tests use `unittest.mock` patching `frappe.*` per `frappe-erpnext.md` rule.

**Acceptance for P1 end-of-phase verification (per task spec):**
- `test -f` on all 4 new DocType JSON files
- `grep -q corporate_income_tax_account` in VN Accounting Settings JSON
- `grep -q transfer_to_finished_goods` in Manufacturing Costing Settings JSON
- `env/bin/python -m py_compile apps/vn_accounting/vn_accounting/setup/__init__.py` exits 0

**Live testing in-session (NOT in Verification Commands per multi-session rule #13):**
1. `bench --site dcnet.localhost migrate`
2. `bench restart && bench --site dcnet.localhost clear-cache`
3. Open all 4 Settings pages — verify field descriptions render

---

## P2 — Phase 2: LCV (Landed Cost Voucher universal)

> **Outcome:** LCV auto-fills expense accounts from Settings (domestic + import). VAT NK split logic correct. Sidebar "Giá thành" section has 5 items.

### P2.1 — LCV hooks

**File:** `apps/vn_accounting/vn_accounting/landed_cost/lcv_hooks.py`

```python
def lcv_apply_default_expense_account(doc, method):
    """before_validate — auto-fill expense_account from Settings by matching expense_type_key.
    No-op if auto_apply_settings_on_new_lcv=0 or row.expense_account already set."""

def lcv_validate_import_vat_split(doc, method):
    """validate — ensure VAT deductible + non-deductible split sums to VAT NK total."""
```

### P2.2 — Custom Fields on Landed Cost Voucher

**File:** `apps/vn_accounting/vn_accounting/fixtures/custom_field.json` (extend existing)

- `vn_is_import_lcv` (Check, Section Break before "Items", description="Tick nếu phiếu này phân bổ chi phí nhập khẩu (hàng từ nước ngoài). Khi tick → các loại phí nhập khẩu (thuế NK, VAT NK, phí hải quan) sẽ hiển thị trong danh sách phụ phí.")
- `vn_is_subject_to_import_duty` (Check, default=1, depends_on=`eval:doc.vn_is_import_lcv`, description per spec line 153)

### P2.3 — Page `landed-cost-allocation-settings`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/page/landed_cost_allocation_settings/landed_cost_allocation_settings.json` + `.js`

Friendly wrapper for the Single DocType — same fields rendered with section headers + help panel top.

### P2.4 — Script Report `Landed Cost Pending Allocation`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/report/landed_cost_pending_allocation/landed_cost_pending_allocation.{py,json,js}`

Report query: GL entries on 1388/331 with no LCV link. Cols per spec §4.5 line 463. "Tạo LCV" button on each row via custom `.js`.

### P2.5 — Sidebar update (5 items)

**File:** `apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json`

Append 5 items to "Giá thành" section per spec §5 (lines 545-551).

### P2.6 — Translations (~25 entries)

**File:** `apps/vn_accounting/vn_accounting/translations/vi.csv`

Append: LCV terms (Landed Cost Allocation, Pending Allocation, 12 expense types VN labels).

### P2.7 — vn_help articles GT-01, GT-02

- `apps/vn_help/vn_help/help_articles/co/lcv-co-ban.md` — Phân bổ chi phí mua hàng cơ bản
- `apps/vn_help/vn_help/help_articles/co/lcv-nhap-khau.md` — LCV cho hàng nhập khẩu

YAML frontmatter per `reference_vn_help_authoring_standard.md`. Tiếng Việt thuần — no "Landed Cost Voucher", call it "Phiếu phân bổ chi phí mua hàng".

### P2.8 — Tests Phase 2

| File | Purpose |
|---|---|
| `apps/vn_accounting/tests/test_lcv_defaults.py` | Auto-fill domestic + import, override behavior |
| `apps/vn_accounting/tests/test_lcv_validation.py` | VAT split 0/100, 50/50, 100/0, reject invalid |
| `apps/vn_accounting/tests/test_pending_allocation_report.py` | Query correct, 1388/331 untied surface |

---

## P3 — Phase 3: Tổng hợp (Sổ kế toán + Kết chuyển 911 + Khóa sổ)

> **Outcome:** S03a-DN + S03b-DN render TT99/2025 layout. Wizard kết chuyển 911 auto-detects fiscal year. PCV restricted to Accounts Manager + audit log.

### P3.1 — Script Report `S03a-DN Sổ Nhật Ký Chung`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/report/s03a_dn_so_nhat_ky_chung/s03a_dn_so_nhat_ky_chung.{py,json,js}`

Cols: Ngày | Số CT | Loại CT | Diễn giải | TK Nợ | TK Có | PS Nợ | PS Có
Sort: `posting_date ASC, creation ASC`
Excel export: openpyxl helper in `financial_reporting/excel.py` (shared with BCTC).

### P3.2 — Script Report `S03b-DN Sổ Cái`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/report/s03b_dn_so_cai/s03b_dn_so_cai.{py,json,js}`

Layout 1 TK / trang. Drill-through via standard ERPNext GL Entry filter URL.

### P3.3 — Page `period-closing-911`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/page/period_closing_911/period_closing_911.{json,js}`

3-section layout per spec §4.1 mockup. Help panel top (Mục đích / Các bước / Kết quả).

**Helper file:** `apps/vn_accounting/vn_accounting/period_closing/wizard.py`

API endpoints:
- `get_closing_preview(company, period_start, period_end)` — returns `is_fiscal_year_end`, `revenue_je_preview`, `expense_je_preview` (include/exclude 821 by auto-detect), `result_je_preview`
- `create_closing_journal_entries(company, period_end, mappings, include_tax_account)` — creates 3 draft JE

### P3.4 — Period Closing Voucher extension

**File:** `apps/vn_accounting/vn_accounting/period_closing/pcv_hooks.py`

- `pcv_validate_vn_requirements(doc, method)` — reject draft JE, unbalanced, 911 not done, empty reason
- `pcv_audit_log(doc, method)` — comment with signer + date + reason
- `pcv_validate_cancel(doc, method)` — for `on_cancel`

**File:** `apps/vn_accounting/vn_accounting/fixtures/custom_field.json` (extend)

- `vn_lock_unlock_reason` (Long Text, reqd=1, description per spec line 318)
- `vn_operating_status` on Company (Select per spec line 314)

**File:** `apps/vn_accounting/vn_accounting/fixtures/custom_docperm.json` (new or extend)

DocPerm override per spec lines 305-310. delete=0 for all roles.

**File:** `apps/vn_accounting/vn_accounting/hooks.py`

Register PCV hooks:
```python
"Period Closing Voucher": {
    "validate": "vn_accounting.period_closing.pcv_hooks.pcv_validate_vn_requirements",
    "on_submit": "vn_accounting.period_closing.pcv_hooks.pcv_audit_log",
    "on_cancel": "vn_accounting.period_closing.pcv_hooks.pcv_audit_log",
}
```

### P3.5 — Sidebar update (4 items)

Append to "Tổng hợp" section per spec §5 lines 555-560.

### P3.6 — Translations (~20 entries)

### P3.7 — vn_help articles TH-01..TH-04

### P3.8 — Tests Phase 3

| File | Purpose |
|---|---|
| `tests/test_911_je_generation.py` | 3 JE structure, debit=credit per JE |
| `tests/test_fiscal_year_detection.py` | Auto-detect, 821 inclusion logic |
| `tests/test_pcv_validation.py` | Reject draft / unbalanced / empty reason |
| `tests/test_pcv_permissions.py` | Accounts Manager only, audit log written |

---

## P4 — Phase 4: BCTC (B01, B02, B03 + B09)

> **Outcome:** 4 BCTC reports operational. B01 equation `mã_270 = mã_440` holds. Drill-through works. B09 multi-sheet Excel.

### P4.1 — BCTC resolver engine

**File:** `apps/vn_accounting/vn_accounting/financial_reporting/resolver.py`

```python
def resolve_bctc_line(company, line: BCTCLine, period_start, period_end) -> Decimal:
    """Returns Decimal value for this line in this period.
    Recursive for line_formula referencing other line codes.
    Uses account_formula syntax: +TK,+TK,-TK (with wildcard 511%)."""
```

5 `value_type` modes: `closing_debit / closing_credit / period_debit / period_credit / formula`.

### P4.2 — Script Report `B01-DN`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/report/b01_dn_bao_cao_tinh_hinh_tai_chinh/b01_dn_bao_cao_tinh_hinh_tai_chinh.{py,json,js}`

Cols: Mã | Tên chỉ tiêu | Số cuối kỳ | Số đầu năm
Filter: Company + As-of date + fiscal year
JS adds:
- Hover ℹ icon on Mã → formula tooltip
- Click number → drill to GL Entries (URL with filters constructed from `account_formula`)
- "Cấu hình mapping" button → opens BCTC Mapping
- "Xuất Excel" button → calls `financial_reporting/excel.py::export_b01(company, as_on_date)`
- Equation check `mã_270 == mã_440` (within tolerance) — red banner if mismatch

### P4.3 — Script Report `B02-DN`

**File:** `report/b02_dn_bao_cao_kqhdkd/*` — same pattern.

### P4.4 — Script Report `B03-DN`

**File:** `report/b03_dn_bao_cao_lctt/*` — phương pháp gián tiếp only (Phase 1 per D16).

### P4.5 — Page `b09-dn-generator`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/page/b09_dn_generator/b09_dn_generator.{json,js}`

**Helper:** `apps/vn_accounting/vn_accounting/financial_reporting/b09_generator.py`

openpyxl multi-sheet per spec §4.6 (lines 479-488):
- Sheet 1 `1_Van_xuoi` — placeholders
- Sheets 2-N `5.x_Chi_tiet_*` — auto-fill from GL/Asset/Stock/Loan
- Auto-fill cells: gray bg + locked. Editable cells: white + unlocked. `worksheet.protection.enable()`.

### P4.6 — BCTC Mapping form buttons (`.js`)

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/bctc_mapping/bctc_mapping.js`

Implement dialog UIs for "Copy from another Company" + "Restore defaults" (full or row-level).

### P4.7 — Sidebar update (5 items)

Append to "Báo cáo tài chính" section per spec §5 lines 566-572. Default `route_options` with `fiscal_year={current}` + `as_on_date={today}` helper resolution at click time (use existing sidebar route_options interpolation; if helper doesn't exist, add to sidebar JS bundle or use server-side default in report's `default_filters`).

### P4.8 — Translations (~40 entries)

### P4.9 — vn_help articles BCTC-01..BCTC-04

### P4.10 — Tests Phase 4

| File | Purpose |
|---|---|
| `tests/test_bctc_resolver.py` | Formula parser, all 5 value_type, line_formula recursion |
| `tests/test_b01_equation.py` | Seed test Company GL → assert mã_270 == mã_440 |
| `tests/test_b02_calculations.py` | Compute mã 60 end-to-end |
| `tests/test_bctc_mapping_clone.py` | Copy from Company + Restore defaults |

---

## P5 — Phase 5: Giá thành sản xuất

> **Outcome:** WIP Valuation works (4 methods). Manufacturing Costing Wizard rẽ nhánh đúng (manufacturing → 155 + Stock Entry; services/xây lắp → 632 direct).

### P5.1 — DocType `Work In Progress Valuation`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/doctype/work_in_progress_valuation/work_in_progress_valuation.json`

All fields per spec §3.5 (lines 261-284) including `physical_units_in_progress`, `equivalent_completion_pct`, `computed_closing_wip` (read-only, auto-compute), `valuation_method` (4 options).

Submittable: No (status workflow only).

**Controller:** `work_in_progress_valuation.py`
- `validate()`: auto-compute `computed_closing_wip` based on `valuation_method` (per spec line 278)
- Status workflow: Draft → Calculated → Posted → Cancelled

### P5.2 — Script Report `Production Cost Aggregation`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/report/production_cost_aggregation/*`

621/622/627 phát sinh kỳ, group by cost_object.

### P5.3 — Page `manufacturing-costing-wizard`

**File:** `apps/vn_accounting/vn_accounting/vn_accounting/page/manufacturing_costing_wizard/*`

7-step flow per spec §4.2 (line 386-397). Branching at Step 6/7 per `transfer_to_finished_goods`.

**Helpers:** `apps/vn_accounting/vn_accounting/costing/wizard.py`

API endpoints per spec line 411-414:
- `aggregate_production_costs(company, period_start, period_end, cost_object_type)`
- `calculate_unit_costs(wip_valuations)`
- `create_costing_journal_entries(company, posting_date, calculations, account_overrides, transfer_mode)`

### P5.4 — Custom Fields on Project

**File:** `fixtures/custom_field.json` extend with 4 Project fields per spec §4.7 (lines 511-514).

### P5.5 — Sidebar update (3 manufacturing items)

Append to "Giá thành" — LCV items added in P2 already; add Tập hợp / Bảng tính / etc.

### P5.6 — Translations (~30 entries)

### P5.7 — vn_help articles GT-03, GT-04

### P5.8 — Tests Phase 5

| File | Purpose |
|---|---|
| `tests/test_unit_cost_calculation.py` | Edge cases (0 qty, 0 closing, equivalent production) |
| `tests/test_overhead_allocation.py` | 6 allocation bases, sum=627 |
| `tests/test_costing_branching.py` | Services → 632 direct; manufacturing → 155 + Stock Entry |
| `tests/test_wip_valuation_methods.py` | 4 methods compute correctly |

---

## P6 — Phase 6: Polish + i18n full + Tests regression + Docs

> **Outcome:** All 12 vn_help articles complete. Full translation pass. No-hardcoded-TK regression test passes. UI guidance regression test passes. CODEBASE.md updated. Full E2E smoke test.

### P6.1 — Complete vn_help articles (12 total)

Verify all 12 articles per §12.3 exist with proper YAML frontmatter + tiếng Việt thuần.

### P6.2 — Translation pass

Review `vi.csv` completeness — every new English string has VN translation. Run `bench --site dcnet.localhost clear-cache` and visually check sidebar + forms.

### P6.3 — No-hardcoded-TK regression test

**File:** `apps/vn_accounting/tests/test_no_hardcoded_accounts.py`

Per spec §8.3 — grep regex `["']\b[1-9]\d{2,4}["']` in `landed_cost/`, `costing/`, `period_closing/`, `financial_reporting/` Python files. Whitelist: fixture JSONs, lookup helpers with comment `# fallback default TT99/2025`.

### P6.4 — UI guidance regression test

**File:** `apps/vn_accounting/tests/test_ui_guidance_coverage.py`

Per spec §8.4 — scan all new DocType JSONs:
- Every `reqd=1` field has `description` ≥ 10 chars
- Every Link/Select/Date/Currency/Float/Percent has `description`
- DocType has ≥ 1 Section Break with `description`
- Custom button `.js` has `__()` wrap

### P6.5 — CODEBASE.md + CODEBASE_DETAIL.md update

**Files:** `apps/vn_accounting/docs/CODEBASE.md` (and detail) — add 4 new sub-packages + ~12 new DocTypes.

### P6.6 — Excel layout polish

Verify font (Times New Roman 11pt), column widths, merged headers across all 4 BCTC reports + S03a/S03b. Open in real Excel/LibreOffice for verification.

### P6.7 — Full E2E smoke test

Per task spec Live Testing — Full smoke:
1. Create fresh Company "Smoke Test Co" with country=Vietnam, COA template=large
2. Verify BCTC Mapping auto-cloned + COA seeded
3. Walk every sidebar item in 3 sections (Giá thành / Tổng hợp / BCTC) — 15 items
4. Each opens without error + default filter populated + inline guidance visible
5. Random-sample 10 fields/buttons → all have tooltips/descriptions

### P6.8 — FEATURES.md update

Move C7.*, C8.*, C9.*, C10.*, relevant C2.* to "Done" status with date.

### P6.9 — Branch finalization

Commits clean, branch ready for PR to `develop`.

---

## Self-Review Notes

### 1. Spec coverage

| Spec section | Plan task |
|---|---|
| §3.1 LCV Allocation Settings | P1.1 |
| §3.2 Manufacturing Costing Settings | P1.2 |
| §3.3 Period Closing extensions on VN Accounting Settings | P1.3 |
| §3.4 BCTC Mapping (per-Company) + Template | P1.4, P4.6 |
| §3.5 WIP Valuation | P5.1 |
| §3.6 Period Closing Voucher extensions | P3.4 |
| §4.1 Wizard 911 | P3.3 |
| §4.2 Wizard costing | P5.3 |
| §4.3 BCTC engine | P4.1 |
| §4.4 S03a/S03b | P3.1, P3.2 |
| §4.5 Auxiliary reports (Pending Allocation, Production Aggregation) | P2.4, P5.2 |
| §4.6 B09-DN Excel generator | P4.5 |
| §4.7 Project setup guide (xây lắp) | P5.4 + P5.7 |
| §5 Sidebar wire-up (15 items) | P2.5, P3.5, P4.7, P5.5 |
| §6 Hooks & lifecycle | P1.5, P2.1, P3.4 |
| §7 Translations | P2.6, P3.6, P4.8, P5.6, P6.2 |
| §8 Tests (8.1-8.4) | P1.6, P2.8, P3.8, P4.10, P5.8, P6.3, P6.4 |
| §9 Phase decomposition | Mapped to P1-P6 |
| §12 UI Guidance | Cross-cutting — every DocType + page + report in all phases |
| §12.3 vn_help (12 articles) | P2.7, P3.7, P4.9, P5.7, P6.1 |

**Coverage: 100%** — every spec section maps to ≥1 plan task. ✅

### 2. Placeholder scan

- All file paths concrete (no TBD/TODO)
- Account number lookups described as "lookup 911*" pattern (matches `setup/account_lookup.py` convention of existing app — verify in P1 implementation)
- Test patterns reference concrete file names

No TBD/TODO except items in spec §10.8 (out-of-scope) — all listed in task spec as deferred. ✅

### 3. Type consistency

| Type / Name | Used in | Note |
|---|---|---|
| `LCV Allocation Settings` (Single) | P1.1, P2.1 | Consistent |
| `LCV Expense Type Setting` (child) | P1.1 | Consistent |
| `Manufacturing Costing Settings` (Single) | P1.2, P5.3 | Consistent |
| `VN Accounting Settings` (extended) | P1.3, P3.3, P3.4 | Existing DocType — extend only |
| `Account List Item` (child, reusable) | P1.3 | New |
| `BCTC Mapping` (per-Company) | P1.4, P4.6 | Consistent |
| `BCTC Mapping Template` (hidden) | P1.4 | Consistent |
| `BCTC Line` (child) | P1.4 | Consistent |
| `Work In Progress Valuation` (Status-only) | P5.1 | Submittable: No |
| `vn_is_import_lcv` / `vn_is_subject_to_import_duty` (Custom Field on LCV) | P2.2 | Consistent |
| `vn_lock_unlock_reason` (Custom Field on PCV) | P3.4 | Consistent |
| `vn_operating_status` (Custom Field on Company) | P3.4 | Consistent |
| `vn_is_construction_project` + 3 friends (Custom Field on Project) | P5.4 | Consistent |
| Hook `pcv_validate_vn_requirements` (validate) + `pcv_audit_log` (on_submit/on_cancel) | P3.4 | Consistent across hooks.py + module |
| Hook `lcv_apply_default_expense_account` (before_validate) + `lcv_validate_import_vat_split` (validate) | P2.1 | Consistent |
| Helper `ensure_bctc_mapping_for_company` (Company.on_update) | P1.5, P4 | Consistent |
| Function `resolve_bctc_line(company, line, period_start, period_end)` | P4.1, P4.2-P4.4 | Consistent |

**Names consistent across all tasks.** ✅

### 4. Risks / mitigations

| Risk | Mitigation |
|---|---|
| BCTC Mapping fixture import — Frappe fixture loader may not handle deeply-nested child tables | Test seed in P1 via `after_install` Python (programmatic insert) rather than JSON fixture loader; keep JSON files as data source read by Python |
| `Company.on_update` running too often + cloning BCTC Mapping repeatedly | Idempotency check `frappe.db.exists("BCTC Mapping", {"company": ...})` before clone |
| `vn_help` article path convention may differ from `apps/vn_help/vn_help/help_articles/co/` — verify against `reference_vn_help_authoring_standard.md` before authoring | Check existing articles' path during P2 start |
| Custom Field `idx` on LCV may push fields into wrong tab (per `frappe-v16-ui.md` rule "Custom Field idx Algorithm Pushes Past Tab Breaks") | Anchor `vn_is_import_lcv` via `insert_after` to a mid-tab field, NOT last field of a tab |
| Test fixture for `test_b01_equation` needs full Company + COA + sample GL — heavy setup | Use `setUpClass` with minimal Company + 5-10 hand-crafted GL Entries; do NOT seed full ERPNext sample data |
| Sidebar `route_options` `{current}` / `{today}` interpolation — check if existing sidebar bundle supports this; if not, expand at click time via JS or add server-side default | Investigate during P4.7; may need extending `vn_accounting/public/js/sidebar.bundle.js` |

### 5. Multi-session boundary suggestions

For runner phase progression via session-last marker `Phase N status: ✅ DONE`:

- **Session 1 (THIS):** P0 (branch + scaffold + plan + commit)
- **Sessions 2-4:** P1 (4 Settings DocTypes + seeds + tests) — likely 2-3 sessions
- **Sessions 5-6:** P2 (LCV) — 2 sessions
- **Sessions 7-9:** P3 (Tổng hợp) — 3 sessions
- **Sessions 10-14:** P4 (BCTC) — 4-5 sessions (heaviest)
- **Sessions 15-17:** P5 (Giá thành SX) — 3 sessions
- **Session 18:** P6 (Polish) — 1-2 sessions

Total estimated: 15-18 sessions (matches spec §9 estimate).

---

**Phase 0 status: ✅ DONE** (plan committed)

Next session starts P1.1 — `LCV Allocation Settings` DocType JSON + controller + seed fixture.
