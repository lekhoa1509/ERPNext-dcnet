---
name: erpnext
description: |
  Complete ERPNext skill covering ALL business modules and development patterns.
  Use for: Accounting (GL, Payments, Bank Recon, Reports), Assets (lifecycle, depreciation),
  Buying (PO, Supplier, RFQ), Selling (SO, Quotation, Customer, POS, Product Bundle),
  Stock (Inventory, Valuation, Batch/Serial, Warehouse), Manufacturing (BOM, Work Orders),
  Projects (Tasks, Timesheets), Setup (Company, Employee, Config),
  CRM (Lead, Opportunity, Prospect, Campaign),
  ERPNext code patterns, Jinja templates (Print formats, Email),
  Whitelisted API methods, Error handling & Permissions,
  Custom app development on ERPNext, Controller patterns & hooks.
  Triggers: Sales Order, Purchase Order, Stock Entry, Journal Entry, Payment Entry,
  Sales Invoice, Purchase Invoice, Delivery Note, Purchase Receipt,
  Lead, Opportunity, Customer, Supplier, Item, Warehouse, BOM, Work Order,
  Asset, Project, Timesheet, GL Entry, Bank Reconciliation,
  print format, jinja, whitelisted, controller, permission, custom app.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch
version: "5.0.0"
---

# ERPNext Skill

> Consolidated knowledge base for ALL ERPNext module development.

## Domain Index

| # | Domain | Reference File | Key Topics |
|---|--------|---------------|------------|
| 1 | **Accounting** | [references/domains/accounting.md](references/domains/accounting.md) | GL Entries, Payments, Bank Recon, Tax, Financial Reports |
| 2 | **Assets** | [references/domains/assets.md](references/domains/assets.md) | Asset lifecycle, Depreciation, Maintenance, CWIP |
| 3 | **Buying** | [references/domains/buying.md](references/domains/buying.md) | Purchase Orders, Suppliers, RFQ, Procurement |
| 4 | **Selling** | [references/domains/selling.md](references/domains/selling.md) | Sales Orders, Quotations, Customers, POS, Product Bundle |
| 5 | **Stock** | [references/domains/stock.md](references/domains/stock.md) | Inventory, Valuation (FIFO/MA), Batch/Serial, Warehouse, Pick List |
| 6 | **Manufacturing** | [references/domains/manufacturing.md](references/domains/manufacturing.md) | BOM, Work Orders, Job Cards, Production Planning |
| 7 | **Projects** | [references/domains/projects.md](references/domains/projects.md) | Project, Tasks, Timesheets, Billing |
| 8 | **Setup** | [references/domains/setup.md](references/domains/setup.md) | Company, Employee, Org Structure, Config |
| 9 | **CRM** | [references/domains/crm.md](references/domains/crm.md) | Lead, Opportunity, Prospect, Campaign, Contract |
| 10 | **Code Interpreter** | [references/domains/code-interpreter.md](references/domains/code-interpreter.md) | ERPNext code patterns, common operations |
| 11 | **Jinja Templating** | [references/domains/jinja.md](references/domains/jinja.md) | Print formats, Email templates, Portal pages, Letter Head, jenv hooks, V16 Chrome PDF |
| 12 | **Whitelisted Methods** | [references/domains/whitelisted-methods.md](references/domains/whitelisted-methods.md) | API endpoint patterns, @frappe.whitelist in ERPNext |
| 13 | **Errors & Permissions** | [references/domains/errors-permissions.md](references/domains/errors-permissions.md) | Error handling, Role permissions, permission hooks |
| 14 | **Custom App** | [references/domains/custom-app.md](references/domains/custom-app.md) | Custom app on ERPNext, pyproject.toml, patches, fixtures |
| 15 | **Controllers** | [references/domains/controllers.md](references/domains/controllers.md) | Controller patterns, lifecycle hooks, override, flags |

## Quick Domain Router

**What are you working with?**

