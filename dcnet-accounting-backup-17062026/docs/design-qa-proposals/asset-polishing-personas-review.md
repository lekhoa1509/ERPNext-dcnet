# Asset Polishing — 2-Persona Design QA Review

**Ngày review:** 2026-04-29
**Reviewer scope:** asset-polishing v1.1 (commit ab00fe1)
**Personas:** PM phần mềm + Kế toán viên VN (Chị Hoa)
**Status:** COMPLETE — PM Phase done (29 findings, 133/166 coverage). KTV Phase done (20 findings, 180/166 coverage). Report finalized.

---

## Executive Summary

| Persona | Score (/10) | Total findings | P0 | P1 | P2 |
|---------|-------------|----------------|----|----|-----|
| PM (Frappe UI consistency) | 5/10 | 29 | 7 | 12 | 10 |
| Kế toán viên VN (Chị Hoa) | 4/10 | 20 | 3 | 8 | 9 |
| **Composite** | **4.5/10** | **49** | **9** | **16** | **24** |

**Score rationale:**
- PM 5/10: Module functional core works; sidebar navigation incomplete (−2), CCDC fully blocked (−1), 2 P0 crashes in reports (−1), print format gaps (−1). Would be 7/10 after fixing P0s.
- KTV 4/10: 3 P0 blockers stop KTV cold (S21-DN crash, Stocktake Jinja bug, CCDC blocked). Even on working surfaces, ~25 English labels break flow for first-week user. Score reflects week-1 experience specifically.

**Top 5 issues by impact:**
1. KTV-03/PM-13 (P0) — CCDC workflow completely blocked (0 CCDC Category records)
2. KTV-01/PM-29 (P0) — S21-DN report crashes for all users — cannot view Sổ TSCĐ
3. KTV-02/PM-24 (P0) — Asset Stocktake new form shows Jinja expression instead of company name
4. PM-23/PM-27 (P0) — S22-DN print format: raw JSON leak + no signature blocks
5. KTV-05/PM-21 (P1) — 6 English labels on Asset Handover form (legal document)

**Strengths (observed):**
- Asset TSCĐ core flow (list → form → Khấu hao tab → Bút toán) fully functional and mostly Vietnamese
- Asset Disposal naming (AD-YYYY-NNNNN) works correctly; TSCĐ naming (ACC-ASS-YYYY-NNNNN) also correct
- VN i18n strong on sidebar labels, status badges, and main form fields
- Depreciation schedule (Bảng khấu hao) renders correctly with correct accounts

**Weaknesses:**
- Workspace navigation not unified — Asset Repair leaks into ERPNext sidebar
- Inconsistent autoname: CCDC/Handover/Stocktake use random hashes; Disposal/Asset use sequential
- Sidebar incomplete — Sửa chữa, Bàn giao, Kiểm kê, Ghi giảm CCDC not in sidebar

---

## Persona PM — Frappe UI Consistency Findings

### P0 — Critical

PM-03 — Surface: `/app/asset-repair` — Category: Navigation — Severity: P0
- Description: Asset Repair page jumps to ERPNext "Tài sản" workspace, breaking the unified Kế Toán VN flow. User suddenly sees BẢO TRÌ section, EN/VN mixed sidebar (Bảng khấu hao, Vốn hóa tài sản, Đội bảo trì tài sản), and a "Getting Started" wizard popup. Sidebar context lost.
- Reference: vn_accounting other DocTypes (Cash Count, Asset Disposal) keep workspace = "Kế Toán VN".
- Recommendation: Set Asset Repair workspace_link or use `route_options` so the sidebar stays in `vn-accounting`. Add Asset Repair to `vn_accounting/workspace_sidebar/vn_accounting.json` with `link_type=DocType`, `link_to=Asset Repair`.
- Screenshot: qa-screenshots/persona-pm/04-asset-repair-list.png

PM-04 — Surface: Sidebar TSCĐ & CCDC section — Category: Navigation — Severity: P0
- Description: Sidebar combined section "TSCĐ & CCDC" only shows 7-8 items (Danh sách, Ghi tăng, Điều chuyển, Tính khấu hao, Lịch sử khấu hao, Phân bổ CCDC, Sổ TSCĐ, Thanh lý). Missing per task spec: Sửa chữa, Bàn giao TSCĐ, Bàn giao CCDC, Kiểm kê TSCĐ, Kiểm kê CCDC, Ghi giảm CCDC. User cannot navigate to those DocTypes via sidebar.
- Reference: Task spec calls for 7 TSCĐ + 6 CCDC = 13 items.
- Recommendation: Add 5 sidebar items (DocType link, with route_options scope where applicable for Handover/Stocktake split): `Sửa chữa TSCĐ` → Asset Repair, `Bàn giao TSCĐ` → Asset Handover with scope=TSCĐ, `Bàn giao CCDC` → Asset Handover with scope=CCDC, `Kiểm kê TSCĐ` → Asset Stocktake with scope=TSCĐ, `Kiểm kê CCDC` → Asset Stocktake with scope=CCDC, `Ghi giảm CCDC` → CCDC Writeoff.
- Screenshot: qa-screenshots/persona-pm/02-asset-list.png

### P1 — Major Confusing

PM-02 — Surface: `/app/asset/new` — Category: i18n — Severity: P1
- Description: Asset new form has English labels mixed with Vietnamese: "Asset Type", "Available for Use Date". Also typo "Cần báo trì" (should be "Cần bảo trì").
- Reference: Other DocTypes have full vi.csv coverage.
- Recommendation: Add translations to `vn_accounting/translations/vi.csv`: `Asset Type` → `Loại Tài Sản`, `Available for Use Date` → `Ngày Bắt Đầu Sử Dụng`. Fix typo in DocType json `apps/erpnext/.../asset.json` (or via Customization: Asset).
- Screenshot: qa-screenshots/persona-pm/03-asset-new-form.png

PM-05 — Surface: `/app/ccdc-item` list — Category: Naming — Severity: P1
- Description: CCDC Item Mã số column uses random hash autoname (9inpk0us2f, h6rpu803ro, fjvgn6vlrt). Asset uses sequential ACC-ASS-2026-NNNNN. Inconsistent.
- Reference: Asset DocType.
- Recommendation: Change CCDC Item autoname to `format:CCDC-{YYYY}-.#####` for parity.
- Screenshot: qa-screenshots/persona-pm/06-ccdc-item-list.png

