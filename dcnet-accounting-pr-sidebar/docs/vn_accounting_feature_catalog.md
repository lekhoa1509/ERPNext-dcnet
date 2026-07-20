# vn_accounting — Danh mục chức năng (Feature Catalog)

Generated từ sidebar `workspace_sidebar/vn_accounting.json` + actual controller / report / page code.

Ký hiệu cột "Loại":
- **C** = Custom (ship trong app vn_accounting)
- **S** = Stock ERPNext / Frappe
- **X** = Cross-app (vn_banking, dcnet_contract, dcnet_pakd, …)

Ký hiệu cột "Kiểu":
- DocType / Report (Script) / Page / URL

---

## Tổng quan (Dashboard)

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Tổng quan | Page | C | `vn-accounting-dashboard` | Dashboard chính của vn_accounting — 5 KPI thẻ (LN gross, doanh thu, chi phí, công nợ, dòng tiền) + 8 biểu đồ chia theo Tháng/Quý/Năm/Tuần. Filter granularity. Render bằng frappe-charts. (Ref: `page/vn_accounting_dashboard/`) |

---

## Tiền mặt

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Phiếu thu | Report | C | `Cash Receipts` | Báo cáo Script: list các bút toán Dr 111 (Cash) — wrap quanh `cash_book` với filter `direction=Receipt`. Lấy từ `tabGL Entry` theo `account_type='Cash'`. Filters: company, from/to, account, branch. |
| Phiếu chi | Report | C | `Cash Payments` | Tương tự Phiếu thu nhưng Cr 111. Filter `direction=Payment`. |
| Kiểm kê quỹ | DocType | C | `Cash Count` | Đối chiếu tồn quỹ thực tế vs sổ. Controller `CashCount.validate()` tự tính book_balance (qua `get_opening_balance` + GL Entry), tổng denomination mệnh giá, chênh lệch, và auto-fill TK chênh lệch. Status flow: Draft → Pending Resolution → Resolved (lock after JE chênh lệch). Child table `Cash Count Denomination` để liệt kê mệnh giá. |
| Sổ quỹ tiền mặt | Report | C | `Cash Book` | Sổ chi tiết theo tài khoản tiền mặt. `ref_doctype=GL Entry`. Hiển thị posting_date, voucher_no, opening, debit, credit, closing balance per row, theo TK 111. |
| Phiếu quỹ chi nhánh | DocType | C | `Branch Cash Entry` | Phiếu thu/chi nội bộ theo chi nhánh (NOT GL-posting, chỉ ghi sổ nội bộ). Validate user branch perm qua `validate_user_can_manage_branch_cash`. Phục vụ chi nhánh có quỹ tiền mặt nội bộ chưa hợp nhất. |
| Sổ quỹ chi nhánh | Report | C | `Sổ nội bộ` (`so_noi_bo`) | Sổ chi tiết Branch Cash Entry theo chi nhánh + accounting_unit. `ref_doctype=Branch Cash Entry`. |

---

## Ngân hàng

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Thu ngân hàng | Report | C | `Bank Receipts` | Wrap `bank_account_book` với direction=Receipt. Lấy GL Entry Dr 112 (Bank). |
| Chi ngân hàng | Report | C | `Bank Payments` | Wrap `bank_account_book` với direction=Payment. GL Entry Cr 112. |
| Sổ Tài khoản ngân hàng | Report | C | `Bank Account Book` | Sổ chi tiết theo từng TK 112 con (1121/1122/…). `ref_doctype=GL Entry`. |
| Đối soát sao kê | Page | X | `bank-reconcile` (vn_banking) | Module vn_banking: upload XLS sao kê 4 bank VN (BIDV/MB/Sacombank/PG Bank), match rule-based + name-fuzzy với SI/PI/PE, inline-PE creation. Cross-app — không thuộc vn_accounting. |
| Điều chuyển nội bộ | Report | C | `Internal Transfer` | Tra cứu các JE chuyển nội bộ giữa các TK 111/112. `ref_doctype=GL Entry`. |
| Bút toán ngân hàng | DocType | S | `Journal Entry` | Stock ERPNext, mở dropdown filter cho voucher_type=Bank Entry. |
| Tiền gửi có kỳ hạn | DocType | C | `Term Deposit` | Hợp đồng tiền gửi: principal, kỳ hạn, lãi suất, ngày đáo hạn. Controller `TermDeposit.validate()` build lịch lãi qua `treasury.interest_calculator.build_interest_schedule()`, tính total interest, set default account (TK 128). Child `Term Deposit Interest` lưu từng kỳ trả lãi. |
| Tổng hợp tiền gửi có kỳ hạn | Report | C | `Term Deposit Summary` | Báo cáo gộp tất cả Term Deposit theo trạng thái + due date. |
| Khoản vay ngân hàng | DocType | C | `Bank Loan` | Hợp đồng vay: principal, kỳ hạn, lãi suất, lịch trả. Controller `BankLoan.validate()` build lịch qua `treasury.repayment_calculator.build_repayment_schedule()`. Child `Bank Loan Repayment` cho từng kỳ. |
| Tổng hợp khoản vay ngân hàng | Report | C | `Bank Loan Summary` | Báo cáo tổng hợp Bank Loan theo trạng thái + lịch trả. |
| Dự báo dòng tiền | Page | C | `cash-flow-forecast` | Page custom: dự báo dòng tiền theo granularity (ngày/tuần/tháng/quý), tách "Hiện hành" vs "Dự báo". Filter MultiSelectList. (Ref: `page/cash_flow_forecast/`) |

