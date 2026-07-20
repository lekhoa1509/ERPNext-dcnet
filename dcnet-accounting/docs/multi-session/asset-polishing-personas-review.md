# Task: Design QA — 2-Persona Review (PM + Kế toán viên VN)

## Context

Asset Polishing v1.1 đã ship với 9 DocTypes, 9 print formats, 10 polish items. Cần round design QA chuyên sâu với **2 góc nhìn cụ thể**:

1. **PM phần mềm** — Frappe UI consistency lens (không biết nghiệp vụ kế toán, chỉ quan tâm tính đồng nhất chung)
2. **Kế toán viên Việt Nam** — End-user lens (UI thuần Việt, ghi chú nghiệp vụ rõ ràng, thân thiện)

Output: **báo cáo chi tiết** để làm cơ sở cải tiến v1.2 (không code change trong task này).

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing` (worktree)
- Branch: `feat/asset-polishing` (read-only review, không commit code change)
- Bench root: `/home/long/long/frappe-bench-dcnet`
- Site test: `dcnet.localhost`
- Test URL: `http://dcnet.localhost:8001`

### Surfaces under review

| Surface | Route | Ghi chú |
|---------|-------|---------|
| Sidebar 2 sections | `/app/vn-accounting` workspace | TSCĐ + CCDC sections |
| Asset (TSCĐ) form | `/app/asset/<name>` + `/app/asset/new` | List + Create + View Submitted |
| Asset Repair form | `/app/asset-repair/new` | Với repair_classification 3-way |
| Asset Disposal form | `/app/asset-disposal/<name>` | Đã có v1.0 |
| CCDC Item form | `/app/ccdc-item/<name>` + `/new` | List + Create + Submitted |
| CCDC Allocation Schedule | `/app/ccdc-allocation-schedule/<name>` | Với progress column |
| CCDC Writeoff form | `/app/ccdc-writeoff/new` | Auto-fill remaining preview |
| Asset Handover form | `/app/asset-handover/new?scope=TSCĐ` + `?scope=CCDC` | 2 scope variants |
| Asset Stocktake form | `/app/asset-stocktake/<name>` | 4 workflow states |
| VN Accounting Settings | `/app/vn-accounting-settings` | Tab "Phân quyền TSCĐ & CCDC" |
| Print S22-DN (TSCĐ) | `/printview?doctype=Asset Handover&...` | Biên bản bàn giao TSCĐ |
| Print S22-DN (CCDC) | tương tự | Biên bản bàn giao CCDC |
| Print Biên bản kiểm kê | Asset Stocktake print | |
| Print Biên bản sửa chữa | Asset Repair print | |
| Print Biên bản ghi giảm CCDC | CCDC Writeoff print | |
| Report S21-DN | `/app/query-report/Sổ TSCĐ S21-DN` | |
| Report S22-DN | `/app/query-report/...` | Group by location |

Total: **10 forms + 5 print formats + 2 reports + 1 sidebar = 18 surfaces**

### Output file

`docs/design-qa-proposals/asset-polishing-personas-review.md` — report đầu ra chính.

Plus 2 coverage tracking files (1 mỗi persona):
- `qa-screenshots/persona-pm/coverage.md`
- `qa-screenshots/persona-ktv/coverage.md`

Không tạo file khác. Không sửa code.

### Interaction Coverage Matrix (BẮT BUỘC — enforce thoroughness)

Task này read-only nhưng phải **TƯƠNG TÁC** đầy đủ với mọi element trên TSCĐ + CCDC mới tạo, không chỉ screenshot list view rồi đoán. Mỗi persona phải maintain checklist `coverage.md` đánh dấu `[x]` mỗi item đã actually-click/fill/test.

**Mỗi DocType có danh sách items bắt buộc dưới đây.** Agent copy template vào `coverage.md`, đánh dấu khi test xong, log finding nếu phát hiện vấn đề.

#### Asset (TSCĐ) — 21 items

```
[ ] List view: open /app/asset
[ ] List view: click filter "Status" → verify dropdown options
[ ] List view: click "+ Add Asset" button
[ ] New form: fill required fields (asset_name, asset_category, item_code, gross_purchase_amount, available_for_use_date)
[ ] New form: click "Phương pháp khấu hao" → verify dropdown chỉ 2 options
[ ] New form: open "Finance Books" section → expand
[ ] New form: open "Depreciation Schedule" section
[ ] New form: open "Insurance" section
[ ] New form: click Save → verify draft created
[ ] New form: click Submit → verify status=Submitted
[ ] Submitted Asset: click "Menu" dropdown → list all menu items
[ ] Submitted Asset: click "Create" button group → verify options (Repair, Movement, etc.)
[ ] Submitted Asset: scroll to bottom, check Activity log section
[ ] Submitted Asset: click sidebar "Asset Movement" link
[ ] Submitted Asset: click sidebar "Asset Depreciation Schedule" link
[ ] Submitted Asset: click sidebar "Asset Repair" link (or via Menu)
[ ] Print preview Asset: click "Print" → verify formats list
[ ] Submitted Asset: edit `custodian` field via dialog → verify updates
[ ] Submitted Asset: trigger Cancel action → verify dialog confirms
[ ] Test depreciation Schedule list: filter by asset
[ ] Test custom field tooltip (Phương pháp khấu hao): hover → verify Vietnamese
```

