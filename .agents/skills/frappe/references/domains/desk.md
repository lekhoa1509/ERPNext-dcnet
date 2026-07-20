<!-- Source: frappe-desk skill -->

# Frappe Desk JavaScript API

> Customize ERPNext/Frappe Desk interface using built-in JavaScript APIs.

**Docs:** https://docs.frappe.io/framework/user/en/api

## Quick Topic Reference

| Topic | Documentation | API Reference |
|-------|---------------|---------------|
| **Dialog** | [references/docs/dialog.md](references/docs/dialog.md) | [api_reference/desktop.md](api_reference/desktop.md) |
| **Form** | [references/docs/form.md](references/docs/form.md) | [api_reference/form/](api_reference/) |
| **Notifications** | - | [api_reference/notifications.md](api_reference/notifications.md) |
| **Query Report** | - | [api_reference/query_report.md](api_reference/query_report.md) |
| **Workspace** | - | [api_reference/workspace.md](api_reference/workspace.md) |

## What is Frappe Desk?

Frappe Desk = Built-in admin interface in Frappe Framework that auto-generates UI from DocType metadata.

```
https://your-site.com/app/           ← Frappe Desk
https://your-site.com/app/lead       ← List View (auto-generated)
https://your-site.com/app/lead/NEW   ← Form View (auto-generated)
```

## ⚡ Codebase Statistics

**Languages:**
- **Python**: 123 files (100%)

**Analysis Performed:**
- ✅ API Reference (C2.5) - 123 files
- ✅ Dependency Graph (C2.6)
- ✅ Design Patterns (C3.1) - 92 patterns in 38 files
- ✅ Test Examples (C3.2) - 76 examples
- ✅ Configuration Patterns (C3.4) - 72 configs (1550 settings)
- ✅ Tutorials (C3.3) - 19 how-to guides

---

## Quick Reference

| Task | API |
|------|-----|
| Create dialog/popup | `new frappe.ui.Dialog()` |
| Quick user input | `frappe.prompt()` |
| Confirmation dialog | `frappe.confirm()` |
| Message/Alert | `frappe.msgprint()` |
| Toast notification | `frappe.show_alert()` |
| Form customization | `frappe.ui.form.on()` |
| Add custom button | `frm.add_custom_button()` |
| Field manipulation | `frm.set_value()`, `frm.toggle_display()` |
| Server calls | `frappe.call()`, `frappe.db.*` |

---

## Essential Examples

### Dialog with Form Fields

```javascript
let d = new frappe.ui.Dialog({
    title: 'Create Lead',
    fields: [
        { label: 'Name', fieldname: 'lead_name', fieldtype: 'Data', reqd: 1 },
        { label: 'Email', fieldname: 'email', fieldtype: 'Data', options: 'Email' },
        { label: 'Company', fieldname: 'company', fieldtype: 'Link', options: 'Company' },
        { label: 'Notes', fieldname: 'notes', fieldtype: 'Small Text' }
    ],
    primary_action_label: 'Create',
    primary_action(values) {
        frappe.call({
            method: 'frappe.client.insert',
            args: { doc: { doctype: 'Lead', ...values } },
            callback: (r) => {
                d.hide();
                frappe.set_route('Form', 'Lead', r.message.name);
            }
        });
    }
});
d.show();
```

### Client Script - Form Customization

```javascript
// In Client Script for Sales Order
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // Add custom button
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Delivery'), () => {
                frappe.model.open_mapped_doc({
                    method: 'erpnext.selling.doctype.sales_order.sales_order.make_delivery_note',
                    frm: frm
                });
            }, __('Create'));
        }
    },

    // Field change trigger
    customer(frm) {
        if (frm.doc.customer) {
            frappe.call({
                method: 'erpnext.selling.doctype.customer.customer.get_credit_limit',
                args: { customer: frm.doc.customer },
                callback: (r) => {
                    frm.set_value('credit_limit', r.message);
                }
            });
        }
    },

    // Validation before save
    validate(frm) {
        if (frm.doc.grand_total < 0) {
            frappe.throw(__('Total cannot be negative'));
        }
    }
});
```

### Server Call with frappe.call()

```javascript
frappe.call({
    method: 'erpnext.selling.doctype.sales_order.sales_order.get_items',
    args: {
        customer: cur_frm.doc.customer,
        company: cur_frm.doc.company
    },
    callback: function(r) {
        if (r.message) {
            r.message.forEach(item => {
                let row = cur_frm.add_child('items');
                row.item_code = item.item_code;
                row.qty = item.qty;
            });
            cur_frm.refresh_field('items');
        }
    },
    freeze: true,
    freeze_message: __('Loading items...')
});
```

