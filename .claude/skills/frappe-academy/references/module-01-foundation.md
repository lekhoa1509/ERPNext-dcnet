# Module 1: Frappe Foundation

> **Mục tiêu:** Hiểu kiến trúc Frappe Framework, làm quen với Bench CLI, nắm vững request lifecycle và app structure.
> **Thời lượng:** 5 lessons | **Độ khó:** Beginner
> **Yêu cầu:** Docker + devcontainer-frappe-1 đang chạy

---

## L1.1: Frappe Architecture

### Tổng quan
Frappe là một full-stack web framework viết bằng Python và JavaScript. Nó theo mô hình **metadata-driven** — thay vì viết code cho mỗi table/form, bạn khai báo DocType (metadata) và Frappe tự động tạo database table, REST API, form UI, và permissions. Bài này giải thích kiến trúc tổng thể, bench là gì, và multi-site architecture.

### Key Concepts

#### 1. MVC Pattern trong Frappe
Frappe không theo MVC truyền thống mà theo **Model-View-Controller-Metadata**:

| Layer | Frappe tương ứng | Mô tả |
|-------|-----------------|-------|
| **Model** | DocType JSON + Controller `.py` | Định nghĩa fields, validations, business logic |
| **View** | Form (JS) + List View + Report | Tự động generate từ DocType metadata |
| **Controller** | Python class kế thừa `Document` | Lifecycle hooks: `validate()`, `on_submit()`, etc. |
| **Metadata** | DocType definition | "Engine" điều khiển tất cả — thay đổi metadata = thay đổi app |

#### 2. Bench — Công cụ quản lý
**Bench** là CLI tool quản lý mọi thứ: sites, apps, processes, deployment.

```
bench/
├── apps/                  # Tất cả Frappe apps (frappe, erpnext, custom_app...)
│   ├── frappe/            # Framework core (BẮT BUỘC)
│   └── erpnext/           # ERP module (tùy chọn)
├── sites/                 # Tất cả sites
│   ├── common_site_config.json  # Config chung
│   ├── site1.local/       # Site 1
│   │   ├── site_config.json     # Config riêng
│   │   └── private/             # Files upload
│   └── site2.local/       # Site 2 (multi-tenant)
├── config/                # nginx, supervisor, redis configs
├── env/                   # Python virtualenv
└── logs/                  # Log files
```

> **Quan trọng:** Bench = tool, Frappe = framework, Site = instance. Một bench có thể chạy nhiều sites (multi-tenancy).

#### 3. Multi-site Architecture
Frappe hỗ trợ **multi-tenancy** — nhiều site dùng chung 1 codebase nhưng database riêng biệt:

```
                    ┌──────────────┐
                    │   Bench CLI  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐ ┌───┴────┐ ┌────┴─────┐
        │  Site A   │ │ Site B │ │  Site C  │
        │  DB: db_a │ │ DB: db_b│ │ DB: db_c │
        └───────────┘ └────────┘ └──────────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────┴───────┐
                    │  Shared Apps │
                    │  (frappe,    │
                    │   erpnext)   │
                    └──────────────┘
```

Mỗi site có:
- **Database riêng** (MariaDB/PostgreSQL)
- **Redis riêng** cho cache, queue, realtime
- **site_config.json** riêng
- **Files/uploads** riêng

#### 4. Process Architecture

```
Bench start chạy 4 processes:
┌─────────────────────────────────────────┐
│  bench start                            │
├─────────┬──────────┬──────────┬─────────┤
│ web     │ worker   │ schedule │ watch   │
│ (gunicorn)│(rq worker)│(scheduler)│(node)  │
│ Port 8000│ Background│ Cron jobs│ JS/CSS │
│         │ jobs     │          │ rebuild │
└─────────┴──────────┴──────────┴─────────┘
```

### Code Examples

```bash
# Trong devcontainer-frappe-1:

# Xem version của frappe và các apps
bench version

# Liệt kê tất cả apps đã cài
bench list-apps

# Xem tất cả sites
ls sites/

# Xem site config
cat sites/flow.local/site_config.json

# Xem các tables trong database (frappe tự tạo từ DocType)
bench --site flow.local mariadb -e "SHOW TABLES LIKE 'tab%' LIMIT 10;"

# Mỗi DocType = 1 table với prefix "tab"
# DocType "Sales Order" → table "tabSales Order"
bench --site flow.local mariadb -e "DESCRIBE \`tabSales Order\` LIMIT 5;"
```

