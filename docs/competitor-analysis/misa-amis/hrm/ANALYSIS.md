# MISA AMIS HRM (Nhân sự) — Phân tích chi tiết

> **Ngày phân tích:** 19/03/2026
> **Phiên bản:** v1.0
> **Người phân tích:** DCNET Team

---

## 1. Tổng quan sản phẩm

| Item | Value |
|------|-------|
| **Tên** | MISA AMIS HRM (Nhân sự) |
| **Thuộc** | Nền tảng MISA AMIS (Mảng Nhân sự) |
| **Platform** | SaaS (Cloud), No-code |
| **Khách hàng** | 17,000+ doanh nghiệp |
| **Giá** | Standard: 14,658,000 VND/năm (30 NV) — Professional: 26,278,000 VND/năm (30 NV) |
| **Mobile** | Có (iOS/Android) — check-in GPS, Face ID, QR |
| **AI** | eKYC, facial recognition, AI contract/JD generation, payroll analysis |
| **Chứng nhận** | ISO 27001:2013, ISO 27017:2015, ISO 9001:2015, CMMi Dev Level 3 |
| **Rating** | 4.8/5 (1,781 reviews) |
| **Website** | https://amis.misa.vn/amis-nhan-su/ |

### Vị trí trong hệ sinh thái MISA AMIS

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Tài chính   │  │  Bán hàng   │  │  ★ Nhân sự  │  │  Điều hành  │
│  (Kế toán)   │  │  (CRM)      │  │   (HRM)     │  │ (Quy trình) │
└──────┬───────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       └─────────────────┴────────────────┴────────────────┘
                    Nền tảng MISA AMIS hợp nhất
```

### 9 ứng dụng con (Sub-systems)

| # | Ứng dụng | Tên tiếng Anh | Gói |
|---|----------|---------------|-----|
| 1 | AMIS Thông tin nhân sự | Employee Information | Standard |
| 2 | AMIS Chấm công | Attendance/Timekeeping | Standard |
| 3 | AMIS Tiền lương | Payroll | Standard |
| 4 | AMIS Bảo hiểm xã hội | Social Insurance | Standard |
| 5 | AMIS Thuế TNCN | Personal Income Tax | Standard |
| 6 | AMIS Nhân viên (Portal) | Employee Self-Service | Standard |
| 7 | AMIS Tuyển dụng | Recruitment | Standard |
| 8 | AMIS Mục tiêu | Goal/Objective Management | Professional |
| 9 | AMIS Đánh giá | Employee Evaluation | Professional |

---

## 2. Bốn trụ cột chính

### 2.1 Quản lý Tổ chức & Nhân sự (Organization & Employee)

#### Cơ cấu tổ chức (Organization Structure)

- **Cây phân cấp** (tree structure): Công ty → Khối → Phòng → Ban → Nhóm
- Tự động tạo đơn vị gốc từ đăng ký kinh doanh
- CRUD đơn vị tổ chức + thùng rác khôi phục
- **Org chart visualization** (sơ đồ tổ chức dạng diagram)
- Cấp tổ chức tùy chỉnh (khi mặc định không đủ)
- Đồng bộ dữ liệu tổ chức xuyên suốt tất cả module AMIS
- Hỗ trợ multi-branch (nhiều chi nhánh/đơn vị)

#### Hồ sơ nhân viên (Employee Profile)

- Thông tin cá nhân: CCCD, địa chỉ, gia đình, người phụ thuộc
- Thông tin công việc: phòng ban, vị trí, loại HĐ, ngày bắt đầu
- Học vấn: bằng cấp, chứng chỉ
- Lịch sử công tác: kinh nghiệm trước + career progression nội bộ
- **AI eKYC:** Auto-đọc CCCD, hộ chiếu, CV, bằng cấp → điền form tự động
- Quản lý ảnh + tài liệu đính kèm
- Advanced filtering và search

#### Chức danh & Vị trí (Job Position / Title)

- Quản lý vị trí trong cơ cấu tổ chức
- Mô tả chức năng, nhiệm vụ, trách nhiệm cho mỗi vị trí
- Dùng cho: phân quyền, phê duyệt, gán nhân viên
- Liên kết tới: chính sách chấm công, nghỉ phép, đánh giá

#### Hợp đồng lao động (Employment Contract)

- Quản lý theo loại: thử việc, xác định thời hạn, không xác định thời hạn
- **Cảnh báo tự động** khi HĐ sắp hết hạn
- Tạo & in HĐ hàng loạt
- Quản lý phụ lục HĐ
- **AI generate** mẫu HĐ, quyết định bổ nhiệm
- Gia hạn HĐ qua AMIS Quy Trình

#### Vòng đời nhân viên (Employee Lifecycle)

```
Tuyển dụng → Tiếp nhận → Thử việc → Chính thức → Điều chuyển/Thăng tiến
                                                  → Kỷ luật/Khen thưởng
                                                  → Nghỉ việc/Sa thải
