# vn_accounting — Codebase Summary

**Lines of code:** ~15,800 (Python: 7,100 | JS: 2,030 | JSON: 5,200 | CSS: 407 | HTML: 296) — excluding docs/tests/__pycache__

## Overview

Vietnamese accounting localization for ERPNext v16 per Thông tư 99/2025/TT-BTC. Ships 2 COA templates (large & small enterprise), Company defaults auto-mapper, 12 script reports (Trial Balance, Account Detail Ledger, Cash/Bank Books, Receipts/Payments, Internal Transfer, **S03a-DN Sổ Nhật ký chung**, **S03b-DN Sổ Cái**, B01-DN, B02-DN, B03-DN), a custom Dashboard Page (5 KPIs + 8 charts), 4 DocTypes for Cash Count + Treasury (Term Deposit, Bank Loan), Cash Flow Forecast Page, Workspace + sidebar navigation, daily scheduled job for treasury operations. Phase 5 additions: Landed Cost (LCV) auto-fill for domestic + import LCVs, Period Closing custom hooks (vn_lock_unlock_reason audit), and Financial Reporting engine (BCTC resolver with 10 value_types: closing/period/net/delta, fixpoint formula resolution; 2 templates `vn_large_enterprise` and `vn_small_trade`; B09-DN multi-sheet Excel generator).

**Rebuilt 2026-05-11:** Dropped manufacturing scope (costing/, WIP Valuation, mfg-costing-wizard, production-cost-aggregation) to focus app on thương mại + dịch vụ DN. Sidebar now 15 items / 3 sections (Giá thành / Tổng hợp / BCTC); section "Phân tích & Quản trị" removed (4 native ERPNext reports accessible via search bar).

## Stack

Frappe v16 + ERPNext v16 + HRMS v16. Python 3.10+. Required apps: `frappe`, `erpnext`.

## Directory tree (L-2)

