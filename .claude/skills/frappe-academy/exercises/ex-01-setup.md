# Module 1 Exercises: Frappe Foundation
# Bài tập Module 1: Nền tảng Frappe

> **Environment / Môi trường:**
> - Container: `devcontainer-frappe-1`
> - Bench path: `/workspace/development/frappe-bench`
> - Site: `flow.local`
> - Prefix for all commands:
>   ```bash
>   docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && <command>"
>   ```

---

## Exercise 1.1: Khám phá bench environment / Explore bench environment

### Mục tiêu / Objective
Làm quen với Frappe bench — hiểu cấu trúc thư mục, các app đã cài, version hiện tại.
Get familiar with the Frappe bench — understand directory structure, installed apps, and current versions.

### Bước thực hiện / Steps

**Step 1:** List tất cả apps đã cài trên site / List all installed apps on the site
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local list-apps"
```

**Step 2:** Kiểm tra version Frappe / Check Frappe version
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench version"
```

**Step 3:** Xem cấu trúc thư mục bench / View bench directory structure
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && ls -la"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && ls -la apps/"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && ls -la sites/"
```

**Step 4:** Xem các site hiện có / List existing sites
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local show-config"
```

**Step 5:** Kiểm tra trạng thái site / Check site status
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local doctor"
```

### Kết quả mong đợi / Expected Output
- Bạn thấy được danh sách apps: `frappe`, `erpnext`, `dcnet_apps` (hoặc tương tự)
- Version Frappe là v16.x
- Thư mục `apps/` chứa source code của các app
- Thư mục `sites/` chứa config và database của từng site

### Kiểm tra / Verification
```bash
# Tất cả các lệnh trên chạy không lỗi
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench version" | grep "frappe"
```

<details>
<summary>Gợi ý / Hints</summary>

- `bench version` trả về version của **tất cả apps**, không chỉ frappe
- `sites/flow.local/` chứa `site_config.json` — file cấu hình riêng của site
- `apps/frappe/` là framework core, `apps/erpnext/` là ERP module
- Nếu `bench doctor` báo lỗi Redis/MariaDB, kiểm tra các service trong container đã chạy chưa

</details>

---

## Exercise 1.2: Tạo custom app "frappe_learn" / Create custom app "frappe_learn"

### Mục tiêu / Objective
Tạo một Frappe app mới từ đầu, hiểu cấu trúc file của một app.
Create a new Frappe app from scratch, understand the file structure of an app.

### Bước thực hiện / Steps

**Step 1:** Tạo app mới / Create new app
```bash
docker exec -it devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench new-app frappe_learn"
```

> **Lưu ý / Note:** Lệnh này sẽ hỏi bạn một số câu hỏi (app title, description, publisher, email). Nhập như sau:
> - App Title: `Frappe Learn`
> - App Description: `Learning exercises for Frappe Framework`
> - App Publisher: `DCNET`
> - App Email: `learn@dcnet.vn`
> - App License: `MIT`

**Step 2:** Xem cấu trúc app vừa tạo / View the created app structure
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && find apps/frappe_learn -type f | head -30"
```

**Step 3:** Xem nội dung file `pyproject.toml` / View pyproject.toml
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && cat apps/frappe_learn/pyproject.toml"
```

**Step 4:** Xem nội dung file `modules.txt` / View modules.txt
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && cat apps/frappe_learn/frappe_learn/modules.txt"
```

**Step 5:** Xem nội dung file `hooks.py` / View hooks.py
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && cat apps/frappe_learn/frappe_learn/hooks.py"
```

### Kết quả mong đợi / Expected Output
- Thư mục `apps/frappe_learn/` được tạo thành công
- `pyproject.toml` chứa metadata của app (name, version, dependencies)
- `modules.txt` chứa tên module mặc định: `Frappe Learn`
- `hooks.py` chứa cấu hình cơ bản: `app_name`, `app_title`, `app_publisher`
- Cấu trúc thư mục:
  ```
  frappe_learn/
  ├── pyproject.toml
  ├── frappe_learn/
  │   ├── __init__.py
  │   ├── hooks.py
  │   ├── modules.txt
  │   ├── patches.txt
  │   ├── templates/
  │   └── frappe_learn/      # module folder (same name as app)
  │       └── __init__.py
  ```

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && test -f apps/frappe_learn/pyproject.toml && echo 'OK: pyproject.toml exists' || echo 'FAIL: pyproject.toml missing'"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && test -f apps/frappe_learn/frappe_learn/hooks.py && echo 'OK: hooks.py exists' || echo 'FAIL: hooks.py missing'"
```

<details>
<summary>Gợi ý / Hints</summary>