---

## Mua hàng

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Đơn mua hàng | DocType | S | `Purchase Order` | Stock ERPNext. |
| Đơn mua hàng cần lập hóa đơn | DocType | S | `Purchase Order` (filter) | Stock list với route_options lọc PO đã nhận hàng nhưng chưa có PI. |
| Hoá đơn mua hàng | DocType | S | `Purchase Invoice` | Stock ERPNext + Custom Fields `is_non_deductible` + `non_deductible_reason` (TNDN B4 phase 2). |
| Nhập kho mua hàng | DocType | S | `Purchase Receipt` | Stock ERPNext. |
| Điều khoản thanh toán | DocType | S | `Payment Terms Template` | Stock ERPNext. |
| Công nợ phải trả | Report | S | `Accounts Payable` | Stock ERPNext AP report. |
| Bảng tổng hợp công nợ NCC | Report | S | `Accounts Payable Summary` | Stock ERPNext AP summary by supplier. |
| BC mua hàng | Report | S | `Purchase Analytics` | Stock ERPNext analytics. |
| Mua không VAT | Report | C | `Purchase No VAT` | Báo cáo PI không có VAT (TK 1331 = 0). Dùng để tách CP không khấu trừ đầu vào. |
| BC theo mặt hàng | Report | S | `Item-wise Purchase Register` | Stock ERPNext. |
| Bút toán chung | DocType | S | `Journal Entry` | Stock + custom flag `is_non_deductible` trên JE Account row (Pattern A). |

---

## Bán hàng

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Báo giá | DocType | S | `Quotation` | Stock ERPNext. |
| Đơn bán hàng | DocType | S | `Sales Order` | Stock ERPNext. |
| Đơn bán hàng cần xuất hóa đơn | DocType | S | `Sales Order` (filter) | Stock list filter SO đã giao nhưng chưa SI. |
| Hoá đơn bán hàng | DocType | S | `Sales Invoice` | Stock ERPNext. |
| Điều khoản thanh toán | DocType | S | `Payment Terms Template` | Stock ERPNext (alias trong section Bán hàng). |
| Công nợ phải thu | Report | S | `Accounts Receivable` | Stock ERPNext AR. |
| Bảng tổng hợp công nợ KH | Report | S | `Accounts Receivable Summary` | Stock ERPNext AR by customer. |
| BC bán hàng | Report | S | `Sales Analytics` | Stock ERPNext. |
| Phiếu xuất kho | DocType | S | `Delivery Note` | Stock ERPNext. |
| Bút toán chung | DocType | S | `Journal Entry` | Stock (alias trong Bán hàng). |

---

