# SPEC — Tính năng CRM (để AI đọc và triển khai)

> **Mục đích tài liệu:** Đây là tài liệu mô tả chức năng (functional spec) dùng làm input cho AI/dev khi xây dựng hệ thống CRM. Nguồn gốc: bản tổng hợp tính năng **MISA AMIS CRM** (16 nhóm module) — được dùng làm tham chiếu nghiệp vụ, **không** bắt buộc sao chép nguyên trạng MISA.
> **Nền tảng triển khai:** ERPNext / Frappe (đã chốt ở tài liệu confirm SO trước đó). Khi có doctype ERPNext tương đương thì tái sử dụng; chỉ tạo custom doctype/custom field khi MISA có mà ERPNext không có.
> **Ngành đặc thù:** Công ty dịch vụ viễn thông (DCNET) — sản phẩm cốt lõi là **đường truyền**. Có các luồng riêng (khảo sát, đấu nối, NOC, ngắt line, tính cước) đánh dấu rõ ở mục 17.

---

## 0. Cách AI nên dùng tài liệu này

1. Đọc mục **1–3** trước để nắm bối cảnh, nguyên tắc chung và mô hình dữ liệu — áp dụng cho TẤT CẢ module.
2. Mỗi module ở mục **4** có cấu trúc cố định: `Mục tiêu` → `Thực thể/Doctype` → `Trường dữ liệu` → `Trạng thái` → `Luồng nghiệp vụ` → `Quy tắc nghiệp vụ` → `Ghi chú triển khai`.
3. Khi một trường/luồng được ghi chú **(DCNET)** → đó là yêu cầu đặc thù viễn thông, ưu tiên làm đúng.
4. Khi ghi chú **(SAU)** → tính năng phát triển ở giai đoạn sau, không thuộc MVP.
5. Mọi giả định không có trong tài liệu → **hỏi lại**, không tự bịa ra nghiệp vụ.

---

## 1. Bối cảnh & nền tảng

- Hệ thống quản lý toàn bộ vòng đời khách hàng: **Lead → Cơ hội → Báo giá/PAKD → Hợp đồng → Đơn hàng → Doanh thu → Chăm sóc sau bán**.
- Triển khai trên **ERPNext**, kết nối kế toán (đã thay MISA AMIS Kế toán bằng ERPNext Accounts trong dự án này).
- Tích hợp dự kiến: Kế toán (native trong ERPNext), HRMS (nhân sự), Dự án/Công việc, Zalo OA.
- Đối tượng người dùng: nhân viên kinh doanh (KD), phòng thực hiện (P.TH), quản lý, kế toán, NOC (vận hành mạng).

## 2. Nguyên tắc chung (áp dụng mọi module)

| Nguyên tắc | Mô tả |
|---|---|
| CRUD chuẩn | Mọi thực thể chính hỗ trợ Tạo / Xem / Sửa / Xóa. |
| **Xóa mềm (soft delete)** | Không xóa cứng dữ liệu — đánh dấu trạng thái xóa, giữ lịch sử. |
| Trường bắt buộc | Validate các trường bắt buộc trước khi lưu. |
| **Phân quyền theo phạm vi** | Xem/sửa/xóa theo: của bản thân / của nhóm được chia sẻ / phòng ban / toàn công ty. |
| **Share (dùng chung)** | Bản ghi có thể được chia sẻ cho người/nhóm khác (trường "dùng chung"). |
| Lịch sử & timeline | Mọi thực thể chính có dòng thời gian tương tác (gọi, email, ghi chú, hoạt động). |
| Bộ lọc lưu được | Tìm kiếm nâng cao đa điều kiện; cho phép lưu bộ lọc để tái sử dụng. |
| Import/Export Excel | Nhập hàng loạt từ `.xlsx/.csv` theo mẫu chuẩn; tự kiểm tra trùng lặp và báo lỗi trước khi import. |
| Đính kèm tài liệu | Cho phép đính kèm file/ảnh vào bản ghi và ghi chú. |

## 3. Mô hình dữ liệu tổng quan

```
Lead ──(chuyển đổi)──> Customer + Contact
                         │
                         ├── Opportunity (Cơ hội KD) ──> Quotation (Báo giá)
                         │                            └─> PAKD (Phương án KD)
                         │                                   ├──> Contract (Hợp đồng / PLHĐ)
                         │                                   └──> Commission (Hoa hồng)
                         │
                         ├── Sales Order (Đơn hàng) ──> Invoice (Hóa đơn, ERPNext Accounts)
                         │
                         └── Account/Đường truyền (DCNET) ── 1 Khách / 1 đường truyền / 1 địa chỉ
```

