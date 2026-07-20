# DCNET Apps - Custom Business Modules

Custom Frappe application for DCNET Flow business logic.

## Overview

This is a standalone Frappe app containing all DCNET custom modules.
Strategy: 1 app, multiple modules inside (standard Frappe/ERPNext pattern).

See `docs/plans/2026-02-11-app-architecture-design.md` for architecture decision.

## Architecture

```
dcnet_apps/                    # Frappe App (this folder)
├── dcnet_apps/                # Python package
│   ├── hooks.py               # App configuration
│   ├── install.py             # After install/migrate setup
│   ├── boot.py                # Boot session customization
│   ├── modules.txt            # Module list
│   ├── crm/                   # CRM extensions (Lead validation)
│   ├── core/                  # Shared utilities
│   ├── public/                # CSS, images, SVG icons
│   ├── locale/                # Vietnamese translations
│   └── fixtures/              # Custom fields, property setters
├── pyproject.toml             # Python packaging
└── README.md                  # This file
```

## Development Setup

### Docker (Recommended)

Already configured in `.devcontainer/`:

```bash
# Open in VS Code → "Reopen in Container"
# OR manually:
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

### Manual Installation

```bash
cd frappe-bench/apps
ln -s /path/to/dcnet_apps .
cd dcnet_apps && pip install -e .
bench --site your-site install-app dcnet_apps
```

## Creating New Modules

### 1. Create Module Structure

```bash
cd dcnet_apps/dcnet_apps
mkdir -p my_module/{doctype,report,workspace}
touch my_module/__init__.py
```

### 2. Register Module

Add to `modules.txt`:
```
My Module
```

### 3. Create DocTypes

In Frappe Desk: DocType → New → Set Module: "My Module"

## Extending ERPNext DocTypes

Use `doc_events` in `hooks.py`:

```python
doc_events = {
    "Lead": {
        "validate": "dcnet_apps.crm.lead.lead_validation.validate_lead_duplicate"
    }
}
```

Or override the class:

```python
override_doctype_class = {
    "Sales Order": "dcnet_apps.my_module.controllers.sales_order.CustomSalesOrder"
}
```

## Module Standards

Each module should follow Frappe best practices:

```
my_module/
├── __init__.py
├── doctype/
│   └── my_doctype/
│       ├── my_doctype.py       # Controller
│       ├── my_doctype.json     # DocType definition
│       ├── my_doctype.js       # Client-side logic
│       └── test_my_doctype.py  # Unit tests
├── report/
│   └── my_report/
│       ├── my_report.py
│       └── my_report.json
└── workspace/
    └── my_workspace/
        └── my_workspace.json
```

## Dependencies

- **Frappe Framework** ~= 16.0
- **ERPNext** ~= 16.0

## Testing

```bash
# Run tests for specific module
bench --site flow.local run-tests --app dcnet_apps --module my_module

# Run all tests
bench --site flow.local run-tests --app dcnet_apps
```

## Documentation

Business documentation is in `docs/modules/{STT}-{slug}/`.

---

**Team:** DCNET Cloud
**Framework:** Frappe v16 / ERPNext v16
**Last Updated:** 2026-02-11
