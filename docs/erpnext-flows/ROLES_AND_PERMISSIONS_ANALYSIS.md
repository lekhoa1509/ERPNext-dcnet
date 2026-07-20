# Phân tích Roles & Permissions trong DCNET Flow

> **Mục đích:** Phân tích hệ thống roles trong dự án, áp dụng cho phòng ban của công ty
> **Nguồn tham khảo:** FITTING_COACHING_WORKFLOW_BUILDER.md, Frappe Framework
> **Ngày:** 31/01/2026

---

## 1. Tổng quan về Roles trong Frappe/ERPNext

### 1.1. Khái niệm Role

**Role (Vai trò)** trong Frappe là đơn vị phân quyền cơ bản:
- Định nghĩa **quyền truy cập** DocType (Create, Read, Update, Delete, Submit, Cancel)
- Kiểm soát **workflow transitions** (ai được chuyển trạng thái nào)
- Giới hạn **dữ liệu** thông qua User Permissions

### 1.2. Phân biệt Role vs Department vs Designation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SO SÁNH CÁC KHÁI NIỆM                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         DEPARTMENT                                    │   │
│  │                    (Phòng ban tổ chức)                               │   │
│  │                                                                       │   │
│  │  • Phòng Kinh doanh                                                  │   │
│  │  • Phòng Kỹ thuật                                                    │   │
│  │  • Phòng Kế toán                                                     │   │
│  │  • Phòng Nhân sự                                                     │   │
│  │                                                                       │   │
│  │  ➜ Mục đích: Quản lý nhân sự, báo cáo theo phòng ban                │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                │                                             │
│                                ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         DESIGNATION                                   │   │
│  │                      (Chức danh/Vị trí)                              │   │
│  │                                                                       │   │
│  │  • Trưởng phòng                                                      │   │
│  │  • Nhân viên                                                         │   │
│  │  • Thực tập sinh                                                     │   │
│  │  • Chuyên viên                                                       │   │
│  │                                                                       │   │
│  │  ➜ Mục đích: Xác định cấp bậc, lương, phúc lợi                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                │                                             │
│                                ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                           ROLE                                        │   │
│  │                    (Vai trò trong hệ thống)                          │   │
│  │                                                                       │   │
│  │  • Sales User / Sales Manager                                        │   │
│  │  • Fitting User / Fitting Manager                                    │   │
│  │  • Stock User / Stock Manager                                        │   │
│  │  • Accounts User / Accounts Manager                                  │   │
│  │                                                                       │   │
│  │  ➜ Mục đích: PHÂN QUYỀN TRUY CẬP HỆ THỐNG                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3. Mối quan hệ: 1 người có thể có nhiều Roles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                    EMPLOYEE: Nguyễn Văn A                                   │
│                                                                              │
│   ┌─────────────────────┐                                                   │
│   │  Department:        │   ┌─────────────────────────────────────────┐    │
│   │  Phòng Kinh doanh   │   │            ROLES ASSIGNED               │    │
│   └─────────────────────┘   │                                          │    │
│                              │  ✅ Sales User                          │    │
│   ┌─────────────────────┐   │  ✅ Fitting User                         │    │
│   │  Designation:       │   │  ✅ Stock User (chỉ xem)                 │    │
│   │  Nhân viên          │   │  ❌ Accounts User (không có)             │    │
│   └─────────────────────┘   │  ❌ HR User (không có)                   │    │
│                              │                                          │    │
│                              └─────────────────────────────────────────┘    │
│                                                                              │
│   ➜ Anh A làm ở phòng Kinh doanh, chức vụ Nhân viên                        │
│   ➜ Trong hệ thống: có quyền Sales, Fitting, xem Stock                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Roles từ FITTING_COACHING_WORKFLOW_BUILDER.md

### 2.1. Các Roles được định nghĩa

| Role | Tên tiếng Việt | Module | Quyền chính |
|------|---------------|--------|-------------|
| **Sales User** | Nhân viên Sale | CRM, Selling | Tạo đơn, xác nhận lịch, hủy |
| **Sales Manager** | Quản lý Sale | CRM, Selling | Duyệt hủy giữa chừng, xử lý ngoại lệ |
| **Fitting Technician** | NV Kỹ thuật Fitting | Fitting | Thực hiện fitting, nhập thông số |
| **Coach** | Huấn luyện viên | Coaching | Test, dạy học, điểm danh |

