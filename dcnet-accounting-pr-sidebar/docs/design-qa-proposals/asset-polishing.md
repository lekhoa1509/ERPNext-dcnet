# Design QA Proposals — Asset Polishing

## Session 2026-04-29 Phase 3 Bàn giao + Kiểm kê

### Verified via console / browser
- Asset Handover scope=TSCĐ submit: Asset.location DC HCM → DC Hà Nội, Asset.custodian updated (verified SQL)
- Asset Movement ACC-ASM-2026-00429 created automatically on TSCĐ handover submit (purpose=Transfer, from DC HCM → DC Hà Nội)
- Asset Stocktake spkcjijm8l: 75 TSCĐ items loaded via "Tải danh sách" button, 1 item marked "Mất"
- Scope validation: CCDC Item in TSCĐ scope → ValidationError raised correctly
- S22-DN report renders correctly with TSCĐ records grouped by location (0 console errors)
- Department Head role user (no Asset access): "Not permitted" error on Asset list + Asset record access

### Bugs fixed in this phase
- `gross_purchase_amount` → `total_asset_cost` in both asset_stocktake.py and s22-dn report
- Asset Movement field `to_location` → `target_location` (ERPNext child row field name)
- `_create_asset_movement()` must run BEFORE `_update_targets()` — otherwise source == target location error
- Print formats had `doc_type: "Asset"` instead of their respective DocTypes — fixed both
- asset_handover.js: was setting `target_doctype` field options to Asset (wrong), now sets `target_name` options via `update_docfield_property`

### Proposals
- ✅ Applied 2026-04-29 — Asset Handover form: "Hành động" button group — added "Xem biên bản" quick-preview alongside "In biên bản"
- ✅ Applied 2026-04-29 — Asset Stocktake: summary row at bottom of stocktake_items showing counts (Còn nguyên / Hỏng / Mất / Thiếu)
- ✅ Applied 2026-04-29 — Asset Handover: co_signer field highlighted yellow when total_asset_value ≥ 80% of handover_threshold
- ✅ Applied 2026-04-29 — Print format S22-DN: `@media print` CSS — table headers repeat, rows + signature block don't split mid-page

## Session 2026-04-29 Phase 2 CCDC Backbone

### Verified via console
- CCDC Item submit → JE N 242 / C 153 auto-submitted (GL entries confirmed)
- CCDC Allocation Schedule: 3 periods, sum = cost, per-period rounding correct
- Scheduler: posts Period 1 → JE N 6413 / C 242 auto-submitted (GL entries confirmed)
- CCDC Writeoff: remaining_242 calculated correctly (5000000), JE N 6413 / C 242 posted, schedule→Cancelled, status→"Đã ghi giảm"

### Auto-fixed
- Changed `_lookup_account` to use `account_number` field (not `account_name LIKE`) — more reliable
- Changed default CCDC expense account from TK 627 to TK 6413 (Chi phí dụng cụ, đồ dùng) per DCNET COA
- Auto-submit CCDC JEs (routine entries); keep Asset Repair JE as Draft for accountant review

### Proposals
- ✅ Applied 2026-04-29 — CCDC Item form: added "Lịch phân bổ" custom button after submit for quick navigation to Allocation Schedule list
- ✅ Applied 2026-04-29 — CCDC Writeoff form: `remaining_242_amount` and `remaining_153_amount` auto-fetched via `get_writeoff_preview` whitelisted method when `ccdc_item` set, before submit
- ✅ Applied 2026-04-29 — Allocation Schedule list view: added "Tiến độ" column (`progress_text` field) showing posted/total ratio, populated in `before_save`

## Session 2026-04-29 Phase 1

### Auto-fixed
- (none yet — Phase 1 QA not run yet; screenshots pending bench migrate)

### Proposals
- ✅ Applied 2026-04-29 — Settings "Phân quyền TSCĐ & CCDC" tab: 3 threshold fields (disposal/handover/min_asset_value) grouped under collapsible Section Break "Ngưỡng giá trị"
- ✅ Applied 2026-04-29 — S21-DN report column "GTKH luỹ kế" renamed to "KH luỹ kế" for cleaner table display
- ✅ Applied 2026-04-29 — Sidebar CCDC section: "Phân bổ CCDC" → "Lịch phân bổ CCDC" to clarify it shows the schedule list, not an allocate action

## Session 2026-04-29 v1.2 Browser QA Pass

### All P0 Verified via Browser (Playwright MCP)

- ✅ PM-24 (P0-3): Asset Stocktake new form — Công ty auto-fills "DCNET" (screenshot: qa-screenshots/v1.2-fixes/PM-24-stocktake-company-default.png)
- ✅ PM-29 (P0-2): S21-DN report — opens from sidebar, renders 21+ asset rows, 0 console errors (screenshot: qa-screenshots/v1.2-fixes/S21-DN-working.png, sidebar-smoke-s21dn.png)
- ✅ PM-03 (P0-4): Asset Repair — opens from Kế Toán VN sidebar with breadcrumb "Kế Toán VN / Sửa chữa tài sản" (screenshot: qa-screenshots/v1.2-fixes/PM-03-asset-repair-ktvn-sidebar.png)
- ✅ PM-06 (P0-6): S22-DN print — no raw JSON visible, clean print with Phạm vi/Ngày đăng/Công ty/table/Tổng (screenshot: qa-screenshots/v1.2-fixes/PM-06-s22dn-print-preview.png)
- ✅ PM-04 (sidebar): 16 items across TSCĐ (9) + CCDC (7) sections — all present (console-verified via JS enumeration)

### Smoke Test Results
- S22-DN report: 21+ rows, 0 errors ✓
- Danh sách CCDC (CCDC Item list): loads correctly ✓
- Kiểm kê TSCĐ (Asset Stocktake list): loads correctly ✓
- Thanh lý (Asset Disposal list): loads correctly ✓
- Bàn giao TSCĐ (Asset Handover list): verified via earlier session PM-03 ✓

### Root Causes Found This Session (not in Session 1 notes)
1. S21-DN SQL: `tabAsset` v16 renamed `gross_purchase_amount` → `total_asset_cost`; `accumulated_depreciation_amount` must be computed as `total_asset_cost - value_after_depreciation`; `notes` field does not exist (use NULL)
2. Workspace sidebar sync direction: `bench migrate` exports DB→JSON, NOT imports JSON→DB. Session 1 edited JSON only — changes never reached DB. Fixed via direct DB update (118-item sidebar) + custom Python export.
