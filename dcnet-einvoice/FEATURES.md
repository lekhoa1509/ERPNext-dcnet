# einvoice — Features Matrix

App: `einvoice` | Stack: Frappe v16 + ERPNext v16 | Pháp lý: NĐ 123/2020, TT 78/2021

Ứng dụng đóng vai trò lớp tích hợp (integration layer) giữa ERPNext và các nhà cung cấp Hóa đơn điện tử Việt Nam (Mắt Bão, Viettel, MISA, Custom). Phục vụ 2 chiều: phát hành HĐĐT đầu ra (outward) và đồng bộ HĐĐT đầu vào (inward). Mọi feature dưới đây đều truy vết về `docs/BUSINESS_LOGIC.md`.

## A. Done (đã hoàn thành)

### A1. Hạ tầng & Cấu hình Provider

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A1.1 | DocType: EInvoice Provider | Cấu hình 1 nhà cung cấp / 1 công ty: MST, API URL (purchase + sales), token/username/password, ký hiệu mẫu số & ký hiệu mặc định (§4 BL) | Done | 2026-03 |
| A1.2 | DocType: EInvoice Settings | Single DocType — provider mặc định, chế độ phát hành (Draft/Publish), bulk limit, frequency sync, N-day window, mode_of_payment mặc định (§5.3, §5.5, §6.1) | Done | 2026-03 |
| A1.3 | Registry pattern 3 provider types + Custom | Mắt Bão, Viettel, MISA, Custom. Mỗi type map tới class provider tương ứng | Done | 2026-03 |
| A1.4 | Test kết nối provider | Button "Kiểm tra kết nối" trên form Provider — cập nhật connection_status + last_checked (§4 BL) | Done | 2026-03 |
| A1.5 | Mã hoá credential | Token/password/API key lưu dạng Password fieldtype — không hiển thị sau khi lưu (§8 BL) | Done | 2026-03 |
| A1.6 | BaseProvider + token cache Redis | Token cache theo key `einvoice_token:{provider}:{type}`, TTL ngắn hơn token gốc (1h token → cache 58 phút, §8 BL) | Done | 2026-03 |
| A1.7 | Shared `_api_call()` helper | Timeout 30s, xử lý Timeout/HTTPError/ConnectionError, chuyển thành `EInvoiceProviderError` với status + body[:500] | Done | 2026-03 |
| A1.8 | Custom exception hierarchy | `exceptions.py`: EInvoiceError / ProviderError / ProviderNotReady / AuthError / ValidationError — thông báo UX thân thiện | Done | 2026-03 |

### A2. Phát hành HĐĐT Đầu ra (Outward)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A2.1 | Nút "Phát hành HĐĐT" trên Sales Invoice | Chỉ hiện khi docstatus=1, chưa phát hành (§5.1 BL) | Done | 2026-03 |
| A2.2 | Ánh xạ SI → payload provider | `map_sales_invoice_to_payload()` — Mắt Bão adapter. Chuyển SI, items, tax, customer MST sang cấu trúc API | Done | 2026-03 |
| A2.3 | Ghi nhận kết quả phát hành | Lưu số HĐĐT, ký hiệu mẫu số, ký hiệu HĐ, mã tra cứu, URL PDF ngược trở lại Sales Invoice (§5.1 BL) | Done | 2026-03 |
| A2.4 | Chế độ Draft vs Publish | issue_mode cấu hình cấp Settings, có thể ghi đè từng HĐ khi phát hành (§5.3 BL) | Done | 2026-03 |
| A2.5 | Huỷ HĐĐT có lý do | Nút "Huỷ HĐĐT" kèm lý do bắt buộc, gửi lệnh huỷ sang provider, cập nhật trạng thái (§5.1 BL) | Done | 2026-03 |
| A2.6 | Phát hành hàng loạt (bulk) | Action list view Sales Invoice — respecting bulk_limit từ Settings (§5.4 BL) | Done | 2026-03 |
| A2.7 | Bulk chạy nền với ngưỡng | > ngưỡng → background job; dưới ngưỡng → synchronous. Lỗi 1 HĐ không dừng cả lô (§5.4 BL) | Done | 2026-03 |
| A2.8 | Ký hiệu mẫu số & ký hiệu | Lấy mặc định từ Provider, cho phép ghi đè per-invoice (§5.2 BL) | Done | 2026-03 |
| A2.9 | Mặc định hình thức thanh toán | Dùng mode_of_payment mặc định từ Settings khi SI chưa có (§5.5 BL) | Done | 2026-03 |
| A2.10 | Token tự làm mới khi hết hạn giữa bulk | Phát hiện 401 → gọi lại authenticate, xoá cache, retry 1 lần; lỗi tiếp → đánh dấu HĐ lỗi, qua HĐ kế (§9.5 BL) | Done | 2026-03 |
| A2.11 | DocType: EInvoice Issuance Log | Nhật ký mọi lần phát hành/huỷ: user, thời điểm, SI ref, kết quả, mã lỗi (§8 BL) | Done | 2026-03 |

