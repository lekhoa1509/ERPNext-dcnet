# MISA AMIS CRM — Phân tích chi tiết

> **Nguồn:** Phân tích trực tiếp từ 10 video hướng dẫn MISA AMIS CRM (Phần 1-11, tổng ~3.2 giờ)
> **Ngày phân tích:** 11/06/2026
> **Phân tích bởi:** Claude Code (frames extracted từ video, visual analysis)

---

## 1. Tổng quan sản phẩm

| Thuộc tính | Chi tiết |
|------------|---------|
| **Tên đầy đủ** | MISA AMIS Bán hàng (tích hợp CRM + Sales) |
| **Nền tảng** | MISA AMIS (SaaS cloud, Việt Nam) |
| **Mô hình** | SaaS, subscription theo user/tháng |
| **Khách hàng mục tiêu** | SME Việt Nam, B2B sales teams |
| **Mobile** | AMIS CRM 2 (iOS/Android), đầy đủ tính năng |
| **AI** | Không xuất hiện rõ trong các video CRM |
| **Website** | amis.misa.vn/amis-ban-hang |
| **Help center** | helpamis.misa.vn |

### Vị trí trong hệ sinh thái MISA AMIS

```
MISA AMIS Platform
├── AMIS Bán hàng (CRM)       ← module này
│   ├── Tiềm năng (Lead)
│   ├── Liên hệ (Contact)
│   ├── Khách hàng (Customer)
│   ├── Cơ hội (Opportunity)
│   ├── Báo giá (Quotation)
│   └── Đơn hàng (Sales Order)
├── AMIS Kế toán              ← tích hợp 2 chiều (sync)
├── AMIS aiMarketing          ← Email/SMS campaigns
└── AMIS Omnichannel          ← Social media / Zalo OA
```

### Luồng tích hợp CRM ↔ Kế toán (4 loại sync)

```
CRM                           Kế toán
Khách hàng    ←──Lấy sang──── Customer
Hàng hóa      ←──Lấy sang──── Products
Báo giá       ──Sinh từ──────► Quotation
Đơn hàng      ──Tự động sync─► Sales Order
Hóa đơn       ──Cập nhật lại── Invoice
```

---

## 2. Trụ cột chính

### 2.1 Quản lý Pipeline Bán hàng (Lead → SO)

Luồng chuẩn MISA CRM:

```
Tiềm năng (Lead)
  → Chuyển đổi (Convert)
    → Khách hàng + Liên hệ + Cơ hội
      → Báo giá
        → [Sinh] Đơn hàng
          → [Đề nghị ghi DS] → Ghi doanh số
            → [Đề nghị xuất HĐ] → Hóa đơn (in Kế toán)
```

**Trạng thái Đơn hàng:**
- Tình trạng: Chưa thực hiện / Đang thực hiện / Hoàn thành
- Tình trạng ghi doanh số: Bản nhập → Đề nghị ghi → Ghi số
- Tình trạng giao hàng: Chưa giao / Đang giao / Hoàn thành
- Tình trạng thanh toán: Chưa thanh toán / Thanh toán 1 phần / Đã thanh toán

### 2.2 Quản lý Tiềm năng (Lead) — chi tiết nhất

| Tính năng | Mô tả |
|-----------|-------|
| **40+ fields chuẩn** | Xưng hô, Tên, Chức danh, Phòng ban, ĐT (x3), Email (x2), Zalo, Tổ chức, MST, Lĩnh vực, Ngành nghề, Doanh thu, Ngày thành lập... |
| **Form Layout Editor** | Drag-and-drop, 21 loại field, cấu hình required/log/sort/gợi ý |
| **Kiểm tra trùng** | Trên trường ĐT di động, real-time |
| **3-panel list view** | Left filter + Center list + Right activity feed |
| **Bulk actions** | 13 hành động: gắn thẻ, campaign, chuyển đổi, gộp trùng, SMS, Email, in nhãn, xóa, xuất... |
| **Import Excel** | 4-bước wizard, field mapping có màu, 5.000 rows (.xlsx), không giới hạn (.csv) |
| **Nhật ký (audit log)** | Track mọi thay đổi field với before/after values |
| **Activities trên list** | Gọi, email, task — không cần mở record |

### 2.3 Form Customization Engine