#### Asset Repair — 12 items

```
[ ] New form: open from Asset Submitted via "Create > Asset Repair"
[ ] New form: fill required (asset, failure_date, completion_date, repair_cost, description_of_work)
[ ] New form: select "Repair Classification" → verify 3 options visible
[ ] New form: select "Sửa chữa lớn vốn hóa" → verify any conditional fields appear
[ ] New form: select "Nâng cấp cải tạo" → verify Depr Schedule recreate hint shown
[ ] New form: enter repair_cost ≥ 10% gross_purchase_amount → verify warning toast
[ ] New form: click Save → verify draft
[ ] New form: click Submit → verify GL Entry created (open via Menu > "View" > "GL Entry")
[ ] Submitted Repair: click "Print" → "Biên bản sửa chữa" → verify 3-sign layout
[ ] Submitted Repair: scroll to expense_account / capitalization_account fields → verify auto-filled
[ ] Submitted Repair: cancel → verify reverse JE
[ ] Capitalized repair: open underlying Asset → verify nguyên giá increased
```

#### Asset Disposal — 8 items

```
[ ] New form: select asset, enter disposal_date, disposal_amount, recovery_amount
[ ] New form: fill participants child table (≥3 signers)
[ ] Submit → verify GL: 214 + 811 / 211 + cash/recovery / 711
[ ] Print "Biên bản thanh lý" → verify 4-sign layout
[ ] Threshold check: nguyên giá ≥ 50tr submit by non-Manager → verify ValidationError
[ ] Cancel → verify reversal GL
[ ] Edit participants child row → verify dialog
[ ] Asset.status post-disposal → verify "Disposed"
```

#### CCDC Item — 14 items

```
[ ] List view /app/ccdc-item: verify columns include status with badge color
[ ] List view: filter by status (Mới mua / Đang sử dụng / Hết phân bổ / Đã ghi giảm)
[ ] New form: click "+ Add CCDC Item"
[ ] New form: fill item_code (link), category, cost, useful_period_months, allocation_periods
[ ] New form: click Link "ccdc_category" → verify 5 seeded categories
[ ] New form: click Save → draft, status="Mới mua"
[ ] Set available_for_use_date + click Submit → verify status="Đang sử dụng" + JE 242/153 + Allocation Schedule auto-created
[ ] Submitted CCDC Item: click "Lịch phân bổ" toolbar button (#4 v1.1) → verify navigates to Schedule list filtered
[ ] Submitted CCDC Item: open Allocation Schedule from link
[ ] Hover status badge → verify tooltip explains state
[ ] Try editing custodian field after submit → verify dialog
[ ] Filter list by location → verify
[ ] Test sidebar shortcut "Tạo CCDC" → opens new form with docstatus=0 filter pre-fill
[ ] Auto-create flow: create test PI with item.is_low_value_asset=1 → submit → verify CCDC Item draft auto-created
```

#### CCDC Category — 5 items

```
[ ] List view /app/ccdc-category: verify 5 seeded categories
[ ] Open one category → verify accounts mapping (153 + 242 + expense)
[ ] Edit useful_period_default → save
[ ] Try delete → verify validation if used
[ ] Tree view if available
```

#### CCDC Allocation Schedule — 10 items

```
[ ] List view /app/ccdc-allocation-schedule: verify "Tiến độ" column shows X/Y format (#6 v1.1)
[ ] List view: filter by ccdc_item
[ ] Open submitted Schedule: verify N entries summing to cost
[ ] Hover progress text → verify tooltip
[ ] Open child Allocation Entry → verify period_no, allocation_amount, status
[ ] Click linked Journal Entry from posted entry → verify GL
[ ] Try cancel Schedule → verify behavior (should require Writeoff workflow)
[ ] Verify last entry has rounding adjustment
[ ] Trigger scheduler manually via console → verify next pending entry posted
[ ] Filter by status: Pending vs Posted
```

#### CCDC Writeoff — 11 items

```
[ ] New form: select ccdc_item → verify auto-fill remaining_242_amount + remaining_153_amount (#5 v1.1)
[ ] New form: enter writeoff_date, writeoff_reason
[ ] New form: select reason "Mất" → verify compensation_amount + compensation_employee fields shown
[ ] New form: enter compensation_amount, compensation_employee
[ ] Click Save → draft
[ ] Click Submit → verify JE clears 242 (cancel pending entries) + 153 if applicable
[ ] Submitted: click "Print" → "Biên bản ghi giảm CCDC" → verify 2-sign layout
[ ] Verify CCDC Item.status updated to "Đã ghi giảm"
[ ] Verify Allocation Schedule.status updated to "Cancelled"
[ ] Cancel Writeoff → verify reverse JE
[ ] Try writeoff CCDC Item already "Đã ghi giảm" → verify validation error
```

