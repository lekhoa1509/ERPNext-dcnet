# VN Banking — Features

App: `vn_banking` | Stack: Frappe v16 + ERPNext v16 | Chuẩn: TT99/2025

## A. Features Đã Thực Hiện

### A1. Parser Sao Kê Ngân Hàng

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A1.1 | Parser BIDV | Sao kê `.xlsx` BIDV — đọc header row, cột ngày/số tiền/nội dung/tham chiếu | Done | 2026-04 |
| A1.2 | Parser MB Bank | Sao kê `.xlsx` MB Bank — xử lý merged cells (phải dùng `data_only=True`, không dùng `read_only`) | Done | 2026-04 |
| A1.3 | Parser Sacombank | Sao kê `.xlsx` Sacombank — format bảng sao kê chuẩn | Done | 2026-04 |
| A1.4 | Parser PG Bank | Sao kê HTML-as-`.xls` (PG Bank xuất HTML với đuôi .xls) — auto-detect rồi route qua `pandas.read_html` | Done | 2026-04 |
| A1.5 | Auto-detect format | `detect.py` tự nhận diện định dạng từ tên ngân hàng + row ngày đầu tiên | Done | 2026-04 |
| A1.6 | Bank Statement Format DocType | Khai báo mapping cột (date/credit/debit/description/reference/counter_account) theo chữ cái cột (A/B/C...), không theo header label | Done | 2026-04 |
| A1.7 | Normalizer | Chuẩn hóa số tiền, ngày, direction (credit/debit) về `NormalizedTransaction` | Done | 2026-04 |
| A1.8 | Dedupe hash | Hash theo `date + amount + reference + description` — upload lại file cũ → 0 giao dịch mới | Done | 2026-04 |
| A1.9 | Dedupe feedback | Khi toàn bộ file trùng → fallback hiển thị original import, có thông báo rõ ràng | Done | 2026-04 |

### A2. Matcher Engine

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A2.1 | InvoiceNoMatcher | Regex extract số hóa đơn (SI/PI) từ nội dung chuyển khoản — High confidence | Done | 2026-04 |
| A2.2 | InvoiceAmountMatcher | Tìm hóa đơn có `outstanding_amount` khớp duy nhất trong dung sai — High confidence | Done | 2026-04 |
| A2.3 | PartyAmountMatcher | Xác định đối tác từ counter_account_no/name, tìm hóa đơn khớp — Medium confidence | Done | 2026-04 |
| A2.4 | NameAmountMatcher | Fuzzy match tên đối tác bằng `rapidfuzz.partial_ratio` ≥80% — Low confidence | Done | 2026-04 |
| A2.5 | Multi-invoice combinations | Một giao dịch khớp N hóa đơn (combinations_sum_match), tối đa 5 tổ hợp | Done | 2026-04 |
| A2.6 | Confidence scoring | 4 mức: High (xanh lá) / Medium (vàng) / Low (cam) / None (đỏ) | Done | 2026-04 |
| A2.7 | Match engine pipeline | `engine.py` chạy tuần tự các matcher đã enable, dừng khi có High match | Done | 2026-04 |
| A2.8 | Bank Match Rule table | Bảng quy tắc child table: enable/disable, priority, confidence_override, tolerance_override (scaffold v2) | Done | 2026-04 |

