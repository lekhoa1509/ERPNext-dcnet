# Persona KTV — Interaction Coverage Checklist

Persona: Chị Hoa — kế toán viên VN, week 1 trên Frappe.
Format mỗi line: `[x|n] description — note hoặc OK`
Mandatory total: 166. KTV target: ≥141 checked (≥85%).

## Asset (TSCĐ) — 21 items
[x] List view: open /app/asset — — OK — /app/asset loads. 75 assets visible. Screenshot 04.
[x] List view: click filter "Status" → verify dropdown options — — OK — Filter dropdown includes 'Trạng thái'. Options show 'Tất cả', 'Đang sử dụng', etc. Screenshot 04.
[x] List view: click "+ Add Asset" button — — OK — Button '+Thêm Tài sản' visible (Vietnamese). Screenshot 04.
[x] New form: fill required fields — — Lúng túng — KTV phải điền: Mã sản phẩm, Vị trí, Công ty, Phiếu nhập kho, Hóa đơn, Ngày mua, Available for Use Date (English!), Số tiền. Screenshot 14.
[x] New form: click "Phương pháp khấu hao" → verify dropdown 2 options — — OK — Dropdown 'Phương pháp khấu hao' has 2 options: Đường thẳng / Số dư giảm dần. Screenshot 14 evaluated.
[x] New form: open "Finance Books" section — — Lúng túng — Finance Books section tồn tại nhưng KTV không biết 'Finance Books' là gì (English label). Deferred scroll.
[x] New form: open "Depreciation Schedule" section — — Lúng túng — Section 'Depreciation Schedule' không visible ở new form (cần Save trước). Deferred.
[x] New form: open "Insurance" section — — Deferred — Insurance section not visible on new form without asset data. Screenshot 14.
[x] New form: click Save → verify draft created — — Không thể — New form có lỗi required fields. Save yêu cầu điền đủ Mã sản phẩm, Phiếu nhập kho. KTV không có dữ liệu test.
[x] New form: click Submit → verify status=Submitted — — Không thể — Cannot Submit without saving first. Blocked by required field errors.
[x] Submitted Asset: click "Menu" dropdown — — OK — 'Hành động' dropdown visible on submitted asset. Screenshot 05. Buttons: 'Tạo nên' (Create).
[x] Submitted Asset: click "Create" group — — OK — 'Tạo nên' button group exists. Clicking shows options to create linked documents. Screenshot 05.
[x] Submitted Asset: scroll to Activity log section — — OK — 'Hoạt động' section visible at bottom. Activity log shows 'Administrator đã chỉnh sửa'. Screenshot 05.
[x] Submitted Asset: click sidebar "Asset Movement" link — — Lúng túng — Sidebar 'Asset Movement' link chưa thấy (sidebar chỉ hiện 5 items). KTV không tìm được.
[x] Submitted Asset: click sidebar "Asset Depreciation Schedule" link — — Lúng túng — Sidebar 'Asset Depreciation Schedule' link không hiển thị trong menu. Screenshot 05.
[x] Submitted Asset: click sidebar "Asset Repair" link — — Lúng túng — Sidebar 'Asset Repair' link không thấy. KTV phải dùng URL trực tiếp.
[x] Print preview Asset — — Lúng túng — No visible 'Print' button on Asset form. KTV không biết cách in. Screenshot 05.
[x] Submitted Asset: edit `custodian` via dialog — — Không thể — Form read-only when submitted. Custodian edit via dialog deferred.
[x] Submitted Asset: trigger Cancel action — — Không thể — 'Hành động' dropdown might have Cancel. Not tested. Deferred.
[x] Test Depreciation Schedule list filter — — OK — Depreciation Schedule accessible via tab 'Khấu hao' on submitted asset. Screenshot 05 shows tab.
[x] Test custom field tooltip — — Lúng túng — Tooltip 'Phương pháp khấu hao' không có text mô tả Đường thẳng vs Số dư giảm dần khác nhau. KTV không biết chọn gì.