#### Asset Handover (TSCĐ scope) — 13 items

```
[ ] Sidebar: click "Bàn giao TSCĐ" → verify route_options pre-fill scope=TSCĐ
[ ] New form: scope auto-set TSCĐ
[ ] New form: fill from_employee, to_employee, to_department, to_location
[ ] New form: child table — click "Add Row" → set target_doctype dropdown
[ ] New form: target_doctype dropdown → verify chỉ Asset (not CCDC Item) per scope
[ ] New form: target_name Dynamic Link → verify only Submitted TSCĐ assets in suggestion
[ ] New form: try mix CCDC Item → verify ValidationError on save
[ ] Total ≥ 100tr without co_signer → verify field highlight yellow (#9 v1.1) + tooltip
[ ] Total ≥ 100tr submit without co_signer → verify error
[ ] Submit with valid → verify Asset.location/custodian update + Asset Movement bóng created
[ ] Click "Xem biên bản" toolbar (#7 v1.1) → preview
[ ] Click "Print" → "S22-DN" → verify TSCĐ layout 3-sign
[ ] Cancel → verify revert from before_handover_snapshot
```

#### Asset Handover (CCDC scope) — 10 items

```
[ ] Sidebar: click "Bàn giao CCDC" → verify scope=CCDC pre-fill
[ ] target_doctype dropdown → verify chỉ CCDC Item
[ ] target_name → verify only active CCDC Items
[ ] Submit → verify CCDC Item.location/custodian update (no Asset Movement created)
[ ] Print "S22-DN" → verify CCDC layout (different from TSCĐ)
[ ] Toolbar "Sao chép sang phiếu TSCĐ" → verify duplicates with scope flipped
[ ] Total ≥ 100tr threshold same as TSCĐ
[ ] Cancel → revert
[ ] Verify route from CCDC Item form: any "Bàn giao" shortcut?
[ ] Threshold disabled in Settings: verify no co_signer requirement
```

#### Asset Stocktake (full workflow) — 18 items

```
[ ] List view /app/asset-stocktake: verify workflow state column
[ ] New form: scope, stocktake_date, location, department
[ ] New form: click "Tải danh sách" button → verify items populated
[ ] Verify items filter by scope (only Asset for TSCĐ scope, only CCDC for CCDC scope)
[ ] Verify items exclude Disposed/Đã ghi giảm
[ ] Each item row: physical_status dropdown → 3 options
[ ] Mark 2 items "Còn nguyên", 1 "Hỏng", 1 "Mất"
[ ] Verify summary row footer (#8 v1.1) shows counts
[ ] Workflow: Draft → "Bắt đầu kiểm kê" button → state=In Progress
[ ] Workflow: In Progress → "Hoàn thành" → state=Completed
[ ] Workflow: Completed → "Duyệt" (Accounts Manager only)
[ ] Login as non-Manager → try Approve → verify button hidden
[ ] Login as Manager → Approve → verify JE created for Mất, Asset.status updated
[ ] Approve flow: difference_resolution dropdown (Bồi thường / Ghi chi phí / Treo chờ xử lý)
[ ] Print "Biên bản kiểm kê" → 3-sign layout
[ ] Edit child after Approved → verify locked
[ ] Closed state: verify all fields read-only
[ ] Try create new Stocktake same location overlapping date → verify behavior
```

#### VN Accounting Settings — Phân quyền tab — 14 items

```
[ ] Open /app/vn-accounting-settings → click tab "Phân quyền TSCĐ & CCDC"
[ ] Verify "Ngưỡng giá trị" section collapsible (#1 v1.1)
[ ] Click section header → toggle expand/collapse
[ ] Edit disposal_threshold → save → verify audit log entry appears
[ ] Toggle "Bật ngưỡng kiểm soát" → save → verify behavior on Disposal form
[ ] Toggle "scope_by_department" → save → verify User Permissions auto-created
[ ] Permission Matrix table: verify 15 default rows
[ ] Edit one row (toggle write off for Stocktake Member) → save → verify Custom DocPerm updated via SQL
[ ] Edit row → 📍 icon appears (changed indicator)
[ ] Hover 📍 icon → tooltip shows default value
[ ] Click "Khôi phục mặc định" button → confirm dialog → verify table reset
[ ] Audit log section: verify ≥3 latest entries shown
[ ] Add new custom row → save → verify Custom DocPerm row created
[ ] Toggle "asset_revaluation_enabled" → verify Asset Value Adjustment exposed/hidden
```

#### Sidebar — 8 items

```
[ ] Verify TSCĐ section: 7 items (Danh sách, Tạo, Khấu hao, Sửa chữa, Bàn giao, Kiểm kê, Thanh lý, Sổ S21-DN, Lịch sử khấu hao)
[ ] Verify CCDC section: 6 items (Danh sách, Tạo, Lịch phân bổ, Ghi giảm, Bàn giao CCDC, Kiểm kê CCDC, Sổ S22-DN)
[ ] Click each link → verify route correct + filter applied (route_options)
[ ] Verify icons render (Lucide icons not broken)
[ ] Reload page after click — sidebar persists 3-tier (localStorage → boot → default)
[ ] Right-click sidebar item → no broken context menu
[ ] Mobile responsive: collapse to hamburger
[ ] Search sidebar (Frappe search) — find "Bàn giao" → verify highlights
```