## Hợp đồng & PAKD

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Danh sách hợp đồng | DocType | X | `DCNET Contract` (dcnet_contract) | Master hợp đồng client, sở hữu billing schedule + payment lifecycle. Tách app riêng (dcnet_contract). |
| Phương án kinh doanh | DocType | X | `Phuong An Kinh Doanh` (dcnet_pakd) | PAKD master — phương án kinh doanh, gồm Beneficiary Lines (commission/markup/kickback), Commission Lines, Workflow approval. JE auto-split per component + auto-flag `is_non_deductible` khi `recipient_tax_pct=0 AND no invoice_no`. |
| Hóa đơn cần ghi sổ | Report | X | `Invoices to Post` (dcnet_contract) | Hóa đơn theo contract chưa nhập sổ kế toán. |
| Hóa đơn quá hạn cần đôn thúc | Report | X | `Invoices Overdue by Contract` (dcnet_contract) | SI quá hạn theo contract — phục vụ đôn thúc thanh toán. |
| Thu tiền theo hợp đồng | Report | X | `Payments by Contract` (dcnet_contract) | PE theo từng contract — dòng tiền thu thực tế. |
| Sổ hoa hồng NVKD (phải trả) | Report | X | `Commission Register` (dcnet_pakd) | Sổ chi tiết hoa hồng NVKD theo PAKD: Posted (đã JE) + Pending (PE đã thu nhưng JE hoa hồng chưa post). |
| Phải trả phía khách (kickback/markup/referral) | Report | X | `Beneficiary Payable` (dcnet_pakd) | Beneficiary kickback/markup/referral phải trả khách hoặc bên thứ 3, kèm trạng thái thanh toán. |
| Công nợ theo hợp đồng | Report | X | `Outstanding Receivables by Contract` (dcnet_contract) | AR theo từng contract — phân biệt billed vs collected vs outstanding. |
| Kỳ thu tiền quá hạn | Report | X | `Overdue Billing Periods` (dcnet_contract) | Kỳ billing đã quá hạn của các contract recurring. |

---

## Kho

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Cài đặt PAKD | DocType | X | `PAKD Settings` (dcnet_pakd) | Single doc cấu hình PAKD (TK hoa hồng, ngưỡng duyệt, rule template defaults). |
| Nhập xuất kho | DocType | S | `Stock Entry` | Stock ERPNext. |
| Lịch sử nhắc duyệt PAKD | DocType | X | `PAKD Reminder Log` (dcnet_pakd) | Log nhắc duyệt PAKD (cron job push notification). |
| Kiểm kê kho | DocType | S | `Stock Reconciliation` | Stock ERPNext. |
| Số lô | DocType | S | `Batch` | Stock ERPNext. |
| Số seri | DocType | S | `Serial No` | Stock ERPNext. |
| BC nhập xuất tồn | Report | S | `Stock Balance` | Stock ERPNext. |
| BC tuổi kho | Report | S | `Stock Ageing` | Stock ERPNext. |
| Sổ chi tiết kho | Report | S | `Stock Ledger` | Stock ERPNext. |
| Định mức tồn kho | Report | S | `Itemwise Recommended Reorder Level` | Stock ERPNext. |
| Gói sản phẩm | DocType | S | `Product Bundle` | Stock ERPNext. |

---

## TSCĐ (Tài sản cố định)

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Danh sách | DocType | S | `Asset` | Stock ERPNext Asset + Custom Field `is_welfare_asset` (Pattern A — tài sản phúc lợi không khấu hao trừ TNDN). |
| Tính khấu hao | DocType | S | `Asset Depreciation Schedule` | Stock ERPNext. |
| Sửa chữa | DocType | S | `Asset Repair` | Stock ERPNext (vn_accounting override `make_gl_entries` cho capitalize=0 case). |
| Bàn giao TSCĐ | DocType | C | `Asset Handover` | Phiếu bàn giao tài sản giữa các bên (giao → nhận). Validate scope (TSCĐ/CCDC) consistency, tính total_asset_value, check threshold qua VN Accounting Settings.enable_value_thresholds. Child `Asset Handover Item` liệt kê từng asset. |
| Kiểm kê TSCĐ | DocType | C | `Asset Stocktake` | Kiểm kê TSCĐ theo location/department. `load_items()` auto-populate stocktake_items từ Asset list filter theo location + department. Child `Asset Stocktake Item` với cột book_value vs counted_value. |
| Thanh lý tài sản | DocType | C | `Asset Disposal` | Phiếu thanh lý tài sản: ghi nhận giá thanh lý, lợi nhuận/lỗ, JE Dr 214 + Dr 811 / Cr 211 + Cr 711. Method `execute()` post JE, `cancel_disposal()` revert. Child `Asset Disposal Participant` cho hội đồng thanh lý. |
| Sổ S21-DN | Report | C | `S21-DN` | Sổ TSCĐ theo TT99/2025 — fixed asset register chuẩn VN. `ref_doctype=Asset`. |
| Lịch sử khấu hao | Report | S | `Asset Depreciation Ledger` | Stock ERPNext. |

