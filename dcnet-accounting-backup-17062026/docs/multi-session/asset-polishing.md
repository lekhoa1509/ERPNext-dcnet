# Task: Asset Polishing — TSCĐ & CCDC theo TT99/2025

## Context

vn_accounting needs full coverage of Fixed Assets (TSCĐ) and Tools/Equipment (CCDC) lifecycle per Vietnamese accounting standards (TT99/2025/TT-BTC, effective 2026-01-01). Currently the sidebar has 8 placeholder items in "TSCĐ & CCDC" but CCDC is 0% implemented (only a JE filter stub), there is no Bàn giao/Kiểm kê form (S22-DN required by law), and ERPNext Asset labels are mostly English. This task implements per the approved design spec at `docs/superpowers/specs/2026-04-29-asset-polishing-design.md` (commit `0d9ab59`).

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing` (worktree)
- Branch: `feat/asset-polishing` (already created)
- Bench root for migrate/build/test: `/home/long/long/frappe-bench-dcnet`
- Test site: `dcnet.localhost`
- Test URL: `http://dcnet.localhost:8001`
- Design spec: `docs/superpowers/specs/2026-04-29-asset-polishing-design.md` — **read this first every session**

### Related files

| File | Purpose | Action |
|------|---------|--------|
| `docs/superpowers/specs/2026-04-29-asset-polishing-design.md` | Design source of truth | Read FIRST every session |
| `docs/superpowers/plans/2026-04-29-asset-polishing-plan.md` | Implementation plan | Created in Phase 0 |
| `vn_accounting/vn_accounting/doctype/` | DocType directory | Create 9 new + 1 child for Settings |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json` | Settings DocType (~22 fields after cash count) | Add ~10 fields for Permission tab + thresholds + audit log |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.py` | Settings controller | Add on_update sync logic + reset_permission_matrix whitelisted |
| `vn_accounting/fixtures/asset_permission_defaults.json` | Default permission rules | Create — ~15 rows per design §9.3 |
| `vn_accounting/fixtures/property_setter.json` | Property Setters | Add: hide 3 depreciation methods on Asset.depreciation_method |
| `vn_accounting/fixtures/custom_field.json` | Custom Fields | Add: Item.is_low_value_asset, Asset Repair.repair_classification, Asset Handover.scope, Asset Stocktake.scope |
| `vn_accounting/chart_of_accounts/vn_small_enterprise.json` | VN small COA | TK 242 rename "Chi phí trả trước" |
| `vn_accounting/chart_of_accounts/vn_large_enterprise.json` | VN large COA | TK 242 rename + verify 211 group |
| `vn_accounting/translations/vi.csv` | VN translations | Add ~30 ERPNext Asset labels + ~50 new for custom DocTypes |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Sidebar nav | Replace section "TSCĐ & CCDC" with 2 sections "TSCĐ" + "CCDC" per design §5.1 |
| `vn_accounting/install.py` | Install hooks | Add asset_category re-seed, ccdc_category seed, permission defaults loader |
| `vn_accounting/hooks.py` | App hooks | Add doc_events for Purchase Invoice on_submit (auto-create CCDC Item), scheduler_events for monthly CCDC allocation |
| `vn_accounting/treasury/journal_entry_builder.py` | Reusable JE builder | Reference pattern; create `vn_accounting/asset/journal_entry_builder.py` similar |
| `vn_accounting/vn_accounting/doctype/asset_disposal/` | Pattern reference | Copy structure for biên bản 4-sign |
| `vn_accounting/vn_accounting/doctype/cash_count/` | Pattern reference | Copy for workflow + biên bản pattern |
| `vn_accounting/vn_accounting/print_format/` | Print formats | Add 8 new biên bản (S21-DN, S22-DN, kiểm kê, sửa chữa, ghi giảm CCDC, giao nhận TSCĐ) |
| `vn_accounting/vn_accounting/report/` | Reports | Add Script Reports: `s21_dn_so_tscd`, `s22_dn_theo_doi_tscd_ccdc` |
| `apps/dcnet_sample/dcnet_sample/...` | Demo data | Add asset/ccdc demo seed in Phase 4 |
| `tests/` | Test directory | Create 5 unit test files per design §12.1 |

## Requirements

### Phase 0: Implementation Plan

**Outcome:** A detailed implementation plan committed to `docs/superpowers/plans/2026-04-29-asset-polishing-plan.md`.

Steps:
1. Read the full design spec at `docs/superpowers/specs/2026-04-29-asset-polishing-design.md`.
2. Use the **superpowers:writing-plans** skill to write an ordered, file-level implementation plan with exact code outlines for each unit (DocType JSON, controller methods, JE routing, fixtures, sidebar items, translations).
3. **Self-review** the plan with the 3-point checklist:
   - **Spec coverage** — every section of the design spec maps to ≥1 plan task.
   - **Placeholder scan** — no TBD/TODO except those explicitly marked Out-of-Scope in design §13.
   - **Type consistency** — DocType names, field names, account numbers consistent across all plan tasks.
4. **Self-fix** any issues found inline. Add a "Self-Review Notes" section recording what was found and fixed.
5. Commit plan with message `docs(asset-polishing): implementation plan from design spec`.

### Phase 1: Foundation + TSCĐ Polish