| Component | Mô tả |
|-----------|-------|
| **Layout Editor** | Drag-and-drop builder, URL: `/crm/settings-layout/{DocType}/{id}` |
| **21 field types** | Một dòng, Nhiều dòng, Email, ĐT, Danh sách, Chọn nhiều, Ngày, Ngày/Giờ, Số nguyên, Số tự tăng, Tiền tệ, %, Thập phân, Số lớn, Tích chọn, URL, Tìm kiếm, Người dùng, Tìm kiếm nhiều, Bảng thông tin, Công thức |
| **Dropdown configurator** | Edit options, set default, bắt buộc, hiển thị gợi ý, log tracking, sort A-Z |
| **Custom fields** | Xuất hiện seamless với standard fields (VD: Chiến dịch MKT, Địa chỉ phòng khám) |
| **Multi-layout** | Một DocType có nhiều layout, chọn layout khi import |
| **Tất cả DocType** | Lead, Contact, Customer, Opportunity, Quote, SO đều có layout riêng |

### 2.4 Di tuyến (Field Sales Routing)

| Tính năng | Mô tả |
|-----------|-------|
| **Lộ trình** | Plan chuyến thăm khách, Mã + Tên + Ngày bắt đầu/kết thúc + Danh sách KH |
| **Lịch lặp** | Recurring schedule: "Sau mỗi 1 tuần vào Thứ 2" |
| **Lọc khách hàng** | Condition builder (Tỉnh/TP = Hà Nội) → auto-populate route |
| **GPS Tracking** | Real-time map tất cả field reps, battery %, last update time |
| **Check-in** | GPS pin + timestamp + ghi chú từ mobile |
| **Tồn kho tại điểm** | Mobile: xem tồn kho của từng khách hàng trong chuyến thăm |
| **Manager view** | Desktop: "Chưa ghé thăm" / "Đã ghé thăm (N)" per rep + map pins |

### 2.5 Print Template System

- **Cơ chế:** Excel file với `##Module.Field##` merge field syntax
- **Per-module:** Mỗi DocType có template riêng (Báo giá, Đơn hàng...)
- **Multi-template:** Nhiều template per DocType, chọn khi in
- **Field reference:** File Excel mapping tên field → token (VD: `##Bao gia.Khach hang##`)
- **Upload:** Thiết lập > Mẫu, max 5MB, có "Dùng chung" flag

---

## 3. Tích hợp

| Ứng dụng | Loại tích hợp | Data đồng bộ |
|----------|--------------|-------------|
| **AMIS Kế toán** | 2 chiều, bi-directional sync | KH, Hàng hóa, Báo giá, ĐH, HĐ, Chứng từ bán hàng |
| **AMIS aiMarketing** | Push data | Leads, Customers → campaigns |
| **AMIS Omnichannel** | Pull data | Zalo OA, Mạng xã hội → Leads |
| **Tổng đài điện thoại** | Click-to-call | Gọi trực tiếp từ Lead/KH form |
| **SMS Brandname** | Push | Gửi SMS từ list hoặc automation |
| **Email** | Gmail integration | Sync email history per record |
| **Facebook** | Social lead capture | Mạng xã hội tab |
| **AMIS.VN** | SSO + user sync | "Lấy dữ liệu AMIS.VN" members |
| **WebForms** | Embed | Landing page → Lead capture |
| **API** | REST | Dành cho nhà phát triển |

---

## 4. Báo cáo & Dashboard

### Dashboard Ban quản trị (4 KPI + 5 charts)

| KPI Card | Dữ liệu |
|----------|---------|
| Số lượng đơn hàng | Count + % change vs kỳ trước |
| Doanh số đặt hàng | Value + % change |
| Số lượng đã ghi nhận | Count confirmed revenue |
| Doanh số đã ghi nhận | Value confirmed revenue |

**Charts:** Funnel cơ hội theo giai đoạn | Tăng trưởng đơn hàng | Tăng trưởng KH | Doanh số theo thời gian | Mục tiêu doanh số

### Catalog báo cáo (20+ reports)

| Nhóm | Báo cáo |
|------|---------|
| **Cơ hội** | Phân tích nguồn gốc, Lý do thua, Theo loại HH, Theo thị trường, Tiến độ, Chuyển giai đoạn |
| **Đơn hàng** | Theo KH, Chi tiết theo HH, Được ghi nhận, Theo loại ĐH, Theo Đơn vị/NVKD |
| **Nhân viên** | Năng lực nhân viên |
| **Mục tiêu** | Tình hình thực hiện theo loại HH |
| **Khách hàng** | Thống kê theo thị trường |
| **Kho** | Tồn kho & đơn chưa giao, Tình hình thực hiện ĐĐH |

**Mỗi report:** Tham số lọc (chi nhánh, ngày, nhóm HH, kho), Export, date shown last run

---

