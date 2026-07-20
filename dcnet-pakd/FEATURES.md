# DCNET PAKD — Features

App: `dcnet_pakd` | Version: 0.2.0 | Stack: Frappe v16 + ERPNext v16 | Phụ thuộc: `dcnet_contract >= 0.2.0`, `hrms`

Phương Án Kinh Doanh — bảng tính hoa hồng bán hàng (thay thế Excel Mẫu 01/03 sau realignment v0.2.0 D4). Kiến trúc thin-layer: dcnet_contract sở hữu billing schedule & thu tiền, PAKD chỉ sở hữu chính sách hoa hồng + approval + hạch toán commission theo cash-basis.

## v0.2.0 changelog (2026-05-14 — realignment 8 decisions D1-D8)

- **Engine rewrite** — split output: `commission_line` (Sales Commission + License Fee, rule-template-driven) vs `beneficiaries` (Manager Services + Add Costs + Referral, PAKD-row-driven). 4-option canonical `rate_base`: `contract_revenue`, `contract_minus_ac_unit` (Mẫu 01 MS/SC), `contract_minus_ac_total` (Mẫu 03 MS), `ac_only`. Excel cell-by-cell match in `tests/test_golden_excel.py`.
- **Revision lookup** — `resolve_active_revision(revisions, period_start_date)` returns the latest Approved PAKD Revision row whose `effective_from` ≤ period_start. Engine + pivot view both use it; 5 unit tests cover the resolver.
- **Beneficiary JE** — `post_beneficiary_je(pakd, line)` writes a draft JE per beneficiary row: 2-leg when no recipient (DR `account_<kind>` / CR `counter_<kind>`); 3-leg when recipient + TNCN > 0 (DR / CR `account_external_payable` net / CR `account_pit_withholding` pit). API `post_beneficiary_now(beneficiary_line)` triggers from the pivot cell popover.
- **Pivot view rebuild** — FTTH branch removed (D4). Rows = SC + License + 1 row per Beneficiary Line. Column headers carry a 4px top border color-coded by the active revision (R0 green, R1 blue, ...). Click on a beneficiary cell opens a row-level popover with "Đăng JE ngay" → `post_beneficiary_now`.
- **HTML section "Hóa đơn & Thanh toán"** — Contract form + PAKD form both render an 8-column status table (Kỳ / Loại / Hạn / Số tiền / SI / Trạng thái / PE / Commission). Lazy-load gate at > 50 SI.
- **Schema drops** — `pakd_type "Monthly FTTH Rollup"` option, `PAKD Item.salary_coefficient`, `PAKD Item.revenue_actual`, `PAKD Item.contract_line_ref`, `Phuong An Kinh Doanh.external_commission_*` flat block (9 fields), `Phuong An Kinh Doanh.amended_from`, `post_external_commission_je` accounting function (replaced by `post_beneficiary_je`).
- `PAKD Commission Line.component` Select narrowed to Sales Commission + License Fee.

## A. Features Đã Thực Hiện

### A1. Data Model & Rule Engine

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A1.1 | DocType: Phuong An Kinh Doanh | Master DocType. Naming `PAKD-.YYYY.-.#####`. Không submittable, dùng workflow_state. Liên kết `contract_ref` → DCNET Contract, fetch_from khách hàng/NVKD/branch/service_type | Done | 2026-04 |
| A1.2 | Child: PAKD Item | Bảng hạng mục. Conditional fields theo `pakd_type` (Recurring / FTTH Rollup / One-off). Server computes revenue_contract, add_costs, manager_services, license_fee, sales_commission | Done | 2026-04 |
| A1.3 | Child: PAKD Commission Line | 1 row = (billing_period × component). State Pending → Posted → Cancelled. Granular tracking cho partial payment + prepay | Done | 2026-04 |
| A1.4 | DocType: PAKD Commission Rule Template | Cấu hình rate theo (service_type, branch, pakd_type). 4-tier resolution: contract override → branch+service → service → pakd_type default. Effective date range (valid_from/valid_to) | Done | 2026-04 |
| A1.5 | Child: PAKD Rule Component | Component-level rules: Manager Services / Add Costs / Phí GPVT / Lương KD. base_formula: unit_price / unit_price_minus_add_costs / add_costs_gross / revenue_actual | Done | 2026-04 |
| A1.6 | Single DocType: PAKD Settings | Cấu hình cutoff_day, default template, TK 6418/6425/3388, salary_component "Lương kinh doanh" | Done | 2026-04 |
| A1.7 | Rule engine pure function | `utils/engine.py::compute_pakd_line()` — pure server-side, tuân thủ rule "single source of truth for calculation" (không có JS formula engine) | Done | 2026-04 |
| A1.8 | Engine reads Contract at runtime | Đọc package_term_months, payment_mode, setup_fee, unit_price_total, contract_type, billing_schedule từ Contract qua `get_cached_doc` — không duplicate fetch_from | Done | 2026-04 |