---

## CCDC (Công cụ dụng cụ)

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Danh sách CCDC | DocType | C | `CCDC Item` | Master CCDC. Lifecycle: Draft → "Đang sử dụng" (after submit) → "Đã ghi giảm". `validate()`: cost > 0, useful_period_months > 0, balance entries. `on_submit()`: post JE (Dr 242 / Cr 153) + create CCDC Allocation Schedule. `_autofill_entries()` build accounting_entries từ defaults. |
| Ghi giảm CCDC | DocType | C | `CCDC Writeoff` | Phiếu ghi giảm CCDC khi hỏng/mất/thanh lý. `validate()` check CCDC Item chưa bị ghi giảm. `on_submit()`: post JE + cancel pending allocation schedules + set CCDC Item.status="Đã ghi giảm". |
| Bàn giao CCDC | DocType | C | `Asset Handover` (scope=CCDC) | Cùng DocType với TSCĐ nhưng filter scope=CCDC. |
| Kiểm kê CCDC | DocType | C | `Asset Stocktake` (scope=CCDC) | Cùng DocType với TSCĐ nhưng filter scope=CCDC. |
| Sổ S22-DN | Report | C | `S22-DN Theo Doi TSCD CCDC` | Sổ theo dõi CCDC theo TT99/2025. `ref_doctype=Asset` (legacy ref — actual data từ CCDC Item). |
| Lịch phân bổ CCDC (242→6423) | DocType | C | `CCDC Allocation Schedule` | Lịch phân bổ CCDC 242 → 6423 hàng tháng. Auto-created từ `CCDCItem.on_submit()`. Cancel khi CCDC Writeoff. Method `get_progress()` báo tiến độ allocation. |

---

## Tiền lương

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Bảng chấm công | DocType | S | `Attendance` | Stock Frappe HRMS. |
| Bảng giờ công (theo dự án) | DocType | S | `Timesheet` | Stock Frappe HRMS + tag `project` để chia giờ theo dự án. |
| Bảng lương | DocType | S | `Payroll Entry` | Stock Frappe HRMS. |
| Phiếu lương | DocType | S | `Salary Slip` | Stock Frappe HRMS. |
| Cơ cấu lương | DocType | S | `Salary Structure` | Stock Frappe HRMS. |
| Thành phần lương | DocType | S | `Salary Component` | Stock + Custom Field `is_non_deductible` + `non_deductible_reason` (Pattern A — vd lương phúc lợi). |
| Gán Cơ cấu lương | DocType | S | `Salary Structure Assignment` | Stock Frappe HRMS. |
| Lương bổ sung | DocType | S | `Additional Salary` | Stock Frappe HRMS. |
| Danh sách nhân viên | DocType | S | `Employee` | Stock Frappe HRMS. |

---

## Giá thành

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Phân bổ CP vào giá vốn | DocType | S | `Landed Cost Voucher` | Stock ERPNext + Custom Fields (Hàng nhập khẩu flag, target_account override per line — TK 156 con). Hook `on_submit` post JE bù theo target_account. |
| CP chờ phân bổ (TK 242) | Report | C | `Landed Cost Pending Allocation` | Báo cáo PI đã ghi TK 242 (deferred expense) nhưng chưa allocate qua Process Deferred Accounting. `ref_doctype=GL Entry`. |
| Dự án — Giá thành | DocType | C | `Project Costing` | Master project costing — gom chi phí + giai đoạn (Project Costing Stage). Sở hữu các cost stages từng giai đoạn. `validate()` validate stage consistency. Method `close()` write-off WIP còn lại, `reopen()` mở lại. `get_wip_balance()` query GL TK 154 theo project. |
| Tiến độ xuất hóa đơn | Report | C | `Project Invoicing Progress` | Theo dõi từng stage: ngày dự kiến, trạng thái, days_to_due, giá xuất, SI link. Dùng để planning xuất hóa đơn theo tiến độ. |
| Kết chuyển CP SXC (627→154) | DocType | C | `Cost Allocation Run` | KTT phân bổ chi phí gián tiếp (TK 627) ra projects theo shares % (manual hoặc theo BOM/TS hours). Child `Cost Allocation Share` (project + %) + `Cost Allocation Source` (source GL/Salary Slip). `on_submit()` post JE Dr 154 (per project) / Cr 627. |
| Cài đặt phân bổ CP vào giá vốn | DocType | C | `LCV Allocation Settings` | Single config: TK 156-con mặc định cho từng loại phụ phí LCV. Child `LCV Expense Type Setting` (expense_type → target_account). |