```

- Onboarding: workflow cấu hình (cấp tài khoản, giao tài sản, HĐ, training)
- Offboarding: xử lý nghỉ việc qua AMIS Quy Trình workflow

---

### 2.2 Chấm công & Nghỉ phép (Attendance & Leave)

#### Chấm công (Attendance)

| Phương thức | Chi tiết |
|-------------|---------|
| **GPS** | Vị trí thực tế qua điện thoại |
| **Face ID (AI)** | Nhận diện khuôn mặt AI |
| **QR Code** | Quét mã QR tại công ty |
| **WiFi** | Kết nối WiFi công ty = check-in |
| **Vân tay** | Thiết bị chấm công truyền thống |
| **Tablet** | Dùng tablet làm thiết bị chấm công |

- Quản lý ca làm việc (shift management) linh hoạt
- Cảnh báo OT vượt giới hạn pháp luật (40h/tháng, 200h/năm)
- Auto-tính giờ làm, đi muộn, về sớm
- Tích hợp CRM: chấm công ngoại tuyến cho sale rep
- API export dữ liệu chấm công

#### Nghỉ phép (Leave Management)

| Loại nghỉ | Chi tiết |
|------------|---------|
| **Phép năm** | Tính từ thử việc/chính thức, thâm niên +1 ngày/5 năm, carryover rules |
| **Nghỉ không lương** | Tùy chính sách |
| **Nghỉ bù** (từ OT) | Auto-hết hạn sau khoảng thời gian configurable |
| **Thai sản** | Tùy chọn cộng dồn phép trong thời gian thai sản |
| **Ốm đau** | Theo luật lao động |
| **Nghỉ cưới** | Theo quy định |
| **Tùy chỉnh** | Tự tạo loại nghỉ mới |

- Kế hoạch nghỉ phép năm (annual leave planning)
- Cấu hình ngày nghỉ hàng tuần (theo đơn vị hoặc vị trí)
- Quản lý ngày lễ (pre-load lễ quốc gia + tùy chỉnh)
- Theo dõi số dư phép real-time (chặn vượt quota)
- Workflow phê duyệt nghỉ phép
- In phiếu xin phép
- Báo cáo nghỉ phép theo tháng/nhân viên

---

### 2.3 Lương & Thuế (Payroll & Tax)

#### Tiền lương (Payroll)

- Tính lương tự động theo công thức configurable
- Bảng lương tổng hợp + chi tiết
- Phân bổ lương theo phòng ban → đẩy sang Kế toán
- Phê duyệt bảng lương qua AMIS Quy Trình
- **AI phân tích lương** (mới 08/2025): phát hiện bất thường, so sánh trends
- **MISA AVA:** giải thích công thức lương bằng AI

#### Bảo hiểm xã hội (Social Insurance)

- Quản lý BHXH, BHYT, BHTN theo quy định VN
- Theo dõi tham gia, tạm ngưng, kết thúc
- Tính đóng BHXH tự động

#### Thuế TNCN (Personal Income Tax)

- Tính thuế TNCN hàng tháng/năm
- Quản lý giảm trừ người phụ thuộc
- Báo cáo thuế theo biểu mẫu

---

### 2.4 Tuyển dụng & Đánh giá (Recruitment & Evaluation)

#### Tuyển dụng (Recruitment)

- Pipeline tuyển dụng đầy đủ (từ JD → phỏng vấn → offer)
- **Auto-import** ứng viên từ: Vietnamworks, CareerBuilder, Vieclam24h
- Screening và quản lý hồ sơ ứng viên
- Lịch phỏng vấn + email thông báo tự động
- **AI generate** mô tả công việc (JD)
- **Blacklist detection:** phát hiện nhân viên cũ có vấn đề
- **Cổng ứng viên (Candidate Portal):** self-service theo dõi trạng thái
- Đề xuất tiếp nhận thử việc → chính thức
- Tích hợp AMIS Quy Trình cho approval workflows

#### Đánh giá nhân viên (Employee Evaluation) — Professional only

| Framework | Hỗ trợ |
|-----------|--------|
| **KPI** | Key Performance Indicators |
| **OKR** | Objectives and Key Results |
| **BSC** | Balanced Scorecard |
| **Competency** | Khung năng lực |
| **360°** | Đánh giá đa chiều |
| **Self-Assessment** | Tự đánh giá |

- Chu kỳ đánh giá linh hoạt: tuần/tháng/quý/nửa năm/năm
- Template tùy chỉnh theo phòng ban/vị trí
- Auto tổng hợp kết quả + xếp hạng nhân viên
- Phân quyền xem/sửa đánh giá
- Báo cáo theo năng lực, phòng ban, vị trí

#### Quản lý Mục tiêu (Goal Management) — Professional only

- Hỗ trợ: KPI, OKR, BSC, MBO
- Goal cascading: phân bổ mục tiêu theo cấp tổ chức
- Alignment ngang và dọc
- Theo dõi tiến độ real-time + cảnh báo bottleneck
- Dashboard đa chiều (theo tổ chức hoặc functional area)

---

## 3. Tích hợp (Integration)

### Tích hợp nội bộ MISA AMIS

| Kết nối | Chi tiết |
|---------|---------|
| **HR → Kế toán** | Phân bổ lương theo phòng ban, bảng tổng hợp thanh toán |
| **HR → Thuế** | Tính thuế TNCN hàng tháng/năm |
| **Tuyển dụng → HR** | Chuyển ứng viên → nhân viên (auto thông báo) |
| **HR → Mạng XH nội bộ** | Auto đăng thông báo tuyển/nghỉ/thăng tiến |
| **Chấm công → CRM** | Đồng bộ dữ liệu sale rep ngoại tuyến |
| **★ HR → Quy Trình** | Hub kết nối: tiếp nhận, HĐ, thăng tiến, kỷ luật, nghỉ việc, lương |

### Kết nối với AMIS Quy Trình (Process)

AMIS Quy Trình đóng vai trò **"hub kết nối"** cho các workflow HR:

| Quy trình | Trigger | Kết quả |
|-----------|---------|---------|
| Tiếp nhận thử việc | Tuyển dụng offer | Tạo hồ sơ NV |
| Chấp nhận chính thức | Hết thử việc | Update trạng thái |
| Gia hạn HĐ | HĐ sắp hết hạn | HĐ mới |
| Thăng tiến/Điều chuyển | Đề xuất manager | Update vị trí |
| Kỷ luật/Khen thưởng | Sự kiện | Ghi nhận hồ sơ |
| Nghỉ việc | Đơn xin nghỉ | Offboarding process |
| Phê duyệt bảng lương | Kế toán submit | Giải ngân |

### External API

| Item | Value |
|------|-------|
| **Auth** | Connection Code + Security Key (không phải OAuth) |
| **Outbound** | Dữ liệu chấm công, 7 loại yêu cầu, bảng công |
| **Inbound** | Dữ liệu chấm công từ thiết bị bên ngoài |
| **Payroll export** | Đẩy sang phần mềm kế toán/lương ngoài |
| **Hạn chế** | API cơ bản, cần IT triển khai, không RESTful chuẩn |

---

## 4. Báo cáo & Dashboard

- **50+ báo cáo** đa chiều (Standard)
- **30+ loại** báo cáo tùy chỉnh
- Phân tích biến động nhân sự (turnover)
- Headcount theo phòng ban
- Tổng hợp nghỉ phép theo tháng/nhân viên
- Tổng hợp chấm công (theo thời gian, KPI)
- Phân tích lương (AI-powered)
- Xếp hạng nhân viên
- Đánh giá theo năng lực/phòng ban/vị trí
- Dashboard đa chiều với biểu đồ trực quan
- Export Excel

---

## 5. AI Features (2024-2025)

| Tính năng | Ngày | Module |
|-----------|------|--------|
| Phân tích lương bằng AI | 08/2025 | Payroll |
| MISA AVA giải thích công thức lương | 07/2025 | Payroll |
| Dashboard nhân viên nâng cao | 06/2025 | Employee Portal |
| Nhận diện khuôn mặt AI | 03/2025 | Attendance |
| MISA AVA Mobile Assistant | 02/2025 | Mobile |
| AI eKYC (đọc CCCD, CV, bằng cấp) | 11/2024 | Employee Info |
| Blacklist detection | 09/2024 | Recruitment |
| AI tạo mẫu HĐ | 09/2024 | Employee Info |
| AI tạo JD | 07/2024 | Recruitment |

---

## 6. Ưu điểm

1. **All-in-one HR platform** — 9 ứng dụng con cover toàn bộ HR lifecycle
2. **AI-powered mạnh** — eKYC, facial recognition, payroll analysis, JD/contract generation
3. **Chấm công đa phương thức** — 6 cách check-in (GPS, Face ID, QR, WiFi, vân tay, tablet)
4. **Tích hợp sâu AMIS Quy Trình** — mọi workflow HR chạy qua process engine
5. **Tuân thủ luật lao động VN** — BHXH, thuế TNCN, giới hạn OT, ngày lễ
6. **Đánh giá đa framework** — KPI, OKR, BSC, 360°, Competency
7. **Tuyển dụng tích hợp job boards VN** — Vietnamworks, CareerBuilder, Vieclam24h
8. **Mobile app đầy đủ** — check-in, xin phép, phê duyệt, AI assistant

---

## 7. Nhược điểm / Hạn chế

1. **Vendor lock-in** — Chỉ tích hợp tốt trong hệ sinh thái MISA
2. **API hạn chế** — Connection Code + Security Key, không phải OAuth/REST chuẩn
3. **Training module yếu** — Không có ứng dụng đào tạo riêng, chỉ là phần nhỏ của onboarding
4. **Offboarding cơ bản** — Chỉ là workflow, không phải module cấu trúc
5. **Không open-source** — Không tự host, không customize deep
6. **Cơ cấu tổ chức đơn giản** — Chỉ cây phân cấp, không hỗ trợ matrix organization
7. **Không có succession planning** — Thiếu tính năng quy hoạch kế nhiệm
8. **Giá tăng nhanh** — >200 NV phải contact MISA, gói Professional gần gấp đôi Standard

---

## 8. Mapping: AMIS HRM vs ERPNext

> Bảng so sánh giúp đánh giá gap và định hướng custom development cho DCNET Flow.

### 8.1 Tổ chức & Nhân sự

| # | Tính năng AMIS HRM | ERPNext equivalent | Gap | Ghi chú |
|---|---|---|---|---|
| 1 | Cơ cấu tổ chức (tree) | Department (tree structure) | **Available** | ERPNext Department có parent-child, company-based |
| 2 | Org chart visualization | Organization Chart | **Available** | ERPNext có sẵn trang Organization Chart |
| 3 | Chức danh / Vị trí | Designation + Employee Skill Map | **Available** | Designation = chức danh, có thể thêm custom fields |
| 4 | Hồ sơ nhân viên đầy đủ | Employee DocType | **Available** | ERPNext Employee có 60+ fields, đầy đủ thông tin |
| 5 | AI eKYC (đọc CCCD/CV) | — | **Full gap** | Cần custom hoặc tích hợp 3rd party OCR |
| 6 | Hợp đồng lao động | — (Custom DocType) | **Full gap** | ERPNext không có Employment Contract, cần custom |
| 7 | Cảnh báo HĐ hết hạn | — | **Full gap** | Cần scheduler + notification custom |
| 8 | AI generate HĐ/QĐ | — | **Full gap** | Có thể bù bằng n8n + Claude (post go-live) |
| 9 | Vòng đời NV (lifecycle) | Employee Lifecycle | **Available** | ERPNext có Promotion, Transfer, Separation... |
| 10 | Người phụ thuộc | Employee → Dependents (table) | **Partial** | ERPNext có basic dependents, thiếu chi tiết thuế TNCN |
| 11 | Quản lý trực tiếp | Employee.reports_to | **Available** | Field reports_to trên Employee DocType |

### 8.2 Chấm công & Nghỉ phép

| # | Tính năng AMIS HRM | ERPNext equivalent | Gap | Ghi chú |
|---|---|---|---|---|
| 12 | Chấm công GPS | — | **Full gap** | ERPNext không có GPS check-in |
| 13 | Chấm công Face ID | — | **Full gap** | Cần 3rd party integration |
| 14 | Chấm công QR/WiFi | — | **Full gap** | Cần custom |
| 15 | Chấm công vân tay | Attendance (manual/import) | **Partial** | ERPNext nhận data từ biometric device qua API |
| 16 | Quản lý ca (shift) | Shift Type + Shift Assignment | **Available** | ERPNext có sẵn shift management |
| 17 | Cảnh báo OT vượt giới hạn | — | **Full gap** | Cần custom validation |
| 18 | Nghỉ phép (types) | Leave Type + Leave Application | **Available** | ERPNext có đầy đủ leave management |
| 19 | Phép năm + thâm niên | Leave Policy + Earned Leave | **Partial** | ERPNext có Earned Leave nhưng thâm niên cần custom |
| 20 | Nghỉ bù từ OT | Compensatory Leave Request | **Available** | ERPNext có sẵn |
| 21 | Annual leave planning | — | **Full gap** | Cần custom DocType |
| 22 | Cảnh báo số dư phép | Leave Allocation + validation | **Available** | ERPNext validate tự động khi submit Leave Application |

### 8.3 Lương & Thuế

| # | Tính năng AMIS HRM | ERPNext equivalent | Gap | Ghi chú |
|---|---|---|---|---|
| 23 | Tính lương tự động | Payroll Entry + Salary Structure | **Available** | ERPNext Payroll system đầy đủ |
| 24 | BHXH/BHYT/BHTN | Salary Component | **Partial** | Cần config salary components theo luật VN |
| 25 | Thuế TNCN | Salary Component + Tax Slab | **Partial** | ERPNext có Tax Slab, cần config biểu thuế VN |
| 26 | AI phân tích lương | — | **Full gap** | Có thể bù bằng n8n + Claude |
| 27 | Phân bổ lương → Kế toán | Payroll → GL Entry | **Available** | ERPNext auto-tạo GL Entry từ Payroll |
| 28 | Phê duyệt bảng lương | Workflow on Payroll Entry | **Available** | Config workflow cho Payroll Entry |

### 8.4 Tuyển dụng & Đánh giá

| # | Tính năng AMIS HRM | ERPNext equivalent | Gap | Ghi chú |
|---|---|---|---|---|
| 29 | Pipeline tuyển dụng | Staffing Plan + Job Opening + Job Applicant | **Available** | ERPNext có recruitment module cơ bản |
| 30 | Auto-import job boards | — | **Full gap** | Cần custom integration (Vietnamworks API) |
| 31 | AI generate JD | — | **Full gap** | n8n + Claude |
| 32 | Blacklist detection | — | **Full gap** | Cần custom |
| 33 | Candidate Portal | — | **Full gap** | ERPNext Job Applicant không có self-service portal |
| 34 | KPI/OKR evaluation | Appraisal | **Partial** | ERPNext Appraisal cơ bản, thiếu OKR/BSC/360° |
| 35 | Goal cascading | — | **Full gap** | Cần custom DocType + dashboard |
| 36 | 360° feedback | — | **Full gap** | Cần custom |

### 8.5 Khác

| # | Tính năng AMIS HRM | ERPNext equivalent | Gap | Ghi chú |
|---|---|---|---|---|
| 37 | Onboarding workflow | Employee Onboarding | **Available** | ERPNext có Employee Onboarding template |
| 38 | Offboarding workflow | Employee Separation | **Available** | ERPNext có Employee Separation |
| 39 | Mobile app (HR) | Frappe HR mobile | **Partial** | Frappe mobile cơ bản hơn nhiều |
| 40 | 50+ báo cáo HR | HR Reports | **Partial** | ERPNext có ~15 HR reports, cần thêm custom |
| 41 | Employee Self-Service Portal | Employee Self Service (portal) | **Partial** | ERPNext có ESS nhưng UX kém hơn |
| 42 | Dashboard đa chiều | Dashboard Chart + Number Card | **Available** | ERPNext dashboard system đủ dùng |

### Tổng kết Gap

| Loại | Số lượng | Tỷ lệ |
|------|:--------:|:------:|
| **Available** (ERPNext có sẵn) | 18 | 43% |
| **Partial** (có nhưng cần bổ sung) | 9 | 21% |
| **Full gap** (cần build mới) | 15 | 36% |
| **N/A** (không cần) | 0 | 0% |

### Key Takeaways cho DCNET Flow

1. **ERPNext HR module đủ dùng cho DCNET scope** — Khách hàng DCNET (Thăng Long TM, Nhật Minh Sport) là công ty thương mại, HR không phải core, chỉ cần quản lý nhân viên + phòng ban + phân quyền workflow cơ bản
2. **Phòng ban (Department) là nền tảng** — Cần setup Department tree đúng ngay từ đầu, vì nó ảnh hưởng tới permissions, workflow approval, report filtering
3. **Chấm công là gap lớn nhất** — Nếu khách cần chấm công (GPS/Face ID/QR), phải custom hoặc tích hợp 3rd party (khả năng cao ngoài scope DCNET)
4. **Hợp đồng lao động cần custom** — ERPNext không có Employment Contract DocType, nếu khách cần quản lý HĐ phải tạo custom DocType
5. **Employee.reports_to** là key — Dùng cho approval routing trong workflow, cần setup đúng
6. **AI features** — Không cần trong phase 1, có thể bù bằng n8n + Claude (T7/2026)

---

## 9. Modules vệ tinh (Satellite Modules)

> Các module liên quan/phụ thuộc — tên gọi trong MISA vs ERPNext

| Module vệ tinh | Tên trong MISA AMIS | ERPNext DocType | Vai trò với HRM |
|-----------------|----------------------|-----------------|-----------------|
| **Phòng ban** | AMIS TTNV → Cơ cấu tổ chức | `Department` (tree) | ⭐ Nền tảng: phân quyền, báo cáo, workflow routing |
| **Chức danh** | AMIS TTNV → Chức danh/Vị trí | `Designation` | Phân loại NV, gán workflow executor theo vị trí |
| **Quy trình** | AMIS Quy Trình | `Workflow` + `Assignment Rule` | Hub kết nối: phê duyệt mọi nghiệp vụ HR |
| **Kế toán** | AMIS Kế toán | `GL Entry`, `Journal Entry` | Nhận phân bổ lương, thanh toán |
| **CRM** | AMIS CRM/Bán hàng | `Employee` → `Sales Person` | Chấm công ngoại tuyến cho sale rep |
| **Mạng XH nội bộ** | AMIS MXHNB | `Comment` + `Notification` | Thông báo tuyển/nghỉ/thăng tiến |

### Phòng ban trong MISA vs ERPNext — Chi tiết

| Khía cạnh | MISA AMIS | ERPNext |
|-----------|-----------|---------|
| **Cấu trúc** | Tree (Công ty → Khối → Phòng → Ban → Nhóm) | Tree (Company → Department → Sub-department) |
| **Multi-company** | 1 cơ cấu/công ty | Department gắn Company, multi-company supported |
| **Org chart** | Có (diagram view) | Có (Organization Chart page) |
| **Cấp tùy chỉnh** | Có (thêm level mới) | Không (fixed tree, chỉ parent-child) |
| **Khôi phục** | Có (thùng rác) | Không (delete vĩnh viễn, cần backup) |
| **Dùng cho workflow** | Executor = "phòng ban" + "quản lý trực tiếp" | Role-based only → cần `Assignment Rule` để route theo department |
| **Dùng cho phân quyền** | Department-based permissions | `User Permission` với Department filter |
| **Dùng cho báo cáo** | Filter mặc định mọi report | Filter trên hầu hết HR reports |

---

## 10. Bài học áp dụng cho DCNET Flow

### Tổ chức & Phòng ban

- **Setup Department tree ngay T3** — Đây là master data nền tảng, ảnh hưởng mọi module sau
- **Employee.reports_to PHẢI setup** — Dùng cho approval routing, nếu không setup thì workflow không biết route cho ai
- **Designation nên chuẩn hóa** — Dùng cho filter permission, không nên để free-text

### Workflow Integration

- **MISA dùng Quy Trình làm hub** — DCNET nên dùng ERPNext Workflow + Assignment Rule tương tự
- **Auto-assign approval theo reports_to** — Viết Assignment Rule: khi tạo Leave Application → auto assign cho `employee.reports_to`
- **Notification quan trọng** — Mỗi workflow transition cần email/push notification

### UX/UI

- **Employee Self-Service cần đẹp** — MISA có portal riêng cho NV, ERPNext ESS cơ bản → cần custom UI
- **Mobile-first cho chấm công + phê duyệt** — Manager cần approve nhanh trên điện thoại
- **Dashboard HR cho leadership** — Headcount, turnover, leave usage, attendance summary

### Ngoài scope nhưng cần lưu ý

- **Chấm công** — Nếu khách yêu cầu, nên tích hợp 3rd party (thiết bị chấm công) qua API, không tự build
- **Hợp đồng lao động** — Nếu cần, tạo simple Custom DocType, không cần complex như MISA
- **Đánh giá KPI/OKR** — Ngoài scope T3-T8, có thể plan cho phase 2

---

## Sources

### Trang chính thức
- https://amis.misa.vn/amis-nhan-su/
- https://amis.misa.vn/90798/danh-gia-toan-dien-phan-mem-nhan-su-amis-misa-amis-hrm/
- https://amis.misa.vn/67470/gia-phan-mem-nhan-su-amis-hrm/
- https://amis.misa.vn/128379/bang-gia-phan-mem-misa-amis/
- https://amis.misa.vn/227597/hrm-platform/

### Help Center
- https://helpamis.misa.vn/amis-thong-tin-nhan-su/kb/tong-quan-luong-nghiep-vu-ket-noi-giua-cac-ung-dung-trong-bo-misa-amis-hrm/
- https://helpamis.misa.vn/amis-thong-tin-nhan-su/kb/co-cau-to-chuc/
- https://helpamis.misa.vn/amis-cham-cong/kb/quy-dinh-nghi-tren-amis-cham-cong/
- https://helpamis.misa.vn/amis-cham-cong/kb/tich-hop-api-de-chuyen-du-lieu-tu-amis-cham-cong-sang-cac-phan-mem-khac/

### Tích hợp
- https://amis.misa.vn/123005/amis-quy-trinh-ket-noi-misa-amis-hrm/
- https://helpamis.misa.vn/amis-quy-trinh/kb/ket-noi-voi-bo-misa-amis-hrm-thong-tin-nhan-su-tuyen-dung-tien-luong/

### Tính năng mới
- https://amis.misa.vn/tinh-nang-moi-misa-amis-hrm/
- https://amis.misa.vn/133471/tinh-nang-moi-nhat-tren-amis-tuyen-dung-va-amis-thong-tin-nhan-su/
- https://amis.misa.vn/102312/tinh-nang-phan-mem-amis-danh-gia/
- https://amis.misa.vn/amis-muc-tieu/
