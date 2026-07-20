---
name: frappe
description: |
  Complete Frappe Framework skill covering ALL framework domains.
  Use for: Document CRUD, Database API, Authentication, Workflows, Web Framework,
  Desk UI customization, Client Scripts, Dialogs, Desktop Icons,
  Integration (Webhooks, OAuth, Connected Apps, Social Login),
  frappe-ui (Vue 3 components, Resources, SPA frontend),
  Data Import/Export (CSV/Excel, Migration, BRAVO),
  DocType creation & field types, Testing (FrappeTestCase, fixtures, pytest),
  Service layer patterns, App structure (hooks.py, modules.txt, pyproject.toml),
  REST API (@frappe.whitelist, frappe.call), Bench CLI commands.
  Triggers: frappe.get_doc, frappe.db, frappe.whitelist, frappe.call,
  frappe.ui.Dialog, client script, frm.add_custom_button, desk icon,
  webhook, oauth, connected app, social login, frappe-ui, createResource,
  data import, export, bench command, DocType, testing, FrappeTestCase.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch
version: "5.0.0"
---

# Frappe Framework Skill

> Consolidated knowledge base for ALL Frappe Framework development.

## Domain Index

| # | Domain | Reference File | Key Topics |
|---|--------|---------------|------------|
| 1 | **Framework Core** | [references/domains/framework-core.md](references/domains/framework-core.md) | Document CRUD, Database API, Auth, Workflows, REST API, Rate Limiting |
| 2 | **Desk UI** | [references/domains/desk.md](references/domains/desk.md) | Client Scripts, Dialogs, Form customization, Desktop Icons, Notifications |
| 3 | **Integration** | [references/domains/integration.md](references/domains/integration.md) | Webhooks, OAuth 2.0, Connected Apps, Social Login, Integration Request |
| 4 | **frappe-ui** | [references/domains/ui.md](references/domains/ui.md) | Vue 3 components, createResource, createDocumentResource, SPA frontend |
| 5 | **Data Import** | [references/domains/data-import.md](references/domains/data-import.md) | CSV/Excel import, Export, Templates, BRAVO Migration, Bank Statements |
| 6 | **DocType Patterns** | [references/domains/doctype.md](references/domains/doctype.md) | DocType creation, field types, naming rules, child tables |
| 7 | **Testing** | [references/domains/testing.md](references/domains/testing.md) | FrappeTestCase, pytest, fixtures, factories, test patterns |
| 8 | **Service Layer** | [references/domains/service.md](references/domains/service.md) | Service patterns, background jobs, repository pattern |
| 9 | **App Structure** | [references/domains/app-structure.md](references/domains/app-structure.md) | App scaffolding, hooks.py, modules.txt, pyproject.toml |
| 10 | **API Patterns** | [references/domains/api.md](references/domains/api.md) | REST API design, @frappe.whitelist, frappe.call patterns |
| 11 | **Bench Commands** | [references/domains/bench-commands.md](references/domains/bench-commands.md) | CLI reference for bench, site management, app management |

## Quick Domain Router

**What are you trying to do?**

| Task | Domain |
|------|--------|
| Create/read/update/delete documents | Framework Core |
| Database queries (frappe.db) | Framework Core |
| Login, authentication, permissions | Framework Core |
| Workflow state machines | Framework Core |
| Customize forms with JavaScript | Desk UI |
| Create dialogs, popups, alerts | Desk UI |
| Add custom buttons to forms | Desk UI |
| Manage desktop icons | Desk UI |
| Send webhooks on doc events | Integration |
| OAuth2 provider or client | Integration |
| Social login (Google, GitHub) | Integration |
| Build Vue 3 SPA frontend | frappe-ui |
| Use createResource / createListResource | frappe-ui |
| Import CSV/Excel data | Data Import |
| Export data, download templates | Data Import |
| Migrate from BRAVO | Data Import |
| Create new DocType | DocType Patterns |
| Write tests for DocTypes | Testing |
| Background jobs, enqueue | Service Layer |
| Create new Frappe app | App Structure |
| Configure hooks.py | App Structure |
| Build REST API endpoints | API Patterns |
| bench CLI commands | Bench Commands |

