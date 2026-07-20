# VN Accounting — Features

App: `vn_accounting` | Stack: Frappe v16 + ERPNext v16 | Chuẩn: TT99/2025

## A. Features Đã Thực Hiện

### A1. Hệ Thống Tài Khoản (COA)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A1.1 | COA Doanh nghiệp lớn | 185 tài khoản theo TT99/2025 (`vn_large_enterprise.json`) | Done | 2026-04 |
| A1.2 | COA Doanh nghiệp nhỏ | 141 tài khoản theo TT99/2025 (`vn_small_enterprise.json`) | Done | 2026-04 |
| A1.3 | Đăng ký COA vào ERPNext | Override `get_charts_for_country` — hiện VN templates khi chọn country=Vietnam | Done | 2026-04 |
| A1.4 | Auto-detect large/small | `set_vn_defaults()` tự nhận diện template khi tạo Company | Done | 2026-04 |
| A1.5 | Thiết lập mặc định công ty | Gán TK mặc định (cash 111, bank 112, AR 131, AP 331, revenue 511, COGS 632...) vào Company fields | Done | 2026-04 |

### A2. Báo Cáo Kế Toán

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A2.1 | Bảng cân đối số phát sinh | Trial Balance Sheet — Opening/period/closing debit/credit per account | Done | 2026-04 |
| A2.2 | Sổ chi tiết tài khoản | Account Detail Ledger — GL per account with running balance | Done | 2026-04 |
| A2.3 | Sổ quỹ tiền mặt | Cash Book — TK 111% (thu + chi) | Done | 2026-04 |
| A2.4 | Sổ tiền gửi ngân hàng | Bank Account Book — TK 112% | Done | 2026-04 |
| A2.5 | Thu tiền mặt | Cash Receipts — debit transactions TK 111% | Done | 2026-04 |
| A2.6 | Chi tiền mặt | Cash Payments — credit transactions TK 111% | Done | 2026-04 |
| A2.7 | Thu ngân hàng | Bank Receipts — debit transactions TK 112% | Done | 2026-04 |
| A2.8 | Chi ngân hàng | Bank Payments — credit transactions TK 112% | Done | 2026-04 |
| A2.9 | Chuyển khoản nội bộ | Internal Transfer — vouchers with both debit & credit in cash/bank | Done | 2026-04 |

### A3. Workspace & Navigation

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A3.1 | Workspace "Kế Toán VN" | 5 KPI cards + 4 charts + 20+ shortcuts | Done | 2026-04 |
| A3.2 | Sidebar 40+ items | 7 sections: Tổng quan, Quỹ tiền mặt, Ngân hàng, Kế toán chung, Báo cáo, Tài sản & Nợ, Kho & Giá vốn | Done | 2026-04 |
| A3.3 | Sidebar 3-tier persistence | localStorage → boot defaults → Frappe default. Custom sidebar không bị mất khi F5 | Done | 2026-04 |
| A3.4 | Sidebar route_options fix | Monkey-patch Frappe v16 sidebar — DocType links giữ filter khi navigate | Done | 2026-04 |
| A3.5 | Sidebar active highlight scoring | Scoring algorithm cho multiple items cùng DocType (VD: 4 items → Journal Entry) | Done | 2026-04 |
| A3.6 | Desktop Icon | Đăng ký icon trên Desk home, link_type=Workspace Sidebar | Done | 2026-04 |

### A4. Dashboard

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A4.1 | 5 Number Cards | Tồn Quỹ, Tổng Doanh Thu, Tổng Chi Phí, Công Nợ Phải Thu, Công Nợ Phải Trả | Done | 2026-04 |
| A4.2 | 4 Dashboard Charts | Doanh Thu vs Chi Phí (monthly), Biến Động Tiền, Công Nợ Phải Thu/Trả (top party) | Done | 2026-04 |
| A4.3 | Dashboard v2 — Frappe Page | Custom page: 5 KPIs + 8 charts + granularity filter (Tháng/Quý/Năm/Tuần) | Done | 2026-04-15 |
| A4.4 | Y-axis abbreviated | Rút gọn số trên trục Y (1.000.000 → 1M) | Done | 2026-04-15 |
| A4.5 | Rolling window charts | Doanh Thu & Chi Phí, Dòng Tiền luôn hiện 12 tháng rolling | Done | 2026-04-15 |
| A4.6 | Dòng Tiền tách datasets | 2 datasets riêng: Tiền mặt (TK 111) + Ngân hàng (TK 112) | Done | 2026-04-15 |

