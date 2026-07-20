# vn_accounting — Codebase Detail

File-by-file index with key function line numbers. Format: `filename → purpose; key_func():LXX`.

---

## Repo root

- `pyproject.toml` → flit_core build config; `version` read from `vn_accounting/__init__.py`
- `README.md` → install + quick start
- `FEATURES.md` → Done/In-Progress/Planned feature matrix
- `.gitignore`, `.github/` → standard; no CI beyond GitHub hooks

## `tests/` (pytest, excluded from LOC count)

- `test_coa.py` → verifies VN COA template registration and `get_chart()` tree return
- `test_company_defaults.py` → end-to-end: create Company (VN) → assert all VN default fields populated
- `test_report_utils.py` → unit: `extract_account_numbers`, `get_accounts_by_prefix`, opening balance calc
- `test_no_hardcoded_accounts.py` → regression: scans landed_cost/costing/period_closing/financial_reporting for hardcoded TK string literals (whitelist: seed files, # fallback comments, account_number lookups, TK label columns)
- `test_ui_guidance_coverage.py` → verifies 5 new DocType JSONs have field descriptions ≥10 chars on reqd=1 and Link/Select/Currency/Date fields

## `docs/`

- `BUSINESS_LOGIC.md` → pure business rules for accountants (starting point)
- `erpnext-v16-ke-toan.md` → historical notes on ERPNext v16 accounting quirks
- `specs/` → feature design specs (per spec file)
- `CODEBASE.md` → summary (entry point for new devs/AI)
- `CODEBASE_DETAIL.md` → this file

---

## `vn_accounting/` (inner package — top level)

- `__init__.py` → `__version__="1.1.0"`; `_patch_get_chart()`:L4 monkey-patches `erpnext...chart_of_accounts.get_chart` at import time so VN templates resolve via lazy-import convention
- `hooks.py` → app config (49 lines): `override_whitelisted_methods` (get_charts_for_country), `doc_events` (Company.on_update, Journal Entry.on_submit/cancel), `boot_session`, `after_install`/`after_migrate`, `scheduler_events.daily`, `app_include_js`/`app_include_css`, Print Format fixture
- `boot.py` → `boot_session(bootinfo)`:L11 walks `WORKSPACE_SIDEBARS` list, reads each Workspace Sidebar doc, injects `bootinfo["workspace_defaults"]` map `{DocType: [{sidebar, priority}]}` (tier 2 of 3-tier selection)
- `install.py` → `after_install()`:L9, `after_migrate()`:L19, `_sync_standard_docs()`:L29 (upsert Number Card + Dashboard Chart from JSON, bypassing "Cannot edit Standard" via `db_set`), `_sync_workspace_sidebar()`:L69, `_ensure_desktop_icon()`:L93 (Workspace Sidebar link_type with required link_to), `_seed_treasury_settings()`:L139, `_fix_workspace_labels()`:L179 (SQL fix for Unicode stripped on migrate)
- `modules.txt` → single entry: `VN Accounting`
- `patches.txt` → empty (required so `is_frappe_app()` returns True)

## `vn_accounting/api/` — dashboard + forecast backend

- `dashboard.py` → `get_dashboard()`:L147 (whitelisted, single endpoint for KPIs + all charts), `_get_kpis()`:L118, `_sum_gl()`:L29, `_sum_gl_multi()`:L47, `_balance_gl()`:L67, `_balance_gl_cash()`:L85, `_calc_delta()`:L103, `_get_prev_period()`:L110
- `dashboard_charts.py` → 8 chart data functions (376 lines): `get_revenue_expense_chart()`:L164, `get_cash_timeline()`:L191, `get_ar_donut()`:L212, `get_ap_donut()`:L232, `get_revenue_by_item_group()`:L252, `get_expense_by_type()`:L275, `get_top_customers_revenue()`:L312, `get_ar_aging()`:L341; period builder `_build_periods()`:L104 (week/month/quarter/year); top-N donut `_top_n_donut()`:L83
- `forecast.py` → `get_forecast_data()`:L13 (whitelisted, main endpoint — calls aggregator, returns entries + opening balance GL TK 111+112+113 + metadata), `get_forecast_chart()`:L64 (whitelisted, committed-only entries grouped by month for Dashboard v2), `_group_by_month()`:L104 (period grouping with rolling balance)

## `vn_accounting/chart_of_accounts/`

- `coa_registry.py` → `_load_vn_templates()`:L17 (lazy load + cache JSON), `get_charts_for_country()`:L36 (whitelisted override — adds VN templates when country=Vietnam), `get_chart()`:L53 (monkey-patched in __init__.py — returns VN tree or falls back to original)
- `vn_large_enterprise.json` → TT99/2025 COA tree for large DN (TK 621/622/627 manufacturing cost tiers)
- `vn_small_enterprise.json` → TT99/2025 COA tree for small DN (merged cost accounts)
- `vn_large_enterprise.csv`, `vn_small_enterprise.csv` → same COA data in CSV form (reference for accountants)

## `vn_accounting/setup/`

- `company_defaults.py` → `set_vn_defaults(doc, method)`:L8 (Company.on_update): guards by country + first-time flag, detects template variant by presence of TK 621, calls `_get_defaults_large()`:L48 / `_get_defaults_small()`:L66, assigns cash/bank/AR/AP/revenue/COGS/VAT-in/VAT-out/depreciation/stock_adjustment/payroll_payable via `db_set`

## `vn_accounting/treasury/`

- `interest_calculator.py` → `build_interest_schedule()`:L12 (dispatcher), `_build_end_of_term()`:L51, `_build_periodic()`:L59, `_build_prepaid()`:L83, `_build_compound()`:L91, `calculate_accrued_interest()`:L117, `calculate_early_settlement_interest()`:L127
- `repayment_calculator.py` → `build_repayment_schedule()`:L12 (dispatcher), `_build_interest_only()`:L44, `_build_emi()`:L80
- `journal_entry_builder.py` → `create_deposit_je()`:L35, `create_interest_je()`:L62, `create_settlement_je()`:L85, `create_disbursement_je()`:L140, `create_repayment_je()`:L153, `create_deposit_accrual_je()`:L179 (VAS dự thu), `create_loan_accrual_je()`:L191 (VAS dự chi), `create_loan_settlement_je()`:L203; internals `_get_bank_gl_account()`:L10, `_create_je()`:L15
- `je_hooks.py` → `on_je_submit()`:L7 / `on_je_cancel()`:L13 — updates linked Term Deposit Interest / Bank Loan Repayment row status (Booked / Draft Created); refs `_update_linked_rows()`:L17 and `_update_cash_count_on_je()` for Cash Count integration
- `scheduled.py` → `process_treasury_schedules()`:L10 (daily): `_process_deposit_interest()`, `_process_loan_repayments()`, `_check_deposit_maturity()`, `_check_loan_maturity()`, `_send_maturity_alerts()`
- `test_interest_calculator.py`, `test_repayment_calculator.py` → pytest unit tests for calculators

## `vn_accounting/forecast/` — Cash Flow Forecast providers + aggregator (1,199 lines Python)

- `aggregator.py` (91 lines) → `get_all_forecast_entries()`:L59 (discovers providers via `frappe.get_hooks("cash_flow_forecast_providers")`, calls each, validates, isolates errors), `validate_entry()`:L15 (schema check: 7 required fields, amount>0, direction in/out, confidence 4-tier, date format)
- `erpnext_providers.py` (247 lines) → 5 ERPNext pipeline providers:
  - `get_quotation_forecast()`:L13 — open Quotations, confidence=possible, amount=grand_total
  - `get_sales_order_forecast()`:L51 — SO per_billed<100, confidence=probable, amount=unbilled portion
  - `get_purchase_order_forecast()`:L98 — PO per_billed<100, confidence=probable, schedule_date+30
  - `get_unpaid_si_forecast()`:L145 — SI outstanding>0, confidence=committed/overdue, applies payment delay
  - `get_unpaid_pi_forecast()`:L194 — PI outstanding>0, confidence=committed/overdue
  - `_get_payment_schedule_date()`:L239 — helper for SO/PO first unpaid schedule row
- `treasury.py` (153 lines) → `get_treasury_forecast()`:L12 (dispatcher), `_get_term_deposit_entries()`:L25 (active deposits → interest + principal inflows), `_deposit_cash_flows()`:L43 (per-deposit schedule rows), `_get_bank_loan_entries()`:L78 (active loans → repayment outflows), `_loan_cash_flows()`:L97 (per-loan schedule rows with monthly/quarterly/annual frequency)
- `payment_delay.py` (72 lines) → `get_payment_delay()`:L11 (SQL: median(PE.posting_date − SI.due_date) per customer, 12-month window), `get_payment_delay_cached()`:L46 (in-memory cache per request), `adjust_expected_date()`:L60 (shifts date forward by delay days), `clear_delay_cache()`:L54
- `payroll_provider.py` (158 lines) → `get_payroll_forecast()`:L17 (auto-detect HRMS: Payroll Entry → probable, fallback GL TK 334 → possible), `get_insurance_forecast()`:L32 (GL TK 3383+3384+3386, due 20th), `_from_payroll_entry()`:L43, `_from_gl_salary()`:L62, `_from_gl_insurance()`:L83, `_project_salary()`:L105 (monthly projection, 5th of month), `_project_insurance()`:L130
- `tax_provider.py` (160 lines) → `get_tax_forecast()`:L12 (dispatcher for 3 tax types), `_get_monthly_median()`:L26 (GL median helper), `_project_vat()`:L48 (TK 33311, monthly, due 20th of following month), `_project_cit()`:L81 (TK 3334, quarterly — Jan 30 / Apr 30 / Jul 30 / Oct 30), `_project_pit()`:L130 (TK 3335, monthly, due 20th)
- `historical_projection.py` (125 lines) → `get_opex_forecast()`:L12 (GL TK 6xx excluding payroll, 12-month analysis, recurring ≥8/12 months threshold, same-month-last-year with median fallback, cap 2× median), `_project_account()`:L85 (per-account monthly projection)
- `revenue_projection.py` (123 lines) → `get_revenue_forecast()`:L13 (GL TK 5xx, 12-month analysis, same-month-last-year), `_project_revenue()`:L83 (per-account projection)
- `test_aggregator.py` (70 lines) → `TestValidateEntry`:L5 — pytest: valid/invalid entry, negative/zero/missing fields, date format, direction/confidence validation

## `vn_accounting/landed_cost/` — Landed Cost Voucher automation

- `lcv_hooks.py` (101 lines) → `lcv_apply_default_expense_account(doc, method)`:L24 (before_validate: fills missing `expense_account` on LCV charge rows from `LCV Allocation Settings`; skips rows already set by KTT), `lcv_validate_import_vat_split(doc, method)`:L55 (validate: for import LCVs, checks deductible + non-deductible import VAT split is consistent); `_IMPORT_ONLY_KEYS`:L13 (set of expense_type keys hidden on domestic LCV)
- `seed.py` (109 lines) → `seed_lcv_allocation_settings()` (idempotent: seeds `LCV Allocation Settings` with TT99/2025 defaults: 6411 domestic freight, customs split for import, VAT NK accounts 1331/6411 non-deductible)

### `landed_cost/` tests

- *(no standalone tests in this sub-package — covered by `tests/test_no_hardcoded_accounts.py` regression gate)*

## `vn_accounting/costing/` — Manufacturing Costing

- `seed.py` (61 lines) → `seed_manufacturing_costing_settings()` (idempotent: sets TK 621/622/627 defaults on `Manufacturing Costing Settings` for VN large enterprise COA; skips if any account already configured)

### `costing/tests/`

- `test_unit_cost_calculation.py` → unit: cost-per-unit formula with mixed allocation methods
- `test_wip_valuation_methods.py` → unit: WIP valuation (FIFO vs weighted average) boundary cases
- `test_costing_branching.py` → unit: branching scenarios when overhead account empty or partial period

## `vn_accounting/period_closing/` — Period Closing Wizard

- `wizard_api.py` (192 lines) → `check_fiscal_year_end(company, period_end)`:L7 (whitelisted: True when period_end = fiscal year end), `get_closing_preview(company, period_end, include_821)`:L25 (whitelisted: builds 3-JE preview list without inserting), `create_closing_journal_entries(company, period_end, include_821)`:L77 (whitelisted: materializes 3 draft JEs), `_get_period_closing_settings(company)`:L110 (reads `VN Accounting Settings`; COA fallback lookup for TK 911/4212), `_get_revenue_balances()`:L145 (GL TK 5%%), `_get_expense_balances()`:L167 (GL TK 6%%, optionally 821%%)
- `pcv_hooks.py` (39 lines) → `pcv_validate_vn_requirements(doc, method)`:L1 (Period Closing Voucher validate: requires `vn_lock_unlock_reason` + Accounts Manager role), `pcv_on_submit(doc, method)`:L15 (writes immutable Comment with reason + user)
- `seed.py` → *(minimal — TK 911/4212 seeded via VN Accounting Settings; period closing seeds are COA-dependent)*

### `period_closing/` tests

- `test_fiscal_year_detection.py` → unit: `check_fiscal_year_end` calendar logic (year-end / mid-period / leap year)
- `test_pcv_validation.py` → unit: `pcv_validate_vn_requirements` role + reason validation

## `vn_accounting/financial_reporting/` — BCTC Reports + B09

- `resolver.py` (196 lines) → `resolve_bctc_line(company, line, period_start, period_end, resolved_cache)`:L8 (evaluates one BCTC Line: dispatches by `value_type` to account GL queries or `line_formula` arithmetic), `resolve_all_lines(company, lines, period_start, period_end)`:L173 (evaluates full line list in dependency order, returns `dict[code → Decimal]`), `_parse_account_formula(formula)`:L56 (+/-/= prefix TK pattern parser), `_query_gl_balance()`:L81, `_balance_as_of()`:L97 (closing balance side), `_period_movement()`:L122 (debit/credit movement during period), `_resolve_line_formula()`:L146 (arithmetic: `=code1+code2-code3`)
- `bctc_mapping_lifecycle.py` (57 lines) → `ensure_bctc_mapping_for_company(doc, method)`:L6 (Company.after_insert: skips non-VN; auto-creates BCTC Mapping from template), `_detect_coa_template(company)`:L19 (checks TK 621/622/627 presence → `vn_large_enterprise` or `vn_small_enterprise`), `_clone_template_to_company(company, coa_template)`:L41 (inserts BCTC Mapping with B01/B02/B03 child rows cloned from templates)
- `b09_generator.py` (390 lines) → `generate_b09(company, fiscal_year)`:L32 (main entry: builds 8-sheet openpyxl workbook — Vận xuôi, AR detail, AP detail, Asset movement, Inventory, Equity + style init), `_build_van_xuoi_sheet()`:L111 (opening + closing + movement per BCTC line), `_build_ar_detail_sheet()`:L191, `_build_ap_detail_sheet()`:L204, `_build_asset_movement_sheet()`:L216, `_build_inventory_sheet()`:L224, `_build_equity_sheet()`:L231; data fetchers `_get_ar_detail()`:L240, `_get_ap_detail()`:L272, `_get_asset_movement()`:L299, `_get_inventory_summary()`:L331, `_get_equity_movement()`:L361
- `bctc_template_seed.py` → seeds `BCTC Mapping Template` records for `vn_large_enterprise` + `vn_small_enterprise` × B01/B02/B03 with TT99/2025 line codes and formulas
- `test_bctc_resolver.py` → 40 pytest tests: formula parsing, GL query mocks, line formula arithmetic, resolve_all_lines dependency order, B01 balance equation (mã_270 = mã_440)

## `vn_accounting/print_format/`

- `cash_count_report/cash_count_report.html` → Mẫu 08a biên bản kiểm kê quỹ tiền mặt (Jinja)
- `cash_count_report/cash_count_report.json` → Print Format DocType record (shipped as fixture via hooks.py)

## `vn_accounting/translations/`

- `vi.csv` → 222-line English → Vietnamese dictionary (covers all DocType labels, Select options, form descriptions, error messages, JS button text); Frappe auto-loads via native translation cache

## `vn_accounting/workspace_sidebar/`

- `vn_accounting.json` → "VN Accounting" sidebar fixture with 40+ navigation items grouped by section; uses DocType + `route_options` pattern for sticky sidebar (see sidebar_route_options.bundle.js IIFE 1)

## `vn_accounting/public/js/`

- `sidebar_route_options.bundle.js` (460 lines) → **3 monkey-patches in sequence**:
  - IIFE 1: patch `frappe.ui.sidebar_item.TypeLink.prototype.get_path` to encode `route_options` as query string
  - IIFE 2: accordion auto-expand/collapse with localStorage persistence + `is_route_in_sidebar()` scoring patch for same-DocType items
  - IIFE 3: `frappe.ui.Sidebar.prototype.set_workspace_sidebar` 3-tier selection (localStorage → `frappe.boot.workspace_defaults` → Frappe default)
- `dashboard_charts.bundle.js` (58 lines) → Chart.js plugin registration + VN-locale number/date formatters used by `vn_accounting_dashboard.js`

## `vn_accounting/public/css/`

- `vn_accounting.bundle.css` → theme overrides for sidebar, workspace number cards, dashboard page (77 lines)

---

## `vn_accounting/vn_accounting/` (Frappe module dir)

### top-level

- `__init__.py` → empty module init
- `number_card_methods.py` → 5 whitelisted aggregators for standard Number Cards: `get_total_revenue()`:L36, `get_total_expenses()`:L56, `get_accounts_receivable()`:L79, `get_accounts_payable()`:L97, `get_cash_balance()`:L115; helper `_get_fiscal_year_dates()`:L18
- `report_utils.py` → shared report helpers + prefix constants (CASH_PREFIX=111, BANK_PREFIX=112, REVENUE_PREFIX=511, AR_PREFIX=131, AP_PREFIX=331, EXPENSE_PREFIXES=[621,622,627,641,642]): `extract_account_numbers()`:L24, `get_accounts_by_prefix()`:L45, `get_opening_balance()`:L86, `get_transactions()`:L104

### `doctype/`

- `cash_count/cash_count.py` → 203 lines: `validate()`, `on_submit()` posts 2-step VAS JE (1381/3381 initial + 1388/711 resolution), `before_print()` computes print context, `make_diff_je()`, denomination totals
- `cash_count/cash_count.js` → client script: live denomination totals, actual vs book diff, print
- `cash_count/cash_count.json` → schema
- `cash_count_denomination/cash_count_denomination.py` → child table controller (8 lines, validate only)
- `term_deposit/term_deposit.py` → 127 lines: `validate()`, `on_submit()` posts deposit JE + generates interest schedule via `build_interest_schedule()`, `on_cancel()`, rollover handler
- `term_deposit/term_deposit.js` → setup buttons (Settle Early, Rollover), schedule preview
- `term_deposit_interest/term_deposit_interest.py` → child table stub (8 lines)
- `bank_loan/bank_loan.py` → 134 lines: `validate()`, `on_submit()` posts disbursement JE + generates repayment schedule via `build_repayment_schedule()`, `on_cancel()`, settlement handler, outstanding balance recomputation
- `bank_loan/bank_loan.js` → setup buttons, schedule preview
- `bank_loan_repayment/bank_loan_repayment.py` → child table stub
- `vn_accounting_settings/vn_accounting_settings.py` → Single DocType controller (9 lines) — defaults for TK 1281 / 515 / 3411 / 635 / 242 / 335, seeded in `install._seed_treasury_settings()`
- `vn_accounting_settings/vn_accounting_settings.json` → schema
- `lcv_allocation_settings/` → Single — LCV expense type → account mapping; `is_import_lcv` flag; child table `lcv_expense_type_setting` (expense_type, expense_account, is_import_only)
- `manufacturing_costing_settings/` → Single — TK 621/622/627 account fields + cost allocation method Select (Tỷ lệ nguyên vật liệu / Giờ lao động trực tiếp / Chi phí lao động trực tiếp)
- `work_in_progress_valuation/` → Submittable — period_start, period_end, company; child rows per cost element (direct_material, direct_labor, overhead) with GL account source and amount; WIP snapshot for period-end reporting
- `bctc_mapping/` → Per-company BCTC Mapping — company, coa_template; child tables `b01_lines`/`b02_lines`/`b03_lines` of type `BCTC Line`; auto-created by `bctc_mapping_lifecycle.ensure_bctc_mapping_for_company`
- `bctc_line/` → Child table — code, description, account_formula (e.g. `+111+112`), line_formula (e.g. `=10-11`), value_type (closing_debit/closing_credit/period_debit/period_credit/formula)
- `bctc_mapping_template/` → Master — pre-defined mapping rows per COA template; cloned to per-company BCTC Mapping on Company creation

### `report/` (all Script Reports)

- `trial_balance_sheet/` → `trial_balance_sheet.py` + `.js`: opening + period + closing debit/credit per account (Bảng cân đối số phát sinh)
- `account_detail_ledger/` → per-account GL with running balance, party filter (Sổ chi tiết tài khoản)
- `cash_book/` → all TK 111% accounts (Sổ quỹ tiền mặt); exports `validate_filters()` imported by cash_receipts/cash_payments
- `bank_account_book/` → all TK 112% accounts (Sổ tiền gửi ngân hàng); exports `validate_filters()` for bank_receipts/bank_payments
- `cash_receipts/` → cash debit transactions only (Phiếu thu tiền mặt)
- `cash_payments/` → cash credit transactions only (Phiếu chi tiền mặt)
- `bank_receipts/` → bank debit transactions only
- `bank_payments/` → bank credit transactions only
- `internal_transfer/` → vouchers with both debit and credit sides in cash/bank accounts (Chuyển khoản nội bộ)

### `number_card/` (standard, synced via install._sync_standard_docs)

- `ton_quy/` → Cash Balance (TK 111+112) — backed by `number_card_methods.get_cash_balance`
- `tong_doanh_thu/` → Total Revenue (TK 511)
- `tong_chi_phi/` → Total Expenses (TK 621-642)
- `cong_no_phai_thu/` → AR (TK 131)
- `cong_no_phai_tra/` → AP (TK 331)

### `dashboard_chart/` (standard, synced via install._sync_standard_docs)

- `doanh_thu_chi_phi_thang/` → Revenue vs Expenses monthly timeline (Count/Sum chart)
- `bien_dong_tien/` → Cash flow timeline (Custom source: cash_balance_timeline)
- `cong_no_phai_thu/` → AR aggregate (aggregate_function_based_on=outstanding_amount)
- `cong_no_phai_tra/` → AP aggregate (outstanding_amount)

### `dashboard_chart_source/` (Custom chart sources)

- `cash_balance_timeline/cash_balance_timeline.py` → `get()`: combines TK 111+112 into a single line chart; whitelisted + `@cache_source`
- `revenue_expense_monthly/revenue_expense_monthly.py` → `get()`: 2-line chart (revenue vs expenses per month) used by Desk dashboard

### `page/`

- `vn_accounting_dashboard/` → Dashboard v2:
  - `vn_accounting_dashboard.js` (291 lines): `VNADashboard` class — granularity map (Tuần/Tháng/Quý/Năm), date range builder, `refresh()` calls `api.dashboard.get_dashboard`, renders 5 KPI cards + 8 Chart.js charts, locale-aware formatting
  - `vn_accounting_dashboard.html` (empty — JS-driven)
  - `vn_accounting_dashboard.css` (104 lines): grid layout, KPI cards, chart containers
  - `vn_accounting_dashboard.json`: Page DocType record (roles: Accounts User/Manager)
- `cash_flow_forecast/` → Cash Flow Forecast Page:
  - `cash_flow_forecast.js` (508 lines): `CashFlowForecast` class — Company/Period/GroupBy filters, 4 confidence toggles (overdue/committed/probable/possible) with bilingual tooltips, per-source inflow/outflow toggles, 4 summary cards (total inflow/outflow/net/closing), Chart.js bar+line (green inflow bars, red outflow bars, blue dashed closing balance line, orange threshold line), drill-down table (period summary rows with color coding + expandable detail rows with source links), CSV export (2-sheet: Summary+Detail), Y-axis VN abbreviation (tỷ/tr/ng), methodology panel
  - `cash_flow_forecast.css` (222 lines): responsive grid, confidence badges, toggle styling, table colors
  - `cash_flow_forecast.json`: Page DocType record (roles: Accounts User, Accounts Manager, System Manager)
- `under_development/` → Placeholder page for planned features (icon: construction); target of sidebar items for Cash Count print etc. when work is WIP

### `workspace/`

- `vn_accounting/vn_accounting.json` → "Ke Toan VN" Workspace record: 5 number cards + 4 charts + 17 shortcuts organized in 6 sections (Tiền mặt / Ngân hàng / Công nợ / Doanh thu - chi phí / Báo cáo / Thiết lập)
