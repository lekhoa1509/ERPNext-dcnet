# Phân tích & đề xuất: Realtime cho Query Reports (FB-2026-00625)

> Trạng thái: **Phân tích — chưa triển khai.** Tài liệu đề xuất phương án để chốt trước khi code.
> FB gốc: "frontend engineer muốn các query report phải realtime" — màn `query-report/Cash Receipts`.
> Ngày: 2026-05-29 · App: vn_accounting

---

## 1. Tóm tắt điều hành (TL;DR)

- Đây **KHÔNG phải arch change lớn** như đánh giá ban đầu. Frappe v16 **đã có sẵn toàn bộ hạ tầng realtime** (socket.io server, `frappe.realtime.on()`, `doctype_subscribe()`), và **mỗi lần lưu chứng từ đã tự broadcast event `list_update`** tới phòng (room) của doctype đó (`frappe/model/document.py:1434`). Query report cũng đã dùng realtime sẵn cho prepared-report.
- **Việc cần làm thật sự = (a) sửa kết nối socket.io + (b) wiring nhỏ ở client.** Console của chính FB này báo `Error connecting to socket.io: timeout` → realtime hiện **chưa kết nối được**. Đây là tiền đề: không sửa cái này thì mọi phương án realtime đều vô nghĩa.
- **Đề xuất: Phương án C (Hybrid)** — event-driven push khi socket.io OK, fallback poll nhẹ khi mất kết nối, cộng "dirty-check" rẻ trước khi re-query nặng. Triển khai **theo phase, opt-in theo report**, KHÔNG bật realtime cho mọi report (Balance Sheet/P&L/BCTC giữ on-demand).

---

## 2. Hiện trạng kỹ thuật (cái gì đã có, cái gì thiếu)

### 2.1 Hạ tầng realtime đã có sẵn
| Thành phần | Hiện trạng | Vị trí |
|---|---|---|
| Socket.io server | Chạy port riêng `9002` (web = 8001) | `Procfile: socketio` |
| Redis cho socketio | `redis://127.0.0.1:13002` | `common_site_config.json` |
| Client API | `frappe.realtime.on(event, cb)`, `frappe.realtime.doctype_subscribe(dt)` | `socketio_client.js:12,145` |
| Broadcast khi lưu doc | `notify_update()` tự `publish_realtime("list_update", …, after_commit=True)` cho doctype room | `document.py:1414-1434` |
| Realtime trong query report | Đã subscribe `report_generated` cho prepared report | `query_report.js:115` |
| Pattern stale-check | `setInterval(check_if_report_is_stale, 60000)` đã tồn tại | `query_report.js:796` |

**Kết luận:** không thiếu hạ tầng. Thiếu (1) kết nối socket.io ổn định, (2) đoạn wiring "report tự refresh khi dữ liệu nguồn đổi".

### 2.2 Vấn đề chặn (#0): socket.io timeout
Console FB: `Error connecting to socket.io: timeout` (×2).
- **Local dev:** client gọi `/socket.io` nhưng proxy/port không trỏ đúng `socketio_port=9002` (xem rule "Frappe Realtime Socket.io Port" — realtime chạy port riêng web server).
- **Production (`dcnet.nextstar-erp.com`):** nginx phải proxy `location /socket.io` → `http://127.0.0.1:<socketio_port>`. Nếu thiếu block này → timeout.
- **Đây là PREREQUISITE.** Mọi phương án A/C/D phụ thuộc socket.io. Chỉ phương án B (poll) sống sót khi socket.io chết.

### 2.3 Nguồn dữ liệu các report nhóm "cần realtime"
Các report giám sát hằng ngày (Cash Receipts, Bank…) **đọc từ `tabGL Entry`** (`report_utils.py:219 get_transactions`). GL Entry được sinh khi submit **Payment Entry / Journal Entry / Sales Invoice / Purchase Invoice / Stock Entry**.

> ⚠️ Lưu ý quan trọng: GL Entry là doctype `in_create` (chỉ sinh tự động). Trigger realtime **đáng tin cậy nhất = subscribe các doctype chứng từ NGUỒN** (PE/JE/SI/PI) — đây là các doc người dùng submit và chắc chắn phát `list_update` qua vòng đời chuẩn — chứ không dựa vào emission của GL Entry (đường `make_gl_entries` bulk, không chắc chắn).

---

## 3. Phân loại report theo nhu cầu realtime (Performance Budget)