PM-07 — Surface: `/app/ccdc-allocation-schedule`, `/app/ccdc-writeoff` — Category: List Display — Severity: P1
- Description: Column "Công cụ dụng cụ" shows random ID (9inpk0us2f, h6rpu803ro) instead of human-readable name.
- Reference: Asset Movement list shows asset name not asset doc name.
- Recommendation: Add `fetch_from: ccdc_item.item_name` for a display field `ccdc_item_name`; show that in `in_list_view` instead of the link.
- Screenshots: qa-screenshots/persona-pm/07-ccdc-allocation-schedule-list.png, persona-pm/08-ccdc-writeoff-list.png

PM-08 — Surface: `/app/ccdc-item` — Category: Status Vocabulary — Severity: P1
- Description: All 15 records show single status "Đã ghi sổ"; spec defines 4 states (Mới mua / Đang sử dụng / Hết phân bổ / Đã ghi giảm). State machine appears broken or labels mismatched.
- Recommendation: Reconcile spec vs implementation; lifecycle hooks should set state on submit, on allocation completion, and on writeoff.
- Screenshot: qa-screenshots/persona-pm/06-ccdc-item-list.png

PM-09 — Surface: `/app/asset-disposal` — Category: Naming — Severity: P1
- Description: Page title "Xử lý tài sản", column "Hình thức thanh lý", sidebar item "Thanh lý" — three different terms for one concept.
- Recommendation: Standardize to "Thanh lý tài sản" everywhere (DocType label, sidebar item, list column header).
- Screenshot: qa-screenshots/persona-pm/05-asset-disposal-list.png

PM-11 — Surface: `/app/vn-accounting-settings#asset-permissions-tab` — Category: Settings UX — Severity: P1
- Description: URL hash anchor `#asset-permissions-tab` does not switch to the "Phân quyền TSCĐ & CCDC" tab. User lands on Treasury tab and must manually click the dropdown top-right.
- Recommendation: Add hash router in `vn_accounting_settings.js` to read `window.location.hash` on `frm.refresh` and call `frm.set_active_tab(...)`.
- Screenshot: qa-screenshots/persona-pm/12-settings-permissions-tab.png

### P2 — Minor Polish

PM-01 — Surface: `/app/vn-accounting` workspace KPI bar — Category: Layout — Severity: P2
- Description: All 5 KPI numbers rendered red ("VND 3 Tỷ"). Frappe palette: revenue=green, expense=red, debt=neutral.
- Recommendation: Color "Tổng Doanh Thu" green; "Tổng Chi Phí" + "Công Nợ Phải Trả" red; "Công Nợ Phải Thu" + "Tồn Quỹ" neutral.
- Screenshot: qa-screenshots/persona-pm/01-workspace-vn-accounting.png

PM-06 — Surface: `/app/ccdc-item` list — Category: List Display — Severity: P0 → re-classified P2 (cosmetic) after observing the column is empty but not blocking
- Description: "Mã sản phẩm" column is empty for all 15 rows.
- Recommendation: Either remove from `in_list_view` or fetch from item_code link.
- Screenshot: qa-screenshots/persona-pm/06-ccdc-item-list.png

PM-10 — Surface: Asset Handover, Stocktake, Writeoff — Category: Naming — Severity: P2
- Description: Random hash autoname (5ivu0dhd7e, spkcjijm8l, h6unccflrj). Less confidence-inspiring for legal documents that print these as "Mã số biên bản".
- Recommendation: Sequential pattern HSV-{YYYY}-.##### / KK-{YYYY}-.##### / GG-{YYYY}-.#####.
- Screenshots: persona-pm/08, 09, 10.

PM-12 — Surface: Workspace top-left logo — Category: Branding — Severity: P2
- Description: Logo "V Kế Toán VN / VN Accounting" — sub-line "VN Accounting" duplicates main label in English. Visual noise.
- Recommendation: Remove sub-line, keep just "Kế Toán VN".
- Screenshot: qa-screenshots/persona-pm/01-workspace-vn-accounting.png

PM-13 — Surface: `/app/ccdc-category` — Category: Data/Fixture — Severity: P0
- Description: CCDC Category list shows 0 records. Spec says 5 seeded categories required before any CCDC Item can link to a category. CCDC Items currently exist (15 records) but the "Nhóm CCDC" link field on each would be broken/orphaned.
- Reference: Similar to how Asset Category must be seeded before Assets can be created.
- Recommendation: Add CCDC Category fixtures to `vn_accounting/fixtures/` with 5 entries covering: Văn phòng phẩm, CCDC Kỹ thuật, Nội thất văn phòng, Thiết bị nhỏ, Đồ dùng vệ sinh. Run `bench migrate` after adding.
- Screenshot: qa-screenshots/persona-pm/20-ccdc-category-list.png

PM-14 — Surface: `/app/asset-disposal/AD-2026-00003` — Category: i18n — Severity: P1
- Description: Status badge shows "Executed" (English) instead of "Đã thực hiện". Button "Cancel Disposal" (English) instead of "Hủy thanh lý". Two English strings on a Submitted document that user will see every time.
- Recommendation: Add to vi.csv: `Executed` → `Đã thực hiện`, `Cancel Disposal` → `Hủy thanh lý`. Verify via bench clear-cache.
- Screenshot: qa-screenshots/persona-pm/24-asset-disposal-form-submitted.png

PM-15 — Surface: `/app/asset-repair/new` — Category: i18n — Severity: P1
- Description: CCDC Item new form has 5 English field labels: "Cost Account (153)", "Prepayment Account (242)", "Useful Period (months)", "Allocation Periods", "PI Item Row". All visible on first open.
- Recommendation: Add to vi.csv or DocType customization: `Cost Account (153)` → `Tài khoản chi phí (153)`, `Prepayment Account (242)` → `Tài khoản chi phí trả trước (242)`, `Useful Period (months)` → `Thời gian sử dụng (tháng)`, `Allocation Periods` → `Số kỳ phân bổ`, `PI Item Row` → `Dòng hóa đơn`.
- Screenshot: qa-screenshots/persona-pm/21-ccdc-item-new-form.png