### A5. Ngân Quỹ (Treasury) — Tiền Gửi Có Kỳ Hạn

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A5.1 | DocType: Term Deposit | Quản lý sổ tiền gửi. Submittable. Status: Draft/Active/Matured/Settled/Early Settled | Done | 2026-04-15 |
| A5.2 | 5 kiểu trả lãi | End of Term, Monthly, Quarterly, Prepaid, Compound | Done | 2026-04-15 |
| A5.3 | Tự động sinh lịch trả lãi | `build_interest_schedule()` — pure function, actual/365 | Done | 2026-04-15 |
| A5.4 | JE gửi tiền on_submit | Nợ 1281 / Có 112x. Prepaid: 3-leg JE (Nợ 1281, Có 112x, Có 515) | Done | 2026-04-15 |
| A5.5 | Tất toán (maturity + early) | Nút "Tất toán" / "Tất toán trước hạn" — tạo draft JE | Done | 2026-04-15 |
| A5.6 | Tái tục | Nút "Tái tục" khi Matured — tạo Term Deposit mới (gốc + lãi nếu Compound/EoT) | Done | 2026-04-15 |
| A5.7 | Lãi kép (Compound) | Lãi nhập gốc mỗi tháng, principal_at_start tăng dần | Done | 2026-04-15 |

### A6. Ngân Quỹ (Treasury) — Khoản Vay Ngân Hàng

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A6.1 | DocType: Bank Loan | Quản lý khoản vay. Submittable. Status: Draft/Active/Matured/Settled | Done | 2026-04-15 |
| A6.2 | 2 kiểu trả nợ | Interest Only (lãi hàng kỳ + gốc cuối kỳ), EMI (trả đều gốc+lãi) | Done | 2026-04-15 |
| A6.3 | Tự động sinh lịch trả nợ | `build_repayment_schedule()` — pure function | Done | 2026-04-15 |
| A6.4 | JE giải ngân on_submit | Nợ 112x / Có 3411 | Done | 2026-04-15 |
| A6.5 | Tất toán trước hạn | Nút "Tất toán" — gốc còn lại + lãi pro-rata | Done | 2026-04-15 |
| A6.6 | Cập nhật lãi suất (thả nổi) | Nút "Cập nhật lãi suất" — regenerate lịch từ kỳ chưa Booked | Done | 2026-04-15 |

### A7. Ngân Quỹ — Tự Động Hóa & Cài Đặt

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A7.1 | Scheduled job (daily) | Tạo draft JE cho lãi/nợ đến hạn, cập nhật maturity status | Done | 2026-04-15 |
| A7.2 | Cảnh báo đáo hạn | Notification Log cho Accounts Manager, cấu hình X ngày trước | Done | 2026-04-15 |
| A7.3 | VN Accounting Settings | Single DocType: TK mặc định (1281, 515, 3411, 635), alert days | Done | 2026-04-15 |
| A7.4 | Default account inheritance | Form tự lấy TK từ Settings, cho phép override per record | Done | 2026-04-15 |

### A8. Bản Địa Hóa

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A8.1 | English-first i18n | Tất cả labels/options/descriptions bằng English trong source | Done | 2026-04-15 |
| A8.2 | Vietnamese translations | 95 entries trong `translations/vi.csv` | Done | 2026-04-15 |
| A8.3 | Monkey-patch Frappe sidebar | JS bundles load sau desk.bundle.js, patch prototype trực tiếp | Done | 2026-04 |

### A9. Tests

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A9.1 | Interest calculator tests | 7 test cases: 5 kiểu lãi + tổng + early settlement | Done | 2026-04-15 |
| A9.2 | Repayment calculator tests | 5 test cases: Interest Only + EMI (monthly/quarterly) + sum check | Done | 2026-04-15 |
| A9.3 | COA registry tests | Template loading, account structure | Done | 2026-04 |
| A9.4 | Company defaults tests | Large/small detection, account mapping | Done | 2026-04 |
| A9.5 | Report utils tests | Account prefix extraction, GL query utilities | Done | 2026-04 |