## 5. Quản lý chất lượng & Automation

| Tính năng | Mô tả |
|-----------|-------|
| **Quy trình bán hàng** | Custom sales pipeline stages |
| **Quy trình làm việc** | Workflow automation rules |
| **Quy trình phê duyệt** | Multi-level approval for Quotation/SO |
| **Quy tắc phân bổ** | Auto-assign Lead/Opportunity to rep |
| **Quy tắc chấm điểm** | Lead scoring rules |
| **Quy trình ghi doanh số** | Revenue recognition workflow |
| **Bàn giao công việc** | Offboarding: transfer all tasks/records |
| **Nhật ký truy cập** | User access audit log |
| **Thùng rác** | Soft delete with restore |

---

## 6. Ưu điểm

1. **Pipeline hoàn chỉnh** — Lead → SO → Invoice trong 1 hệ thống, không cần chuyển app
2. **Form customization mạnh** — Visual drag-drop builder, 21 field types, per-DocType layout
3. **Import Excel thông minh** — Color-coded field mapping, owner assignment rules, 5K row limit
4. **Di tuyến độc đáo** — GPS tracking + recurring schedule + mobile check-in là differentiator mạnh cho field sales Việt Nam
5. **Tri-pane list view** — Filter panel + List + Activity feed cùng lúc = UX vượt trội so với standard list
6. **Kế toán native** — Sync 2 chiều với AMIS Kế toán, không cần middleware, data real-time
7. **Nhật ký chi tiết** — Mọi field change đều tracked với before/after values
8. **Print template Excel** — Kế toán/sales VN quen Excel, approach này rất phù hợp thị trường
9. **Mobile đầy đủ** — Full CRM trên mobile, không phải app lite
10. **Bulk actions phong phú** — 13 hành động batch, bao gồm gộp trùng và in nhãn thư

---

## 7. Nhược điểm / Hạn chế

1. **SaaS lock-in** — Không on-premise, data ở cloud MISA, không phù hợp doanh nghiệp cần data sovereignty
2. **Tích hợp ngoài hệ sinh thái khó** — Chủ yếu tích hợp AMIS apps; kết nối ERP khác phức tạp
3. **Print template phức tạp** — `##Module.Field##` syntax cần Excel skill, khó với user thường
4. **Pricing không minh bạch** — Không hiển thị giá công khai, cần liên hệ sales
5. **Phụ thuộc Internet** — SaaS thuần, không offline mode (quan trọng với field sales vùng sâu)
6. **Di tuyến chưa có route optimization** — Chỉ plan thủ công, không tự tính đường ngắn nhất
7. **Report không customizable** — Catalog cố định 20 reports, không có ad-hoc report builder
8. **Duplicate check hạn chế** — Chỉ trên phone field, không cross-field dedup

---

## 8. Mapping vs ERPNext