| Task | Domain |
|------|--------|
| Journal Entries, GL, Payments, Bank Recon | Accounting |
| Fixed assets, depreciation schedules | Assets |
| Purchase Orders, Suppliers, RFQ | Buying |
| Sales Orders, Quotations, Customers, POS | Selling |
| Stock Entry, Delivery Note, Warehouse, Batches | Stock |
| BOM, Work Orders, Production Planning | Manufacturing |
| Projects, Tasks, Timesheets | Projects |
| Company setup, Employees, System config | Setup |
| Leads, Opportunities, Campaigns | CRM |
| ERPNext code patterns & operations | Code Interpreter |
| Print formats, Email templates, Portal pages | Jinja Templating |
| Building API endpoints for ERPNext | Whitelisted Methods |
| Error handling, permission checks | Errors & Permissions |
| Building custom app on top of ERPNext | Custom App |
| DocType controllers, hooks, overrides | Controllers |

---

## Essential Quick Reference

### Key Document Flows

```
SALES:     Lead → Opportunity → Quotation → Sales Order → Delivery Note → Sales Invoice → Payment Entry
PURCHASE:  Supplier → RFQ → Supplier Quotation → Purchase Order → Purchase Receipt → Purchase Invoice → Payment Entry
STOCK:     Stock Entry (Receipt/Issue/Transfer) → Stock Ledger Entry → Bin update → GL Entry (perpetual)
MANUFACTURING: BOM → Production Plan → Work Order → Stock Entry (Material Transfer) → Stock Entry (Manufacture)
```

### Sales Order

```python
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice

# Create SO
so = frappe.new_doc("Sales Order")
so.customer = "CUST-001"
so.delivery_date = frappe.utils.add_days(frappe.utils.today(), 7)
so.append("items", {
    "item_code": "ITEM-001",
    "qty": 10,
    "rate": 1000,
    "delivery_date": frappe.utils.add_days(frappe.utils.today(), 7)
})
so.insert()
so.submit()

# Create DN from SO
dn = make_delivery_note(so.name)
dn.save()
dn.submit()

# Create SI from SO
si = make_sales_invoice(so.name)
si.save()
si.submit()
```

### Purchase Order

```python
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt, make_purchase_invoice

po = frappe.new_doc("Purchase Order")
po.supplier = "SUPP-001"
po.append("items", {
    "item_code": "ITEM-001",
    "qty": 100,
    "rate": 500,
    "schedule_date": frappe.utils.add_days(frappe.utils.today(), 14)
})
po.insert()
po.submit()

# Create PR from PO
pr = make_purchase_receipt(po.name)
pr.save()
pr.submit()
```

### Stock Entry

```python
from erpnext.stock.doctype.stock_entry.stock_entry import make_stock_entry

# Material Receipt
se = make_stock_entry(item_code="ITEM-001", qty=100,
    to_warehouse="Stores - Company", rate=50, purpose="Material Receipt")
se.submit()

# Material Transfer
se = make_stock_entry(item_code="ITEM-001", qty=50,
    from_warehouse="Stores - Company", to_warehouse="Finished Goods - Company",
    purpose="Material Transfer")
se.submit()

# Get stock balance
from erpnext.stock.utils import get_stock_balance
qty = get_stock_balance("ITEM-001", "Stores - Company")
```

### Payment Entry

```python
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

# Payment against Sales Invoice
pe = get_payment_entry("Sales Invoice", "SINV-001")
pe.save()
pe.submit()

# Payment against Purchase Invoice
pe = get_payment_entry("Purchase Invoice", "PINV-001")
pe.save()
pe.submit()
```

### GL Entry (Journal Entry)

```python
je = frappe.new_doc("Journal Entry")
je.posting_date = frappe.utils.today()
je.append("accounts", {
    "account": "Debtors - Company",
    "debit_in_account_currency": 10000,
    "party_type": "Customer",
    "party": "CUST-001"
})
je.append("accounts", {
    "account": "Sales - Company",
    "credit_in_account_currency": 10000
})
je.insert()
je.submit()
```