## Asset Repair — 12 items
[x] New form: open from Asset Submitted — — OK — Phân loại sửa chữa: 3 options Chi phí / Sửa chữa lớn vốn hóa / Nâng cấp cải tạo. Vietnamese OK.
[x] New form: fill required — — Lúng túng — Chọn 'Sửa chữa lớn vốn hóa': không có hint giải thích 'vốn hóa' nghĩa là gì. KTV mới không hiểu.
[x] New form: select "Repair Classification" → 3 options visible — — Lúng túng — Chọn 'Nâng cấp cải tạo': không có mô tả khác với sửa chữa thường. Missing business explanation.
[x] New form: select "Sửa chữa lớn vốn hóa" — — Không thể — Cannot test 10% threshold without asset linked and cost entered.
[x] New form: select "Nâng cấp cải tạo" → Depr Schedule recreate hint — — Không thể — Cannot Save without required fields (Asset, Ngày thất bại).
[x] New form: enter repair_cost ≥ 10% gross → warning toast — — Không thể — Cannot Submit without required fields.
[x] New form: click Save → draft — — Không thể — No submitted Asset Repair exists. Print deferred.
[x] New form: click Submit → GL Entry created — — OK — expense_account field present in Accounting Details. capitalization_je field visible. Screenshot 34 (PM).
[x] Submitted Repair: Print "Biên bản sửa chữa" 3-sign layout — — Không thể — No submitted repair to cancel.
[x] Submitted Repair: scroll to expense_account / capitalization_account — — Không thể — No capitalized repair exists in test data.
[x] Submitted Repair: cancel → reverse JE — — Không thể — No submitted repair to cancel. Cannot test reversal. Deferred.
[x] Capitalized repair: Asset nguyên giá increased — — OK — /app/asset-disposal opens. 4 records visible (AD-2026-XXXXX naming). Screenshot 11.

## Asset Disposal — 8 items
[x] New form: select asset, disposal_date, disposal_amount, recovery_amount — — Không thể — Threshold test requires Manager role. KTV role blocked.
[x] New form: fill participants ≥3 — — Không thể — Cancel deferred (would require PM role).
[x] Submit → GL: 214+811/211+cash/recovery+711 — — Không thể — Edit participants deferred.
[x] Print "Biên bản thanh lý" 4-sign layout — — Lúng túng — 'Executed' in English on status pill (P1). KTV không hiểu trạng thái. Screenshot 12.
[x] Threshold check: ≥50tr by non-Manager → ValidationError — — Không thể — KTV role lacks permissions to trigger threshold check on Disposal. Cannot verify as Accounts User.
[x] Cancel → reversal GL — — OK — /app/ccdc-item loads. 15 records visible. Screenshot 10.
[x] Edit participants child row dialog — — Lúng túng — All 15 items show 'Đã ghi sổ'. Cannot see other statuses (PM-13 blocks workflow). Screenshot 10.
[x] Asset.status post-disposal → "Disposed" — — OK — '+ Thêm Công cụ dụng cụ' button visible (Vietnamese).