### 2.2. Ánh xạ Roles với Workflow Actions

**FITTING WORKFLOW:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FITTING WORKFLOW ROLES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   STATE              ACTION                  ALLOWED ROLES                   │
│   ──────────────────────────────────────────────────────────────────────    │
│                                                                              │
│   registered    ──▶  Xác nhận lịch     ──▶  Sales User                      │
│   registered    ──▶  Hủy đơn           ──▶  Sales User, Sales Manager       │
│                                                                              │
│   confirmed     ──▶  Bắt đầu fitting   ──▶  Fitting Technician              │
│   confirmed     ──▶  Đổi lịch          ──▶  Sales User                      │
│   confirmed     ──▶  Khách không đến   ──▶  Sales User                      │
│                                                                              │
│   in_progress   ──▶  Hoàn thành        ──▶  Fitting Technician              │
│   in_progress   ──▶  Hủy giữa chừng    ──▶  Sales Manager ⚠️ (chỉ Manager)  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**COACHING WORKFLOW:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COACHING WORKFLOW ROLES                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   STATE              ACTION                  ALLOWED ROLES                   │
│   ──────────────────────────────────────────────────────────────────────    │
│                                                                              │
│   new           ──▶  Làm test đầu vào  ──▶  Coach                           │
│   new           ──▶  Khách hủy         ──▶  Sales User                      │
│                                                                              │
│   tested        ──▶  Tư vấn gói        ──▶  Sales User                      │
│   tested        ──▶  Không phù hợp     ──▶  Sales Manager ⚠️                │
│                                                                              │
│   consulted     ──▶  Đăng ký & TT      ──▶  Sales User                      │
│   consulted     ──▶  Khách từ chối     ──▶  Sales User                      │
│                                                                              │
│   paid          ──▶  Bắt đầu khóa học  ──▶  Coach                           │
│                                                                              │
│   in_progress   ──▶  Xin nghỉ tạm      ──▶  Sales User, Coach               │
│   in_progress   ──▶  Hoàn thành khóa   ──▶  Coach                           │
│                                                                              │
│   paused        ──▶  Học tiếp          ──▶  Sales User                      │
│   paused        ──▶  Hủy (quá hạn)     ──▶  Sales Manager ⚠️                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Áp dụng cho Phòng ban Công ty

### 3.1. Mapping: Phòng ban → Roles

| Phòng ban (Department) | Roles gán cho nhân viên |
|------------------------|-------------------------|
| **Phòng Kinh doanh** | Sales User, (Sales Manager cho TP) |
| **Phòng Fitting/Kỹ thuật** | Fitting User, Fitting Manager |
| **Phòng Coaching/Đào tạo** | Coach (role riêng) |
| **Phòng Kho vận** | Stock User, Stock Manager |
| **Phòng Kế toán** | Accounts User, Accounts Manager |
| **Ban Giám đốc** | All Manager roles + Report viewers |

