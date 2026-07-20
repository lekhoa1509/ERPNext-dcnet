# DCNET Flow — Tài Liệu Onboarding

> Tạo tự động từ knowledge graph của codebase ngày 21/03/2026.
> Commit: `5464768`

---

## Tổng Quan Dự Án

**DCNET Flow** là nền tảng quản lý doanh nghiệp toàn diện, kết hợp CRM, Bán hàng, Kho, Kế toán và các module nghiệp vụ chuyên biệt. Được xây dựng trên **Frappe v16** và **ERPNext v16**, cung cấp hệ thống ERP tích hợp với các ứng dụng tùy chỉnh chạy trên nền ERPNext.

| Thuộc tính | Chi tiết |
|------------|----------|
| **Ngôn ngữ** | Python (chính), JavaScript, Vue, TypeScript, Shell |
| **Framework** | Frappe v16, ERPNext v16 |
| **Cơ sở dữ liệu** | MariaDB 10.6 |
| **Cache** | Redis 6.2 |
| **Môi trường phát triển** | Docker devcontainer (VS Code) |
| **Triển khai** | 2 site riêng cho 2 công ty, dùng chung codebase |

### Cấu Trúc Repository

```
flow_next/
├── dcnet_core/          # ERPNext v16 (symlink thành apps/erpnext)
├── dcnet_apps/          # Module tùy chỉnh DCNET (symlink thành apps/dcnet_apps)
├── dcnet_hrms/          # Hệ thống quản lý nhân sự
├── development/         # Script cài đặt & thiết lập dev
├── docs/                # Tài liệu nghiệp vụ (specs, modules, kế hoạch)
└── .devcontainer/       # Docker Compose + devcontainer config
```

---

## Các Tầng Kiến Trúc

Codebase được tổ chức thành **7 tầng kiến trúc** với tổng cộng **4.267 file mã nguồn**:

### 1. ERPNext Nghiệp Vụ Cốt Lõi (1.938 files)

Các module nghiệp vụ ERP chính: Kế toán, Bán hàng, Mua hàng, Kho, CRM, Hỗ trợ, Tổng đài, và tài nguyên frontend dùng chung.

**Thư mục chính:**
- `dcnet_core/erpnext/accounts/` — Sổ cái, Hóa đơn, Thanh toán, Đối chiếu ngân hàng, Quy tắc giá, Trung tâm chi phí, Ngân sách
- `dcnet_core/erpnext/selling/` — Đơn bán hàng, Báo giá, Khách hàng
- `dcnet_core/erpnext/buying/` — Đơn mua hàng, Nhà cung cấp, Yêu cầu báo giá
- `dcnet_core/erpnext/stock/` — Kho hàng, Phiếu xuất/nhập kho, Tồn kho, Quản lý Batch/Serial
- `dcnet_core/erpnext/crm/` — Lead, Cơ hội kinh doanh, Khách hàng tiềm năng
- `dcnet_core/erpnext/public/` — JS tiện ích dùng chung, templates, trang portal

### 2. HRMS — Nhân Sự (933 files)

Hệ thống quản lý nhân sự toàn diện, bao phủ toàn bộ vòng đời nhân viên.

**Thư mục chính:**
- `dcnet_hrms/hrms/payroll/` — Phiếu lương, xử lý bảng lương, tính thuế TNCN
- `dcnet_hrms/hrms/hr/` — Hồ sơ nhân viên, onboarding, điều chuyển, đánh giá
- `dcnet_hrms/hrms/overrides/` — Ghi đè DocType ERPNext cho tích hợp HR

### 3. Patches & Migrations (460 files)

Các bản vá cơ sở dữ liệu, migration schema, và script nâng cấp phiên bản cho ERPNext và HRMS.

- `dcnet_core/erpnext/patches/` — Script migration từ v12 đến v16
- `dcnet_hrms/hrms/patches/` — Migration riêng cho HRMS

### 4. ERPNext Sản Xuất & Dự Án (438 files)

Sản xuất, Gia công, Dự án, Quản lý chất lượng, và Bảo trì.

**Thư mục chính:**
- `dcnet_core/erpnext/manufacturing/` — BOM (Định mức), Lệnh sản xuất, Kế hoạch sản xuất
- `dcnet_core/erpnext/projects/` — Công việc, Bảng chấm công
- `dcnet_core/erpnext/quality_management/` — Kiểm tra chất lượng, Quy trình

### 5. ERPNext Thiết Lập & Cấu Hình (381 files)

Thiết lập, Tài sản cố định, Bản địa hóa theo vùng, Tiện ích, và cấu hình gốc.

