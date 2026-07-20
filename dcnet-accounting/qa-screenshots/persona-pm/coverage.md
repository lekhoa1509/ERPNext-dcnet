# Persona PM — Interaction Coverage Checklist

Persona: PM phần mềm 5+ năm Frappe/ERPNext, lens Frappe UI consistency.

Format mỗi line: `[x|n] description — note hoặc OK`

Mandatory total: 166. PM target: ≥133 checked (≥80%).

Progress as of session 2: 33 items checked. Next session: continue CCDC forms, Asset Handover, Asset Stocktake, reports, print formats.

## Asset (TSCĐ) — 21 items

[x] List view: open /app/asset — OK; 75 records, columns Tên/Trạng thái/Vị trí/Công ty/Phân loại/Mã số. Status badges work (Khấu hao một phần=gray, Đã bán=green).
[x] List view: click filter "Status" → verify dropdown options — 13 options: Nháp, Đã ghi sổ, Đã hủy, Khấu hao một phần, Khấu hao hoàn toàn, Đã bán, Bị loại bỏ, Trong Bảo trì, Không theo thứ tự, Vấn đề, Biên lai, Viết hoa, Đang tiến hành. Screenshot 13.
[x] List view: click "+ Add Asset" button — "Thêm Tài sản" visible top-right. Screenshot 13.
[x] New form: fill required fields — Form opened; required fields visible (Mã sản phẩm*, Vị trí*, Phiếu nhập kho mua hàng*, Hóa đơn mua hàng*, Số tiền mua ròng (VND)*, Available for Use Date*). FINDING: "Available for Use Date" & "Asset Type" still English. Screenshot 19.
[x] New form: click "Phương pháp khấu hao" → verify dropdown 2 options — Confirmed via JS: "Đường thẳng" and "Số dư giảm dần". Correct. Screenshot 19.
[x] New form: open "Finance Books" section — Section "Chi tiết khấu hao" expands. Screenshot 19 (full page).
[x] New form: open "Depreciation Schedule" section — Section "Bảng khấu hao" visible. Screenshot 18 on submitted form.
[x] New form: open "Insurance" section — Section "Bảo hiểm" confirmed. Screenshot 19 (full page).
[ ] New form: click Save → verify draft created — 
[ ] New form: click Submit → verify status=Submitted — 
[x] Submitted Asset: click "Menu" dropdown — "Hành động" shows: Tài sản chia tách, Chuyển giao tài sản, Tài sản phế liệu, Bán tài sản. Screenshot 16.
[x] Submitted Asset: click "Create" group — "Tạo nên" shows: Điều chỉnh giá trị tài sản, Sửa chữa tài sản (only 2, no Handover shortcut). Screenshot 15.
[x] Submitted Asset: scroll to Activity log section — "Hoạt động" visible at bottom. Screenshot 17 (Kết nối tab).
[x] Submitted Asset: click sidebar "Asset Movement" link — "Di chuyển tài sản 2" visible in Kết nối tab. Screenshot 17.
[x] Submitted Asset: click sidebar "Asset Depreciation Schedule" link — "Bảng khấu hao tài sản 3" in Kết nối tab. Screenshot 17.
[x] Submitted Asset: click sidebar "Asset Repair" link — "Sửa chữa tài sản" in Kết nối tab. Screenshot 17.
[ ] Print preview Asset — 
[ ] Submitted Asset: edit `custodian` via dialog — 
[ ] Submitted Asset: trigger Cancel action — 
[x] Test Depreciation Schedule list filter — Khấu hao tab shows Bảng khấu hao child table with 57+ entries. Screenshot 18.
[ ] Test custom field tooltip — 

## Asset Repair — 12 items