KHÔNG bật realtime đại trà. Phân 3 bậc theo 2 trục: **tần suất theo dõi trong ngày** + **chi phí SQL**.
Đã duyệt 2026-05-29 — đây là registry chính thức (lưu trong `realtime_reports.bundle.js`).

### TIER 1 — Auto BẬT (giám sát tiền/quỹ hằng ngày, SQL nhẹ) — 8 report
Mở suốt ngày để theo dõi dòng tiền vào/ra; lọc 1-2 TK + khoảng ngày → SQL nhẹ.

| Report (doc name) | Doctype trigger (subscribe) | Vì sao T1 |
|---|---|---|
| Cash Receipts | Payment Entry, Journal Entry | Theo dõi thu tiền mặt trong ngày |
| Cash Payments | Payment Entry, Journal Entry | Theo dõi chi tiền mặt |
| Bank Receipts | Payment Entry, Journal Entry | Tiền về tài khoản NH |
| Bank Payments | Payment Entry, Journal Entry | Chi qua NH |
| Cash Book | Payment Entry, Journal Entry | Số dư quỹ chạy realtime |
| Bank Account Book | Payment Entry, Journal Entry | Số dư NH realtime |
| So Quy Chi Nhanh | Branch Cash Entry | Thủ quỹ CN theo dõi liên tục |
| So Noi Bo | Branch Cash Entry | Giao dịch nội bộ CN trong ngày |

### TIER 2 — Toggle, mặc định TẮT (sổ chi tiết + worklist, SQL trung bình) — 8 report
Mở khi đối chiếu/xử lý tồn đọng; user tự bật khi cần.

| Report (doc name) | Doctype trigger | Vì sao T2 |
|---|---|---|
| Account Detail Ledger | Payment Entry, Journal Entry, Sales Invoice, Purchase Invoice, Stock Entry | Đối chiếu 1 TK, không liên tục |
| S03b-DN So Cai | (như trên) | Quét nhiều TK, nặng hơn |
| S03a-DN So Nhat Ky Chung | (như trên) | Toàn bộ bút toán |
| Auto Generated Docs Pending | Journal Entry | Worklist tồn đọng |
| Orphan Payments | Payment Entry, Branch Cash Entry | Worklist kiểm tra định kỳ |
| Landed Cost Pending Allocation | Purchase Invoice | Worklist phân bổ (tần suất thấp) |
| Purchase No VAT | Purchase Invoice | Kiểm tra vận hành |
| Internal Transfer | Payment Entry, Journal Entry | Chuyển quỹ, volume thấp |

> ⚠️ `Landed Cost Pending Allocation` hiện **thiếu file `.js`** → không có filter UI (lỗi sẵn có, ngoài scope FB này). Realtime vẫn gắn được; dirty-check tự bỏ qua khi thiếu filter company/date.

### TIER 3 — KHÔNG realtime (báo cáo kỳ, SQL nặng / cadence tháng-quý) — 17 report
Không có trong registry. Giữ on-demand / prepared_report.

B01-DN BCTC · B02-DN KQHDKD · B03-DN LCTT · Bang Can Doi So Phat Sinh · Trial Balance Sheet · Quyet Toan TNDN Reconciliation · Bao Cao Chi Phi Khong Duoc Tru · vat_return_01_gtgt · Project PnL Detailed · Project Cost Collection · Project Invoicing Progress · S21-DN / S21-DN So TSCD · S22-DN Theo Doi TSCD CCDC · Term Deposit Summary · Bank Loan Summary · Misa Account Conflicts.

**Lý do loại:** resolver fixpoint / tổng hợp toàn kỳ (BCTC, CĐSPS, P&L), cadence tháng/quý/năm (tờ khai VAT, quyết toán TNDN), dữ liệu đổi cực hiếm (TSCĐ, tiền gửi, khoản vay), hoặc công cụ migration one-off.

### Nguyên tắc gán tier cho report MỚI sau này
- **T1** = "tiền/quỹ + theo dõi trong ngày + lọc hẹp 1-2 TK".
- **T2** = "sổ chi tiết nhiều TK + worklist vận hành".
- **T3** = "tổng hợp toàn kỳ + cadence tháng/quý + dữ liệu đổi hiếm".