**Outcome:** Site `dcnet.localhost` shows TK 242 as "Chi phí trả trước"; Asset.depreciation_method dropdown has only 2 options; Sidebar has 2 sections (TSCĐ + CCDC) with all link items routing correctly (CCDC links may 404 until Phase 2); Asset Repair form has `repair_classification` field with JE routing; VN Accounting Settings has tab "Phân quyền TSCĐ & CCDC"; Sổ S21-DN report renders with TT99 columns.

Sub-tasks:
1. Update `vn_small_enterprise.json` + `vn_large_enterprise.json`: TK 242 label "Chi phí trả trước"
2. Add Property Setter fixture: `Asset.depreciation_method.options = "\nĐường thẳng\nSố dư giảm dần"`
3. Add ~30 entries to `vi.csv` per design §7.1 (Asset, Asset Category, Asset Repair, Movement, Custodian, Available-for-use, depreciation method options, etc.)
4. Asset Category re-seed (6 categories) — add to `install.after_migrate` per design §7.4
5. Custom Field `Item.is_low_value_asset` (Check)
6. Custom Field `Asset Repair.repair_classification` (Select 3-way) per design §4.5 + §7.3
7. Asset Repair extend: `validate()` warning ≥10%, `on_submit` JE routing per classification (Chi phí | Sửa chữa lớn | Nâng cấp). Use `vn_accounting/asset/journal_entry_builder.py` (new). When classification == "Nâng cấp cải tạo", recreate Asset Depreciation Schedule with new gross_purchase_amount and useful_life.
8. Print format: Biên bản sửa chữa TSCĐ (3-sign template, A4 dọc)
9. Sidebar reorg: replace section "TSCĐ & CCDC" with 2 new sections (TSCĐ + CCDC) per design §5.1. Add CCDC link items as placeholders (target Asset Handover/Stocktake which don't exist yet — that's OK; Phase 2-3 will create them).
10. Script Report `s21_dn_so_tscd` per design §6 — columns: mã TS, tên, ngày sử dụng, nguyên giá, kỳ KH, % KH năm, GTKH năm, GTKH luỹ kế, GTCL, ghi chú. Replace sidebar link "Sổ TSCĐ" target.
11. VN Accounting Settings tab "Phân quyền TSCĐ & CCDC":
    - Add fields per design §9.1 — section breaks + thresholds (3 fields) + scope_by_department flag + asset_revaluation_enabled flag + permission_matrix (Table → Asset Permission Rule child) + permission_audit_log (Long Text)
    - Create child DocType `Asset Permission Rule` per design §9 fixture schema
    - `on_update` hook: validate thresholds, sync permission_matrix → Custom DocPerm (delete-and-recreate for affected DocTypes), apply department User Permissions if flag, write audit_log entry
    - Whitelisted method `reset_permission_matrix()` reads `asset_permission_defaults.json` fixture
    - Form button "Khôi phục mặc định" calls reset method
    - Form indicator (📍 icon) on rows where current values differ from fixture defaults
    - Audit log display: latest 5 entries in HTML field
12. Create `asset_permission_defaults.json` fixture per design §9.3 (~15 rows)

**Verification within session (before QA):**
- `bench --site dcnet.localhost migrate` succeeds
- `bench --site dcnet.localhost console` → check `frappe.db.get_value("Account", {"company":"<test>", "account_number":"242"}, "account_name")` returns "Chi phí trả trước - <abbr>"
- Open `http://dcnet.localhost:8001/app/asset/new` → depreciation_method shows 2 options
- Settings tab "Phân quyền TSCĐ & CCDC" loads, default 15 rows, click "Khôi phục mặc định" reset table

### Phase 1 QA Gate

After Phase 1 implementation done, run full QA before moving to Phase 2:

13. **Persona QA — Kế toán trưởng (use `/qa` skill, screenshots to `qa-screenshots/phase1-ktt/`)**:
    - Open VN Accounting Settings → Phân quyền tab → verify default 15 rules render
    - Edit 1 rule (toggle off Stocktake / Stocktake Member) → click Áp dụng → verify Custom DocPerm count updated
    - Set ngưỡng thanh lý 30tr → save → verify audit log entry appears
    - Click "Khôi phục mặc định" → confirm dialog → reset → verify table back to defaults
    - Console errors == 0
14. **Persona QA — Kế toán tài sản (`qa-screenshots/phase1-kttsm/`)**:
    - Navigate sidebar → verify TSCĐ + CCDC sections, click each link verify route correct (CCDC may 404 — expected pre-Phase 2)
    - Open `/app/asset/new` → verify VN labels (Nguyên giá, Phương pháp khấu hao 2 options)
    - Create Asset Repair classification="Sửa chữa lớn vốn hóa", repair_cost=20% of nguyên giá → submit → verify GL Entry has TK 241 + warning shown
    - Open Sổ S21-DN report → verify columns match TT99 layout
    - Console errors == 0
15. **Design QA — Phase 1 scope (`/design-qa` skill, append to `docs/design-qa-proposals/asset-polishing.md`)**: visit Settings Permission tab + sidebar + Asset Repair form + S21-DN report via Playwright MCP. Cosmetic fixes (spacing, label wording, alignment) implement + commit atomically. Structural proposals (flow change, new field, workflow change) → append to proposals file with `## Session YYYY-MM-DD HH:MM Phase 1` header.
16. **Bug fix loop**: For each critical bug found in QA → systematic-debugging investigation → fix → re-run failing scenario → confirm pass. Commit each fix atomically.
17. **Phase 1 checkpoint commit**: `git commit -m "feat(asset-polishing): Phase 1 foundation + TSCĐ polish complete + QA pass"`