#### Print formats — 6 items mỗi print, total 30

```
For each print (S22-DN TSCĐ, S22-DN CCDC, Biên bản kiểm kê, Biên bản sửa chữa, Biên bản ghi giảm CCDC):
[ ] Open print preview from form
[ ] Verify font Times New Roman 12pt
[ ] Verify A4 portrait
[ ] Try Export PDF → verify download
[ ] Verify ≥3 ô chữ ký aligned correctly
[ ] Verify TT99/2025 mention in footer
```

#### Reports — 6 items

```
[ ] Sổ S21-DN: open report, run with company filter
[ ] S21-DN: verify columns match TT99 (mã TS, tên, ngày sử dụng, nguyên giá, kỳ KH, % KH năm, KH năm, KH luỹ kế, GTCL)
[ ] S21-DN: try sort by column header
[ ] Sổ S22-DN: open, filter by location → verify TSCĐ + CCDC at that location
[ ] S22-DN: try without filter → verify "all locations" group view
[ ] Both reports: try Export Excel → verify download
```

**Total mandatory checkboxes: ~166 items.**

**Coverage requirement per persona:**
- Persona PM: ≥80% of 166 = **≥133 checked** items
- Persona KTV: ≥85% of 166 = **≥141 checked** items (KTV cần test thực dụng nhiều hơn)
- Each persona's `coverage.md` ≥1 line per checked item, format: `[x] {item description} — {note hoặc "OK"}`

### Tiered Fix Policy (mới — cho phép auto-fix trong tier)

Mỗi persona vừa review vừa CÓ THỂ tự fix nếu finding rơi vào tier của họ. Items ngoài tier → chỉ log vào report, KHÔNG sửa.

**Tier 1 — Cả 2 personas có thể auto-fix:**
- Thêm/sửa entry trong `vn_accounting/translations/vi.csv` (missing translations)
- Sửa label text trong DocType `.json` (chỉ field `label`, KHÔNG đổi `fieldname` / `fieldtype`)
- Sửa tooltip / description / placeholder text trong DocType json (chỉ text, không thêm field)
- Sửa text trong print format `html` field (typo, alignment, label tiếng Việt)
- Sidebar item label rename (`workspace_sidebar/vn_accounting.json`)
- Diacritics fix trong Vietnamese strings (mọi nơi)

**Tier 2 — PM persona only:**
- Button placement / order reordering trong `.js` file (chỉ vị trí, không đổi behavior)
- Section break / column break layout adjustment trong DocType `.json` (rearrange existing fields)
- List view column changes: `in_list_view`, `columns` width, ordering
- Icon swap (Lucide icon name) trong sidebar / Property Setter
- Status indicator color / badge color (chỉ visual)

**Tier 3 — KTV persona only:**
- Thêm `description` field cho field business-critical (TK 242 là gì, sửa chữa lớn vs nâng cấp khác chỗ nào...)
- Thêm tooltip Vietnamese cho cryptic term
- Đổi default value (today, current company, current user) cho UX
- Bổ sung error message tiếng Việt với diacritics đầy đủ

**Tier 4 — KHÔNG auto-fix (chỉ log into report, defer to v1.2):**
- Thêm/xóa field
- Đổi workflow state machine
- Đổi permission rules
- Thêm DocType / print format / report mới
- Đổi account routing trong JE
- Đổi validation logic
- Đổi threshold default value
- Bất kỳ thay đổi nào ảnh hưởng tới Journal Entry / data model

→ **Nếu không chắc nằm tier nào → Tier 4 (log only).** Khi nghi ngờ là defer, không sửa.

**Cap auto-fix per persona:**
- PM ≤ 15 auto-fixes per session (cap 20 total across phase)
- KTV ≤ 20 auto-fixes per session (cap 30 total)
- Quá cap → log only kể cả Tier 1-3. Tránh scope creep.

**Commit pattern auto-fix:**
- 1 commit / item, atomic
- Message format: `fix(asset-polishing): {brief desc} (review #{persona-ID})`
- Ví dụ: `fix(asset-polishing): add Vietnamese tooltip for TK 242 (review #KTV-07)`
- Sau mỗi commit: bench cycle (build/migrate nếu json change) + verify nothing broken

**Report khi có auto-fix:**
- Section mới "Auto-Fixed in Review" liệt kê items đã apply, kèm commit SHA
- Section deferred items chỉ chứa Tier 4 + items vượt cap

**Bench cycle sau JSON change:**
```bash
cd /home/long/long/frappe-bench-dcnet
git -C apps/vn_accounting checkout --detach feat/asset-polishing
bench --site dcnet.localhost migrate  # only if .json changed
bench build --app vn_accounting          # only if .js / .css changed
bench --site dcnet.localhost clear-cache # always after vi.csv change
```

## Requirements

### Phase 1 — Persona PM (Frappe UI Consistency)