### Mini Quiz

<details>
<summary>Q1: Frappe theo mô hình gì? MVC, MVP, hay Metadata-driven?</summary>

**A:** Metadata-driven. Frappe dùng DocType metadata làm trung tâm — từ metadata nó generate Model (DB table), View (Form UI), và Controller (Python class). Không giống MVC truyền thống nơi bạn phải viết riêng từng layer.
</details>

<details>
<summary>Q2: Một bench có thể chạy bao nhiêu sites? Chung dùng gì và riêng gì?</summary>

**A:** Một bench có thể chạy **nhiều sites** (multi-tenancy). Chung dùng: codebase (apps), Python env, processes. Riêng: database, site_config.json, uploaded files, Redis namespaces.
</details>

<details>
<summary>Q3: Khi bạn tạo DocType "Library Book", Frappe tạo table tên gì trong database?</summary>

**A:** `tabLibrary Book`. Frappe thêm prefix `tab` trước tên DocType. Truy vấn: `SELECT * FROM \`tabLibrary Book\``.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `references/architecture/` để hiểu thêm về architectural patterns
- **DEEP DIVE:** Xem skill `frappe` -> `references/config_patterns/` để hiểu cấu hình bench và site

---

## L1.2: Bench CLI

### Tổng quan
Bench CLI là "Swiss Army knife" của Frappe developer. Mọi thao tác — từ tạo app, migrate database, đến deploy production — đều qua bench. Bài này phân loại và giải thích các lệnh quan trọng nhất, phân biệt giữa **bench commands** (tác động lên bench) và **frappe commands** (tác động lên site).

### Key Concepts

#### 1. Phân loại Bench Commands

| Nhóm | Commands | Mục đích |
|------|----------|---------|
| **App Management** | `new-app`, `get-app`, `remove-app`, `list-apps` | Quản lý Frappe apps |
| **Site Management** | `new-site`, `drop-site`, `use`, `set-config` | Quản lý sites |
| **Development** | `start`, `build`, `watch`, `clear-cache` | Chạy và dev |
| **Database** | `migrate`, `mariadb`, `backup`, `restore` | Database operations |
| **Deployment** | `setup`, `retry-worker`, `doctor` | Production setup |

#### 2. Bench vs Frappe Commands

```bash
# BENCH commands — tác động lên bench/infra
bench start              # Chạy tất cả processes
bench build              # Build JS/CSS assets
bench new-app my_app     # Tạo app mới
bench get-app <url>      # Clone app từ git

# FRAPPE commands — tác động lên 1 site cụ thể (cần --site)
bench --site flow.local migrate          # Chạy database migrations
bench --site flow.local clear-cache      # Xóa cache
bench --site flow.local console          # Python REPL với frappe context
bench --site flow.local mariadb          # MySQL console cho site đó

# Nếu chỉ có 1 site, có thể bỏ --site
bench migrate   # Tự hiểu là site duy nhất
```

#### 3. Development Workflow Commands

```bash
# === HÀNG NGÀY ===
bench start                    # Chạy dev server (port 8000)
bench --site flow.local clear-cache   # Khi UI không cập nhật
bench build --app dcnet_apps   # Rebuild JS/CSS chỉ cho 1 app

# === KHI THAY ĐỔI DOCTYPE ===
bench --site flow.local migrate        # Apply schema changes
bench --site flow.local migrate --skip-failing  # Bỏ qua patch lỗi (dev only!)

# === DEBUG ===
bench --site flow.local console        # frappe.get_doc(), frappe.db.sql()
bench --site flow.local doctor         # Kiểm tra sức khỏe hệ thống
bench --site flow.local show-config    # Xem merged config

# === TESTING ===
bench --site flow.local run-tests --app dcnet_apps --module dcnet_dashboard -v
bench --site flow.local run-tests --doctype "Sales Order" -v

# === PRODUCTION ===
bench --site flow.local backup              # Backup DB + files
bench --site flow.local restore <sql.gz>    # Restore từ backup
bench --site flow.local set-admin-password  # Reset admin password
```

#### 4. App Lifecycle

```bash
# Tạo app mới
bench new-app frappe_learn
# → Tạo: apps/frappe_learn/ với structure chuẩn

# Cài app vào site
bench --site flow.local install-app frappe_learn

# Gỡ app khỏi site (giữ code)
bench --site flow.local uninstall-app frappe_learn

# Xóa app code
bench remove-app frappe_learn
```

