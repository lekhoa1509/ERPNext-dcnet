# Custom App Development on ERPNext

App structure, hooks.py configuration, patches, fixtures, module organization, override patterns, and version differences for building custom apps on Frappe/ERPNext.

---

## App Structure

### Directory Layout

```
my_app/
├── pyproject.toml              # Build config (flit_core)
├── my_app/
│   ├── __init__.py             # MUST contain __version__
│   ├── hooks.py                # App configuration (CRITICAL)
│   ├── modules.txt             # List of modules (one per line)
│   ├── patches.txt             # Migration patches
│   ├── templates/
│   │   ├── __init__.py
│   │   └── pages/              # Web pages
│   ├── my_module/              # Module directory (matches modules.txt)
│   │   ├── __init__.py
│   │   └── doctype/
│   │       └── my_doctype/
│   │           ├── my_doctype.json   # DocType definition
│   │           ├── my_doctype.py     # Controller
│   │           ├── my_doctype.js     # Client script
│   │           └── test_my_doctype.py
│   ├── public/                 # Static assets (served at /assets/my_app/)
│   │   ├── css/
│   │   ├── js/
│   │   └── icons/
│   └── www/                    # Website pages (URL = file path)
└── .github/                    # CI/CD (optional)
```

### pyproject.toml (flit_core)

```toml
[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "my_app"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
description = "My Custom ERPNext App"
requires-python = ">=3.10"
readme = "README.md"
dynamic = ["version"]

# CRITICAL: Do NOT put frappe or erpnext in dependencies!
# They are managed by bench, not pip
```

### __init__.py (REQUIRED)

```python
# my_app/__init__.py
__version__ = "0.0.1"
# CRITICAL: __version__ MUST be defined here. Bench uses it for versioning.
```

### modules.txt

```
My Module
Another Module
```

**IMPORTANT:** Module names use spaces (e.g., `My Module`). Directory names use underscores (e.g., `my_module`). The conversion is `frappe.scrub("My Module")` -> `my_module`.

---

## Creating and Installing

### Create New App

```bash
# Inside bench directory
bench new-app my_app
# Follow prompts: app name, description, publisher, email

# App is created in apps/my_app/
```

### Install App on Site

```bash
bench --site mysite.local install-app my_app

# After installing, run migrate to create DocTypes
bench --site mysite.local migrate
```

### Development Workflow

```bash
# After modifying DocType JSON or adding patches
bench --site mysite.local migrate

# After modifying Python/JS
bench --site mysite.local clear-cache

# Run tests
bench --site mysite.local run-tests --app my_app -v
bench --site mysite.local run-tests --app my_app --module my_module -v
bench --site mysite.local run-tests --app my_app --doctype "My DocType" -v
```

---

## hooks.py Configuration

### Essential Hooks

```python
app_name = "my_app"
app_title = "My App"
app_publisher = "Your Company"
app_description = "Custom ERPNext modules"
app_email = "dev@yourcompany.com"
app_license = "MIT"

# Required for frappe to find the app
required_apps = ["frappe", "erpnext"]
```

### DocType Events (Non-Breaking Hooks)

```python
# React to events on ANY DocType without modifying its code
doc_events = {
    "Sales Order": {
        "validate": "my_app.overrides.sales_order.validate",
        "on_submit": "my_app.overrides.sales_order.on_submit",
        "on_cancel": "my_app.overrides.sales_order.on_cancel",
        "on_update": "my_app.overrides.sales_order.on_update",
        "before_save": "my_app.overrides.sales_order.before_save",
        "on_trash": "my_app.overrides.sales_order.on_trash",
        "on_update_after_submit": "my_app.overrides.sales_order.on_update_after_submit",
    },
    "Sales Invoice": {
        "on_submit": "my_app.overrides.sales_invoice.on_submit",
    },
    # Wildcard: runs for ALL doctypes
    "*": {
        "on_update": "my_app.overrides.global_hooks.track_changes"
    }
}
```

```python
# my_app/overrides/sales_order.py
import frappe
from frappe import _

def validate(doc, method):
    """Called during Sales Order validate. doc is the Sales Order document."""
    if doc.custom_priority == "Urgent" and not doc.delivery_date:
        frappe.throw(_("Delivery date is required for urgent orders"))

def on_submit(doc, method):
    """Called after Sales Order is submitted."""
    if doc.custom_requires_approval:
        send_approval_notification(doc)
```

### Override DocType Class (v14+)

```python
# hooks.py
override_doctype_class = {
    "Sales Order": "my_app.overrides.custom_sales_order.CustomSalesOrder"
}
```