**Persona profile:** PM phần mềm 5+ năm kinh nghiệm Frappe/ERPNext. KHÔNG biết nghiệp vụ kế toán VN. Quan tâm:

1. **Tính đồng nhất với Frappe UI conventions:**
   - Button placement (primary action top-right; secondary trong dropdown "Menu"; "Action" group cho workflow buttons)
   - Form layout (Section Break dùng đúng; column_break tỷ lệ; field grouping logic)
   - Color scheme (status indicator colors theo Frappe palette: gray/green/red/orange/blue)
   - Sidebar item icon set (Lucide icons; consistent style)
   - List view filters (mặc định lọc gì; saved views; column ordering)
   - Breadcrumbs + page header + back button
   - Modal/dialog style (frappe.ui.Dialog patterns)
   - Error/success/warning toast vs alert vs validation message

2. **Tính đồng nhất nội bộ vn_accounting:**
   - So sánh 9 DocTypes mới với DocTypes có sẵn (Cash Count, Asset Disposal, Branch Cash Entry, Term Deposit)
   - Asset Handover/Stocktake có giống pattern Cash Count workflow không?
   - Asset Repair classification field có style giống Cash Count difference_type không?
   - Print format header/footer/sign block layout — có khớp với Asset Disposal đã merge?
   - Settings tab structure — có cùng pattern với 2 tab cũ (Tài khoản mặc định, Treasury)?

3. **Navigation & workflow:**
   - User journey từ sidebar → form → submit → list — có dead-end không?
   - "Sao chép sang phiếu CCDC" button placement có discoverable?
   - Stocktake workflow 4-state chuyển trạng thái có buttons rõ ràng?
   - CCDC Item.status hiển thị ở list view có badge color đúng?

**Procedure:**

1. Setup browser via Playwright MCP, login admin.
2. Visit MỖI surface trong scope list. Per surface:
   - Take screenshot tới `qa-screenshots/persona-pm/<surface-slug>.png`
   - Check console errors via `browser_console_messages`
   - So sánh với reference DocType (Cash Count cho workflow, Asset Disposal cho biên bản, Term Deposit cho Submittable, Sales Invoice cho Asset-equivalent)
   - Log mỗi finding tới in-memory notes (sẽ tổng hợp ở report)
3. Mục tiêu: **≥15 findings** từ persona PM (không quá kén — nếu ≥30 cũng OK).

**Mỗi finding format:**
- Surface (URL/route)
- Category (Consistency / Layout / Interaction / Navigation / Comparison)
- Severity (P0 critical-blocking / P1 major-confusing / P2 minor-polish)
- Description (1-2 câu)
- Reference (DocType nào ở vn_accounting đã làm khác, hoặc Frappe convention)
- Recommendation (1 câu đề xuất sửa)
- Screenshot link

### Phase 2 — Persona Kế toán viên VN (End User)

**Persona profile:** Chị Hoa — kế toán tài sản công ty SME 50 nhân viên, dùng Frappe lần đầu, tiếng Anh hạn chế. Quan tâm:

1. **UI thuần Việt:**
   - Có còn label tiếng Anh nào lộ ra (chưa translate vi.csv)?
   - Tooltip + help text + placeholder bằng tiếng Việt?
   - Error message tiếng Việt đầy đủ diacritics?
   - Confirm dialog ("Bạn có chắc...") có Vietnamese?
   - Sidebar item label tiếng Việt rõ ràng (vs cryptic technical name)?
   - Print format header / footer / column tiếng Việt đúng chuẩn VN?

2. **Giải thích nghiệp vụ:**
   - Field "Phương pháp khấu hao": có giải thích đường thẳng vs số dư giảm dần KHÁC nhau ở đâu? (qua tooltip / description block)
   - Field "Repair Classification": Sửa chữa lớn vs Nâng cấp khác nhau thế nào? (đa số kế toán lúng túng)
   - "TK 242 - Chi phí trả trước": có hint cho người mới biết tài khoản này?
   - Stocktake "Còn nguyên / Hỏng / Mất": có giải thích Hỏng vs Mất khi nào?
   - Threshold "Ngưỡng bàn giao 100tr": kế toán mới có hiểu là cần KTT đồng ký?
   - CCDC Allocation Schedule "12 kỳ": có giải thích 12 kỳ là tháng / quý / năm?

3. **Ghi chú nghiệp vụ rõ ràng:**
   - DocType description (xuất hiện top of new form): có không?
   - Field description ngay bên dưới label cho field business-critical: có không?
   - Workflow state description (Draft / In Progress / Completed / Approved / Closed): có giải thích không?
   - Print format có legal note (theo TT99/2025 PL3...) không?

4. **Dễ dùng (UX cho non-tech):**
   - Default values có sẵn (today, current company, current user)?
   - Required field hint rõ (red asterisk)?
   - Khi tạo CCDC Item, có suggest nguyên giá từ PI không cần nhập tay?
   - Multi-step workflow có progress indicator (Step 1/4) không?
   - Lỡ tay submit sai có cancel + sửa được không (clear UX)?
   - Print preview có visible button không cần đào menu?