**Ngân sách:** chi phí server ≈ (số report T1 đang mở × số user) × (số lần dữ liệu nguồn đổi). Với push event-driven + debounce + dirty-check + bỏ-qua-khi-tab-ẩn, một ngày thường vài chục→vài trăm event nhẹ — chấp nhận được. Poll đại trà thì chi phí = (report mở × user) ÷ chu kỳ — đắt, chỉ dùng làm fallback chu kỳ dài (60s).

---

## 4. Các phương án

### Phương án A — Event-driven (subscribe `list_update`)
- Report page subscribe `list_update` cho các doctype nguồn của nó (PE, JE, SI, PI…).
- Khi nhận event → debounce 2-3s → `report.refresh()`.
- **Backend = 0 thay đổi** (tận dụng emission có sẵn). Client patch nhỏ + 1 bảng config "report → danh sách doctype nguồn".
- ✅ Đúng nghĩa realtime (độ trễ ~giây). ✅ Nhẹ. ❌ Phụ thuộc socket.io.

### Phương án B — Polling (`setInterval`)
- `setInterval(() => report.refresh(), N giây)`.
- ✅ Đơn giản nhất, ✅ sống cả khi socket.io chết. ❌ Re-query toàn bộ SQL mỗi N giây cho mọi client — đắt với report nặng. ❌ Không "real" time (độ trễ tới N giây).

### Phương án C — Hybrid (ĐỀ XUẤT)
- **Chính:** Phương án A (push) khi socket.io connected.
- **Fallback:** Phương án B (poll chu kỳ dài 60s) khi socket.io disconnected.
- **Tối ưu:** trước khi re-query nặng, gọi endpoint "dirty-check" rẻ trả `max(modified)` của các doctype nguồn (theo company + khoảng ngày của filter). Chỉ refresh nếu giá trị đổi → tránh chạy lại SQL khi không có gì mới (tái dụng pattern stale-check đã có ở `query_report.js:796`).
- ✅ Realtime khi mạng tốt, vẫn cập nhật khi socket.io chập chờn, ✅ chống tải bằng dirty-check. ❌ Code nhiều hơn A.

### Phương án D — Targeted push có payload (phức tạp nhất)
- Hook trên insert GL Entry/PE → `publish_realtime("vn_report_dirty", {company, date_range})` → client chỉ refresh report khớp scope.
- ✅ Kiểm soát chính xác. ❌ Thêm code backend trên **hot path** (mỗi lần ghi GL) — rủi ro hiệu năng + bảo trì. Để dành nếu A/C không đủ.

### Scorecard (trọng số: Đúng-realtime ×1.5, Tải server ×1.5, Độ phức tạp ×1, Bền khi mất socket ×1)
| Phương án | Realtime | Tải server | Đơn giản | Bền | Tổng /10 |
|---|---|---|---|---|---|
| A Event-driven | 9 | 8 | 8 | 4 | 7.6 |
| B Polling | 4 | 3 | 9 | 9 | 5.6 |
| **C Hybrid** | **9** | **9** | **6** | **9** | **8.6** |
| D Targeted push | 9 | 7 | 4 | 5 | 6.7 |

→ **Chọn C (8.6).** Khoảng cách với runner-up A (7.6) = 1.0 < 2.5 nhưng C chỉ là A cộng thêm fallback + dirty-check, không phải hướng đi khác — nên chọn C an toàn, có thể ship dần (Phase 1 = đúng phần A của C).

---

## 5. Kiến trúc phương án đề xuất (C)

### 5.1 Khai báo realtime trên report (config-driven, không hardcode)
Mỗi Script Report khai báo trong `<report>.js`:
```js
frappe.query_reports["Cash Receipts"] = {
  filters: [ /* … */ ],
  vn_realtime: {                       // ← khai báo opt-in
    source_doctypes: ["Payment Entry", "Journal Entry"],  // doctype nguồn sinh GL
    default_on: true,                  // T1 = bật mặc định; T2 = false
    debounce_ms: 2500,
  },
};
```

### 5.2 Một bundle patch chung (vn_accounting `app_include_js`)
`realtime_reports.bundle.js` patch `frappe.views.QueryReport`:
1. Khi report load + có `vn_realtime` + người dùng bật toggle:
   - `frappe.realtime.doctype_subscribe(dt)` cho từng `source_doctypes`.
   - `frappe.realtime.on("list_update", handler)` — handler lọc theo doctype nguồn, debounce, rồi gọi dirty-check → `report.refresh()`.