### A3. Đồng bộ HĐĐT Đầu vào (Inward)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A3.1 | DocType: EInvoice Inward | Lưu HĐ đầu vào: MST bên bán, số HĐ, ngày, ký hiệu, tổng trước thuế, thuế suất, tiền thuế, mã tra cứu, URL PDF (§6.2 BL) | Done | 2026-03 |
| A3.2 | Status workflow: New → Matched → PI Created | + Ignored, + Error (§6.2 BL) | Done | 2026-03 |
| A3.3 | Scheduler sync định kỳ | Cron mỗi 15 phút + hourly + daily + weekly — gate bằng frequency Settings (§6.1 BL) | Done | 2026-03 |
| A3.4 | `run_if_frequency_match` check elapsed | So sánh `now - last_sync` với frequency; chưa đủ → bỏ qua (§6.1 BL) | Done | 2026-03 |
| A3.5 | Khoá phân tán (distributed lock) | Đảm bảo chỉ 1 sync chạy cùng lúc (§6.1 BL) | Done | 2026-03 |
| A3.6 | Sync thủ công qua button | "Sync ngay" trên list view, bypass frequency check (§6.1 BL) | Done | 2026-03 |
| A3.7 | N-day window | Mặc định 30 ngày, cấu hình trong Settings (§6.1 BL) | Done | 2026-03 |
| A3.8 | Dedupe theo mã tra cứu | Mã tra cứu unique → lần sync sau lấy lại HĐ cũ → bỏ qua (§9.7 BL) | Done | 2026-03 |
| A3.9 | DocType: EInvoice Sync Log | Nhật ký mỗi lần sync: provider, thời điểm, số HĐ lấy về, số mới, số trùng, lỗi (§6.1 BL) | Done | 2026-03 |
| A3.10 | Thoát im lặng khi chưa cấu hình | Scheduler detect chưa có Settings/Provider → exit không log lỗi (§9.6 BL) | Done | 2026-03 |

### A4. Matching & Tạo Purchase Invoice

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A4.1 | Auto-match PI đã tồn tại | Tìm PI cùng supplier + ngày ±N + tổng ±1%. Duy nhất 1 kết quả → match tự động (§6.2 BL) | Done | 2026-03 |
| A4.2 | Nút "Tạo HĐ mua" | Tự dựng Purchase Invoice từ dữ liệu Inward, set supplier, items, tax template (§6.2 BL) | Done | 2026-03 |
| A4.3 | Tax template matching theo thuế suất | Tính rate từ `tax / pre_tax * 100`, khớp rate với Purchase Taxes template — ưu tiên mặc định nếu nhiều (§6.3 BL) | Done | 2026-03 |
| A4.4 | Cảnh báo thuế suất không khớp | Không tìm thấy mẫu → cảnh báo, dùng mẫu mặc định, yêu cầu kế toán kiểm tra (§6.3, §9.8 BL) | Done | 2026-03 |
| A4.5 | So sánh tổng thuế sau khi tạo PI | Chênh > 1% → flag cảnh báo cho kế toán (§6.3 BL) | Done | 2026-03 |
| A4.6 | Nút "Bỏ qua" | Kế toán đánh dấu Ignored kèm ghi chú (§6.2 BL) | Done | 2026-03 |
| A4.7 | PI tạo kèm tax table đầy đủ | Fix bug: PI cũ tạo thiếu tax → tổng sai | Done | 2026-03 |

