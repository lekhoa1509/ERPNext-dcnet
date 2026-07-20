# DCNET Flow Development Environment

## Quick Start

### Option 1: VS Code Dev Containers (Recommended)

1. Install [VS Code](https://code.visualstudio.com/) and [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. Open project folder in VS Code

3. Click "Reopen in Container" when prompted (or press `F1` → "Dev Containers: Reopen in Container")

4. Wait for container to build and installer to run (~5-10 minutes first time)

5. **Bench will auto-start in background** - Access at http://flow.local:8000 or http://localhost:8000

### Option 2: Docker Compose (Without VS Code)

```bash
cd .devcontainer
docker compose up -d

# First time: Wait 10-15 minutes for auto-installation
# View logs to monitor progress:
docker compose logs -f frappe

# Once installed, access at http://localhost:8000
```

**Note:** Installer runs automatically on first start. Check logs with `docker compose logs -f frappe`

## Installed Apps

| App | Source | Branch |
|-----|--------|--------|
| Frappe | Official | version-16 |
| ERPNext | dcnet_core | version-16 (includes CRM module) |
| DCNET Apps | dcnet_apps | main |

> **Note:** Using ERPNext built-in CRM module (Lead, Opportunity, Customer), not separate Frappe CRM app.

## Default Credentials

- **Site**: flow.local
- **URL**: http://flow.local:8000
- **Admin Password**: 123456
- **Database Root Password**: 123

> **Note:** Add `127.0.0.1 flow.local` to `/etc/hosts` on your machine

## Auto-Start

Bench tự động cài đặt và khởi động khi chạy container:

- **Docker Compose**: Bench chạy foreground, logs hiển thị trực tiếp
- **VS Code**: Bench chạy background

```bash
# View logs (Docker Compose)
docker compose logs -f frappe

# View logs (VS Code - background mode)
tail -f /tmp/bench.log

# Stop bench
docker compose stop frappe

# Restart bench
docker compose restart frappe
```

## Development Commands

```bash
# Create new DocType
bench --site flow.local new-doctype "My DocType"

# Run tests
bench --site flow.local run-tests --app dcnet_apps

# Migrate after schema changes
bench --site flow.local migrate

# Clear cache
bench --site flow.local clear-cache
```

## Folder Structure

```
flow_next/
├── .devcontainer/          # VS Code devcontainer config
│   ├── docker-compose.yml
│   └── devcontainer.json
├── development/            # Development workspace
│   ├── installer.py        # Auto-setup script
│   └── frappe-bench/       # Frappe bench (created by installer)
├── dcnet_core/             # ERPNext v16 source (mounted as erpnext app, includes CRM)
├── dcnet_apps/             # Custom DCNET apps
└── docs/                   # Documentation
```

## Troubleshooting

### Reinstall from scratch

```bash
# Từ host machine (ngoài container)
rm -rf development/frappe-bench
docker compose restart frappe

# Hoặc từ trong container
docker compose exec frappe bash -c "rm -rf /workspace/development/frappe-bench"
docker compose restart frappe
```

Installer sẽ tự động chạy lại khi container restart.

### Database connection issues
```bash
bench set-config -g db_host mariadb
bench --site flow.local migrate
```

### Redis connection issues
```bash
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
```