**Thư mục chính:**
- `dcnet_core/erpnext/setup/` — Thiết lập Công ty, Nhân viên, Workspace
- `dcnet_core/erpnext/assets/` — Tài sản cố định, lịch khấu hao
- `dcnet_core/erpnext/regional/` — Tuân thủ pháp luật theo quốc gia (bản địa hóa Việt Nam)
- `dcnet_core/erpnext/hooks.py` — Điểm khởi đầu ứng dụng ERPNext

### 6. Ứng Dụng Tùy Chỉnh — DCNET (104 files)

Các module nghiệp vụ tùy chỉnh của DCNET, mở rộng ERPNext cho nhu cầu đặc thù Việt Nam.

**Thư mục chính:**
- `dcnet_apps/dcnet_apps/hooks.py` — Điểm khởi đầu app tùy chỉnh (fixtures, events, overrides)
- `dcnet_apps/dcnet_apps/install.py` — Thiết lập icon desktop, định dạng tiền tệ, workspace
- `dcnet_apps/dcnet_apps/dcnet_einvoice/` — Tích hợp hóa đơn điện tử Việt Nam (nhà cung cấp Mật Báo)
- `dcnet_apps/dcnet_apps/dcnet_report/` — Báo cáo tùy chỉnh (Cảnh báo tồn kho thấp, Tình trạng bảo hành)
- `dcnet_apps/dcnet_apps/dcnet_image_management/` — Quản lý hình ảnh sản phẩm
- `dcnet_apps/dcnet_apps/barcode_management/` — Tạo và in mã vạch
- `dcnet_apps/dcnet_fixtures/` — Trình tạo dữ liệu mẫu (kế toán Việt Nam, chu kỳ bán hàng)

### 7. Công Cụ Phát Triển (13 files)

Script thiết lập môi trường phát triển và cấu hình trợ lý AI.

- `development/installer.py` — Script tự động cài đặt cho devcontainer
- `development/start-bench.sh` — Script khởi động Bench

---

## Các Khái Niệm Quan Trọng

### Kiến Trúc DocType trong Frappe

**DocType** là thành phần cơ bản nhất của Frappe — tương đương với model + view + controller trong Django gộp lại thành một. Mỗi DocType nằm trong thư mục riêng:

```
doctype/{tên}/
├── {tên}.json        # Định nghĩa fields, permissions, workflow (schema)
├── {tên}.py          # Controller phía server (Python class)
├── {tên}.js          # Script phía client (JavaScript)
├── test_{tên}.py     # Unit tests
└── {tên}_dashboard.py  # Dashboard tài liệu liên quan (tùy chọn)
```

**Các pattern quan trọng:**
- Controller kế thừa từ `frappe.model.document.Document`
- Lifecycle hooks: `validate()`, `before_save()`, `on_submit()`, `on_cancel()`
- Client script sử dụng `frappe.ui.form.on()` để xử lý sự kiện form

### hooks.py — Điểm Khởi Đầu Ứng Dụng

Mỗi ứng dụng Frappe khai báo các điểm tích hợp trong `hooks.py`:
- `fixtures` — Dữ liệu tự động export/import
- `doc_events` — Handler Python được kích hoạt theo lifecycle DocType
- `scheduler_events` — Tác vụ lên lịch kiểu cron
- `override_whitelisted_methods` — Thay thế API endpoint có sẵn
- `jenv` — Filter/method Jinja template tùy chỉnh

### GL Entry — Bút Toán Kép

Mọi giao dịch tài chính đều tạo ra **GL (General Ledger) Entry** — đơn vị nguyên tử của kế toán:

```
Hóa đơn bán → Nợ 131 (Phải thu KH), Có 5111 (Doanh thu), Có 33311 (Thuế GTGT)
               + Nợ 632 (Giá vốn), Có 1561 (Hàng tồn kho)
Hóa đơn mua → Nợ 1561 (Hàng tồn kho), Nợ 1331 (Thuế GTGT), Có 331 (Phải trả NCC)
Phiếu thu/chi → Nợ 1111/1121 (Tiền mặt/Ngân hàng), Có 131 (Phải thu KH)
```

### Kế Toán Việt Nam (Thông Tư 200)

Dự án sử dụng hệ thống tài khoản theo Thông tư 200/2014/TT-BTC. File COA tùy chỉnh (`docs/accounting/ChartOfAccountsImporter_v2.csv`) với 254 tài khoản.

---

## Lộ Trình Học — 10 Bước Khám Phá Codebase

Làm theo 10 bước sau để hiểu codebase từ điểm khởi đầu đến phần tùy chỉnh:

### Bước 1: Điểm Khởi Đầu & Kiến Trúc Ứng Dụng