5. **Vietnamese accounting practice fit:**
   - Format số: 50,000,000 VND (dấu phẩy ngăn ngàn) hay 50.000.000 đ?
   - Date format: dd/mm/yyyy (chuẩn VN) hay yyyy-mm-dd (ISO)?
   - Currency display: "VND" hay "đ" hay "₫"?
   - Address display có hiển thị tỉnh/quận/phường?

**Procedure:**

1. Login as test user "Chị Hoa" — tạo Frappe user mới `chihoa@test.com` với role Accounts User + User Permission Department=Finance.
2. Navigate qua các surface từ góc nhìn Chị Hoa:
   - Mỗi surface: try làm 1 task đơn giản (tạo TSCĐ, bàn giao, kiểm kê) như người mới
   - Note xuống mọi câu hỏi "không hiểu", "tìm mãi không thấy", "lỡ click sai"
   - Capture screenshot tới `qa-screenshots/persona-ktv/<surface-slug>.png`
3. Mục tiêu: **≥20 findings** từ persona KTV (chị này khắt khe hơn vì là end user trực tiếp).

**Mỗi finding format:** giống persona PM, thêm category cho KTV: (i18n / Business Clarity / Workflow / Format / Notes/Help / Vietnamese Convention).

### Phase 3 — Tổng hợp Report

Tạo file `docs/design-qa-proposals/asset-polishing-personas-review.md` với cấu trúc sau:

```markdown
# Asset Polishing — 2-Persona Design QA Review

**Ngày review:** 2026-04-29
**Reviewer scope:** asset-polishing v1.1 (commit ab00fe1)
**Personas:** PM phần mềm + Kế toán viên VN (Chị Hoa)

---

## Executive Summary

| Persona | Score (/10) | Total findings | P0 | P1 | P2 |
|---------|-------------|----------------|----|----|-----|
| PM (Frappe UI consistency) | X.X | NN | N | N | N |
| Kế toán viên VN | X.X | NN | N | N | N |
| **Composite** | X.X | NN | N | N | N |

**Top 3 issues across both personas:**
1. ...
2. ...
3. ...

**Strengths:**
- ...
- ...

**Weaknesses:**
- ...

---

## Persona PM — Frappe UI Consistency Findings

### P0 — Critical (≥1 expected, có thể 0)
[Findings with full format]

### P1 — Major Confusing (≥3 expected)
[...]

### P2 — Minor Polish (rest)
[...]

---

## Persona KTV — End User Findings

### P0 — Critical
[...]

### P1 — Major Confusing
[...]

### P2 — Minor Polish
[...]

---

## Cross-Cutting Issues (both personas flagged)

| Issue | PM perspective | KTV perspective | Severity | Suggested fix |
|-------|---------------|-----------------|----------|--------------|
| ...   | ...           | ...             | P0/P1/P2 | ...          |

---

## Prioritized Fix List for v1.2

### P0 (must fix before next release)
- [ ] Item 1 — owner: TBD — estimate: 2h
- [ ] Item 2 — owner: TBD — estimate: 1h
...

### P1 (should fix in v1.2)
[...]

### P2 (nice-to-have, defer)
[...]

---

## Suggested v1.2 Sprint Scope

Recommended scope — group by area:
- **i18n cleanup** (~2h): X items
- **UX polish** (~3h): X items
- **Consistency fixes** (~2h): X items
- **Help text + descriptions** (~3h): X items
- **Total:** ~Xh / X items

---

## Appendix — Screenshots Index

| Persona | Surface | Screenshot |
|---------|---------|------------|
| PM | Asset form | qa-screenshots/persona-pm/asset-form.png |
[...]

```

**Format requirements for findings:**
- Mỗi finding **trong report** phải có ít nhất: ID (PM-NN hoặc KTV-NN), Surface, Category, Severity, Description (≥30 chars), Recommendation (≥20 chars), Screenshot path
- Báo cáo TOTAL ≥ 35 findings (15 PM + 20 KTV minimum)
- Cross-cutting section ≥ 3 entries
- Prioritized fix list ≥ 5 P0/P1 items với estimate

### Phase 4 — Final QA + Commit

1. Verify report file ≥ 800 dòng (đủ độ chi tiết) hoặc ≥ 35 findings (count `### ` headers OR `**ID:**` markers)
2. Verify cả 2 personas có screenshots dirs
3. Self-review report 3-point: (1) đủ findings count, (2) recommendation actionable không phải vague, (3) prioritization có rationale
4. Commit final: `docs(asset-polishing): 2-persona design QA review report`
5. Update `MEMORY.md` ở `/home/long/.claude/projects/-home-long-long-frappe-bench-dcnet/memory/` với summary v1.1 polish + v1.2 candidate scope (2-3 dòng)

## Acceptance Criteria

### Phase 1 PM Review
- [ ] `qa-screenshots/persona-pm/` chứa ≥30 PNG (interaction screenshots, không chỉ list views)
- [ ] `qa-screenshots/persona-pm/coverage.md` exists with ≥133 `[x]` checkboxes (≥80% of 166 mandatory items)
- [ ] Each `[x]` line has note ≥1 char (not blank)
- [ ] In-progress notes có ≥15 PM findings (track via report draft)
- [ ] Mỗi finding có screenshot reference khớp file thực tế