### A2. 3 PAKD Types

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A2.1 | Recurring Telecom | Doanh thu = qty × unit_price (hàng tháng). Commission rate cố định từ Rule Template. Áp dụng cho dịch vụ viễn thông định kỳ | Done | 2026-04 |
| A2.2 | Monthly FTTH Rollup | Mẫu 02: doanh thu thực tế user-entered + `salary_coefficient` thủ công theo hợp đồng (không auto từ rules). Phản ánh thực tế FTTH DN: hệ số thương lượng theo deal | Done | 2026-04 |
| A2.3 | One-off Sale/Project | Bán lẻ thiết bị / dự án. Doanh thu = qty × unit_price 1 lần. Commission rate từ rules, setup fee excluded (month_index=0) | Done | 2026-04 |

### A3. Approval Workflow

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A3.1 | Workflow "PAKD Approval" | 7 states × 14 transitions. 4 routes: HCM-NV / HCM-BGĐ / HN-NV / HN-BGĐ. Seeded qua `_ensure_pakd_approval_workflow()` trong after_migrate | Done | 2026-04 |
| A3.2 | 6 custom roles | PAKD Sales Rep / Sales Director HCM / Sales Director HN / General Department / Branch Director HN / Board. Tạo qua `_ensure_custom_roles()` trong after_install | Done | 2026-04 |
| A3.3 | Client script — workflow UX | `phuong_an_kinh_doanh.js` — chuyển trạng thái, validate trước advance, back-link button | Done | 2026-04 |
| A3.4 | English-first workflow states | Tất cả states bằng English trong source (Draft, Pending Sales Director, Pending General Dept, Pending Branch Director, Pending Board, Approved, Rejected). Vietnamese qua vi.csv | Done | 2026-04 |
| A3.5 | Branch segregation | User Permission trên Branch enforce HCM/HN phân quyền | Done | 2026-04 |

### A4. Commission Posting — Cash Basis

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A4.1 | PE on_submit hook | `events.on_payment_entry_submit` — khi PE Receive submit → tìm SI references → tìm Contract → tìm PAKD Approved → post matching commission lines | Done | 2026-04 |
| A4.2 | PE on_cancel hook | `events.on_payment_entry_cancel` — tìm lines có payment_entry=PE.name và state=Posted → reverse (cancel AS/JE, flip line → Cancelled) | Done | 2026-04 |
| A4.3 | Contract on_cancel hook | `events.on_contract_cancel` — flip Pending lines → Cancelled. Posted lines không reverse (immutable) | Done | 2026-04 |
| A4.4 | Additional Salary (Lương KD) | `integrations/payroll.py` — 1 AS gộp tất cả periods paid per payment event. employee = sales_person, salary_component từ Settings | Done | 2026-04 |
| A4.5 | Journal Entry (MS/AC/GPVT) | `integrations/accounting.py` — Draft JE. DR TK chi phí (6418/6425) / CR TK đối ứng (3388). Kế toán review rồi submit | Done | 2026-04 |
| A4.6 | Cutoff logic payment_date | Nếu `payment_date.day <= cutoff_day_of_month` (mặc định 5) → `payroll_month = previous month`. Boundary inclusive | Done | 2026-04 |
| A4.7 | Prepay 12-tháng handling | 1 PE → 12 billing rows flip Paid → 12 lines Posted → 1 AS gom all | Done | 2026-04 |
| A4.8 | PE reversal — cancel Draft AS | Delete Draft AS (không dùng `.cancel()` vì AS is_submittable) | Done | 2026-04 |
| A4.9 | Integration mechanism (doc_events) | Không dùng publish_realtime. Cả dcnet_contract + dcnet_pakd đều đăng ký `doc_events["Payment Entry"]["on_submit"]`. Thứ tự đảm bảo qua required_apps dependency | Done | 2026-04 |