### Code Examples

```bash
# Trong devcontainer:
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench version"

# Xem tất cả bench commands
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --help"

# Xem help của 1 command cụ thể
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench migrate --help"

# Kiểm tra sức khỏe site
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local doctor"

# Xem installed apps trên site
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local list-apps"
```

### Mini Quiz

<details>
<summary>Q1: Sau khi thay đổi fields trong DocType, bạn cần chạy lệnh gì để cập nhật database?</summary>

**A:** `bench --site <site> migrate`. Lệnh này đọc metadata từ DocType JSON files và tự động ALTER TABLE để khớp với definition mới. Nó cũng chạy các patches chưa chạy.
</details>

<details>
<summary>Q2: Phân biệt `bench build` và `bench start --build`?</summary>

**A:** `bench build` — build JS/CSS assets 1 lần rồi dừng. `bench start` — chạy dev server với hot-reload (bao gồm watch process tự rebuild khi file thay đổi). Không có flag `--build` cho `bench start` — watch process làm việc này.
</details>

<details>
<summary>Q3: Làm sao để vào Python REPL có sẵn frappe context để test code nhanh?</summary>

**A:** `bench --site <site> console`. Trong console, bạn có thể dùng `frappe.get_doc()`, `frappe.db.sql()`, `frappe.db.get_value()`, etc. Để thoát: `exit()` hoặc Ctrl+D.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> domain "Bench Commands" để có full reference của mọi lệnh
- **DEEP DIVE:** Xem skill `docker` để biết cách chạy bench commands trong devcontainer

---

## L1.3: HTTP & Routing

### Tổng quan
Mọi request đến Frappe đi qua một pipeline rõ ràng: WSGI server (Gunicorn) -> Frappe middleware -> Route resolution -> Response. Hiểu được request lifecycle giúp bạn debug hiệu quả và biết dùng endpoint nào cho API calls. Bài này giải thích chi tiết từng bước.

### Key Concepts

#### 1. Request Lifecycle

```
Client (Browser/API)
      │
      ▼
┌─────────────┐
│   Gunicorn   │  WSGI server, nhiều workers
│   :8000      │  (dev) hoặc Nginx → Gunicorn (prod)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Frappe App  │  frappe.app.application() — WSGI callable
│  Middleware  │  1. Xác định site (Host header)
│              │  2. Init frappe.local (thread-local context)
│              │  3. Connect database
│              │  4. Load session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Router     │  Map URL → handler function
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Handler     │  Permission check → Execute → Response
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response    │  JSON / HTML / File
└─────────────┘
```

#### 2. URL Routing Rules

| URL Pattern | Handler | Mục đích | Ví dụ |
|-------------|---------|---------|-------|
| `/api/method/{dotted.path}` | Python function | Gọi whitelisted method | `/api/method/frappe.client.get_count` |
| `/api/resource/{doctype}` | REST CRUD | DocType API tự động | `/api/resource/Sales Order` |
| `/api/resource/{doctype}/{name}` | REST single doc | Lấy/sửa 1 document | `/api/resource/Sales Order/SO-0001` |
| `/app/{doctype}` | Desk List View | Frappe Desk UI | `/app/sales-order` |
| `/app/{doctype}/{name}` | Desk Form View | Xem/sửa form | `/app/sales-order/SO-0001` |
| `/{page_name}` | Website page | Public website | `/about`, `/blog` |
| `/printview` | Print format | In document | `/printview?doctype=SO&name=SO-0001` |

#### 3. API Method Call

```python
# Server side — khai báo whitelisted method
# Trong file: my_app/my_module/api.py

import frappe

@frappe.whitelist()
def get_book_status(book_name):
    """API endpoint: /api/method/my_app.my_module.api.get_book_status"""
    book = frappe.get_doc("Library Book", book_name)
    return {
        "status": book.status,
        "current_borrower": book.current_borrower
    }

@frappe.whitelist(allow_guest=True)
def get_public_books():
    """Guest có thể gọi — không cần đăng nhập"""
    return frappe.get_all("Library Book",
        filters={"status": "Available"},
        fields=["name", "title", "author"]
    )
```

