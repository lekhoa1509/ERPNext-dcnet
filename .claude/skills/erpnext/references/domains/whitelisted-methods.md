# ERPNext Whitelisted Methods

Patterns for `@frappe.whitelist()` in ERPNext controllers, common `make_*` and `get_*` methods, permission handling, response formatting, and mapped document creation.

---

## @frappe.whitelist() Basics

### What It Does

`@frappe.whitelist()` exposes a Python function as an HTTP API endpoint callable from the client side. Without it, `frappe.call()` from JS will return a 403 Forbidden.

```python
import frappe
from frappe import _

@frappe.whitelist()
def get_item_stock(item_code, warehouse=None):
    """Callable via frappe.call('myapp.api.get_item_stock', {item_code: 'ITEM-001'})"""
    from erpnext.stock.utils import get_stock_balance
    if warehouse:
        return get_stock_balance(item_code, warehouse)
    return frappe.get_all("Bin",
        filters={"item_code": item_code, "actual_qty": [">", 0]},
        fields=["warehouse", "actual_qty"]
    )
```

### Key Parameters

| Parameter | Usage | Description |
|-----------|-------|-------------|
| `@frappe.whitelist()` | Default | Requires logged-in user |
| `@frappe.whitelist(allow_guest=True)` | Public API | No login required (use with caution) |
| `@frappe.whitelist(methods=["POST"])` | Restrict HTTP method | Only allow POST requests |

### Permission Check Inside Whitelisted Methods

```python
@frappe.whitelist()
def approve_order(order_name):
    # Always validate permissions inside whitelisted methods
    frappe.has_permission("Sales Order", "write", throw=True)

    doc = frappe.get_doc("Sales Order", order_name)
    doc.custom_approved = 1
    doc.save()
    return doc.name
```

---

## Common make_* Patterns (Document Creation)

### Sales Flow make_* Methods

| Method | Source | Target | Module Path |
|--------|--------|--------|-------------|
| `make_sales_order` | Quotation | Sales Order | `erpnext.selling.doctype.quotation.quotation` |
| `make_delivery_note` | Sales Order | Delivery Note | `erpnext.selling.doctype.sales_order.sales_order` |
| `make_sales_invoice` | Sales Order | Sales Invoice | `erpnext.selling.doctype.sales_order.sales_order` |
| `make_sales_invoice` | Delivery Note | Sales Invoice | `erpnext.stock.doctype.delivery_note.delivery_note` |
| `make_purchase_order` | Sales Order | Purchase Order | `erpnext.selling.doctype.sales_order.sales_order` |
| `make_material_request` | Sales Order | Material Request | `erpnext.selling.doctype.sales_order.sales_order` |
| `create_pick_list` | Sales Order | Pick List | `erpnext.selling.doctype.sales_order.sales_order` |

### Buying Flow make_* Methods

| Method | Source | Target | Module Path |
|--------|--------|--------|-------------|
| `make_purchase_order` | Supplier Quotation | Purchase Order | `erpnext.buying.doctype.supplier_quotation.supplier_quotation` |
| `make_purchase_order` | Material Request | Purchase Order | `erpnext.stock.doctype.material_request.material_request` |
| `make_purchase_receipt` | Purchase Order | Purchase Receipt | `erpnext.buying.doctype.purchase_order.purchase_order` |
| `make_purchase_invoice` | Purchase Order | Purchase Invoice | `erpnext.buying.doctype.purchase_order.purchase_order` |
| `make_rm_stock_entry` | Purchase Order | Stock Entry | `erpnext.buying.doctype.purchase_order.purchase_order` |

### Accounts Flow make_* Methods

| Method | Source | Target | Module Path |
|--------|--------|--------|-------------|
| `get_payment_entry` | Sales Invoice | Payment Entry | `erpnext.accounts.doctype.payment_entry.payment_entry` |
| `get_payment_entry` | Purchase Invoice | Payment Entry | `erpnext.accounts.doctype.payment_entry.payment_entry` |
| `get_payment_entry` | Sales Order | Payment Entry | `erpnext.accounts.doctype.payment_entry.payment_entry` |
| `make_debit_note` | Sales Invoice | Sales Invoice (return) | `erpnext.accounts.doctype.sales_invoice.sales_invoice` |
| `make_sales_return` | Delivery Note | Delivery Note (return) | `erpnext.stock.doctype.delivery_note.delivery_note` |

### CRM Flow make_* Methods

