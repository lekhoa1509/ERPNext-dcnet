# Frappe Academy — Curriculum Reference

> **Chương trình học Frappe Framework & ERPNext Development**
> 9 Modules (Module 0 optional) | ~46 Lessons | ~56 giờ học ước tính
>
> Ngôn ngữ: Giải thích bằng tiếng Việt, giữ nguyên thuật ngữ kỹ thuật bằng tiếng Anh.

---

## Learning Path Diagram

```
[Module 0: Python Bridge — optional, for PHP/Laravel devs]
    │
    ▼
Module 1: Frappe Foundation
    │
    ├──► Module 2: DocType Mastery
    │        │
    │        ├──► Module 3: Client & Server Scripting
    │        │        │
    │        │        └──► Module 4: Controllers & Hooks
    │        │                 │
    │        │                 ├──► Module 5: Database API & REST API
    │        │                 │
    │        │                 └──► Module 6: Desk UI & frappe-ui
    │        │                          │
    │        │                          └──► Module 7: Advanced Topics
    │        │                                   │
    │        │                                   └──► Module 8: ERPNext Development
    │        │
    │        └──► Module 6 (partial — L6.1, L6.2 có thể học song song với Module 3)
    │
    └──► Module 5 (partial — L5.1 có thể học sớm sau Module 1)
```

### Recommended Order (Thứ tự khuyến nghị)

| Giai đoạn | Modules | Mô tả |
|:---------:|---------|-------|
| **Pre-req** | 0 (optional) | Python Bridge — nếu bạn từ PHP/Laravel |
| **Beginner** | 1 → 2 | Nền tảng — hiểu framework và data model |
| **Intermediate** | 3 → 4 → 5 | Scripting & API — viết logic nghiệp vụ |
| **Advanced** | 6 → 7 | UI, testing, permissions, templates, deploy |
| **Capstone** | 8 | Áp dụng lên ERPNext thực tế |

### Total Estimated Time (Tổng thời gian ước tính)

| Module | Giờ |
|--------|:---:|
| Module 0: Python Bridge *(optional)* | 4 |
| Module 1: Frappe Foundation | 5 |
| Module 2: DocType Mastery | 8 |
| Module 3: Client & Server Scripting | 8 |
| Module 4: Controllers & Hooks | 6 |
| Module 5: Database API & REST API | 6 |
| Module 6: Desk UI & frappe-ui | 6 |
| Module 7: Advanced Topics | 8 |
| Module 8: ERPNext Development | 7 |
| **Tổng (không Module 0)** | **~54 giờ** |

---

## Module 0: Python Bridge *(Optional — cho PHP/Laravel devs)*

**Python nhanh cho người biết PHP/Laravel**

> Module optional dành riêng cho developer PHP/Laravel chuyển sang Frappe.
> Nếu bạn đã thoải mái Python, bỏ qua và bắt đầu từ Module 1.

### Learning Objectives

- Chuyển đổi tư duy PHP/Laravel sang Python mà không cần học lại từ đầu
- Nắm vững các tính năng Python mà Frappe sử dụng nhiều (decorator, comprehension, context manager)
- Hiểu hệ thống module/import của Python so với `use` trong PHP
- Thành thạo Frappe utility functions (`flt`, `cint`, `today`, `add_days`...)

### Lessons

| Bài | Tiêu đề | Chủ đề |
|:---:|---------|--------|
| L0.1 | Python Syntax so với PHP | Bảng so sánh cú pháp, indentation, string format |
| L0.2 | Python features Frappe dùng nhiều | Decorator, list comprehension, dict unpacking, context manager |
| L0.3 | Module & Package System | Import, `__init__.py`, Frappe utility functions |
| L0.4 | Laravel ↔ Frappe Equivalents | Bảng mapping framework-level và code-level |

### Reference

`references/module-00-python-bridge.md` | Exercises: `exercises/ex-00-python-bridge.md`

---

## Module 1: Frappe Foundation

**Nền tảng Frappe Framework**

> Hiểu kiến trúc tổng thể của Frappe, cách framework hoạt động từ request đến response,
> và thành thạo công cụ Bench CLI để quản lý apps và sites.