---

## Thuế

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| HĐ GTGT đầu vào | DocType | X | `EInvoice Inward` (einvoice) | App `einvoice`: ghi HĐ GTGT mua vào lấy về từ provider VN (Mắt Bão, EasyInvoice, …). |
| HĐ GTGT đầu ra | DocType | S | `Sales Invoice` | Stock SI (alias trong Thuế section). Outward einvoice push qua app `einvoice`. |
| Tờ khai thuế GTGT (01/GTGT) | Report | C | `vat_return_01_gtgt` | Tờ khai 01/GTGT TT80/2021 — tổng hợp SI/PI theo nhóm thuế suất, output xuất XLSX/HTKK. `ref_doctype=Sales Invoice`. |
| Mẫu thuế bán hàng | DocType | S | `Sales Taxes and Charges Template` | Stock ERPNext. |
| Mẫu thuế mua hàng | DocType | S | `Purchase Taxes and Charges Template` | Stock ERPNext. |
| Mẫu thuế hàng hoá | DocType | S | `Item Tax Template` | Stock ERPNext. |
| [Pending] Kiểm tra MST | Page | C | `under-development` | Placeholder cho feature tra cứu MST qua API GDT — chưa implement. |

---

## Tổng hợp

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Đánh giá lại ngoại tệ | DocType | S | `Exchange Rate Revaluation` | Stock ERPNext — JE đánh giá lại số dư ngoại tệ cuối kỳ. |
| Phiếu khóa sổ kỳ | DocType | S | `Period Closing Voucher` | Stock ERPNext — đóng kỳ, kết chuyển 5xx/6xx về 421. |
| Định nghĩa kỳ kế toán | DocType | S | `Accounting Period` | Stock ERPNext — định nghĩa kỳ + lock voucher type. |
| Sổ nhật ký chung | Report | S | `General Ledger` | Stock ERPNext. (vn_accounting cũng ship `S03a-DN Sổ nhật ký chung` theo format TT99/2025 — không link sidebar) |
| Sổ chi tiết tài khoản | Report | C | `Account Detail Ledger` | Sổ chi tiết TK kiểu S38-DN TT99/2025 — gồm party + cost center. `ref_doctype=GL Entry`. |
| Bảng cân đối số phát sinh | Report | C | `Trial Balance Sheet` | Bảng CĐSP theo TT99/2025 — Tài khoản | Số dư đầu | PS Nợ kỳ | PS Có kỳ | Lũy kế Nợ | Lũy kế Có | Số dư cuối. `ref_doctype=GL Entry`. |

---

