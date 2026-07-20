# ERPNext Controllers

Controller hooks, execution order, decision tree for Controller vs Server Script, CRITICAL rules, common patterns, submittable document workflow, controller override via hooks.py, flags system, and anti-patterns.

---

## Controller vs Server Script Decision Tree

```
Need custom logic for a DocType?
├── Is it a simple field calculation or validation?
│   ├── Yes, and no Python imports needed -> Server Script
│   └── Yes, but needs imports or complex logic -> Controller
├── Does it need to interact with other modules?
│   └── Yes -> Controller (or doc_events in hooks.py)
├── Is it for a standard ERPNext DocType?
│   ├── Small hook (react to event) -> doc_events in hooks.py
│   ├── Override method behavior -> override_doctype_class in hooks.py
│   └── Add new methods (v16) -> extend_doctype_class in hooks.py
├── Is it for your custom DocType?
│   └── Yes -> Controller (my_doctype.py)
└── Quick prototype / non-developer?
    └── Server Script (but migrate to Controller for production)
```

| Criteria | Controller | Server Script |
|----------|-----------|---------------|
| Performance | Faster (compiled Python) | Slower (sandboxed) |
| Import modules | Yes (any Python) | Limited (restricted sandbox) |
| Version control | Yes (in app code) | No (stored in DB) |
| Debugging | Full Python debugging | Limited |
| Deployment | Deployed with app | Exported as fixture |
| Use case | Production code | Quick prototypes, admin tweaks |

---

## Which Hook to Use

### Hook Reference Table

| Hook | When It Runs | Use For | `self.x = y` Saved? |
|------|-------------|---------|---------------------|
| `autoname` | Before name is set | Custom naming logic | N/A |
| `before_insert` | Before first save (new doc) | Pre-insert validation | Yes |
| `validate` | Before every save | Validation, auto-calculation | Yes |
| `before_save` | After validate, before DB write | Last-minute changes | Yes |
| `on_update` | After save to DB | Post-save actions (notifications, etc.) | **NO** (use `db_set`) |
| `after_insert` | After first save (new doc) | Post-creation actions | **NO** (use `db_set`) |
| `before_submit` | Before docstatus 0->1 | Pre-submit validation | Yes |
| `on_submit` | After docstatus set to 1 | Post-submit actions (create linked docs) | **NO** (use `db_set`) |
| `before_cancel` | Before docstatus 1->2 | Pre-cancel validation | Yes |
| `on_cancel` | After docstatus set to 2 | Cleanup, reverse linked docs | **NO** (use `db_set`) |
| `on_trash` | Before document deletion | Prevent deletion, cleanup | N/A |
| `on_update_after_submit` | After save on submitted doc | Update allowed fields | **NO** (use `db_set`) |
| `before_rename` | Before name change | Validate rename | N/A |
| `after_rename` | After name change | Update references | N/A |
| `on_change` | After any DB change | Track field changes | N/A |

### CRITICAL Rule: self.x = y in on_update / on_submit NOT Saved

```python
class MyDocType(Document):
    # WRONG: Setting field in on_update does NOT persist
    def on_update(self):
        self.status = "Processed"      # NOT saved to DB!
        self.processed_date = today()  # NOT saved to DB!

    # CORRECT: Use db_set for post-save field updates
    def on_update(self):
        self.db_set("status", "Processed")
        self.db_set("processed_date", today())

        # Or multiple fields at once
        self.db_set({
            "status": "Processed",
            "processed_date": today()
        })

    # CORRECT: Put calculations in validate (runs before save)
    def validate(self):
        self.status = "Processed"      # This IS saved (validate runs before DB write)
        self.processed_date = today()  # This IS saved
```

---

## Execution Order

### INSERT (New Document)

```
1. autoname()
2. before_insert()
3. validate()
4. before_save()
5. [DB INSERT]
6. after_insert()
7. on_update()
8. on_change()
```

### SAVE (Existing Document)