### Learning Objectives (Mục tiêu học tập)

- Hiểu kiến trúc MVC của Frappe và mối quan hệ giữa bench, sites, apps
- Sử dụng thành thạo Bench CLI cho các tác vụ phát triển hàng ngày
- Hiểu HTTP request lifecycle trong Frappe (WSGI → routing → response)
- Nắm cấu trúc một Frappe app và vai trò của từng file cấu hình
- Tự tạo được một custom app mới trên devcontainer

### Prerequisites (Yêu cầu trước)

- Python cơ bản (functions, classes, decorators)
- HTML/CSS/JavaScript cơ bản
- Git cơ bản (clone, commit, push)
- Biết dùng terminal/command line
- Docker đã cài đặt (cho devcontainer)

### Estimated Time: ~5 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L1.1 | **Frappe Architecture** | Kiến trúc MVC (Model-View-Controller) của Frappe. Khái niệm bench (workspace chứa nhiều sites), site (một instance ứng dụng), app (module code). Cách chúng liên kết với nhau. So sánh với Django/Rails để dễ hiểu. |
| L1.2 | **Bench CLI** | Các lệnh quan trọng nhất: `bench new-app`, `bench new-site`, `bench --site [site] migrate`, `bench clear-cache`, `bench start`, `bench get-app`. Thực hành từng lệnh trên devcontainer. |
| L1.3 | **HTTP & Routing** | Request lifecycle: WSGI server (Werkzeug/Gunicorn) → `frappe.handler` → URL routing → response. Cách Frappe map URL `/api/method/...` và `/api/resource/...`. Static files, WebSocket. |
| L1.4 | **App Structure** | Cấu trúc thư mục một Frappe app: `hooks.py` (điểm cấu hình trung tâm), `modules.txt` (danh sách modules), `pyproject.toml` (metadata), `patches/` (database migrations). Giải thích vai trò từng file. |
| L1.5 | **Quiz + Hands-on** | Tạo custom app `frappe_learn` trên devcontainer. Chạy `bench new-app`, thêm vào site, verify trên Desk. Quiz kiểm tra kiến thức Module 1. |

### Key Skills Referenced

- `frappe` — Framework Core, App Structure, Bench Commands

---

## Module 2: DocType Mastery

**Làm chủ DocType — trái tim của Frappe**

> DocType là khái niệm cốt lõi nhất trong Frappe — nó đồng thời là model (database table),
> view (form UI), và controller (business logic). Module này dạy cách thiết kế DocType
> đúng cách, từ field types đến naming rules đến child tables.

### Learning Objectives (Mục tiêu học tập)

- Hiểu DocType là gì và tại sao nó là trung tâm của Frappe
- Phân biệt và sử dụng đúng các field types (Link, Table, Select, Dynamic Link...)
- Thiết kế naming rules phù hợp cho từng loại DocType
- Tạo và quản lý child tables (parent-child relationship)
- Hiểu Workflow & States để quản lý trạng thái document
- Tự tạo được một mini app hoàn chỉnh (Library Management)

### Prerequisites (Yêu cầu trước)

- Module 1: Frappe Foundation (hoàn thành)
- Hiểu cơ bản về relational database (tables, foreign keys)