### Lead Management (CRM)

```python
# Create Lead
lead = frappe.new_doc("Lead")
lead.lead_name = "John Doe"
lead.company_name = "ACME Corp"
lead.email_id = "john@acme.com"
lead.source = "Website"
lead.insert()

# Convert Lead to Customer
from erpnext.crm.doctype.lead.lead import make_customer
customer = make_customer(lead.name)
customer.save()
```

### Stock Valuation Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **FIFO** | First In First Out | Perishable goods, compliance |
| **Moving Average** | Weighted average | General merchandise |
| **LIFO** | Last In First Out | Specific accounting needs |

### Controller Override Pattern

```python
# hooks.py
override_doctype_class = {
    "Sales Invoice": "myapp.overrides.CustomSalesInvoice"
}

# myapp/overrides.py
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvoice(SalesInvoice):
    def validate(self):
        super().validate()  # ALWAYS call parent
        self.custom_validation()
```

### Controller Hook Decision

```
validate     → Changes to self ARE saved. Use for: validation, calculations
on_update    → Changes to self NOT saved. Use for: notifications, linked docs (use db_set)
on_submit    → After docstatus=1. Use for: stock/GL entries, status updates
on_cancel    → After docstatus=2. Use for: reverse entries
after_insert → Only new documents. Use for: auto-create linked docs
```

### Override Whitelisted Methods

Override ERPNext's built-in whitelisted functions without modifying core:

```python
# hooks.py
override_whitelisted_methods = {
    # Override make_sales_invoice from Sales Order
    "erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice":
        "dcnet_apps.overrides.selling.make_sales_invoice",
    # Override make_delivery_note
    "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note":
        "dcnet_apps.overrides.selling.make_delivery_note",
    # Override get_item_details
    "erpnext.stock.get_item_details.get_item_details":
        "dcnet_apps.overrides.stock.get_item_details",
}
```

```python
# dcnet_apps/overrides/selling.py
import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice as _original

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
    """Custom make_sales_invoice with additional logic."""
    # Call original
    si = _original(source_name, target_doc, ignore_permissions)
    # Add custom logic
    si.custom_source_order = source_name
    return si
```

### Property Setters

Modify stock DocType field properties without changing core:

```python
# Via code (in after_migrate or install)
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

# Change field property
make_property_setter("Sales Invoice", "customer", "reqd", "0", "Check")
make_property_setter("Sales Invoice", "due_date", "hidden", "1", "Check")
make_property_setter("Sales Invoice", "status", "options", "\nDraft\nPending\nPaid\nCustom Status", "Text")
make_property_setter("Sales Invoice", "posting_date", "default", "Today", "Text")

# DocType-level property (field_name=None)
make_property_setter("Sales Invoice", None, "quick_entry", "1", "Check")
make_property_setter("Sales Invoice", None, "track_changes", "1", "Check")

# Allow edit after submit
make_property_setter("Sales Invoice", "custom_field", "allow_on_submit", "1", "Check")
```

```python
# Via fixtures (hooks.py)
fixtures = [
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "DCNET Apps"]]
    }
]
```

### Workflow State Machine (ERPNext Workflow DocType)

```python
# Create workflow programmatically
def create_po_approval_workflow():
    if frappe.db.exists("Workflow", "PO Approval"):
        return

    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "name": "PO Approval",
        "document_type": "Purchase Order",
        "is_active": 1,
        "send_email_alert": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {"state": "Draft",            "doc_status": 0, "allow_edit": "Purchase User",    "style": ""},
            {"state": "Pending Approval", "doc_status": 0, "allow_edit": "Purchase Manager", "style": "Warning"},
            {"state": "Approved",         "doc_status": 1, "allow_edit": "Purchase Manager", "style": "Success"},
            {"state": "Rejected",         "doc_status": 0, "allow_edit": "Purchase Manager", "style": "Danger"},
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for Approval",
                "next_state": "Pending Approval",
                "allowed": "Purchase User",
                "condition": "doc.grand_total > 0"
            },
            {
                "state": "Pending Approval",
                "action": "Approve",
                "next_state": "Approved",
                "allowed": "Purchase Manager",
                "condition": ""
            },
            {
                "state": "Pending Approval",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Purchase Manager",
                "condition": ""
            },
            {
                "state": "Rejected",
                "action": "Revise",
                "next_state": "Draft",
                "allowed": "Purchase User",
                "condition": ""
            },
        ]
    })
    workflow.insert(ignore_permissions=True)
```