### Confirmation Dialog

```javascript
frappe.confirm(
    __('Are you sure you want to delete this record?'),
    () => {
        // On Yes
        frappe.call({
            method: 'frappe.client.delete',
            args: { doctype: 'Lead', name: 'LEAD-001' }
        });
    },
    () => {
        // On No
        frappe.show_alert({ message: __('Cancelled'), indicator: 'blue' });
    }
);
```

### Show Alert/Toast

```javascript
// Success toast
frappe.show_alert({ message: __('Record saved'), indicator: 'green' }, 5);

// Warning toast
frappe.show_alert({ message: __('Missing email'), indicator: 'orange' }, 5);

// Message popup
frappe.msgprint({
    title: __('Success'),
    message: __('Customer created successfully'),
    indicator: 'green'
});
```

---

## Field Manipulation

```javascript
// Set field value
frm.set_value('status', 'Approved');

// Set multiple values
frm.set_value({ status: 'Approved', approved_by: frappe.session.user });

// Toggle field visibility
frm.toggle_display('discount_amount', frm.doc.apply_discount);

// Toggle required
frm.toggle_reqd('phone', frm.doc.contact_by === 'Phone');

// Set field read-only
frm.set_df_property('customer', 'read_only', 1);

// Set field options dynamically
frm.set_df_property('warehouse', 'options', ['Stores', 'Finished Goods']);

// Filter Link field
frm.set_query('item_code', () => {
    return {
        filters: { 'is_stock_item': 1 }
    };
});

// Set filter with custom query
frm.set_query('customer', () => {
    return {
        query: 'erpnext.controllers.queries.customer_query',
        filters: { 'territory': frm.doc.territory }
    };
});
```

---

## frappe.db API (Client-side)

```javascript
// Get single value
frappe.db.get_value('Customer', 'CUST-001', 'credit_limit')
    .then(r => console.log(r.message.credit_limit));

// Get single doc
frappe.db.get_doc('Customer', 'CUST-001')
    .then(doc => console.log(doc.customer_name));

// Get list
frappe.db.get_list('Customer', {
    filters: { territory: 'Vietnam' },
    fields: ['name', 'customer_name', 'credit_limit'],
    limit: 20
}).then(customers => console.log(customers));

// Count
frappe.db.count('Lead', { status: 'Open' })
    .then(count => console.log(count));

// Insert
frappe.db.insert({
    doctype: 'Lead',
    lead_name: 'New Lead',
    company_name: 'ACME Corp'
}).then(doc => console.log(doc.name));

// Set value
frappe.db.set_value('Lead', 'LEAD-001', 'status', 'Converted');

// Delete
frappe.db.delete_doc('Lead', 'LEAD-001');

// Check exists
frappe.db.exists('Customer', 'CUST-001')
    .then(exists => console.log(exists));
```

---

## 📝 Code Examples from Tests

*High-quality examples extracted from test files (C3.2)*

**Workflow: Create and update ToDo**

```python
todo = frappe.get_doc({
    "doctype": "ToDo",
    "description": "Test ToDo",
    "status": "Open"
}).insert()

# Update
todo.status = "Closed"
todo.save()
```

**Workflow: Create Event with reminder**

```python
event = frappe.get_doc({
    "doctype": "Event",
    "subject": "Test Event",
    "starts_on": frappe.utils.now_datetime(),
    "ends_on": frappe.utils.add_to_date(frappe.utils.now_datetime(), hours=1),
    "send_reminder": 1
}).insert()
```

*See `test_examples/` for all 76 extracted examples*

---

## 📚 Available References

This skill includes detailed reference documentation:

- **Manual Docs**: `references/docs/` - Comprehensive guides
  - [dialog.md](references/docs/dialog.md) - Dialog, prompt, confirm, msgprint
  - [form.md](references/docs/form.md) - Form customization, Client Scripts

- **API Reference**: `api_reference/` - Complete API documentation (123 files)
  - [desktop.md](api_reference/desktop.md) - Desktop API
  - [notifications.md](api_reference/notifications.md) - Notification system
  - [query_report.md](api_reference/query_report.md) - Query Reports
  - [listview.md](api_reference/listview.md) - List View

- **Tutorials**: `tutorials/` - 19 how-to guides from test workflows
- **Examples**: `test_examples/` - 76 usage examples from tests
- **Config Patterns**: `config_patterns/` - 72 DocType configurations

---

## Related Skills

- **frappe** - Frappe Framework core
- **frappe-ui** - Vue 3 component library for Frappe
- **erpnext_selling** - ERPNext Selling module

---

---

## Desktop Icon Management (DCNET Flow)

> Add/remove icons on the Desk home page for DCNET Flow modules.