```python
# my_app/overrides/custom_sales_order.py
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

class CustomSalesOrder(SalesOrder):
    def validate(self):
        super().validate()  # ALWAYS call super()
        self.custom_validation()

    def custom_validation(self):
        if self.custom_field and not self.custom_other_field:
            frappe.throw(_("Custom Other Field is required when Custom Field is set"))

    def on_submit(self):
        super().on_submit()  # ALWAYS call super()
        self.create_custom_record()
```

### Extend DocType Class (v16+)

```python
# hooks.py -- v16 only
extend_doctype_class = {
    "Sales Order": "my_app.overrides.sales_order_ext.SalesOrderExt"
}
```

```python
# my_app/overrides/sales_order_ext.py
class SalesOrderExt:
    """Methods added to Sales Order class without replacing it.
    Multiple apps can extend the same DocType."""

    def custom_method(self):
        """Available as self.custom_method() on Sales Order instances."""
        return self.grand_total * 0.1

    def get_custom_data(self):
        return frappe.get_all("Custom Child", filters={"parent": self.name})
```

### override_doctype_class vs doc_events vs extend_doctype_class

| Feature | `override_doctype_class` | `doc_events` | `extend_doctype_class` (v16) |
|---------|------------------------|--------------|------------------------------|
| Replaces class | Yes (one app only) | No | No |
| Multiple apps | No (last wins) | Yes | Yes |
| Access `self` | Yes | No (uses `doc` param) | Yes |
| Override methods | Yes | No (hooks into events) | No (adds new methods) |
| Risk level | High | Low | Low |
| Use when | Need to change core behavior | React to events | Add new functionality |

---

## Patches (Data Migration)

### patches.txt Format

```
# patches.txt

[pre_model_sync]
# Runs BEFORE DocType schema changes are applied
# Use for: renaming fields, moving data before field is removed
my_app.patches.v1_0.rename_old_field
my_app.patches.v1_0.migrate_data_before_schema_change

[post_model_sync]
# Runs AFTER DocType schema changes are applied
# Use for: populating new fields, creating default records
my_app.patches.v1_0.populate_new_field
my_app.patches.v1_0.create_default_settings
my_app.patches.v1_0.setup_workflows
```

### Writing a Patch

```python
# my_app/patches/v1_0/populate_new_field.py
import frappe

def execute():
    """Populate custom_category field based on item_group."""
    # Use frappe.db for direct DB updates (faster, no controller hooks)
    frappe.db.sql("""
        UPDATE `tabSales Order`
        SET custom_category = CASE
            WHEN customer_group = 'Retail' THEN 'B2C'
            ELSE 'B2B'
        END
        WHERE custom_category IS NULL OR custom_category = ''
    """)

    # Or use get_all + set_value for smaller datasets
    for so in frappe.get_all("Sales Order",
        filters={"custom_category": ["in", [None, ""]]},
        fields=["name", "customer_group"]
    ):
        category = "B2C" if so.customer_group == "Retail" else "B2B"
        frappe.db.set_value("Sales Order", so.name, "custom_category", category)

    frappe.db.commit()
```

### Patch Best Practices

| Do | Don't |
|----|-------|
| Use `frappe.db.sql` for bulk updates | Don't use `get_doc().save()` for bulk (slow) |
| Call `frappe.db.commit()` at the end | Don't forget commit (changes may be lost) |
| Check if migration already done (idempotent) | Don't assume patch runs only once |
| Handle missing fields gracefully | Don't crash if field doesn't exist yet |
| Log progress for long patches | Don't run silently for minutes |

---

## Fixtures

### Exporting Fixtures via hooks.py

```python
# hooks.py
fixtures = [
    # Export all records of these DocTypes
    "Custom Field",
    "Property Setter",
    "Workflow",
    "Workflow State",
    "Workflow Action Master",

    # Export with filters
    {"dt": "Custom Field", "filters": [["module", "=", "My Module"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "My Module"]]},
    {"dt": "Role", "filters": [["name", "like", "My App%"]]},
    {"dt": "Workflow", "filters": [["name", "in", ["My Workflow 1", "My Workflow 2"]]]},

    # Export with specific fields only
    {"dt": "Custom Field", "filters": [["module", "=", "My Module"]], "or_filters": []},
]
```

### Export and Import Commands

```bash
# Export fixtures to JSON files in my_app/fixtures/
bench --site mysite.local export-fixtures --app my_app

# Import fixtures (happens automatically during migrate)
bench --site mysite.local import-fixtures --app my_app
```

### Fixture Files Location

```
my_app/
├── my_app/
│   ├── fixtures/
│   │   ├── custom_field.json          # Auto-generated from export
│   │   ├── property_setter.json
│   │   ├── workflow.json
│   │   └── role.json
```

---