2. Nếu `frappe.realtime.socket?.connected === false` → bật fallback `setInterval(dirtyCheckThenMaybeRefresh, 60000)`.
3. Cleanup: hủy subscribe + clear interval khi rời route (tránh leak — xem rule jqXHR/abort + generation token).

### 5.3 Endpoint dirty-check (rẻ)
```python
@frappe.whitelist()
def report_data_fingerprint(doctypes: str, company: str, from_date: str, to_date: str) -> str:
    dts = frappe.parse_json(doctypes)
    parts = []
    for dt in dts:
        m = frappe.db.get_value(dt, {"company": company, "docstatus": 1,
              "modified": [">=", from_date]}, "max(modified)") # 1 truy vấn nhẹ, có index modified
        parts.append(f"{dt}:{m}")
    return "|".join(parts)
```
Client so sánh fingerprint cũ/mới; chỉ `report.refresh()` khi đổi. Tránh chạy lại SQL report nặng vô ích.

### 5.4 Guardrails chống quá tải (BẮT BUỘC)
- **Debounce per report** ≥ 2.5s; gộp burst (bulk import, JE nhiều dòng → 1 lần refresh).
- **Bỏ qua khi tab ẩn:** `if (document.visibilityState !== "visible") return;` — không refresh report ở tab nền.
- **Dirty-check trước re-query** (5.3) — chặn re-query khi không có dữ liệu mới.
- **Chỉ T1 auto-subscribe;** T2 cần user bật; T3 không có `vn_realtime`.
- **Tôn trọng prepared_report:** report nặng dùng background generation — không realtime.
- **Toggle UI** trên thanh report ("🔴 Realtime: Bật/Tắt") để user tự kiểm soát + thấy trạng thái kết nối.

---

## 6. Kế hoạch theo phase

| Phase | Nội dung | Effort | Phụ thuộc |
|---|---|---|---|
| **0 — Prereq** | Sửa kết nối socket.io: local (proxy/port 9002), prod (nginx `/socket.io` → socketio_port). Verify `frappe.realtime.socket.connected === true`. | 0.5 session | — |
| **1 — MVP push (T1)** | `realtime_reports.bundle.js` + `vn_realtime` config cho ~6 report T1 (Cash/Bank). Subscribe `list_update`, debounce, visibility guard. | 1 session | Phase 0 |
| **2 — Dirty-check + fallback** | Endpoint fingerprint + poll fallback 60s khi socket mất + cleanup-on-route-change. | 0.5 session | Phase 1 |
| **3 — Toggle UI + T2** | Nút bật/tắt realtime + trạng thái kết nối; mở config cho report T2 (mặc định tắt). | 0.5 session | Phase 2 |

Tổng ~2.5 session. **Có thể dừng sau Phase 1** nếu chỉ cần "report tự cập nhật" cơ bản (đúng ý FB).

---

## 7. Rủi ro & giảm thiểu
| Rủi ro | Giảm thiểu |
|---|---|
| Socket.io vẫn timeout sau Phase 0 (firewall UDP/proxy) | Fallback poll (Phase 2) đảm bảo report vẫn cập nhật; log trạng thái kết nối lên toggle UI |
| Bão refresh khi bulk import (Misa, JE nhiều dòng) | Debounce + dirty-check + `frappe.flags.in_import` đã skip `list_update` ở backend (`document.py:1419`) |
| Re-query report nặng làm chậm DB | Phân bậc T1/T2/T3 + dirty-check + chỉ refresh khi tab visible |
| Memory leak khi đổi route | Hủy subscribe + clear interval + generation token (rule "frappe.call jqXHR abort") |
| Multi-tab cùng user | Mỗi tab tự debounce; dirty-check chống re-query trùng |

---

## 8. Khuyến nghị chốt
1. **Sửa socket.io trước (Phase 0)** — đây là nguyên nhân gốc của console error trong FB, và là tiền đề.
2. **Ship Phase 1 (push cho T1)** như MVP đáp ứng FB. Nhẹ, ~1 session, backend gần như 0 thay đổi.
3. **KHÔNG realtime hóa T3 (BCTC/P&L)** — giữ on-demand, dùng prepared_report.
4. Phase 2-3 làm sau theo nhu cầu thực tế.

> **Câu hỏi cần anh quyết trước khi code:** (a) bắt đầu từ Phase 0+1 luôn, hay chỉ chốt tài liệu? (b) danh sách report T1 ở mục 3 đã đúng nhu cầu chưa? (c) có cần toggle UI ngay từ Phase 1 không?