### Phase 2: CCDC Backbone

**Outcome:** Site can mua CCDC qua Purchase Invoice with `is_low_value_asset=1` → auto-create CCDC Item draft → submit + ngày xuất + N kỳ → JE 242/153 + CCDC Allocation Schedule auto-create with N entries → scheduler runs monthly → JE 627/641/642 / 242 each period → kỳ cuối CCDC.status="Hết phân bổ"; CCDC Writeoff giữa kỳ creates JE clearing 242 + 153 correctly.

Sub-tasks:
1. DocType `CCDC Category` (Master) — fields: category_name, parent_category_account (Link 153 sub), expense_account_default (Link 627/641/642), useful_period_default (Int, months), is_group flag
2. Seed 5 default CCDC Categories per design §7.5 (in `install.after_install` + idempotent in `after_migrate`)
3. DocType `CCDC Item` (Submittable) — fields: item_code (Link Item), item_name, ccdc_category, company, location, custodian, cost, cost_account (Link 153), expense_account (Link 627/641/642), prepayment_account (Link 242), purchase_date, available_for_use_date, useful_period_months, allocation_periods, status (Select: Mới mua, Đang sử dụng, Hết phân bổ, Đã ghi giảm), purchase_invoice (Link), purchase_invoice_item, scope_for_handover (Hidden, default "CCDC")
4. CCDC Item validate: cost > 0, useful_period_months > 0, allocation_periods >= 1
5. CCDC Item `on_submit`:
   - Create JE: N TK 242 / C TK 153, posting_date = available_for_use_date
   - Create CCDC Allocation Schedule with N child entries (cost / N each, last entry handles rounding)
6. DocType `CCDC Allocation Schedule` (Submittable) — fields: ccdc_item (Link), start_date, total_amount, periods, frequency (Select: Monthly only for v1), allocation_entries (Table), status
7. DocType `CCDC Allocation Entry` (Child) — fields: period_no, period_start_date, allocation_amount, journal_entry (Link), status (Pending / Posted), posted_at
8. Scheduler hook `vn_accounting.tasks.allocate_ccdc_monthly` (in hooks.py `scheduler_events.daily`): for each Pending entry where `period_start_date <= today`, post JE N expense / C 242, set status=Posted, link JE.
9. Hook PI `on_submit`: for each item with `is_low_value_asset=1`, auto-create CCDC Item draft (status=Mới mua, prefill cost, item_code, purchase_invoice link). Surface link in PI page.
10. DocType `CCDC Writeoff` (Submittable) — fields: ccdc_item (Link, reqd, must be Submitted + status != "Đã ghi giảm"), writeoff_date, writeoff_reason (Select: Mất, Hỏng không sửa được, Hết hạn sử dụng, Khác), compensation_amount (Currency), compensation_employee (Link Employee, conditional), remaining_242_amount (Currency, read_only), remaining_153_amount (Currency, read_only), remarks
11. CCDC Writeoff `on_submit`:
    - Calc remaining 242 amount (sum unposted allocation entries)
    - JE clear 242: N expense / C 242 (full remaining)
    - If remaining 153 > 0 (CCDC chưa xuất dùng): JE N (632 if no comp, else 1381) / C 153
    - Cancel pending CCDC Allocation Schedule entries
    - Set CCDC Item.status = "Đã ghi giảm"
12. Print format: Biên bản ghi giảm CCDC (2-sign template)
13. Update sidebar: enable CCDC links (Danh sách CCDC, Tạo CCDC, Phân bổ CCDC, Ghi giảm CCDC)

**Verification within session (before QA):**
- Create test PI with item.is_low_value_asset=1, submit → CCDC Item draft auto-created (verify via `frappe.get_all("CCDC Item", filters={"purchase_invoice": pi.name})`)
- Submit CCDC Item → JE 242/153 GL Entry exists with correct amounts; CCDC Allocation Schedule has N entries
- Run scheduler manually: `bench --site dcnet.localhost execute vn_accounting.tasks.allocate_ccdc_monthly` → first Pending entry → JE posted, status=Posted
- CCDC Writeoff giữa kỳ → remaining 242 cleared, status="Đã ghi giảm"

### Phase 2 QA Gate

After Phase 2 implementation done, run full QA before moving to Phase 2:

14. **Persona QA — Kế toán tài sản (`qa-screenshots/phase2-kttsm/`)**:
    - Create Item with is_low_value_asset=1 → create PI line → submit PI → verify CCDC Item draft auto-created
    - Open auto-created CCDC Item → set ngày xuất + 12 kỳ → submit → verify JE 242/153 + Allocation Schedule
    - View Allocation Schedule → verify 12 entries summing to cost
    - Trigger scheduler manually → verify first entry posted, GL Entry exists 627/242
    - Create CCDC Writeoff for active CCDC giữa kỳ phân bổ → submit → verify GL clear remaining 242 + 153
    - Print biên bản ghi giảm CCDC → verify 2-sign layout
    - Console errors == 0 throughout
15. **Design QA — Phase 2 scope (append to `docs/design-qa-proposals/asset-polishing.md`)**: visit CCDC Item form, CCDC Allocation Schedule view, CCDC Writeoff form, biên bản ghi giảm preview via Playwright MCP. Cosmetic fixes implement + commit. Structural proposals → append with `## Session YYYY-MM-DD HH:MM Phase 2` header.
16. **Bug fix loop**: critical bugs → systematic-debugging → fix → retest. Commit atomically.
17. **Phase 2 checkpoint commit**: `git commit -m "feat(asset-polishing): Phase 2 CCDC backbone complete + QA pass"`