---

## Essential Quick Reference

### Document CRUD

```python
# Create
doc = frappe.new_doc("ToDo")
doc.description = "Task"
doc.insert()

# Read
doc = frappe.get_doc("Customer", "CUST-001")
value = frappe.db.get_value("User", "john@example.com", "email")
items = frappe.get_all("Customer", filters={"territory": "Vietnam"}, fields=["name", "customer_name"], limit=10)

# Update
doc.customer_name = "New Name"
doc.save()
# Or direct DB update (bypasses hooks):
doc.db_set("status", "Active")

# Submit/Cancel (submittable DocTypes)
doc.submit()   # docstatus 0 → 1
doc.cancel()   # docstatus 1 → 2

# Delete
frappe.delete_doc("ToDo", "TODO-001")
```

### Document Lifecycle Hooks

```
INSERT:  before_insert → autoname → validate → before_save → [DB] → after_insert → on_update → on_change
SAVE:    validate → before_save → [DB UPDATE] → on_update → on_change
SUBMIT:  validate → before_submit → [DB: docstatus=1] → on_update → on_submit → on_change
CANCEL:  before_cancel → [DB: docstatus=2] → on_cancel
DELETE:  on_trash → after_delete
```

### Database API

```python
# ORM methods
frappe.db.get_value("DocType", name, fieldname)
frappe.db.get_list("DocType", filters={}, fields=[], limit=20)
frappe.db.set_value("DocType", name, fieldname, value)
frappe.db.exists("DocType", name)
frappe.db.count("DocType", filters={})

# Raw SQL
result = frappe.db.sql("""
    SELECT name, amount FROM `tabSales Invoice`
    WHERE customer = %s AND posting_date BETWEEN %s AND %s
""", ("CUST-001", "2024-01-01", "2024-12-31"), as_dict=True)
```

### REST API

```python
@frappe.whitelist()
def get_data(customer):
    """Authenticated API endpoint"""
    return frappe.get_doc("Customer", customer)

@frappe.whitelist(allow_guest=True)
def public_endpoint():
    """No login required"""
    return {"status": "ok"}

@frappe.whitelist(methods=["POST"])
def create_order(customer, items):
    """POST-only endpoint"""
    pass
```

### Client-Side JavaScript

```javascript
// Dialog
let d = new frappe.ui.Dialog({
    title: 'My Dialog',
    fields: [
        { label: 'Name', fieldname: 'name', fieldtype: 'Data', reqd: 1 },
        { label: 'Company', fieldname: 'company', fieldtype: 'Link', options: 'Company' }
    ],
    primary_action_label: 'Submit',
    primary_action(values) { d.hide(); }
});
d.show();

// Client Script - Form customization
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Action'), () => { /* ... */ }, __('Group'));
        }
    },
    customer(frm) {
        // Field change handler
    },
    validate(frm) {
        if (frm.doc.grand_total < 0) frappe.throw(__('Invalid total'));
    }
});

// Field manipulation
frm.set_value('status', 'Approved');
frm.toggle_display('field', condition);
frm.toggle_reqd('field', condition);
frm.set_df_property('field', 'read_only', 1);
frm.set_query('item_code', () => ({ filters: { 'is_stock_item': 1 } }));

// Server call
frappe.call({
    method: 'myapp.api.get_data',
    args: { customer: 'CUST-001' },
    callback: (r) => console.log(r.message),
    freeze: true
});

// Client-side DB
frappe.db.get_value('Customer', 'CUST-001', 'credit_limit').then(r => {});
frappe.db.get_list('Customer', { filters: {}, fields: [], limit: 20 }).then(r => {});
```

### Webhook Configuration

```python
webhook = frappe.new_doc('Webhook')
webhook.webhook_doctype = 'Note'
webhook.webhook_docevent = 'on_change'
webhook.request_url = 'https://api.example.com/hook'
webhook.request_method = 'POST'
webhook.request_structure = 'JSON'
webhook.insert()
```