### A5. Stub Providers (Viettel / MISA)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A5.1 | Viettel stub | Mọi method raise `EInvoiceProviderNotReady("viettel")` — message "Provider chưa sẵn sàng, liên hệ đội triển khai" (§4, §2 out-of-scope BL) | Done | 2026-03 |
| A5.2 | MISA stub | Tương tự Viettel — giữ chỗ cho pluggability tương lai | Done | 2026-03 |
| A5.3 | Cảnh báo trên form Provider | JS hiển thị warning khi chọn type=Viettel/MISA | Done | 2026-03 |

### A6. Bảo mật & Quyền

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A6.1 | Role guard `only_for()` trên API | Mọi API endpoint require System Manager hoặc Accounts Manager (§8 BL) | Done | 2026-03 |
| A6.2 | DocType permissions | Kế toán User chỉ được đọc, không phát hành/huỷ/sync (§3, §8 BL) | Done | 2026-03 |
| A6.3 | Audit trail | User + thời điểm + kết quả cho mọi phát hành/huỷ/sync qua Issuance Log & Sync Log (§8 BL) | Done | 2026-03 |
| A6.4 | Log không chứa payload HĐ | Error log chỉ ghi mã lỗi + message tóm tắt, không dump payload (§8 BL) | Done | 2026-03 |

### A7. Workspace & UX

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A7.1 | Workspace "EInvoice" | Shortcut 5 DocTypes, fixture trong `workspace/einvoice/einvoice.json` | Done | 2026-03 |
| A7.2 | Desktop Icon trên Desk home | link_type="Workspace Sidebar", ASCII label, icon dùng Lucide mặc định | Done | 2026-04 |
| A7.3 | App logo + app tile | `add_to_apps_screen` — tile "Hóa đơn điện tử" route `/app/einvoice-settings` | Done | 2026-03 |
| A7.4 | Sales Invoice form customization | Button phát hành/huỷ, hiển thị số HĐĐT + mã tra cứu + link PDF | Done | 2026-03 |
| A7.5 | Sales Invoice list action | Bulk issue action trên list view | Done | 2026-03 |
| A7.6 | EInvoice Inward list action | Button "Sync ngay" + filter theo status | Done | 2026-03 |

### A8. EasyInvoice (SoftDreams) — Push-Draft Outward Flow

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A8.1 | Provider type EasyInvoice + 6 custom fields SI | `provider_type=EasyInvoice`, fields: `einvoice_pushed`, `einvoice_ikey`, `einvoice_status_text`, `einvoice_pushed_at`, `einvoice_link_view`, `einvoice_xml_file` | Done | 2026-05-07 |
| A8.2 | EasyInvoice auth (MD5 per-request) | `EasyInvoiceProvider._authenticate_easy()` — MD5(username+password+timestamp), no token cache | Done | 2026-05-07 |
| A8.3 | XML builder (pure Python) | `easyinvoice_xml.py` — escape, VAT infer, `<Invoices><Inv><IDTBHSS>` shape + 12 unit tests | Done | 2026-05-07 |
| A8.4 | `map_sales_invoice_to_payload()` | Reads SI customer, tax, items; infers VAT rate; formats `arising_date`; builds invoice_dict | Done | 2026-05-07 |
| A8.5 | `push_draft_invoice()` → endpoint #1 | POST `importInvoice`, parse per-ikey error from `KeyInvoiceMsg`, return `{success, ikey, status_code, status_text}` | Done | 2026-05-07 |
| A8.6 | `sync_invoice_state()` → endpoint #25 | POST `queryInvoicesByIkeys`, return per-ikey state dict with `invoice_status`, `no`, `lookup_code`, `link_view` | Done | 2026-05-07 |
| A8.7 | `download_attachment()` → endpoint #24 | POST `downloadInv`, validate magic bytes (PDF: `%PDF`, XML: `<?xml`/`<Inv`), return raw bytes | Done | 2026-05-07 |
| A8.8 | `IssuanceService.push_draft()` | Service method: validate pushed guard, resolve provider, call push_draft_invoice, write SI fields + Issuance Log | Done | 2026-05-07 |
| A8.9 | `services/state_sync.py` | `sync_pending_invoices()` + `_apply_state_update()` + `_download_and_attach()` bg job | Done | 2026-05-07 |
| A8.10 | Scheduler cron */15 outward sync | `tasks/sync_outward_states.py` gated by `enable_auto_sync`; added to `hooks.py` cron bucket | Done | 2026-05-07 |
| A8.11 | API: 3 endpoints outward | `push_to_easyinvoice`, `sync_outward_states_now`, `get_easyinvoice_link` | Done | 2026-05-07 |
| A8.12 | SI form: push button + status indicator | "Đẩy lên EasyInvoice" button, "Đồng bộ trạng thái" button, orange pending headline, green issued headline | Done | 2026-05-07 |
| A8.13 | 15 unit tests (provider + state_sync) | `tests/test_easyinvoice_provider.py` (12 tests) + `tests/test_state_sync.py` (3 tests) | Done | 2026-05-07 |