## Báo cáo tài chính

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Báo cáo tình hình tài chính (B01-DN) | Report | C | `B01-DN Bao Cao Tinh Hinh Tai Chinh` | Balance Sheet TT99/2025 (đã rename từ "Bảng cân đối kế toán" TT200). Tính số dư theo BCTC Mapping; sub-codes 100/110/111/… theo cấu trúc B01-DN. |
| Báo cáo kết quả HĐKD (B02-DN) | Report | C | `B02-DN Bao Cao KQHDKD` | Income Statement TT99/2025 — doanh thu, giá vốn, CP bán hàng, CP QLDN, thuế TNDN, LN. |
| Báo cáo lưu chuyển tiền tệ (B03-DN) | Report | C | `B03-DN Bao Cao LCTT` | Cash Flow Statement TT99/2025 — dòng tiền HĐ kinh doanh / Đầu tư / Tài chính (gián tiếp). |
| Thuyết minh BCTC (B09-DN) | Page | C | `b09-dn-generator` | Page generator multi-sheet Excel cho Thuyết minh BCTC. Mỗi sheet 1 phần thuyết minh (chính sách kế toán, biến động TSCĐ, vốn chủ, …). |
| Quyết toán TNDN (Form 03) | Report | C | `Quyet Toan TNDN Reconciliation` | Form 03/TNDN Reconciliation — 19 dòng cấu trúc A (LN kế toán) → B (điều chỉnh B4/B5/B6) → C (thu nhập chịu thuế) → D (thuế TNDN) + X1/X2/X3 (phân tích tỷ lệ thuế hiệu lực). Auto-fill B4 từ GL Entry.is_non_deductible. |
| Chi phí không được trừ (B4) | Report | C | `Bao Cao Chi Phi Khong Duoc Tru` | List GL Entry flagged `is_non_deductible=1` theo lý do (6 nhóm). 9 cột: Ngày / Loại CT / Số CT / Tài khoản / Loại bên / Bên liên quan / Lý do / Số tiền / Ghi chú. Summary B4 + chart by reason. |
| Tư vấn — Chi phí không trừ TNDN | URL | C | `/app/vn-help?app=vn_accounting&dir=help/bctc&file=tu-van-chi-phi-khong-duoc-tru` | Article tư vấn KTT: căn cứ pháp lý (NĐ 320/2025 + VAS 17), phân biệt chênh lệch vĩnh viễn vs tạm thời, 6 lý do, 6 hiểu lầm phổ biến, FAQ. Mở new tab. |
| Phân tích lợi nhuận (theo TTCP/Dự án) | Report | S | `Profitability Analysis` | Stock ERPNext — phân tích LN theo Cost Center / Project / Accounting Dimension. |
| So sánh ngân sách (Thực tế vs KH) | Report | S | `Budget Variance Report` | Stock ERPNext + monkey-patch fix locale month-key bug (vn_accounting `__init__.py`). |
| BC lãi lỗ quản trị | Report | S | `Profit and Loss Statement` | Stock ERPNext. |
| Tóm tắt Dự án | Report | S | `Project Summary` | Stock ERPNext. |
| Cấu hình BCTC Mapping | DocType | C | `BCTC Mapping` | Mapping Account → BCTC line code (theo từng template B01/B02/B03). Method `copy_from_company()` clone mapping từ company khác. `restore_from_template()` restore default từ `BCTC Mapping Template` (vn_large_enterprise / vn_small_trade). Child `BCTC Line` (line_code → account formula). |

---

## Danh mục

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Hệ thống tài khoản | DocType | S | `Account` | Stock ERPNext. |
| Khách hàng | DocType | S | `Customer` | Stock ERPNext. |
| Nhà cung cấp | DocType | S | `Supplier` | Stock ERPNext. |
| Hàng hoá, vật tư | DocType | S | `Item` | Stock ERPNext. |
| Kho | DocType | S | `Warehouse` | Stock ERPNext. |
| Nhân viên | DocType | S | `Employee` | Stock Frappe HRMS. |
| Định mức vật tư (BOM) | DocType | S | `BOM` | Stock ERPNext. |

---

## Thiết lập

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Mẫu hợp đồng | DocType | X | `DCNET Contract Template` (dcnet_contract) | Template hợp đồng (DOCX) với placeholder. |
| Cây tài khoản | DocType | S | `Account` (Tree view) | Stock ERPNext (alias trong Thiết lập). |
| Cài đặt Hợp đồng | DocType | X | `DCNET Contract Settings` (dcnet_contract) | Single config dcnet_contract. |
| Import cây tài khoản | DocType | S | `Chart of Accounts Importer` | Stock ERPNext. |
| Mẫu quy tắc hoa hồng | DocType | X | `PAKD Commission Rule Template` (dcnet_pakd) | Template rule hoa hồng (Sales Comm, Account Comm, Markup, Kickback, Referral). |
| Năm tài chính | DocType | S | `Fiscal Year` | Stock ERPNext. |
| Cài đặt PAKD | DocType | X | `PAKD Settings` (dcnet_pakd) | Single PAKD config (alias trong Thiết lập). |
| Kỳ kế toán | DocType | S | `Accounting Period` | Stock (alias). |
| Lịch sử nhắc duyệt PAKD | DocType | X | `PAKD Reminder Log` (dcnet_pakd) | Log nhắc duyệt (alias). |
| Trung tâm chi phí | DocType | S | `Cost Center` | Stock ERPNext. |
| Dự án | DocType | S | `Project` | Stock ERPNext. |
| Ngân sách | DocType | S | `Budget` | Stock ERPNext. |
| Cài đặt kho | DocType | S | `Stock Settings` | Stock ERPNext. |
| Cài đặt kế toán | DocType | C | `VN Accounting Settings` | Single config trung tâm: TK defaults (chênh lệch, asset thresholds, branch cash, deferred expense), permission matrix (cross-cutting role→DocType), enable_value_thresholds flag. `on_update()` sync permissions to DocPerm. |