Liên kết quan trọng:
- 1 Customer ↔ nhiều Contact (kèm vai trò: người quyết định / người dùng / kế toán…).
- 1 Opportunity → nhiều Báo giá / nhiều PAKD; toàn bộ báo giá liên kết về 1 cơ hội.
- 1 PAKD → 1 Hợp đồng **hoặc** 1 PAKD → nhiều Hợp đồng.
- 1 Customer → 1 đường truyền → 1 địa chỉ (mô hình DCNET).

---

## 4. Các module chức năng

### I. Quản lý Lead (Khách hàng tiềm năng)

- **Mục tiêu:** Tiếp nhận, nuôi dưỡng và chuyển đổi lead thành cơ hội/khách hàng.
- **Thực thể/Doctype:** `Lead` (ERPNext Lead, mở rộng custom field).
- **Trường dữ liệu:**
  - *Cá nhân:* xưng hô, họ tên, phòng ban, chức danh, SĐT, SĐT cơ quan, email, mã số thuế, nguồn gốc (source).
  - *Loại tiềm năng (custom select):* KH viễn thông · KH CNTT · KH hộ gia đình · KH mua bán thi công · KH mua bán.
  - *Tổ chức:* quốc gia, địa chỉ, mô tả, thông tin ngân hàng.
  - *Hệ thống:* dùng chung (share).
- **Trạng thái:** Mới → Đang chăm sóc → Đã chuyển đổi / Mất (Disqualify).
- **Luồng nghiệp vụ:**
  1. Tạo lead thủ công hoặc import Excel (tối đa 5.000 dòng/lần) hoặc từ form/landing page.
  2. Phân loại & gán nhãn (Hot/Warm/Cold, theo nguồn, theo sản phẩm).
  3. Phân công cho NV (thủ công hoặc tự động: vòng tròn / theo khu vực / theo nhóm SP / theo tải) — **tạo công việc đi kèm khi phân công**.
  4. Chuyển đổi Lead → Cơ hội và/hoặc Customer **chỉ bằng một thao tác, giữ nguyên toàn bộ lịch sử**.
  5. Nếu không theo đuổi → ghi **Lý do mất** (sai đối tượng / không ngân sách / chọn đối thủ…) phục vụ báo cáo chất lượng lead.
- **Quy tắc nghiệp vụ:** Chuyển đổi không được mất dữ liệu. Import phải dò trùng trước khi ghi.
- **Ghi chú triển khai:** Chi tiết lead có tab: ghi chú, tài liệu, hàng hóa quan tâm, lịch sử giao dịch. Danh sách có bộ lọc (của bản thân / nhóm chia sẻ / đã chuyển đổi).

### II. Quản lý Liên hệ (Contact)

- **Mục tiêu:** Quản lý người liên hệ gắn với khách hàng.
- **Thực thể:** `Contact`.
- **Tính năng:** CRUD; import Excel; bộ lọc (tên, bộ phận, của bản thân, của nhóm).
- **Chi tiết liên hệ — các tab:** chi tiết · ghi chú · tài liệu đính kèm · hàng hóa đã mua · cơ hội · đơn hàng · báo giá · hóa đơn · công việc · email/SMS · nội dung trao đổi.
- **Hành động nhanh:** Nút **"Sinh cơ hội (báo giá / đơn hàng)"** ngay trên chi tiết liên hệ.

### III. Quản lý Khách hàng (Customer / Account)