Mỗi ứng dụng Frappe bắt đầu từ `hooks.py`. Hãy đọc file này trước để hiểu cách 3 ứng dụng (ERPNext, DCNET Apps, HRMS) đăng ký với framework.

**File cần đọc:**
- `dcnet_apps/dcnet_apps/hooks.py` — Hooks app tùy chỉnh (fixtures, events, overrides)
- `dcnet_core/erpnext/__init__.py` — Khởi tạo ERPNext
- `dcnet_apps/dcnet_apps/install.py` — Thiết lập sau cài đặt (icons, tiền tệ, workspaces)

### Bước 2: Giải Phẫu DocType — Ví Dụ Account (Tài Khoản)

Nghiên cứu DocType Account như một mẫu tham chiếu hoàn chỉnh. Nó minh họa JSON schema, Python controller, JavaScript client script, và hiển thị dạng cây.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/account/account.py` — Controller server
- `dcnet_core/erpnext/accounts/doctype/account/account.js` — Client script
- `dcnet_core/erpnext/accounts/doctype/account/account_tree.js` — Hiển thị dạng cây
- `dcnet_core/erpnext/accounts/doctype/account/test_account.py` — Tests

### Bước 3: Hệ Thống Tài Khoản & Thiết Lập Kế Toán Việt Nam

Hiểu cách ERPNext nạp hệ thống tài khoản theo từng quốc gia. Trình nhập khẩu xử lý các dictionary Python có cấu trúc định nghĩa cây tài khoản.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/account/chart_of_accounts/chart_of_accounts.py`
- `dcnet_core/erpnext/accounts/doctype/chart_of_accounts_importer/chart_of_accounts_importer.py`

### Bước 4: GL Entry — Trái Tim Của Kế Toán Kép

GL Entry là đơn vị nguyên tử của ghi nhận tài chính. Mọi hóa đơn, thanh toán, và biến động kho cuối cùng đều tạo ra GL entries.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/gl_entry/gl_entry.py`
- `dcnet_core/erpnext/accounts/doctype/journal_entry/journal_entry.py`

### Bước 5: Hóa Đơn Mua & Bán — Chứng Từ Giao Dịch

Đây là các chứng từ nghiệp vụ chính điều khiển chu kỳ mua-bán. Hiểu cách hóa đơn tạo GL entries, cập nhật kho, và quản lý thuế.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py`
- `dcnet_core/erpnext/accounts/doctype/pos_invoice/pos_invoice.py`

### Bước 6: Xử Lý Thanh Toán & Đối Chiếu

Payment Entry xử lý mọi luồng tiền. Bank Reconciliation đối chiếu sao kê ngân hàng với các giao dịch.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/payment_entry/payment_entry.py`
- `dcnet_core/erpnext/accounts/doctype/payment_reconciliation/payment_reconciliation.py`
- `dcnet_core/erpnext/accounts/doctype/bank_reconciliation_tool/bank_reconciliation_tool.py`

### Bước 7: Giá, Khuyến Mãi & Tích Điểm

Hệ thống định giá xử lý giá buôn/lẻ, chiết khấu theo số lượng, chương trình khuyến mãi, và tích điểm khách hàng thân thiết.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/pricing_rule/pricing_rule.py`
- `dcnet_core/erpnext/accounts/doctype/pricing_rule/utils.py`
- `dcnet_core/erpnext/accounts/doctype/loyalty_program/loyalty_program.py`

### Bước 8: Báo Cáo Tài Chính & Khóa Sổ

Báo cáo tài chính truy vấn GL entries theo kỳ. Period Closing Voucher xử lý khóa sổ cuối năm.

**File cần đọc:**
- `dcnet_core/erpnext/accounts/doctype/financial_report_template/financial_report_engine.py`
- `dcnet_core/erpnext/accounts/doctype/period_closing_voucher/period_closing_voucher.py`

### Bước 9: Module Tùy Chỉnh DCNET

Gói dcnet_apps mở rộng ERPNext với các tính năng đặc thù Việt Nam: tích hợp hóa đơn điện tử, báo cáo tùy chỉnh, quản lý hình ảnh.

**File cần đọc:**
- `dcnet_apps/dcnet_apps/dcnet_einvoice/providers/matbao.py` — Nhà cung cấp HĐĐT
- `dcnet_apps/dcnet_apps/dcnet_report/report/low_stock_alert/low_stock_alert.py`
- `dcnet_apps/dcnet_apps/dcnet_report/report/serial_no_warranty_status/serial_no_warranty_status.py`

### Bước 10: Công Cụ Phát Triển & Dữ Liệu Mẫu