Key workflow rules:
- `workflow_state_field` must be a Select field on the DocType (auto-created if missing)
- `doc_status`: 0=Draft, 1=Submitted, 2=Cancelled — maps to ERPNext docstatus
- `allow_edit`: Role that can edit the document in this state
- `condition`: Python expression evaluated with `doc` context
- Only ONE workflow can be active per DocType at a time
- State changes trigger `doc_events` hooks (validate, on_submit, on_cancel)

### Permission Patterns

```python
# Check permission
if not frappe.has_permission("Sales Order", "write", doc=so):
    frappe.throw("No permission", frappe.PermissionError)

# Permission query conditions (hooks.py)
def get_permission_query_conditions(user):
    if not user: user = frappe.session.user
    if "Sales Manager" not in frappe.get_roles(user):
        return f"(`tabSales Order`.owner = {frappe.db.escape(user)})"

# has_permission hook
def has_permission(doc, ptype, user):
    if doc.department != frappe.db.get_value("Employee", {"user_id": user}, "department"):
        return False  # Deny access
```

### Jinja in Print Formats

```jinja
{# Print format for Sales Invoice #}
{% for item in doc.items %}
<tr>
    <td>{{ item.item_code }}</td>
    <td>{{ item.qty }}</td>
    <td>{{ frappe.format_value(item.rate, {"fieldtype": "Currency"}) }}</td>
    <td>{{ frappe.format_value(item.amount, {"fieldtype": "Currency"}) }}</td>
</tr>
{% endfor %}
<tr>
    <td colspan="3"><strong>Total</strong></td>
    <td>{{ frappe.format_value(doc.grand_total, {"fieldtype": "Currency"}) }}</td>
</tr>
```

### Custom App Structure

```
apps/my_custom_app/
├── pyproject.toml
├── my_custom_app/
│   ├── __init__.py          # MUST contain __version__ = "0.0.1"
│   ├── hooks.py
│   ├── modules.txt
│   ├── patches.txt          # [pre_model_sync] / [post_model_sync]
│   ├── patches/
│   ├── public/
│   └── templates/
```

---

## Existing Reference Directories

These reference directories from the original skills contain detailed API docs, tutorials, and examples.
Each old skill directory has its own set of references:

| Source Skill | api_reference/ | tutorials/ | test_examples/ | patterns/ |
|-------------|:-:|:-:|:-:|:-:|
| erpnext_accounting | 401 files | 280 guides | Yes | Yes |
| erpnext_stock | 194 files | 180 guides | Yes | Yes |
| erpnext_selling | 70 files | 42 guides | Yes | Yes |
| erpnext_buying | 54 files | 26 guides | Yes | Yes |
| erpnext_manufacturing | 106 files | 59 guides | Yes | Yes |
| erpnext_projects | 39 files | 22 guides | Yes | Yes |
| erpnext_setup | 74 files | 27 guides | Yes | Yes |
| erpnext_assets | 49 files | 44 guides | Yes | Yes |
| erpnext-crm | 59 files | 11 guides | Yes | Yes |

**Note:** After consolidation, old skill directories are deleted. Reference files are preserved in the old directories until fully migrated.

---

## Related Skills

- **frappe** - Frappe Framework (Document API, Database, Auth, Desk UI, Testing)
- **dcnet-module** - DCNET Flow module documentation builder

---

**Version 5.0.0** | Consolidated from: 9 ERPNext module skills + 6 external development skills