---

### A10. Treasury Critical Fixes (v1.1.0)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A10.1 | Bút toán dự thu/dự chi lãi | VAS: Nợ 1388 / Có 515 (tiền gửi), Nợ 635 / Có 335 (vay). Nút trên form + Settings TK mới | Done | 2026-04-16 |
| A10.2 | Schedule rebuild protection | `_build_schedule()` skip khi docstatus=1 — bảo vệ rows Booked | Done | 2026-04-16 |
| A10.3 | EMI actual/365 | EMI tính lãi theo ngày thực tế/365, không dùng rate/12 | Done | 2026-04-16 |
| A10.4 | Company validation | Validate bank_account cùng company trước khi tạo JE | Done | 2026-04-16 |
| A10.5 | JE link-back | Field `deposit_je`/`disbursement_je` trên parent, populate on_submit | Done | 2026-04-16 |
| A10.6 | on_cancel handler | Cancel/delete linked JE khi cancel Term Deposit / Bank Loan | Done | 2026-04-16 |
| A10.7 | Prepaid actual/365 | Lãi trả trước dùng actual_days/365, không dùng term_months/12 | Done | 2026-04-16 |
| A10.8 | JE → outstanding sync | Submit JE repayment → update row status Booked + outstanding_amount | Done | 2026-04-16 |
| A10.9 | Required account fields | deposit_account, loan_account, interest accounts → reqd=1 | Done | 2026-04-16 |
| A10.10 | JE cost_center | Tất cả JE rows kèm cost_center mặc định từ Company | Done | 2026-04-16 |
| A10.11 | Alert text i18n | Alert subject/message wrapped `_()`, vi.csv entries | Done | 2026-04-16 |

### A11. Dự Báo Dòng Tiền (Cash Flow Forecast)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A11.1 | Hook-based provider system | Cơ chế plugin: app ngoài đăng ký nguồn dữ liệu forecast qua `cash_flow_forecast_providers` hook. Error isolation — 1 provider lỗi không ảnh hưởng provider khác | Done | 2026-04-20 |
| A11.2 | Aggregator + schema validation | Thu thập entries từ tất cả providers, validate 7 required fields (date, amount, direction, confidence, category, source_doctype, source_name), reject invalid + log | Done | 2026-04-20 |
| A11.3 | 5 ERPNext pipeline providers | Quotation (possible), SO (probable), PO (probable), SI unpaid (committed/overdue), PI unpaid (committed/overdue). Lifecycle-aware — no double-counting | Done | 2026-04-20 |
| A11.4 | Treasury providers (2) | Lãi tiền gửi + đáo hạn gốc (Term Deposit), trả nợ gốc + lãi (Bank Loan). Đọc từ interest/repayment schedule rows | Done | 2026-04-20 |
| A11.5 | Payroll provider | Dự báo lương từ HRMS Payroll Entry (probable) hoặc GL TK 334 median 6 tháng (possible). Auto-detect HRMS installed | Done | 2026-04-20 |
| A11.6 | Insurance provider | Dự báo BHXH/BHYT/BHTN từ GL TK 3383+3384+3386, trung vị 6 tháng, ngày 20 hàng tháng | Done | 2026-04-20 |
| A11.7 | Tax provider (3 loại thuế) | GTGT: GL TK 33311 median 3 tháng, nộp ngày 20 tháng sau. TNDN: GL TK 3334, nộp theo quý. TNCN: GL TK 3335, nộp tháng sau | Done | 2026-04-20 |
| A11.8 | Historical OpEx projection | GL TK 6xx (trừ payroll) 12 tháng, recurring ≥8/12, same-month-last-year fallback median, cap 2× median | Done | 2026-04-20 |
| A11.9 | Revenue projection | GL TK 5xx 12 tháng, same-month-last-year, cap 2× median | Done | 2026-04-20 |
| A11.10 | Payment delay factor | Per-customer median(PE.posting_date − SI.due_date) 12 tháng. Điều chỉnh expected_date cho SI inflow. In-memory cache per request | Done | 2026-04-20 |
| A11.11 | Custom Frappe Page | Trang forecast: Company/Period/GroupBy filters + 4 confidence toggles + per-source toggles + 4 summary cards + bar+line Chart.js + drill-down table + CSV export | Done | 2026-04-20 |
| A11.12 | Dashboard v2 chart integration | `get_forecast_chart()` endpoint — committed entries only, grouped by month, hiển thị trên Dashboard v2 | Done | 2026-04-20 |
| A11.13 | Minimum cash threshold | Ngưỡng tiền mặt tối thiểu từ VN Accounting Settings + cảnh báo 3 cấp (đỏ < 0 / vàng < threshold / bình thường) | Done | 2026-04-20 |
| A11.14 | Rolling balance calculation | Số dư cuộn kỳ-sang-kỳ: Opening = GL TK 111+112+113, Closing = Opening + Inflow − Outflow | Done | 2026-04-20 |
| A11.15 | Bilingual UX | Tooltips song ngữ EN+VI, methodology panel, Y-axis abbreviated (tỷ/tr/ng) | Done | 2026-04-20 |
| A11.16 | Sidebar integration | Mục "Dự báo dòng tiền" trong sidebar section Tổng quan | Done | 2026-04-20 |
| A11.17 | Translations | ~25 entries vi.csv cho Cash Flow Forecast | Done | 2026-04-20 |
| A11.18 | Aggregator unit tests | Valid/invalid entry validation, negative/zero/missing-field rejection, date format, error isolation | Done | 2026-04-20 |