- **Mục tiêu:** Hồ sơ khách hàng 360°.
- **Thực thể:** `Customer` (ERPNext).
- **Trường/khối thông tin:** thông tin DN/cá nhân, địa chỉ, MST, ngành nghề, người liên hệ, lịch sử giao dịch, công nợ.
- **Tính năng:**
  - Phân loại cá nhân / doanh nghiệp (B2B & B2C); liên kết contact với tổ chức.
  - Phân nhóm (VIP/tiềm năng/thường xuyên) + gán nhãn tùy chỉnh không giới hạn.
  - Import/Export; tự dò trùng.
  - Tab **Bán hàng:** đơn hàng, trả lại hàng bán, cơ hội, báo giá, hóa đơn, hàng hóa đã mua, đại lý/công ty con — lấy từ phân hệ Kế toán.
  - **Lịch sử tương tác** (timeline toàn diện: gọi, email, Zalo, ghi chú, lịch hẹn, hỗ trợ).
  - **Quản lý nhiều Contact/1 account**, kèm vai trò.
  - **Theo dõi công nợ** (số nợ, hạn thanh toán, lịch sử) — đồng bộ từ Kế toán.
  - Phân quyền theo NV phụ trách/phòng ban/vùng.
  - Tìm kiếm & lọc nâng cao; lưu bộ lọc.
  - **Nhắc nhở chăm sóc định kỳ** (tuần/tháng/quý) — kết hợp Workflow.
  - **Gộp/Merge** khách hàng trùng, giữ toàn bộ lịch sử.
  - Tab **Hoạt động** gắn theo từng khách hàng, giao việc theo NV/phòng ban.

### IV. Quản lý Cơ hội kinh doanh (Opportunity / Deal)

- **Mục tiêu:** Quản lý deal theo pipeline, dự báo doanh thu.
- **Thực thể:** `Opportunity` (ERPNext).
- **Trường:** liên kết khách hàng, sản phẩm/dịch vụ quan tâm, giá trị ước tính, ngày dự kiến chốt; sản phẩm kèm số lượng/đơn giá/chiết khấu.
- **Trạng thái pipeline (mặc định, cấu hình được):** Tiếp cận → Tư vấn → Báo giá → Đàm phán → Chốt (Thắng/Thua).
- **Luồng DCNET (quan trọng):** `KD lập yêu cầu → P.TH check thông tin → thực hiện khảo sát → KD báo giá cho KH → Kết thúc Thắng/Thất bại`. **(DCNET)**
- **Tính năng:**
  - Tạo từ Lead hoặc tạo trực tiếp.
  - Chi tiết gồm tab: tổng quan · chi tiết · hàng hóa · liên hệ · bán hàng · hoạt động · trao đổi.
  - Pipeline Kanban kéo-thả giữa các giai đoạn; **tùy chỉnh số lượng/giai đoạn** và xác suất thắng tương ứng.
  - **Dự báo doanh thu (Forecast):** giá trị × xác suất thắng, tổng hợp theo tháng/quý/năm.
  - Tạo **Báo giá từ Cơ hội** (một cú nhấp, không nhập lại).
  - Ghi **Lý do Thắng/Thua** (Win/Loss).
  - Nhắc nhở **thời hạn chốt deal** (gần/quá hạn) qua email/app.
  - Phân quyền theo NV/nhóm/phòng ban.
  - Báo cáo Pipeline & phễu bán hàng (funnel + tỷ lệ chuyển đổi).

### V. Quản lý Hoạt động (Activity)

- **Mục tiêu:** Quản lý mọi tương tác và công việc.
- **Tính năng:**
  - **Task:** tạo/giao/theo dõi, gắn vào KH/cơ hội/hợp đồng; trạng thái Chưa làm / Đang làm / Hoàn thành; hỗ trợ sub-task.
  - **Lịch hẹn/Cuộc họp:** lịch ngày/tuần/tháng, mời tham gia, ghi kết quả; nhắc trước 15–30 phút.
  - **Call Log:** kết quả gọi (đã liên hệ / không nghe / hẹn gọi lại); ghi âm nếu tích hợp tổng đài; Click-to-call.
  - **Note:** ghi chú nhanh, đính kèm file/ảnh, định dạng văn bản.
  - **Email trong CRM:** gửi/nhận, lịch sử, kết nối Gmail/Outlook, theo dõi tỷ lệ mở.
  - **Nhắc nhở tự động** qua app/email/SMS.
  - Đồng bộ Google/Outlook Calendar hai chiều **(SAU)**.
  - Xem lịch theo nhóm (tùy quyền).
  - **Activity Timeline** tổng hợp toàn bộ tương tác.

### VI. Quản lý Sản phẩm & Dịch vụ

- **Thực thể:** `Item` (ERPNext).
- **Tính năng:** danh mục SP/DV (mã, tên, mô tả, ĐVT, hình ảnh, trạng thái); phân loại theo cây danh mục nhiều cấp; **quản lý nhiều bảng giá** (niêm yết/đại lý/VIP, đa tiền tệ); chiết khấu & khuyến mãi (theo %/số tiền/số lượng); import Excel; **liên kết tồn kho** từ Kế toán để kiểm tra khả năng giao hàng.
- **(DCNET):** "Đường truyền" là một loại Item dịch vụ — xem mục 17.