```javascript
// Client side — gọi API từ browser
frappe.call({
    method: "my_app.my_module.api.get_book_status",
    args: { book_name: "BOOK-001" },
    callback: function(r) {
        if (r.message) {
            console.log("Status:", r.message.status);
        }
    }
});

// Hoặc dùng REST API trực tiếp
fetch("/api/method/my_app.my_module.api.get_book_status", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-Frappe-CSRF-Token": frappe.csrf_token
    },
    body: JSON.stringify({ book_name: "BOOK-001" })
});
```

#### 4. frappe.local — Thread-local Context

```python
# Mỗi request có context riêng, lưu trong frappe.local
frappe.local.site        # Tên site đang xử lý
frappe.local.request     # Werkzeug Request object
frappe.local.response    # Response dict
frappe.local.form_dict   # Request parameters (GET/POST merged)
frappe.local.session     # Session data (user, csrf_token, etc.)
frappe.local.db          # Database connection
frappe.local.cache       # Request-scoped cache

# Shortcut hay dùng:
frappe.session.user      # = frappe.local.session.user
frappe.form_dict         # = frappe.local.form_dict
frappe.db                # = frappe.local.db
```

### Code Examples

```python
# Trong bench console: test API routing
# docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console"

# Xem 1 route resolve như nào
import frappe
frappe.get_doc("Sales Order", "SO-00001")  # Direct doc access

# Xem tất cả whitelisted methods
whitelisted = frappe.get_all("Server Script",
    filters={"script_type": "API"},
    fields=["name", "api_method"]
)
print(whitelisted)

# Test REST API từ command line
# GET — lấy list
# curl http://flow.local:8000/api/resource/DocType?limit_page_length=5

# GET — lấy 1 doc
# curl http://flow.local:8000/api/resource/User/Administrator

# POST — tạo doc (cần auth)
# curl -X POST http://flow.local:8000/api/resource/ToDo \
#   -H "Authorization: token api_key:api_secret" \
#   -H "Content-Type: application/json" \
#   -d '{"description": "Test from API"}'
```

### Mini Quiz

<details>
<summary>Q1: URL để gọi function `erpnext.selling.api.get_item_price` qua API là gì?</summary>

**A:** `/api/method/erpnext.selling.api.get_item_price`. Tất cả whitelisted methods đều truy cập qua `/api/method/` + dotted path đến function.
</details>

<details>
<summary>Q2: Phân biệt `/api/resource/Sales Order` và `/app/sales-order`?</summary>

**A:** `/api/resource/Sales Order` — REST API, trả về JSON data (dùng cho API calls, integrations). `/app/sales-order` — Desk UI, render HTML form/list (dùng cho user truy cập qua browser). Lưu ý: API dùng tên gốc có space, Desk dùng slug lowercase có dash.
</details>

<details>
<summary>Q3: Decorator `@frappe.whitelist(allow_guest=True)` khác gì với `@frappe.whitelist()`?</summary>

**A:** `@frappe.whitelist()` — chỉ logged-in users mới gọi được (403 nếu chưa login). `@frappe.whitelist(allow_guest=True)` — bất kỳ ai cũng gọi được, kể cả Guest (chưa đăng nhập). Cẩn thận với `allow_guest` — chỉ dùng cho public data.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `references/api_reference/` để có full REST API reference
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-whitelisted/` để hiểu coding rules cho whitelisted methods

---

## L1.4: App Structure

### Tổng quan
Mỗi Frappe app có cấu trúc thư mục chuẩn, với `hooks.py` là file quan trọng nhất — nó "đăng ký" app của bạn với framework. Bài này đi sâu vào từng file và folder, đặc biệt là hooks.py với các event types. Hiểu rõ app structure là nền tảng để xây dựng bất kỳ custom app nào.

### Key Concepts

#### 1. App Directory Structure

```
my_app/
├── my_app/                     # Python package (trùng tên với app)
│   ├── __init__.py             # Package init
│   ├── hooks.py                # ⭐ QUAN TRỌNG NHẤT — đăng ký events, fixtures, etc.
│   ├── modules.txt             # Danh sách modules (1 dòng = 1 module)
│   ├── patches.txt             # Database migration patches
│   ├── templates/              # Jinja templates (email, print, web)
│   │   ├── pages/              # Website pages
│   │   └── includes/           # Shared template fragments
│   ├── www/                    # Public web pages (URL = folder path)
│   ├── public/                 # Static files (JS, CSS, images)
│   │   ├── js/
│   │   └── css/
│   ├── config/                 # App config
│   │   └── desktop.py          # Desktop icons (deprecated, dùng Workspace)
│   ├── my_module/              # Một module (tương ứng với 1 dòng trong modules.txt)
│   │   ├── doctype/            # DocTypes trong module này
│   │   │   └── my_doctype/
│   │   │       ├── my_doctype.json    # DocType definition (metadata)
│   │   │       ├── my_doctype.py      # Controller (Python)
│   │   │       ├── my_doctype.js      # Client Script (form behavior)
│   │   │       ├── my_doctype_list.js # List View customization
│   │   │       ├── test_my_doctype.py # Unit tests
│   │   │       └── __init__.py
│   │   ├── report/             # Script Reports
│   │   ├── workspace/          # Workspace definitions
│   │   ├── number_card/        # Dashboard Number Cards
│   │   └── dashboard_chart/    # Dashboard Charts
│   └── install.py              # Chạy sau install-app (setup data)
├── pyproject.toml              # Python package metadata (thay setup.py)
├── license.txt
└── README.md
```

#### 2. hooks.py — Chi tiết

```python
# hooks.py — "bộ não" của app