### Phase 2 KTV Review
- [ ] `qa-screenshots/persona-ktv/` chứa ≥30 PNG
- [ ] `qa-screenshots/persona-ktv/coverage.md` exists with ≥141 `[x]` checkboxes (≥85% of 166)
- [ ] Each `[x]` line has note (Vietnamese for KTV: "OK", "Lúng túng", "Không hiểu", v.v.)
- [ ] In-progress notes có ≥20 KTV findings
- [ ] Test user `chihoa@test.com` đã tạo + login successful (verify console)

### Phase 3 Report
- [ ] File `docs/design-qa-proposals/asset-polishing-personas-review.md` exists
- [ ] Report có ≥35 findings tổng (grep IDs `PM-` + `KTV-` count)
- [ ] Executive Summary table populated với scores 0-10 + counts
- [ ] Cross-Cutting Issues section ≥3 entries
- [ ] Prioritized Fix List có ≥5 P0/P1 items với estimate
- [ ] Suggested v1.2 Sprint Scope section có total estimate
- [ ] Appendix Screenshots Index liệt kê ≥36 screenshot rows

### Phase 4 Standard
- [ ] Report committed (git log shows commit)
- [ ] Auto-fix commits (nếu có) follow format `fix(asset-polishing): ... (review #{persona-ID})` (verify grep)
- [ ] Total auto-fix commits ≤ 50 (PM 20 + KTV 30 cap)
- [ ] No commits ngoài: review report + auto-fix items + screenshots/coverage. Verify via:
      `git log feat/asset-polishing --since="task-start" --pretty=format:"%s" | grep -vE "^(fix.*review #|docs.*personas-review|qa.*coverage)" | wc -l == 0`
- [ ] Bench migrate + build pass after all auto-fixes (verify in last commit)
- [ ] Report Section "Auto-Fixed in Review" liệt kê tất cả items đã apply + commit SHA
- [ ] MEMORY.md có entry mới cho v1.2 candidate scope (only deferred items)

## Constraints

- **Auto-fix CHỈ trong tier của persona** (xem Tiered Fix Policy section). Tier 4 items → log only.
- **Cap auto-fix:** PM ≤ 20 total, KTV ≤ 30 total. Vượt cap → log only.
- **KHÔNG tạo DocType mới**, không thêm field, không đổi workflow/permission/JE routing
- **KHÔNG sửa Python controller logic** (chỉ JSON / JS / CSV / HTML print format)
- Test user `chihoa@test.com` được tạo qua console, sau Phase 2 KHÔNG xóa (giữ cho v1.2 testing)
- Screenshots PNG, không quá 2MB mỗi file
- Findings KHÔNG duplicate giữa 2 personas — cross-cutting nằm ở section riêng
- Recommendation KHÔNG được vague ("cần cải thiện") — phải actionable ("đổi label X → Y", "thêm tooltip Z", "di chuyển button A đến vị trí B")
- Severity rationale phải có (P0 = blocking, P1 = confusing đa số user, P2 = minor)
- Mỗi auto-fix commit atomic + message format `fix(asset-polishing): {desc} (review #{persona-ID})`
- Sau auto-fix làm bench cycle phù hợp + verify regression không xảy ra

## Verification Commands

test -f docs/design-qa-proposals/asset-polishing-personas-review.md
test -d qa-screenshots/persona-pm
test -d qa-screenshots/persona-ktv
test -f qa-screenshots/persona-pm/coverage.md
test -f qa-screenshots/persona-ktv/coverage.md
sh -c 'count=$(find qa-screenshots/persona-pm -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 30'
sh -c 'count=$(find qa-screenshots/persona-ktv -name "*.png" 2>/dev/null | wc -l); test "$count" -ge 30'
sh -c 'pm_checked=$(grep -cE "^\[x\]" qa-screenshots/persona-pm/coverage.md); test "$pm_checked" -ge 133'
sh -c 'ktv_checked=$(grep -cE "^\[x\]" qa-screenshots/persona-ktv/coverage.md); test "$ktv_checked" -ge 141'
sh -c 'pm_blank=$(grep -cE "^\[x\] [^—]+ —\s*$" qa-screenshots/persona-pm/coverage.md 2>/dev/null || echo 0); test "$pm_blank" -eq 0'
sh -c 'ktv_blank=$(grep -cE "^\[x\] [^—]+ —\s*$" qa-screenshots/persona-ktv/coverage.md 2>/dev/null || echo 0); test "$ktv_blank" -eq 0'
sh -c 'count=$(grep -cE "^(PM|KTV)-[0-9]+" docs/design-qa-proposals/asset-polishing-personas-review.md); test "$count" -ge 35'
sh -c 'pm_count=$(grep -cE "^PM-[0-9]+" docs/design-qa-proposals/asset-polishing-personas-review.md); test "$pm_count" -ge 15'
sh -c 'ktv_count=$(grep -cE "^KTV-[0-9]+" docs/design-qa-proposals/asset-polishing-personas-review.md); test "$ktv_count" -ge 20'
grep -q "Cross-Cutting Issues" docs/design-qa-proposals/asset-polishing-personas-review.md
grep -q "Prioritized Fix List" docs/design-qa-proposals/asset-polishing-personas-review.md
grep -q "v1.2 Sprint Scope" docs/design-qa-proposals/asset-polishing-personas-review.md
grep -q "Executive Summary" docs/design-qa-proposals/asset-polishing-personas-review.md
sh -c 'autofix_count=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "fix.*review #(PM|KTV)-" 2>/dev/null || echo 0); test "$autofix_count" -le 50'
sh -c 'pm_autofix=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "review #PM-" 2>/dev/null || echo 0); test "$pm_autofix" -le 20'
sh -c 'ktv_autofix=$(git log feat/asset-polishing --pretty=format:"%s" | grep -cE "review #KTV-" 2>/dev/null || echo 0); test "$ktv_autofix" -le 30'
grep -qE "^## Auto-Fixed in Review" docs/design-qa-proposals/asset-polishing-personas-review.md
git log --oneline feat/asset-polishing | grep -qE "2-persona design QA review"