### A5. Chi Phí Ngoài

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A5.1 | Manager Services | Rule component chi phí MS. Post vào JE Nợ 6418 / Có 3388 | Done | 2026-04 |
| A5.2 | Add Costs | Add costs ngoài hợp đồng (đã tính trong unit_price hoặc user nhập riêng). Post JE | Done | 2026-04 |
| A5.3 | Phí GPVT (License Fee) | Phí giấy phép viễn thông 2.2%, chỉ áp cho Recurring Telecom. Post JE Nợ 6425 | Done | 2026-04 |

### A6. Contract Integration

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A6.1 | Liên kết Contract | `contract_ref` Link DCNET Contract, required. Fetch 12+ fields từ Contract (customer/sales_person/branch/service_type/...) | Done | 2026-04 |
| A6.2 | Unique constraint per Contract | (contract_ref, pakd_type) unique cho Recurring/One-off (1:1). Monthly FTTH Rollup cho phép nhiều PAKD (khác months) | Done | 2026-04 |
| A6.3 | Edge case guards | Validate contract_ref.status != Cancelled trước advance workflow. Throw error nếu no rule template matches | Done | 2026-04 |

### A7. Print Formats

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A7.1 | Mẫu 01 — PAKD Recurring Telecom | Jinja HTML, header VN, bảng hạng mục + tổng, 3 chữ ký | Done | 2026-04 |
| A7.2 | Mẫu 02 — PAKD FTTH Rollup | Jinja HTML, cột contract_line_ref + revenue_actual + salary_coefficient | Done | 2026-04 |
| A7.3 | Mẫu 03 — PAKD One-off | Jinja HTML cho bán lẻ/dự án | Done | 2026-04 |

### A8. Reports

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A8.1 | Commission Register | Script Report — danh sách hoa hồng đã post, filter theo NVKD/branch/tháng | Done | 2026-04 |
| A8.2 | Pending PAKD Aging | Script Report — PAKD đang pending approval, group theo workflow_state + số ngày chờ | Done | 2026-04 |
| A8.3 | Profitability by Service | Script Report — doanh thu / chi phí / lãi gộp theo service_type | Done | 2026-04 |

### A9. Workspace & Navigation

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A9.1 | Workspace "PAKD Module" | Module workspace với shortcuts + charts cơ bản | Done | 2026-04 |
| A9.2 | Workspace Sidebar `dcnet_pakd` | Sidebar navigation cho module PAKD (danh sách PAKD, Rule Template, Settings, 3 reports) | Done | 2026-04 |
| A9.3 | Slug conflict fix | Workspace đổi tên để tránh xung đột slug với DocType | Done | 2026-04 |

### A10. Bản Địa Hóa

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A10.1 | English-first i18n | Tất cả labels/options/workflow states/channel/components/error messages bằng English trong source | Done | 2026-04 |
| A10.2 | Vietnamese translations | 126 entries trong `translations/vi.csv` (di chuyển đúng path `dcnet_pakd/translations/` để Frappe auto-load) | Done | 2026-04 |
| A10.3 | English translations | 98 entries `dcnet_pakd/translations/en.csv` (source-of-truth keys) | Done | 2026-04 |
| A10.4 | Print format VN headers | Fix headers in print format Jinja về Vietnamese đúng chuẩn | Done | 2026-04 |

### A11. Settings & Install

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A11.1 | after_install | Tạo roles + singleton Settings + seed default accounts + seed 3 Rule Templates | Done | 2026-04 |
| A11.2 | after_migrate | Ensure Settings singleton + re-seed rule templates + ensure workflow | Done | 2026-04 |
| A11.3 | Default accounts seeding | 6418/6425/3388, salary component "Lương kinh doanh" | Done | 2026-04 |
| A11.4 | 3 Rule Template seeds | Defaults per pakd_type (Recurring / FTTH Rollup / One-off) | Done | 2026-04 |
| A11.5 | Edge case validation guards | Hardening validate() cho các edge case: contract cancelled, no rule match, duplicate PAKD | Done | 2026-04 |

### A12. Tests

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A12.1 | Engine golden tests | `tests/test_engine.py` — replay formulas từ Excel Mẫu 01/02/03 | Done | 2026-04 |
| A12.2 | Integration tests B & C | `tests/test_chains_b_c.py` — One-off VTTB chain + FTTH Rollup chain | Done | 2026-04 |
| A12.3 | Console bug fixes | 2 integration bugs phát hiện qua console testing đã fix | Done | 2026-04 |

