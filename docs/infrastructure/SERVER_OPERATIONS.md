# DCNET Flow - Server Operations Guide

> **Server:** 163.227.121.154 (erp-test)
> **OS:** Ubuntu 24.04 | **User:** frappe
> **Domain:** flow-demo.dcnet.vn (pending DNS)
> **Bench:** /home/frappe/frappe-bench
> **Repo:** /home/frappe/flow_next (branch: develop)

---

## SSH & User

```bash
# SSH vào server
ssh root@163.227.121.154

# Chuyển sang user frappe (LUÔN dùng frappe, không dùng root cho bench)
sudo su - frappe

# Hoặc SSH thẳng nếu đã setup SSH key cho frappe
ssh frappe@163.227.121.154
```

---

## Deploy (Cập nhật code)

```bash
# Quick deploy
bash /home/frappe/deploy.sh

# Hoặc chạy tay từng bước:
cd /home/frappe/flow_next && git pull origin develop
cd /home/frappe/frappe-bench
./env/bin/pip install -e apps/erpnext --quiet
./env/bin/pip install -e apps/dcnet_apps --quiet
bench build --force
bench --site flow-demo.dcnet.vn migrate
sudo supervisorctl restart all
```

---

## Bench Commands (Hay dùng)

```bash
cd /home/frappe/frappe-bench

# --- Site Management ---
bench --site flow-demo.dcnet.vn migrate          # Apply patches + fixtures
bench --site flow-demo.dcnet.vn clear-cache       # Clear cache
bench --site flow-demo.dcnet.vn clear-website-cache
bench build                                        # Build JS/CSS assets
bench build --force                                # Force rebuild tất cả

# --- Dev Mode (bật/tắt) ---
bench --site flow-demo.dcnet.vn set-config developer_mode 1   # BẬT (staging)
bench --site flow-demo.dcnet.vn set-config developer_mode 0   # TẮT (production)

# --- Console & DB ---
bench --site flow-demo.dcnet.vn console            # Python console (frappe context)
bench --site flow-demo.dcnet.vn mariadb            # MySQL shell

# --- Backup ---
bench --site flow-demo.dcnet.vn backup --with-files
# Output: sites/flow-demo.dcnet.vn/private/backups/

# --- Restore ---
bench --site flow-demo.dcnet.vn restore \
  /path/to/database.sql.gz \
  --with-private-files /path/to/private-files.tar \
  --with-public-files /path/to/files.tar

# --- Fixtures (staging only) ---
bench --site flow-demo.dcnet.vn dcnet-fixtures generate
bench --site flow-demo.dcnet.vn dcnet-fixtures generate --module master
bench --site flow-demo.dcnet.vn dcnet-fixtures status
bench --site flow-demo.dcnet.vn dcnet-fixtures clear --force

# --- Scheduler ---
bench --site flow-demo.dcnet.vn enable-scheduler
bench --site flow-demo.dcnet.vn disable-scheduler
bench --site flow-demo.dcnet.vn doctor             # Check scheduler health
```

---

## Service Management

```bash
# Supervisor (gunicorn, workers, redis, socketio)
sudo supervisorctl status                  # Xem trạng thái tất cả
sudo supervisorctl restart all             # Restart tất cả
sudo supervisorctl restart frappe-bench-frappe-web:*   # Chỉ restart web
sudo supervisorctl stop all                # Dừng tất cả
sudo supervisorctl start all               # Bật tất cả

# Nginx
sudo nginx -t                              # Test config
sudo systemctl reload nginx                # Reload (không downtime)
sudo systemctl restart nginx               # Restart

# MariaDB
sudo systemctl status mariadb
sudo systemctl restart mariadb

# Redis
sudo systemctl status redis-server
sudo systemctl restart redis-server

# SSL (Let's Encrypt)
sudo certbot certificates                 # Xem cert hiện tại
sudo certbot renew --dry-run              # Test auto-renew
sudo certbot renew                        # Renew thủ công (nếu cần)
# Auto-renew: systemd timer tự chạy (certbot.timer)
```

---

## Logs & Debug

```bash
# --- Frappe Logs ---
tail -f /home/frappe/frappe-bench/logs/frappe.log      # Error log (quan trọng nhất)
tail -f /home/frappe/frappe-bench/logs/web.log          # Web requests
tail -f /home/frappe/frappe-bench/logs/worker.log       # Background jobs
tail -f /home/frappe/frappe-bench/logs/worker.error.log # Worker errors
tail -f /home/frappe/frappe-bench/logs/scheduler.log    # Scheduler

# --- Nginx Logs ---
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# --- Tìm lỗi cụ thể ---
grep "Error" /home/frappe/frappe-bench/logs/frappe.log | tail -20
grep "Traceback" /home/frappe/frappe-bench/logs/frappe.log | tail -10

# --- System ---
free -h                  # RAM usage
df -h                    # Disk usage
uptime                   # Load average
ps aux --sort=-%mem | head -20   # Top memory processes
du -sh /home/frappe/frappe-bench/sites/flow-demo.dcnet.vn/   # Site disk usage
```