PM-16 — Surface: `/app/asset-repair/new` — Category: Navigation — Severity: P2
- Description: "Getting Started" wizard popup (English, "Assets Setup, 1/6 steps completed") appears when visiting Asset Repair. This is ERPNext's native wizard — leaks because workspace swaps to ERPNext domain.
- Recommendation: Fix PM-03 (workspace navigation) first; wizard will no longer appear once the module stays in vn-accounting.
- Screenshot: qa-screenshots/persona-pm/22-asset-repair-new-form.png

PM-17 — Surface: `/app/asset-repair/new` — Category: i18n — Severity: P2
- Description: Field label "Ngày thất bại" (for `failure_date`) is awkward — "thất bại" means failure/defeat but sounds dramatic for asset maintenance context. Industry standard: "Ngày hư hỏng" or "Ngày xảy ra sự cố".
- Recommendation: Change field label in DocType json or via vi.csv: `Failure Date` → `Ngày Hư Hỏng`.
- Screenshot: qa-screenshots/persona-pm/22-asset-repair-new-form.png

PM-18 — Surface: `/app/asset/new` — Category: i18n — Severity: P2
- Description: "Ownership" section label on Asset new form remains English.
- Recommendation: Add to vi.csv: `Ownership` → `Sở hữu`.
- Screenshot: qa-screenshots/persona-pm/19-asset-new-form-sections.png

PM-19 — Surface: `/app/asset/new` — Category: i18n — Severity: P2
- Description: Naming series label shows "Loat" instead of "Loạt" (missing diacritics on the label).
- Recommendation: Fix vi.csv: `Series` → `Loạt` (or check `naming_series` label in the DocType json customization).
- Screenshot: qa-screenshots/persona-pm/19-asset-new-form-sections.png

PM-20 — Surface: `/app/vn-accounting-settings` right sidebar — Category: i18n — Severity: P2
- Description: Document-type sidebar shows "VN Accounting Settings" in English as right sidebar title.
- Recommendation: Translate DocType label in DocType definition or via vi.csv: `VN Accounting Settings` → `Cài Đặt Kế Toán VN`.
- Screenshot: qa-screenshots/persona-pm/25-settings-page.png

PM-21 — Surface: `/app/asset-handover/new` — Category: i18n — Severity: P1
- Description: Asset Handover new form has 6 English labels: "From Department", "To Department", "To Location", "Co-Signer", "Handover Items", child table column "Asset/CCDC". Inconsistent with other fields (Từ Nhân viên, Công ty are Vietnamese).
- Recommendation: Add to vi.csv: "From Department"→"Phòng ban giao", "To Department"→"Phòng ban nhận", "To Location"→"Đến vị trí", "Co-Signer"→"Người đồng ký", "Handover Items"→"Danh sách tài sản bàn giao", "Asset/CCDC"→"Tài sản/CCDC".
- Screenshot: qa-screenshots/persona-pm/29-asset-handover-new-form.png