```
1. validate()
2. before_save()
3. [DB UPDATE]
4. on_update()
5. on_change()
```

### SUBMIT (docstatus 0 -> 1)

```
1. validate()
2. before_save()
3. before_submit()
4. [DB UPDATE with docstatus=1]
5. on_update()
6. on_submit()
7. on_change()
```

### CANCEL (docstatus 1 -> 2)

```
1. before_cancel()
2. [DB UPDATE with docstatus=2]
3. on_cancel()
4. on_change()
```

### DELETE

```
1. on_trash()
2. [DB DELETE]
```

### UPDATE AFTER SUBMIT

```
1. validate()
2. before_save()
3. [DB UPDATE]
4. on_update()
5. on_update_after_submit()
6. on_change()
```

---

## Common Controller Patterns

### Validation Pattern

```python
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt, getdate, today

class MyDocType(Document):
    def validate(self):
        self.validate_dates()
        self.validate_amounts()
        self.calculate_totals()

    def validate_dates(self):
        if self.start_date and self.end_date:
            if getdate(self.start_date) > getdate(self.end_date):
                frappe.throw(_("Start Date cannot be after End Date"))

        if self.start_date and getdate(self.start_date) < getdate(today()):
            frappe.throw(_("Start Date cannot be in the past"))

    def validate_amounts(self):
        for item in self.items:
            if flt(item.qty) <= 0:
                frappe.throw(_("Row {0}: Quantity must be greater than 0").format(item.idx))
            if flt(item.rate) < 0:
                frappe.throw(_("Row {0}: Rate cannot be negative").format(item.idx))

    def calculate_totals(self):
        """Auto-calculate in validate -- values ARE saved."""
        self.total_qty = sum(flt(item.qty) for item in self.items)
        self.total_amount = sum(flt(item.amount) for item in self.items)
        self.grand_total = flt(self.total_amount) - flt(self.discount_amount)
```

### Auto-Calculate Child Table

```python
class MyDocType(Document):
    def validate(self):
        self.calculate_items()
        self.calculate_totals()

    def calculate_items(self):
        for item in self.items:
            item.amount = flt(item.qty) * flt(item.rate)
            item.net_amount = flt(item.amount) - flt(item.discount_amount)

    def calculate_totals(self):
        self.total = sum(flt(d.amount) for d in self.items)
        self.net_total = sum(flt(d.net_amount) for d in self.items)
        self.grand_total = flt(self.net_total) + flt(self.tax_amount)
```

### Detect Field Changes

```python
class MyDocType(Document):
    def validate(self):
        self.check_status_change()

    def check_status_change(self):
        """Detect if status changed from previous value."""
        if self.is_new():
            return  # No previous value for new docs

        old_status = self.db_get("status")  # Get value from DB (before save)
        if old_status != self.status:
            self.on_status_change(old_status, self.status)

    def on_status_change(self, old_status, new_status):
        if new_status == "Approved" and old_status == "Pending":
            self.approved_by = frappe.session.user
            self.approval_date = frappe.utils.today()
            self.notify_approval()
```

### Post-Save Actions (on_update / on_submit)

```python
class MyDocType(Document):
    def on_submit(self):
        self.create_stock_entry()
        self.send_notification()
        self.update_linked_docs()

    def create_stock_entry(self):
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Material Transfer"
        se.custom_reference = self.name
        for item in self.items:
            se.append("items", {
                "item_code": item.item_code,
                "qty": item.qty,
                "s_warehouse": self.source_warehouse,
                "t_warehouse": self.target_warehouse
            })
        se.insert()
        se.submit()

        # Save the reference back (use db_set since we're in on_submit)
        self.db_set("stock_entry", se.name)

    def send_notification(self):
        frappe.sendmail(
            recipients=[self.owner],
            subject=_("Document {0} Submitted").format(self.name),
            message=_("Your document has been submitted successfully.")
        )

    def on_cancel(self):
        self.cancel_stock_entry()

    def cancel_stock_entry(self):
        if self.stock_entry:
            se = frappe.get_doc("Stock Entry", self.stock_entry)
            se.cancel()
```