### VII. Báo giá & Đơn hàng

**Báo giá (`Quotation`):**
- Tạo báo giá có template (logo, thông tin công ty, bảng SP, điều khoản TT, hiệu lực).
- **Quy trình phê duyệt nhiều cấp** (NV → trưởng nhóm → giám đốc), tự thông báo người duyệt.
- Trạng thái: **Nháp → Chờ duyệt → Đã gửi → Khách xem → Chấp nhận / Từ chối**.
- Chuyển **Báo giá → Đơn hàng** một thao tác.
- Lưu **lịch sử phiên bản**, so sánh khác biệt.

**Đơn hàng (`Sales Order`):**
- Trạng thái: Mới → Đang xử lý → Đang giao → Hoàn thành / Hủy.
- **Đồng bộ Kế toán:** khi hoàn thành → tự tạo hóa đơn, ghi nhận doanh thu (ERPNext Accounts).
- Tạo đơn: kế thừa từ báo giá hoặc tạo mới.
- **Luồng DCNET:** `P.TH → đơn hàng → chọn hàng hóa → tạo` (hàng hóa đi kèm với **Account/đường truyền** nếu là loại hình dịch vụ). **(DCNET)**
- **Mapping trường MISA → ERPNext của Sales Order:** xem tài liệu confirm riêng (`2026-06-15-confirm-so-crm`). Các trường cần thêm Custom Field đã liệt kê ở đó — chỉ thêm trường nào khách xác nhận "Có dùng".

### VIII. Quản lý Hợp đồng (Contract)

- **Thực thể:** `Contract` (ERPNext, mở rộng).
- **Trạng thái vòng đời:** Soạn thảo → Phê duyệt → Ký kết → Đang thực hiện → Kết thúc / Thanh lý.
- **Tính năng:** tạo từ mẫu (tự điền KH/giá trị/điều khoản); phê duyệt nhiều cấp; **nhắc gia hạn trước 15/30/60 ngày**; đính kèm file hợp đồng đã ký (PDF/Word/scan); quản lý giá trị & lịch thanh toán theo đợt (liên kết công nợ Kế toán); liên kết Hợp đồng ↔ Cơ hội ↔ Khách hàng.

### IX. Quản lý Phương án kinh doanh (PAKD)

> Module đặc thù, **không có sẵn trong ERPNext** → cần custom doctype `PAKD`.

- **Luồng:** `Cơ hội → PAKD → duyệt → Hợp đồng / PLHĐ → Hóa đơn`.
- **Trạng thái:** Nháp · Chờ duyệt · Đang duyệt · Đã duyệt · Từ chối · Hủy.
- **Tính năng:**
  - Tạo PAKD tương tự báo giá; chi tiết có tab: thông tin chi tiết · hàng hóa · tài liệu · đơn hàng · công việc.
  - Sửa/xóa (**xóa mềm**).
  - **Tạo Hợp đồng từ PAKD** (kế thừa thông tin).
  - **Liên kết PAKD:** 1 PAKD → 1 Hợp đồng, hoặc 1 PAKD → nhiều Hợp đồng.
  - **Clone PAKD:** khi khách không đồng ý → clone từ bản trước → đánh dấu version (lưu lịch sử) → loại: *Xin tăng / giảm giá*. Toàn bộ báo giá liên kết về một cơ hội KD.
  - Phân quyền: xem PAKD của bản thân + được chia sẻ.
  - Xem thông tin quản lý hoa hồng của NV (cá nhân / quản lý trực tiếp).
- **Luồng hoa hồng (đẩy dữ liệu tính hoa hồng từ PAKD):**
  1. PAKD được Sếp duyệt **+** Khách đồng ý → tạo **nháp hoa hồng** cho NV theo kỳ từ PAKD.
  2. Kế toán xuất hóa đơn theo kỳ.
  3. Chuyển trạng thái Nháp của hoa hồng (Nháp → có thể trả lương).
  4. Tính vào lương bổ sung theo kỳ lương.
  5. Sau khi chi trả → **đánh dấu đã chi và khóa, không sửa được**.
  - **Quy tắc:** Hoa hồng chỉ tính từ khi **bắt đầu hợp đồng VÀ khách đã thanh toán**.