```
vn_accounting/                          # repo root
├── README.md
├── FEATURES.md                         # Done/In-Progress/Planned matrix
├── pyproject.toml
├── docs/                               # specs, business logic, CODEBASE, vn_accounting_features_handover (Tài liệu bàn giao)
├── tests/                              # pytest: test_coa, test_company_defaults, test_report_utils
└── vn_accounting/                      # inner package (pip install target)
    ├── __init__.py                     # __version__, _patch_get_chart() monkey-patch
    ├── hooks.py                        # app config entry point
    ├── boot.py                         # boot_session injects workspace_defaults
    ├── install.py                      # after_install/after_migrate — sync docs, seed, fix labels
    ├── modules.txt / patches.txt       # required Frappe metadata
    ├── api/                            # whitelisted endpoints (dashboard.py, dashboard_charts.py, forecast.py)
    ├── chart_of_accounts/              # VN COA JSON + CSV + coa_registry.py override
    ├── misa_migration/                 # Misa SME → ERPNext pipeline (Phase A-E, 5-phase orchestrator)
    │   ├── parsers/                    # NKC, bảng kê, opening balance parsers (9 file types)
    │   ├── importers/                  # phase_4_orchestrator (insert + submit_phase_4_drafts), nkc_handlers/, ob_handlers/
    │   ├── bulk_pump/                  # SQL-INSERT alt to ORM submit (10-15x faster, archival use)
    │   │   ├── orchestrator.py         # run_bulk_pump_full + auto-stamp cost_center + auto-run backfill_audit_fixes
    │   │   ├── bulk_executor.py        # group-by-keyset bulk INSERT (NOT NULL safe)
    │   │   ├── account_resolver.py     # Misa TK → Frappe Account.name (descendant-prefix fallback)
    │   │   ├── builders/               # per-DocType SQL row builders (SI/PI/PE/JE/SE/Asset/OB/masters)
    │   │   ├── backfill_audit_fixes.py # 15-step idempotent backfill (party case, SE GL, PI 1331, year-end close)
    │   │   ├── coa_bootstrap.py        # whitelisted API: install VAS CoA on fresh Company
    │   │   ├── account_conflicts.py    # whitelisted API: list/rename Account name conflicts (Misa vs Frappe)
    │   │   └── post_derive.py          # PE→SI/PI ref backfill, Bin/PLE rebuild
    │   ├── scripts/                    # post-bulk_pump audit + repost + validation pipeline (9 scripts, 100% match)
    │   │   ├── derive_masters_from_batch.py    # auto-discover masters from NKC+BR+MV content
    │   │   ├── audit_source_data_gaps.py       # 8-category source quality check
    │   │   ├── validate_closing_balance.py     # DB vs Bang_can_doi + Tong_hop_ton_kho compare
    │   │   ├── repost_si_gl_from_nkc.py        # SI revenue Cr split per Misa NKC
    │   │   ├── repost_pe_gl_from_nkc.py        # preserve multi-leg PE (1 UNC → N TKs)
    │   │   ├── repost_pi_gl_from_nkc.py        # PI 6xx vs 242 vs 1331 split + no-331 case
    │   │   ├── repost_pn_stock_to_payable.py   # SE GL re-route to Cr 331
    │   │   ├── backfill_missing_ob_bins.py     # recover missing OB Inventory Bins
    │   │   └── snap_bin_to_source_cb.py        # final Bin reconciliation (archival only)
    │   ├── setup/coa_leaves.py         # bootstrap 18 Misa level-5 leaves under level-4 groups
    │   ├── setup/company_defaults.py   # ensure_company_defaults_for_misa + ensure_party_accounts_for_misa
    │   ├── context.py                  # multi-Company override via frappe.local.flags
    │   ├── docs/screenshots/           # Phase E9 Vue UI tour PNGs + 20-e2e-100pct-success
    │   └── tests/                      # 380 unit tests covering all phases
    ├── setup/                          # company_defaults.py — Company on_update VN mapping
    ├── treasury/                       # Term Deposit + Bank Loan logic (calc, JE builder, JE hooks, scheduled)
    ├── forecast/                       # Cash Flow Forecast: aggregator, 11 providers, payment delay
    ├── landed_cost/                    # LCV hooks (auto-fill expense accounts, import VAT split) + seed
    ├── period_closing/                 # PCV hooks (vn_lock_unlock_reason validation + audit comment) + seed
    ├── financial_reporting/            # BCTC resolver, B09-DN Excel generator, BCTC lifecycle + seed
    ├── print_format/                   # Cash Count Report HTML
    ├── translations/vi.csv             # 222-line English → Vietnamese dictionary
    ├── workspace_sidebar/              # sidebar navigation fixture (40+ items)
    ├── public/js/                      # sidebar_route_options.bundle.js, dashboard_charts.bundle.js
    ├── public/css/                     # vn_accounting.bundle.css
    └── vn_accounting/                  # Frappe module dir (doctypes, reports, charts, cards, pages, workspace)
        ├── doctype/                    # 17 DocTypes
        ├── report/                     # 10 script reports (incl. Misa Account Conflicts review UI)
        ├── number_card/                # 5 standard number cards
        ├── dashboard_chart/            # 4 standard dashboard charts
        ├── dashboard_chart_source/     # cash_balance_timeline, revenue_expense_monthly
        ├── page/                       # vn_accounting_dashboard, cash_flow_forecast, under_development
        ├── workspace/                  # ke_toan_vn.json
        ├── number_card_methods.py      # 5 whitelisted aggregators
        └── report_utils.py             # shared helpers + prefix constants
```

## Data model

### DocTypes (in this app)

| DocType | Purpose |
|---------|---------|
| Cash Count | Periodic/ad-hoc cash count (Mẫu 08a), 2-step VAS diff posting, print |
| Cash Count Denomination | Child table — physical count by denomination |
| Term Deposit | TK 1281 time deposit — interest schedule, rollover, settlement |
| Term Deposit Interest | Child table — per-period interest rows w/ JE link + status |
| Bank Loan | TK 3411 loan — disbursement, repayment schedule, maturity |
| Bank Loan Repayment | Child table — principal+interest rows w/ JE link + status |
| VN Accounting Settings | Single — default accounts for treasury posting (1281 / 515 / 3411 / 635 / 242 / 335) + Permission Matrix for TSCĐ/CCDC |
| CCDC Item | Công cụ dụng cụ — life cycle: Mới mua → Đang sử dụng → Hết phân bổ → Đã ghi giảm; submittable; JE N242/C153 on submit |
| CCDC Category | Master — category_name, expense_account_default (627/641/642), useful_period_default |
| CCDC Allocation Schedule | Auto-created on CCDC Item submit; N child entries (cost/N each); scheduler posts JE N expense/C242 per period |
| CCDC Allocation Entry | Child — period_no, period_start_date, allocation_amount, journal_entry, status (Pending/Posted) |
| CCDC Writeoff | Submittable — clears remaining TK 242 + TK 153; cancels pending allocation entries |
| Asset Handover | Bàn giao TSCĐ/CCDC — scope (TSCĐ/CCDC), updates Asset.location/custodian on submit; creates Asset Movement for TSCĐ; on_cancel reverts from snapshot |
| Asset Handover Item | Child — target_doctype (Asset or CCDC Item), target_name (Dynamic Link), book_value |
| Asset Stocktake | Kiểm kê tài sản — load_items() from location/department; approve() creates JE 1381/211 for Mất items |
| Asset Stocktake Item | Child — target_doctype, target_name, book_value, physical_status (Còn nguyên/Hỏng/Mất) |
| Asset Permission Rule | Child of VN Accounting Settings — role, doctype, perm_read/create/write/submit/cancel |
| LCV Allocation Settings | Single — maps LCV expense_type → expense_account; flags for import LCV (VAT NK split deductible/non-deductible) |
| LCV Expense Type Setting | Child table — expense_type, expense_account, is_import_only |
| Work In Progress Valuation | Submittable — records WIP snapshot per period: direct material/labor/overhead with account sources |
| Manufacturing Costing Settings | Single — TK 621/622/627 direct material/labor/overhead account defaults |
| BCTC Mapping | Per-company — holds B01/B02/B03 line mapping tables; auto-created on Company insert (Vietnam); cloned from BCTC Mapping Template |
| BCTC Line | Child table — code, description, account_formula (+111, =10-11 syntax), line_formula, value_type |
| BCTC Mapping Template | Master — one template per COA variant (vn_large_enterprise / vn_small_enterprise) × report (b01/b02/b03) |