## B. In Progress (đang làm)

| # | Feature | Mô tả | Owner | Notes |
|---|---------|-------|-------|-------|

_(Trống — app đang ở trạng thái stable)_

## C. Planned (dự kiến)

| # | Feature | Rationale | Priority | Trigger |
|---|---------|-----------|----------|---------|
| C1 | Viettel provider implementation | Hoàn thiện stub — nhu cầu doanh nghiệp lớn dùng Viettel SInvoice (§4 BL) | High | Khi có khách hàng DCNET yêu cầu hoặc test account Viettel sẵn sàng |
| C2 | MISA provider implementation | Hoàn thiện stub — MISA meInvoice phổ biến với SME VN | Medium | Sau Viettel, khi có sample API docs + sandbox |
| C3 | Validate MST trước khi phát hành | Check 10 hoặc 13 chữ số, pattern đúng — tránh provider từ chối với lỗi khó hiểu (§9.9 BL) | High | Ngay khi có ca thực tế fail do MST sai |
| C4 | Multi-currency / HĐ ngoại tệ | Đính kèm tỷ giá khi phát hành, tiền thuế ghi VND (§9.3 BL) | Medium | Khi có khách xuất khẩu |
| C5 | Chuẩn hoá chiết khấu thương mại | Phân biệt chiết khấu thương mại (trên line) vs chiết khấu thanh toán, gom dòng âm ERP về đơn giá (§9.4 BL) | Medium | Khi gặp case thực tế bị reject |
| C6 | Đối chiếu cuối kỳ ERP vs HĐĐT | Report so sánh SI đã phát hành vs SI chưa phát hành vs HĐ bị huỷ ERP nhưng HĐĐT chưa huỷ (§9.1 BL) | High | Cần cho kế toán trưởng đối soát |
| C7 | HĐ thuế suất 8% (nghị quyết 43) | Theo dõi các lần gia hạn, auto-update mẫu thuế đầu vào (§9.2 BL) | Medium | Khi có thay đổi chính sách |
| C8 | Notification đáo hạn cuộn ký hiệu | Cảnh báo khi sắp hết số HĐ đã đăng ký (§9.12 BL) | Low | Khi doanh nghiệp chuyển sang phát hành khối lượng lớn |
| C9 | Custom provider framework | Hoàn thiện type "Custom" cho integration riêng (VNPT, BKAV, M-Invoice...) | Low | Nhu cầu từ dự án cụ thể |
| C10 | Dashboard phát hành | Số HĐ phát hành/tháng, tỷ lệ lỗi, top customer/supplier — phục vụ giám sát | Medium | Sau đối soát cuối kỳ (C6) |
| C11 | Vietnamese translations (vi.csv) | Label DocType & button hiện Vietnamese qua `translations/vi.csv` — tuân thủ English-first rule bench | Medium | Khi có user test với ngôn ngữ `vi` |
| C12 | Test suite mở rộng | Unit test cho Mắt Bão provider, token cache, tax template matching — nền tảng đã có từ A8.13 | Low | Khi cần đảm bảo coverage trước Viettel/MISA |

## Legend

| Cột | Nghĩa |
|-----|-------|
| Status | Done = merged vào main, In Progress = đang build trên branch, Planned = có rationale chưa code |
| Priority | High = cần cho go-live/đối soát, Medium = cần trong 3 tháng, Low = nice-to-have |
| §X BL | Tham chiếu mục X trong `docs/BUSINESS_LOGIC.md` |