### Phase 3: Bàn giao + Kiểm kê

**Outcome:** Asset Handover form for both TSCĐ and CCDC (route_options scope filter works), submit updates Asset/CCDC location+custodian + creates Asset Movement bóng (TSCĐ only), threshold validation works. Asset Stocktake with workflow 4 state, auto-loads items by location, approve action creates JE for missing items + updates target status. Both forms render correct biên bản.

Sub-tasks:
1. DocType `Asset Handover` (Submittable) — fields per design §4.3: scope (Select [TSCĐ, CCDC], reqd, default from route_options), posting_date, from_employee, from_department, to_employee, to_department, to_location, co_signer_employee, handover_items (Table), total_asset_value (read_only), reason, remarks, before_handover_snapshot (JSON, read_only)
2. DocType `Asset Handover Item` (Child) — fields: target_doctype (Link DocType, must be Asset or CCDC Item), target_name (Dynamic Link), asset_name (Data, read_only fetched), book_value (Currency, read_only), serial_no, remarks
3. Asset Handover validate:
   - All items.target_doctype matches scope (TSCĐ→Asset, CCDC→CCDC Item)
   - If thresholds enabled and total_asset_value >= handover_threshold → co_signer_employee reqd
   - Save snapshot of current Asset/CCDC.location+custodian to before_handover_snapshot
4. Asset Handover on_submit:
   - For each item: update target's location, custodian, department per parent values
   - If scope=TSCĐ: also create Asset Movement record linked to this Handover (for ERPNext audit trail)
5. Asset Handover on_cancel: revert from before_handover_snapshot
6. Print format: Biên bản giao nhận / Sổ S22-DN — Jinja template renders different headers/columns per scope (TSCĐ uses 01-TSCĐ TT99 layout, CCDC uses S22-DN layout). 3-sign (Bên giao / Bên nhận / Kế toán) + co_signer if present.
7. Form toolbar button "📋 Sao chép sang phiếu CCDC" (or "TSCĐ") — duplicates current doc with scope flipped
8. DocType `Asset Stocktake` (Workflow) — fields per design §4.4
9. DocType `Asset Stocktake Item` (Child) — fields: target_doctype, target_name (Dynamic Link), book_value, physical_status (Select: Còn nguyên, Hỏng, Mất), remarks, last_stocktake_date (read_only)
10. Workflow `Asset Stocktake Workflow` — states: Draft → In Progress → Completed → Approved → Closed; transitions per design §4.4. Roles: Accounts User can submit Draft→In Progress→Completed; Accounts Manager approves/rejects.
11. Stocktake button "Tải danh sách" — `@frappe.whitelist()` server method: load all Asset (scope=TSCĐ) or CCDC Item (scope=CCDC) at given location/department where status not in (Disposed, Đã ghi giảm), populate stocktake_items
12. Stocktake on_approve (workflow action):
    - For each item: handle 3 statuses per design §4.4 (Còn nguyên = no-op, Mất = JE 1381/211 or 1381/153, Hỏng = update target.status=Damaged)
    - Set last_stocktake_date for all items regardless of status
13. Print format: Biên bản kiểm kê (3-sign: Trưởng đoàn / Thủ kho / Kế toán)
14. Script Report `s22_dn_theo_doi_tscd_ccdc`: filter by location + department (or "all"), group by location, columns include both TSCĐ and CCDC active records at that location.

**Verification within session (before QA):**
- Create Bàn giao TSCĐ for 1 Asset, submit → Asset.custodian + location updated, Asset Movement record exists
- Validate scope: try add CCDC Item to scope=TSCĐ phiếu → ValidationError thrown
- Threshold: handover with total > 100tr without co_signer → error
- Create Stocktake at location X → click Tải danh sách → items populated
- Stocktake approve with 1 Mất → JE 1381/211 created with correct amount; Asset.status=Lost

### Phase 3 QA Gate

After Phase 3 implementation done, run full QA before moving to Phase 4:

15. **Persona QA — Kế toán tài sản (`qa-screenshots/phase3-kttsm/`)**:
    - Create Asset Handover scope=TSCĐ → add 1 Asset → set to_employee + to_department → submit → verify Asset.custodian/location updated + Asset Movement record exists
    - Print biên bản S22-DN → verify TSCĐ layout, 3-sign correct
    - Create Asset Handover scope=CCDC → add 1 CCDC Item → submit → verify CCDC Item.location updated, biên bản S22-DN CCDC layout
    - Click "Sao chép sang phiếu CCDC" toolbar button → verify duplicate created with scope flipped
    - Create Asset Stocktake scope=TSCĐ at location X → click Tải danh sách → verify items populated → mark 1 Mất + 1 Hỏng → submit (Draft → In Progress → Completed)
    - Console errors == 0
16. **Persona QA — Kế toán trưởng (`qa-screenshots/phase3-ktt/`)**:
    - Open Stocktake from Persona 1 (Completed state) → workflow approve action → verify GL Entry N 1381 / C 211 cho Mất + Asset.status=Lost cho Mất + Damaged cho Hỏng
    - Print biên bản kiểm kê → verify 3-sign (Trưởng đoàn / Thủ kho / Kế toán)
    - Create Asset Handover scope=TSCĐ với total ≥ 100tr nhưng không co_signer → verify ValidationError
    - View Sổ S22-DN report → filter location → verify TSCĐ + CCDC group
    - Console errors == 0
