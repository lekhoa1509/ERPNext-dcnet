# DCNET Flow - VM Deployment Plan (Bare Metal)

> **Version:** 2.0
> **Created:** 08/03/2026
> **Status:** Draft - Chờ duyệt
> **Target:** Staging/Demo → Production
> **Author:** DCNET Team

---

## Overview

Triển khai DCNET Flow lên VM bare metal (không Docker), giữ đồng bộ source với local dev qua Git.

> **Lưu ý:** Frappe chính thức khuyến nghị Docker cho production. Tài liệu này dùng bare metal theo yêu cầu dự án, bám sát [Frappe Installation Docs](https://docs.frappe.io/framework/user/en/installation) và [Production Setup](https://docs.frappe.io/framework/user/en/bench/guides/setup-production).

| Item | Value |
|------|-------|
| **Server IP** | 163.227.121.154 |
| **OS** | Ubuntu 24.04 LTS (khuyến nghị) hoặc 22.04 LTS |
| **CPU** | 16 vCPU |
| **RAM** | 32 GB |
| **Mục đích** | Staging/Demo → Production |
| **Domain** | flow-demo.dcnet.vn (team admin trỏ về IP public) |

### Stack (Theo Frappe v16 Official Requirements)

| Component | Version | Nguồn |
|-----------|---------|-------|
| **Python** | **3.14** | `pyproject.toml`: `>=3.14,<3.15` (BẮT BUỘC) |
| **Node.js** | **24** | Frappe docs: Node 24 cho v16 |
| **MariaDB** | **11.8** | Frappe docs: MariaDB 11.8 cho v16 |
| **Redis/Valkey** | **6+** | Frappe docs |
| **Yarn** | **1.22+** | Frappe docs |
| **pip** | **25.3+** | Frappe docs |
| **wkhtmltopdf** | **0.12.6** | Patched Qt version |
| **Nginx** | latest | Reverse proxy + SSL |
| **Supervisor** | latest | Process manager |
| **Frappe** | 16.x | Branch `version-16` |
| **ERPNext** | 16.x | Từ `dcnet_core/` (monorepo) |
| **dcnet_apps** | 1.x | Custom modules |

> **QUAN TRỌNG:** Frappe v16 yêu cầu **chính xác Python 3.14.x** (không phải 3.12 hay 3.13). Đây là hard requirement trong `pyproject.toml`. Cài qua deadsnakes PPA trên Ubuntu 22.04/24.04.

---

## Git Sync Strategy

### Monorepo Structure

```
flow_next/                    ← Git repo (clone trên cả local + server)
├── dcnet_core/               ← ERPNext v16 source
├── dcnet_apps/               ← Custom modules
│   └── dcnet_fixtures/       ← Sample data (chỉ dùng staging)
├── docs/                     ← Documentation (không ảnh hưởng runtime)
└── development/              ← Dev only (không dùng trên server)
```

### Sync Flow

```
[Local Dev] ──push──→ [GitHub: develop] ──pull──→ [Server: /home/frappe/flow_next]
                                                         │
                                                    symlink vào
                                                         ↓
                                              frappe-bench/apps/erpnext
                                              frappe-bench/apps/dcnet_apps
```

**Quy trình deploy:**
1. Local: commit + push to `develop` (hoặc `main` cho prod)
2. Server: `cd /home/frappe/flow_next && git pull`
3. Server: `cd /home/frappe/frappe-bench && bench migrate`
4. Server: `sudo supervisorctl restart all`

### Branch Mapping

| Server | Branch | Khi nào |
|--------|--------|---------|
| Staging/Demo | `develop` | Trước go-live |
| Production | `main` | Sau go-live (04/08/2026) |

---

## Deployment Steps

### Phase 1: Server Preparation

#### Step 1.1 — System Update & Essential Packages

```bash
# SSH vào server
ssh root@163.227.121.154

# Update system
sudo apt update && sudo apt upgrade -y

# Essential packages
sudo apt install -y \
  git \
  curl \
  wget \
  software-properties-common \
  build-essential \
  pkg-config \
  libffi-dev \
  libssl-dev \
  libmariadb-dev \
  libmysqlclient-dev \
  libjpeg-dev \
  zlib1g-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libwebp-dev \
  libharfbuzz-dev \
  libfribidi-dev \
  libxcb1-dev \
  xvfb \
  libfontconfig \
  cron \
  gcc \
  python3-dev \
  python3-setuptools
```

#### Step 1.2 — Create `frappe` User

```bash
# Tạo user frappe (không dùng root để chạy bench)
sudo adduser --disabled-password --gecos "" frappe
sudo usermod -aG sudo frappe

# Cho phép frappe sudo không password (tạm thời, cho cài đặt)
echo "frappe ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/frappe

# Chuyển sang user frappe
su - frappe
```

#### Step 1.3 — Install Python 3.14 (BẮT BUỘC cho Frappe v16)

```bash
# Thêm deadsnakes PPA (cần cho Ubuntu 22.04/24.04)
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.14 + dev + venv
sudo apt install -y \
  python3.14 \
  python3.14-dev \
  python3.14-venv

# Verify
python3.14 --version   # Python 3.14.x

# KHÔNG thay thế system python3!
# Chỉ dùng python3.14 cho bench init
```

#### Step 1.4 — Install Node.js 24 (BẮT BUỘC cho Frappe v16)

```bash
# Install nvm (chạy với user frappe)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc

# Install Node 24
nvm install 24
nvm use 24
nvm alias default 24

# Install yarn
npm install -g yarn

# Verify
node --version    # v24.x.x
npm --version     # 10.x.x+
yarn --version    # 1.22.x
```

#### Step 1.5 — Install MariaDB 11.8 (BẮT BUỘC cho Frappe v16)

```bash
# Thêm MariaDB official repository
# Ref: https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/
sudo apt install -y apt-transport-https curl
sudo curl -o /etc/apt/keyrings/mariadb-keyring.pgp 'https://supermirror.de/mariadb/mariadb-keyring.pgp'

# Thêm repo (Ubuntu 24.04 = noble, Ubuntu 22.04 = jammy)
UBUNTU_CODENAME=$(lsb_release -cs)
sudo tee /etc/apt/sources.list.d/mariadb.sources <<EOF
X-Repolib-Name: MariaDB
Types: deb
URIs: https://supermirror.de/mariadb/repo/11.8/ubuntu
Suites: ${UBUNTU_CODENAME}
Components: main
Signed-By: /etc/apt/keyrings/mariadb-keyring.pgp
EOF

sudo apt update

# Install MariaDB 11.8
sudo apt install -y mariadb-server mariadb-client

# Verify
mariadb --version   # 11.8.x

# Secure installation
sudo mysql_secure_installation
# → Set root password (GHI NHỚ!)
# → Unix socket auth: N
# → Remove anonymous users: Y
# → Disallow root login remotely: Y
# → Remove test database: Y
# → Reload privilege tables: Y

# Configure MariaDB for Frappe
sudo tee /etc/mysql/mariadb.conf.d/99-frappe.cnf <<EOF
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# InnoDB tuning (32GB RAM → 8GB buffer pool)
innodb_buffer_pool_size = 8G
innodb_log_file_size = 512M
innodb_log_buffer_size = 64M
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit = 1

# Frappe requirement
innodb_read_only_compressed = OFF

[mysql]
default-character-set = utf8mb4
EOF

# Restart MariaDB
sudo systemctl restart mariadb
sudo systemctl enable mariadb
```

#### Step 1.6 — Install Redis

```bash
sudo apt install -y redis-server

# Verify
redis-server --version   # 6.x+ hoặc 7.x

# Enable
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

#### Step 1.7 — Install wkhtmltopdf 0.12.6 (Patched Qt)

```bash
# Download patched version (Ubuntu apt package thường KHÔNG patched)
# Check arch
ARCH=$(dpkg --print-architecture)

# Ubuntu 24.04 (noble) hoặc 22.04 (jammy)
if [ "$UBUNTU_CODENAME" = "noble" ] || [ "$UBUNTU_CODENAME" = "jammy" ]; then
  wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.${UBUNTU_CODENAME}_${ARCH}.deb
  sudo dpkg -i wkhtmltox_0.12.6.1-3.${UBUNTU_CODENAME}_${ARCH}.deb
  sudo apt install -f -y   # Fix dependencies nếu cần
fi

# Verify — phải thấy "wkhtmltopdf 0.12.6 (with patched qt)"
wkhtmltopdf --version
```

#### Step 1.8 — Install fail2ban (Security)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

### Phase 2: Frappe Bench Setup

#### Step 2.1 — Install Bench CLI + Prerequisites

```bash
# Chạy với user frappe
sudo su - frappe

# Install uv (BẮT BUỘC — bench mới dùng uv thay pip để tạo venv)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Install pipx + bench
sudo apt install -y pipx
pipx install frappe-bench
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Tạo symlink để sudo tìm được bench
sudo ln -s /home/frappe/.local/bin/bench /usr/local/bin/bench

# Install gh CLI (để clone private repo)
sudo apt install -y gh
gh auth login   # → GitHub.com → HTTPS → Paste token (cần quyền repo)

# Verify
bench --version
uv --version
gh --version
```

#### Step 2.2 — Initialize Frappe Bench

```bash
cd /home/frappe

# Prerequisite: libmariadb-dev cho mysqlclient build
sudo apt install -y libmariadb-dev pkg-config

# Init bench với Frappe v16 + Python 3.14
bench init frappe-bench \
  --frappe-branch version-16 \
  --python python3.14

# Nếu mysqlclient build fail, set env vars rồi install thủ công:
# export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags libmariadb)
# export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs libmariadb)
# cd frappe-bench && uv pip install -e apps/frappe --python env/bin/python

cd frappe-bench

# Tạo apps.txt (nếu bench init không tạo)
echo "frappe" > sites/apps.txt

# Verify
ls apps/frappe/   # Phải có
```

#### Step 2.3 — Clone Monorepo & Setup Symlinks

```bash
# Clone monorepo (ngoài frappe-bench) — dùng gh vì repo private
cd /home/frappe
gh repo clone dcnet-cloud/flow_next
cd flow_next
git checkout develop   # staging dùng develop

# Tạo symlinks trong frappe-bench/apps/
cd /home/frappe/frappe-bench/apps

# ERPNext từ monorepo
ln -s /home/frappe/flow_next/dcnet_core erpnext

# Custom apps từ monorepo
ln -s /home/frappe/flow_next/dcnet_apps dcnet_apps
```

#### Step 2.4 — Install App Dependencies

```bash
cd /home/frappe/frappe-bench

# Install Python dependencies vào bench venv
./env/bin/pip install -e apps/erpnext
./env/bin/pip install -e apps/dcnet_apps

# Install Node dependencies (BẮT BUỘC trước bench build)
cd apps/frappe && yarn install && cd ../..

# Install onscan.js (required by ERPNext POS)
cd apps/frappe && yarn add onscan.js && cd ../..

# Register apps
echo "erpnext" >> sites/apps.txt
echo "dcnet_apps" >> sites/apps.txt

# Build assets (JS/CSS)
bench build
```

#### Step 2.5 — Create Site

```bash
cd /home/frappe/frappe-bench

# Fix Redis config (bench mặc định port 11000, Ubuntu Redis dùng 6379)
bench set-config -g redis_cache redis://127.0.0.1:6379
bench set-config -g redis_queue redis://127.0.0.1:6379
bench set-config -g redis_socketio redis://127.0.0.1:6379

# Tạo site (PHẢI có --db-root-username root)
bench new-site flow-demo.dcnet.vn \
  --db-root-username root \
  --mariadb-root-password YOUR_MYSQL_ROOT_PASSWORD \
  --admin-password YOUR_ADMIN_PASSWORD

# Install apps vào site (THỨ TỰ QUAN TRỌNG)
bench --site flow-demo.dcnet.vn install-app erpnext
bench --site flow-demo.dcnet.vn install-app dcnet_apps

# Set default site
bench use flow-demo.dcnet.vn

# Enable scheduler
bench --site flow-demo.dcnet.vn enable-scheduler

# Migrate (apply fixtures, custom fields, workspaces)
bench --site flow-demo.dcnet.vn migrate
```

---

### Phase 3: Production Configuration

#### Step 3.1 — Install Nginx & Supervisor

```bash
sudo apt install -y nginx supervisor
```

#### Step 3.2 — Setup Production (Thủ công — `bench setup production` cần ansible)

```bash
cd /home/frappe/frappe-bench

# Generate Nginx config
sudo bench setup nginx

# Generate Supervisor config
sudo bench setup supervisor

# QUAN TRỌNG: Thêm node-socketio vào supervisor config
# bench setup supervisor KHÔNG tự thêm socketio, phải thêm thủ công
# Tìm full path node (nvm cài trong user space, supervisor chạy root không thấy)
NODE_PATH=$(which node)   # VD: /home/frappe/.nvm/versions/node/v24.14.0/bin/node

# Dùng nano thêm vào cuối file /home/frappe/frappe-bench/config/supervisor.conf:
sudo nano /home/frappe/frappe-bench/config/supervisor.conf
# Thêm block sau (KHÔNG có spaces đầu dòng):
# [program:frappe-bench-node-socketio]
# command=/home/frappe/.nvm/versions/node/v24.14.0/bin/node /home/frappe/frappe-bench/apps/frappe/socketio.js
# priority=4
# autostart=true
# autorestart=true
# stdout_logfile=/home/frappe/frappe-bench/logs/node-socketio.log
# stderr_logfile=/home/frappe/frappe-bench/logs/node-socketio.error.log
# user=frappe
# directory=/home/frappe/frappe-bench

# Symlink configs vào system directories
sudo ln -sf /home/frappe/frappe-bench/config/supervisor.conf /etc/supervisor/conf.d/frappe-bench.conf
sudo ln -sf /home/frappe/frappe-bench/config/nginx.conf /etc/nginx/conf.d/frappe-bench.conf

# Disable default nginx site (tránh conflict)
sudo rm -f /etc/nginx/sites-enabled/default

# QUAN TRỌNG: Fix Nginx permission — www-data cần traverse /home/frappe/
sudo chmod 711 /home/frappe

# Fix Nginx log format error (nếu có "unknown log format main")
sudo sed -i 's/access_log.*main;/access_log \/var\/log\/nginx\/access.log;/' /etc/nginx/conf.d/frappe-bench.conf

# Reload services
sudo supervisorctl reread
sudo supervisorctl update
sudo nginx -t && sudo systemctl reload nginx

# Verify — phải thấy TẤT CẢ RUNNING, kể cả node-socketio
sudo supervisorctl status
```

> **Lưu ý:**
> - `sudo bench setup production frappe` yêu cầu ansible → dùng `bench setup nginx` + `bench setup supervisor` riêng rồi symlink thủ công.
> - Supervisor config KHÔNG tự thêm node-socketio → phải thêm thủ công.
> - `command` phải dùng **full path** tới node (VD: `/home/frappe/.nvm/versions/node/v24.14.0/bin/node`) vì supervisor chạy root không có nvm PATH.

#### Step 3.3 — Verify Site Access

```bash
# Test Nginx serve assets
curl -I http://localhost/assets/frappe/dist/css/login.bundle.*.css

# Nếu 404 nhưng file tồn tại → kiểm tra permission:
sudo -u www-data stat /home/frappe/frappe-bench/sites/assets/frappe/dist/css/
# Nếu Permission denied → sudo chmod 711 /home/frappe

# Truy cập: http://flow-demo.dcnet.vn
```

#### Step 3.4 — Firewall

```bash
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS (cho sau)
sudo ufw --force enable

# Verify
sudo ufw status
```

#### Step 3.5 — Production Tuning

```bash
cd /home/frappe/frappe-bench

# Gunicorn workers: min(2×CPU+1, RAM/300MB) → min(33, ~100) → 17 workers cho 32GB
bench set-config gunicorn_workers 17

# Background workers
bench set-config background_workers 4

# Verify config
cat sites/common_site_config.json
```

#### Step 3.6 — Disable Developer Mode

```bash
# QUAN TRỌNG: Production KHÔNG bật developer mode
bench --site flow-demo.dcnet.vn set-config developer_mode 0
bench --site flow-demo.dcnet.vn clear-cache

# Restart để apply
sudo supervisorctl restart all
```

#### Step 3.7 — Setup Redis Security (Optional nhưng khuyến nghị)

```bash
cd /home/frappe/frappe-bench

# Tạo Redis users với password
bench create-rq-users
```

---

### Phase 4: ERPNext Initial Setup

#### Step 4.1 — Setup Wizard

Truy cập `http://flow-demo.dcnet.vn` và hoàn thành Setup Wizard:

| Field | Value |
|-------|-------|
| Language | Vietnamese |
| Country | Vietnam |
| Timezone | Asia/Ho_Chi_Minh |
| Currency | VND |
| Chart of Accounts | Import từ `docs/accounting/ChartOfAccountsImporter_v2.csv` |
| Company | Thăng Long TM (hoặc Nhật Minh Sport tùy site) |

#### Step 4.2 — Run Custom Setup

```bash
cd /home/frappe/frappe-bench

# Migrate (apply fixtures, custom fields, workspaces, etc.)
bench --site flow-demo.dcnet.vn migrate

# Clear cache
bench --site flow-demo.dcnet.vn clear-cache

# Restart
sudo supervisorctl restart all
```

#### Step 4.3 — Load Demo Data (Staging Only)

```bash
# Chỉ chạy trên staging, KHÔNG chạy trên production
bench --site flow-demo.dcnet.vn dcnet-fixtures generate
```

---

### Phase 5: SSL & Domain (Khi có domain)

#### Step 5.1 — DNS Setup

```
A record: flow-demo.dcnet.vn → 163.227.121.154
```

#### Step 5.2 — Update Site Name (nếu tạo với tên tạm)

```bash
cd /home/frappe/frappe-bench
bench setup add-domain flow-demo.dcnet.vn --site staging.local
# Hoặc: rename site folder + update nginx config
```

#### Step 5.3 — Let's Encrypt SSL

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Lấy SSL cert
sudo certbot --nginx -d flow-demo.dcnet.vn

# Auto-renew (certbot tự thêm cron/systemd timer)
sudo certbot renew --dry-run
```

---

## Deploy Script (Day-to-day)

```bash
# Tạo file /home/frappe/deploy.sh
cat > /home/frappe/deploy.sh << 'SCRIPT'
#!/bin/bash
set -e

SITE="flow-demo.dcnet.vn"
BRANCH="develop"
BENCH_DIR="/home/frappe/frappe-bench"
REPO_DIR="/home/frappe/flow_next"

echo "=== DCNET Flow Deploy ==="
echo "$(date) | Branch: $BRANCH | Site: $SITE"

# 1. Pull latest code
echo ">>> Pulling code..."
cd "$REPO_DIR"
git pull origin "$BRANCH"

# 2. Install dependencies (nếu có thay đổi pyproject.toml)
echo ">>> Installing dependencies..."
cd "$BENCH_DIR"
./env/bin/pip install -e apps/erpnext --quiet
./env/bin/pip install -e apps/dcnet_apps --quiet

# 3. Build assets
echo ">>> Building assets..."
bench build --force

# 4. Migrate database
echo ">>> Running migrations..."
bench --site "$SITE" migrate

# 5. Clear cache
bench --site "$SITE" clear-cache

# 6. Restart services
echo ">>> Restarting services..."
sudo supervisorctl restart all

echo "=== Deploy complete! ==="
SCRIPT

chmod +x /home/frappe/deploy.sh
```

**Sử dụng:**
```bash
ssh frappe@163.227.121.154
./deploy.sh
```

---

## Backup Strategy

```bash
# Manual backup
cd /home/frappe/frappe-bench
bench --site flow-demo.dcnet.vn backup --with-files

# Backup location: sites/flow-demo.dcnet.vn/private/backups/

# Auto backup (daily 2AM) — thêm vào crontab của user frappe
(crontab -l 2>/dev/null; echo "0 2 * * * cd /home/frappe/frappe-bench && bench --site flow-demo.dcnet.vn backup --with-files >> /var/log/frappe-backup.log 2>&1") | crontab -
```

---

## Monitoring

```bash
# Check all services
sudo supervisorctl status

# Check logs
tail -f /home/frappe/frappe-bench/logs/frappe.log
tail -f /home/frappe/frappe-bench/logs/worker.error.log
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# System resources
df -h && free -h && uptime
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 502 Bad Gateway | `sudo supervisorctl restart all` |
| Assets not loading | `bench build --force && sudo systemctl reload nginx` |
| Permission denied | `sudo chown -R frappe:frappe /home/frappe/frappe-bench` |
| Redis connection refused | `sudo systemctl restart redis-server && sudo supervisorctl restart all` |
| MariaDB gone away | Check `innodb_buffer_pool_size`, `sudo systemctl restart mariadb` |
| Python package conflict | `./env/bin/pip install -e apps/erpnext --force-reinstall` |
| Site not accessible | `bench use SITENAME` + verify `server_name` in nginx config |
| EXTERNALLY-MANAGED error | Dùng `pipx` hoặc `rm /usr/lib/python3.14/EXTERNALLY-MANAGED` |
| bench build fails (node) | Verify `node --version` = v24.x, `nvm use 24` |

---

## Security Checklist (Trước khi cho khách demo)

- [ ] Đổi admin password (không dùng mặc định)
- [ ] Đổi MySQL root password (strong, >= 16 chars)
- [ ] Disable root SSH login (`PermitRootLogin no` in `/etc/ssh/sshd_config`)
- [ ] Setup SSH key authentication (disable password auth)
- [ ] UFW enabled (chỉ mở 22, 80, 443)
- [ ] fail2ban running
- [ ] Tắt developer mode (`developer_mode = 0`)
- [x] Setup SSL (Let's Encrypt, auto-renew)
- [ ] Xóa frappe sudoers NOPASSWD: `sudo rm /etc/sudoers.d/frappe` → dùng `bench setup sudoers` thay thế
- [ ] Redis security: `bench create-rq-users`

---

## Chuyển từ Staging → Production

Khi sẵn sàng go-live (dự kiến 04/08/2026):

1. **Git:** `cd /home/frappe/flow_next && git checkout main && git pull`
2. **Site:** Tạo site mới hoặc restore backup sạch
3. **Data:** Import dữ liệu BRAVO (xem migration plan)
4. **DNS:** Trỏ domain chính thức → `bench setup add-domain`
5. **SSL:** `sudo certbot --nginx -d flow-demo.dcnet.vn`
6. **Backup:** Daily backup + offsite storage
7. **Monitoring:** Setup uptime monitoring (UptimeRobot/Healthchecks.io)
8. **Security:** Hoàn thành checklist trên

---

## Verification Checklist (Sau khi cài xong)

```bash
# Chạy tất cả để verify
python3.14 --version        # 3.14.x
node --version               # v24.x.x
yarn --version               # 1.22.x
mariadb --version            # 11.8.x
redis-server --version       # 6.x+ hoặc 7.x
wkhtmltopdf --version        # 0.12.6 (with patched qt)
bench --version              # 5.x
nginx -v                     # nginx/1.x
supervisord --version        # 4.x

# Bench status
cd /home/frappe/frappe-bench
bench version                # frappe 16.x, erpnext 16.x, dcnet_apps 1.x
sudo supervisorctl status    # Tất cả RUNNING
curl -I http://localhost     # HTTP 200
```

---

## Task Checklist

### Phase 1: Server Preparation
- [x] 1.0 Fix DNS (resolv.conf → 8.8.8.8) + hostname (/etc/hosts → erp-test)
- [x] 1.1 System update & essential packages (725 packages installed)
- [x] 1.2 Create frappe user (NOPASSWD sudo)
- [x] 1.3 Install Python 3.14 (deadsnakes PPA) ✓ 3.14.x
- [x] 1.4 Install Node.js 24 (nvm) ✓ v24.14.0 + yarn 1.22.22
- [x] 1.5 Install MariaDB 11.8 (official repo) ✓ 11.8.6-MariaDB
- [x] 1.6 Install Redis ✓ 7.0.15
- [x] 1.7 Install wkhtmltopdf ✓ 0.12.6

### Phase 2: Frappe Bench
- [x] 2.1 Install Bench CLI (pipx) ✓ bench 5.29.1
- [x] 2.2 Init Frappe Bench (--python python3.14) ✓ (cần cài `uv` + `libmariadb-dev pkg-config` trước)
- [x] 2.3 Clone monorepo (gh repo clone) & symlinks ✓
- [x] 2.4 Install app dependencies ✓ (yarn install trong apps/frappe, yarn add onscan.js)
- [x] 2.5 Create site flow-demo.dcnet.vn & install apps ✓ (Redis port fix: set-config redis_* → 6379)

### Phase 3: Production Config
- [x] 3.1 Install Nginx + Supervisor ✓
- [x] 3.2 bench setup production ✓ (thủ công: setup nginx + setup supervisor + symlink + socketio thủ công, bỏ fail2ban/ansible)
- [x] 3.3 Configure Nginx + Verify ✓ (fix: chmod 711 /home/frappe, xóa log format "main", node full path cho socketio)
- [ ] 3.4 Firewall (UFW)
- [ ] 3.5 Production tuning (gunicorn workers)
- [ ] 3.6 Disable developer mode
- [ ] 3.7 Redis security (optional)

### Phase 4: ERPNext Setup
- [ ] 4.1 Setup Wizard ← **NEXT**
- [ ] 4.2 Migrate & custom setup
- [ ] 4.3 Load demo data (staging only)

### Phase 5: SSL & Domain
- [x] 5.1 DNS setup ✓ (team admin trỏ flow-demo.dcnet.vn → IP public)
- [x] 5.2 Site đã tạo với domain thật (flow-demo.dcnet.vn)
- [x] 5.3 Let's Encrypt SSL ✓ (certbot --nginx, auto-renew OK)

### Post-setup
- [ ] Deploy script tạo & test
- [ ] Backup cron setup
- [ ] Verification checklist pass
- [ ] Security checklist hoàn thành

---

## References

- [Frappe Installation Docs](https://docs.frappe.io/framework/user/en/installation)
- [Frappe Production Setup](https://docs.frappe.io/framework/user/en/bench/guides/setup-production)
- [MariaDB 11.8 on Ubuntu](https://linuxcapable.com/how-to-install-mariadb-11-8-on-ubuntu-linux/)
- [Python 3.14 on Ubuntu (deadsnakes)](https://linuxcapable.com/install-python-3-14-on-ubuntu-linux/)
- [ERPNext v16 Installation Guide](https://cloud.erpgulf.com/blog/support-forum/installing-erpnext-version-16)
- [Frappe v16 pyproject.toml](https://github.com/frappe/frappe/blob/version-16/pyproject.toml)