---

## B. Features Đang Phát Triển

(Trống)

---

## C. Features Sẽ Thực Hiện

### C0. Kiểm Kê Quỹ Tiền Mặt (Cash Count)

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C0.1 | DocType: Cash Count | Regular DocType (không submittable), status workflow Draft→Counted→Approved→Closed/Resolved | High | Spec: docs/superpowers/specs/2026-04-16-cash-count-design.md |
| C0.2 | Child: Cash Count Denomination | Bảng kê mệnh giá (9 loại VND), optional toggle | High | |
| C0.3 | Tính số dư sổ sách | Auto-fetch GL balance tại count_date, reuse report_utils | High | |
| C0.4 | Bút toán chênh lệch bước 1 | Button tạo Draft JE: Nợ 1381/Có 111 (thiếu) hoặc Nợ 111/Có 3381 (thừa) | High | VAS 2 bước |
| C0.5 | Default account + save | Auto-fill TK từ Settings, tick "Lưu mặc định" ghi ngược Settings | High | |
| C0.6 | Print Format Mẫu 08a | Jinja HTML, conditional mệnh giá, 3 chữ ký, Times New Roman | High | |
| C0.7 | Sidebar integration | Thêm "Kiểm kê quỹ" vào section Quỹ tiền mặt | High | |
| C0.8 | Translations | ~20 entries vi.csv cho Cash Count | High | |

### C1. Ngân Quỹ — Phase 2

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C1.1 | Multi-currency deposits/loans | Hỗ trợ USD/EUR deposits, tự quy đổi VND theo tỷ giá | Medium | Cần exchange_rate field + multi-currency JE |
| C1.2 | Grace period | Gia hạn X ngày trước khi tính lãi quá hạn | Low | |
| C1.3 | Tài sản đảm bảo (Collateral) | Liên kết Asset/Property làm tài sản thế chấp | Low | |
| C1.4 | Trả đều gốc (Equal Principal) | Kiểu trả nợ thứ 3: gốc đều + lãi giảm dần | Medium | Phổ biến ở VN |
| C1.5 | Phân loại ngắn/dài hạn | Tự phân loại TK 128x (ngắn hạn) vs 228x (dài hạn) theo maturity | Medium | Ảnh hưởng BCTC |
| C1.6 | So sánh lãi suất khi tái tục | Gợi ý lãi suất thị trường khi renew | Low | |
| C1.7 | Dashboard integration | Treasury summary trên Dashboard v2 (tổng tiền gửi, tổng dư nợ) | Medium | |
| C1.8 | Phạt lãi quá hạn | Tự tính penalty interest khi repayment quá due_date | Low | |

### C2. Báo Cáo Bổ Sung