17. **Persona QA — Trưởng phòng (`qa-screenshots/phase3-deptHead/`)**:
    - Create test user with Department Head role + User Permission Department=IT
    - Login as that user → navigate Asset list → verify chỉ thấy TSCĐ thuộc phòng IT (custodian/department=IT)
    - Try open Asset thuộc phòng Kế toán → verify No Permission error
    - Verify Asset list KHÔNG có "+ New" button (no create permission)
    - Verify CCDC Item list cùng behavior
    - Console errors == 0
18. **Design QA — Phase 3 scope (append to `docs/design-qa-proposals/asset-polishing.md`)**: visit Asset Handover form (TSCĐ + CCDC), Stocktake form, biên bản S22-DN preview (cả 2 scope), biên bản kiểm kê preview, Sổ S22-DN report via Playwright MCP. Cosmetic fixes implement + commit. Structural proposals → append với `## Session YYYY-MM-DD HH:MM Phase 3` header.
19. **Bug fix loop**: critical bugs → systematic-debugging → fix → retest. Commit atomically.
20. **Phase 3 checkpoint commit**: `git commit -m "feat(asset-polishing): Phase 3 bàn giao + kiểm kê complete + QA pass"`

### Phase 4: Demo Data + Final Integration QA + Docs

**Outcome:** Demo data displays in UI; unit tests Tier 1 pass; final end-to-end integration QA confirms cross-phase flows work; CODEBASE.md + FEATURES.md updated; ready to merge.

Per-phase QA already done in Phase 1/2/3 gates. This phase adds: cross-phase integration test, demo data, unit tests, docs update.

Sub-tasks:
1. Demo data via dcnet_sample patch (or vn_accounting setup_demo if dcnet_sample unavailable):
   - 10 TSCĐ (5 ghi tăng từ PI seed, 5 backdated) — varied categories
   - 20 CCDC Items (10 đang phân bổ, 5 hết phân bổ, 5 đã ghi giảm) — varied categories
   - 5 Asset Handovers (3 TSCĐ + 2 CCDC) to different departments
   - 1 Asset Stocktake at "Văn phòng Hà Nội" location, Approved with 1 Mất + 1 Hỏng
2. Run unit tests Tier 1 (per design §12.1): test_ccdc_allocation, test_permission_sync, test_asset_repair_classification, test_stocktake_diff_calc, test_s21_dn_report. Fix failures. Use `bench --site dcnet.localhost console` + unittest (run-tests xung đột với sample data).
3. **Cross-phase integration QA — full lifecycle (`qa-screenshots/phase4-integration/`)**:
   - Mua TSCĐ qua PI → ghi tăng Asset → bàn giao phòng IT (S22-DN print) → tháng sau khấu hao auto chạy → sửa chữa lớn vốn hóa → kiểm kê cuối quý → thanh lý
   - Mua CCDC qua PI auto-create → xuất dùng phân bổ → bàn giao phòng IT → 12 tháng phân bổ chạy đủ → ghi giảm
   - Verify: GL Entry chain consistent, Asset.status đúng từng bước, custodian update correct
   - Console errors == 0 toàn flow
4. **Final Design QA exploratory** (`docs/design-qa-proposals/asset-polishing.md`): nếu phát hiện vấn đề mới sau khi tất cả phases tích hợp với demo data thật, append `## Session YYYY-MM-DD HH:MM Final Integration` section. Cosmetic fix + commit.
5. Update `docs/CODEBASE.md`: list 9 new DocTypes + relationships. Update `docs/CODEBASE_DETAIL.md`: 1 line per new file.
6. Update `FEATURES.md`: mark C4.1 (Khấu hao chuẩn VN — partial) C4.2 (Sổ TSCĐ S21-DN — Done), C4.3 (CCDC phân bổ TK 242 — Done) as Done; add new rows for Bàn giao S22-DN, Kiểm kê TSCĐ/CCDC, Sửa chữa lớn vốn hóa.
7. Update `README.md` if needed: add asset-polishing to feature list.
8. Final commit: `feat(asset-polishing): v1.0 ship — TT99/2025 compliance, full TSCĐ + CCDC lifecycle`.

## Acceptance Criteria

Each criterion must be checkable by an agent. Outcome-based, not inventory-based.

### Phase 0 Plan
- [ ] File `docs/superpowers/plans/2026-04-29-asset-polishing-plan.md` exists, ≥300 lines, contains "## Self-Review Notes" section
- [ ] Plan committed (git log shows commit on feat/asset-polishing referencing the plan file)