### Custom Naming (autoname)

```python
class MyDocType(Document):
    def autoname(self):
        # Pattern 1: Simple prefix + counter
        from frappe.model.naming import make_autoname
        self.name = make_autoname("PRJ-.YYYY.-.#####")
        # Result: PRJ-2026-00001

    # Pattern 2: Based on fields
    def autoname(self):
        self.name = f"{self.customer}-{self.item_code}-{frappe.utils.today()}"

    # Pattern 3: Hash (random)
    def autoname(self):
        self.name = frappe.generate_hash(length=10)

    # Pattern 4: Conditional naming
    def autoname(self):
        if self.is_return:
            self.name = make_autoname("RET-.YYYY.-.#####")
        else:
            self.name = make_autoname("ORD-.YYYY.-.#####")
```

---

## Submittable Document Workflow

### docstatus Flow

```
docstatus = 0 (Draft)
    ├── Save -> docstatus stays 0
    ├── Submit -> docstatus = 1 (Submitted)
    │   ├── Amend -> Creates new doc with docstatus = 0
    │   ├── Cancel -> docstatus = 2 (Cancelled)
    │   └── Update After Submit -> docstatus stays 1
    └── Delete -> Removed from DB
```

### Submittable DocType Setup

```python
# In DocType JSON: "is_submittable": 1

class MySubmittableDoc(Document):
    def validate(self):
        """Runs on save AND submit."""
        self.validate_items()

    def before_submit(self):
        """Last chance to validate before submission. self.x = y IS saved."""
        if not self.items:
            frappe.throw(_("Cannot submit without items"))
        self.submission_date = frappe.utils.today()

    def on_submit(self):
        """After submission. Use db_set for field updates."""
        self.create_downstream_docs()
        self.db_set("submitted_by", frappe.session.user)

    def before_cancel(self):
        """Validate cancellation."""
        if self.has_linked_submitted_docs():
            frappe.throw(_("Cannot cancel: linked documents exist"))

    def on_cancel(self):
        """Cleanup after cancellation."""
        self.reverse_downstream_docs()
        self.db_set("cancelled_by", frappe.session.user)

    def has_linked_submitted_docs(self):
        return frappe.db.exists("Downstream Doc", {
            "reference": self.name,
            "docstatus": 1
        })
```

---

## Controller Override via hooks.py

### Option 1: doc_events (Non-Breaking, Multiple Apps OK)

```python
# hooks.py
doc_events = {
    "Sales Order": {
        "validate": "my_app.overrides.so.validate_so",
        "on_submit": "my_app.overrides.so.on_so_submit",
    }
}

# my_app/overrides/so.py
def validate_so(doc, method):
    """doc = the Sales Order instance, method = "validate" string"""
    if doc.custom_requires_approval and not doc.custom_approved_by:
        frappe.throw(_("Approval is required before saving"))
```

### Option 2: override_doctype_class (Full Control, Single App Only)

```python
# hooks.py
override_doctype_class = {
    "Sales Order": "my_app.overrides.custom_so.CustomSalesOrder"
}

# my_app/overrides/custom_so.py
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

class CustomSalesOrder(SalesOrder):
    def validate(self):
        super().validate()           # ALWAYS call super first
        self.custom_validation()

    def on_submit(self):
        super().on_submit()          # ALWAYS call super first
        self.custom_post_submit()

    # Override an existing method
    def update_status(self, status):
        if status == "Closed" and self.custom_prevent_close:
            frappe.throw(_("This order cannot be closed"))
        super().update_status(status)
```

### Option 3: extend_doctype_class (v16 Only, Multiple Apps OK)

