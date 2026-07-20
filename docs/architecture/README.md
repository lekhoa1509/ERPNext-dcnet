# Architecture Documentation

System architecture documentation for DCNET Flow.

## Documents

| Document | Description |
|----------|-------------|
| [DEVCONTAINER_ARCHITECTURE.md](./DEVCONTAINER_ARCHITECTURE.md) | Devcontainer setup, services, symlink strategy |
| [FRAPPE_ARCHITECTURE.md](./FRAPPE_ARCHITECTURE.md) | Frappe framework internals |

## Quick Reference

### Tech Stack

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│  Frappe Desk (SPA) + Frappe CRM (Vue.js)        │
├─────────────────────────────────────────────────┤
│                   Web Server                     │
│  Bench dev server (Werkzeug)                    │
├─────────────────────────────────────────────────┤
│                   Framework                      │
│  Frappe Framework v16 (Python)                  │
├─────────────────────────────────────────────────┤
│                   Applications                   │
│  ERPNext v16 (dcnet_core)                       │
│  Frappe CRM (dcnet_crm)                         │
│  Custom Modules (dcnet_apps)                    │
├─────────────────────────────────────────────────┤
│                   Data Layer                     │
│  MariaDB 10.6 + Redis 6.2 (Cache/Queue)        │
└─────────────────────────────────────────────────┘
```

### Development Environment

| Component | Technology |
|-----------|------------|
| Container | VS Code Devcontainer |
| Base Image | frappe/bench:latest |
| Database | MariaDB 10.6 |
| Cache | Redis 6.2 |
| Python | 3.14 |
| Node.js | Latest LTS |

### Key Concepts

- **DocType** = Database table + Form UI + API + Permissions
- **Document** = Python class representing a record
- **Hooks** = Event-driven extension system
- **Desk** = Admin SPA interface (Frappe)
- **CRM UI** = Vue.js SPA (Frappe CRM)
- **Symlink Strategy** = Local apps linked into bench for hot-reload

### App Structure

```
frappe-bench/apps/
├── frappe/          # Framework (cloned by bench init)
├── erpnext/         # → /workspace/dcnet_core (symlink)
├── crm/             # → /workspace/dcnet_crm (symlink)
└── dcnet_apps/      # → /workspace/dcnet_apps (symlink)
```

---

**Last Updated:** 2026-01-13
**Version:** Frappe v16 + ERPNext v16 + Frappe CRM
**Architecture:** VS Code Devcontainer