Hệ thống fixture tạo dữ liệu mẫu thực tế cho Việt Nam phục vụ phát triển.

**File cần đọc:**
- `dcnet_apps/dcnet_fixtures/commands.py` — Lệnh CLI
- `dcnet_apps/dcnet_fixtures/dcnet_fixtures/generators/foundation.py` — Trình tạo dữ liệu nền
- `dcnet_apps/dcnet_fixtures/dcnet_fixtures/generators/vietnamese_accounting.py`

---

## Vùng Code Phức Tạp

Các khu vực có code phức tạp nhất (646 files xếp hạng "complex"). Cần tiếp cận cẩn thận:

| Khu vực | Số file phức tạp | Ví dụ |
|---------|:----------------:|-------|
| **Kế toán** | ~150+ | `payment_entry.py`, `purchase_invoice.py`, `pos_invoice.py`, `pricing_rule/utils.py` |
| **Kho** | ~80+ | `stock_entry.py`, `stock_reconciliation.py`, `stock_ledger.py` |
| **Bán hàng/Mua hàng** | ~60+ | `sales_order.py`, `purchase_order.py`, `request_for_quotation.py` |
| **Nhân sự - Bảng lương** | ~50+ | `salary_slip.py`, `payroll_entry.py`, `expense_claim.py` |
| **Sản xuất** | ~48 | `bom.py` (90 hàm!), `work_order.py`, `production_plan.py` |
| **Tài sản cố định** | ~30+ | `asset.py` (88 methods), `depreciation.py` (43 hàm) |
| **DCNET tùy chỉnh** | 19 | `install.py` (846 dòng), `matbao.py`, `hooks.py` |

### Top "Rồng" (file phức tạp nhất)

1. **`bom.py`** — 90 hàm, duyệt cây BOM đệ quy
2. **`asset.py`** — 88 methods, logic khấu hao phức tạp
3. **`test_account.py`** — 66 hàm test, kiểm thử kế toán toàn diện
4. **`depreciation.py`** — 43 hàm, tính toán khấu hao tài sản
5. **`test_pricing_rule.py`** — 40 hàm test, các trường hợp biên về giá
6. **`install.py`** (dcnet_apps) — 846 dòng, thiết lập sau cài đặt

---

## Bắt Đầu Nhanh

### 1. Thiết lập môi trường phát triển

```bash
cd .devcontainer
docker compose up -d

# Chờ 10-15 phút cho lần cài đặt tự động đầu tiên
docker compose logs -f frappe
```

Truy cập: http://localhost:8000 — Đăng nhập: `Administrator` / `123456`

### 2. Chạy lệnh bench

```bash
# Bên trong Docker container
docker exec devcontainer-frappe-1 bash -c \
  "cd /workspace/development/frappe-bench && bench --site flow.local [lệnh]"

# Các lệnh thường dùng
bench --site flow.local migrate          # Chạy migration
bench --site flow.local clear-cache      # Xóa cache
bench --site flow.local run-tests --app dcnet_apps  # Chạy tests
```

### 3. Tạo dữ liệu mẫu

```bash
bench --site flow.local dcnet-fixtures generate                    # Tất cả modules
bench --site flow.local dcnet-fixtures generate --module master    # Module cụ thể
bench --site flow.local dcnet-fixtures status                      # Kiểm tra trạng thái
```

### 4. Đọc tài liệu specs

Nguồn chính thức cho yêu cầu tính năng:
- `docs/feature/FEATURE_SPECIFICATION.md` — Giai đoạn 1: CRM
- `docs/feature/ERP_SPECIFICATION.md` — Giai đoạn 2: ERP
- `docs/feature/IMPORT_PROCESS_SPECIFICATION.md` — Quy trình nhập khẩu

---

## Tài Liệu Tham Khảo

| Tài liệu | Đường dẫn |
|-----------|-----------|
| Quy tắc phát triển | `CLAUDE.md` |
| Quy trình Git | `docs/git-flow.md` |
| Timeline dự án | `docs/roadmap/TIMELINE_2026.md` |
| Tiến độ modules | `docs/modules/PROGRESS.md` |
| Hạ tầng cloud | `docs/infrastructure/CLOUD_INFRASTRUCTURE_PLAN.md` |
| Phân tích hệ thống tài khoản | `docs/accounting/COA_ANALYSIS.md` |
| Tham chiếu luồng ERPNext | `docs/erpnext-flows/` (19 file phân tích) |
| Tài liệu kiến trúc | `docs/architecture/` |

---

*Tạo từ phân tích knowledge graph của 4.267 file mã nguồn với 19.531 thành phần code.*