---

## Git Operations (Trên server)

```bash
cd /home/frappe/flow_next

# Check branch & status
git branch
git status
git log --oneline -5

# Pull latest
git pull origin develop

# Nếu cần chuyển branch (VD: staging → production)
git fetch origin
git checkout main
git pull origin main
```

---

## Pip & Dependencies

```bash
cd /home/frappe/frappe-bench

# Install/update app dependencies
./env/bin/pip install -e apps/frappe
./env/bin/pip install -e apps/erpnext
./env/bin/pip install -e apps/dcnet_apps

# Nếu lỗi mysqlclient (thiếu dev headers)
sudo apt install -y libmariadb-dev pkg-config
export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags libmariadb)
export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs libmariadb)

# Check installed versions
./env/bin/pip list | grep -E "frappe|erpnext|dcnet"

# uv (bench dùng thay pip)
uv --version
```

---

## Troubleshooting

| Vấn đề | Lệnh fix |
|---------|----------|
| 502 Bad Gateway | `sudo supervisorctl restart all` |
| Assets 404 (Nginx permission) | `sudo chmod 711 /home/frappe` (www-data cần traverse) |
| Assets không load (hash cũ) | `bench build --force && bench --site X clear-cache && sudo supervisorctl restart all` |
| Permission denied | `sudo chown -R frappe:frappe /home/frappe/frappe-bench` |
| Redis refused (port 11000) | `bench set-config -g redis_cache redis://127.0.0.1:6379` (+ queue + socketio) |
| Redis refused (service) | `sudo systemctl restart redis-server && sudo supervisorctl restart all` |
| MariaDB gone away | `sudo systemctl restart mariadb` |
| mysqlclient build fail | `sudo apt install -y libmariadb-dev pkg-config` |
| uv not found (bench init) | `curl -LsSf https://astral.sh/uv/install.sh \| sh && source ~/.bashrc` |
| EXTERNALLY-MANAGED | Dùng `uv pip` hoặc `./env/bin/pip` (không dùng system pip) |
| sudo: bench not found | `sudo ln -s /home/frappe/.local/bin/bench /usr/local/bin/bench` |
| bench build fail (node module) | `cd apps/frappe && yarn install && yarn add onscan.js && cd ../..` |
| bench build fail (node version) | `nvm use 24 && bench build` |
| socketio can't find node | Supervisor dùng full path: `/home/frappe/.nvm/versions/node/v24.14.0/bin/node` |
| socketio 502 Bad Gateway | Check `sudo supervisorctl status` → socketio phải RUNNING |
| Nginx log format "main" error | `sudo sed -i 's/access_log.*main;/access_log \/var\/log\/nginx\/access.log;/' /etc/nginx/conf.d/frappe-bench.conf` |
| bench setup production (ansible) | Bỏ qua, setup thủ công: `bench setup nginx && bench setup supervisor` + symlink |
| Site trắng sau migrate | `bench build --force && bench --site X clear-cache` |
| Scheduler không chạy | `bench --site X enable-scheduler && bench --site X doctor` |

---

## File Paths (Quan trọng)

```
/home/frappe/
├── flow_next/                    # Git repo (source of truth)
│   ├── dcnet_core/               # ERPNext v16
│   ├── dcnet_apps/               # Custom modules
│   └── docs/                     # Documentation
├── frappe-bench/
│   ├── apps/
│   │   ├── frappe/               # Frappe framework (bench init)
│   │   ├── erpnext -> flow_next/dcnet_core   # Symlink
│   │   └── dcnet_apps -> flow_next/dcnet_apps # Symlink
│   ├── env/                      # Python venv
│   ├── logs/                     # All logs
│   ├── config/                   # Supervisor & Nginx configs
│   └── sites/
│       ├── flow-demo.dcnet.vn/   # Site directory
│       │   ├── private/backups/  # Backups
│       │   └── site_config.json  # Site config
│       └── common_site_config.json  # Global config
└── deploy.sh                     # Deploy script
```

---

## Cron Jobs (User frappe)

```bash
# Xem cron hiện tại
crontab -l

# Expected:
# 0 2 * * * — Daily backup lúc 2AM
```

---

*Last updated: 08/03/2026*