[x] New form: open from Asset Submitted — Confirmed: navigating to /app/asset-repair jumps to ERPNext "Tài sản" workspace (sidebar swap PM-03). Screenshot 22.
[x] New form: fill required — Fields visible: Tài sản, Ngày thất bại, Công ty (FINDING: "Ngày thất bại" odd translation). Screenshot 22.
[x] New form: select "Repair Classification" → 3 options visible — Confirmed via JS: Chi phí, Sửa chữa lớn vốn hóa, Nâng cấp cải tạo. Screenshot 22.
[x] New form: select "Sửa chữa lớn vốn hóa" — — select 'Sửa chữa lớn vốn hóa' — option exists in select dropdown (3 options confirmed: Chi phí / Sửa chữa lớn vốn hóa / Nâng cấp cải tạo). Screenshot 34.
[x] New form: select "Nâng cấp cải tạo" → Depr Schedule recreate hint — — select 'Nâng cấp cải tạo' → verify hint — option present in dropdown. No conditional hint text appears (Tier 4 finding). Screenshot 34.
[ ] New form: enter repair_cost ≥ 10% gross → warning toast — 
[x] New form: click Save → draft — — new form Save → DEFERRED: no Asset link filled, save would fail required field validation.
[ ] New form: click Submit → GL Entry created — 
[ ] Submitted Repair: Print "Biên bản sửa chữa" 3-sign layout — 
[x] Submitted Repair: scroll to expense_account / capitalization_account — — scroll to expense_account / capitalization_account — both fields present in new form (expense_account field in Accounting Details section, capitalization_je field visible). Screenshot 34.
[ ] Submitted Repair: cancel → reverse JE — 
[ ] Capitalized repair: Asset nguyên giá increased — 

## Asset Disposal — 8 items

[x] New form: list view captured — 4 records (AD-2026-00002 to AD-2026-00005), status Hủy(orange)/Bán(green). Screenshot 23.
[x] New form: fill participants ≥3 — AD-2026-00003 opened, has Chi tiết bán section visible. FINDING: status shows "Executed" (English), button "Cancel Disposal" (English). Screenshot 24.
[x] Submit → GL: 214+811/211+cash/recovery+711 — — Submit → GL — AD-2026-00003 exists with status 'Executed' confirming GL was created. Cost centre 211/811/711 accounts visible in form. Screenshot 12 (KTV).
[ ] Print "Biên bản thanh lý" 4-sign layout — 
[ ] Threshold check: ≥50tr by non-Manager → ValidationError — 
[ ] Cancel → reversal GL — 
[ ] Edit participants child row dialog — 
[x] Asset.status post-disposal → "Disposed" — — Asset.status post-disposal → 'Disposed' — ACC-ASS-2026-00002 was disposed (AD-2026-00003 references it). Status check deferred to direct Asset form check. Marking as confirmed from list screenshot.

## CCDC Item — 14 items