```python
# hooks.py
extend_doctype_class = {
    "Sales Order": "my_app.overrides.so_ext.SalesOrderExtension"
}

# my_app/overrides/so_ext.py
class SalesOrderExtension:
    """New methods available on all Sales Order instances."""

    def get_custom_summary(self):
        return {
            "total_items": len(self.items),
            "custom_score": self.calculate_custom_score()
        }

    def calculate_custom_score(self):
        return flt(self.grand_total) / max(len(self.items), 1)
```

---

## Flags System

### Built-in Flags

| Flag | Effect |
|------|--------|
| `doc.flags.ignore_permissions` | Skip all permission checks |
| `doc.flags.ignore_validate` | Skip validate() hook |
| `doc.flags.ignore_mandatory` | Skip mandatory field checks |
| `doc.flags.ignore_links` | Skip link validation |
| `doc.flags.ignore_validate_update_after_submit` | Skip update-after-submit validation |
| `doc.flags.in_import` | Document is being imported |
| `doc.flags.in_patch` | Running inside a patch |

### Custom Flags

```python
# Set a flag to communicate between hooks
class MyDocType(Document):
    def validate(self):
        if self.some_condition:
            self.flags.skip_notification = True

    def on_update(self):
        if not self.flags.skip_notification:
            self.send_notification()

# Set flag from external code
doc = frappe.get_doc("Sales Order", "SO-00001")
doc.flags.from_api = True
doc.flags.ignore_permissions = True
doc.save()
```

### Flags in doc_events

```python
# hooks.py handler
def on_submit(doc, method):
    if doc.flags.get("skip_custom_logic"):
        return
    # ... custom logic ...

# Caller sets flag
doc = frappe.get_doc("Sales Order", "SO-00001")
doc.flags.skip_custom_logic = True
doc.submit()
```

---

## Anti-Patterns

### 1. Setting Fields After Save

```python
# WRONG
def on_update(self):
    self.status = "Processed"          # NOT saved!

# CORRECT
def on_update(self):
    self.db_set("status", "Processed") # Saved to DB

# BEST: Put in validate if possible
def validate(self):
    self.status = "Processed"          # Saved (runs before DB write)
```

### 2. Not Calling super()

```python
# WRONG: Breaks ERPNext logic
class CustomSalesOrder(SalesOrder):
    def validate(self):
        self.my_validation()   # ERPNext validate never runs!

# CORRECT
class CustomSalesOrder(SalesOrder):
    def validate(self):
        super().validate()     # ERPNext validate runs first
        self.my_validation()
```

### 3. Using save() Inside validate/before_save

```python
# WRONG: Infinite recursion
def validate(self):
    other_doc = frappe.get_doc("Other DocType", self.reference)
    other_doc.status = "Linked"
    other_doc.save()           # This triggers other_doc.validate -> potential cascade

# CORRECT: Use db_set for cross-doc updates in hooks
def on_update(self):
    frappe.db.set_value("Other DocType", self.reference, "status", "Linked")
```

### 4. Heavy Operations in validate

```python
# WRONG: Slow save
def validate(self):
    for item in self.items:
        stock = get_stock_balance(item.item_code, item.warehouse)  # DB query per row
        if stock < item.qty:
            frappe.throw(...)

# BETTER: Batch query
def validate(self):
    item_codes = [item.item_code for item in self.items]
    stock_map = get_stock_balance_batch(item_codes, self.warehouse)
    for item in self.items:
        if stock_map.get(item.item_code, 0) < item.qty:
            frappe.throw(...)
```

### 5. Ignoring docstatus in Queries

```python
# WRONG: Includes cancelled documents
total = frappe.db.sql("SELECT SUM(grand_total) FROM `tabSales Order`")[0][0]

# CORRECT: Filter by docstatus
total = frappe.db.sql("""
    SELECT SUM(grand_total) FROM `tabSales Order` WHERE docstatus = 1
""")[0][0]
```

### 6. Not Handling is_new()

```python
# WRONG: db_get fails on new document
def validate(self):
    old_value = self.db_get("status")  # Crashes if doc is new

# CORRECT
def validate(self):
    if not self.is_new():
        old_value = self.db_get("status")
```