| Method | Source | Target | Module Path |
|--------|--------|--------|-------------|
| `make_customer` | Lead | Customer | `erpnext.crm.doctype.lead.lead` |
| `make_opportunity` | Lead | Opportunity | `erpnext.crm.doctype.lead.lead` |
| `make_quotation` | Opportunity | Quotation | `erpnext.crm.doctype.opportunity.opportunity` |
| `make_quotation` | Lead | Quotation | `erpnext.crm.doctype.lead.lead` |

---

## Common get_* Patterns (Data Retrieval)

### Item Details

```python
from erpnext.stock.get_item_details import get_item_details

@frappe.whitelist()
def get_item_details(args):
    """Called when item_code is selected in a transaction form.
    Returns rate, warehouse, account, tax template, etc."""
    # args is a JSON string from client
    return get_item_details(args)
```

### Payment Entry

```python
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

@frappe.whitelist()
def get_payment_entry(dt, dn, party_amount=None, bank_account=None, bank_amount=None):
    """Create Payment Entry from Sales Invoice / Purchase Invoice / Sales Order / Purchase Order"""
    return get_payment_entry(dt, dn, party_amount, bank_account, bank_amount)
```

### Party Details

```python
from erpnext.accounts.party import get_party_details

@frappe.whitelist()
def get_party_details(party=None, party_type="Customer", **kwargs):
    """Get address, contact, account, price list, etc. for a party.
    Called when customer/supplier is selected in transaction."""
    return get_party_details(party, party_type, **kwargs)
```

---

## Mapped Document Creation with frappe.model.mapper

### get_mapped_doc Pattern

The `get_mapped_doc` function is the core mechanism behind all `make_*` methods. It copies fields from a source document to a target document based on a field mapping definition.

```python
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.run_method("set_missing_values")
        target.run_method("set_po_nos")
        target.run_method("calculate_taxes_and_totals")

    def update_item(source_doc, target_doc, source_parent):
        target_doc.qty = flt(source_doc.qty) - flt(source_doc.delivered_qty)
        target_doc.stock_qty = target_doc.qty * flt(source_doc.conversion_factor)

    def condition(doc):
        # Only map items that have pending delivery
        return abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier != 1

    doclist = get_mapped_doc(
        "Sales Order",           # Source DocType
        source_name,             # Source document name
        {
            "Sales Order": {     # Parent mapping
                "doctype": "Delivery Note",
                "validation": {
                    "docstatus": ["=", 1]   # Source must be submitted
                },
                "field_map": {
                    "name": "against_sales_order",   # SO name -> DN.against_sales_order
                }
            },
            "Sales Order Item": {   # Child table mapping
                "doctype": "Delivery Note Item",
                "field_map": {
                    "rate": "rate",
                    "name": "so_detail",             # SO Item name -> DN Item.so_detail
                    "parent": "against_sales_order",
                },
                "postprocess": update_item,          # Called per row after mapping
                "condition": condition,              # Filter: only include if True
            },
            "Sales Taxes and Charges": {   # Another child table
                "doctype": "Sales Taxes and Charges",
                "add_if_empty": True
            }
        },
        target_doc,                # Existing target doc (for amendments)
        set_missing_values         # Called once after all mapping
    )

    return doclist
```

### Field Mapping Options

| Key | Purpose | Example |
|-----|---------|---------|
| `"doctype"` | Target DocType | `"Delivery Note"` |
| `"field_map"` | Source field -> Target field | `{"name": "so_detail"}` |
| `"field_no_map"` | Fields to exclude | `["naming_series"]` |
| `"validation"` | Source doc validation | `{"docstatus": ["=", 1]}` |
| `"condition"` | Row filter function | `lambda doc: doc.qty > 0` |
| `"postprocess"` | Per-row modification | `update_item` function |
| `"add_if_empty"` | Add even if source empty | `True` |

---

## Response Formatting

### Return Values from Whitelisted Methods

```python
@frappe.whitelist()
def simple_return():
    """Simple value -- available as r.message in JS"""
    return "success"

@frappe.whitelist()
def dict_return():
    """Dict -- available as r.message in JS"""
    return {"status": "ok", "count": 42}

@frappe.whitelist()
def doc_return(name):
    """Document -- serialized to dict automatically"""
    return frappe.get_doc("Sales Order", name)

@frappe.whitelist()
def list_return():
    """List of dicts"""
    return frappe.get_all("Item", fields=["name", "item_name"], limit=10)
```

### Client-Side Calling