### Reports, Cards, Charts (standard JSON, upserted on install/migrate)

- **Number Cards (5):** Tồn Quỹ (111+112), Tổng Doanh Thu (511), Tổng Chi Phí (621-642), Công Nợ Phải Thu (131), Công Nợ Phải Trả (331) — all backed by `number_card_methods.py`
- **Dashboard Charts (4):** Doanh Thu Chi Phí Tháng, Biến Động Tiền, Công Nợ Phải Thu, Công Nợ Phải Trả
- **Script Reports (11):** Trial Balance Sheet, Account Detail Ledger, Cash Book, Bank Account Book, Cash Receipts, Cash Payments, Bank Receipts, Bank Payments, Internal Transfer, **Bao Cao Chi Phi Khong Duoc Tru** (TNDN B4 aggregation), **Quyet Toan TNDN Reconciliation** (Form 03/TNDN structure)
- **Non-Deductible Custom Fields (11)** on JE Account / GL Entry / PI Item / EC Detail / Asset / Salary Component — backed by `non_deductible/helper.py` + `je_hooks.py` (validate + JE→GL propagation) + `source_hooks.py` (PI/EC/Salary Slip propagation)

## Entry points

- **`hooks.py`** — `override_whitelisted_methods` (get_charts_for_country), `doc_events.Company.on_update` (set_vn_defaults), `doc_events.Company.after_insert` (auto-create BCTC Mapping), `doc_events.Journal Entry.on_submit/on_cancel` (treasury schedule sync), `doc_events.Landed Cost Voucher.before_validate/validate` (LCV expense account auto-fill + import VAT split), `doc_events.Period Closing Voucher.validate/on_submit` (VN PCV validation + audit log), `boot_session` (workspace defaults), `after_install`/`after_migrate` (sync JSON + desktop icon + seed treasury/LCV/costing settings), `scheduler_events.daily` (treasury JE drafts + maturity alerts), `cash_flow_forecast_providers` (11 provider registrations), `app_include_js`/`app_include_css`, Print Format fixture
- **Dashboard API** — `vn_accounting.api.dashboard.get_dashboard()` single endpoint returning KPIs + 8 charts; chart functions in `dashboard_charts.py`; granularity-aware period builder
- **Forecast API** — `vn_accounting.api.forecast.get_forecast_data()` (all entries + opening balance + metadata), `get_forecast_chart()` (committed-only for Dashboard v2 chart); aggregator in `forecast/aggregator.py` discovers providers via hooks
- **Number Card methods** — `vn_accounting.vn_accounting.number_card_methods.get_*()` × 5 whitelisted
- **Chart Source methods** — `cash_balance_timeline.get()` and `revenue_expense_monthly.get()` (whitelisted, `@cache_source`)
- **JS bundles** — `sidebar_route_options.bundle.js` (3 monkey-patches: route_options, accordion, 3-tier sidebar persistence), `dashboard_charts.bundle.js` (Chart.js plugins)
- **Workspace fixtures** — `workspace/ke_toan_vn/ke_toan_vn.json` (5 cards + 4 charts + shortcuts), `workspace_sidebar/vn_accounting.json` (40+ nav items with route_options)

## Core flows

1. **Company setup** — user creates Company with Country=Vietnam → ERPNext calls `get_charts_for_country()` (overridden) → VN templates offered → COA created via monkey-patched `get_chart()` → Company `on_update` fires `set_vn_defaults()` → TK 111/112/131/331/511/632/1331/33311/214/635/... assigned to Company default fields; treasury defaults seeded in `VN Accounting Settings`.
2. **Dashboard v2** — user opens `/desk/vn-accounting-dashboard` → JS picks granularity (Week/Month/Quarter/Year) → POST `api.dashboard.get_dashboard` → backend runs GL aggregations for 5 KPIs + 8 charts → Chart.js renders.
3. **Cash Count** — user enters denominations → controller computes actual total → diff vs book → on submit, posts 2-step VAS JE (1381/3381 holding → 1388/711 resolution) → Print Format Mẫu 08a.
4. **Treasury (Term Deposit / Bank Loan)** — user creates Term Deposit → `build_interest_schedule()` generates rows → daily scheduler creates draft JEs for due rows → on JE submit, `je_hooks` marks row as `Booked`; maturity alerts sent via scheduler.
5. **Cash Flow Forecast** — user opens `/desk/cash-flow-forecast` → JS calls `api.forecast.get_forecast_data(company, months)` → aggregator reads `cash_flow_forecast_providers` from hooks → calls 11 provider functions in sequence (each returns list of ForecastEntry dicts) → validates schema, isolates errors → returns entries + opening balance (GL TK 111+112+113) → JS groups by period, applies confidence/source toggles client-side, renders Chart.js bar+line + drill-down table with rolling balance and threshold warnings.
6. **Sidebar persistence** — login triggers `boot_session` → injects `workspace_defaults` (DocType → preferred sidebar map) → JS `sidebar_route_options.bundle.js` monkey-patches `frappe.ui.Sidebar.prototype.set_workspace_sidebar` with 3-tier selection (localStorage > boot defaults > Frappe default) → VN sidebar sticks across DocType navigation.
7. **Route-options on sidebar** — Frappe v16 sidebar drops `route_options` on DocType links; IIFE 1 in the bundle patches `get_path` to encode them as `?field=value` query params, then scores items by `cur_frm.doc` match to pick the right active highlight when multiple items target the same DocType.
8. **Landed Cost (LCV)** — user creates Landed Cost Voucher → `before_validate` hook (`lcv_hooks.lcv_apply_default_expense_account`) reads `LCV Allocation Settings`, fills missing `expense_account` per charge type; for import LCVs, `validate` hook checks VAT NK split is complete (deductible + non-deductible sum = gross import VAT). LCV Allocation Settings seeds TT99/2025 defaults (6411 domestic, 6411+1331 import VAT split) on first install.
9. **Period Closing wizard** — user calls `period_closing.wizard_api.get_closing_preview(company, period_end)` → returns 3 JE previews (kết chuyển doanh thu → TK 911, kết chuyển chi phí → TK 911, kết chuyển lãi/lỗ → TK 421); `create_closing_journal_entries()` materializes the 3 draft JEs. `pcv_hooks.pcv_validate_vn_requirements` gates Period Closing Voucher submit to Accounts Manager role + mandatory lock reason; `pcv_on_submit` writes immutable audit comment.
10. **BCTC Financial Reports** — Company `after_insert` triggers `bctc_mapping_lifecycle.ensure_bctc_mapping_for_company` → detects COA variant (large vs small enterprise by TK 621/622/627 presence) → clones template rows into per-company `BCTC Mapping`. Reports B01/B02/B03 call `financial_reporting.resolver.resolve_all_lines(company, lines, period_start, period_end)` → evaluates `account_formula` (+/- account code patterns) and `line_formula` (code arithmetic) from BCTC Mapping to produce line values. B09-DN Excel export: `b09_generator.generate_b09(company, fiscal_year)` builds 8-sheet openpyxl workbook (Vận xuôi + AR/AP detail + Asset movement + Inventory + Equity + B09 header).
11. **Project Costing (FB-00605, shipped 2026-05-16)** — KTT tạo Project Costing per Project + Stages markup theo 6 phương pháp. PI/SE/DN/EC submit với project tag → `wip_override_engine` JE bù 2-layer (Dr 154 override / Cr default). Pivot Tool Page (`project-costing-pivot`) vanilla JS để KTT pin chi phí từ Common Pool vào stage. Generate SI draft từ stage → SI submit triggers `cogs_engine` Dr 632 / Cr 154. Cost Allocation Run (manual end-of-month) phân bổ chi phí gián tiếp Dr 154 (per project) / Cr 627 với flexible Cr override (622 lương / 6424 khấu hao). `close_engine` validates 154 balance = 0 hoặc write-off Dr 642/632. JE re-classify helper button + Salary Slip hook tự sinh bù JE. Marker `[PROJECT_COSTING:<x>][TYPE:<X>]` cho 6 types: ALLOCATION_RUN / WIP_OVERRIDE / STAGE_COGS / CLOSE_WRITEOFF / JE_RECLASSIFY / SALARY_REALLOCATE. Embedded JE traceability section trên Project Costing form.
12. **Misa Migration Framework (Phase A shipped 2026-05-19)** — kế toán bấm sidebar 'Công cụ Import' → mở Frappe Page `/app/misa-migration-hub` (Vue 3 + Pinia SFC bundle) → 4-step stepper Upload / Phân tích / Duyệt / Đăng. Phase A ships only Upload step end-to-end: create Misa Migration Batch (8-state lifecycle via `status` field), upload Excel file via standard `/api/method/upload_file`, attach to Batch's child `Misa Migration File` table, transition DRAFT → UPLOADED via `state.transition()`. Per-company filelock (`frappe.utils.synchronization.filelock`) enforces 1 active batch / Company. 10 Custom Fields on SI/PI/PE/JE/SE/PR/Customer/Supplier/Employee/Item store original Misa code when ERPNext doc.name had to be renamed (spec §15.4). DocTypes: Misa Migration Batch (parent) / File (child) / Row (heap, autoname=hash) / Field Mapping (Single, column header map) / Account Mapping (Single, TK Misa → ERPNext Account map). Phase B (Reference + CoA importers) / C (Master) / D (Transactions) / E (Polish) deferred — `api/parse.py`/`review.py`/`post.py`/`undo.py` throw 'chưa triển khai' stubs.
13. **Non-Deductible Expense Tracking (Pattern A, shipped 2026-05-25)** — kế toán đánh dấu cờ `is_non_deductible` + chọn lý do (6 options) trên dòng chi phí thực phát sinh (JE Account / PI Item / EC Detail / Salary Component / Asset.is_welfare_asset). JE validate hook (`non_deductible.je_hooks.validate_non_deductible`) bắt buộc chọn lý do khi tick cờ. On submit, `propagate_to_gl_entry` mirror cờ từ JE Account → GL Entry (match by `voucher_no + account + debit + credit` tuple — `voucher_detail_no` không populate cho JE). Source-doc hooks (`source_hooks.py`) mirror cờ từ PI Item / EC Detail / Salary Component → GL Entry trên on_submit. dcnet_pakd `post_beneficiary_je` auto-tag DR row khi `recipient_tax_pct=0 AND no invoice_no`. Reports: "Bao Cao Chi Phi Khong Duoc Tru" (list flagged GL entries by reason, chart, summary B4 total) + "Quyet Toan TNDN Reconciliation" (Form 03/TNDN structure A doanh thu → B điều chỉnh với B4 autofill → C thu nhập chịu thuế → D thuế phải nộp + X1/X2/X3 phân tích tỷ lệ thuế hiệu lực = B09 giải trình). Help article in `help/bctc/tu-van-chi-phi-khong-duoc-tru.md` cho KTT. Spec: `docs/specs/2026-05-25-non-deductible-expense-tracking.md`. Legal basis: NĐ 320/2025/NĐ-CP Điều 9-10 + VAS 17.

## Read first (devs)

1. `docs/BUSINESS_LOGIC.md` — non-technical business rules (what the app must do and why)
2. `vn_accounting/hooks.py` — all extension points in one file
3. `vn_accounting/chart_of_accounts/coa_registry.py` + `vn_accounting/__init__.py` — COA override mechanism
4. `vn_accounting/setup/company_defaults.py` — VN account → Company default mapping logic
5. `vn_accounting/api/dashboard.py` + `vn_accounting/vn_accounting/page/vn_accounting_dashboard/vn_accounting_dashboard.js` — Dashboard v2
6. `vn_accounting/forecast/aggregator.py` + `vn_accounting/api/forecast.py` — Cash Flow Forecast provider system + API
7. `vn_accounting/public/js/sidebar_route_options.bundle.js` — 3 monkey-patches (route_options, accordion, sidebar persistence)
8. `vn_accounting/financial_reporting/resolver.py` — BCTC formula resolver (account_formula + line_formula engine)
9. `vn_accounting/period_closing/wizard_api.py` — period-closing 3-JE preview + creation wizard
10. `docs/CODEBASE_DETAIL.md` — file-by-file index with line numbers