## Module Organization

### Naming Convention

| Concept | Format | Example |
|---------|--------|---------|
| Module name (modules.txt) | Title Case with spaces | `My Module` |
| Directory name | lowercase with underscores | `my_module` |
| DocType name | Title Case with spaces | `My Custom DocType` |
| DocType directory | lowercase with underscores | `my_custom_doctype` |
| Field name | lowercase with underscores | `custom_field_name` |
| Custom field (on other DocTypes) | `custom_` prefix | `custom_my_field` |

### Module Directory Structure

```
my_app/
├── my_module/
│   ├── __init__.py
│   ├── setup.py                    # Module setup (called during install)
│   ├── api.py                      # Whitelisted API methods
│   ├── utils.py                    # Shared utilities
│   ├── doctype/
│   │   ├── my_parent_doc/
│   │   │   ├── my_parent_doc.json  # DocType definition
│   │   │   ├── my_parent_doc.py    # Server controller
│   │   │   ├── my_parent_doc.js    # Client script
│   │   │   └── test_my_parent_doc.py
│   │   └── my_child_doc/
│   │       ├── my_child_doc.json
│   │       └── my_child_doc.py
│   ├── report/
│   │   └── my_report/
│   │       ├── my_report.json
│   │       ├── my_report.py
│   │       └── my_report.js
│   ├── workspace/
│   │   └── my_workspace/
│   │       └── my_workspace.json
│   └── page/
│       └── my_page/
│           ├── my_page.json
│           ├── my_page.py
│           ├── my_page.js
│           └── my_page.html
```

---

## Install/Setup Hooks

### after_install and after_migrate

```python
# hooks.py
after_install = "my_app.install.after_install"
after_migrate = "my_app.install.after_migrate"
```

```python
# my_app/install.py
import frappe

def after_install():
    """Runs once after app installation."""
    create_default_roles()
    create_default_settings()
    setup_workflows()

def after_migrate():
    """Runs after every bench migrate."""
    setup_desk_icons()
    ensure_workspaces()
```

---

## Website and Portal Hooks

```python
# hooks.py

# Add routes
website_route_rules = [
    {"from_route": "/my-page/<path:name>", "to_route": "my_page"},
]

# Portal menu items
standard_portal_menu_items = [
    {"title": "My Portal", "route": "/my-portal", "role": "Customer"}
]

# Jinja methods available in web templates
jinja = {
    "methods": [
        "my_app.utils.jinja_methods.get_custom_data"
    ]
}
```

---

## Scheduler Hooks

```python
# hooks.py
scheduler_events = {
    "all": [
        "my_app.tasks.every_minute_task"     # Every minute (use sparingly)
    ],
    "daily": [
        "my_app.tasks.daily_cleanup"
    ],
    "daily_long": [
        "my_app.tasks.daily_heavy_task"      # Uses long worker queue
    ],
    "hourly": [
        "my_app.tasks.hourly_sync"
    ],
    "weekly": [
        "my_app.tasks.weekly_report"
    ],
    "monthly": [
        "my_app.tasks.monthly_summary"
    ],
    "cron": {
        "0 9 * * 1": [                       # Monday 9 AM
            "my_app.tasks.weekly_monday_task"
        ],
        "*/15 * * * *": [                     # Every 15 minutes
            "my_app.tasks.frequent_check"
        ]
    }
}
```

---

## Critical Rules

| Rule | Detail |
|------|--------|
| `__version__` required | Must be in `my_app/__init__.py` -- bench crashes without it |
| No frappe in deps | Never add `frappe` or `erpnext` to `pyproject.toml` dependencies |
| Module names = spaces | `modules.txt` uses spaces, directories use underscores |
| `custom_` prefix for fields | Custom Fields on standard DocTypes MUST start with `custom_` |
| Always call `super()` | When overriding controller methods, always call parent |
| Fixtures are fragile | Export after every change, test import on clean site |
| patches.txt order matters | Patches run top-to-bottom, one time only |
| `required_apps` in hooks | List dependencies so bench installs them first |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Build system | `setup.py` | `pyproject.toml` | `pyproject.toml` |
| `extend_doctype_class` | Not available | Not available | Available |
| `override_doctype_class` | Available | Available | Available |
| Workspace format | JSON v1 | JSON v2 | JSON v2 (sidebar) |
| Python | 3.8-3.10 | 3.10-3.11 | 3.10-3.12 |
| MariaDB | 10.6+ | 10.6+ | 10.6+ |
| Node | 16-18 | 18 | 18-20 |
| patches.txt sections | Flat list | pre/post_model_sync | pre/post_model_sync |
| Custom Field naming | `custom_` optional | `custom_` required | `custom_` required |