- `bench new-app` tự động tạo cấu trúc thư mục chuẩn cho Frappe app
- Trong Frappe v16, `pyproject.toml` thay thế `setup.py` (Python packaging standard mới)
- `modules.txt` định nghĩa các module của app — mỗi dòng là một module name
- Nếu bạn gặp lỗi "app already exists", xóa thư mục cũ: `rm -rf apps/frappe_learn`
- Tên app phải là snake_case (VD: `frappe_learn`, KHÔNG PHẢI `frappe-learn`)

</details>

---

## Exercise 1.3: Cài app vào site / Install app on site

### Mục tiêu / Objective
Cài app `frappe_learn` vào site `flow.local` và xác nhận app hoạt động.
Install the `frappe_learn` app on site `flow.local` and verify it works.

### Bước thực hiện / Steps

**Step 1:** Cài app vào site / Install app on site
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local install-app frappe_learn"
```

**Step 2:** Xác nhận app đã cài thành công / Verify app is installed
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local list-apps"
```

**Step 3:** Chạy migrate để đồng bộ / Run migrate to sync
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

**Step 4:** Clear cache / Clear cache
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

**Step 5:** Kiểm tra qua API / Verify via API
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
apps = frappe.get_installed_apps()
print("Installed apps:", apps)
print("frappe_learn installed:", "frappe_learn" in apps)
EOF
```

### Kết quả mong đợi / Expected Output
- `bench --site flow.local list-apps` hiển thị `frappe_learn` trong danh sách
- Migrate chạy thành công, không lỗi
- API trả về `frappe_learn installed: True`

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local list-apps" | grep "frappe_learn"
```

<details>
<summary>Gợi ý / Hints</summary>

- `install-app` sẽ tự động tạo Module Def record trong database
- Nếu gặp lỗi "App not found", kiểm tra `apps/frappe_learn` có tồn tại không
- Nếu gặp lỗi "App already installed", app đã được cài rồi — không cần làm gì thêm
- `bench migrate` là lệnh quan trọng nhất — chạy mỗi khi thay đổi schema (DocType, Custom Field...)
- `bench clear-cache` giúp làm sạch cache khi UI không cập nhật

</details>

---

## Exercise 1.4: Tạo Module "Library" / Create "Library" Module

### Mục tiêu / Objective
Tạo module "Library" trong app `frappe_learn` — đây là namespace để chứa các DocType sau này.
Create a "Library" module inside `frappe_learn` app — this is the namespace for DocTypes later.

### Bước thực hiện / Steps

**Step 1:** Tạo thư mục module / Create module directory
```bash
docker exec devcontainer-frappe-1 bash -c "mkdir -p /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library"
docker exec devcontainer-frappe-1 bash -c "touch /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/library/__init__.py"
```

**Step 2:** Thêm module vào `modules.txt` / Add module to modules.txt
```bash
docker exec devcontainer-frappe-1 bash -c "echo 'Library' >> /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/modules.txt"
```

**Step 3:** Xem lại nội dung modules.txt / Verify modules.txt content
```bash
docker exec devcontainer-frappe-1 bash -c "cat /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/modules.txt"
```

**Step 4:** Chạy migrate để tạo Module Def / Run migrate to create Module Def
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

**Step 5:** Xác nhận Module Def đã được tạo / Verify Module Def was created
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
module = frappe.get_doc("Module Def", "Library")
print(f"Module: {module.module_name}")
print(f"App: {module.app_name}")
EOF
```

### Kết quả mong đợi / Expected Output
- Thư mục `frappe_learn/library/` được tạo với `__init__.py`
- `modules.txt` chứa 2 dòng: `Frappe Learn` và `Library`
- Migrate thành công
- Console hiển thị: `Module: Library`, `App: frappe_learn`

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
exists = frappe.db.exists("Module Def", "Library")
print(f"Module 'Library' exists: {bool(exists)}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- Mỗi module trong Frappe tương ứng với 1 record "Module Def" trong database
- Tên module trong `modules.txt` phải CHÍNH XÁC khớp với tên thư mục (case-sensitive mapping: "Library" → `library/`)
- Frappe tự động convert: "Library Management" → `library_management/` (lowercase + underscore)
- Nếu module không xuất hiện sau migrate, kiểm tra: (1) modules.txt có đúng tên không, (2) thư mục có `__init__.py` không
- Một app có thể có nhiều modules — mỗi module là một nhóm DocTypes liên quan

</details>

---

## Exercise 1.5: Khám phá hooks.py / Explore hooks.py

### Mục tiêu / Objective
Hiểu cấu trúc và các tùy chọn cấu hình trong `hooks.py` — file trung tâm của mỗi Frappe app.
Understand the structure and configuration options in `hooks.py` — the central file of every Frappe app.

### Bước thực hiện / Steps

**Step 1:** Mở và đọc hooks.py hiện tại / Read current hooks.py
```bash
docker exec devcontainer-frappe-1 bash -c "cat /workspace/development/frappe-bench/apps/frappe_learn/frappe_learn/hooks.py"
```

**Step 2:** Chỉnh sửa hooks.py — thêm app_title và app_description / Edit hooks.py
Sửa file `apps/frappe_learn/frappe_learn/hooks.py` với nội dung sau:

```python
app_name = "frappe_learn"
app_title = "Frappe Learn"
app_publisher = "DCNET"
app_description = "Learning exercises for Frappe Framework"
app_email = "learn@dcnet.vn"
app_license = "MIT"
app_version = "0.1.0"