### Phase 1 Foundation + TSCĐ Polish
- [ ] `bench --site dcnet.localhost console` returns "Chi phí trả trước" for `frappe.db.get_value("Account", {"account_number":"242", "company":<any test company>}, "account_name")`
- [ ] `bench --site dcnet.localhost console` shows Asset.depreciation_method options as ["Đường thẳng", "Số dư giảm dần"] only (verify via Property Setter query)
- [ ] Sidebar JSON has 2 sections "TSCĐ" and "CCDC" replacing "TSCĐ & CCDC" (verify via grep on workspace_sidebar JSON)
- [ ] Asset Repair has Custom Field `repair_classification`; classification != "Chi phí" + submit creates JE with TK 241 (verify GL Entry)
- [ ] VN Accounting Settings tab "Phân quyền TSCĐ & CCDC" loads in browser (Playwright snapshot saved to `qa-screenshots/phase1-ktt/settings-tab.png`)
- [ ] `frappe.get_single("VN Accounting Settings")` has `permission_matrix` Table field with ≥15 default rows after `reset_permission_matrix()` call
- [ ] Custom DocPerm rows match permission_matrix after Settings save (verify SQL: count by parent in 9 affected DocTypes ≥15)
- [ ] Sổ S21-DN report renders with TT99 columns when accessed via `/app/query-report/Sổ TSCĐ S21-DN` (Playwright snapshot to `qa-screenshots/phase1-kttsm/s21-dn.png`)

### Phase 1 QA Gate
- [ ] `qa-screenshots/phase1-ktt/` contains ≥4 PNG (Settings tab, edit rule, threshold change, reset defaults)
- [ ] `qa-screenshots/phase1-kttsm/` contains ≥4 PNG (sidebar 2 sections, asset form labels, asset repair JE, S21-DN report)
- [ ] `docs/design-qa-proposals/asset-polishing.md` contains `## Session ` header với "Phase 1" mention
- [ ] Phase 1 checkpoint commit exists on `feat/asset-polishing` (grep commit message "Phase 1 foundation")
- [ ] No critical bugs unresolved at Phase 1 end (verify: no `[ ]` items in session-last.md learnings labeled "Phase 1 critical")

### Phase 2 CCDC Backbone
- [ ] PI submit with item.is_low_value_asset=1 → exactly 1 CCDC Item draft created with matching cost (verify via `frappe.db.count("CCDC Item", {"purchase_invoice": pi.name})`)
- [ ] CCDC Item submit creates JE N 242 / C 153 (verify GL Entry rows)
- [ ] CCDC Allocation Schedule created with N entries summing to CCDC Item.cost (verify SQL)
- [ ] Manual scheduler trigger `bench execute vn_accounting.tasks.allocate_ccdc_monthly` posts first Pending entry → JE N expense / C 242 verify GL
- [ ] CCDC Writeoff submit clears remaining 242: GL Entry sum on TK 242 for CCDC = 0 after writeoff
- [ ] Sidebar CCDC links route to existing DocTypes (no 404)

### Phase 2 QA Gate
- [ ] `qa-screenshots/phase2-kttsm/` contains ≥6 PNG (PI auto-create, CCDC submit, Allocation Schedule, scheduler post, Writeoff, biên bản ghi giảm)
- [ ] `docs/design-qa-proposals/asset-polishing.md` contains `## Session ` header với "Phase 2" mention
- [ ] Phase 2 checkpoint commit exists (grep "Phase 2 CCDC backbone")
- [ ] No critical bugs unresolved at Phase 2 end

### Phase 3 Bàn giao + Kiểm kê
- [ ] Asset Handover (scope=TSCĐ) submit updates Asset.custodian + Asset.location (verify SQL on tabAsset)
- [ ] Asset Handover with scope=TSCĐ + add CCDC Item to child → ValidationError raised (verify by attempting via console)
- [ ] Asset Handover threshold: total_asset_value >= 100tr without co_signer_employee → error
- [ ] Asset Movement record created on TSCĐ handover submit (verify SQL)
- [ ] Asset Handover cancel reverts location/custodian (verify before_handover_snapshot used)
- [ ] Asset Stocktake "Tải danh sách" populates child items from location/department (verify count > 0 with seeded data)
- [ ] Asset Stocktake approve with 1 item physical_status="Mất" creates JE N 1381 / C 211 (verify GL)
- [ ] Sổ S22-DN report renders grouped by location (Playwright snapshot to `qa-screenshots/phase3-ktt/s22-dn.png`)

### Phase 3 QA Gate
- [ ] `qa-screenshots/phase3-kttsm/` contains ≥5 PNG (Handover TSCĐ, Handover CCDC, biên bản S22-DN cả 2 layouts, Stocktake create, copy-toolbar)
- [ ] `qa-screenshots/phase3-ktt/` contains ≥4 PNG (Stocktake approve, GL chênh lệch, threshold validation, S22-DN report)
- [ ] `qa-screenshots/phase3-deptHead/` contains ≥3 PNG (filtered Asset list, no-permission error, no-create button)
- [ ] `docs/design-qa-proposals/asset-polishing.md` contains `## Session ` header với "Phase 3" mention
- [ ] Phase 3 checkpoint commit exists (grep "Phase 3 bàn giao")
- [ ] No critical bugs unresolved at Phase 3 end

### Phase 4 Demo Data + Final Integration QA + Docs
- [ ] Demo data: ≥10 Asset + ≥20 CCDC Item + ≥5 Asset Handover + ≥1 Asset Stocktake submitted (verify SQL counts)
- [ ] Unit tests pass: 5 unit test modules ≥80% coverage. Use `bench --site dcnet.localhost console` + unittest (run-tests xung đột với sample data per memory).
- [ ] `qa-screenshots/phase4-integration/` contains ≥8 PNG (full TSCĐ lifecycle + full CCDC lifecycle screenshots)
- [ ] Cross-phase integration QA: GL Entry chain consistent across mua → bàn giao → khấu hao → kiểm kê → thanh lý (verify SQL aggregate)
- [ ] Console errors == 0 across full integration flow
- [ ] CODEBASE.md updated: contains "CCDC Item" and "Asset Handover" mentions (grep)
- [ ] FEATURES.md updated: C4.1, C4.2, C4.3 marked Done (grep "C4.1.*Done")
- [ ] Final commit message references "asset-polishing v1.0 ship"