> **Cập nhật 2026-05-11:** Đổi tên C2.1 theo TT99/2025 ("Báo cáo tình hình tài chính", không còn "Bảng cân đối kế toán"). C2.1–C2.6 nằm trong phase "Giá thành + Tổng hợp + BCTC" (xem C7–C9 dưới đây). Spec: `docs/specs/2026-05-11-giathanh-tonghop-bctc.md`. BUSINESS_LOGIC mục 11-14.

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C2.1 | **Báo cáo tình hình tài chính (B01-DN)** | BCTC theo mẫu B01-DN TT99/2025 — đổi tên từ "Bảng cân đối kế toán" | High | BL §14, mapping TK ↔ mã chỉ tiêu cấu hình qua BCTC Mapping DocType |
| C2.2 | Báo cáo kết quả kinh doanh (B02-DN) | BCTC theo mẫu B02-DN TT99/2025 | High | BL §14 |
| C2.3 | Báo cáo lưu chuyển tiền tệ (B03-DN) | BCTC theo mẫu B03-DN — phương pháp gián tiếp (phase 1) | High | BL §14 |
| C2.4 | Thuyết minh BCTC (B09-DN) | Mẫu B09-DN TT99/2025 — khung + số liệu sẵn, kế toán điền văn xuôi | Medium | BL §14 |
| C2.5 | Sổ nhật ký chung (S03a-DN) | General Journal — tất cả bút toán theo thời gian, mẫu S03a-DN TT99/2025 | High | BL §13 |
| C2.6 | Sổ cái tài khoản (S03b-DN) | General Ledger per account — mẫu S03b-DN TT99/2025 (khác A2.2 Sổ chi tiết về format) | High | BL §13 |
| C2.7 | Bảng kê hoá đơn GTGT | VAT invoice register — đầu vào + đầu ra | High | Cần cho kê khai thuế (thuộc C3) |

### C3. Thuế

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C3.1 | Tờ khai thuế GTGT | Mẫu 01/GTGT — auto-fill từ GL data | High | |
| C3.2 | Tờ khai thuế TNDN | Mẫu 03/TNDN tạm tính + quyết toán | Medium | |
| C3.3 | Tờ khai thuế TNCN | Mẫu 05/KK-TNCN — tổng hợp từ HRMS payroll | Medium | Cần HRMS integration |
| C3.4 | Hoá đơn điện tử (e-Invoice) | Kết nối VNPT/Viettel/BKAV e-invoice provider | High | API integration |

### C4. Tài Sản Cố Định

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C4.1 | Bảng tính khấu hao TSCĐ | Khấu hao TT99/2025 — Đường thẳng, Số dư giảm dần; Property Setter ẩn 3 phương pháp khác | Done | asset-polishing v1.0 |
| C4.2 | Sổ TSCĐ | Sổ theo dõi TSCĐ theo mẫu S21-DN + S22-DN (TSCĐ & CCDC by location) | Done | asset-polishing v1.0 |
| C4.3 | CCDC phân bổ | CCDC Item lifecycle TK 242/153, Allocation Schedule N kỳ, monthly scheduler | Done | asset-polishing v1.0 |
| C4.4 | Bàn giao TSCĐ/CCDC | Asset Handover with scope, S22-DN print, Asset Movement, threshold validation | Done | asset-polishing v1.0 |
| C4.5 | Kiểm kê tài sản | Asset Stocktake with Tải danh sách, approve JE 1381/211, status update | Done | asset-polishing v1.0 |
| C4.6 | Sửa chữa TSCĐ | Asset Repair classification (Chi phí/Vốn hóa/Nâng cấp), JE routing TK 241 | Done | asset-polishing v1.0 |

### C5. Kho & Giá Vốn

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C5.1 | Phương pháp bình quân gia quyền | Tính giá vốn xuất kho theo FIFO/Weighted Avg chuẩn VN | Medium | ERPNext có, cần verify mapping TK |
| C5.2 | Sổ chi tiết vật tư | Material ledger theo mẫu VN | Low | |

### C6. Tích Hợp

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C6.1 | Import số dư đầu kỳ từ Misa | Tool chuyển đổi: đọc file Misa → tạo Opening Entry | High | Cho dự án migration DCNET |
| C6.2 | vn_banking integration | Đối soát sao kê ngân hàng → auto-match SI/PI → auto-create PE | High | App riêng, đã có spec |
| C6.3 | HRMS payroll VN | Bảng lương theo mẫu VN, thuế TNCN, BHXH/BHYT/BHTN | Medium | Extends HRMS app |