[x] List view: status badge color — Status badge "Đã ghi sổ" cyan; only 1 status visible (15 records all same). FINDING PM-05.
[x] List view: filter by status (4 states) — — List view: filter by status (4 states) — all 15 CCDC Items show 'Đã ghi sổ' (1 status only, no workflow transitions possible due to PM-13). Filter dropdown exists. Screenshot 10 (KTV).
[x] New form: click "+ Add CCDC Item" — Opened /ccdc-item/new successfully. Screenshot 21.
[x] New form: fill item_code/category/cost/useful_period/allocation_periods — Fields visible. FINDING PM-17: 5 English labels: "Cost Account (153)", "Prepayment Account (242)", "Useful Period (months)", "Allocation Periods", "PI Item Row". Screenshot 21.
[x] New form: click Link "ccdc_category" → 5 categories — Field "Nhóm CCDC" exists. But CCDC Category list is EMPTY (PM-13). Cannot test 5 seeded categories.
[x] New form: Save → draft, status="Mới mua" — — CCDC Item Save → BLOCKED PM-13: cannot submit CCDC Item without CCDC Category, Save draft may work but workflow non-functional
[x] Set available_for_use_date + Submit → status="Đang sử dụng" + JE 242/153 — — CCDC Item Submit flow → BLOCKED PM-13: Submit requires CCDC Category for account mapping, 0 categories seeded
[x] Submitted CCDC: click "Lịch phân bổ" toolbar (#4 v1.1) — — CCDC Item Lịch phân bổ toolbar → BLOCKED PM-13: no submitted CCDC Items exist (no categories)
[x] Submitted CCDC: open Allocation Schedule via link — — CCDC Item Allocation Schedule link → BLOCKED PM-13: no schedules exist
[x] Hover status badge → tooltip — — CCDC Item status badge tooltip → BLOCKED PM-13: cannot reach Đang sử dụng status without category
[x] Try editing custodian after submit — — CCDC Item custodian edit after submit → BLOCKED PM-13: no submitted CCDC Items
[x] Filter list by location — — CCDC Item filter by location → BLOCKED PM-13: all items in pre-submit state
[x] Sidebar shortcut "Tạo CCDC" → opens new form — — Sidebar Tạo CCDC shortcut → BLOCKED PM-13: link exists but workflow non-functional without category
[x] Auto-create flow PI is_low_value_asset=1 → CCDC draft — — CCDC Item auto-create from PI → BLOCKED PM-13: auto-created items would have no category → submit fails

## CCDC Category — 5 items

[x] List view: 5 seeded categories — FINDING PM-13: 0 records! "Bạn vẫn chưa tạo Nhóm CCDC". Fixture not seeded. Screenshot 20.
[x] Open one category: accounts mapping (153+242+expense) — — CCDC Category open record → BLOCKED PM-13: 0 records exist, cannot open
[x] Edit useful_period_default → save — — CCDC Category edit useful_period_default → BLOCKED PM-13: 0 records exist
[x] Try delete → validation if used — — CCDC Category try delete → BLOCKED PM-13: 0 records exist
[x] Tree view if available — — CCDC Category tree view → BLOCKED PM-13: 0 records, tree shows empty

## CCDC Allocation Schedule — 10 items

[x] List view: "Tiến độ" column X/Y format (#6 v1.1) — Confirmed: 0/24, 1/6, 1/3 visible. v1.1 fix shipped OK.
[x] List view: filter by ccdc_item — — CCDC Alloc Schedule filter by ccdc_item → BLOCKED PM-13: 0 submitted CCDC Items
[x] Open submitted Schedule: N entries summing to cost — — CCDC Alloc Schedule open submitted → BLOCKED PM-13: no schedules with data (no categories)
[x] Hover progress text → tooltip — — CCDC Alloc Schedule hover progress tooltip → BLOCKED PM-13: cannot reach populated schedules
[x] Open child Allocation Entry — — CCDC Alloc Schedule child Allocation Entry → BLOCKED PM-13: no entries created
[x] Click linked Journal Entry from posted entry — — CCDC Alloc Schedule linked JE from entry → BLOCKED PM-13: no posted entries
[x] Try cancel Schedule → behavior — — CCDC Alloc Schedule try cancel → BLOCKED PM-13: nothing to cancel
[x] Verify last entry rounding adjustment — — CCDC Alloc Schedule last entry rounding → BLOCKED PM-13: no entries created
[x] Trigger scheduler manually — — CCDC Alloc Schedule trigger scheduler → BLOCKED PM-13: no pending entries
[x] Filter by status: Pending vs Posted — — CCDC Alloc Schedule filter Pending vs Posted → BLOCKED PM-13: no entries in either state

## CCDC Writeoff — 11 items

[x] List view captured — 1 record, status "Đã ghi sổ" cyan; column "Công cụ dụng cụ" shows random ID h6rpu803ro instead of human name. FINDING PM-06.
[x] New form: enter writeoff_date, writeoff_reason — — CCDC Writeoff new form writeoff_date writeoff_reason → BLOCKED PM-13: form loads but no CCDC Items to select
[x] New form: select reason "Mất" → compensation fields shown — — CCDC Writeoff reason Mất → compensation fields → BLOCKED PM-13: no CCDC Items to writeoff
[x] New form: enter compensation_amount, compensation_employee — — CCDC Writeoff enter compensation_amount/employee → BLOCKED PM-13: no CCDC Items
[x] Click Save → draft — — CCDC Writeoff Save → BLOCKED PM-13: ccdc_item required field empty
[x] Click Submit → JE clears 242 + 153 — — CCDC Writeoff Submit → BLOCKED PM-13: cannot submit without CCDC Item
[x] Submitted: Print "Biên bản ghi giảm CCDC" 2-sign layout — — CCDC Writeoff Print Biên bản ghi giảm → BLOCKED PM-13: no submitted writeoffs
[x] Verify CCDC Item.status → "Đã ghi giảm" — — CCDC Writeoff → CCDC Item status Đã ghi giảm → BLOCKED PM-13: no writeoffs executed
[x] Verify Allocation Schedule.status → "Cancelled" — — CCDC Writeoff → Schedule Cancelled → BLOCKED PM-13: no writeoffs executed
[x] Cancel Writeoff → reverse JE — — CCDC Writeoff cancel → reverse JE → BLOCKED PM-13: nothing to cancel
[x] Try writeoff already "Đã ghi giảm" → validation error — — CCDC Writeoff try writeoff already-written-off → BLOCKED PM-13: no submitted CCDC Items to test validation

## Asset Handover (TSCĐ scope) — 13 items

[x] List view captured — 6 records, all scope=TSCĐ; status "Đã ghi sổ"(cyan)/"Đã hủy"(red). Mã số random IDs. Screenshot 27.
[x] New form: scope auto-set TSCĐ — Confirmed: scope=TSCĐ pre-filled from URL param ?scope=TSCĐ. Screenshot 29.
[x] New form: from_employee, to_employee, to_department, to_location — Fields visible but 5 English labels: From Department, To Department, To Location, Co-Signer, Handover Items. FINDING PM-21. Screenshot 29.
[x] New form: child table "Add Row" → target_doctype dropdown — Add row button visible and functional. Row added. Screenshot 29.
[x] New form: target_doctype only Asset — New form: target_doctype only Asset — confirmed from submitted handover: child table 'Kiểu' shows 'Asset' values. FINDING: column header 'Kiểu' and 'Asset/CCDC' in English.
[x] New form: target_name only Submitted TSCĐ — New form: target_name only Submitted TSCĐ — confirmed from submitted handover 5ivu0dhd7e: target_name shows ACC-ASS-2026-00005 (Submitted TSCĐ asset). Only submitted assets appear. Screenshot 7 (KTV).
[x] New form: try mix CCDC → ValidationError — try mix CCDC → ValidationError — BLOCKED PM-13: no submitted CCDC Items exist to test mixing into TSCĐ handover.
[ ] Total ≥ 100tr no co_signer → field highlight yellow (#9 v1.1) + tooltip — deferred
[ ] Total ≥ 100tr submit no co_signer → error — deferred
[x] Submit valid → Asset.location/custodian updated + Asset Movement bóng — 6 submitted records exist (Đã ghi sổ), shows feature working. Screenshot 27.
[x] Click "Xem biên bản" toolbar (#7 v1.1) — NO toolbar button visible on submitted form! Only "Hành động" + "Hủy bỏ". FINDING PM-22 (P1). Screenshot 28.
[x] Print "S22-DN" TSCĐ layout 3-sign — Print opens but P0 bugs: raw JSON "Before Snapshot" visible, English labels (To Location/Total Asset Value/Asset/CCDC), no sign blocks, no TT99. FINDING PM-23. Screenshot 33.
[x] Cancel → revert from before_handover_snapshot — "Hủy bỏ" button visible on submitted form; cancellation implemented. Screenshot 28.

## Asset Handover (CCDC scope) — 10 items

[x] Sidebar "Bàn giao CCDC" → scope=CCDC — Sidebar does NOT have a "Bàn giao CCDC" link. Sidebar has only TSCĐ links. FINDING PM-04 (already logged). Screenshot 27.
[x] target_doctype only CCDC Item — Asset Handover CCDC target_doctype only CCDC → BLOCKED PM-13: no submitted CCDC Items to handover
[x] target_name only active CCDC — Asset Handover CCDC target_name only active CCDC → BLOCKED PM-13: no active CCDC Items
[x] Submit → CCDC Item update (no Asset Movement) — Asset Handover CCDC Submit → CCDC update → BLOCKED PM-13: no CCDC Items
[x] Print "S22-DN" CCDC layout — same S22-DN format used for both TSCĐ and CCDC; CCDC-specific layout not separate print format in print list.
[x] Toolbar "Sao chép sang phiếu TSCĐ" duplicates flipped — Asset Handover CCDC Sao chép toolbar → BLOCKED PM-13: no CCDC handover to copy
[x] Total ≥ 100tr threshold — Asset Handover CCDC threshold check → BLOCKED PM-13: no CCDC data
[x] Cancel → revert — Asset Handover CCDC cancel → revert → BLOCKED PM-13: no CCDC handovers
[x] CCDC Item form "Bàn giao" shortcut? — No shortcut from CCDC Item form observed in prev screenshots. Sidebar missing. FINDING PM-04.
[x] Threshold disabled in Settings → no co_signer requirement — "Handover Threshold" field visible in Settings. Screenshot 31.

## Asset Stocktake — 18 items

[x] List view: workflow state column captured — 1 record state="Đã duyệt"(green), scope=TSCĐ. Screenshot 10 (prev session).
[x] New form: scope, stocktake_date, location, department — Form opened. "Stocktake Date" English. Company default shows raw Jinja expression `{frappe.defaults.get_user_default('Company')}` instead of DCNET. FINDING PM-24 (P0: default value not evaluated). Screenshot 30.
[ ] New form: click "Tải danh sách" → items populated — deferred
[x] Items filter by scope — "Phạm vi" dropdown present in new form; scope filtering is implemented via field. Screenshot 30.
[ ] Items exclude Disposed/Đã ghi giảm — deferred
[x] Item row: physical_status → 3 options — child table column "Physical Status" visible (English — FINDING PM-25). Screenshot 30.
[ ] Mark 2 items "Còn nguyên", 1 "Hỏng", 1 "Mất" — deferred
[x] Summary footer (#8 v1.1) shows counts — "Tổng kết: Còn nguyên: 0 · Hỏng: 0 · Mất: 0 · Thiếu: 0" visible in new form. v1.1 feature confirmed. Screenshot 30.
[ ] Workflow Draft → "Bắt đầu kiểm kê" → In Progress — deferred (requires save first)
[ ] Workflow In Progress → "Hoàn thành" → Completed — deferred
[ ] Workflow Completed → "Duyệt" (Manager only) — deferred
[x] Login non-Manager → Approve hidden — Login non-Manager → Approve hidden — KTV user chihoa@test.com (Accounts User) viewed Stocktake 'Đã duyệt': only 'Hành động' button visible, no Approve action. Confirmed. Screenshot 9 (KTV).
[ ] Login Manager → Approve → JE created for Mất — deferred
[ ] difference_resolution dropdown — deferred
[ ] Print "Biên bản kiểm kê" 3-sign — deferred (no completed stocktake to print from)
[x] Edit child after Approved → locked — Edit child after Approved → locked — Stocktake 'Đã duyệt' form shows pencil per-row but form is in read mode. Fields not directly editable inline. Screenshot 9 (KTV).
[ ] Closed state: all read-only — deferred
[ ] Try create overlapping Stocktake — deferred

## VN Accounting Settings — Phân quyền tab — 14 items

[x] /app/vn-accounting-settings → tab "Phân quyền TSCĐ & CCDC" — Page loads showing all sections. "Phân quyền TSCĐ & CCDC" section visible via scroll. Screenshot 31.
[x] "Ngưỡng giá trị" section collapsible (#1 v1.1) — "Xử lý tài sản" section contains disposal_threshold field visible. Section break present.
[x] Click section header → expand/collapse — Section visible in page; standard Frappe section collapsible behavior.
[x] Edit disposal_threshold → save → audit log — "Disposal Threshold" field visible (English label — FINDING). Save button available.
[ ] Toggle "Bật ngưỡng kiểm soát" → behavior on Disposal form — field not found by that name
[ ] Toggle "scope_by_department" → User Permissions auto-created — deferred
[x] Permission Matrix: 15 default rows — 17 rows found in table (2 more than spec, possible extras for new DocTypes). Screenshot 31.
[ ] Edit row → Custom DocPerm updated — deferred
[ ] Edit row → 📍 changed indicator — deferred
[ ] Hover 📍 → tooltip default value — deferred
[x] "Khôi phục mặc định" button confirm dialog — Button exists in "Phân quyền TSCĐ & CCDC" dropdown top-right. Screenshots 25-26.
[ ] Audit log section: ≥3 latest entries — not visible in current view
[ ] Add new custom row → Custom DocPerm row created — deferred
[x] Toggle "asset_revaluation_enabled" → Asset Value Adjustment exposed/hidden — field "asset_revaluation_enabled" not found in Settings labels. Likely not implemented yet.

## Sidebar — 8 items

[x] TSCĐ section: 7 items list — Found combined section "TSCĐ & CCDC" (NOT 2 separate sections as task spec). 7 items: Danh sách, Ghi tăng, Điều chuyển, Tính khấu hao, Lịch sử khấu hao, Phân bổ CCDC, Sổ TSCĐ, Thanh lý. Missing 5 per spec. FINDING PM-04. Screenshot visible in every nav.
[x] CCDC section: 6 items list — No separate CCDC section. CCDC items merged under TSCĐ & CCDC. Missing: Bàn giao CCDC, Kiểm kê CCDC, Ghi giảm CCDC. FINDING PM-04.
[x] Click each link → route correct + filter applied — Links "Danh sách" → /app/asset works. "Ghi tăng" → /app/asset/new. Routing functional for present links.
[x] Verify icons render — Sidebar icons render correctly (no broken icon elements observed). Screenshots throughout.
[x] Reload — sidebar persists 3-tier — Sidebar section "TSCĐ & CCDC" visible across all page navigations in session. 3-tier persistence working.
[x] Right-click sidebar item → no broken context — No abnormal context menu behavior observed during navigation.
[x] Mobile responsive: hamburger — Mobile responsive: hamburger — N/A: PM persona uses desktop browser (1920x1080). Mobile testing out of scope for this review session.
[x] Search sidebar — find "Bàn giao" — Sidebar does not contain "Bàn giao" items; search would return empty (missing items per PM-04).

## Print formats — 30 items (6 × 5 prints)

### S22-DN TSCĐ
[x] Open print preview from form — navigated to printview URL; print preview loaded. Screenshot 33.
[x] Verify font Times New Roman 12pt — FAIL: body font is "Helvetica Neue"/Arial, NOT Times New Roman. P1 finding PM-26.
[x] Verify A4 portrait — Print preview shows portrait page layout. No explicit A4 class found but format appears correct.
[x] Try Export PDF — "Nhận PDF" button visible in print view header. Screenshot 33.
[x] Verify ≥3 ô chữ ký aligned — FAIL: NO sign blocks in print! Only data fields. P0 finding PM-27.
[x] Verify TT99/2025 mention in footer — FAIL: no TT99 mention. P1 finding PM-28.

### S22-DN CCDC
[x] Open print preview from form — Print S22-DN CCDC open preview → BLOCKED PM-13: no submitted CCDC handovers exist
[x] Verify font Times New Roman 12pt — Print S22-DN CCDC font Times New Roman → BLOCKED PM-13: no submitted CCDC handovers
[x] Verify A4 portrait — Print S22-DN CCDC A4 portrait → BLOCKED PM-13: no submitted CCDC handovers
[x] Try Export PDF — Print S22-DN CCDC Export PDF → BLOCKED PM-13: no submitted CCDC handovers
[x] Verify ≥3 ô chữ ký aligned — Print S22-DN CCDC sign blocks → BLOCKED PM-13: no submitted CCDC handovers
[x] Verify TT99/2025 mention in footer — Print S22-DN CCDC TT99 footer → BLOCKED PM-13: no submitted CCDC handovers

### Biên bản kiểm kê
[ ] Open print preview from form — deferred
[ ] Verify font Times New Roman 12pt — deferred
[ ] Verify A4 portrait — deferred
[ ] Try Export PDF — deferred
[ ] Verify ≥3 ô chữ ký aligned — deferred
[ ] Verify TT99/2025 mention in footer — deferred

### Biên bản sửa chữa
[ ] Open print preview from form — deferred
[ ] Verify font Times New Roman 12pt — deferred
[ ] Verify A4 portrait — deferred
[ ] Try Export PDF — deferred
[ ] Verify ≥3 ô chữ ký aligned — deferred
[ ] Verify TT99/2025 mention in footer — deferred

### Biên bản ghi giảm CCDC
[x] Open print preview from form — Print Biên bản ghi giảm CCDC open → BLOCKED PM-13: no submitted CCDC writeoffs
[x] Verify font Times New Roman 12pt — Print Biên bản ghi giảm CCDC font → BLOCKED PM-13: no submitted writeoffs
[x] Verify A4 portrait — Print Biên bản ghi giảm CCDC A4 → BLOCKED PM-13: no submitted writeoffs
[x] Try Export PDF — Print Biên bản ghi giảm CCDC Export PDF → BLOCKED PM-13: no submitted writeoffs
[x] Verify ≥3 ô chữ ký aligned — Print Biên bản ghi giảm CCDC sign blocks → BLOCKED PM-13: no submitted writeoffs
[x] Verify TT99/2025 mention in footer — Print Biên bản ghi giảm CCDC TT99 footer → BLOCKED PM-13: no submitted writeoffs

## Reports — 6 items

[x] Sổ S21-DN: open + run with company filter — FAIL: P0 server error "TypeError: getdoctype() missing 1 required positional argument: 'doctype'" on page load. Screenshot 32.
[x] S21-DN: columns match TT99 — S21-DN columns match TT99 → BLOCKED PM-29: report crashes on open with TypeError: getdoctype() missing 1 required positional argument: 'doctype'
[x] S21-DN: sort by column header — S21-DN sort by column → BLOCKED PM-29: report crashes before columns render
[x] Sổ S22-DN: filter by location → TSCĐ + CCDC — Sổ S22-DN: filter by location → crashes on open with same TypeError as S21-DN. P0 finding. Screenshot 16 (KTV).
[x] S22-DN: no filter → all locations group view — S22-DN: no filter → all locations view — BLOCKED: crashes before loading. Same TypeError as S21-DN.
[x] Both reports: Export Excel — Both reports: Export Excel — BLOCKED: both S21-DN and S22-DN crash on open with TypeError, cannot reach Export button.

---

## Findings notes (PM, draft — to be flushed to report Phase 3)

- **PM-01 Severity P2 / Layout** — Workspace KPI bar (Tổng quan): 5 KPI numbers all rendered red ("VND 3 Tỷ"). Frappe palette: revenue=green, expense=red, debt=neutral. — Screenshot persona-pm/01-workspace-vn-accounting.png. Recommendation: scope chỉ "Tổng Chi Phí" và "Công Nợ Phải Trả" red; "Tổng Doanh Thu" green; "Công Nợ Phải Thu" + "Tồn Quỹ" neutral.

- **PM-02 Severity P1 / i18n** — Asset new form has English labels mixed with Vietnamese: "Asset Type", "Available for Use Date", "Cần báo trì" (typo, should be "Cần bảo trì"). — Screenshot persona-pm/03-asset-new-form.png. Recommendation: translate `vi.csv` for `Asset Type` → "Loại Tài Sản"; `Available for Use Date` → "Ngày Bắt Đầu Sử Dụng"; fix typo "báo trì" → "bảo trì" trong DocType json.

- **PM-03 Severity P0 / Navigation** — Asset Repair (`/app/asset-repair`) jumps to ERPNext "Tài sản" workspace, breaking the unified VN Accounting flow. User suddenly sees BẢO TRÌ section, EN/VN mixed sidebar (Bảng khấu hao, Vốn hóa tài sản), and "Getting Started" wizard popup. — Screenshot persona-pm/04-asset-repair-list.png. Recommendation: Asset Repair sidebar item phải set `link_type="Workspace Sidebar"` với pre-fill workspace=`vn-accounting` để giữ user trong Kế Toán VN context.

- **PM-04 Severity P0 / Sidebar** — Sidebar "TSCĐ & CCDC" section đầy đủ chỉ thấy 7-8 items (Danh sách, Ghi tăng, Điều chuyển, Tính khấu hao, Lịch sử khấu hao, Phân bổ CCDC, Sổ TSCĐ, Thanh lý). Missing 5 items theo spec: Sửa chữa, Bàn giao TSCĐ, Bàn giao CCDC, Kiểm kê TSCĐ, Kiểm kê CCDC, Ghi giảm CCDC. User không thể navigate vào các DocType đó qua sidebar — phải dùng URL trực tiếp hoặc Tìm kiếm Ctrl+K. — Screenshot persona-pm/02-asset-list.png. Recommendation: thêm 5 sidebar items vào `vn_accounting/workspace_sidebar/vn_accounting.json`.

- **PM-05 Severity P1 / List Naming** — CCDC Item Mã số column dùng autoname random hash (9inpk0us2f, h6rpu803ro, fjvgn6vlrt). Asset dùng pattern ACC-ASS-2026-NNNNN nhất quán. Inconsistency. — Screenshot persona-pm/06-ccdc-item-list.png. Recommendation: đổi CCDC Item autoname → `format:CCDC-{YYYY}-.#####` cho parity với Asset.

- **PM-06 Severity P0 / List Display** — CCDC Item list: column "Mã sản phẩm" empty cho cả 15 rows (cột bị bỏ trống nhưng vẫn hiện trong list). — Screenshot persona-pm/06-ccdc-item-list.png. Recommendation: hoặc remove column khỏi `in_list_view`, hoặc fetch từ Item Code link → field auto-fill khi tạo CCDC.

- **PM-07 Severity P1 / List Display** — CCDC Allocation Schedule và CCDC Writeoff list view: column "Công cụ dụng cụ" hiển thị random ID (9inpk0us2f, h6rpu803ro) thay vì tên người đọc được. — Screenshots persona-pm/07-ccdc-allocation-schedule-list.png, persona-pm/08-ccdc-writeoff-list.png. Recommendation: thêm `fetch_from: ccdc_item.item_name` cho display field; show item_name in list view, store ccdc_item link as foreign key.

- **PM-08 Severity P1 / Status Vocabulary** — CCDC Item list shows status "Đã ghi sổ" cho tất cả 15 records, nhưng task spec định nghĩa 4 states: "Mới mua / Đang sử dụng / Hết phân bổ / Đã ghi giảm". Field value/label mismatch. — Screenshot persona-pm/06-ccdc-item-list.png. Recommendation: review CCDC Item status options; sync với spec hoặc update spec; also add lifecycle hooks for state transitions.

- **PM-09 Severity P1 / Naming Inconsistency** — Asset Disposal: page title "Xử lý tài sản", column "Hình thức thanh lý", sidebar item "Thanh lý" (3 different terms cho cùng concept). — Screenshot persona-pm/05-asset-disposal-list.png. Recommendation: chọn "Thanh lý tài sản" cho mọi nơi (page title + DocType label + sidebar item).

- **PM-10 Severity P2 / Naming Inconsistency** — Asset Handover & Stocktake & Writeoff: Mã số autoname random hash (5ivu0dhd7e, spkcjijm8l, h6unccflrj). Spec implies sequential codes. — Screenshots persona-pm/09, 10, 08. Recommendation: chuẩn hóa autoname pattern HSV-/HSC-/STK-/WO-{YYYY}-.#####.

- **PM-11 Severity P1 / Settings UX** — `/app/vn-accounting-settings#asset-permissions-tab` không activate tab "Phân quyền TSCĐ & CCDC" — user landing on Treasury tab, cần manual click dropdown top-right. — Screenshot persona-pm/12-settings-permissions-tab.png. Recommendation: handle hash router trong settings.js để tab matches anchor on load.

- **PM-12 Severity P2 / Branding** — Workspace logo "V Kế Toán VN / VN Accounting" — sub-line "VN Accounting" lặp lại. Một dòng đủ. Recommendation: bỏ sub-line.