| # | Tính năng MISA CRM | ERPNext Equivalent | Gap | Ghi chú |
|---|-------------------|-------------------|-----|---------|
| 1 | Tiềm năng (Lead) list + form | CRM Lead | ✅ | ERPNext Lead đủ fields cơ bản |
| 2 | Liên hệ (Contact) | Contact | ✅ | Đầy đủ |
| 3 | Khách hàng (Customer/Account) | Customer | ✅ | Đầy đủ |
| 4 | Cơ hội (Opportunity) + funnel stages | Opportunity | ✅ | ERPNext có stages tùy chỉnh |
| 5 | Báo giá (Quotation) | Quotation | ✅ | Đầy đủ |
| 6 | Đơn hàng (Sales Order) | Sales Order | ✅ | Đầy đủ |
| 7 | Hàng hóa (Product) với multi-price | Item + Pricing Rule | ✅ | ERPNext Pricing Rule mạnh hơn |
| 8 | Chuyển đổi Lead → KH + Cơ hội | CRM Lead → Customer (tự động) | ✅ | Built-in conversion |
| 9 | Báo giá → Sinh Đơn hàng | Quotation → Make Sales Order | ✅ | Built-in |
| 10 | Phê duyệt Quotation/SO | Document Workflow | ✅ | ERPNext workflow engine |
| 11 | Quy tắc phân bổ (assignment rules) | Assignment Rule | ✅ | Built-in |
| 12 | Kanban view | Kanban View | ✅ | Built-in trên bất kỳ DocType |
| 13 | Tích hợp Kế toán (CRM ↔ Accounting) | Native (1 hệ thống) | ✅ | **ERPNext tốt hơn** — cùng DB, không cần sync |
| 14 | Tồn kho lookup từ Activity | Stock Ledger query | ✅ | Custom script đơn giản |
| 15 | Email gửi từ record | Email từ CRM | 🔶 | Cần cấu hình email account |
| 16 | SMS gửi từ record | SMS via integration | 🔶 | Cần SMS gateway (Twilio/VNPT) |
| 17 | Saved filters trên list | List View filter lưu | 🔶 | ERPNext có nhưng UX kém hơn |
| 18 | Activity feed panel (right panel) | Timeline trên form | 🔶 | ERPNext timeline ở trong form, không trên list view |
| 19 | Tri-pane list view (filter+list+feed) | 2-pane list | 🔶 | Cần custom JS để thêm right panel |
| 20 | Nhật ký field-level (audit log) | Document Version History | 🔶 | ERPNext có nhưng ít chi tiết hơn (toàn record, không per-field) |
| 21 | Print template (Excel merge) | Jinja Print Format | 🔶 | ERPNext dùng Jinja HTML, không phải Excel |
| 22 | Custom form layout builder (visual) | Form Customization Tool | 🔶 | ERPNext có nhưng không phải drag-drop visual builder |
| 23 | Import Excel wizard (field mapping UI) | Data Import Tool | 🔶 | ERPNext Data Import có nhưng UX kém hơn (no color-coded mapping) |
| 24 | Bulk actions phong phú (13 actions) | List View bulk actions | 🔶 | ERPNext có nhưng chỉ ~5 actions chuẩn |
| 25 | Kiểm tra trùng (phone real-time) | Duplicate Alert | 🔶 | ERPNext có Duplicate Alert nhưng không real-time inline |
| 26 | Quy tắc chấm điểm (Lead scoring) | — | ❌ | Không có trong ERPNext chuẩn |
| 27 | Di tuyến (Field Sales Routing) | — | ❌ | Hoàn toàn không có, cần build mới |
| 28 | GPS Employee Tracking (real-time map) | — | ❌ | Không có, cần tích hợp Google Maps API |
| 29 | Mobile check-in với GPS | — | ❌ | Frappe Mobile không có check-in |
| 30 | Recurring visit schedule (lặp lại) | — | ❌ | Không có concept này trong ERPNext |
| 31 | Tồn kho per-khách hàng trong di tuyến | — | ❌ | Custom feature của MISA |
| 32 | Mạng xã hội (Facebook/Zalo lead capture) | — | ❌ | Cần tích hợp riêng |
| 33 | Email Marketing (campaigns) | Email Campaign | 🔶 | ERPNext có nhưng basic hơn |
| 34 | Catalog 20+ sales reports chuẩn | CRM Reports | 🔶 | ERPNext có ~10 CRM reports, thiếu một số loại phân tích |
| 35 | WebForms (landing page → lead) | Web Form | ✅ | ERPNext Web Form đủ dùng |
| 36 | Bàn giao công việc (offboarding) | — | ❌ | Cần custom: reassign all records/tasks khi NV nghỉ |
| 37 | CRM User permissions (org tree) | User Permission (DocType-level) | 🔶 | ERPNext User Permission mạnh hơn nhưng UX khác |
| 38 | Quy trình ghi doanh số | — | ❌ | Concept VN-specific: "ghi doanh số" = revenue recognition step trước invoice |

### Tổng kết gap

| Level | Số lượng | % |
|-------|----------|---|
| ✅ Available | 14 | 37% |
| 🔶 Partial | 14 | 37% |
| ❌ Full gap | 10 | 26% |
| ➖ N/A | 0 | 0% |

**Kết luận:** ERPNext covers ~74% features (Available + Partial). 10 features cần build mới, trong đó **Di tuyến** là complex nhất.

---

## 9. Modules vệ tinh

| Module vệ tinh | Tên trong MISA | ERPNext equivalent | Vai trò |
|----------------|---------------|-------------------|---------|
| Hệ thống tổ chức | Hệ thống > Cơ cấu tổ chức (9 cấp) | Company + Department (tree) | Phân quyền theo đơn vị, routing đơn hàng |
| Nhân viên | Hệ thống > Thành viên → AMIS.VN | Employee + User | Master data cho assignment, tracking |
| Hàng hóa | Hàng hóa (multi-price tier) | Item + Item Price + Pricing Rule | Báo giá, đơn hàng |
| Kế toán | AMIS Kế toán (separate app) | ERPNext Accounting (same app!) | Chứng từ, hóa đơn, công nợ |
| Kho | Tồn kho lookup (AMIS Kế toán side) | Stock Ledger / Bin | Kiểm tra tồn kho khi bán hàng |
| Email Marketing | AMIS aiMarketing (separate app) | Email Campaign | Campaigns từ Lead/Customer list |
| SMS | SMS Brandname (separate app) | SMS integration | Bulk SMS, workflow trigger |
| Mạng xã hội | AMIS Omnichannel (separate app) | — (cần build) | Lead từ Facebook/Zalo |
| Mục tiêu | Mục tiêu (built-in CRM) | Sales Person + Target | KPI sales rep và team |
| Chiến dịch | Chiến dịch (built-in) | Campaign | Gắn Lead/SO vào marketing campaign |