### A3. Bank Reconcile UI

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A3.1 | Bank Reconcile page | Frappe Page — entry point đối soát sao kê | Done | 2026-04 |
| A3.2 | Upload dialog | Chọn Bank Account + drag-drop file + progress realtime | Done | 2026-04 |
| A3.3 | Smart upload flow | Nhận diện định dạng từ tên ngân hàng + validate row ngày | Done | 2026-04 |
| A3.4 | Transaction table | Bảng giao dịch với màu confidence + filter theo direction (Thu/Chi) | Done | 2026-04 |
| A3.5 | Side panel | Chi tiết giao dịch: đối tác gợi ý, hóa đơn gợi ý, giải thích matcher, chênh lệch | Done | 2026-04 |
| A3.6 | Stat bar | Thống kê theo mức confidence + empty state khi 0 giao dịch | Done | 2026-04 |
| A3.7 | Bulk actions bar | Tạo PE hàng loạt + Submit hàng loạt, scope theo import hiện tại | Done | 2026-04 |
| A3.8 | Party/Invoice pickers | Chọn đối tác + hóa đơn thủ công cho giao dịch không tự match | Done | 2026-04 |
| A3.9 | Explanation tooltip | Hiển thị matcher nào đã khớp + lý do (VD: "InvoiceNoMatcher: tìm thấy ACC-SI-2026-00045") | Done | 2026-04 |

### A4. Payment Entry Automation

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A4.1 | Create single PE | Tạo PE đơn lẻ từ giao dịch: ngày + số tiền + liên kết hóa đơn + mode_of_payment | Done | 2026-04 |
| A4.2 | Bulk create PE draft | Tạo hàng loạt PE nháp cho giao dịch High confidence | Done | 2026-04 |
| A4.3 | Bulk submit PE | Submit hàng loạt PE nháp, scope theo import batch hiện tại | Done | 2026-04 |
| A4.4 | Multi-invoice allocation | 1 PE phân bổ nhiều hóa đơn với số tiền tương ứng | Done | 2026-04 |
| A4.5 | Fee/difference deduction | Chênh lệch nhỏ (≤ dung sai) → thêm dòng Deductions vào PE, ghi vào TK 6415/6425/6427 | Done | 2026-04 |
| A4.6 | cost_center trên Deductions | Dòng Deductions kèm cost_center từ Company default | Done | 2026-04 |
| A4.7 | Mode of payment default | Set `mode_of_payment` mặc định theo direction (Credit/Debit) để sidebar filter đúng | Done | 2026-04 |
| A4.8 | Inline PE reconciliation | Đối soát PE trực tiếp trong bảng, không mở form riêng | Done | 2026-04 |
| A4.9 | Debit PE (chi tiền) | Hỗ trợ tạo PE phía chi (Pay) cho giao dịch Nợ — trả Nhà cung cấp | Done | 2026-04 |

### A5. Settings & Cấu Hình

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A5.1 | Bank Statement Settings | Single DocType — toàn bộ cấu hình tập trung | Done | 2026-04 |
| A5.2 | Enable/disable matchers | 4 toggle cho 4 matcher (invoice_no, invoice_amount, party_amount, name_amount) | Done | 2026-04 |
| A5.3 | Multi-invoice config | `enable_multi_invoice_match` + `multi_invoice_max_combinations` (mặc định 5) | Done | 2026-04 |
| A5.4 | Tolerance config | Fixed Amount (mặc định 1.000 VND) hoặc Percent (mặc định 0.1%) | Done | 2026-04 |
| A5.5 | Date window | `amount_date_tolerance_days` — tìm hóa đơn ±N ngày (mặc định 3) | Done | 2026-04 |
| A5.6 | Invoice number patterns | Child table chứa regex; seed mặc định: `ACC-SI-\d{4}-\d+`, `ACC-PI-\d{4}-\d+`, `SI-\d+`, `PINV-\d+` | Done | 2026-04 |
| A5.7 | PE action default | Draft / Submit khi tạo PE tự động | Done | 2026-04 |
| A5.8 | Mode of payment default | `default_mode_of_payment_credit` + `default_mode_of_payment_debit` | Done | 2026-04 |
| A5.9 | Difference account | Cấu hình TK chênh lệch (6415/6425/6427) cho dòng Deductions | Done | 2026-04 |

### A6. Workspace & Navigation

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A6.1 | Workspace "Banking VN" | Workspace với shortcut Bank Reconcile | Done | 2026-04 |
| A6.2 | Workspace Sidebar | Sidebar "Banking VN" với các link: Bank Reconcile, Bank Statement Import, Settings, Formats, Matcher Types | Done | 2026-04 |
| A6.3 | Stats bar empty fix | Fix hiển thị rỗng khi không có dữ liệu + sidebar links hoàn chỉnh | Done | 2026-04 |

