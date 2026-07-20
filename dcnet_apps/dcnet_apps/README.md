# DCNET Apps - Custom Modules

This folder contains all DCNET custom modules and extensions.

## Structure

```
dcnet_apps/
├── hooks.py             # App hooks (doc_events, fixtures, install hooks)
├── install.py           # After install/migrate setup (branding, desk, translations)
├── boot.py              # Boot session customization
├── modules.txt          # Registered Frappe modules
├── crm/                 # CRM extensions (Lead validation)
├── core/                # Shared utilities (data import validation)
├── public/              # CSS, images, SVG icons
├── locale/              # Vietnamese translations (frappe + erpnext)
└── fixtures/            # Custom fields, property setters
```

## Development Rules

### DO:
- Write ALL custom code in this folder
- Create new modules as subfolders (e.g., `fitting/`, `coaching/`)
- Follow Frappe module structure (doctype/, report/, workspace/)
- Register new modules in `modules.txt`
- Use proper naming conventions

### DON'T:
- Edit ERPNext core modules (accounts/, buying/, selling/, etc.)
- Modify inherited doctypes directly - use controllers/hooks instead
- Create code outside dcnet_apps/

## Creating a New Module

```bash
# 1. Create module folder
mkdir -p dcnet_apps/my_module/{doctype,report,workspace}

# 2. Add __init__.py
touch dcnet_apps/my_module/__init__.py

# 3. Register in modules.txt
echo "My Module" >> modules.txt

# 4. Start developing!
```

## Extending ERPNext DocTypes

To extend an ERPNext doctype (e.g., Lead), use hooks:

```python
# hooks.py - doc_events
doc_events = {
    "Lead": {
        "validate": "dcnet_apps.crm.lead.lead_validation.validate_lead_duplicate"
    }
}
```

Or override the class:

```python
# hooks.py - override_doctype_class
override_doctype_class = {
    "Lead": "dcnet_apps.crm.lead.lead_controller.CustomLead"
}
```

---

**Team:** DCNET Cloud
**Framework:** Frappe v16 / ERPNext v16
**Last Updated:** 2026-02-11