---

## Công cụ Import

| Tên (Sidebar) | Kiểu | Loại | Target | Mô tả |
|---|---|---|---|---|
| Misa Migration Hub | Page | C | `misa-migration-hub` | Page Vue 3 SFC mount qua `frappe.misa_migration.Hub`. Upload Misa export XLSX, parse 5 sheets (COA / OB / Customer / Supplier / Voucher), preview, post lô lớn vào ERPNext. UI chính cho migration. |
| Lịch sử Migration | DocType | C | `Misa Migration Batch` | Phiên migration Misa → ERPNext. Status lifecycle 8 trạng thái: DRAFT → UPLOADED → PARSED → REVIEWED → POSTING → POSTED → REVERSING → REVERSED + STUCK (watchdog). `is_submittable=0` — không dùng docstatus. Locking qua `frappe.db.get_lock` per-company. |

---

## Cross-cutting features (không trên sidebar nhưng có trong code)

| Feature | Tên DocType/Module | Mô tả |
|---|---|---|
| Non-Deductible Tracking | Custom Fields trên JE Account / GL Entry / PI Item / EC Detail / Asset / Salary Component | Pattern A — cờ `is_non_deductible` + `non_deductible_reason` (6 lý do). Validate hook bắt buộc lý do khi tick. On submit hooks mirror cờ từ source-doc → GL Entry. dcnet_pakd `_is_non_deductible_beneficiary` auto-tag DR row khi `recipient_tax_pct=0 AND no invoice_no`. |
| Branch cash isolation | `Branch Cash Access` + `Branch Cash Entry` | User chi nhánh chỉ thấy / mutate phiếu thu-chi nội bộ của chi nhánh mình. Service `branch_cash.service.validate_user_can_manage_branch_cash`. |
| Sổ S03a/S03b-DN | Reports `S03a-DN So Nhat Ky Chung` + `S03b-DN So Cai` | Sổ kế toán TT99/2025 format — không link sidebar trong default config nhưng available trong Report list. |
| Project costing (627→154→632) | `Cost Allocation Run` + `Project Costing` + `Project Costing Stage` | Chuỗi VAS xây lắp: direct cost Dr 154/Project / indirect Dr 627 → CAR phân bổ Dr 154/Project / Cr 627 → SI submit hook Dr 632 / Cr 154/Project. Project close write-off WIP còn lại. |
| Asset permission matrix | `Asset Permission Rule` | Per-role-asset access rule (read/write theo asset category, branch). |
| Project P&L | Report `Project PnL Detailed` | Báo cáo P&L per project — query qua `Account.root_type` (Income/Expense), không hardcode TK 511/632 (per memory). |
| Project Cost Collection | Report `Project Cost Collection` | Tổng hợp chi phí theo project — phục vụ phân tích. |
| Account list catalog | `Account List Item` | Child DocType phục vụ filter / lookup grouping. |

---

## Tổng kê số lượng

| Loại | Số items trong sidebar |
|---|---|
| Stock DocType / Report (S) | ~55 |
| Custom DocType / Report / Page (C) | ~50 |
| Cross-app (X) — vn_banking / dcnet_contract / dcnet_pakd / einvoice | ~12 |
| URL | 1 |
| Section break | 15 |
| **Total** | 152 |

Custom modules cấp app vn_accounting cung cấp:
- **35 custom DocTypes** (Cash Count, Branch Cash Entry, Term Deposit, Bank Loan, CCDC Item/Writeoff/Allocation, Asset Handover/Stocktake/Disposal, Project Costing, Cost Allocation Run, BCTC Mapping, VN Accounting Settings, Misa Migration Batch, …)
- **26 custom Reports** (Cash Receipts/Payments/Book, Bank Receipts/Payments/Book, B01-B03-DN, S21/S22-DN, S03a/S03b-DN, Account Detail Ledger, Trial Balance Sheet, VAT Return 01/GTGT, Non-Deductible B4, Form 03 Reconciliation, Project Invoicing Progress, …)
- **5 custom Pages** (VN Accounting Dashboard, Cash Flow Forecast, B09-DN Generator, Misa Migration Hub, Under Development placeholder)

---

*File generated 2026-05-25 từ workspace_sidebar/vn_accounting.json + code base. Để regenerate, đọc lại sidebar JSON + scan custom DocType controllers / Report .py.*