### Standard Criteria
- [ ] `bench --site dcnet.localhost migrate` succeeds with 0 errors (final state)
- [ ] `bench build --app vn_accounting` succeeds with 0 errors (final state)
- [ ] No file in vn_accounting/ exceeds 800 lines hard limit
- [ ] All commits on feat/asset-polishing follow conventional commits format

## Constraints

- Do NOT modify ERPNext core files in `apps/erpnext/` — use Custom Field, Property Setter, monkey-patch in vn_accounting only
- Do NOT modify Frappe core files in `apps/frappe/`
- Do NOT delete or rename existing Asset Disposal DocType (already merged in main, preserve compatibility)
- Do NOT change sidebar item ordering for non-TSCĐ/CCDC sections (Quỹ tiền mặt, Ngân hàng, etc.)
- Do NOT skip QA when site has data — always work on dcnet.localhost which has demo data
- File size: hard limit 800 lines per file; target ≤500 lines (per programming.md rules)
- Performance: scheduler `allocate_ccdc_monthly` must complete < 60s for site with 100 active CCDC
- Translations: VN Unicode required (no asciified Vietnamese); ERPNext labels stay English in JSON, translation via vi.csv only
- Permission Matrix sync: do NOT delete Custom DocPerm rows for DocTypes outside the 9 affected ones
- DocType naming: English internal names (CCDC Item, Asset Handover); Vietnamese only in `label` and translations
- All print formats: Times New Roman 12pt, A4 portrait, follow asset_disposal_report pattern
- Use `frappe.qb` (query builder) or parameterized SQL for all DB queries (no f-string SQL)

## Verification Commands

test -f docs/superpowers/specs/2026-04-29-asset-polishing-design.md
test -f docs/superpowers/plans/2026-04-29-asset-polishing-plan.md
grep -q "Self-Review Notes" docs/superpowers/plans/2026-04-29-asset-polishing-plan.md
grep -q '"242"' vn_accounting/chart_of_accounts/vn_small_enterprise.json
grep -q "Chi phí trả trước" vn_accounting/chart_of_accounts/vn_small_enterprise.json
test -f vn_accounting/fixtures/asset_permission_defaults.json
python3 -c "import json; d=json.load(open('vn_accounting/fixtures/asset_permission_defaults.json')); assert isinstance(d, list) and len(d) >= 15, f'expected >=15 default rules, got {len(d)}'"
python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/vn_accounting.json')); parents=[i.get('label','') for i in d['items'] if i.get('child')==0]; tscd=[p for p in parents if p.strip()=='TSCĐ']; ccdc=[p for p in parents if p.strip()=='CCDC']; assert len(tscd)==1 and len(ccdc)==1, f'sidebar must have 2 separate sections (exact label TSCĐ and CCDC); parents={parents}'"
test -d vn_accounting/vn_accounting/doctype/ccdc_item
test -d vn_accounting/vn_accounting/doctype/ccdc_category
test -d vn_accounting/vn_accounting/doctype/ccdc_allocation_schedule
test -d vn_accounting/vn_accounting/doctype/ccdc_writeoff
test -d vn_accounting/vn_accounting/doctype/asset_handover
test -d vn_accounting/vn_accounting/doctype/asset_handover_item
test -d vn_accounting/vn_accounting/doctype/asset_stocktake
test -d vn_accounting/vn_accounting/doctype/asset_stocktake_item
test -d vn_accounting/vn_accounting/doctype/asset_permission_rule
grep -q "repair_classification" vn_accounting/fixtures/custom_field.json
grep -q "is_low_value_asset" vn_accounting/fixtures/custom_field.json
grep -q "depreciation_method" vn_accounting/fixtures/property_setter.json
test -d vn_accounting/vn_accounting/print_format/asset_handover_s22_dn
test -d vn_accounting/vn_accounting/print_format/asset_stocktake_report
test -d vn_accounting/vn_accounting/print_format/ccdc_writeoff_report
test -d vn_accounting/vn_accounting/print_format/asset_repair_report
test -d vn_accounting/vn_accounting/report/s21_dn_so_tscd
test -d vn_accounting/vn_accounting/report/s22_dn_theo_doi_tscd_ccdc
test -f docs/design-qa-proposals/asset-polishing.md
grep -q "## Session 2026-" docs/design-qa-proposals/asset-polishing.md
grep -qE "C4\.1.*Done|C4\.2.*Done|C4\.3.*Done" FEATURES.md
grep -qi "ccdc item" docs/CODEBASE.md
grep -qi "asset handover" docs/CODEBASE.md
test -d qa-screenshots/phase1-ktt
test -d qa-screenshots/phase1-kttsm
test -d qa-screenshots/phase2-kttsm
test -d qa-screenshots/phase3-kttsm
test -d qa-screenshots/phase3-ktt
test -d qa-screenshots/phase3-deptHead
test -d qa-screenshots/phase4-integration
sh -c 'count=$(find qa-screenshots/phase1-ktt -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 4'
sh -c 'count=$(find qa-screenshots/phase1-kttsm -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 4'
sh -c 'count=$(find qa-screenshots/phase2-kttsm -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 6'
sh -c 'count=$(find qa-screenshots/phase3-kttsm -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 5'
sh -c 'count=$(find qa-screenshots/phase3-ktt -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 4'
sh -c 'count=$(find qa-screenshots/phase3-deptHead -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 3'
sh -c 'count=$(find qa-screenshots/phase4-integration -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 8'
git log --oneline feat/asset-polishing | grep -qE "Phase 1 foundation"
git log --oneline feat/asset-polishing | grep -qE "Phase 2 CCDC backbone"
git log --oneline feat/asset-polishing | grep -qE "Phase 3 bàn giao"
find vn_accounting -name "*.py" -not -path "*/node_modules/*" -exec wc -l {} + 2>/dev/null | awk 'NF==2 && $1>800 {print "OVERSIZE:", $0; over=1} END {exit over+0}'
git log --oneline main..feat/asset-polishing | head -1 | grep -qE "."