# === BASIC INFO ===
app_name = "my_app"
app_title = "My App"
app_publisher = "DCNET"
app_description = "Custom business modules"
app_version = "0.0.1"

# === DOCUMENT EVENTS ===
# Chạy code khi document thay đổi
doc_events = {
    # Cho 1 DocType cụ thể
    "Sales Order": {
        "validate": "my_app.overrides.sales_order.custom_validate",
        "on_submit": "my_app.overrides.sales_order.on_submit_handler",
        "on_cancel": "my_app.overrides.sales_order.on_cancel_handler",
    },
    # Cho TẤT CẢ DocTypes
    "*": {
        "after_insert": "my_app.utils.log_creation",
    }
}

# === SCHEDULER EVENTS ===
# Background jobs chạy định kỳ
scheduler_events = {
    "daily": [
        "my_app.tasks.daily_cleanup"
    ],
    "hourly": [
        "my_app.tasks.sync_inventory"
    ],
    "weekly": [
        "my_app.tasks.generate_weekly_report"
    ],
    "cron": {
        "0 9 * * 1-5": [  # 9h sáng, thứ 2-6
            "my_app.tasks.send_morning_summary"
        ]
    }
}

# === FIXTURES ===
# Export/import data khi migrate
fixtures = [
    # Export tất cả records của DocType
    "Custom Field",
    # Export có filter
    {"dt": "Custom Field", "filters": [["module", "=", "My Module"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My Module"]]},
]

# === JINJA ===
# Thêm functions/filters vào Jinja templates
jinja = {
    "methods": [
        "my_app.utils.jinja_methods.format_vnd"
    ],
}

# === WEBSITE ===
website_route_rules = [
    {"from_route": "/my-page/<name>", "to_route": "my_page"},
]

# === OVERRIDE ===
override_whitelisted_methods = {
    "frappe.client.get_count": "my_app.overrides.custom_get_count"
}

# === BOOT ===
# Data gửi xuống browser khi load trang
boot_session = "my_app.startup.boot.boot_session"

# === AFTER MIGRATE ===
# Chạy sau mỗi lần bench migrate
after_migrate = [
    "my_app.install.after_migrate"
]
```

#### 3. modules.txt

```
# Mỗi dòng = 1 module
# Module = nhóm các DocTypes liên quan
# Tên module PHẢI khớp với folder name (case-sensitive)
My Module
Another Module
```

> **Lưu ý:** Khi thêm module mới, PHẢI thêm vào modules.txt VÀ tạo folder tương ứng. Nếu không, `bench migrate` sẽ báo lỗi.

#### 4. patches.txt

```
# Data migration scripts — chạy 1 lần duy nhất
# Format: dotted.path.to.function
my_app.patches.v1_0.rename_old_field
my_app.patches.v1_1.migrate_customer_data
```

```python
# my_app/patches/v1_0/rename_old_field.py
import frappe

def execute():
    """Rename field 'old_name' to 'new_name' in My DocType"""
    if frappe.db.has_column("My DocType", "old_name"):
        frappe.db.sql("""
            UPDATE `tabMy DocType`
            SET new_name = old_name
            WHERE old_name IS NOT NULL
        """)
        frappe.db.commit()
```

#### 5. pyproject.toml (thay setup.py từ Frappe v15+)

```toml
[project]
name = "my_app"
dynamic = ["version"]

[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[tool.bench.frappe-dependencies]
frappe = ">=16.0.0"
erpnext = ">=16.0.0"
```

### Code Examples

```bash
# Tạo app mới trong devcontainer
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench new-app frappe_learn"

# Xem cấu trúc app vừa tạo
docker exec devcontainer-frappe-1 bash -c "ls -la /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/"

# Xem hooks.py mặc định
docker exec devcontainer-frappe-1 bash -c "cat /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/hooks.py"

# Xem modules.txt
docker exec devcontainer-frappe-1 bash -c "cat /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/modules.txt"

# Cài app vào site
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local install-app frappe_learn"
```

### Mini Quiz

<details>
<summary>Q1: Bạn muốn chạy custom code mỗi khi Sales Order được submit. Cấu hình ở đâu trong hooks.py?</summary>

**A:** Trong `doc_events`:
```python
doc_events = {
    "Sales Order": {
        "on_submit": "my_app.overrides.sales_order.handle_submit"
    }
}
```
Sau đó tạo file `my_app/overrides/sales_order.py` với function `handle_submit(doc, method)`.
</details>

<details>
<summary>Q2: Sau khi thêm module "Library" vào modules.txt, bạn cần làm gì nữa?</summary>

**A:** Phải tạo folder `my_app/library/` (lowercase, khớp với tên module) với file `__init__.py`. Sau đó chạy `bench --site <site> migrate` để Frappe nhận module mới. Nếu chỉ thêm vào modules.txt mà không tạo folder → lỗi.
</details>

<details>
<summary>Q3: `fixtures` trong hooks.py dùng để làm gì? Khi nào chúng được apply?</summary>

**A:** `fixtures` định nghĩa data cần export vào JSON files và tự động import khi `bench migrate`. Thường dùng cho: Custom Fields, Property Setters, Roles, Workflows — những thứ cần đồng bộ giữa dev và production. Data được lưu trong `my_app/fixtures/` folder.
</details>

### Skill References

- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-hooks/` để hiểu tất cả hook types và coding rules
- **DEEP DIVE:** Xem skill `dcnet_quality` -> `syntax/erpnext-syntax-customapp/` để hiểu best practices khi xây dựng custom app
- **DEEP DIVE:** Xem skill `frappe` -> `references/patterns/` để hiểu các patterns thường dùng

---

## L1.5: Quiz + Practice

### Tổng quan
Tổng hợp kiến thức từ 4 bài trước thành 10 câu quiz và 1 bài tập thực hành. Bài tập yêu cầu tạo app "frappe_learn" trên devcontainer — đây là app sẽ dùng xuyên suốt các module tiếp theo. Hoàn thành bài này trước khi sang Module 2.

### Tổng hợp Quiz (10 câu)

<details>
<summary>Q1: Frappe Framework viết bằng ngôn ngữ gì?</summary>

**A:** **Python** (backend) và **JavaScript** (frontend). Template dùng **Jinja2**. CSS dùng **SCSS**. Database: **MariaDB** (mặc định) hoặc PostgreSQL.
</details>

<details>
<summary>Q2: Bench, Frappe, Site — giải thích mối quan hệ?</summary>

**A:** **Bench** = CLI tool + directory structure quản lý apps và sites. **Frappe** = web framework (1 app trong bench). **Site** = 1 instance với database riêng. Quan hệ: Bench chứa nhiều Apps, Bench chứa nhiều Sites, mỗi Site cài một số Apps.
</details>

<details>
<summary>Q3: Lệnh nào để tạo app mới? Lệnh nào để cài app vào site?</summary>

**A:** `bench new-app <app_name>` — tạo app. `bench --site <site> install-app <app_name>` — cài app vào site.
</details>

<details>
<summary>Q4: DocType "Purchase Invoice" tương ứng với table nào trong database?</summary>

**A:** `tabPurchase Invoice`. Tất cả DocTypes có prefix `tab`.
</details>

<details>
<summary>Q5: Phân biệt `bench migrate` và `bench build`?</summary>

**A:** `bench migrate` — cập nhật database schema (ALTER TABLE), chạy patches, sync fixtures. `bench build` — compile JS/CSS assets (webpack). Hai lệnh khác nhau hoàn toàn — migrate cho data, build cho frontend.
</details>

<details>
<summary>Q6: URL pattern `/api/resource/Item/ITEM-001` làm gì?</summary>

**A:** REST API — lấy document `Item` có name `ITEM-001`. Method GET = đọc, PUT = update, DELETE = delete. Trả về JSON.
</details>

<details>
<summary>Q7: File nào trong app là quan trọng nhất và tại sao?</summary>

**A:** `hooks.py` — nó "đăng ký" app với Frappe framework. Không có hooks.py, Frappe không biết app của bạn muốn làm gì: không doc_events, không scheduler, không fixtures, không overrides.
</details>

<details>
<summary>Q8: `@frappe.whitelist()` decorator dùng để làm gì?</summary>

**A:** Cho phép function được gọi từ client (browser) qua `/api/method/`. Không có decorator này, function KHÔNG THỂ gọi từ frontend — Frappe sẽ trả 403. Thêm `allow_guest=True` để cho phép user chưa đăng nhập gọi.
</details>

<details>
<summary>Q9: Khi nào dùng `doc_events` và khi nào dùng Controller method?</summary>

**A:** `doc_events` (hooks.py) — khi muốn hook vào DocType của APP KHÁC (VD: hook vào Sales Order của ERPNext). Controller method — khi viết logic cho DocType của CHÍNH MÌNH (VD: validate() trong my_doctype.py). Cả hai đều chạy trên cùng lifecycle, nhưng doc_events linh hoạt hơn cho cross-app.
</details>

<details>
<summary>Q10: `bench --site flow.local console` cho bạn làm gì?</summary>

**A:** Mở Python REPL (interactive shell) với Frappe context đã load — site đã connect, database đã sẵn sàng. Bạn có thể gọi `frappe.get_doc()`, `frappe.db.sql()`, `frappe.get_all()` trực tiếp. Tuyệt vời để test nhanh code trước khi viết vào file.
</details>

### Bài tập thực hành: Tạo app "frappe_learn"

> **Mục tiêu:** Tạo Frappe app đầu tiên, cài đặt vào site, verify hoạt động.

#### Bước 1: Tạo app

```bash
# Vào devcontainer
docker exec -it devcontainer-frappe-1 bash

# Di chuyển đến bench
cd /workspace/development/frappe-bench

# Tạo app mới
bench new-app frappe_learn
# Trả lời:
#   App Title: Frappe Learn
#   App Description: Learning Frappe Framework
#   App Publisher: DCNET
#   App Email: dev@dcnet.vn
#   App License: MIT
```

#### Bước 2: Cài app vào site

```bash
bench --site flow.local install-app frappe_learn

# Verify
bench --site flow.local list-apps
# Kết quả phải có: frappe_learn
```

#### Bước 3: Kiểm tra cấu trúc

```bash
ls -la apps/frappe_learn/frappe_learn/
# Phải thấy:
# hooks.py, modules.txt, __init__.py, templates/, public/, etc.

cat apps/frappe_learn/frappe_learn/modules.txt
# Phải thấy: Frappe Learn

cat apps/frappe_learn/frappe_learn/hooks.py
# Xem nội dung mặc định
```

#### Bước 4: Test console

```bash
bench --site flow.local console

# Trong console:
>>> import frappe_learn
>>> print(frappe_learn.__path__)
# Phải in ra path đến app

>>> frappe.get_installed_apps()
# Phải có 'frappe_learn' trong list

>>> exit()
```

#### Bước 5: Sửa hooks.py (tùy chọn)

```python
# Thêm vào hooks.py:
app_logo_url = "/assets/frappe_learn/images/logo.png"

# Sau đó chạy:
# bench --site flow.local clear-cache
```

#### Kiểm tra hoàn thành

- [ ] App `frappe_learn` đã tạo thành công
- [ ] App đã cài vào site `flow.local`
- [ ] `bench --site flow.local list-apps` hiển thị `frappe_learn`
- [ ] Console import được `frappe_learn`
- [ ] Hiểu cấu trúc folder của app

> **Tiếp theo:** Module 2 sẽ dùng app `frappe_learn` để tạo DocTypes — Library Book, Library Member, Library Transaction.

### Skill References

- **DEEP DIVE:** Xem skill `frappe` -> `references/tutorials/` để có thêm bài tập nâng cao
- **DEEP DIVE:** Xem skill `frappe` -> `test_examples/` để hiểu cách viết tests cho Frappe apps