## Live Testing Procedure

### Setup browser session
1. cwd = `/home/long/long/frappe-bench-dcnet/.worktrees/vn_accounting-asset-polishing`
2. Verify bench đang chạy: `curl -s http://dcnet.localhost:8001/api/method/ping || echo "bench not running, start: cd /home/long/long/frappe-bench-dcnet && bench start"`
3. Use Playwright MCP for stateful auth (cookies persist across multi-step QA)

### Per-surface review pattern
For each surface in scope list:
1. `mcp__plugin_playwright_playwright__browser_navigate` to URL
2. `mcp__plugin_playwright_playwright__browser_take_screenshot` to `qa-screenshots/persona-<pm|ktv>/<surface-slug>.png`
3. `mcp__plugin_playwright_playwright__browser_snapshot` (DOM tree) for inspection
4. `mcp__plugin_playwright_playwright__browser_console_messages` to capture any errors
5. For Persona KTV: try interactions (fill field, click button, navigate) to find UX friction
6. Add findings to in-memory notes; final flush to report at Phase 3

### Test user creation (Phase 2 setup)
```python
# bench --site dcnet.localhost console
import frappe
if not frappe.db.exists("User", "chihoa@test.com"):
    user = frappe.get_doc({
        "doctype": "User",
        "email": "chihoa@test.com",
        "first_name": "Hoa",
        "last_name": "Nguyễn",
        "language": "vi",
        "send_welcome_email": 0,
        "new_password": "testpass123",
        "roles": [{"role": "Accounts User"}, {"role": "Employee"}]
    })
    user.insert()
    frappe.db.commit()
print("Test user ready")
```

### Worktree dance
NOT needed for this task — no code changes. apps/vn_accounting stays at whatever current state. Only edit files in `docs/` + `qa-screenshots/` of worktree.

## Agent Persona

You are a senior UX researcher specializing in business software. You can switch lenses fluently between:

**Lens 1 — PM (Frappe UI):**
- 5+ years building/maintaining Frappe/ERPNext apps
- Pattern memory: knows that Submit primary button is top-right, Save is implicit on form close, "Menu" dropdown holds destructive actions
- Compares new DocTypes against established Frappe modules (Sales Invoice, Customer, Asset native, ToDo) for consistency
- Cares about: user can predict where to click after seeing 1 form

**Lens 2 — Kế toán viên VN (Chị Hoa):**
- 10+ years VN accounting experience, but Frappe is week 1
- Vietnamese is primary language; English only for cryptic technical terms (still avoidable)
- Cares about: "tôi click cái này thì sao? lỡ sai có sửa được không?", "chỗ này điền gì?", "chuẩn VN không?"
- Reads: TT99/2025, mẫu sổ legal, biên bản cần đầy đủ chữ ký

You always:
- Switch persona explicitly; clearly mark each finding with persona ID prefix
- Recommend ACTIONABLE fixes (specific text/position/behavior change)
- Reference Frappe convention or VN accounting standard when applicable
- Prioritize ruthlessly (P0/P1/P2) with rationale

You NEVER:
- Modify code in this task (read-only)
- Skip screenshots — visual evidence required for each finding
- Vague recommendations ("improve UX", "make better")
- Mix persona findings (separate sections)

## Model

auto

## Time Budget

- Max hours: 10 (bumped 8 → 10 — auto-fix tier requires bench cycles + per-fix verify)
- Max sessions: 14 (PM ~6, KTV ~6, Report ~2)
- Per-session minutes: 30

**Per-phase session estimate:**
- Phase 1 PM (≥133 interactions + ≤20 auto-fix với bench cycle): 6 sessions
- Phase 2 KTV (≥141 interactions + ≤30 auto-fix): 6 sessions
- Phase 3 Report consolidation (gồm Auto-Fixed section + commit links): 2 sessions