### X. Marketing & Chiến dịch

- Quản lý **Campaign** đa kênh (email/SMS/Zalo/Facebook): mục tiêu, ngân sách, thời gian; dashboard hiệu quả.
- **Email Marketing** (gửi hàng loạt, template drag-and-drop, theo dõi open/click).
- **SMS Marketing** (cần tích hợp nhà cung cấp SMS).
- **Zalo ZNS** (xác nhận đơn, nhắc thanh toán, chúc mừng sinh nhật — cần Zalo OA duyệt ZNS).
- **Segmentation** động theo điều kiện lọc.
- **Landing Page & Form** thu lead không cần code, đồng bộ CRM, tích hợp Google Analytics.
- **Marketing Automation** (kịch bản: đăng ký → email chào → 3 ngày sau email SP → phân công gọi).
- Báo cáo hiệu quả chiến dịch (email gửi, open, click, lead, cơ hội, doanh thu, ROI).

### XI. Chăm sóc khách hàng (Customer Service)

- **Ticket** đa kênh (email/Zalo/điện thoại/web form): phân loại, phân công, theo dõi trạng thái.
- **Ưu tiên** (Khẩn cấp/Cao/Trung bình/Thấp) + phân loại vấn đề (kỹ thuật/thanh toán/sản phẩm).
- **SLA** theo loại & mức ưu tiên; cảnh báo sắp/vi phạm SLA.
- **Phân công** ticket tự động (theo kỹ năng/tải/ca) hoặc thủ công.
- Lịch sử hỗ trợ theo khách hàng.
- **CSAT/NPS** khảo sát sau khi đóng ticket.
- **Knowledge Base** (FAQ, hướng dẫn, quy trình xử lý lỗi).
- Báo cáo CSKH (số ticket, thời gian xử lý TB, tỷ lệ đúng hạn, CSAT theo NV/nhóm).

### XII. Báo cáo & Phân tích

- **Dashboard tổng quan** realtime (doanh số, lead mới, deal mở, tỷ lệ chốt, hiệu suất NV) — widget tùy chỉnh.
- Báo cáo: Doanh số bán hàng · Pipeline & phễu · Dự báo doanh thu · Hoạt động nhân viên · Nguồn lead & chuyển đổi · KPI mục tiêu · Win/Loss.
- Nhiều dạng biểu đồ (cột/đường/tròn/vùng/heatmap).
- **Xuất Excel/PDF**; **lên lịch gửi báo cáo tự động** (ngày/tuần/tháng).

### XIII. Nhân viên KD & Phân quyền

- Quản lý danh sách người dùng (thêm/sửa/vô hiệu hóa), phân nhóm theo phòng ban/nhóm KD/vùng — đồng bộ HRM.
- **Phân quyền theo vai trò (Role):** bộ quyền xem/tạo/sửa/xóa cho từng module.
- **Phân vùng kinh doanh (Territory):** chia theo địa lý/danh mục KH; tự phân công dữ liệu theo vùng.
- **Mục tiêu doanh số (KPI)** theo NV/nhóm theo tháng/quý/năm; theo dõi % hoàn thành realtime.
- **Leaderboard** (doanh số/deal chốt/điểm KPI; công khai/riêng tư).
- Báo cáo hiệu suất cá nhân (self-service).
- **News Feed** nội bộ.

### XIV. Tự động hóa quy trình (Workflow Automation)

- Thiết lập Workflow If/Then không cần code.
- **Trigger:** tạo record / đổi trạng thái / đến ngày / nhận email / điền form.
- Hành động tự động: phân công, gửi email/thông báo, cập nhật dữ liệu, tạo task, nhắc thời hạn.
- **Drip Email** nuôi dưỡng lead theo lịch.

### XV. Kết nối nội bộ (Tích hợp phân hệ)

- **Kế toán:** đồng bộ 2 chiều — đơn hàng CRM → hóa đơn; công nợ/tồn kho → CRM. (Trong dự án này dùng **ERPNext Accounts** thay MISA Kế toán.)
- **HRMS:** đồng bộ nhân viên/cơ cấu tổ chức; nhân viên nghỉ → dữ liệu KH tự chuyển giao.
- **Dự án/Công việc:** hợp đồng ký → tự tạo dự án triển khai, liên kết KH/hợp đồng/dự án (phù hợp công ty dịch vụ/IT).

### XVI. Kết nối nền tảng ngoài