# App icon and color (shows on Desk)
app_icon = "octicon octicon-book"
app_color = "#3498db"

# Includes in <head>
# ------------------
# app_include_css = "/assets/frappe_learn/css/frappe_learn.css"
# app_include_js = "/assets/frappe_learn/js/frappe_learn.js"

# Document Events
# ---------------
# doc_events = {
#     "Library Transaction": {
#         "after_insert": "frappe_learn.library.notifications.send_borrow_notification"
#     }
# }

# Scheduled Tasks
# ---------------
# scheduler_events = {
#     "daily": [
#         "frappe_learn.library.tasks.check_overdue_books"
#     ]
# }

# Fixtures
# --------
# fixtures = [
#     {"dt": "Custom Field", "filters": [["module", "=", "Library"]]}
# ]
```

**Step 3:** Xem hooks.py của frappe (framework) để tham khảo / View frappe's hooks.py for reference
```bash
docker exec devcontainer-frappe-1 bash -c "head -50 /workspace/development/frappe-bench/apps/frappe/frappe/hooks.py"
```

**Step 4:** Xem hooks.py của erpnext để tham khảo / View erpnext's hooks.py for reference
```bash
docker exec devcontainer-frappe-1 bash -c "head -50 /workspace/development/frappe-bench/apps/erpnext/erpnext/hooks.py"
```

**Step 5:** Clear cache và kiểm tra / Clear cache and verify
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

### Kết quả mong đợi / Expected Output
- `hooks.py` đã được cập nhật với `app_title`, `app_description`, `app_icon`, `app_color`
- Bạn hiểu các section chính trong hooks.py:
  - **App metadata:** `app_name`, `app_title`, `app_publisher`, `app_version`
  - **Includes:** CSS/JS files để inject vào trang web
  - **Document Events:** Hook vào lifecycle của DocType (before_save, after_insert, on_submit...)
  - **Scheduled Tasks:** Cron jobs (daily, hourly, weekly, monthly, cron)
  - **Fixtures:** Export/import data từ database (Custom Field, Property Setter...)

### Kiểm tra / Verification
```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local console" <<'EOF'
from frappe_learn import hooks
print(f"App Title: {hooks.app_title}")
print(f"App Description: {hooks.app_description}")
print(f"App Version: {hooks.app_version}")
EOF
```

<details>
<summary>Gợi ý / Hints</summary>

- `hooks.py` là file QUAN TRỌNG NHẤT của mỗi Frappe app — nó là "điểm kết nối" giữa app và framework
- Tất cả các hook đều là Python dict/list — Frappe đọc và merge chúng từ tất cả apps
- Thứ tự app trong `sites/apps.txt` quyết định thứ tự ưu tiên khi có conflict
- `doc_events` là cách để app này hook vào DocType của app khác (cross-app integration)
- `scheduler_events` chạy bởi `bench schedule` process — phải đảm bảo process này đang chạy
- Frappe docs chính thức về hooks: https://frappeframework.com/docs/user/en/python-api/hooks
- **KHÔNG BAO GIỜ** import trực tiếp từ hooks.py trong production code — dùng `frappe.get_hooks()`

</details>

---

## Tổng kết Module 1 / Module 1 Summary

Sau khi hoàn thành tất cả bài tập, bạn đã:
After completing all exercises, you have:

| # | Kỹ năng / Skill | Trạng thái / Status |
|---|-----------------|---------------------|
| 1.1 | Hiểu bench environment và cấu trúc thư mục | [ ] |
| 1.2 | Tạo Frappe app mới từ đầu | [ ] |
| 1.3 | Cài app vào site và kiểm tra | [ ] |
| 1.4 | Tạo module trong app | [ ] |
| 1.5 | Hiểu và cấu hình hooks.py | [ ] |

### Verification toàn bộ / Full Module Verification
```bash
# Chạy tất cả kiểm tra cùng lúc
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && \
  echo '=== Apps ===' && bench --site flow.local list-apps && \
  echo '=== Module Def ===' && bench --site flow.local console <<'PYEOF'
print('frappe_learn installed:', 'frappe_learn' in frappe.get_installed_apps())
print('Library module exists:', bool(frappe.db.exists('Module Def', 'Library')))
PYEOF"
```

> **Tiếp theo / Next:** [Exercise 02 - DocType Mastery](ex-02-doctype.md)
