# DCNET Flow

Business Flow Platform - Integrated CRM & ERP System.

## Quick Start

```bash
cd .devcontainer
docker compose up -d

# View logs (first time takes 10-15 minutes for auto-install)
docker compose logs -f frappe
```

Access: http://localhost:8000
Login: `Administrator` / `123456`

> Optional: Add `127.0.0.1 flow.local` to `/etc/hosts` for http://flow.local:8000

**Guides:**
- [development/README.md](./development/README.md) - Development setup guide
- [docs/architecture/DEVCONTAINER_ARCHITECTURE.md](./docs/architecture/DEVCONTAINER_ARCHITECTURE.md) - Full architecture documentation

---

## Documentation

### Architecture
System architecture documentation: [docs/architecture/](./docs/architecture/)
- [DEVCONTAINER_ARCHITECTURE.md](./docs/architecture/DEVCONTAINER_ARCHITECTURE.md) - Devcontainer setup, symlinks
- [FRAPPE_ARCHITECTURE.md](./docs/architecture/FRAPPE_ARCHITECTURE.md) - Frappe framework internals

### Business Modules
Module workflows and business processes: [docs/modules/](./docs/modules/)

| Module | Status | Description |
|--------|--------|-------------|
| [Lead](./docs/modules/lead/) | Complete | Lead management workflow |
| [Fitting](./docs/modules/fitting/) | Complete | Professional fitting service |
| [Coaching](./docs/modules/coaching/) | In Progress | Training & coaching program |

### Requirements Specs
Source of truth for features: [docs/feature/](./docs/feature/)
- `FEATURE_SPECIFICATION.md` - Phase 1: CRM
- `ERP_SPECIFICATION.md` - Phase 2: ERP
- `IMPORT_PROCESS_SPECIFICATION.md` - Import process

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Frappe v16 |
| ERP | ERPNext v16 (dcnet_core) |
| CRM | ERPNext built-in CRM module (Lead, Opportunity, Customer) |
| Custom Apps | dcnet_apps |
| Database | MariaDB 10.6 |
| Cache | Redis 6.2 |
| Development | VS Code Devcontainer |

---

## Development

See [CLAUDE.md](./CLAUDE.md) for development guidelines.

---

Developed by **DCNET**