### How Frappe Desktop Icons Work (v16)

```
User clicks icon → desktop.js get_route()
  → lookup: frappe.boot.workspace_sidebar_item[label.toLowerCase()]
  → resolve first Link item → navigate to workspace

SVG icon resolution:
  → frappe.utils.get_desktop_icon(label, variant)
  → path: /assets/{app}/icons/desktop_icons/{variant}/{frappe.scrub(label)}.svg
  → validates against frappe.boot.desktop_icon_urls[app][variant]
  → fallback: letter icon with colored background
```

**Critical rules:**
1. `label` MUST match Workspace Sidebar name (English) - Frappe lookups by `label.toLowerCase()`
2. Frappe auto-translates labels to Vietnamese via `__()` on client
3. SVG filename = `frappe.scrub(label)` (e.g., "Financial Reports" → `financial_reports.svg`)
4. The `icon` field on Desktop Icon is HIDDEN/LEGACY - not used for rendering
5. The `app` field determines which app's `public/icons/desktop_icons/` to search

Ref: frappe/frappe#36441 (known bug with label-based lookup)

### Current Desk Layout

Config file: `dcnet_apps/dcnet_apps/install.py` → `setup_desk()`

```python
DESK_ICONS = [
    {"label": "CRM",               "idx": 1},
    {"label": "Selling",           "idx": 2},
    {"label": "Buying",            "idx": 3},
    {"label": "Stock",             "idx": 4},
    {"label": "Assets",            "idx": 5},
    {"label": "Accounting",        "idx": 6},
    {"label": "Financial Reports", "idx": 7},
]
```

Strategy: IDEMPOTENT - `DELETE all → recreate from config` on every migrate.

### How to Add a New Desk Icon

**Step 1: Check if Workspace exists**

```bash
# List all workspaces in ERPNext
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && \
  bench --site flow.local execute 'print(\"\\n\".join(sorted(frappe.get_all(\"Workspace\", pluck=\"name\"))))'"
```

If workspace exists (e.g., "Support") → go to Step 2.
If workspace does NOT exist (custom module like "Fitting") → must create workspace first (see Step 1b).

**Step 1b: Create custom Workspace (for new modules only)**

Create workspace JSON at: `dcnet_apps/dcnet_apps/{module}/workspace/{workspace_name}/workspace.json`

Then add module to `dcnet_apps/dcnet_apps/modules.txt`.

**Step 2: Add to DESK_ICONS config**

Edit `dcnet_apps/dcnet_apps/install.py` → `setup_desk()` → `DESK_ICONS`:

```python
DESK_ICONS = [
    # ... existing icons ...
    {"label": "Support", "idx": 8},  # ← add new entry
]
```

Label MUST be the exact English Workspace name.

**Step 3: Create SVG icon (if custom)**

For custom modules, create SVG icon at:
```
dcnet_apps/dcnet_apps/public/icons/desktop_icons/solid/{scrubbed_label}.svg
```

Example: label "Fitting" → filename `fitting.svg`

Available existing SVGs:
```
accounting, assets, banking, budget, buying, crm, erpnext_settings,
financial_reports, manufacturing, project, projects, quality,
selling, stock, subcontracting, subscription, taxes
```

If the workspace matches an existing SVG name, icon loads automatically.

**Step 4: Migrate**

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench migrate"
```

### How to Add a Folder with Children

Edit `dcnet_apps/dcnet_apps/install.py` → `setup_desk()` → `DESK_FOLDERS`:

```python
DESK_FOLDERS = {
    "Dịch vụ": {                    # Folder label (can be Vietnamese for folders)
        "idx": 8,
        "icon": "fitting",           # SVG name for folder icon
        "children": [
            {"label": "Fitting",  "link_to": "Fitting",  "idx": 1},
            {"label": "Coaching", "link_to": "Coaching", "idx": 2},
        ],
    },
}
```

Note: Folder labels CAN be Vietnamese (folders use different click handler).
But children labels MUST match Workspace Sidebar names (English).

### How to Remove a Desk Icon

Remove the entry from `DESK_ICONS` or `DESK_FOLDERS` in `install.py`, then migrate.
The idempotent strategy deletes all and recreates, so removal is automatic.

### Checklist for New Module Desk Icon

- [ ] Workspace exists in ERPNext (or custom workspace created)
- [ ] Module in `modules.txt` (if custom module)
- [ ] Entry added to `DESK_ICONS` in `install.py`
- [ ] SVG icon at `public/icons/desktop_icons/solid/{name}.svg` (if custom)
- [ ] `bench migrate` run successfully
- [ ] Icon visible on desk with correct SVG
- [ ] Click opens correct workspace

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis
