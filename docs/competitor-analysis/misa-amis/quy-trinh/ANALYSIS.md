# MISA AMIS Quy Trình — Phân tích chi tiết

> **Ngày phân tích:** 17/03/2026
> **Phiên bản:** v1.0
> **Người phân tích:** DCNET Team

---

## 1. Tổng quan sản phẩm

| Item | Value |
|------|-------|
| **Tên** | MISA AMIS Quy Trình |
| **Thuộc** | Nền tảng MISA AMIS (Mảng Điều hành) |
| **Platform** | SaaS (Cloud), No-code |
| **Khách hàng** | 170,000+ doanh nghiệp |
| **Giá** | ~1,000,000 - 5,000,000 VND/năm |
| **Mobile** | Có (iOS/Android) |
| **AI** | 50+ tính năng AI (voice task, auto report, AI process design) |
| **Website** | https://amis.misa.vn/amis-quy-trinh/ |

### Vị trí trong hệ sinh thái MISA AMIS

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Tài chính   │  │  Bán hàng   │  │   Nhân sự   │  │  Điều hành  │
│  (Kế toán)   │  │  (CRM)      │  │   (HRM)     │  │ (Quy trình) │
└──────┬───────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       └─────────────────┴────────────────┴────────────────┘
                    Nền tảng MISA AMIS hợp nhất
```

AMIS Quy Trình nằm trong **mảng Điều hành**, kết nối với các mảng khác (Tài chính, Bán hàng, Nhân sự) để tự động hóa quy trình xuyên suốt doanh nghiệp.

---

## 2. Ba trụ cột chính

### 2.1 Thiết kế Quy trình (Process Design)

#### No-code Process Builder
- Giao diện kéo thả (drag & drop) để thiết kế quy trình
- Không cần kiến thức lập trình
- Preview/chạy thử trước khi phát hành

#### Thư viện mẫu quy trình
- **500+ mẫu quy trình** sẵn có, phân loại theo:
  - Ngành nghề (sản xuất, thương mại, dịch vụ...)
  - Phòng ban (HC-NS, Kế toán, Kinh doanh, IT...)
  - Loại quy trình (phê duyệt, báo cáo, yêu cầu...)
- Có thể clone template → tùy chỉnh theo nhu cầu

#### Form Builder
- Tạo biểu mẫu nhập liệu tùy chỉnh cho mỗi bước
- **Field types:** Text, số, ngày tháng, chọn giá trị (dropdown/radio), file đính kèm, bảng (table), checkbox, rich text
- **Điều kiện trường (Field Conditions):**
  - Logic AND/OR để show/hide fields
  - Thay đổi danh sách giá trị dựa trên điều kiện
  - Validate input theo rules

#### Quản lý phiên bản (Version Control)
- Đánh phiên bản tùy ý (VD: "3782", "5.6.1", "HC2.6") — không bắt buộc sequential
- Lịch sử đầy đủ tất cả phiên bản
- Khôi phục phiên bản cũ
- **Phân biệt 2 loại phiên bản:**
  - **Quy trình thực thi:** Phiên bản đang chạy (production)
  - **Tài liệu quy trình:** Phiên bản tài liệu tham khảo (documentation)

#### Chạy thử (Test Run)
- Test quy trình trước khi phát hành chính thức
- Kiểm tra flow, điều kiện, phân quyền

---

### 2.2 Thực thi Quy trình (Process Execution)

#### Loại bước (Step Types)

| Loại | Mô tả | Hành động |
|------|-------|-----------|
| **Bước phê duyệt** | Xem xét thông tin → quyết định | Đồng ý / Từ chối |
| **Bước thực hiện** | Nhập/xử lý thông tin → chuyển tiếp | Chuyển tiếp / Trả về |
| **Bước song song** | Nhiều bước chạy đồng thời | Từ bước thứ 3 trở đi |
| **Rẽ nhánh** | Điều kiện → đi theo nhánh tương ứng | Tự động theo condition |

#### Loại người thực hiện (Executor Types)

| # | Loại | Mô tả |
|---|------|-------|
| 1 | **Người dùng tự chọn** | Người tạo lượt chạy chọn ai thực hiện |
| 2 | **Nhóm trong ứng dụng** | Assign cho 1 nhóm, ai trong nhóm cũng có thể xử lý |
| 3 | **Người thực hiện bước trước** | Tự động gán cho người đã làm bước trước đó |
| 4 | **Quản lý trực tiếp** | Lấy từ cơ cấu tổ chức HR → gán cho manager |
| 5 | **Vị trí / Nhóm vị trí / Chức danh** | Gán theo job position hoặc job title |

#### Hành động người dùng

| Hành động | Áp dụng | Mô tả |
|-----------|---------|-------|
| **Đồng ý** | Bước phê duyệt | Phê duyệt và chuyển tiếp |
| **Từ chối** | Bước phê duyệt | Từ chối, có thể kết thúc hoặc trả về |
| **Chuyển tiếp** | Bước thực hiện | Hoàn thành bước, chuyển sang bước tiếp |
| **Trả về** | Bước thực hiện | Trả lại bước trước để sửa/bổ sung |
| **Comment** | Tất cả | Ghi chú, trao đổi |
| **Đính kèm file** | Tất cả | Upload tài liệu bổ sung |
| **Thu hồi (Recall)** | Người tạo | Thu hồi lượt chạy khi phát hiện lỗi |
| **Chuyển giao (Reassign)** | Người được gán | Chuyển cho người khác thực hiện |
| **Hủy bỏ** | Người có quyền | Hủy toàn bộ lượt chạy |

#### Trạng thái lượt chạy (Run Status)

```
                    ┌──────────────┐
                    │  Đang thực   │
         ┌────────►│    hiện      │────────┐
         │          └──────┬───────┘        │
         │                 │                │
    [Khởi tạo]      [Hoàn thành]    [Từ chối/Hủy]
         │                 │                │
         │          ┌──────▼───────┐  ┌─────▼──────┐
         │          │  Hoàn thành  │  │ Bị từ chối │
         │          └──────────────┘  └────────────┘
         │                            ┌────────────┐
         │                            │  Bị hủy    │
         │                            └────────────┘
```

---

### 2.3 Tự động hóa (Automation)

#### 3 loại Trigger

| Trigger | Mô tả | Ví dụ |
|---------|-------|-------|
| **Định kỳ** | Theo lịch (ngày/tuần/tháng) | Tổ chức sự kiện tổng kết hàng tháng |
| **Điều kiện từ app khác** | Khi event xảy ra ở HR/Payroll/... | Tiếp nhận nhân sự mới → chạy quy trình onboarding |
| **Cập nhật trường** | Khi field thay đổi giá trị | Tick "Đăng bài" → auto post lên mạng XH |

#### Quy trình liên kết (Linked Processes)

- **Khi hoàn thành lượt chạy** → tự động khởi tạo quy trình tiếp theo
  - VD: Hoàn thành "Đề xuất mua hàng" → tự động chạy "Phê duyệt thanh toán"
- **Khi hoàn thành 1 bước** → chạy quy trình con
  - VD: Bước "Kiểm tra kho" hoàn thành → chạy quy trình "Xuất kho"

---

## 3. Tích hợp (Integration)

| Tích hợp | Chi tiết |
|----------|---------|
| **AMIS Kế toán** | Thanh toán, quyết toán, chứng từ kế toán |
| **AMIS HRM** | Thông tin nhân sự, cơ cấu tổ chức, chức danh |
| **AMIS Lương** | Phê duyệt bảng lương |
| **AMIS WeSign** | Ký số điện tử theo bước quy trình |
| **AMIS Mạng XH nội bộ** | Auto đăng bài thông báo |
| **Open API** | REST API với OAuth (Client ID/Secret) |

### Open API

- **Authentication:** Client ID + Client Secret (OAuth)
- **Data fields khả dụng:**
  - Employee: name, code, email, position, department
  - Organization: cơ cấu tổ chức
  - Job positions: vị trí công việc
- **Hạn chế:** Chỉ expose employee/org data, KHÔNG expose full process model hay process instances

---

## 4. Báo cáo & Dashboard

### Dashboard tổng quan
- Cho lãnh đạo: overview tình hình thực hiện quy trình
- Cho QA: theo dõi compliance, bottleneck

### Báo cáo tự tạo (4 bước)

1. **Lấy dữ liệu:** Lọc theo quy trình, trạng thái, thời gian, người tạo, phòng ban
2. **Tạo bảng tính:** 1 chiều hoặc 2 chiều, tổng, nhóm theo tháng/quý/năm
3. **Tạo biểu đồ:** Cột dọc/ngang, cột chồng, tròn, đường
4. **Chia sẻ:** Tất cả / có quyền / cá nhân / vị trí / nhóm

### Export
- Excel (bảng tính hoặc bảng dữ liệu)

---

## 5. Quản lý chất lượng (QA/Compliance)

- **Soạn thảo & ban hành tài liệu quy trình:** Lưu trữ tập trung, phân quyền xem/sửa
- **Quản lý sự không phù hợp:** Nhân viên report → QA xử lý → tracking
- **Yêu cầu viết/sửa quy trình:** Workflow riêng cho QA team
- **Audit trail:** Lịch sử phiên bản đầy đủ, ai làm gì, khi nào

---

## 6. Ưu điểm

1. **No-code, dễ dùng** cho business users (không cần dev)
2. **500+ template** sẵn có, tiết kiệm thời gian setup
3. **Tích hợp sâu** với hệ sinh thái MISA (kế toán, HR, CRM, lương)
4. **Phù hợp văn hóa doanh nghiệp VN** (thuật ngữ, flow, compliance VN)
5. **Mobile app** đầy đủ tính năng
6. **AI-powered** (50+ tính năng: voice task, auto report, AI process design)
7. **WeSign** tích hợp ký số điện tử
8. **Giá cả phải chăng** cho SME Việt Nam (~1-5M VND/năm)

---

## 7. Nhược điểm / Hạn chế

1. **Vendor lock-in:** Chỉ tích hợp tốt trong hệ sinh thái MISA
2. **Không open-source:** Không thể tự host, không truy cập source code
3. **API hạn chế:** Chỉ employee/org data, không expose process model/instances
4. **Không scripting nâng cao:** Không có custom logic, chỉ no-code conditions
5. **Report builder cơ bản:** So với BI tools (Metabase, Superset) còn hạn chế
6. **Phụ thuộc internet:** SaaS only, không có offline mode

---

## 8. Mapping: AMIS Quy Trình vs ERPNext

> Bảng so sánh giúp đánh giá gap và định hướng custom development cho DCNET Flow.

| # | Tính năng AMIS QT | ERPNext equivalent | Gap | Ghi chú |
|---|---|---|---|---|
| 1 | No-code process builder (kéo thả) | Workflow Builder | **Partial** | ERPNext workflow đơn giản hơn nhiều (state machine, không có visual builder) |
| 2 | 500+ mẫu quy trình | — | **Full gap** | ERPNext không có template library |
| 3 | Form builder (tạo biểu mẫu) | Custom DocType / Web Form | **Partial** | ERPNext có nhưng cần dev, không no-code friendly |
| 4 | Điều kiện trường (AND/OR) | Depends On / fetch_from | **Partial** | ERPNext có cơ bản, không có AND/OR visual builder |
| 5 | Bước phê duyệt | Workflow transitions | **Available** | ERPNext Workflow hỗ trợ approve/reject |
| 6 | Bước thực hiện | Workflow transitions | **Available** | Map được qua workflow states |
| 7 | Bước song song (parallel) | — | **Full gap** | ERPNext workflow là sequential only |
| 8 | Rẽ nhánh (branching) | Workflow conditions | **Partial** | ERPNext chỉ hỗ trợ basic conditions (field-based) |
| 9 | 5 loại executor | Workflow roles | **Partial** | ERPNext chỉ có Role-based, không có "quản lý trực tiếp", "vị trí" |
| 10 | Thu hồi (recall) | Amendment / Cancel | **Partial** | ERPNext có Cancel + Amend, khác concept |
| 11 | Chuyển giao (reassign) | Assignment Rule / Manual | **Available** | ERPNext có assign to user |
| 12 | Auto trigger (định kỳ) | Scheduler / Cron | **Available** | Cần custom code (hooks.py scheduler_events) |
| 13 | Trigger từ app khác | Webhooks / Doc Events | **Available** | ERPNext event hooks mạnh (on_submit, on_update...) |
| 14 | Trigger cập nhật trường | Doc Events / Value Change | **Available** | via controller validate/on_change |
| 15 | Quy trình liên kết (linked) | — | **Full gap** | Cần custom: auto-create next doc on submit |
| 16 | Quy trình con (sub-process) | — | **Full gap** | Cần custom development |
| 17 | WeSign (ký số) | — | **N/A** | Không cần cho DCNET (có thể thêm sau) |
| 18 | Open API (OAuth) | REST API | **Available** | ERPNext API mạnh hơn nhiều (full CRUD trên mọi DocType) |
| 19 | Report builder | Report Builder + Query Report | **Available** | ERPNext report system mạnh, có script report |
| 20 | Dashboard | Dashboard Chart + Number Card | **Available** | ERPNext có sẵn dashboard system |
| 21 | Version control (phiên bản) | Version / Amendment | **Partial** | ERPNext có Version log nhưng khác concept |
| 22 | QA/Compliance tracking | — | **Full gap** | Cần custom DocType + workflow |
| 23 | Mobile app | Frappe Mobile | **Partial** | Frappe mobile cơ bản, ít tính năng |
| 24 | AI features (50+) | — | **Full gap** | Có thể bù bằng n8n + Claude (post go-live) |
| 25 | Comment/discussion | Comment system | **Available** | ERPNext có comment + mention + email |
| 26 | File attachment | File Manager | **Available** | ERPNext hỗ trợ đầy đủ |

### Tổng kết Gap

| Loại | Số lượng | Tỷ lệ |
|------|:--------:|:------:|
| **Available** (ERPNext có sẵn) | 11 | 42% |
| **Partial** (có nhưng cần bổ sung) | 8 | 31% |
| **Full gap** (cần build mới) | 6 | 23% |
| **N/A** (không cần) | 1 | 4% |

### Key Takeaways cho DCNET Flow

1. **ERPNext Workflow đủ dùng cho DCNET Flow** — Khách hàng DCNET (Thăng Long TM, Nhật Minh Sport) cần quy trình phê duyệt cho Purchase/Sales/Stock, không cần no-code process builder phức tạp như MISA
2. **Parallel steps là gap lớn nhất** — Nếu khách cần, phải custom. Nhưng các quy trình mua hàng/bán hàng thường sequential
3. **Linked processes** — ERPNext đã có concept này qua document flow (SO → DN → SI), chỉ cần custom cho trường hợp đặc biệt
4. **AI features** — Kế hoạch n8n + Claude (T7/2026) sẽ bù đắp gap này
5. **Mobile** — Frappe mobile đang cải thiện, đủ dùng cho approval workflows
6. **API** — ERPNext REST API mạnh hơn MISA Open API rất nhiều

---

## 9. Bài học áp dụng cho DCNET Flow

### UX/UI

- **Giao diện phê duyệt nên đơn giản:** Approve/Reject rõ ràng, comment box, file attach
- **Mobile-first cho approval:** Manager cần approve nhanh trên điện thoại
- **Dashboard cho lãnh đạo:** Tổng quan tình hình xử lý, bottleneck

### Workflow Design

- **Template quy trình mẫu:** Tạo sẵn workflow cho Purchase Receipt, Sales Order, Stock Entry... (không cần 500+ nhưng cần cover use cases chính)
- **Notification rõ ràng:** Email + push notification khi có task cần xử lý
- **Escalation:** Auto escalate khi quá hạn (ERPNext chưa có built-in, cần custom)

### Tích hợp

- **Liên kết quy trình:** Tận dụng ERPNext document flow (SO → DN → SI) thay vì build linked process engine
- **Automation:** Dùng ERPNext hooks + scheduler thay vì no-code automation builder

---

## Sources

### Trang chính thức
- https://amis.misa.vn/amis-quy-trinh/
- https://amis.misa.vn/en/process/
- https://amis.misa.vn/130047/huong-dan-su-dung-amis-quy-trinh/
- https://amis.misa.vn/156325/danh-gia-phan-mem-misa-amis-quy-trinh/

### Help Center (chi tiết tính năng)
- https://helpamis.misa.vn/amis-quy-trinh/
- https://helpamis.misa.vn/kb/tong-quan-amis-quy-trinh/
- https://helpamis.misa.vn/amis-quy-trinh/kb/tao-moi-quy-trinh/
- https://helpamis.misa.vn/amis-quy-trinh/kb/thiet-lap-tu-dong/
- https://helpamis.misa.vn/amis-quy-trinh/kb/thiet-lap-dieu-kien-truong/
- https://helpamis.misa.vn/amis-quy-trinh/kb/open-api/
- https://helpamis.misa.vn/amis-quy-trinh/kb/bao-cao-tu-tao/
- https://helpamis.misa.vn/amis-quy-trinh/kb/lich-su-phien-ban-quy-trinh-va-khoi-phuc-lai-phien-ban-cu/
- https://helpamis.misa.vn/amis-quy-trinh/kb/danh-dau-phien-ban-quy-trinh-thuc-thi-va-tai-lieu-quy-trinh/
- https://helpamis.misa.vn/amis-quy-trinh/kb/thu-vien-mau-quy-trinh/
- https://helpamis.misa.vn/amis-quy-trinh/kb/chay-va-thuc-hien-quy-trinh/
