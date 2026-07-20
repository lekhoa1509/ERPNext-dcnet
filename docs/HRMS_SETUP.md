# HRMS Setup Guide

Hướng dẫn cài đặt app HRMS (Frappe HR) vào môi trường dev DCNET Flow.

## Yêu cầu

- Docker container `devcontainer-frappe-1` đang chạy
- Bench đã được init với Frappe + ERPNext

## Cài đặt

### Bước 1: Start container

```bash
cd flow_next
docker compose -f .devcontainer/docker-compose.yml up -d
```

### Bước 2: Vào container

```bash
docker exec -it devcontainer-frappe-1 bash
cd /workspace/development/frappe-bench
```

### Bước 3: Link app HRMS

```bash
# Tạo symlink
ln -s /workspace/dcnet_hrms apps/hrms

# Cài Python dependencies
./env/bin/pip install -e apps/hrms

# Thêm vào apps.txt
grep -q "hrms" sites/apps.txt || echo "hrms" >> sites/apps.txt
```

### Bước 4: Cài dependencies JS

```bash
# html2canvas cần cài vào frappe (esbuild resolve từ đây)
cd apps/frappe && yarn add html2canvas && cd ../..
```

### Bước 5: Tạo symlink /sites (fix build frontend)

HRMS frontend (`socket.js`) dùng relative path `../../../../sites/common_site_config.json`.
Do `apps/hrms` là symlink tới `/workspace/dcnet_hrms`, path resolve ra `/sites/` thay vì `frappe-bench/sites/`.

```bash
# Cần quyền root
exit
docker exec -u root devcontainer-frappe-1 ln -sf /workspace/development/frappe-bench/sites /sites
docker exec -it devcontainer-frappe-1 bash
cd /workspace/development/frappe-bench
```

> **Lưu ý:** Symlink này đã được thêm vào `development/start-bench.sh`, sẽ tự tạo khi restart container. Chỉ cần chạy tay lần đầu.

### Bước 6: Install app lên site + build

```bash
# Install app
bench --site flow.local install-app hrms

# Build tất cả assets (frappe + erpnext + hrms + dcnet_apps)
bench build

# Migrate để tạo DocTypes
bench --site flow.local migrate

# Clear cache
bench --site flow.local clear-cache
```

> **Không cần restart bench.** Bench đang chạy sẵn (docker compose entrypoint tự start).
> Chỉ cần hard refresh browser: `Cmd+Shift+R` (Mac) / `Ctrl+Shift+R` (Windows).

## Truy cập

| URL | Mô tả |
|-----|-------|
| `http://localhost:8000` | ERPNext Desk (có HR module) |
| `http://localhost:8000/hrms` | HRMS Mobile PWA |

Login: `Administrator` / `123456`

## Test Mobile

### Chrome DevTools (nhanh nhất)

1. Mở `http://localhost:8000/hrms`
2. `F12` → click icon mobile (hoặc `Cmd+Shift+M`) → chọn device (iPhone, Pixel...)

### iOS Simulator (Mac)

```bash
# Trỏ Xcode path (1 lần duy nhất)
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -license accept

# Mở Simulator
open -a Simulator
```

Trong Simulator: Safari → `http://localhost:8000/hrms` → Share → **Add to Home Screen** → chạy như app thật.

### Điện thoại thật (cùng WiFi)

Truy cập `http://<IP-mac>:8000/hrms` (xem IP: `ipconfig getifaddr en0`)

## Chạy HRMS Frontend (dev mode, hot reload)

```bash
cd /workspace/dcnet_hrms/frontend
yarn install
yarn dev
# Truy cập: http://localhost:8080
```

## Troubleshooting

### Lỗi `html2canvas` khi build

```
Could not resolve "html2canvas"
```

**Fix:** Cài vào frappe, không phải hrms:

```bash
cd /workspace/development/frappe-bench/apps/frappe
yarn add html2canvas
```

### Lỗi `common_site_config.json` khi build frontend

```
Could not resolve "../../../../sites/common_site_config.json"
```

**Fix:** Tạo symlink `/sites`:

```bash
docker exec -u root devcontainer-frappe-1 ln -sf /workspace/development/frappe-bench/sites /sites
```

### Lỗi 404 assets (desk.bundle.xxx.css)

Assets cũ bị cache hash khác. **Fix:**

```bash
bench build
bench --site flow.local clear-cache
# Hard refresh browser: Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows)
```

### Lỗi `DocType Job Opening not found`

Chưa migrate. **Fix:**

```bash
bench --site flow.local migrate
```

### Lỗi icon "not correctly configured"

Lỗi từ dcnet_apps desktop icons, không ảnh hưởng HRMS. Bỏ qua được.