### 3.2. Ví dụ thực tế: Công ty Golf ABC

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CÔNG TY GOLF ABC - TỔ CHỨC & ROLES                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        BAN GIÁM ĐỐC                                  │   │
│  │                                                                       │   │
│  │   • Giám đốc: Nguyễn Văn X                                          │   │
│  │     Roles: System Manager, All Manager roles, Report viewer          │   │
│  │                                                                       │   │
│  │   • Phó GĐ Kinh doanh: Trần Thị Y                                   │   │
│  │     Roles: Sales Manager, Fitting Manager, Stock Manager             │   │
│  │                                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                │                                             │
│          ┌────────────────────┼────────────────────┐                        │
│          │                    │                    │                        │
│          ▼                    ▼                    ▼                        │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐                 │
│  │  PHÒNG        │   │  PHÒNG        │   │  PHÒNG        │                 │
│  │  KINH DOANH   │   │  FITTING      │   │  COACHING     │                 │
│  │               │   │               │   │               │                 │
│  │ TP: Lê Văn A  │   │ TP: Phạm B    │   │ TP: Hoàng C   │                 │
│  │ • Sales       │   │ • Fitting     │   │ • Coach       │                 │
│  │   Manager     │   │   Manager     │   │ • Sales User  │                 │
│  │               │   │               │   │               │                 │
│  │ NV: 5 người   │   │ NV: 3 người   │   │ NV: 4 người   │                 │
│  │ • Sales User  │   │ • Fitting     │   │ • Coach       │                 │
│  │               │   │   User        │   │               │                 │
│  └───────────────┘   └───────────────┘   └───────────────┘                 │
│          │                    │                    │                        │
│          ▼                    ▼                    ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        PHÒNG KẾ TOÁN                                 │   │
│  │                                                                       │   │
│  │   • Kế toán trưởng: Vũ Thị D                                        │   │
│  │     Roles: Accounts Manager, Purchase User, Sales User (read only)   │   │
│  │                                                                       │   │
│  │   • Kế toán viên: 2 người                                           │   │
│  │     Roles: Accounts User                                             │   │
│  │                                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3. Chi tiết Roles cho từng nhân viên

| Nhân viên | Phòng ban | Chức vụ | Roles được gán |
|-----------|-----------|---------|----------------|
| Nguyễn Văn X | Ban GĐ | Giám đốc | System Manager, All Manager roles |
| Trần Thị Y | Ban GĐ | Phó GĐ | Sales Manager, Fitting Manager |
| Lê Văn A | Kinh doanh | Trưởng phòng | **Sales Manager** |
| NV Sale 1-5 | Kinh doanh | Nhân viên | **Sales User** |
| Phạm B | Fitting | Trưởng phòng | **Fitting Manager** |
| NV Fitting 1-3 | Fitting | Kỹ thuật viên | **Fitting User** |
| Hoàng C | Coaching | Trưởng phòng | **Coach**, Sales User |
| NV Coach 1-4 | Coaching | Huấn luyện viên | **Coach** |
| Vũ Thị D | Kế toán | Kế toán trưởng | Accounts Manager |
| KT viên 1-2 | Kế toán | Kế toán viên | Accounts User |

---

## 4. Vấn đề & Giải pháp khi áp dụng Roles cho Phòng ban

### 4.1. Vấn đề 1: Nhân viên làm nhiều việc (Cross-functional)

**Tình huống:**
- Nhân viên Sale kiêm Fitting
- Coach cũng cần tư vấn gói học (cần Sales User)

**Giải pháp:**
```
✅ Gán NHIỀU roles cho 1 user

Ví dụ: NV Sale kiêm Fitting
→ Gán: Sales User + Fitting User

Ví dụ: Coach cần tư vấn
→ Gán: Coach + Sales User (chỉ read + create Quotation)
```

### 4.2. Vấn đề 2: User/Manager Permission

**Tình huống:**
- User role (Sales User) = quyền thao tác
- Manager role (Sales Manager) = quyền duyệt/phê duyệt

**Giải pháp trong FITTING_COACHING_WORKFLOW_BUILDER.md:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PHÂN QUYỀN USER vs MANAGER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ACTION                        SALES USER      SALES MANAGER               │
│   ──────────────────────────────────────────────────────────────────────    │
│                                                                              │
│   Tạo đơn mới                      ✅               ✅                       │
│   Xác nhận lịch                    ✅               ✅                       │
│   Hủy đơn (bước đầu)               ✅               ✅                       │
│   ──────────────────────────────────────────────────────────────────────    │
│   Hủy giữa chừng                   ❌               ✅ ⚠️ (chỉ Manager)      │
│   Hủy vì quá hạn                   ❌               ✅ ⚠️ (chỉ Manager)      │
│   Không phù hợp (từ chối)          ❌               ✅ ⚠️ (chỉ Manager)      │
│                                                                              │
│   ➜ Manager có quyền PHÊ DUYỆT các trường hợp đặc biệt/ngoại lệ           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3. Vấn đề 3: Data Visibility (Ai xem được data gì?)

**Tình huống:**
- Sale A chỉ nên xem Lead của mình
- Manager xem tất cả Lead của team