### A7. Import Lifecycle

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A7.1 | Bank Statement Import | DocType quản lý từng đợt import — status Draft/Processing/Completed (không submittable) | Done | 2026-04 |
| A7.2 | trigger_import API | Endpoint kích hoạt pipeline ingestion + chạy realtime progress | Done | 2026-04 |
| A7.3 | Bank Txn Invoice Suggestion | Child table lưu gợi ý hóa đơn cho từng giao dịch (matcher output) | Done | 2026-04 |
| A7.4 | Rematch hiện có | Chạy lại đối soát sau khi đổi Settings (bật/tắt matcher, tolerance) | Done | 2026-04 |
| A7.5 | Dismiss transaction | Ẩn giao dịch không liên quan (phí nội bộ, lãi...) khỏi danh sách đối soát | Done | 2026-04 |
| A7.6 | Custom fields | Custom fields trên Bank Transaction + Bank Account (scaffold v2 API) | Done | 2026-04 |
| A7.7 | Seed fixtures | Seed các pattern `ACC-SINV-*` và bank formats trong `install.py` | Done | 2026-04 |

### A8. Reconcile API

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A8.1 | get/suggest endpoints | API trả danh sách giao dịch + gợi ý match cho UI | Done | 2026-04 |
| A8.2 | create_pe endpoint | API tạo PE từ 1 giao dịch | Done | 2026-04 |
| A8.3 | bulk endpoints | API bulk create + bulk submit PE | Done | 2026-04 |
| A8.4 | dismiss endpoint | API đánh dấu dismiss giao dịch | Done | 2026-04 |
| A8.5 | explain endpoint | API trả explanation matcher cho side panel | Done | 2026-04 |
| A8.6 | rematch endpoint | API chạy lại match cho import hiện có | Done | 2026-04 |
| A8.7 | Webhook entry | `api/webhook.py` — scaffold cho internet banking tích hợp sau này | Done | 2026-04 |

### A9. Tests

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A9.1 | Parser tests — 4 formats | `test_parser_all_formats.py` — BIDV, MB, Sacombank, PG Bank | Done | 2026-04 |
| A9.2 | Dedupe tests | `test_dedupe.py` — hash uniqueness + re-upload behavior | Done | 2026-04 |
| A9.3 | InvoiceNoMatcher tests | `test_matcher_invoice_no.py` — regex extraction + tolerance | Done | 2026-04 |
| A9.4 | InvoiceAmountMatcher tests | `test_matcher_invoice_amount.py` — unique outstanding match | Done | 2026-04 |
| A9.5 | PartyAmountMatcher tests | `test_matcher_party_amount.py` — counter_account resolution | Done | 2026-04 |
| A9.6 | NameAmountMatcher tests | `test_matcher_name_amount.py` — fuzzy name match | Done | 2026-04 |
| A9.7 | Combinations tests | `test_matcher_combinations.py` — multi-invoice sum match | Done | 2026-04 |
| A9.8 | Engine pipeline tests | `test_engine_pipeline.py` — tuần tự matcher + stop condition | Done | 2026-04 |
| A9.9 | Excel source tests | `test_source_excel.py` — openpyxl behaviors | Done | 2026-04 |
| A9.10 | Reconcile API tests | `test_reconcile_api.py` — endpoints E2E | Done | 2026-04 |

### A10. Bản Địa Hóa

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A10.1 | English-first i18n | Field labels, options, messages bằng English trong source | Done | 2026-04 |
| A10.2 | Vietnamese translations | `translations/vi.csv` cho các string UI/message | Done | 2026-04 |
| A10.3 | Format help text | Text hướng dẫn định dạng file upload (Vietnamese) | Done | 2026-04 |

---

## B. Features Đang Phát Triển