### C7. Phân Bổ Chi Phí Mua Hàng (LCV)

Áp dụng cho mọi DN có hoạt động mua hàng (thương mại + sản xuất + dịch vụ có vật tư đầu vào). BL §11. Spec: `docs/specs/2026-05-11-giathanh-tonghop-bctc.md`.

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| C7.1 | LCV Allocation Settings | Single DocType: TK mặc định cho 12 loại phụ phí (vận chuyển, bốc xếp, bảo hiểm, lưu kho, hoa hồng, thuế NK, TTĐB NK, VAT NK khấu trừ / không khấu trừ, phí hải quan, phí lưu cont, phí đại lý). Mỗi loại có TK gợi ý theo TT99/2025 + sửa được | Done | 2026-05-11 |
| C7.2 | LCV chi phí mua hàng trong nước | ERPNext LCV pattern với cấu hình mặc định từ Settings. 4 tiêu thức phân bổ: Amount / Qty / Weight / Volume | Done | 2026-05-11 |
| C7.3 | LCV nhập khẩu | LCV mở rộng: thuế NK (3333) + TTĐB NK (3332) + VAT NK split khấu trừ/không khấu trừ + phí hải quan / lưu cont / đại lý. Field "Tỷ lệ VAT khấu trừ" 0-100% | Done | 2026-05-11 |
| C7.4 | Danh sách chi phí chờ phân bổ | Report: phụ phí đã hạch toán 1388/331 nhưng chưa link tới Phiếu nhập mua nào | Done | 2026-05-11 |
| C7.5 | Sidebar item "Phân bổ chi phí mua hàng" | Section Giá thành — link tạo LCV mới + list LCV | Done | 2026-05-11 |
| C7.6 | Translations | ~25 entries vi.csv cho LCV expense types | Done | 2026-05-11 |

### C8. Giá Thành Sản Xuất

Chỉ áp dụng cho DN có sản xuất. BL §12. DN dùng mẫu COA nhỏ tự động ẩn (không có 621/622/627).

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| C8.1 | Manufacturing Costing Settings | Single DocType: TK 621/622/627/154/155 (mặc định, sửa được). Cấu hình đối tượng tập hợp chi phí (Sản phẩm / Work Order / Công trình / Hợp đồng / Lô gia công). Tiêu thức phân bổ 627 mặc định | Done | 2026-05-11 |
| C8.2 | Báo cáo Tập hợp chi phí sản xuất kỳ | Report: 621/622/627 phát sinh trong kỳ, group theo đối tượng cấu hình | Done | 2026-05-11 |
| C8.3 | Đánh giá sản phẩm dở dang | DocType "Work In Progress Valuation": chọn phương pháp (NVL chính / sản lượng tương đương / 50% chi phí chế biến) + nhập số liệu theo đối tượng | Done | 2026-05-11 |
| C8.4 | Wizard Tính giá thành | Page wizard: chọn kỳ → hệ thống tập hợp + phân bổ 627 + áp DDCK → ra bảng giá thành đơn vị + tổng giá trị nhập kho | Done | 2026-05-11 |
| C8.5 | JE Kết chuyển 621/622/627 → 154 + 154 → 155 | 2 JE nháp sinh từ wizard. Kế toán trưởng duyệt + ghi sổ | Done | 2026-05-11 |
| C8.6 | Auto-hide cho mẫu COA nhỏ | Detect mẫu DN nhỏ → ẩn 621/622/627, dùng 154 trực tiếp | Done | 2026-05-11 |
| C8.7 | Sidebar items Giá thành | "Phân bổ chi phí mua hàng (LCV)", "Tập hợp chi phí SX kỳ", "Bảng tính giá thành", "Kết chuyển giá thành" | Done | 2026-05-11 |
| C8.8 | Translations | ~30 entries vi.csv | Done | 2026-05-11 |

### C9. Kết Chuyển Cuối Kỳ & Khóa Sổ