---

## 10. Bài học áp dụng cho DCNET Flow

### UX/UI Lessons

1. **Tri-pane list view** — Thêm right panel hiển thị activity feed ngay trên list, không cần mở form. Implement bằng custom JS frappe.listview_settings trong client script. High impact, medium effort.

2. **Inline action icons per row** — Phone/Email/Calendar icons trên mỗi row (hover visible). ERPNext đã có quick actions, cần enable + style.

3. **Bulk action contextual toolbar** — Khi select rows, toolbar thay đổi context. ERPNext list view có, cần thêm custom actions (merge, campaign assign).

4. **Import wizard UX** — Color-coded field mapping (xanh = matched, cam = chưa map) giúp user không bị nhầm. Custom Data Import page cho DCNET.

5. **Activity feed không cần mở form** — MISA cho phép log call/task/note ngay từ list view right panel. Giảm friction đáng kể cho sales rep.

### Workflow Design Lessons

6. **Lead → Convert → (KH + Liên hệ + Cơ hội) trong 1 bước** — ERPNext CRM đã làm điều này, cần giữ nguyên và không over-customize.

7. **"Ghi doanh số" workflow riêng biệt** — MISA tách bước này vì kế toán VN cần confirm doanh số trước khi xuất hóa đơn. Cần implement: SO → Đề nghị ghi → Ghi → Đề nghị HĐ. Map sang ERPNext: có thể dùng Custom Workflow trên Sales Order.

8. **Đề nghị xuất hóa đơn** — Tạo 1 intermediary form giữa Sales Order và Invoice, để sales team request, kế toán approve và xuất. Cần build Custom DocType "Invoice Request" hoặc dùng SO workflow.

9. **Recurring visit schedule cho Di tuyến** — Lịch lặp lại theo tuần/tháng. Nếu DCNET cần Di tuyến, implement bằng Calendar Event recurring + custom Route DocType.

### Integration Lessons

10. **ERPNext có lợi thế hơn MISA** — CRM và Kế toán cùng 1 database = không cần sync, real-time, không conflict. Đây là điểm bán hàng mạnh nhất của DCNET Flow vs MISA.

11. **Print template approach** — Thay vì Jinja thuần, cân nhắc cho phép upload Excel template (dùng python-docx hoặc xlsxwriter). User VN rất quen Excel format. Medium effort, high user satisfaction.

12. **WebForms cho lead capture** — ERPNext Web Form đủ mạnh, cần config đúng + styling phù hợp thương hiệu khách hàng.

### Features cần prioritize cho DCNET Flow

| Priority | Feature | Effort | Impact |
|----------|---------|--------|--------|
| ⭐⭐⭐ | Workflow "Ghi doanh số" trên Sales Order | Medium | High (đặc thù VN) |
| ⭐⭐⭐ | Import Excel wizard cải tiến (UI rõ hơn) | Medium | High |
| ⭐⭐ | Tri-pane list view (activity feed right panel) | High | High |
| ⭐⭐ | Lead scoring rules | Medium | Medium |
| ⭐⭐ | Bàn giao công việc khi NV nghỉ | Low | Medium |
| ⭐ | Di tuyến + GPS tracking | Very High | Medium (chỉ field sales) |
| ⭐ | Mạng xã hội lead capture | High | Low (có thể dùng web form) |

---

## Sources

1. **Video tutorial series** — "Hướng dẫn sử dụng AMIS CRM cơ bản" (Phần 1-11), ~3.2 giờ, phân tích trực tiếp từ 179 screenshots
2. **MISA AMIS Help Center** — helpamis.misa.vn/amis-ban-hang
3. **MISA AMIS trang chính** — amis.misa.vn/amis-ban-hang
4. **ERPNext CRM Documentation** — docs.erpnext.com/docs/user/manual/en/crm
5. **ERPNext Assignment Rules** — docs.erpnext.com/docs/user/manual/en/setting-up/automation/assignment-rule