- **Zalo OA:** thu lead từ form Zalo, gửi ZNS, chat 2 chiều trong CRM.

---

## 17. Đặc thù viễn thông — DCNET (BẮT BUỘC làm đúng)

> Đây là phần khác biệt lớn nhất so với CRM thông thường. AI phải tuân thủ chính xác.

### 17.1. Account / Đường truyền
- **`Account`** = bản ghi quản lý **đường truyền** — chính là sản phẩm dịch vụ của công ty.
- Mô hình ràng buộc: **1 Khách hàng / 1 đường truyền / 1 địa chỉ**.
- CRUD Account; khi tạo đơn hàng loại hình dịch vụ → hàng hóa **đi kèm với Account**.
- Trường đặc thù cần xác nhận (tham chiếu tài liệu confirm SO): Điểm lắp đặt **A-End**, Điểm lắp đặt **Z-End**, **Khu vực lắp đặt dịch vụ** — chỉ thêm nếu khách xác nhận có nghiệp vụ.

### 17.2. Luồng cơ hội DCNET
`KD lập yêu cầu → P.TH check thông tin → thực hiện khảo sát → KD báo giá cho KH → Kết thúc Thắng / Thất bại`

### 17.3. Luồng đơn hàng dịch vụ
`P.TH → đơn hàng → chọn hàng hóa → tạo` (hàng hóa gắn với Account/đường truyền).

### 17.4. Thanh lý dịch vụ
`Khách thanh lý → báo NOC → ngắt line → cập nhật hóa đơn → ngừng tính cước`

---

## 18. Trạng thái & enum tổng hợp (tham chiếu nhanh)

| Thực thể | Các trạng thái |
|---|---|
| Lead | Mới · Đang chăm sóc · Đã chuyển đổi · Mất (Disqualify) |
| Opportunity | Tiếp cận · Tư vấn · Báo giá · Đàm phán · Thắng · Thua *(cấu hình được)* |
| Quotation | Nháp · Chờ duyệt · Đã gửi · Khách xem · Chấp nhận · Từ chối |
| Sales Order | Mới · Đang xử lý · Đang giao · Hoàn thành · Hủy |
| Contract | Soạn thảo · Phê duyệt · Ký kết · Đang thực hiện · Kết thúc · Thanh lý |
| PAKD | Nháp · Chờ duyệt · Đang duyệt · Đã duyệt · Từ chối · Hủy |
| Commission | Nháp · Có thể trả lương · Đã chi (khóa) |
| Ticket | (theo SLA) Mới · Đang xử lý · Chờ khách · Đã giải quyết · Đóng |

---

## 19. Gợi ý ưu tiên triển khai

| Mức | Module |
|---|---|
| **MVP** | I. Lead · II. Liên hệ · III. Khách hàng · IV. Cơ hội · VII. Báo giá & Đơn hàng · XVII. Account/Đường truyền (DCNET) · Phân quyền cơ bản (XIII) |
| **Giai đoạn 2** | VIII. Hợp đồng · IX. PAKD + hoa hồng · V. Hoạt động đầy đủ · XII. Báo cáo · XIV. Workflow |
| **Giai đoạn 3** | X. Marketing · XI. CSKH · XV–XVI. Tích hợp HRMS/Dự án/Zalo |
| **(SAU)** | Đồng bộ Google/Outlook Calendar |

---

## 20. Câu hỏi mở cần xác nhận với khách trước khi code

1. Loại tiềm năng (5 loại) có cố định không, hay cần thêm/bớt?
2. Pipeline cơ hội dùng mặc định hay theo luồng DCNET (khảo sát) cho toàn bộ, hay tách theo loại hình?
3. PAKD có bắt buộc cho mọi deal hay chỉ áp dụng cho hợp đồng dịch vụ định kỳ?
4. Quy tắc tính hoa hồng (theo kỳ) — công thức cụ thể, kỳ lương như thế nào?
5. Các trường viễn thông (A-End/Z-End/khu vực lắp đặt) — xác nhận theo tài liệu confirm SO.
6. Phạm vi tích hợp kế toán: chỉ đẩy đơn hàng → hóa đơn, hay đồng bộ 2 chiều công nợ/tồn kho ngay từ MVP?

---

*Nguồn tham chiếu: bản tổng hợp tính năng MISA AMIS CRM (2025) + tài liệu confirm "Sinh đơn hàng từ CRM" (15/06/2026).*