**Giải pháp: User Permissions**

```python
# Frappe User Permission
{
    "doctype": "User Permission",
    "user": "sale_a@company.com",
    "allow": "Lead",
    "for_value": "LEAD-00001",  # Lead cụ thể
    "apply_to_all_doctypes": 0,
    "applicable_for": "Lead"
}

# Hoặc dùng Role-based restriction
# Trong DocType permissions:
{
    "role": "Sales User",
    "read": 1,
    "if_owner": 1  # ⚠️ Chỉ xem record mình tạo
}
```

### 4.4. Vấn đề 4: Một phòng ban có nhiều cấp

**Tình huống:**
Phòng Kinh doanh có:
- Giám đốc Kinh doanh
- Trưởng phòng
- Trưởng nhóm
- Nhân viên
- Thực tập sinh

**Giải pháp: Role Profile (nhóm roles)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ROLE PROFILES CHO PHÒNG KINH DOANH                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ROLE PROFILE              ROLES INCLUDED                                  │
│   ──────────────────────────────────────────────────────────────────────    │
│                                                                              │
│   "Sales Director"         Sales Manager, Stock Manager, Accounts User,     │
│                            Report viewer, All CRM permissions               │
│                                                                              │
│   "Sales Team Lead"        Sales Manager (limited), Sales User,             │
│                            Stock User, Fitting User                         │
│                                                                              │
│   "Sales Staff"            Sales User, Fitting User (read only)             │
│                                                                              │
│   "Sales Intern"           Sales User (read only), limited create           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Mapping thực tế từ Fitting Session DocType

Từ `fitting_session.json`, ta thấy permissions được định nghĩa:

```json
"permissions": [
  {
    "role": "System Manager",
    "create": 1, "read": 1, "write": 1, "delete": 1,
    "submit": 1, "cancel": 1, "export": 1, "report": 1
  },
  {
    "role": "Sales User",
    "create": 1, "read": 1, "write": 1,
    "submit": 1, "export": 1, "report": 1
    // ⚠️ KHÔNG có delete, cancel
  },
  {
    "role": "Sales Manager",
    "create": 1, "read": 1, "write": 1, "delete": 1,
    "submit": 1, "cancel": 1, "export": 1, "report": 1
    // ✅ CÓ delete, cancel (quyền cao hơn)
  },
  {
    "role": "Fitting User",
    "create": 1, "read": 1, "write": 1,
    "submit": 1, "report": 1,
    "if_owner": 1  // ⚠️ CHỈ XEM CỦA MÌNH
  },
  {
    "role": "Fitting Manager",
    "create": 1, "read": 1, "write": 1, "delete": 1,
    "submit": 1, "cancel": 1, "export": 1, "report": 1
    // ✅ Quyền đầy đủ
  }
]
```

**Phân tích:**

| Role | Create | Read | Write | Delete | Submit | Cancel |
|------|--------|------|-------|--------|--------|--------|
| System Manager | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sales User | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Sales Manager | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Fitting User | ✅ | ✅* | ✅ | ❌ | ✅ | ❌ |
| Fitting Manager | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

*`if_owner: 1` = Chỉ xem record mình tạo

---

## 6. Best Practices khi thiết kế Roles cho Phòng ban

### 6.1. Nguyên tắc chung

```
✅ DO:
1. Tách biệt User role và Manager role
2. Sử dụng Role Profile để gom nhóm
3. Dùng if_owner để giới hạn data visibility
4. Gán NHIỀU roles khi cần cross-functional

❌ DON'T:
1. Không tạo role riêng cho từng người
2. Không gán System Manager cho nhân viên thường
3. Không bỏ qua phân quyền workflow (ai duyệt gì)
```

### 6.2. Template: Roles cho 1 Module mới

```
Module: {MODULE_NAME}

Roles cần tạo:
1. {Module} User       - Quyền cơ bản (CRUD)
2. {Module} Manager    - Quyền quản lý (+ Delete, Cancel, Approve)

Workflow Transitions:
- Từ Draft → Submitted: {Module} User
- Cancel: {Module} Manager only
- Special actions: {Module} Manager only

Data Visibility:
- User: Chỉ xem record của mình (if_owner)
- Manager: Xem tất cả records
```