### Data Import

```python
from frappe.core.doctype.data_import.importer import Importer

importer = Importer(doctype="Customer", file_path="/path/to/file.csv",
                    import_type="Insert New Records", console=True)
preview = importer.get_data_for_import_preview()
import_log = importer.import_data()
```

### Bench Commands

```bash
bench new-app myapp                           # Create app
bench --site mysite install-app myapp         # Install app
bench --site mysite migrate                   # Run migrations
bench --site mysite run-tests --app myapp -v  # Run tests
bench build --app myapp                       # Build assets
bench --site mysite clear-cache               # Clear cache
bench --site mysite data-import --doctype "Customer" --file /path/to/file.csv
bench --site mysite export-fixtures --app myapp
```

### App Structure (hooks.py)

```python
app_name = "my_app"
app_title = "My App"
required_apps = ["frappe"]

# Document event hooks
doc_events = {
    "Sales Invoice": {
        "validate": "myapp.events.validate_si",
        "on_submit": "myapp.events.on_submit_si",
    }
}

# Override DocType controller
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSalesInvoice"
}

# Fixtures
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "My App"]]}
]
```

### Testing

```python
from frappe.tests import IntegrationTestCase

class TestMyDocType(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create shared fixtures
        frappe.db.commit()

    def test_create(self):
        doc = frappe.new_doc("MyDocType")
        doc.title = "Test"
        doc.insert()
        self.assertEqual(doc.title, "Test")

    def tearDown(self):
        frappe.db.rollback()
```

### Query Builder (frappe.qb)

```python
from frappe.query_builder import DocType, Field
from frappe.query_builder.functions import Count, Sum, Avg, Max, Min, Coalesce

# Basic query
SI = DocType("Sales Invoice")
result = (
    frappe.qb.from_(SI)
    .select(SI.name, SI.customer, SI.grand_total)
    .where(SI.status == "Paid")
    .where(SI.grand_total > 1000)
    .orderby(SI.creation, order=frappe.qb.desc)
    .limit(10)
    .run(as_dict=True)
)

# JOIN query
SII = DocType("Sales Invoice Item")
result = (
    frappe.qb.from_(SI)
    .join(SII).on(SII.parent == SI.name)
    .select(SI.name, SI.customer, SII.item_code, SII.qty, SII.amount)
    .where(SI.docstatus == 1)
    .where(SII.item_code.like("%SHOE%"))
    .run(as_dict=True)
)

# Aggregation with GROUP BY
result = (
    frappe.qb.from_(SI)
    .select(SI.customer, Count(SI.name).as_("count"), Sum(SI.grand_total).as_("total"))
    .where(SI.docstatus == 1)
    .groupby(SI.customer)
    .having(Count(SI.name) > 5)
    .run(as_dict=True)
)

# Subquery
subq = (
    frappe.qb.from_(SII)
    .select(SII.parent)
    .where(SII.item_code == "ITEM-001")
)
result = (
    frappe.qb.from_(SI)
    .select(SI.name, SI.customer)
    .where(SI.name.isin(subq))
    .run(as_dict=True)
)

# LEFT JOIN with Coalesce
Customer = DocType("Customer")
result = (
    frappe.qb.from_(Customer)
    .left_join(SI).on(SI.customer == Customer.name)
    .select(Customer.name, Coalesce(Sum(SI.grand_total), 0).as_("total_sales"))
    .groupby(Customer.name)
    .run(as_dict=True)
)
```

### Realtime Events

```python
# Server-side: publish event
frappe.publish_realtime(
    event="task_progress",
    message={"progress": 50, "status": "Processing..."},
    user=frappe.session.user  # specific user
)

# Broadcast to all users
frappe.publish_realtime("global_update", {"message": "System maintenance in 5 min"})

# Progress bar pattern (long-running tasks)
def heavy_task(items):
    total = len(items)
    for i, item in enumerate(items):
        process(item)
        frappe.publish_realtime("task_progress", {
            "progress": int((i + 1) / total * 100),
            "description": f"Processing {item.name}..."
        }, user=frappe.session.user)
    frappe.publish_realtime("task_progress", {
        "progress": 100,
        "description": "Complete!"
    }, user=frappe.session.user)
```