(Trống — v0.0.1 đã ship đầy đủ scope v1; chưa push to dcnet-cloud remote)

---

## C. Features Sẽ Thực Hiện

### C1. Mở Rộng Ngân Hàng

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C1.1 | Vietcombank parser | Sao kê VCB `.xlsx` / `.csv` | High | Ngân hàng phổ biến nhất VN |
| C1.2 | Techcombank parser | Sao kê TCB | High | |
| C1.3 | VPBank parser | Sao kê VPBank | Medium | |
| C1.4 | ACB parser | Sao kê ACB | Medium | |
| C1.5 | Vietinbank parser | Sao kê CTG | Medium | |
| C1.6 | Agribank parser | Sao kê VBA | Medium | Định dạng có thể là HTML-as-xls |

### C2. Đa Tệ

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C2.1 | Tài khoản ngoại tệ | Hỗ trợ parser cho sao kê USD/EUR | Medium | Cần tỷ giá tại ngày giao dịch |
| C2.2 | Quy đổi VND trong PE | PE đa tệ với exchange_rate tự động | Medium | Tích hợp với Currency Exchange |
| C2.3 | Chênh lệch tỷ giá | Tự động hạch toán chênh lệch tỷ giá vào TK 413/515/635 | Medium | |

### C3. Tự Động Hóa Nâng Cao

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C3.1 | Scheduled reconcile | Cron job chạy match định kỳ cho import chưa xử lý | Medium | Daily hoặc hourly |
| C3.2 | Auto-submit High confidence | Tự submit PE High mà không cần xác nhận (có toggle an toàn) | Low | Cần audit log |
| C3.3 | Notification unmatched | Alert khi có giao dịch chưa match sau N ngày | Medium | Cho Accounts Manager |
| C3.4 | Rule engine learning | ML matcher học từ lịch sử — nâng confidence sau khi user xác nhận lặp lại pattern | Low | Phase 2+ |

### C4. Tích Hợp Ngoài

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C4.1 | Internet Banking API | Kết nối trực tiếp API bank (nếu nhà băng cung cấp) thay upload thủ công | High | Chỉ số ít bank có API mở |
| C4.2 | OCR PDF statement | Đọc sao kê PDF (các ngân hàng không xuất Excel) bằng OCR | Medium | Cần thư viện OCR |
| C4.3 | Webhook nhận push | Endpoint nhận webhook từ internet banking (real-time notification) | Medium | Scaffold đã có ở `api/webhook.py` |
| C4.4 | E-invoice cross-check | Verify hóa đơn điện tử khớp với PE | Low | Cần e-invoice integration |

### C5. Báo Cáo & Dashboard

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C5.1 | Reconcile dashboard | Tỉ lệ match/unmatch theo tháng, top matcher hiệu quả | Medium | |
| C5.2 | Bank statement vs book report | Đối chiếu số dư sao kê vs sổ cái TK 112 | High | Cần cho audit |
| C5.3 | Unmatched transactions report | Danh sách giao dịch chưa match > N ngày | Medium | |

### C6. Bank Match Rule v2

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C6.1 | Rule per bank account | Áp dụng rule khác nhau cho từng Bank Account | Medium | Scaffold đã có field `bank_account` |
| C6.2 | Drag-drop priority UI | UI kéo-thả thay đổi thứ tự matcher | Low | |
| C6.3 | Confidence override từ rule | Ghi đè confidence của matcher theo rule | Low | Scaffold đã có field |
| C6.4 | Custom matcher registry UI | Form đăng ký matcher mới không cần edit fixture | Low | |

---

## Legend

| Status | Nghĩa |
|--------|-------|
| Done | Đã merge vào main hoặc đang trên branch ổn định |
| In Progress | Đang fix/build trên feature branch |
| Planned | Có spec hoặc đã thảo luận, chưa bắt đầu code |
| — (Priority) | High = cần cho go-live, Medium = cần trong 3 tháng, Low = nice-to-have |