### 6.3. Checklist khi gán Role cho nhân viên mới

```markdown
□ Xác định phòng ban (Department)
□ Xác định chức vụ (Designation)
□ Xác định công việc chính → Role chính
□ Kiểm tra cross-functional → Roles bổ sung
□ Kiểm tra cấp bậc → User hay Manager
□ Thiết lập User Permissions nếu cần giới hạn data
□ Test thử với tài khoản mới
```

---

## 7. Áp dụng thực tế: DCNET Flow Roles Matrix

### 7.1. Full Roles List cho DCNET Flow

| # | Role Name | Module | Mô tả |
|---|-----------|--------|-------|
| 1 | Sales User | CRM/Selling | Nhân viên bán hàng |
| 2 | Sales Manager | CRM/Selling | Quản lý bán hàng |
| 3 | Fitting User | Fitting | NV kỹ thuật fitting |
| 4 | Fitting Manager | Fitting | Quản lý fitting |
| 5 | Coach | Coaching | Huấn luyện viên |
| 6 | Coaching Manager | Coaching | Quản lý coaching |
| 7 | Stock User | Stock | NV kho |
| 8 | Stock Manager | Stock | Quản lý kho |
| 9 | Accounts User | Accounting | NV kế toán |
| 10 | Accounts Manager | Accounting | Kế toán trưởng |
| 11 | Purchase User | Buying | NV mua hàng |
| 12 | Purchase Manager | Buying | Quản lý mua hàng |

### 7.2. Department → Roles Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DCNET FLOW - DEPARTMENT TO ROLES MAPPING                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   DEPARTMENT                 PRIMARY ROLES          SECONDARY ROLES          │
│   ──────────────────────────────────────────────────────────────────────    │
│                                                                              │
│   Phòng Kinh doanh          Sales User/Manager     Stock User (view)        │
│                                                     Fitting User            │
│                                                                              │
│   Phòng Fitting             Fitting User/Manager   Sales User (create QT)   │
│                                                                              │
│   Phòng Coaching            Coach                  Sales User               │
│                              Coaching Manager                               │
│                                                                              │
│   Phòng Kho                 Stock User/Manager     Purchase User            │
│                                                                              │
│   Phòng Mua hàng            Purchase User/Manager  Stock User               │
│                                                     Accounts User (view)    │
│                                                                              │
│   Phòng Kế toán             Accounts User/Manager  All User roles (view)    │
│                                                                              │
│   Ban Giám đốc              All Manager roles      System Manager           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Kết luận

### 8.1. Roles ≠ Department

- **Department (Phòng ban):** Cấu trúc tổ chức nhân sự
- **Role (Vai trò):** Quyền truy cập hệ thống

**Một nhân viên:**
- Thuộc 1 Department
- Có thể có NHIỀU Roles

### 8.2. Lợi ích của việc tách biệt

| Khía cạnh | Department | Role |
|-----------|------------|------|
| **Mục đích** | Quản lý nhân sự | Phân quyền hệ thống |
| **Ví dụ thay đổi** | Chuyển phòng ban | Gán thêm quyền |
| **Báo cáo** | Theo phòng ban | Theo chức năng |
| **Workflow** | Không liên quan | Kiểm soát chuyển trạng thái |

### 8.3. Recommendation

1. **Tạo Role theo chức năng**, không theo phòng ban
2. **Sử dụng Role Profile** để gom nhóm roles cho từng vị trí
3. **Workflow transitions** chỉ cho phép roles cụ thể
4. **User Permissions** để giới hạn data visibility

---

## 9. References

- **FITTING_COACHING_WORKFLOW_BUILDER.md** - Ví dụ thực tế workflow roles
- **Frappe Roles Documentation** - https://frappeframework.com/docs/user/en/basics/roles
- **ERPNext Permission System** - https://docs.erpnext.com/docs/user/manual/en/role-and-role-profile

---

**Ngày tạo:** 31/01/2026
**Người tạo:** DCNET Development Team
**Trạng thái:** Hoàn thành