## Live Testing Procedure

These steps are run by the agent inside its session, not by the runner.

### Setup
1. `cd /home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing` (working dir)
2. After DocType JSON or Python changes: `cd /home/long/long/frappe-bench-dcnet && git -C apps/vn_accounting checkout --detach feat/asset-polishing && bench --site dcnet.localhost migrate && bench build --app vn_accounting && bench --site dcnet.localhost clear-cache`
3. **NOTE on worktree dance:** apps/vn_accounting is a separate checkout from the worktree. After committing in the worktree, run `git -C apps/vn_accounting checkout --detach feat/asset-polishing` to sync apps/ to the latest commit. If you edit in apps/ by mistake, force-update the branch ref: `git branch -f feat/asset-polishing <new-sha>` then re-detach.

### Browser QA per Phase
After each Phase's main work, use Playwright MCP (preferred for stateful auth) to:
1. Navigate to `http://dcnet.localhost:8001/app/<form-route>`
2. Test golden path: open form → fill → save → submit
3. Capture console: `mcp__plugin_playwright_playwright__browser_console_messages`
4. Take screenshot to `qa-screenshots/<phase>/<scenario>.png` via `mcp__plugin_playwright_playwright__browser_take_screenshot`
5. Verify GL Entries via `bench --site dcnet.localhost execute frappe.db.sql --kwargs "{'query': 'SELECT account, debit, credit FROM \`tabGL Entry\` WHERE voucher_no=...'}"`

### Test running
- Prefer `bench --site dcnet.localhost console` + `unittest.TestLoader().loadTestsFromModule(...)` over `bench run-tests` (run-tests crashes on dev sites with sample data per memory `feedback_multi_prep_task_data_gen`)

### Rollback if needed
- Worktree commits are preserved; `git checkout main` in apps/vn_accounting then `git -C apps/vn_accounting checkout --detach feat/asset-polishing` to retry

## Agent Persona

You are a senior Frappe/ERPNext developer with deep VAS (Vietnamese Accounting Standards) expertise. You know:

- TT99/2025/TT-BTC accounting circular (effective 2026-01-01) — TK structure, S21-DN/S22-DN forms
- ERPNext Asset module internals — Asset, Asset Movement, Asset Repair, Asset Depreciation Schedule
- Frappe customization patterns — Custom Field, Property Setter, Custom DocPerm, monkey-patching, fixtures (NOT direct ERPNext core edits)
- VN translations pattern — `apps/<app>/<app>/translations/vi.csv` (2-col CSV, Frappe auto-loads from disk per `frappe-spa.md` memory)
- Frappe v16 specifics — bundle.js naming, sidebar Custom DocPerm, `route_options` for filter, `frappe.ready()` removed → use `$(document).ready()`

You always:
- Read the design spec FIRST every session (`docs/superpowers/specs/2026-04-29-asset-polishing-design.md`) — it is source of truth
- Read session-last.md if it exists — pick up "Next Session Task" focused goal
- Use `frappe.get_doc(...).save()` not `frappe.db.set_value` for cacheable DocTypes (per `frappe-spa.md` memory)
- Use `frappe.qb` or parameterized SQL — never f-string SQL
- Commit early, commit often — uncommitted work is lost if session killed
- Use `setsid -f` for long-running commands; never `nohup &` (blocks on stdio)
- Never modify ERPNext core; use override patterns
- Never use `bench --site clear-cache` while user is logged in (kills session)
- Verify each Phase outcome via `bench console` + SQL before claiming complete

You NEVER:
- Skip self-review of plan in Phase 0
- Mark a criterion `[x]` without evidence (verification command output, GL Entry rows, file existence)
- Continue past 90% time warning — STOP and write session-last.md
- Use bare `&` for background processes — use `setsid -f`
- Edit files directly on VPS — local first, commit, push, deploy

## Model

auto

## Time Budget

- Max hours: 20 (bumped from 15 to accommodate per-phase QA per Option B)
- Max sessions: 40 (safety limit; expected ~30 sessions: 5/phase impl + 3-4/phase QA + 4 Phase 4)
- Per-session minutes: 30

**Per-phase session estimate:**
- Phase 0 plan: 1 session
- Phase 1: 4-5 impl + 2-3 QA = ~7 sessions
- Phase 2: 5-6 impl + 2 QA = ~7 sessions
- Phase 3: 5-6 impl + 3-4 QA (3 personas) = ~9 sessions
- Phase 4: 4 sessions (demo + integration QA + docs)