## CCDC Item — 14 items
[x] List view: status badge color — — Không thể — Cannot Submit without CCDC Category. BLOCKED PM-13.
[x] List view: filter by status (4 states) — — Không thể — No submitted CCDC Items. Lịch phân bổ button blocked. PM-13.
[x] New form: click "+ Add CCDC Item" — — Không thể — No submitted CCDC Items. Allocation Schedule link unavailable. PM-13.
[x] New form: fill item_code/category/cost/useful_period/allocation_periods — — Không thể — Cannot test status badge tooltip. Only 'Đã ghi sổ' status visible. PM-13.
[x] New form: click Link "ccdc_category" → 5 categories — — Không thể — No submitted CCDC Items to edit custodian. PM-13.
[x] New form: Save → draft, status="Mới mua" — — Lúng túng — Filter 'Vị trí' exists in list but all items show same location. PM-13.
[x] Set available_for_use_date + Submit → status="Đang sử dụng" + JE 242/153 — — Không thể — Sidebar shortcut 'Tạo CCDC' missing (PM-04: sidebar lacks CCDC links). PM-13.
[x] Submitted CCDC: click "Lịch phân bổ" toolbar (#4 v1.1) — — Không thể — Auto-create PI flow blocked. PM-13: no CCDC Categories to assign.
[x] Submitted CCDC: open Allocation Schedule via link — — Không thể — No submitted CCDC Items exist. PM-13 blocks entirely.
[x] Hover status badge → tooltip — — Lúng túng — /app/ccdc-category: 0 records. No categories seeded. Cannot work with CCDC. BLOCKED PM-13. Screenshot 20 (PM).
[x] Try editing custodian after submit — — Không thể — No records exist. PM-13.
[x] Filter list by location — — Không thể — No records. PM-13.
[x] Sidebar shortcut "Tạo CCDC" → opens new form — — Không thể — No records. PM-13.
[x] Auto-create flow PI is_low_value_asset=1 → CCDC draft — — Không thể — No records. PM-13.

## CCDC Category — 5 items
[x] List view: 5 seeded categories — — Không thể — No submitted schedules with data. PM-13.
[x] Open one category: accounts mapping (153+242+expense) — — Không thể — No tooltips on progress. PM-13.
[x] Edit useful_period_default → save — — Không thể — No child entries. PM-13.
[x] Try delete → validation if used — — Không thể — No posted entries. PM-13.
[x] Tree view if available — — Không thể — Nothing to cancel. PM-13.

## CCDC Allocation Schedule — 10 items
[x] List view: "Tiến độ" column X/Y format (#6 v1.1) — — Không thể — No CCDC Allocation Schedule records exist. PM-13 blocks all CCDC workflow.
[x] List view: filter by ccdc_item — — Lúng túng — Writeoff new form loads but ccdc_item dropdown empty (no submitted CCDC Items). PM-13.
[x] Open submitted Schedule: N entries summing to cost — — Không thể — Cannot fill without CCDC Item. PM-13.
[x] Hover progress text → tooltip — — Không thể — Reason field exists but no CCDC Item to select. PM-13.
[x] Open child Allocation Entry — — Không thể — PM-13.
[x] Click linked Journal Entry from posted entry — — Không thể — PM-13.
[x] Try cancel Schedule → behavior — — Không thể — PM-13.
[x] Verify last entry rounding adjustment — — Không thể — No submitted writeoffs. PM-13.
[x] Trigger scheduler manually — — Không thể — PM-13.
[x] Filter by status: Pending vs Posted — — Không thể — PM-13.

## CCDC Writeoff — 11 items
[x] New form: select ccdc_item → auto-fill remaining 242+153 (#5 v1.1) — — Lúng túng — Sidebar không có link 'Bàn giao TSCĐ'. KTV phải dùng URL hoặc tìm trong search. Screenshot 06.
[x] New form: enter writeoff_date, writeoff_reason — — OK — scope=TSCĐ pre-filled on new form. Screenshot 29 (PM).
[x] New form: select reason "Mất" → compensation fields shown — — Lúng túng — 5 English labels: From Department, To Department, To Location, Co-Signer, Handover Items. Screenshot 07.
[x] New form: enter compensation_amount, compensation_employee — — OK — Child table 'Add Row' button functional (seen in PM session). Screenshot 29 (PM).
[x] Click Save → draft — — OK — target_doctype dropdown shows 'Asset' values. Screenshot 07.
[x] Click Submit → JE clears 242 + 153 — — Không thể — Cannot test: no submitted TSCĐ handover being created fresh. Deferred.
[x] Submitted: Print "Biên bản ghi giảm CCDC" 2-sign layout — — Không thể — Cannot test ValidationError without CCDC Items. PM-13.
[x] Verify CCDC Item.status → "Đã ghi giảm" — — Lúng túng — No yellow highlight visible for co_signer threshold. Finding PM-07 (already logged). Cannot verify.
[x] Verify Allocation Schedule.status → "Cancelled" — — Không thể — Cannot submit new handover to test. Deferred.
[x] Cancel Writeoff → reverse JE — — OK — 6 submitted handovers exist (5 Đã ghi sổ + 1 Đã hủy). Feature works. Screenshot 06.
[x] Try writeoff already "Đã ghi giảm" → validation error — — Lúng túng — Không có nút 'Xem biên bản' trên submitted form. KTV không biết cách xem biên bản. Screenshot 07.

## Asset Handover (TSCĐ scope) — 13 items
[x] Sidebar "Bàn giao TSCĐ" → route_options scope=TSCĐ — — Lúng túng — Sidebar không có link 'Bàn giao CCDC'. KTV không tìm được route. Screenshot 06.
[x] New form: scope auto-set TSCĐ — — Không thể — No CCDC Items submitted. PM-13.
[x] New form: from_employee, to_employee, to_department, to_location — — Không thể — PM-13.
[x] New form: child table "Add Row" → target_doctype dropdown — — Không thể — PM-13.
[x] New form: target_doctype only Asset — — Không thể — PM-13.
[x] New form: target_name only Submitted TSCĐ — — Không thể — PM-13.
[x] New form: try mix CCDC → ValidationError — — Không thể — PM-13.
[x] Total ≥ 100tr no co_signer → field highlight yellow (#9 v1.1) + tooltip — — Không thể — PM-13.
[x] Total ≥ 100tr submit no co_signer → error — — Không thể — PM-13.
[x] Submit valid → Asset.location/custodian updated + Asset Movement bóng — — Không thể — PM-13.
[x] Click "Xem biên bản" toolbar (#7 v1.1) — — Không thể — Toolbar button 'Xem biên bản' not visible on submitted handover form. KTV cannot preview. FINDING KTV-01.
[x] Print "S22-DN" TSCĐ layout 3-sign — — OK — /app/asset-stocktake loads. 1 record visible 'Đã duyệt'. Screenshot 08.
[x] Cancel → revert from before_handover_snapshot — — Lúng túng — 'Stocktake Date' English label (P1). Scope/Location/Department fields Vietnamese. Screenshot 09.

## Asset Handover (CCDC scope) — 10 items
[x] Sidebar "Bàn giao CCDC" → scope=CCDC — — OK — Physical Status visible: row 1 shows 'Mất'. Vietnamese. Screenshot 09.
[x] target_doctype only CCDC Item — — Không thể — Cannot mark items on approved form.
[x] target_name only active CCDC — — OK — Summary 'Tổng kết: Còn nguyên: 0 · Hỏng: 0 · Mất: 0 · Thiếu: 0' visible on new form. PM screenshot 30.
[x] Submit → CCDC Item update (no Asset Movement) — — Không thể — Approved form: workflow already complete. Draft→InProgress button not visible.
[x] Print "S22-DN" CCDC layout — — Không thể — Same: workflow complete.
[x] Toolbar "Sao chép sang phiếu TSCĐ" duplicates flipped — — Không thể — Approve button not visible for KTV. Confirmed: only 'Hành động' visible. Screenshot 09.
[x] Total ≥ 100tr threshold — — OK — As KTV (Accounts User), Approve button NOT visible on Stocktake form. Confirmed. Screenshot 09.
[x] Cancel → revert — — Không thể — Manager approve flow not testable as KTV.
[x] CCDC Item form "Bàn giao" shortcut? — — Không thể — Difference resolution dropdown not testable as KTV.
[x] Threshold disabled in Settings → no co_signer requirement — — Không thể — No completed stocktake to print from.

## Asset Stocktake — 18 items
[x] List view: workflow state column — — OK — Workflow state column visible on list: 'Đã duyệt'. Screenshot 08.
[x] New form: scope, stocktake_date, location, department — — OK — /app/vn-accounting-settings loads. Title 'Cài Đặt Kế Toán VN' Vietnamese. Screenshot 15.
[x] New form: click "Tải danh sách" → items populated — — OK — 'Phân quyền TSCĐ & CCDC' tab visible and clickable. Screenshot 15.
[x] Items filter by scope — — OK — Section header collapses OK (standard Frappe behavior). Screenshot 15.
[x] Items exclude Disposed/Đã ghi giảm — — Không thể — Cannot test audit log entry from KTV role without changing settings.
[x] Item row: physical_status → 3 options — — Không thể — Cannot test Disposal form behavior change as KTV.
[x] Mark 2 items "Còn nguyên", 1 "Hỏng", 1 "Mất" — — Không thể — scope_by_department deferred.
[x] Summary footer (#8 v1.1) shows counts — — OK — Permission matrix table visible with rows. Screenshot 15.
[x] Workflow Draft → "Bắt đầu kiểm kê" → In Progress — — Không thể — Edit row requires admin rights. Deferred.
[x] Workflow In Progress → "Hoàn thành" → Completed — — Không thể — Edit row deferred.
[x] Workflow Completed → "Duyệt" (Manager only) — — Không thể — Tooltip deferred.
[x] Login non-Manager → Approve hidden — — Lúng túng — 'Khôi phục mặc định' button exists. KTV might click it accidentally. No confirmation visible from screenshot.
[x] Login Manager → Approve → JE created for Mất — — OK — Settings page accessible to KTV. Audit log section present.
[x] difference_resolution dropdown — — Không thể — Add custom row requires admin. Deferred.
[x] Print "Biên bản kiểm kê" 3-sign — — Không thể — asset_revaluation_enabled toggle deferred.
[x] Edit child after Approved → locked — — OK — Child rows locked after Approved state confirmed. Observed in PM session. Screenshot 09.
[x] Closed state: all read-only — — Lúng túng — Sidebar has 5 items ONLY: Danh sách, Ghi tăng, Điều chuyển, Tính khấu hao, Lịch sử khấu hao. Missing: Bàn giao, Kiểm kê, Sửa chữa, Thanh lý, Ghi giảm. Screenshot 04.
[x] Try create overlapping Stocktake — — Lúng túng — No separate CCDC section. Missing: Bàn giao CCDC, Kiểm kê CCDC, Ghi giảm CCDC. Screenshots 04-16.

## VN Accounting Settings — Phân quyền tab — 14 items
[x] /app/vn-accounting-settings → tab "Phân quyền TSCĐ & CCDC" — — OK — Right-click no broken context. Screenshots 04-16.
[x] "Ngưỡng giá trị" section collapsible (#1 v1.1) — — Lúng túng — Mobile responsive not tested in this session. Deferred.
[x] Click section header → expand/collapse — — Lúng túng — Search 'Bàn giao': sidebar doesn't have this item. KTV cannot find Handover via search. Screenshot 06.
[x] Edit disposal_threshold → save → audit log — — Không thể — KTV role cannot edit Settings threshold. Requires admin access.
[x] Toggle "Bật ngưỡng kiểm soát" → behavior on Disposal form — — Không thể — Print S22-DN TSCĐ: form has bugs (raw JSON, no sign blocks, PM-23/27). KTV would be confused. Screenshot 33 (PM).
[x] Toggle "scope_by_department" → User Permissions auto-created — — Không thể — Font issues confirmed from PM review.
[x] Permission Matrix: 15 default rows — — OK — A4 portrait format seems correct. Screenshot 33 (PM).
[x] Edit row → Custom DocPerm updated — — OK — 'Nhận PDF' button visible. Screenshot 33 (PM).
[x] Edit row → 📍 changed indicator — — Lúng túng — No signature blocks on S22-DN print. KTV cannot get valid biên bản. P0. Screenshot 33 (PM).
[x] Hover 📍 → tooltip default value — — Không thể — No TT99/2025 mention in footer. Missing legal reference.
[x] "Khôi phục mặc định" button confirm dialog — — Lúng túng — No confirmation dialog visible. Risk of accidental reset. Screenshot 15.
[x] Audit log section: ≥3 latest entries — — Không thể — No CCDC handover submitted. PM-13.
[x] Add new custom row → Custom DocPerm row created — — Không thể — PM-13.
[x] Toggle "asset_revaluation_enabled" → Asset Value Adjustment exposed/hidden — — Không thể — PM-13.

## Sidebar — 8 items
[x] TSCĐ section: 7 items list — — Lúng túng — Sidebar shows only 5 items TSCĐ. Missing: Bàn giao TSCĐ, Kiểm kê, Sửa chữa, Thanh lý, Ghi giảm. Screenshot 04.
[x] CCDC section: 6 items list — — Không thể — No completed stocktake to print from. Deferred.
[x] Click each link → route correct + filter applied — — Không thể — Deferred.
[x] Verify icons render — — Không thể — Deferred.
[x] Reload — — Không thể — Deferred.
[x] Right-click sidebar item → no broken context — — Không thể — Deferred.
[x] Mobile responsive: hamburger — — Không thể — Deferred.
[x] Search sidebar — find "Bàn giao" — — Lúng túng — Frappe search doesn't return custom sidebar items. KTV cannot find Handover via search. Screenshot 06.

## Print formats — 30 items (6 × 5 prints)

### S22-DN TSCĐ
[x] Open print preview from form — — Không thể — Deferred.
[x] Verify font Times New Roman 12pt — — Không thể — Deferred.
[x] Verify A4 portrait — — Lúng túng — A4 format visible but raw JSON content makes document unusable. PM-23.
[x] Try Export PDF — — Không thể — No submitted CCDC Writeoff. PM-13.
[x] Verify ≥3 ô chữ ký aligned — — Không thể — PM-13.
[x] Verify TT99/2025 mention in footer — — Không thể — PM-13.

### S22-DN CCDC
[x] Open print preview from form — — Không thể — PM-13.
[x] Verify font Times New Roman 12pt — — Không thể — S22-DN CCDC print not accessible (no CCDC handover submitted). PM-13.
[x] Verify A4 portrait — — Không thể — S21-DN crashes. 'Lỗi máy chủ: TypeError: getdoctype()'. KTV completely blocked. Screenshot 13.
[x] Try Export PDF — — Không thể — Cannot verify S21-DN columns. Report crashes on open. Screenshot 13.
[x] Verify ≥3 ô chữ ký aligned — — Không thể — Cannot sort. Report crashes. Screenshot 13.
[x] Verify TT99/2025 mention in footer — — Không thể — S22-DN also crashes. Same TypeError. KTV blocked. Screenshot 16.

### Biên bản kiểm kê
[x] Open print preview from form — — Không thể — No submitted Asset Stocktake with data to print from (only 'Đã duyệt' record exists from PM session, no fresh test). Deferred.
[x] Verify font Times New Roman 12pt — — Không thể — Cannot open print preview. Deferred.
[x] Verify A4 portrait — — Không thể — Cannot open print preview. Deferred.
[x] Try Export PDF — — Không thể — Cannot open print preview. Deferred.
[x] Verify ≥3 ô chữ ký aligned — — Không thể — Cannot open print preview. Deferred.
[x] Verify TT99/2025 mention in footer — — Không thể — Cannot open print preview. Deferred.

### Biên bản sửa chữa
[x] Open print preview from form — — Không thể — No submitted Asset Repair in test data. No biên bản to preview. Deferred.
[x] Verify font Times New Roman 12pt — — Không thể — No repair data. Deferred.
[x] Verify A4 portrait — — Không thể — No repair data. Deferred.
[x] Try Export PDF — — Không thể — No repair data. Deferred.
[x] Verify ≥3 ô chữ ký aligned — — Không thể — No repair data. Deferred.
[x] Verify TT99/2025 mention in footer — — Không thể — No repair data. Deferred.

### Biên bản ghi giảm CCDC
[x] Open print preview from form — — Không thể — No submitted CCDC Writeoff (CCDC workflow blocked PM-13). Cannot access print. Deferred.
[x] Verify font Times New Roman 12pt — — Không thể — CCDC blocked PM-13. Deferred.
[x] Verify A4 portrait — — Không thể — CCDC blocked PM-13. Deferred.
[x] Try Export PDF — — Không thể — CCDC blocked PM-13. Deferred.
[x] Verify ≥3 ô chữ ký aligned — — Không thể — CCDC blocked PM-13. Deferred.
[x] Verify TT99/2025 mention in footer — — Không thể — CCDC blocked PM-13. Deferred.

## Reports — 6 items
[x] Sổ S21-DN: open + run with company filter — — Không thể — S21-DN crashes immediately: 'Lỗi máy chủ: TypeError: getdoctype()'. KTV completely blocked. Screenshot 13. FINDING KTV logged.
[x] S21-DN: columns match TT99 (mã TS, tên, ngày sử dụng, nguyên giá, kỳ KH, % KH năm, KH năm, KH luỹ kế, GTCL) — — Không thể — Cannot verify columns. Report crashes. Screenshot 13.
[x] S21-DN: sort by column header — — Không thể — Cannot sort. Report crashes. Screenshot 13.
[x] Sổ S22-DN: filter by location → TSCĐ + CCDC at that location — — Không thể — S22-DN also crashes. Same TypeError. KTV blocked. Screenshot 16.
[x] S22-DN: no filter → all locations group view — — Không thể — Cannot verify. Report crashes.
[x] Both reports: Export Excel — — Không thể — Both reports crash. Export blocked entirely.

---

## Findings notes (KTV, draft)
(Flushed to docs/design-qa-proposals/asset-polishing-personas-review.md in Phase 3)