```javascript
// Basic call
frappe.call({
    method: 'myapp.api.get_item_stock',
    args: { item_code: 'ITEM-001' },
    callback: function(r) {
        if (r.message) {
            console.log(r.message);  // The return value
        }
    }
});

// Async/await style
let r = await frappe.call({
    method: 'myapp.api.get_item_stock',
    args: { item_code: 'ITEM-001' }
});
console.log(r.message);

// Call a DocType method (controller method exposed via whitelist)
frappe.call({
    method: 'approve',                          // Method name on the controller
    doc: cur_frm.doc,                           // Current document
    callback: function(r) { cur_frm.reload_doc(); }
});

// Call via document (runs on server-side controller)
frappe.xcall('erpnext.selling.doctype.sales_order.sales_order.make_delivery_note', {
    source_name: 'SO-00001'
}).then(doc => {
    frappe.model.sync(doc);
    frappe.set_route('Form', doc.doctype, doc.name);
});
```

---

## Writing Custom Whitelisted Methods

### Pattern: Action on Document

```python
@frappe.whitelist()
def custom_approve(docname):
    """Approve a custom document with permission check and validation."""
    doc = frappe.get_doc("My Custom DocType", docname)

    # Permission check
    if not frappe.has_permission("My Custom DocType", "write", doc):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    # Validation
    if doc.docstatus != 1:
        frappe.throw(_("Document must be submitted before approval"))

    if doc.status == "Approved":
        frappe.throw(_("Document is already approved"))

    # Action
    doc.status = "Approved"
    doc.approved_by = frappe.session.user
    doc.approval_date = frappe.utils.today()
    doc.save(ignore_permissions=True)

    # Notification
    frappe.msgprint(_("Document {0} has been approved").format(docname))

    return doc.name
```

### Pattern: Bulk Action

```python
@frappe.whitelist()
def bulk_update_status(names, status):
    """Update status for multiple documents. names is a JSON string from client."""
    import json
    if isinstance(names, str):
        names = json.loads(names)

    updated = []
    errors = []
    for name in names:
        try:
            doc = frappe.get_doc("My DocType", name)
            doc.status = status
            doc.save()
            updated.append(name)
        except Exception as e:
            errors.append({"name": name, "error": str(e)})

    frappe.db.commit()
    return {"updated": updated, "errors": errors}
```

### Pattern: Search / Query Endpoint

```python
@frappe.whitelist()
def get_available_items(warehouse, item_group=None, search_term=None):
    """Get items with stock available in a specific warehouse."""
    filters = {"actual_qty": [">", 0], "warehouse": warehouse}
    if item_group:
        filters["item_group"] = item_group

    bin_data = frappe.get_all("Bin",
        filters=filters,
        fields=["item_code", "actual_qty", "reserved_qty", "projected_qty"]
    )

    result = []
    for b in bin_data:
        item = frappe.get_cached_doc("Item", b.item_code)
        if search_term and search_term.lower() not in item.item_name.lower():
            continue
        result.append({
            "item_code": b.item_code,
            "item_name": item.item_name,
            "available_qty": flt(b.actual_qty) - flt(b.reserved_qty),
            "uom": item.stock_uom
        })

    return sorted(result, key=lambda x: x["item_name"])
```

### Pattern: File/Report Generation

```python
@frappe.whitelist()
def generate_report_pdf(filters):
    """Generate a PDF report and return file URL."""
    import json
    if isinstance(filters, str):
        filters = json.loads(filters)

    html = frappe.render_template("myapp/templates/report.html", {"data": get_report_data(filters)})

    from frappe.utils.pdf import get_pdf
    pdf = get_pdf(html)

    file_name = f"Report_{frappe.utils.today()}.pdf"
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": file_name,
        "content": pdf,
        "is_private": 1
    })
    file_doc.save(ignore_permissions=True)

    return file_doc.file_url
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|------------------|
| No permission check inside whitelist | Any logged-in user can call it | Always check `frappe.has_permission()` |
| Using `eval()` or `exec()` with user input | Security vulnerability | Use `json.loads()` for JSON, validate input |
| Not validating input types | Unexpected errors | Use `flt()`, `cint()`, `cstr()` for type conversion |
| Returning sensitive data | Data leak | Filter fields before returning |
| Heavy computation in sync call | Timeout on client | Use `frappe.enqueue()` for long tasks |
| Missing `@frappe.whitelist()` | 403 error from client | Always decorate public methods |
| Forgetting `frappe.db.commit()` in enqueued jobs | Changes lost | Enqueued functions auto-commit, but manual commit needed in loops |