---

## B. Features Đang Phát Triển

(Trống — v0.1.0 đã code-complete, chưa push GitHub)

---

## C. Features Sẽ Thực Hiện

### C1. Mở Rộng Commission & Chính Sách

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C1.1 | Co-sales (chia hoa hồng) | Nhiều NVKD trên cùng 1 Contract/PAKD, chia % commission | Medium | Spec v3 §12 khóa "1 NVKD per contract" cho v1 — mở lại ở v2 |
| C1.2 | Clawback automation | Khi Contract chấm dứt sớm → auto-generate negative AS/JE hoàn commission đã post | High | Hiện tại posted lines immutable, reverse thủ công |
| C1.3 | Rule engine UI builder | Admin UI để cấu hình rule phức tạp (bậc thang, combo, limit) thay vì chỉ flat rate | Medium | Cần design UX Rule Template mở rộng |
| C1.4 | TNCN tax auto-calc | Tính thuế TNCN lũy tiến cho Lương KD khi AS post, hiển thị net/gross | Medium | Cần tích hợp HRMS tax slab |
| C1.5 | Tiered commission | Commission rate thay đổi theo doanh thu tích luỹ NVKD trong tháng/quý | Medium | |

### C2. Tự Động Hoá & UX

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C2.1 | "Tạo PAKD" button trên Contract | Khi Contract Active → button pre-fill contract_ref, tạo PAKD draft | High | Spec v3 §12.16 |
| C2.2 | Commission dashboard (self-service) | NVKD xem commission của mình: pending/posted, theo tháng | High | Frappe Page filter by sales_person |
| C2.3 | Mobile app cho sales | Read-only list PAKD + status + notification | Low | React Native — chưa ưu tiên |
| C2.4 | Bulk approval (Board) | BGĐ duyệt nhiều PAKD một lần | Low | |
| C2.5 | Email notification | Email NVKD khi PAKD approved / commission posted / rejected | Medium | |

### C3. Báo Cáo & Phân Tích

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C3.1 | Commission forecast | Dự báo commission sẽ post trong tháng dựa trên billing_schedule Invoiced | Medium | |
| C3.2 | Top performers leaderboard | Ranking NVKD theo commission YTD / quý / tháng | Low | |
| C3.3 | Cost-to-revenue trend | Trend chi phí ngoài / doanh thu theo service_type qua thời gian | Medium | |
| C3.4 | P&L by PAKD | Báo cáo lãi gộp từng PAKD: doanh thu vs tất cả chi phí (MS/AC/GPVT/Lương KD) | High | |

### C4. Tích Hợp

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C4.1 | HRMS Payroll Entry integration | Commission AS tự include vào Payroll Entry kỳ đúng | High | Cần verify payroll_month logic end-to-end |
| C4.2 | Historical Excel PAKD import | Tool import Mẫu 01/02/03 cũ vào PAKD DocType | Medium | Cho migration Misa → ERPNext |
| C4.3 | Multi-currency (USD contracts) | Hỗ trợ Contract USD → commission quy đổi VND theo tỷ giá payment_date | Low | v1 VND only |
| C4.4 | vn_banking integration | PE từ bank matching auto-trigger commission posting (đã có sẵn qua PE hook) | — | Đã hoạt động qua PE on_submit |

### C5. Vận Hành

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C5.1 | Push dcnet-cloud/dcnet-pakd | Tạo repo + push code, setup CI gitflow guard | High | Hiện chỉ ở local + goldrag1 |
| C5.2 | Dual remote (dcnet + personal) | Setup cả hai remote theo mô hình các app khác | High | |
| C5.3 | Deployment on dcnet.localhost | Test install-app + migrate + seed workflow + rule templates | High | |
| C5.4 | VPS deploy | Deploy lên VPS DCNET (khi có) | Medium | DCNET chưa có VPS production |

---

## Legend

| Status | Nghĩa |
|--------|-------|
| Done | Đã code-complete, trên branch ổn định |
| In Progress | Đang fix/build trên feature branch |
| Planned | Có spec hoặc đã thảo luận, chưa bắt đầu code |
| — (Priority) | High = cần cho go-live, Medium = cần trong 3 tháng, Low = nice-to-have |