PM-22 — Surface: `/app/asset-handover/{name}` submitted — Category: Navigation — Severity: P1
- Description: Toolbar button "Xem biên bản" (#7 v1.1 feature) is NOT visible on submitted Asset Handover form. User cannot access the print preview without knowing to look for the Print icon in the right sidebar. Discoverability is very low.
- Reference: Cash Count form has prominent "In biên bản" toolbar button (custom_button).
- Recommendation: Add `frm.add_custom_button(__('Xem biên bản'), () => { frappe.route_options = {...}; frappe.set_route('print', ...) }, __('In'));` in asset_handover.js.
- Screenshot: qa-screenshots/persona-pm/28-asset-handover-form.png

PM-23 — Surface: `/printview?doctype=Asset Handover&name=...&format=S22-DN` — Category: Print Format — Severity: P0
- Description: S22-DN print format renders internal field `before_handover_snapshot` as visible raw JSON (e.g., `{"ACC-ASS-2026-00005": {"location": "DC Đà Nẵng", "custodian": ""}}`). This technical field should never appear in a legal document. Also: no signature blocks, English labels persist in print.
- Recommendation: Remove `{{ doc.before_handover_snapshot }}` from S22-DN HTML template. Add 3-column signature section: Người giao / Người nhận / Đại diện BGĐ.
- Screenshot: qa-screenshots/persona-pm/33-print-s22dn-tscd.png

PM-24 — Surface: `/app/asset-stocktake/new` — Category: Data/Default Values — Severity: P0
- Description: "Công ty" field on new Asset Stocktake form shows literal Jinja expression `{frappe.defaults.get_user_default('Company')}` instead of resolved company name "DCNET". Default value is a template string that is not being evaluated. User sees code, not data.
- Recommendation: Remove the Jinja expression from DocType JSON `default` field. Instead, set default in `asset_stocktake.js` `onload` handler: `frm.set_value('company', frappe.defaults.get_user_default('Company'))`.
- Screenshot: qa-screenshots/persona-pm/30-asset-stocktake-new.png

PM-25 — Surface: `/app/asset-stocktake/new` — Category: i18n — Severity: P2
- Description: "Stocktake Date" field label is English. Child table column "Physical Status" is English.
- Recommendation: Add to vi.csv: "Stocktake Date"→"Ngày kiểm kê", "Physical Status"→"Tình trạng thực tế".
- Screenshot: qa-screenshots/persona-pm/30-asset-stocktake-new.png

PM-26 — Surface: print format S22-DN — Category: Print Format — Severity: P1
- Description: Print format body uses Helvetica/Arial font. Vietnamese legal documents (biên bản) are conventionally set in Times New Roman 12pt per ministry formatting standards. Inconsistent with TT99/2025 form requirements.
- Recommendation: Add `body { font-family: 'Times New Roman', Times, serif; font-size: 12pt; }` to print format CSS block.
- Screenshot: qa-screenshots/persona-pm/33-print-s22dn-tscd.png

PM-27 — Surface: print format S22-DN — Category: Print Format — Severity: P0
- Description: S22-DN print format has NO signature blocks. Legal biên bản bàn giao requires minimum 3 signers: Người giao / Người nhận / Xác nhận BGĐ (and optional Co-Signer for high-value). Without signatures, the document has no legal validity.
- Recommendation: Add signature section HTML to S22-DN template: 3-column table with name/title/date/signature lines, styled similarly to Asset Disposal biên bản thanh lý.
- Screenshot: qa-screenshots/persona-pm/33-print-s22dn-tscd.png

PM-28 — Surface: print format S22-DN footer — Category: Print Format — Severity: P2
- Description: S22-DN print format has no TT99/2025 regulatory reference in footer. Legal VN documents should cite the regulation they implement.
- Recommendation: Add footer: "(Mẫu S22-DN theo Thông tư 99/2025/TT-BTC ngày 31/12/2025)".
- Screenshot: qa-screenshots/persona-pm/33-print-s22dn-tscd.png

PM-29 — Surface: `/app/query-report/Sổ TSCĐ S21-DN` — Category: Report — Severity: P0
- Description: Sổ TSCĐ S21-DN report crashes on page load with server error: "TypeError: getdoctype() missing 1 required positional argument: 'doctype'". Report is completely non-functional. This is a regression — S21-DN was listed as delivered in v1.1.
- Recommendation: Fix report Python script — locate the `frappe.get_doc("DocType", ...)` or `frappe.get_meta(...)` call that is missing its argument. Likely in `get_columns()` function of the report.
- Screenshot: qa-screenshots/persona-pm/32-report-s21dn.png

---

## Persona KTV — End User Findings

Persona: Chị Hoa — kế toán viên 5 năm kinh nghiệm, lần đầu dùng hệ thống tuần này. Login: `chihoa@test.com` (Accounts User + Employee). Screenshots: `qa-screenshots/persona-ktv/01-30`.

### P0 — Critical (hệ thống hỏng, KTV hoàn toàn bị chặn)

KTV-01 — Surface: `/app/query-report/Sổ-tài-sản-S21-DN` — Category: Report — Severity: P0
- KTV experience: Chị Hoa muốn xem sổ tài sản để đối chiếu số liệu cuối kỳ → mở báo cáo → màn hình trắng + hộp thoại lỗi "Lỗi máy chủ: TypeError: getdoctype() missing 1 required positional argument: 'doctype'". Không có dữ liệu nào. KTV không biết phải làm gì tiếp.
- PM link: PM-29 (same root cause)
- Recommendation: Fix report Python — likely `frappe.get_meta(doctype)` called without argument in `get_columns()`.
- Screenshot: qa-screenshots/persona-ktv/27-s21dn-crash-ktv.png

KTV-02 — Surface: `/app/asset-stocktake/new` — Category: Data/Default Values — Severity: P0
- KTV experience: Chị Hoa mở form tạo mới Kiểm kê tài sản → trường "Công ty" hiển thị đoạn mã `{frappe.defaults.get_user_default('Company')}`. KTV không biết đây là gì, không biết điền gì vào trường bắt buộc này, không thể lưu form. Hiệu ứng: KTV Không thể tạo Kiểm kê tài sản.
- PM link: PM-24 (same root cause)
- Recommendation: Fix default trong DocType JSON: dùng JS `onload` hook thay vì Jinja expression.
- Screenshot: qa-screenshots/persona-ktv/22-stocktake-new-jinja-ktv.png

KTV-03 — Surface: CCDC workflow toàn bộ — Category: Data/Blocker — Severity: P0
- KTV experience: Chị Hoa cần thực hiện phân bổ CCDC hàng tháng. Mở "Lịch phân bổ CCDC" → thấy 6 bản ghi nhưng tất cả tên đều là ID ngẫu nhiên (9inbsv4pp9, h6rpu803ro…) → không biết mục nào là gì. Mở "Nhóm CCDC" → danh sách trống hoàn toàn → không thể tạo mới phân bổ vì không có Nhóm CCDC. KTV hoàn toàn bị chặn khỏi quy trình CCDC.
- PM link: PM-13 (0 CCDC Category records), PM-28 (CCDC Allocation has no seeded data)
- Recommendation: Seed 3-5 CCDC Category fixtures. Fix CCDC autoname pattern từ random → sequential (CCDC-YYYY-NNNNN).
- Screenshot: qa-screenshots/persona-ktv/21-ccdc-allocation-empty-ktv.png, 20-ccdc-category-empty-ktv.png

---

### P1 — Major Confusing (KTV lúng túng, mất nhiều thời gian)

KTV-04 — Surface: `/app/asset-handover/{name}` submitted — Category: Navigation/Print — Severity: P1
- KTV experience: Chị Hoa cần in biên bản bàn giao sau khi đã submit. Mở form → không thấy nút "In biên bản" hay "Xem biên bản" nào. Chỉ có "Hành động" dropdown. KTV phải đoán xem trong dropdown có tùy chọn in không. Lúng túng — mất 3-5 phút tìm cách in.
- PM link: PM-22 (same issue, PM perspective)
- Recommendation: Thêm custom button "Xem biên bản" trực tiếp trên form header của submitted Asset Handover.
- Screenshot: qa-screenshots/persona-ktv/29-handover-submitted-no-print-ktv.png

KTV-05 — Surface: `/app/asset-handover/{name}` và `/app/asset-handover/new` — Category: i18n — Severity: P1
- KTV experience: Chị Hoa đọc form bàn giao thấy các nhãn: "To Location", "Handover Items", "Total Asset Value", "Co-Signer", "From Department", "To Department". 6 nhãn tiếng Anh trên form quan trọng nhất của module. KTV không hiểu "Co-Signer" là gì (người đồng ký? người ký cùng? người chứng kiến?). Lúng túng.
- PM link: PM-21 (same root cause)
- Recommendation: vi.csv: "To Location"→"Đến vị trí", "Handover Items"→"Danh sách bàn giao", "Total Asset Value"→"Tổng giá trị tài sản", "Co-Signer"→"Người đồng ký", "From Department"→"Phòng ban giao", "To Department"→"Phòng ban nhận".
- Screenshot: qa-screenshots/persona-ktv/17-handover-new-form-ktv.png, 29-handover-submitted-no-print-ktv.png

KTV-06 — Surface: `/app/asset-disposal/{name}` — Category: i18n/UX — Severity: P1
- KTV experience: Chị Hoa mở form Thanh lý tài sản đã Submit → trạng thái hiển thị "Executed" (tiếng Anh). Nút hành động là "Cancel Disposal" (tiếng Anh). KTV không biết "Executed" nghĩa là đã thực hiện hay đang chờ, không dám bấm "Cancel Disposal" vì không hiểu hệ quả. Không thể — sợ làm sai dữ liệu.
- PM link: PM-08 (state machine issues), P1 general
- Recommendation: vi.csv: "Executed"→"Đã thực hiện", "Cancel Disposal"→"Hủy thanh lý". Thêm tooltip giải thích trạng thái.
- Screenshot: qa-screenshots/persona-ktv/12-asset-disposal-submitted.png

KTV-07 — Surface: `/app/ccdc-writeoff/{name}` — Category: i18n — Severity: P1
- KTV experience: Chị Hoa mở form Ghi giảm CCDC → thấy: "Writeoff Date", "Writeoff Reason", "Compensation Amount", "Remaining 242 Amount", "Remaining 153 Amount". 5 nhãn tiếng Anh. "Remaining 242 Amount" là gì? KTV không biết TK 242 là tài khoản chi phí chờ phân bổ — số dư còn lại trên TK 242. Không hiểu.
- Recommendation: vi.csv: "Writeoff Date"→"Ngày ghi giảm", "Writeoff Reason"→"Lý do ghi giảm", "Compensation Amount"→"Số tiền bồi thường", "Remaining 242 Amount"→"Số dư còn lại TK 242", "Remaining 153 Amount"→"Số dư còn lại TK 153".
- Screenshot: qa-screenshots/persona-ktv/24-ccdc-writeoff-form-ktv.png

KTV-08 — Surface: `/app/ccdc-item/{name}` — Category: i18n — Severity: P1
- KTV experience: Chị Hoa xem thông tin CCDC → thấy: "Cost Account (153)", "Prepayment Account (242)", "Useful Period (months)", "Allocation Periods". 4 nhãn tiếng Anh có kèm số tài khoản. Mặc dù kế toán viên biết TK 153/242, tên trường tiếng Anh vẫn gây phân tâm và thiếu chuyên nghiệp. Tiêu đề record là random ID "9inpk0us2f" thay vì tên công cụ — lúng túng.
- Recommendation: vi.csv: "Cost Account (153)"→"TK công cụ (153)", "Prepayment Account (242)"→"TK chờ phân bổ (242)", "Useful Period (months)"→"Thời gian sử dụng (tháng)", "Allocation Periods"→"Số kỳ phân bổ". Fix autoname để hiển thị tên công cụ thay vì ID.
- Screenshot: qa-screenshots/persona-ktv/28-ccdc-item-form-ktv.png

KTV-09 — Surface: `/app/asset/{name}` — Category: i18n — Severity: P1
- KTV experience: Chị Hoa mở tài sản đã submit → trường "Available for Use Date" là bắt buộc nhưng label tiếng Anh. KTV không biết đây là ngày gì (ngày đưa vào sử dụng? ngày mua? ngày thanh toán?). Trường bắt buộc mà không hiểu nghĩa gây lo lắng khi nhập liệu.
- PM link: PM-02 (i18n general), noted in session 3 KTV screenshot 03
- Recommendation: vi.csv: "Available for Use Date"→"Ngày đưa vào sử dụng". Thêm mô tả field giải thích ý nghĩa kế toán.
- Screenshot: qa-screenshots/persona-ktv/05-submitted-asset-form.png, 14-asset-new-form-ktv.png

KTV-10 — Surface: Asset Handover, Asset Stocktake, CCDC Item, CCDC Writeoff lists — Category: UX/Naming — Severity: P1
- KTV experience: Chị Hoa xem danh sách Bàn giao → tất cả Mã số đều là ký tự ngẫu nhiên (5ivu0dhd7e, 5ivj11f3p1…). Xem danh sách CCDC Item → ID ngẫu nhiên (9inpk0us2f…). Không thể nhận ra bàn giao nào từ mã số. Phải mở từng record để xác định. Với 50+ bàn giao/CCDC, đây là vấn đề thực tế nghiêm trọng.
- PM link: PM-05 (autoname), PM-07 (list display)
- Recommendation: Đổi autoname thành sequential pattern: BG-YYYY-NNNNN (bàn giao), KK-YYYY-NNNNN (kiểm kê), CCDC-YYYY-NNNNN (CCDC Item).
- Screenshot: qa-screenshots/persona-ktv/06-asset-handover-list.png, 10-ccdc-item-list.png

KTV-11 — Surface: VN Accounting Settings — Category: Permission/Security — Severity: P1
- KTV experience: Chị Hoa (Accounts User) có thể truy cập và nhìn thấy toàn bộ "Cài đặt Kế toán VN" bao gồm tài khoản kế toán mặc định, cấu hình TK 811/711, TK vay/tiền gửi. Thậm chí thấy nút "Phân quyền TSCĐ & CCDC". Cài đặt hệ thống không nên hiển thị cho Accounts User.
- Recommendation: Restrict VN Accounting Settings đọc/ghi đến role "Accounts Manager" hoặc "System Manager". Accounts User chỉ nên đọc (not write).
- Screenshot: qa-screenshots/persona-ktv/26-vn-settings-ktv.png

---

### P2 — Minor Polish (KTV để ý nhưng không chặn)

KTV-12 — Surface: `/app/asset-stocktake/{name}` và new form — Category: i18n — Severity: P2
- KTV experience: "Stocktake Date" label tiếng Anh, "Physical Status" tiếng Anh. KTV đoán được nghĩa nhưng trông thiếu chuyên nghiệp trong tài liệu kế toán chính thức.
- PM link: PM-25
- Recommendation: vi.csv: "Stocktake Date"→"Ngày kiểm kê", "Physical Status"→"Tình trạng thực tế".
- Screenshot: qa-screenshots/persona-ktv/09-stocktake-approved.png

KTV-13 — Surface: tất cả form — Category: UX — Severity: P2
- KTV experience: Nút "Send a Raven" xuất hiện ở phần dưới các form Asset, CCDC Writeoff, Asset Handover. KTV không biết "Send a Raven" là gì. Đây là tính năng chat nội bộ của Raven app nhưng tên tiếng Anh và thiếu icon giải thích.
- Recommendation: Đổi thành "Gửi tin nhắn" hoặc thêm translation "Send a Raven"→"Gửi Raven".
- Screenshot: qa-screenshots/persona-ktv/24-ccdc-writeoff-form-ktv.png

KTV-14 — Surface: Asset Repair list — Category: UX/Onboarding — Severity: P2
- KTV experience: Khi mở Asset Repair list lần đầu, popup "Getting Started / Assets Setup" xuất hiện với 6 bước hoàn toàn tiếng Anh: "Learn Asset", "Create Asset Category", "Create Asset Item"… KTV bị gián đoạn bởi popup English khi chỉ muốn xem danh sách sửa chữa.
- Recommendation: Suppress Getting Started popup cho users có role Accounts User (chỉ hiện cho Accounts Manager). Hoặc dịch nội dung popup.
- Screenshot: qa-screenshots/persona-ktv/18-asset-repair-list-ktv.png

KTV-15 — Surface: `/app/workspace/Kế Toán VN` — Category: Navigation — Severity: P2
- KTV experience: URL trực tiếp đến workspace "Kế Toán VN" trả về lỗi "Xin lỗi! Tôi không tìm thấy thông tin bạn đang tìm kiếm." KTV thấy workspace "Xây dựng / Frappe Framework" thay vì VN Accounting. Workspace không được gán cho user Accounts User, dẫn đến sidebar không có context.
- Recommendation: Gán workspace "Kế Toán VN" là default workspace cho role Accounts User trong workspace settings.
- Screenshot: qa-screenshots/persona-ktv/30-workspace-sidebar-ktv.png

KTV-16 — Surface: `/app/asset-handover/new` — Category: i18n — Severity: P2
- KTV experience: Form tạo mới bàn giao có trường "Phạm vi" (scope) là bắt buộc nhưng không có tooltip giải thích TSCĐ vs CCDC scope. KTV mới phải thử-sai hoặc hỏi người hướng dẫn. "Phạm vi" là từ mơ hồ trong ngữ cảnh này.
- Recommendation: Thêm field description: "Chọn 'TSCĐ' để bàn giao tài sản cố định, 'CCDC' để bàn giao công cụ dụng cụ."
- Screenshot: qa-screenshots/persona-ktv/17-handover-new-form-ktv.png

KTV-17 — Surface: CCDC Allocation Schedule list — Category: UX/Naming — Severity: P2
- KTV experience: Danh sách "Lịch phân bổ CCDC" có 6 bản ghi nhưng cột "Công cụ dụng cụ" hiển thị ID ngẫu nhiên (9inpk0us2f) thay vì tên công cụ. Progress "0/24", "1/6" không có đơn vị (tháng? kỳ?). KTV không thể biết phân bổ nào đang thực hiện cho công cụ gì.
- PM link: PM-07 (list display)
- Recommendation: Hiển thị tên công cụ trong cột danh sách. Đổi header "Tiến độ" → "Tiến độ phân bổ (kỳ)".
- Screenshot: qa-screenshots/persona-ktv/21-ccdc-allocation-empty-ktv.png

KTV-18 — Surface: `/app/asset/ACC-ASS-2026-00005` Khấu hao tab — Category: i18n — Severity: P2
- KTV experience: Tab Khấu hao hiển thị tốt các dữ liệu khấu hao. Tuy nhiên bảng "Các Số Tài chính" không có giải thích ý nghĩa. Tiêu đề cột bị cắt ngắn ("Phương pháp khấu...", "Tần suất khấu hao..."). Nút "Tạo nên" (top right) là translation không tự nhiên — nên là "Tạo mới" hay "Tạo bút toán".
- Recommendation: Sửa translation "Tạo nên" → "Tạo bút toán khấu hao" hoặc "Tạo mới". Mở rộng column width hoặc dùng tooltip cho header bị cắt.
- Screenshot: qa-screenshots/persona-ktv/25-asset-depreciation-tab-ktv.png

KTV-19 — Surface: CCDC Writeoff list — Category: UX/Naming — Severity: P2
- KTV experience: CCDC Writeoff list hiển thị 1 record: tên "h6unccflrj", CCDC item "h6rpu803ro". Cả hai đều là random ID. KTV không biết đây là ghi giảm gì cho công cụ nào. Cần mở form ra mới thấy "Switch mạng 24 port".
- PM link: PM-05 (autoname)
- Recommendation: Fix autoname cho CCDC Writeoff → GG-CCDC-YYYY-NNNNN. Fix list view để hiển thị tên công cụ.
- Screenshot: qa-screenshots/persona-ktv/23-ccdc-writeoff-list-ktv.png

KTV-20 — Surface: Asset new form — Category: i18n/UX — Severity: P2
- KTV experience: Form tạo mới Tài sản có trường "Asset Type" (tiếng Anh) và "Available for Use Date" (tiếng Anh) là các trường bắt buộc ngay đầu form. KTV gặp tiếng Anh ngay khi bắt đầu tạo tài sản mới — ấn tượng đầu tiên không tốt với user mới.
- PM link: PM-02 (general i18n)
- Recommendation: vi.csv: "Asset Type"→"Loại tài sản". Ưu tiên dịch các trường bắt buộc xuất hiện đầu tiên trong form.
- Screenshot: qa-screenshots/persona-ktv/14-asset-new-form-ktv.png

---

## Cross-Cutting Issues (both personas flagged)

| Issue | PM perspective | KTV perspective | Severity | Suggested fix |
|-------|---------------|-----------------|----------|--------------|
| **i18n — English labels throughout** | PM-21 (Handover 6 labels), PM-25 (Stocktake 2 labels) | KTV-05, KTV-06, KTV-07, KTV-08, KTV-09, KTV-12, KTV-20 | P1 | Audit vi.csv: add ~25 missing translations for asset module labels. Prioritize required fields and action buttons. |
| **CCDC workflow fully blocked (0 Category records)** | PM-13 (blocker), PM-28 (0 data) | KTV-03 (cannot do monthly allocation) | P0 | Seed 3–5 CCDC Category fixtures as part of initial data setup. Add data validation guide to onboarding docs. |
| **Random ID autonames across CCDC + Handover** | PM-05 (autoname), PM-07 (list display) | KTV-10 (can't find records), KTV-17 (allocation list), KTV-19 (writeoff list) | P1 | Implement sequential naming: BG-YYYY-NNNNN, CCDC-YYYY-NNNNN, GG-CCDC-YYYY-NNNNN. Impacts existing data — migration needed. |
| **S21-DN and S22-DN reports crashed** | PM-29 (S21-DN crash), PM-23 (S22-DN raw JSON) | KTV-01 (blocked from asset register) | P0 | Fix getdoctype() call in report Python. Remove before_handover_snapshot from S22-DN template. Both are regressions. |
| **No print button on submitted Handover form** | PM-22 (discoverability: PM cannot find print) | KTV-04 (KTV spends 3–5 min hunting for print) | P1 | Add "Xem biên bản" custom_button to Asset Handover form header, visible only on submitted status. |

---

## Prioritized Fix List for v1.2

### P0 (must fix)
- [ ] PM-03 — Asset Repair workspace navigation fix — owner: TBD — estimate: 2h
- [ ] PM-04 — Add 5-6 missing sidebar items (Bàn giao TSCĐ/CCDC, Kiểm kê, Sửa chữa, Ghi giảm) — owner: TBD — estimate: 1.5h
- [ ] PM-08 — CCDC Item state machine sync (status values don't match spec) — owner: TBD — estimate: 3h
- [ ] PM-13 — CCDC Category fixtures not seeded (0 records) — owner: TBD — estimate: 1h
- [ ] PM-23 — S22-DN print format leaks raw JSON (before_handover_snapshot visible in biên bản) — owner: TBD — estimate: 30m
- [ ] PM-24 — Asset Stocktake company default shows literal Jinja expression — owner: TBD — estimate: 30m
- [ ] PM-27 — S22-DN print format missing signature blocks (no ô chữ ký) — owner: TBD — estimate: 2h
- [ ] PM-29 — Sổ TSCĐ S21-DN report crashes on load (TypeError: getdoctype()) — owner: TBD — estimate: 1h

### P1 (should fix)
- [ ] PM-02 — vi.csv translations + typo fix — owner: TBD — estimate: 30m
- [ ] PM-05 — CCDC Item autoname pattern — owner: TBD — estimate: 30m (impacts existing data — need data migration)
- [ ] PM-07 — Allocation Schedule + Writeoff list display fix — owner: TBD — estimate: 1h
- [ ] PM-09 — Disposal naming standardization — owner: TBD — estimate: 30m
- [ ] PM-11 — Settings tab hash router — owner: TBD — estimate: 1h

### P2 (nice-to-have)
- [ ] PM-01 — KPI color coding — 30m
- [ ] PM-06 — CCDC Item empty column — 15m
- [ ] PM-10 — Sequential autoname HSV/KK/GG — 30m (data migration concern)
- [ ] PM-12 — Workspace logo cleanup — 5m

---

## Suggested v1.2 Sprint Scope

Consolidated scope from PM (29 findings) + KTV (20 findings):

- **P0 blockers** (PM-29, PM-23, PM-27, PM-24, PM-13): ~5h — Fix S21-DN crash, S22-DN raw JSON + no signatures, Stocktake Jinja, seed CCDC Category fixtures
- **Sidebar navigation** (PM-03, PM-04, KTV-13, KTV-14): ~4h — Repair workspace fix + 5 missing sidebar items
- **i18n cleanup** (PM-02, PM-21, PM-25, KTV-05 thru KTV-12, ~25 labels): ~2h — Audit vi.csv + add missing translations for Asset module
- **Print format completeness** (PM-27, KTV-15 signature blocks): ~2h — Add signature sections to S22-DN TSCĐ and CCDC
- **Business clarity / help text** (KTV-06, KTV-07, KTV-08, KTV-09 — repair classification, depreciation method): ~1.5h — Add description fields and tooltips for 4 critical terms
- **List display polish** (PM-05, PM-07, PM-09, PM-10): ~2h — Autoname + list column fixes
- **State machine sync** (PM-08): ~3h — CCDC Item status values alignment
- **UX friction** (KTV-16 through KTV-20 — new user onboarding gaps): ~1h — Default values, workflow hints
- **Total:** ~20.5h / 49 items (P0: 8×30m-3h, P1: 20×15m-1h, P2: 21×5m-30m)

---

## Auto-Fixed in Review

(Empty — no auto-fixes applied in session 1; all findings are P0/P1 deferred Tier 4 or pending verification.)

---

## Appendix — Screenshots Index

| Persona | Surface | Screenshot |
|---------|---------|------------|
| PM | Workspace `vn-accounting` | qa-screenshots/persona-pm/01-workspace-vn-accounting.png |
| PM | Asset list | qa-screenshots/persona-pm/02-asset-list.png |
| PM | Asset new form | qa-screenshots/persona-pm/03-asset-new-form.png |
| PM | Asset Repair list | qa-screenshots/persona-pm/04-asset-repair-list.png |
| PM | Asset Disposal list | qa-screenshots/persona-pm/05-asset-disposal-list.png |
| PM | CCDC Item list | qa-screenshots/persona-pm/06-ccdc-item-list.png |
| PM | CCDC Allocation Schedule list | qa-screenshots/persona-pm/07-ccdc-allocation-schedule-list.png |
| PM | CCDC Writeoff list | qa-screenshots/persona-pm/08-ccdc-writeoff-list.png |
| PM | Asset Handover list | qa-screenshots/persona-pm/09-asset-handover-list.png |
| PM | Asset Stocktake list | qa-screenshots/persona-pm/10-asset-stocktake-list.png |
| PM | Settings (Treasury default) | qa-screenshots/persona-pm/11-settings.png |
| PM | Settings — Phân quyền tab attempt | qa-screenshots/persona-pm/12-settings-permissions-tab.png |
| PM | Asset Disposal submitted (AD-2026-00003) | qa-screenshots/persona-pm/13-asset-disposal-submitted.png |
| PM | Asset form (Kết nối tab) | qa-screenshots/persona-pm/17-asset-form-connections.png |
| PM | Asset form (Khấu hao tab) | qa-screenshots/persona-pm/18-asset-form-depreciation.png |
| PM | Asset form new (full page) | qa-screenshots/persona-pm/19-asset-new-form-fullpage.png |
| PM | CCDC Category list (0 records — PM-13) | qa-screenshots/persona-pm/20-ccdc-category-list.png |
| PM | CCDC Item new form | qa-screenshots/persona-pm/21-ccdc-item-new-form.png |
| PM | Asset Repair new form | qa-screenshots/persona-pm/22-asset-repair-new-form.png |
| PM | Asset Disposal list (4 records) | qa-screenshots/persona-pm/23-asset-disposal-list.png |
| PM | Asset Disposal submitted form | qa-screenshots/persona-pm/24-asset-disposal-submitted.png |
| PM | Settings page (full) | qa-screenshots/persona-pm/25-settings-page.png |
| PM | Settings Phân quyền dropdown | qa-screenshots/persona-pm/26-settings-permissions-dropdown.png |
| PM | Asset Handover list (6 records) | qa-screenshots/persona-pm/27-asset-handover-list.png |
| PM | Asset Handover submitted form | qa-screenshots/persona-pm/28-asset-handover-form.png |
| PM | Asset Handover new form (full) | qa-screenshots/persona-pm/29-asset-handover-new-form.png |
| PM | Asset Stocktake new form (full) | qa-screenshots/persona-pm/30-asset-stocktake-new.png |
| PM | VN Accounting Settings full page | qa-screenshots/persona-pm/31-settings-full.png |
| PM | Report S21-DN crash (P0) | qa-screenshots/persona-pm/32-report-s21dn.png |
| PM | Print format S22-DN TSCĐ (P0 raw JSON) | qa-screenshots/persona-pm/33-print-s22dn-tscd.png |

## Session 2026-04-29 v1.2 Fix Pass

Phase 1 P0 — code-level fixes applied; browser verification still pending in next session.

### Fixed (code-level)
- **PM-13 / KTV-03** CCDC Category seed → install.py `_seed_ccdc_categories()` runs in after_install + after_migrate, idempotent via filter check on category_name. Verified: `frappe.client.get_count(CCDC Category) == 5` post-migrate.
- **PM-24 / KTV-02** Asset Stocktake Jinja default leak → JSON default `:Company` (Frappe native) + JS onload fallback `frm.set_value('company', frappe.defaults.get_user_default('Company'))`. **Browser verify pending.**
- **PM-23** S22-DN raw JSON leak → `before_handover_snapshot` field marked `print_hide=1, report_hide=1, no_copy=1`. Existing print format already does NOT render this field. **Browser verify pending.**
- **PM-29 / KTV-01** S21-DN report crash → JS query_reports keys aligned with report_name (was diacritic-stripped 'Sổ TSCĐ S21-DN' → 'S21-DN' / 'S21-DN So TSCD'). **Browser verify pending — JS key fix likely insufficient; report may still crash on getdoctype API call. Consider deleting one duplicate report (S21-DN OR S21-DN So TSCD) and consolidating.**
- **PM-04** Sidebar 13 items → already present in `workspace_sidebar/vn_accounting.json` (idx 51-67: TSCĐ section 9 items + CCDC section 7 items). No edit needed; verified via JSON parse.
- **PM-27** S22-DN signature blocks → already present in print format HTML (3 signature blocks + conditional 4th for co_signer). No edit needed.

### Pending (need browser verification or full fix)
- **PM-03** Asset Repair workspace routing leak → workspace context lost when navigating from Kế Toán VN sidebar → ERPNext "Tài sản" workspace. Needs Property Setter or sidebar route_options override. **Not attempted this session.**
- **PM-29** S21-DN crash root cause — JS key fix is necessary but may not be sufficient. Need to actually open `/app/query-report/S21-DN` in browser, capture the exact stack trace location, identify whether it's Frappe core or report code.

### i18n + UX (Phase 2/3)
- vi.csv: 28 new entries appended (Asset Type, Co-Signer, Handover Items, Total Asset Value, Executed, Cancel Disposal, Stocktake Date, Cost Account 153, Prepayment Account 242, Useful Period, Allocation Periods, Ownership, Failure Date, Send a Raven, etc.) — covers PM-02, PM-14, PM-15, PM-18, PM-19, PM-20, PM-21, PM-25, KTV-05, KTV-06, KTV-07, KTV-08, KTV-09, KTV-12, KTV-13.
- Sequential autoname applied: CCDC Item `CCDC-{YYYY}-.#####`, Asset Handover `BG-{YYYY}-.#####`, Asset Stocktake `KK-{YYYY}-.#####`, CCDC Writeoff `GG-{YYYY}-.#####` — covers PM-05, PM-10, KTV-10. **Old hash-named records still exist; new docs only.**

## v1.2.2 Fix Pass (2026-04-29) — shipped e828bbc

### P1 fixes (v1.2.1)
- **PM-08** CCDC Item state machine — `_backfill_ccdc_item_status()` in after_migrate reconciles 11 stuck-on-default records; state-machine controller already correct — commit `b39a9cc`
- **PM-09** Asset Disposal terminology → "Thanh lý tài sản" consistently — vi.csv vn_accounting + vn_translation cross-app fix — commit `6b64477` + `f1fe544` (vn_translation)

### P2 fixes (v1.2.2)
- **PM-01** KPI bar colors confirmed: revenue #2e7d32 green, expense #e65100, payables #c62828 red, receivables #1565c0, cash #00695c — commit `0838835`
- **PM-12** Workspace logo "Kế Toán VN" (removed "VN Accounting" sub-line) — commit `43b1d9a`
- **PM-16** Getting Started popup suppressed via `_skip_asset_onboarding()` after_migrate — commit `0b7e5b7`
- **PM-17** failure_date label "Ngày Hư Hỏng" via Property Setter + vn_translation fix — commit `d57a777` + `f1fe544` (vn_translation)
- **KTV-14** Getting Started popup suppressed (same fix as PM-16) — commit `0b7e5b7`
- **KTV-15** Default workspace "VN Accounting" set for Accounts User role — commit `8426298`
- **KTV-18** "Tạo mới" (replaced awkward "Tạo nên"), "Các chỉ số tài chính" — commit `43b1d9a`
- **KTV-19** CCDC Writeoff list shows item name (ccdc_item_name fetch_from) — commit `43b1d9a`
- **KTV-20** Asset Type options translated (Existing/Composite Asset) — commit `3db3fd5`

## Deferred to v1.3
- PM-03 Asset Repair workspace routing (needs investigation: Property Setter vs route_options vs Custom Field)
- PM-11 Settings hash router (#asset-permissions-tab)
- PM-22 / KTV-04 Asset Handover submitted: prominent custom button "Xem biên bản"
- KTV-11 VN Accounting Settings permission boundary (Accounts User shouldn't see)
- PM-06 CCDC Item empty "Mã sản phẩm" column (cosmetic, non-blocking)
- PM-10 Sequential autoname for Handover/Stocktake/Writeoff (data migration needed)