```javascript
// Client-side: listen for events
frappe.realtime.on("task_progress", (data) => {
    frappe.show_progress("Processing", data.progress, 100, data.description);
    if (data.progress === 100) {
        frappe.hide_progress();
        frappe.show_alert({message: "Done!", indicator: "green"});
    }
});

// Dashboard real-time indicator
frappe.realtime.on("order_received", (data) => {
    frappe.show_alert({
        message: __("New order {0} from {1}", [data.order, data.customer]),
        indicator: "blue"
    }, 10);
    // Refresh list if on list view
    if (cur_list && cur_list.doctype === "Sales Order") {
        cur_list.refresh();
    }
});

// Cleanup
frappe.realtime.off("task_progress");
```

### Cache Patterns

```python
# Document cache (auto-managed by frappe)
doc = frappe.get_cached_doc("Customer", "CUST-001")  # Faster read-only access
frappe.clear_document_cache("Customer", "CUST-001")  # Invalidate specific doc

# Custom cache (Redis-backed)
# SET
frappe.cache().set_value("myapp:dashboard_data", data, expires_in_sec=300)

# GET with generator (lazy load)
data = frappe.cache().get_value("myapp:dashboard_data", generator=compute_dashboard)

# DELETE
frappe.cache().delete_value("myapp:dashboard_data")

# Hash-based cache (for structured data)
frappe.cache().hset("myapp:customer_stats", customer_name, stats_dict)
stats = frappe.cache().hget("myapp:customer_stats", customer_name)
frappe.cache().hdel("myapp:customer_stats", customer_name)

# Cache invalidation strategy pattern
class CustomSalesInvoice(SalesInvoice):
    def on_update(self):
        super().on_update()
        self._invalidate_caches()

    def on_cancel(self):
        super().on_cancel()
        self._invalidate_caches()

    def _invalidate_caches(self):
        """Invalidate all related caches when document changes."""
        frappe.clear_document_cache("Sales Invoice", self.name)
        frappe.cache().delete_value(f"myapp:customer_outstanding_{self.customer}")
        frappe.cache().delete_value(f"myapp:monthly_sales_{self.posting_date[:7]}")
        # Clear DocType-level cache
        frappe.clear_cache(doctype="Sales Invoice")
```

### Desktop Icon Management (DCNET Flow)

Config: `dcnet_apps/dcnet_apps/install.py` → `setup_desk()` → `DESK_ICONS`

Rules:
1. Label MUST be English, matching Workspace Sidebar name
2. SVG = `/assets/{app}/icons/desktop_icons/{variant}/{frappe.scrub(label)}.svg`
3. Strategy: IDEMPOTENT (DELETE all → recreate from config)
4. Folder labels CAN be Vietnamese, but children MUST be English

---

## Existing Reference Directories

These reference directories from the original skills contain detailed API docs, tutorials, and examples:

| Directory | Location | Contents |
|-----------|----------|----------|
| **API Reference** | `api_reference/` | 1,100+ function docs from codebase analysis |
| **Architecture** | `architecture/` | MVC, layered architecture analysis |
| **Config Patterns** | `config_patterns/` | DocType configuration patterns |
| **Dependencies** | `dependencies/` | Module dependency graphs |
| **Documentation** | `documentation/` | Workflows, release notes |
| **Patterns** | `patterns/` | Factory, Strategy, Observer patterns |
| **References** | `references/` | Detailed reference docs, domain files |
| **Test Examples** | `test_examples/` | 1,478 real test examples |
| **Tutorials** | `tutorials/` | 369 step-by-step guides |

---

## Related Skills

- **erpnext** - ERPNext modules (Accounting, Stock, Selling, Buying, etc.)
- **dcnet-module** - DCNET Flow module documentation builder

---

**Version 5.0.0** | Consolidated from: frappe, frappe-desk, frappe-integration, frappe-ui, frappe-data-import + 6 external skills
