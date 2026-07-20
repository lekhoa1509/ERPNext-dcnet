# Task: Giá thành — Tổng hợp — Báo cáo tài chính (TT99/2025)

## Model

sonnet

## Wrap-up directive (read first every session)

**CRITICAL — write session-last BEFORE you run out of time.** Each session you MUST:
1. Track time via PostToolUse warnings (70% / 90%). When 70% warning fires, STOP coding and start writing session-last.
2. Commit current work first (`git add . && git commit -m "..."` — uncommitted work is lost if session killed).
3. Write `<project>/.multi-session/session-last-giathanh-tonghop-bctc.md` with:
   - **What done this session** — bullet list with file paths
   - **Verified evidence** for each acceptance criterion you claim done: paste actual `python -m unittest` output, actual `bench --site dcnet.localhost migrate` output, screenshot path for UI test
   - **Self-contained "Next Session Task"** — exact directory paths, exact files to read first, exact commands to verify state, exact next sub-task description
   - **Remaining acceptance criteria** — copy from this file with `[x]` for done, `[ ]` for not done
   - **Phase N status: ✅ DONE** or **🚧 IN PROGRESS** marker (runner uses this for phase progression)
   - **Learnings** (if any) — patterns discovered, mistakes to avoid next time

Do NOT let the runner extract session-last from transcript (`<!-- SESSION_LAST_EXTRACTED_FROM_TRANSCRIPT -->` marker = false-positive risk per multi-session rule #14). Always author session-last yourself with verified evidence.

## Context

vn_accounting sidebar có 3 sections rỗng / thiếu nghiệp vụ cốt lõi cho kế toán Việt Nam theo Thông tư 99/2025/TT-BTC (hiệu lực 2026-01-01):

- **Giá thành** — chưa có item nào. DN thương mại không có phân bổ chi phí mua hàng (vận chuyển, nhập khẩu, thuế NK) → giá vốn méo. DN sản xuất không có cơ chế tính giá thành.
- **Tổng hợp** — đã có Sổ chi tiết tài khoản (A2.2) + Bảng cân đối số phát sinh (A2.1) nhưng thiếu Sổ nhật ký chung (S03a-DN), Sổ cái (S03b-DN, format khác Sổ chi tiết), Kết chuyển cuối kỳ (911 → 421), Khóa sổ kỳ (Period Closing Voucher).
- **Báo cáo tài chính** — chưa có. 4 báo cáo bắt buộc theo TT99/2025 (B01/B02/B03/B09-DN) đều thiếu.

Đồng thời 2 cross-cutting rules áp dụng cho phase này + mọi feature tương lai:
1. **No hardcoded TK** — mọi định khoản/báo cáo phải hiện TK + cho phép kế toán override (Settings DocType pattern)
2. **UI inline guidance mandatory** — phần mềm mới, users chưa quen; mọi field/button/wizard/report phải có hướng dẫn inline

Implement per spec đã chốt với KTT review: `docs/specs/2026-05-11-giathanh-tonghop-bctc.md` (916 dòng, 21 decisions chốt, 8 self-review gaps đã fix).

## Scope

- **Project (= runner cwd):** `/home/long/long/frappe-bench-dcnet` (bench root — all verification commands relative to this)
- App being modified: `apps/vn_accounting`
- Branch: `feat/giathanh-tonghop-bctc` (create từ `apps/vn_accounting` main hiện tại)
- Test site: `dcnet.localhost`
- Test URL: `http://dcnet.localhost:8001`
- Design spec: `apps/vn_accounting/docs/specs/2026-05-11-giathanh-tonghop-bctc.md` — **read this first every session**
- Business logic: `apps/vn_accounting/docs/BUSINESS_LOGIC.md` §11–14
- Feature catalog: `apps/vn_accounting/FEATURES.md` §C7–C10
- Python interpreter: `env/bin/python` (relative to bench root; Frappe 16.x requires Python 3.14)

### Related files

| File | Purpose | Action |
|------|---------|--------|
| `docs/specs/2026-05-11-giathanh-tonghop-bctc.md` | Design source of truth | **Read FIRST every session** |
| `docs/BUSINESS_LOGIC.md` §11-14 | Business rules + edge cases | Reference for KTT-level questions |
| `FEATURES.md` §C7-C10 | Feature inventory | Update status as phases complete |
| `vn_accounting/vn_accounting/doctype/` | DocType directory (triple-nested per Frappe) | Create new DocTypes here |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/` | Extend existing settings | Add Period Closing accounts + LCV + Manufacturing fields |
| `vn_accounting/fixtures/` | Fixture JSON files | Add: BCTC templates (B01/B02/B03 × large/small COA), LCV expense types seed, Period Closing accounts seed, Custom Field + Property Setter, workspace_sidebar update |
| `vn_accounting/landed_cost/` | NEW sub-package | LCV hooks, defaults seed, Landed Cost Pending Allocation report |
| `vn_accounting/costing/` | NEW sub-package | Manufacturing costing wizard page, helpers, Project setup guide |
| `vn_accounting/period_closing/` | NEW sub-package | Wizard kết chuyển 911 page + helpers, PCV validation hooks |
| `vn_accounting/financial_reporting/` | NEW sub-package | BCTC resolver engine, 4 Script Reports, B09 Excel generator, Excel layout helpers |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Sidebar JSON | Add 13 new items into Giá thành/Tổng hợp/BCTC sections (per spec §5) |
| `vn_accounting/translations/vi.csv` | VN translations | Append ~140 entries (per spec §7) |
| `vn_accounting/setup/__init__.py` (or new install.py addition) | Install hooks | Seed 4 Settings + BCTC templates after_install + Company.on_update for per-Company BCTC Mapping |
| `vn_accounting/hooks.py` | App hooks | Register LCV before_validate/validate hooks + PCV validate/on_submit/on_cancel hooks |
| `vn_help/articles/` (apps/vn_help) | Help articles | Add 12 articles per spec §12.3 — tiếng Việt thuần, không nhắc ERPNext/Frappe |
| `tests/` | Test directory | Create 8 unit/integration test files per spec §8 |

## Requirements — 7 Phases (P0–P6)

### Phase 0: Implementation Plan + Branch Setup

**Outcome:** A detailed implementation plan committed to `docs/plans/2026-05-11-giathanh-tonghop-bctc-plan.md`. Branch `feat/giathanh-tonghop-bctc` created from main. Empty sub-packages scaffolded.

Steps:
1. Read **full spec** at `docs/specs/2026-05-11-giathanh-tonghop-bctc.md` (916 lines) + BUSINESS_LOGIC §11-14 + FEATURES §C7-C10.
2. Create branch `feat/giathanh-tonghop-bctc` from current `main` HEAD.
3. Scaffold empty sub-packages: `landed_cost/`, `costing/`, `period_closing/`, `financial_reporting/` (each with `__init__.py`).
4. Use the **superpowers:writing-plans** skill to write file-level implementation plan with exact code outlines for each unit (DocType JSON, controller methods, Settings extensions, fixtures, wizards, reports, sidebar items, translations, tests).
5. **Self-review** plan with 3-point checklist:
   - **Spec coverage** — every section of spec (§3 schema, §4 wizards/reports, §5 sidebar, §6 hooks, §7 i18n, §8 tests) maps to ≥1 plan task
   - **Placeholder scan** — no TBD/TODO except items in §10.8 (out-of-scope)
   - **Type consistency** — DocType names, field names, account roles consistent across plan tasks
6. **Self-fix** issues inline. Add "Self-Review Notes" section.
7. Commit plan + scaffold: `docs(giathanh): implementation plan from design spec`.

### Phase 1: Foundation — 4 Settings DocTypes + BCTC Template Seeding

**Outcome:** Site `dcnet.localhost` has 4 new Settings working: `LCV Allocation Settings` (with 12 expense types seeded), `Manufacturing Costing Settings` (with TT99/2025 defaults), `VN Accounting Settings` extended with Period Closing accounts (TK 911/4212/4211 + revenue/expense lists + corporate_income_tax_account separate), and `BCTC Mapping Template` seeded with B01/B02/B03 templates for both large + small COA. Company VN creation auto-clones BCTC Mapping. UI guidance complete on every field.

Sub-tasks:
1. **LCV Allocation Settings (Single DocType)** per spec §3.1:
   - Fields: `expense_types` table, `auto_apply_settings_on_new_lcv`, `import_vat_default_deductible_pct`
   - Child DocType `LCV Expense Type Setting` (per spec §3.1 child schema)
   - Seed 12 expense types via fixture (per spec §3.1 default table)
   - Each field has rich `description` per UI guidance §12 (vd: "TK trung gian phải nộp NSNN. Khi LCV submit, cơ chế bút toán: Nợ 156 / Có 3333. Khi DN nộp thuế: Nợ 3333 / Có 111. Sửa nếu DN tách chi tiết 33331, 33332.")
2. **Manufacturing Costing Settings (Single)** per spec §3.2:
   - All 11 fields including new `transfer_to_finished_goods` + `services_cogs_account`
   - Defaults via lookup helper (621/622/627/154/155/632 per Company COA)
   - Rich field descriptions; Section Break with help text
3. **Extend VN Accounting Settings** per spec §3.3:
   - Add fields: `pnl_account_911`, `retained_earnings_current_year`, `retained_earnings_prior_year`, `revenue_accounts_to_close` (Table), `expense_accounts_to_close_periodic` (Table, NO 821), `corporate_income_tax_account` (separate 821), `period_closing_balance_tolerance`
   - Child DocType `Account List Item` reusable
   - Section Break "Kết chuyển cuối kỳ" with description explaining periodic vs annual closure
   - `after_install` seed defaults
4. **BCTC Mapping (per-Company)** + **BCTC Mapping Template** (hidden DocType) per spec §3.4:
   - Both DocTypes with `b01_lines`, `b02_lines`, `b03_lines` Tables
   - Child DocType `BCTC Line` per spec child schema (with `code`, `value_type`, `account_formula`, `line_formula`, `display_indent`, etc.)
   - 2 buttons on BCTC Mapping form: "Copy mapping từ Company khác" + "Khôi phục mặc định TT99/2025" (per-line + per-report)
   - Fixture JSON: B01/B02/B03 templates seeded into Template DocType — 2 versions (large COA ~50/18/30 lines, small COA simpler)
   - `Company.on_update` hook: when country=Vietnam + no BCTC Mapping exists → auto-clone from Template (detect coa_template by checking presence of TK 621/622/627)
5. **`after_install` orchestration:** wire all 4 seeds in order — LCV → Manufacturing → Period Closing accounts → BCTC Templates → existing Company VN auto-clone
6. **Tests Phase 1:**
   - `test_settings_seed.py` — all 4 Settings populate correctly after install
   - `test_bctc_template_clone.py` — Company VN creation auto-clones, large vs small detection works
   - `test_doctype_field_descriptions.py` — all reqd=1 fields + Link/Select/Date/Currency fields have descriptions ≥10 chars (per spec §8.4)
7. **UI guidance audit:** run §12.4 checklist on the 4 Settings forms before commit

**Verification Commands:**
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/doctype/lcv_allocation_settings/lcv_allocation_settings.json`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/doctype/manufacturing_costing_settings/manufacturing_costing_settings.json`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/doctype/bctc_mapping/bctc_mapping.json`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/doctype/bctc_line/bctc_line.json`
- `test -f apps/vn_accounting/vn_accounting/fixtures/bctc_template_b01_large.json`
- `grep -q "corporate_income_tax_account" apps/vn_accounting/vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json`
- `grep -q "transfer_to_finished_goods" apps/vn_accounting/vn_accounting/vn_accounting/doctype/manufacturing_costing_settings/manufacturing_costing_settings.json`
- `env/bin/python -m py_compile apps/vn_accounting/vn_accounting/setup/__init__.py` (exit code 0 = compiles)

**Live Testing Procedure (run inside session, not in Verification Commands):**
1. `bench --site dcnet.localhost migrate` (cwd = bench root = project)
2. `bench restart` (per frappe-spa.md rule — Python module changes need restart)
3. `bench --site dcnet.localhost clear-cache`
4. Open `http://dcnet.localhost:8001/app/lcv-allocation-settings` — verify 12 expense types listed with descriptions
5. Open `http://dcnet.localhost:8001/app/manufacturing-costing-settings` — verify all defaults populated
6. Open `http://dcnet.localhost:8001/app/vn-accounting-settings` — verify new Period Closing section appears
7. Open `http://dcnet.localhost:8001/app/bctc-mapping` — verify mapping exists for existing test Company

### Phase 2: LCV — Phân bổ chi phí mua hàng (universal)

**Outcome:** Site `dcnet.localhost` allows creating Landed Cost Voucher with auto-filled expense accounts from Settings. Import LCV has toggle "Có chịu thuế NK?" + VAT split. Sidebar "Giá thành" section has 5 working items. Pending allocation report shows untied costs.

Sub-tasks:
1. **LCV hooks** per spec §6.3 + §3.1:
   - `before_validate` hook on Landed Cost Voucher: auto-fill `expense_account` per row from Settings based on `expense_type_key` matching
   - `validate` hook: split VAT NK validation (0 ≤ deductible_pct ≤ 100, sum lines = total)
2. **Custom Field on Landed Cost Voucher:** `vn_is_subject_to_import_duty` (Check, default=1, depends_on `is_import_lcv` custom field also added). Tooltip per spec §3.1.
3. **Custom Field on Landed Cost Voucher:** `vn_is_import_lcv` (Check) — distinguishes import from domestic LCV. When checked → show 7 import expense type rows; unchecked → show 5 domestic types only.
4. **Page `landed-cost-allocation-settings`** — quick-access page for KTT to review/edit LCV Allocation Settings (wraps the Single DocType in friendly UI)
5. **Script Report `Landed Cost Pending Allocation`** per spec §4.5:
   - Cols: Ngày | Số CT | Nhà cung cấp | Số tiền | TK (1388/331) | Diễn giải | [Tạo LCV button per row]
   - Filter: Company + Date range + Account filter
   - Tooltip column header per UI guidance
6. **Sidebar update:** add 5 items to "Giá thành" section per spec §5 sidebar table
7. **Translations:** ~25 entries for LCV (per spec §7 partial table — Landed Cost Allocation, Pending Allocation, 12 expense types VN labels, etc.)
8. **vn_help articles** GT-01, GT-02 per spec §12.3:
   - `apps/vn_help/vn_help/help_articles/co/lcv-co-ban.md` — Phân bổ chi phí mua hàng cơ bản
   - `apps/vn_help/vn_help/help_articles/co/lcv-nhap-khau.md` — LCV cho hàng nhập khẩu + thuế NK + VAT
   - Tiếng Việt thuần, không nhắc "Landed Cost Voucher" — gọi là "Phiếu phân bổ chi phí mua hàng"
9. **Tests Phase 2:**
   - `landed_cost/test_lcv_defaults.py` — auto-fill from Settings, import vs domestic
   - `landed_cost/test_lcv_validation.py` — VAT split 0/100, 50/50, 100/0, reject invalid
   - `landed_cost/test_pending_allocation_report.py` — query correct, includes 1388/331 untied

**Verification Commands:**
- `grep -q "vn_is_subject_to_import_duty" apps/vn_accounting/vn_accounting/fixtures/custom_field.json`
- `grep -q "vn_is_import_lcv" apps/vn_accounting/vn_accounting/fixtures/custom_field.json`
- `test -f apps/vn_accounting/vn_accounting/landed_cost/__init__.py`
- `grep -q "lcv_apply_default_expense_account" apps/vn_accounting/vn_accounting/landed_cost/__init__.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/landed_cost_pending_allocation/landed_cost_pending_allocation.py`
- `grep -q "Phân bổ chi phí mua hàng" apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json`
- `grep -q "Phân bổ chi phí mua hàng" apps/vn_accounting/vn_accounting/translations/vi.csv`
- `test -f apps/vn_help/vn_help/help_articles/co/lcv-co-ban.md`
- `env/bin/python -m unittest apps/vn_accounting/tests/test_lcv_defaults` (exit code 0 = pass, non-zero = fail)

**Live Testing:**
1. `bench --site dcnet.localhost clear-cache && bench restart`
2. Create Purchase Receipt for some test items in `dcnet.localhost`
3. Navigate to `/app/landed-cost-voucher/new`
4. Toggle `vn_is_import_lcv` ON → verify 7 import expense rows appear
5. Toggle `vn_is_subject_to_import_duty` OFF → verify thuế NK + TTĐB rows hidden
6. Set VAT deductible % = 80 → verify split logic
7. Submit LCV → verify GL Entry: Nợ 156 (with shipping/customs added) / Có 3333 (thuế NK)
8. Open Pending Allocation report → verify any untied 1388 entries appear

### Phase 3: Tổng hợp — Sổ kế toán + Kết chuyển 911 + Khóa sổ

**Outcome:** Sổ nhật ký chung (S03a-DN) + Sổ Cái (S03b-DN) reports render correctly with TT99/2025 layout. Wizard kết chuyển 911 auto-detects fiscal year vs periodic → includes/excludes 821 correctly. Period Closing Voucher restricted to Accounts Manager with mandatory lý do + audit log. Sidebar Tổng hợp section has 4 new items working.

Sub-tasks:
1. **Script Report `S03a-DN Sổ Nhật Ký Chung`** per spec §4.4:
   - Cols: Ngày | Số CT | Loại CT | Diễn giải | TK Nợ | TK Có | PS Nợ | PS Có
   - Filter: Company + Period
   - Sort: posting_date ASC, creation ASC
   - Excel export with TT99/2025 layout
   - Column tooltips, filter hints
2. **Script Report `S03b-DN Sổ Cái`** per spec §4.4:
   - Layout 1 TK / trang, drill-through
   - Cols: Ngày | Số CT | Diễn giải | TK đối ứng | PS Nợ | PS Có | Dư Nợ | Dư Có lũy kế
   - Excel export TT99/2025 layout
3. **Page `period-closing-911` (Wizard Kết chuyển cuối kỳ)** per spec §4.1:
   - 3-section layout (revenue → 911, expense → 911, 911 → 421) per spec mockup
   - Help panel top with Mục đích/Các bước/Kết quả
   - Auto-detect fiscal year vs periodic → include/exclude 821 toggle (override checkbox)
   - Preview button shows 3 JE
   - "Tạo 3 JE nháp" button creates draft JEs
   - Settings link button "Cấu hình tài khoản kết chuyển"
   - Warning banner for FX revaluation pending (link to manual workaround article)
   - Banner for fiscal year mode requiring prior TNDN entry
4. **API endpoints:** `vn_accounting.period_closing.get_closing_preview` + `create_closing_journal_entries` per spec §4.1
5. **Extend Period Closing Voucher** per spec §3.6:
   - Custom Field `vn_lock_unlock_reason` (Long Text, reqd=1) — explicit description guiding KTT
   - Hooks: `validate` (check draft JEs, balance, 911 transfer done, lý do not empty), `on_submit` (audit log to Comment), `on_cancel` (validate unlock reason, audit log)
   - DocPerm override via Custom DocPerm fixture: Accounts Manager read/write/submit/cancel=1, System Manager read=1 only, Accounts User read=1
   - delete=0 for all
   - Custom Field `vn_operating_status` on Company (Select: Going Concern / Dissolution / Bankruptcy / Ceased — phase 2 use)
6. **Sidebar update:** add 4 items to "Tổng hợp" section per spec §5
7. **Translations:** ~20 entries for Period Closing + sổ kế toán
8. **vn_help articles** TH-01 to TH-04 per spec §12.3:
   - Sổ nhật ký chung & Sổ Cái — đọc và xuất Excel
   - Kết chuyển cuối kỳ — quy trình + bút toán 911 (giải thích TNDN handling)
   - Khóa sổ kỳ kế toán — khi nào, ai làm, hậu quả
   - Mở khóa kỳ đã đóng — quy trình + audit log
9. **Tests Phase 3:**
   - `period_closing/test_911_je_generation.py` — 3 JE structure correct, debit=credit per JE
   - `period_closing/test_fiscal_year_detection.py` — auto-detect logic correct (year-end vs periodic), 821 inclusion logic
   - `period_closing/test_pcv_validation.py` — reject draft JE, reject unbalanced, reject empty lý do, accept clean state
   - `period_closing/test_pcv_permissions.py` — only Accounts Manager can submit/cancel, audit log written

**Verification Commands:**
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/s03a_dn_so_nhat_ky_chung/s03a_dn_so_nhat_ky_chung.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/s03b_dn_so_cai/s03b_dn_so_cai.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/page/period_closing_911/period_closing_911.json`
- `grep -q "vn_lock_unlock_reason" apps/vn_accounting/vn_accounting/fixtures/custom_field.json`
- `grep -q "vn_operating_status" apps/vn_accounting/vn_accounting/fixtures/custom_field.json`
- `grep -q "pcv_validate_vn_requirements" apps/vn_accounting/vn_accounting/hooks.py`
- `grep -q "expense_accounts_to_close_periodic" apps/vn_accounting/vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json`
- `test -f apps/vn_help/vn_help/help_articles/co/khoa-so-ky.md`
- `env/bin/python -m unittest apps/vn_accounting/tests/test_911_je_generation` (exit code 0 = pass)

**Live Testing:**
1. `bench --site dcnet.localhost clear-cache && bench restart`
2. Login as Accounts Manager → open `/app/period-closing-911`
3. Pick period = current month → verify auto-detect periodic mode, 821 excluded
4. Pick period = fiscal year end (e.g. 31/12/2026) → verify auto-detect year-end mode, 821 included
5. Click "Preview" → verify 3 JE shown correctly
6. Click "Tạo 3 JE nháp" → verify 3 JEs created in Draft state
7. Submit JEs → verify GL impacts correct
8. Navigate `/app/period-closing-voucher/new` → try submit without lý do → verify rejection
9. Login as Accounts User → verify Period Closing Voucher is read-only (no submit/cancel button)
10. Open S03a-DN + S03b-DN reports → verify data displays correctly, Excel export works

### Phase 4: Báo cáo tài chính — B01, B02, B03 + B09 Excel

**Outcome:** 4 BCTC reports operational with TT99/2025 mappings. B01 equation (Tài sản = Nguồn vốn) holds. Click-through drill works. B09 generates multi-sheet Excel. BCTC Mapping form has 2 helper buttons working. Sidebar BCTC section has 5 items with default fiscal_year filter.

Sub-tasks:
1. **BCTC resolver engine** (`vn_accounting/financial_reporting/resolver.py`) per spec §4.3:
   - Function `resolve_bctc_line(company, line, period_start, period_end)`
   - Parser for `account_formula` syntax: `+TK,+TK,-TK` with wildcard `511%`
   - 5 `value_type` modes: closing_debit / closing_credit / period_debit / period_credit / formula
   - Recursive for `line_formula` (e.g., `=10-11`)
2. **Script Report B01-DN** (`b01_dn_bao_cao_tinh_hinh_tai_chinh`):
   - Cols: Mã | Tên chỉ tiêu | Số cuối kỳ | Số đầu năm
   - Filter: Company + As-of date + fiscal year
   - Hover icon ℹ on Mã → tooltip with formula
   - Click on number → drill to GL Entries filtered by formula
   - "Cấu hình mapping" button → opens BCTC Mapping
   - "Xuất Excel" button → openpyxl-based file with TT99/2025 layout
   - **B01 equation check**: post-render assertion `mã_270 == mã_440` (within tolerance); show red banner if mismatch
3. **Script Report B02-DN** (`b02_dn_bao_cao_kqhdkd`):
   - Cols: Mã | Tên | Kỳ này | Kỳ trước
   - Filter: Company + Period range
   - Same drill + Excel export pattern
4. **Script Report B03-DN** (`b03_dn_bao_cao_lctt`) — phương pháp gián tiếp only (Phase 1):
   - 3 sections (Kinh doanh / Đầu tư / Tài chính)
   - End-of-period figure cross-checks B01 mã 110
5. **Page `b09-dn-generator`** per spec §4.6:
   - openpyxl multi-sheet Excel:
     - Sheet 1 `1_Van_xuoi` (Phần I-IV + VI) — văn xuôi with placeholders `[Kế toán điền: ...]`
     - Sheet 2-N `5.x_Chi_tiet_...` — auto-fill from GL/Asset/Stock/Loan
   - Auto-fill cells have gray bg + locked; editable cells white + unlocked
   - Conditional: only generate sheet if data exists
6. **BCTC Mapping form buttons** per spec §3.4:
   - "Copy mapping từ Company khác" — dialog with source picker + diff preview + confirm
   - "Khôi phục mặc định TT99/2025" — modes: full report OR single row + confirm
7. **Sidebar update:** add 5 items to "Báo cáo tài chính" section per spec §5 with default `route_options` containing `fiscal_year={current}` + `as_on_date={today}`
8. **Translations:** ~40 entries for BCTC
9. **vn_help articles** BCTC-01 to BCTC-04 per spec §12.3
10. **Tests Phase 4:**
    - `financial_reporting/test_bctc_resolver.py` — formula parser (+TK,-TK,wildcard), all 5 value_type modes, line_formula recursion
    - `financial_reporting/test_b01_equation.py` — seed test Company with sample GL → assert mã_270 == mã_440
    - `financial_reporting/test_b02_calculations.py` — compute mã 60 (LN sau thuế) end-to-end
    - `financial_reporting/test_bctc_mapping_clone.py` — Copy from another Company + Restore defaults work correctly

**Verification Commands:**
- `test -f apps/vn_accounting/vn_accounting/financial_reporting/resolver.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/b01_dn_bao_cao_tinh_hinh_tai_chinh/b01_dn_bao_cao_tinh_hinh_tai_chinh.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/b02_dn_bao_cao_kqhdkd/b02_dn_bao_cao_kqhdkd.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/b03_dn_bao_cao_lctt/b03_dn_bao_cao_lctt.py`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/page/b09_dn_generator/b09_dn_generator.json`
- `grep -q "Báo cáo tình hình tài chính" apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json`
- `grep -q "fiscal_year" apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json` (default filter for sidebar BCTC items)
- `test -f apps/vn_help/vn_help/help_articles/co/bctc-b01-cau-truc.md`
- `env/bin/python -m unittest apps/vn_accounting/tests/test_bctc_resolver` (exit code 0 = pass)
- `env/bin/python -m unittest apps/vn_accounting/tests/test_b01_equation` (exit code 0 = pass)

**Live Testing:**
1. `bench --site dcnet.localhost clear-cache && bench restart`
2. Navigate `/app/query-report/B01-DN Bao Cao Tinh Hinh Tai Chinh` — verify default fiscal year populates, data renders
3. Hover icon ℹ on Mã 110 → verify formula tooltip shows "+111,+112,+113 → Số dư Nợ cuối kỳ"
4. Click number on Mã 110 → verify drill to GL Entries filtered
5. Check mã_270 == mã_440 visually (or banner if mismatch)
6. Click "Xuất Excel" → verify file downloads with TT99/2025 layout
7. Navigate to B09 generator page → click "Sinh file B09-DN" → verify multi-sheet Excel downloads
8. Open BCTC Mapping form → click "Khôi phục mặc định TT99/2025" → verify restore works
9. Navigate B02-DN, B03-DN — verify rendering + Excel export

### Phase 5: Giá thành sản xuất

**Outcome:** WIP Valuation DocType operational with all 4 valuation methods. Manufacturing Costing Wizard page works for both manufacturing (→ 155) and services/construction (→ 632 direct). Project setup guide for xây lắp linked from Project form. Production Cost Aggregation report works. Sidebar Giá thành section complete (Manufacturing items added on top of LCV items).

Sub-tasks:
1. **DocType WIP Valuation** per spec §3.5:
   - All fields including new equivalent production fields
   - `computed_closing_wip` auto-compute based on `valuation_method`
   - Status workflow: Draft / Calculated / Posted / Cancelled
   - Rich field descriptions per UI guidance
2. **Script Report `Production Cost Aggregation`** per spec §4.5:
   - 621/622/627 phát sinh kỳ, group by cost_object
   - Filter: Company + Period + cost_object_type
3. **Page `manufacturing-costing-wizard`** per spec §4.2:
   - 7-step flow with branching at Step 6/7 based on `transfer_to_finished_goods`
   - Help panel top + step intros per UI guidance
   - Step 3: WIP Valuation entry (1 row per cost object, multi-method support)
   - Step 4: 627 allocation per Settings basis (Machine Hours / Labor Hours / Volume / etc.)
   - Step 5: unit_cost preview per cost object
   - Step 6 branching:
     - DN sản xuất (transfer_to_finished_goods=1): 2 JE preview (621/622/627 → 154 + 154 → 155)
     - DN dịch vụ/xây lắp (=0): 2 JE preview (621/622/627 → 154 + 154 → 632 services_cogs_account)
   - Step 7: Create draft JEs + Stock Entries (conditional)
4. **Custom Fields on Project** per spec §4.7 for construction:
   - `vn_is_construction_project`, `vn_contract_value`, `vn_handover_percentage`, `vn_construction_phase`
   - Rich descriptions, depends_on conditions
5. **API endpoints:** `aggregate_production_costs`, `calculate_unit_costs`, `create_costing_journal_entries` per spec §4.2
6. **Sidebar update:** add 3 manufacturing items to "Giá thành" section (LCV items already in Phase 2)
7. **Translations:** ~30 entries for manufacturing costing
8. **vn_help articles** GT-03, GT-04 per spec §12.3:
   - Tính giá thành sản xuất cuối kỳ — quy trình 6 bước
   - Setup Project cho DN xây lắp
9. **Tests Phase 5:**
   - `costing/test_unit_cost_calculation.py` — formula edge cases (0 qty, 0 closing, equivalent production)
   - `costing/test_overhead_allocation.py` — 6 allocation bases, sum = 627
   - `costing/test_costing_branching.py` — services mode → JE to 632, manufacturing mode → JE to 155 + Stock Entry
   - `costing/test_wip_valuation_methods.py` — 4 valuation methods compute correctly

**Verification Commands:**
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/doctype/work_in_progress_valuation/work_in_progress_valuation.json`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/page/manufacturing_costing_wizard/manufacturing_costing_wizard.json`
- `test -f apps/vn_accounting/vn_accounting/vn_accounting/report/production_cost_aggregation/production_cost_aggregation.py`
- `grep -q "vn_is_construction_project" apps/vn_accounting/vn_accounting/fixtures/custom_field.json`
- `grep -q "physical_units_in_progress" apps/vn_accounting/vn_accounting/vn_accounting/doctype/work_in_progress_valuation/work_in_progress_valuation.json`
- `grep -q "Bảng tính giá thành" apps/vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json`
- `test -f apps/vn_help/vn_help/help_articles/co/du-an-xay-lap-setup.md`
- `env/bin/python -m unittest apps/vn_accounting/tests/test_costing_branching` (exit code 0 = pass)

**Live Testing:**
1. Manufacturing flow (DN sản xuất): create test Items + Work Orders → run wizard → verify 2 JE + Stock Entry generated
2. Services flow: set Settings `transfer_to_finished_goods=0` → run wizard → verify JE goes to 632 directly, no Stock Entry
3. Construction flow: tick `vn_is_construction_project` on a Project → set contract_value + handover_percentage → run wizard with cost_object_type=Project → verify project-based calculation
4. WIP Valuation: create record with `valuation_method=Equivalent Production` → enter physical_units + completion_pct → verify computed_closing_wip auto-calculates

### Phase 6: Polish + i18n full + Tests regression + Docs

**Outcome:** All 12 vn_help articles complete. Full translation pass (~140 entries verified). No-hardcoded-TK regression test passes. UI guidance coverage test passes. CODEBASE.md + CODEBASE_DETAIL.md updated. Full end-to-end smoke test from Company creation → all 15 sidebar items → all reports → all wizards.

Sub-tasks:
1. **Complete vn_help articles** — verify all 12 articles per §12.3 exist with proper YAML frontmatter + tiếng Việt thuần (no ERPNext/Frappe/DocType mentions)
2. **Translations pass** — review vi.csv completeness, ensure all English source strings have VN translation
3. **No-hardcoded-TK regression test** per spec §8.3:
   - `tests/test_no_hardcoded_accounts.py` — grep regex `["']\b[1-9]\d{2,4}["']` in `landed_cost/`, `costing/`, `period_closing/`, `financial_reporting/` Python files
   - Whitelist: fixture JSONs, test fixtures, lookup helpers with `# fallback default TT99/2025` comment
4. **UI guidance regression test** per spec §8.4:
   - `tests/test_ui_guidance_coverage.py` — scan all new DocTypes for field descriptions, Section Break descriptions, button tooltips in .js files
5. **CODEBASE.md update:** add 4 new sub-packages + ~12 new DocTypes to overview
6. **CODEBASE_DETAIL.md update:** one-line description per new file
7. **Excel layout polish** (per §10.8 promoted into Phase 6):
   - Verify font (Times New Roman 11pt per TT99 convention)
   - Column widths match Phụ lục IV
   - Merge cells in headers correct
   - Tested by opening downloaded files in real Excel/LibreOffice
8. **Full smoke test:**
   - Create fresh Company `Test Co Vietnam` with country=Vietnam
   - Verify BCTC Mapping auto-cloned, COA seeded
   - Create LCV → verify defaults
   - Generate JEs for sample period
   - Run kết chuyển wizard
   - Run khóa sổ
   - Generate B01/B02/B03/B09
   - Run costing wizard
   - All 15 sidebar items click → land on correct page/report/list with no errors
9. **Final FEATURES.md update:** move C7.* + C8.* + C9.* + C10.* + relevant C2.* items to "Done" status with date
10. **Commit & branch ready for PR:**
    - All commits squashed/cleaned
    - Branch ready to merge to main

**Verification Commands:**
- `find apps/vn_help/vn_help/help_articles/co -name "*.md" | wc -l` should be ≥ 12 (articles for this feature set)
- `wc -l apps/vn_accounting/vn_accounting/translations/vi.csv` should be ≥ 230 (existing ~95 + new ~140)
- `env/bin/python -m unittest apps/vn_accounting/tests/test_no_hardcoded_accounts` (exit code 0 = pass)
- `env/bin/python -m unittest apps/vn_accounting/tests/test_ui_guidance_coverage` (exit code 0 = pass)
- `env/bin/python -m unittest discover apps/vn_accounting/tests` (exit code 0 = all pass)
- `grep -q "C7.* | .* | Done" apps/vn_accounting/FEATURES.md`
- `grep -q "C10.* | .* | Done" apps/vn_accounting/FEATURES.md`

**Live Testing — Full smoke (E2E):**
1. Create new test Company "Smoke Test Co" with country=Vietnam, COA template=large
2. Verify auto-seed: COA loaded, BCTC Mapping cloned, default accounts populated
3. Walk through every sidebar item in 3 sections (Giá thành, Tổng hợp, BCTC) — 15 items
4. Each click must open without error, render with default data filter, show inline guidance
5. Final manual UI guidance audit — random sample 10 fields/buttons → verify all have tooltips/descriptions

## Acceptance Criteria

- [ ] All 4 Settings DocTypes seeded with TT99/2025 defaults, no hardcoded TK in controller code
- [ ] LCV with auto-fill from Settings works for both domestic + import, VAT split correct
- [ ] Sổ nhật ký chung (S03a-DN) + Sổ Cái (S03b-DN) render with TT99/2025 layout + Excel export
- [ ] Wizard kết chuyển 911 auto-detects fiscal year, includes/excludes 821 correctly
- [ ] Period Closing Voucher restricted to Accounts Manager, mandatory lý do, audit log working
- [ ] B01 equation `mã_270 = mã_440` holds for seeded test data
- [ ] B01/B02/B03 reports render with formula tooltips + drill-through working
- [ ] B09-DN multi-sheet Excel generated with auto-filled detail sheets + locked cells
- [ ] BCTC Mapping has working "Copy from another Company" + "Restore defaults" buttons
- [ ] Manufacturing Costing Wizard rẽ nhánh đúng: DN sản xuất → 155 + Stock Entry; DN dịch vụ/xây lắp → 632 direct
- [ ] WIP Valuation supports all 4 methods with `computed_closing_wip` auto-compute
- [ ] All 15 sidebar items working with default filters (no empty state)
- [ ] All 12 vn_help articles published in tiếng Việt thuần
- [ ] No-hardcoded-TK regression test passes
- [ ] UI guidance coverage test passes (all reqd fields + Link/Select/Currency have descriptions)
- [ ] Full smoke test: fresh Company → all 15 items → all wizards → all reports work end-to-end
- [ ] FEATURES.md: C7.*, C8.*, C9.*, C10.*, relevant C2.* marked as Done

## Out of Scope (deferred to phase 2)

Per spec §10.8:
- DN không liên tục (B01/B02/B03/B09-DNKLT)
- B03-DN phương pháp trực tiếp
- BCTC hợp nhất công ty con
- BCTC theo IFRS song song
- Wizard "Đánh giá lại tỷ giá ngoại tệ" (Phase 1: KTT làm thủ công)
- LCV rebate / chiết khấu mua sau
- Wizard tính TNDN tạm tính / quyết toán (thuộc section C3 Thuế)
- Bảng kê hoá đơn GTGT (thuộc section C3)
- Tờ khai thuế TNDN, TNCN, GTGT (section C3)
- Phân tích chỉ số tài chính (đã có Dashboard v2)

## Notes for Each Session

1. **Read spec FIRST every session** (`docs/specs/2026-05-11-giathanh-tonghop-bctc.md` — 916 lines, đã chốt với KTT 2026-05-11)
2. **Check BUSINESS_LOGIC.md** §11-14 cho business rules & edge cases
3. **Apply cross-cutting rules:** no hardcoded TK + UI inline guidance — ref memory `feedback_vn_accounting_no_hardcoded_accounts.md` + `feedback_ui_inline_guidance.md`
4. **Filesystem convention:** all DocTypes in `apps/vn_accounting/vn_accounting/vn_accounting/doctype/`, sub-packages (`landed_cost/`, `costing/`, etc.) hold helper code + pages + reports
5. **Bench restart required** after Python edits (frappe-spa.md rule)
6. **Always commit at end of session** + write `session-last-giathanh-tonghop-bctc.md` with: what done, learnings, exact "Next Session Task" with file paths, remaining acceptance criteria
7. **Pure-fix mode for QA findings**: no tier policy — fix everything fixable in scope
