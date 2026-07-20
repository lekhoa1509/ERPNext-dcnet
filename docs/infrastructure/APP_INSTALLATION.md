# Hướng dẫn cài đặt Apps - DCNET Flow

> Tài liệu ghi lại toàn bộ quá trình cài đặt các app trong development environment.

## Tổng quan hệ thống Apps

| # | App | Source | Loại | Ghi chú |
|---|-----|--------|------|---------|
| 1 | `frappe` | `bench init --frappe-branch version-16` | Framework | Auto-install |
| 2 | `erpnext` | Symlink `/workspace/dcnet_core` | Core ERP | Cài qua `installer.py` |
| 3 | `dcnet_apps` | Symlink `/workspace/dcnet_apps` | Custom modules | Cài qua `installer.py` |
| 4 | `dcnet_fixtures` | Symlink `/workspace/dcnet_apps/dcnet_fixtures` | Demo data | Cài thủ công |
| 5 | `hrms` | Folder `dcnet_hrms` (clone từ `frappe/hrms` v16) | HR Module | Symlink như erpnext |

---

## 1. Setup ban đầu (Auto - `installer.py`)

Container: `devcontainer-frappe-1` | Site: `flow.local` | Admin: `123456`

```bash
# Khi mở devcontainer lần đầu, installer.py tự chạy:
cd /workspace/development
python installer.py
```

**`installer.py` tự động làm:**
1. `bench init --frappe-branch version-16 frappe-bench`
2. Config Redis, MariaDB (mariadb/redis-cache/redis-queue)
3. Symlink `erpnext` → `/workspace/dcnet_core`, `dcnet_apps` → `/workspace/dcnet_apps`
4. `pip install -e` cho mỗi app + thêm vào `apps.txt`
5. `yarn add onscan.js` (cho POS)
6. `bench new-site flow.local` (admin password: `123456`)
7. `bench --site flow.local install-app erpnext`
8. `bench --site flow.local install-app dcnet_apps`
9. `bench use flow.local` + enable scheduler + developer_mode

**Sau install:** `bench start` tự chạy via `postStartCommand` trong `devcontainer.json`.

---

## 2. Cài `dcnet_fixtures` (Thủ công)

> `dcnet_fixtures` là app riêng nằm trong `/workspace/dcnet_apps/dcnet_fixtures/`.
> Không nằm trong `installer.py`, cần cài thủ công.

```bash
# Bước 1: Symlink + pip install + thêm apps.txt
cd /workspace/development/frappe-bench
ln -sf /workspace/dcnet_apps/dcnet_fixtures apps/dcnet_fixtures
pip install -e apps/dcnet_fixtures
echo "dcnet_fixtures" >> sites/apps.txt

# Bước 2: Install app trên site
bench --site flow.local install-app dcnet_fixtures

# Bước 3: Generate demo data
bench --site flow.local dcnet-fixtures generate

# Các lệnh khác
bench --site flow.local dcnet-fixtures status          # Xem trạng thái
bench --site flow.local dcnet-fixtures clear --force    # Xóa toàn bộ demo data
bench --site flow.local dcnet-fixtures generate --module master  # Chỉ master data
```

---

## 3. Cài `hrms` (Frappe HR)

> Source: https://github.com/frappe/hrms (branch `version-16`)
> Cách tiếp cận: Giống `dcnet_core` (ERPNext) — clone vào folder `dcnet_hrms`, xóa `.git`, track trong repo chung.

### Đã làm (trên host):

```bash
# Clone HRMS v16 vào folder dcnet_hrms
git clone --branch version-16 --depth 1 https://github.com/frappe/hrms.git dcnet_hrms

# Xóa .git để track trong repo chung (không phải submodule)
rm -rf dcnet_hrms/.git
```

### Cài trong container (lần đầu hoặc khi chưa có):

```bash
cd /workspace/development/frappe-bench
ln -sf /workspace/dcnet_hrms apps/hrms
pip install -e apps/hrms
echo "hrms" >> sites/apps.txt
bench --site flow.local install-app hrms
bench --site flow.local migrate
```

> **Lần sau:** `installer.py` đã được update, tự động symlink + install HRMS.

### Cập nhật HRMS lên version mới:

```bash
# Trên host (ngoài container)
cd dcnet_hrms
# Download source mới từ GitHub, copy đè vào dcnet_hrms
# Hoặc dùng git archive:
# git archive --remote=https://github.com/frappe/hrms --prefix=dcnet_hrms/ version-16 | tar -x

# Trong container
cd /workspace/development/frappe-bench
pip install -e apps/hrms
bench --site flow.local migrate
```

**HRMS cung cấp:**
- Employee, Department, Designation
- Leave Management (Nghỉ phép)
- Attendance (Chấm công)
- Payroll (Bảng lương)
- Expense Claims (Chi phí)
- Shift Management (Ca làm việc)

---

## 4. Cài app từ local path (Template chung)

Khi cần thêm app mới (local hoặc git):

### Từ local path

```bash
cd /workspace/development/frappe-bench

# Symlink
ln -sf /path/to/app apps/{app_name}

# Install dependencies
pip install -e apps/{app_name}

# Thêm vào danh sách apps
echo "{app_name}" >> sites/apps.txt

# Install trên site
bench --site flow.local install-app {app_name}

# Migrate
bench --site flow.local migrate
```

### Từ GitHub

```bash
cd /workspace/development/frappe-bench

# Clone
cd apps && git clone --branch {branch} --depth 1 {git_url} && cd ..

# Install
pip install -e apps/{app_name}
echo "{app_name}" >> sites/apps.txt
bench --site flow.local install-app {app_name}
bench --site flow.local migrate
```

---

## 5. Gỡ app

```bash
# Gỡ app khỏi site
bench --site flow.local uninstall-app {app_name} --yes

# Xóa symlink
rm apps/{app_name}

# Xóa khỏi apps.txt (thủ công hoặc dùng sed)
# Sửa file sites/apps.txt, xóa dòng {app_name}
```

---

## 6. Troubleshooting

### Port 9000 bị chiếm khi `bench start`

`postStartCommand` trong `devcontainer.json` đã chạy `bench start` ở background.
Không cần chạy lại thủ công. Nếu muốn restart:

```bash
pkill -f "bench start"
# Đợi 2 giây
cd /workspace/development/frappe-bench && bench start
```

### Lỗi `bench get-app` với local path

Bench version cũ không hỗ trợ local path qua `get-app`. Dùng cách thủ công:
`ln -sf` + `pip install -e` + thêm `apps.txt`.

### Lỗi `No such command: xxx`

App chưa được install hoặc chưa có trong `apps.txt`. Check:

```bash
bench --site flow.local list-apps    # Xem apps đã install
cat sites/apps.txt                    # Xem apps.txt
```

### Lỗi Workspace thiếu field `type`

ERPNext v16 yêu cầu Workspace JSON phải có `"type": "Workspace"`.
Nếu fixture có `"type": null` → sửa thành `"type": "Workspace"`.

### Lỗi `bench migrate` thiếu `--site`

```bash
# Sai
bench migrate

# Đúng
bench --site flow.local migrate
```

---

## 7. Thứ tự apps hiện tại (`sites/apps.txt`)

```
frappe
erpnext
hrms
dcnet_apps
dcnet_fixtures
```

> **Quan trọng:** Thứ tự trong `apps.txt` quyết định thứ tự migrate.
> `frappe` → `erpnext` → `dcnet_apps` → `dcnet_fixtures` → (hrms khi cài thêm)

---

**Last Updated:** 2026-03-08