Áp dụng cho mọi DN. BL §13.

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| C9.1 | Period Closing Settings | Mở rộng VN Accounting Settings: TK 911 + 4212 + 4211 + danh sách TK doanh thu/chi phí kết chuyển (multi-select, sửa được) | Done | 2026-05-11 |
| C9.2 | Wizard Kết chuyển cuối kỳ | Page wizard: chọn kỳ → hiện bảng đầy đủ TK + số dư + TK đích + nút "Sửa" từng dòng. Preview 3 JE (doanh thu→911, chi phí→911, 911→421) trước khi sinh | Done | 2026-05-11 |
| C9.3 | Khóa sổ kỳ kế toán | Period Closing Voucher: kiểm tra cân đối + tất cả JE đã ghi sổ → chốt kỳ | Done | 2026-05-11 |
| C9.4 | Lock kỳ đã đóng | Sau Period Closing, chứng từ trong kỳ không sửa/xóa được. Quản trị viên override với audit log | Done | 2026-05-11 |
| C9.5 | Sidebar items Tổng hợp | "Sổ nhật ký chung (S03a-DN)", "Sổ cái (S03b-DN)", "Kết chuyển cuối kỳ", "Khóa sổ kỳ" | Done | 2026-05-11 |
| C9.6 | Translations | ~20 entries vi.csv | Done | 2026-05-11 |

### C10. BCTC Foundation & 4 Báo Cáo

BL §14. Mã mẫu B01–B09-DN theo TT99/2025 Phụ lục IV.

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| C10.1 | BCTC Mapping DocType | Per-Company DocType chứa mapping TK ↔ mã chỉ tiêu cho B01/B02/B03. Child tables: B01 Lines, B02 Lines, B03 Lines. Mỗi dòng: mã + tên + công thức TK (sửa được) + loại số liệu (số dư N/C cuối kỳ, phát sinh N/C kỳ, công thức từ mã khác) + wildcard `511%` | Done | 2026-05-11 |
| C10.2 | Seed mapping defaults TT99/2025 | Fixture đầy đủ B01 (~50 mã), B02 (~18 mã), B03 (~30 mã) theo Phụ lục IV. Auto-clone khi tạo Company mới (Vietnam) | Done | 2026-05-11 |
| C10.3 | Nút "Khôi phục mặc định TT99/2025" | Per-row + per-report rollback về template | Done | 2026-05-11 |
| C10.4 | B01-DN: Báo cáo tình hình tài chính | Report chạy mapping → bảng đầy đủ + 2 cột (cuối kỳ / đầu năm). Tooltip công thức trên mỗi dòng. Click drill xuống chứng từ gốc | Done | 2026-05-11 |
| C10.5 | B02-DN: BC KQHĐKD | 18 mã chỉ tiêu, 2 cột (kỳ này / kỳ trước) | Done | 2026-05-11 |
| C10.6 | B03-DN: BC LCTT gián tiếp | 3 mục lớn (kinh doanh / đầu tư / tài chính). Đối chiếu cuối kỳ với B01 mã 110 | Done | 2026-05-11 |
| C10.7 | B09-DN: Thuyết minh | Sinh khung Word/Excel + số liệu sẵn từ B01-B03. Kế toán điền văn xuôi | Done | 2026-05-11 |
| C10.8 | Xuất Excel layout TT99/2025 | File Excel đúng format thông tư (font, cột, ký hiệu, ô trống) — sẵn sàng nộp | Done | 2026-05-11 |
| C10.9 | Phương trình check Tài sản = Nguồn vốn (B01) | Cảnh báo khi mã 270 ≠ mã 440 | Done | 2026-05-11 |
| C10.10 | Sidebar section Báo cáo tài chính | 4 items: "Báo cáo tình hình tài chính (B01-DN)", "BC KQHĐKD (B02-DN)", "BC LCTT (B03-DN)", "Thuyết minh BCTC (B09-DN)". Thêm "Cấu hình mapping BCTC" | Done | 2026-05-11 |
| C10.11 | Bộ KLT (DN không liên tục) | B01/B02/B03/B09-DNKLT — toggle theo Company status. **Phase 2 — chưa làm phase này** | Planned | — |
| C10.12 | Translations | ~40 entries vi.csv cho BCTC | Done | 2026-05-11 |

---

## Legend

| Status | Nghĩa |
|--------|-------|
| Done | Đã merge vào main hoặc đang trên branch ổn định |
| In Progress | Đang fix/build trên feature branch |
| Planned | Có spec hoặc đã thảo luận, chưa bắt đầu code |
| — (Priority) | High = cần cho go-live, Medium = cần trong 3 tháng, Low = nice-to-have |