### Estimated Time: ~8 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L2.1 | **DocType là gì** | DocType = Model + View + Controller. Khi tạo DocType, Frappe tự động tạo: database table, REST API, form UI, list view, permissions. So sánh: 1 DocType = 1 Django Model + 1 ModelAdmin + API endpoints. Các loại: Regular, Single, Child Table, Virtual. |
| L2.2 | **Field Types** | Tổng quan ~30 field types. Focus vào các type quan trọng: `Link` (foreign key), `Table` (child table), `Select` (dropdown), `Dynamic Link` (polymorphic reference), `Attach` (file upload), `Currency`, `Date/Datetime`. Options, depends_on, mandatory, read_only. |
| L2.3 | **Naming Rules** | 5 cách đặt tên document: `autoname` patterns (`field:name`, `naming_series:`, `hash`, `format_value_or_field:PREFIX-.####`, `Prompt`). Khi nào dùng cách nào. Ảnh hưởng đến performance và UX. `naming_series` cho documents cần số thứ tự (Invoice, Order). |
| L2.4 | **Child Tables** | Cách tạo Child DocType (istable=1). Mối quan hệ parent-child: `parent`, `parenttype`, `parentfield`, `idx`. Cách thêm/xóa rows bằng Python và JavaScript. Khi nào dùng Child Table vs Link. |
| L2.5 | **Workflow & States** | Workflow DocType: states, transitions, allowed roles. `doc.docstatus` (0=Draft, 1=Submitted, 2=Cancelled). Amend. Workflow Actions. Khi nào dùng Workflow vs custom status field. |
| L2.6 | **Hands-on: Library Management** | Tạo mini app Library Management với 3 DocTypes: `Book` (naming: ISBN), `Library Member` (naming series: LM-.####), `Book Transaction` (child table: Book Issue/Return). Thêm Workflow cho Transaction. Test trên Desk. |

### Key Skills Referenced

- `frappe` — DocType, Framework Core
- `erpnext` — Code Interpreter (để hiểu DocType patterns trong ERPNext)

---

## Module 3: Client & Server Scripting

**Viết script để mở rộng logic nghiệp vụ**

> Frappe cho phép viết Client Script (JavaScript chạy trên browser) và Server Script
> (Python chạy trên server) mà KHÔNG cần sửa source code. Đây là cách customize
> nhanh nhất và phổ biến nhất trong thực tế.

### Learning Objectives (Mục tiêu học tập)

- Viết Client Script với các trigger events (refresh, validate, form_render...)
- Sử dụng advanced client APIs: set_query, toggle_display, add_custom_button
- Viết Server Script cho Before Save, After Save, và API endpoint
- Nhận biết và tránh các lỗi phổ biến (gotchas) khi viết Server Script
- Sử dụng System Console để debug và test nhanh

### Prerequisites (Yêu cầu trước)

- Module 1 + Module 2 (hoàn thành)
- JavaScript ES6 cơ bản (arrow functions, promises, async/await)

### Estimated Time: ~8 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L3.1 | **Client Script basics** | Cách tạo Client Script trên Desk. Trigger events: `refresh`, `validate`, `onload`, `form_render`, field `onchange`. `frappe.ui.form.on("DocType", {...})`. Cur_frm vs frm. `frm.set_value()`, `frm.refresh_field()`, `frm.save()`. |
| L3.2 | **Client Script advanced** | `frm.set_query("field", ...)` — lọc Link field. `frm.toggle_display("field", condition)` — ẩn/hiện field. `frm.add_custom_button("Label", callback, group)` — thêm nút. `frappe.call({method: ...})` — gọi server. `frappe.confirm()`, `frappe.prompt()`, `frappe.msgprint()`. |
| L3.3 | **Server Script basics** | Tạo Server Script trên Desk. 3 loại: Before Save Event, After Save Event, API. Biến có sẵn: `doc`, `frappe`. Cách truy cập fields: `doc.field_name`. Cách raise exception: `frappe.throw()`. |
| L3.4 | **Server Script gotchas** | **CRITICAL RULES** (lỗi phổ biến nhất khi viết Server Script): (1) KHÔNG `import` — dùng `frappe.utils.now()` thay vì `from frappe.utils import now`. (2) KHÔNG `self.` — dùng `doc.field`. (3) KHÔNG `frappe.db.*` trong Client Script — dùng `frappe.call()`. (4) Sandbox limitations: không truy cập filesystem, không subprocess. |
| L3.5 | **System Console** | Mở System Console (`/app/system-console`). Chạy Python trực tiếp trên server. Debug: `frappe.get_doc()`, `frappe.db.get_value()`, `frappe.db.sql()`. Lưu ý: chạy trong transaction, cần `frappe.db.commit()` để lưu thay đổi. |
| L3.6 | **Hands-on: 5 Scripts** | Viết 5 scripts cho Library app: (1) Validate — check book availability before issue. (2) Auto-calc — tính overdue days. (3) Filter — set_query cho Book field. (4) Button — "Return Book" custom button. (5) API — Server Script endpoint trả danh sách overdue books. |

### Key Skills Referenced

- `dcnet_quality` — Client Scripts (Syntax Layer), Server Scripts (Syntax Layer)
- `frappe` — Framework Core, API

---

## Module 4: Controllers & Hooks

**Controller Python và hooks.py — customize ở tầng code**

> Khi Client/Server Script không đủ mạnh, bạn cần viết Controller (Python class)
> và cấu hình hooks.py. Đây là cách chính thức để build production-grade features.

### Learning Objectives (Mục tiêu học tập)

- Hiểu controller lifecycle và thứ tự các events
- Viết controller class với override và extend patterns
- Cấu hình hooks.py cho doc_events, scheduler, fixtures, overrides
- Tạo scheduled jobs (daily, hourly, cron)
- Áp dụng controller + hooks vào Library app

### Prerequisites (Yêu cầu trước)

- Module 1 + 2 + 3 (hoàn thành)
- Python OOP (class inheritance, super(), decorators)

### Estimated Time: ~6 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L4.1 | **Controller lifecycle** | Thứ tự events khi save document: `before_validate` → `validate` → `before_save` → `before_insert` (new) → `after_insert` (new) → `on_update` → `after_save` → `on_change`. Submit: `before_submit` → `on_submit`. Cancel: `before_cancel` → `on_cancel`. Trash: `on_trash`. Mỗi event dùng cho mục đích gì. |
| L4.2 | **Controller patterns** | File `{doctype_folder}/{doctype_name}.py`. Class kế thừa `Document`. Override method: `def validate(self)`. Gọi parent: `super().validate()`. **QUAN TRONG:** KHONG modify field trong `on_update` — dùng `frappe.db.set_value()` thay vì `self.field = value`. Extend controller của DocType khác. |
| L4.3 | **hooks.py deep dive** | `doc_events`: hook vào lifecycle của DocType bất kỳ. `scheduler_events`: chạy code theo lịch. `fixtures`: export/import data cấu hình. `override_whitelisted_methods`: thay thế API method. `before_migrate`, `after_install`. `jinja`: thêm custom Jinja methods/filters. |
| L4.4 | **Scheduled Jobs** | `scheduler_events` trong hooks.py: `daily`, `hourly`, `weekly`, `monthly`, `cron` (crontab syntax). Cách test: `bench execute [method]`. Logging: `frappe.logger()`. Error handling: jobs fail silently — phải log. RQ (Redis Queue) — background jobs. |
| L4.5 | **Hands-on: Library Controller + Hooks** | Tạo controller cho Book Transaction: validate availability, auto-set return date. Thêm hooks.py: `doc_events` cho auto-notification, scheduled job daily check overdue books, fixture export Library Settings. |

### Key Skills Referenced

- `dcnet_quality` — Controllers (Syntax Layer), hooks.py (Syntax Layer), Scheduler (Syntax Layer)
- `frappe` — Framework Core, Service

---

## Module 5: Database API & REST API

**Truy vấn database và xây dựng API endpoints**

> Frappe cung cấp Database API (Python) để truy vấn dữ liệu an toàn không cần viết raw SQL,
> và REST API framework để expose endpoints cho external systems.

### Learning Objectives (Mục tiêu học tập)

- Sử dụng thành thạo frappe.db API (get_value, get_list, get_all, sql, set_value)
- Viết query an toàn với Query Builder (frappe.qb)
- Hiểu transaction management và caching trong Frappe
- Xây dựng REST API endpoints với @frappe.whitelist
- Test API endpoints bằng curl và frappe.call

### Prerequisites (Yêu cầu trước)

- Module 1 + 2 + 4 (hoàn thành)
- SQL cơ bản (SELECT, JOIN, WHERE, GROUP BY)

### Estimated Time: ~6 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L5.1 | **frappe.db API** | `frappe.db.get_value("DocType", name, fieldname)` — lấy 1 giá trị. `frappe.db.get_list("DocType", filters, fields, order_by, limit)` — lấy danh sách. `frappe.db.get_all()` — bỏ qua permissions. `frappe.db.set_value()` — update trực tiếp (bypass controller). `frappe.db.sql()` — raw SQL (dùng khi cần). `frappe.db.exists()`, `frappe.db.count()`. |
| L5.2 | **Query Builder (frappe.qb)** | `frappe.qb.from_("tabDocType").select("field1", "field2").where(...)`. Type-safe, composable queries. JOIN, subquery, aggregate functions. So sánh với raw SQL: an toàn hơn, dễ maintain hơn. Khi nào dùng qb vs frappe.db vs raw SQL. |
| L5.3 | **Transactions & Caching** | `frappe.db.commit()` — khi nào cần, khi nào không. `frappe.db.savepoint()` — partial rollback. Redis cache: `frappe.cache().set()`, `frappe.cache().get()`. `frappe.local` — request-scoped data. Performance tips: N+1 queries, batch operations. |
| L5.4 | **REST API** | `@frappe.whitelist()` — expose Python function qua HTTP. `@frappe.whitelist(allow_guest=True)` — public API. Request: `frappe.call({method: "app.module.file.function"})`. Resource API: GET/POST/PUT/DELETE `/api/resource/DocType`. Authentication: token, cookie, OAuth. Rate limiting. |
| L5.5 | **Hands-on: 5 API Endpoints** | Tạo 5 endpoints cho Library app: (1) GET — danh sách books available. (2) GET — member borrowing history. (3) POST — issue book (with validation). (4) PUT — return book. (5) GET — overdue report (with aggregation). Test tất cả bằng curl + frappe.call. |

### Key Skills Referenced

- `dcnet_quality` — Database (Core Layer), Whitelisted Methods (Syntax Layer), API (Core Layer)
- `frappe` — API, Data Import

---

## Module 6: Desk UI & frappe-ui

**Tùy chỉnh giao diện Desk và xây dashboard**

> Frappe Desk là giao diện quản trị chính. Module này dạy cách customize form,
> tạo report, và xây dashboard hoàn chỉnh với Number Cards và Charts.

### Learning Objectives (Mục tiêu học tập)

- Customize form layout: custom buttons, sections, dynamic field visibility
- Tạo List View customizations và Report Builder queries
- Viết Script Reports (Python + JS) cho báo cáo phức tạp
- Xây dựng Workspace và Dashboard với Number Cards và Charts
- Tạo dashboard hoàn chỉnh cho Library app

### Prerequisites (Yêu cầu trước)

- Module 1 + 2 + 3 (hoàn thành)
- Module 5 (L5.1 — frappe.db) khuyến nghị

### Estimated Time: ~6 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L6.1 | **Form customization** | Custom buttons (`frm.add_custom_button`), sections, column breaks. `frm.toggle_display()`, `frm.toggle_reqd()`. Dashboard section: `frm.dashboard.add_indicator()`. Form layout: sections, tabs (v14+). Sidebar, timeline. `frm.page.set_primary_action()`. |
| L6.2 | **List View & Report Builder** | List View: default fields, filters, order. Custom List View JS: `frappe.listview_settings`. Row indicators, formatters. Report Builder: built-in query builder cho end users. Saved Reports. |
| L6.3 | **Script Reports** | Python report: file structure (`report/{name}/{name}.py` + `.js` + `.json`). `execute()` returns `(columns, data, message, chart)`. Columns format: `{fieldname, label, fieldtype, width}`. Chart: `{data: {labels, datasets}, type: "bar"}`. Filters trong JS. Report có thể dùng raw SQL cho performance. |
| L6.4 | **Workspace & Dashboard** | Workspace: trang chủ module, cấu hình qua JSON hoặc UI. Content blocks: header, card, number_card, chart, shortcut, spacer. Number Card: Standard (count/sum) hoặc Custom (API method return `{value, fieldtype}`). Dashboard Chart: linked to Report hoặc custom source. `filters_json` format khác nhau giữa Number Card (array-of-arrays) và Chart (object). |
| L6.5 | **Hands-on: Library Dashboard** | Tạo Workspace "Library" hoàn chỉnh: (1) Number Cards — tổng sách, sách đang mượn, overdue count. (2) Chart — books issued per month. (3) Script Report — overdue books detail. (4) Shortcuts — quick links đến các DocTypes. |

### Key Skills Referenced

- `dcnet_quality` — Client Scripts (Syntax Layer), Jinja (Syntax Layer)
- `frappe` — Desk UI, Integration
- `erpnext` — Code Interpreter

---

## Module 7: Advanced Topics

**Chủ đề nâng cao: Permissions, Templates, Testing**

> Các kiến thức cần thiết để đưa app vào production: phân quyền chặt chẽ,
> print format đẹp, test tự động, và quản lý data.

### Learning Objectives (Mục tiêu học tập)

- Thiết kế hệ thống phân quyền đa tầng (Role, User Permission, Permission Rules)
- Viết Jinja templates cho Print Format và Email Template
- Viết automated tests với FrappeTestCase
- Quản lý data fixtures cho development và deployment
- Áp dụng testing và print format vào Library app

### Prerequisites (Yêu cầu trước)

- Module 1 đến 6 (hoàn thành)
- Jinja2 template syntax cơ bản (khuyến nghị)

### Estimated Time: ~6 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L7.1 | **Permissions** | 3 tầng phân quyền: (1) **Role Permission** — DocType level (read, write, create, delete, submit, amend). (2) **User Permission** — restrict theo giá trị Link field (VD: chỉ thấy data của Company mình). (3) **Permission Rules** — conditional permissions (VD: chỉ edit nếu owner). `has_permission()`, `frappe.permissions.add_user_permission()`. |
| L7.2 | **Jinja Templates** | Print Format: HTML + Jinja2 (`doc`, `frappe`, `filters`). Standard format vs Custom HTML. `{% for row in doc.items %}`. Jinja filters: `fmt_money`, `frappe.format_date`. Email Template: variables, conditional content. Cách thêm custom Jinja method qua hooks.py. |
| L7.3 | **Testing** | `FrappeTestCase` — base class cho unit tests. Test structure: `tests/test_{doctype}.py`. Fixtures: `tests/test_records.json`. `self.assertRaises`, `frappe.get_doc().insert()`. Running tests: `bench run-tests --app [app] --module [module]`. Integration tests: test full workflow (create → submit → cancel). |
| L7.4 | **Data Import/Export** | Data Import tool: CSV format, template download. Fixtures trong hooks.py: `fixtures = [{"dt": "Custom Field", "filters": [...]}]`. `bench export-fixtures`. `bench import-csv`. Bulk operations. Migrate data giữa sites. |
| L7.5 | **Hands-on: Tests + Print Format** | Cho Library app: (1) Viết 5 test cases: create book, issue book, return book, overdue check, permission check. (2) Tạo Print Format "Book Issue Receipt" (Jinja). (3) Export fixtures cho Library Settings. Chạy full test suite. |

### Key Skills Referenced

- `dcnet_quality` — Permissions (Core Layer), Jinja (Syntax Layer), Custom App (Implementation Layer)
- `frappe` — Testing, Data Import, Framework Core

---

## Module 8: ERPNext Development

**Phát triển trên nền ERPNext**

> ERPNext là ERP hoàn chỉnh xây trên Frappe. Module này dạy cách phát triển
> custom app tích hợp với ERPNext — kỹ năng cần thiết cho dự án DCNET Flow.

### Learning Objectives (Mục tiêu học tập)

- Hiểu kiến trúc ERPNext: core DocTypes, naming conventions, module structure
- Phân biệt extend vs override khi customize ERPNext
- Sử dụng Custom Fields và Property Setter đúng cách
- Thiết kế integration patterns (Webhook, Connected App)
- Hoàn thành capstone project: mini module trên ERPNext

### Prerequisites (Yêu cầu trước)

- Module 1 đến 7 (hoàn thành)
- ERPNext đã cài đặt trên devcontainer

### Estimated Time: ~7 giờ

### Lessons

| # | Lesson | Mô tả |
|---|--------|-------|
| L8.1 | **ERPNext Architecture** | Core DocTypes: Company, Customer, Supplier, Item, Sales Order, Purchase Order, Stock Entry, Journal Entry. Naming conventions: `ACC-SINV-.YYYY.-.#####`. Module structure: Accounts, Stock, Selling, Buying, HR, CRM. Document flow: Quotation → SO → DN → SI → PE. Perpetual Inventory: Stock Ledger → GL Entry. |
| L8.2 | **Custom App trên ERPNext** | Tạo custom app kế thừa ERPNext. **Extend** (thêm fields, thêm logic) vs **Override** (thay thế behavior). `override_whitelisted_methods` trong hooks.py. `doc_events` để hook vào ERPNext DocTypes. Khi nào dùng Custom Field vs khi nào tạo DocType mới. Best practice: KHÔNG sửa ERPNext source code. |
| L8.3 | **Custom Fields & Property Setter** | Custom Field: thêm field vào DocType có sẵn. Cách tạo: UI, fixtures, hoặc code (`create_custom_fields()`). `custom_` prefix convention. Property Setter: thay đổi property của field có sẵn (label, options, hidden, reqd). Export/import qua fixtures. |
| L8.4 | **Integration Patterns** | Webhook: outgoing notifications khi document changes. Connected App: OAuth2 integration. Background jobs: `frappe.enqueue()`. External API calls: `requests` library. Error handling cho integrations: retry, logging, fallback. Real-world: tích hợp SMS, email, e-invoice. |
| L8.5 | **Capstone Project** | Tạo mini module trên ERPNext (VD: Warranty Management). Bao gồm: (1) Custom DocType: Warranty Claim (linked to Sales Invoice, Item). (2) Custom Fields trên Item: warranty_months. (3) Controller: auto-validate warranty period. (4) API: check warranty status. (5) Dashboard: Number Cards + Chart. (6) Script Report: expiring warranties. (7) Print Format: Warranty Certificate. (8) Tests: 5 test cases. |

### Key Skills Referenced

- `dcnet_quality` — Custom App (Implementation Layer), Controllers, hooks.py, Custom Fields
- `erpnext` — Accounting, Stock, Selling, Buying, Custom App, Controllers
- `frappe` — Framework Core, Integration, API

---

## Quick Reference: Skill Coverage Map

Bảng tổng hợp skills được sử dụng trong từng module.

| Skill | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 |
|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| `frappe` — Framework Core | x | x | x | x | x | x | x | x |
| `frappe` — DocType | | x | | | | | | |
| `frappe` — Bench Commands | x | | | | | | | |
| `frappe` — App Structure | x | | | | | | | |
| `frappe` — API | | | x | | x | | | |
| `frappe` — Desk UI | | | | | | x | | |
| `frappe` — Testing | | | | | | | x | |
| `frappe` — Data Import | | | | | | | x | |
| `frappe` — Integration | | | | | | | | x |
| `erpnext` — Code Interpreter | | x | | | | x | | |
| `erpnext` — Custom App | | | | | | | | x |
| `erpnext` — Accounting/Stock/Selling/Buying | | | | | | | | x |
| `dcnet_quality` — Syntax Layer | | | x | x | x | x | x | x |
| `dcnet_quality` — Core Layer | | | | | x | | x | |
| `dcnet_quality` — Implementation Layer | | | | | | | | x |

---

## Notes for Tutor (Ghi chu cho AI Tutor)

1. **Adaptive pacing:** Neu hoc vien da biet Python/JS tot, co the rut ngan Module 1 va 3.
2. **Hands-on focus:** Moi module ket thuc bang bai tap thuc hanh. Khong chi doc ly thuyet.
3. **Error-driven learning:** Cho hoc vien gap loi truoc, roi giai thich tai sao — dac biet Module 3 (gotchas).
4. **Library app thread:** Bai tap xuyen suot tu Module 2 den Module 7, tao cam giac lien tuc.
5. **DCNET context:** Module 8 ket noi voi du an thuc te DCNET Flow, giup hoc vien thay gia tri thuc tien.
6. **Bilingual:** Giai thich bang tieng Viet, giu nguyen thuat ngu ky thuat (DocType, hooks, controller, scaffold...).
