# ERPNext Errors & Permissions

Common exceptions, the permission system (Role, DocPerm, User Permission), has_permission hooks, permission_query_conditions for list filtering, error handling patterns, and client-side error handling.

---

## Common Exceptions

### Frappe Built-in Exceptions

| Exception | When Raised | Example |
|-----------|-------------|---------|
| `frappe.ValidationError` | Business logic validation fails | `frappe.throw("Qty must be > 0", exc=frappe.ValidationError)` |
| `frappe.PermissionError` | User lacks required permission | `frappe.throw("Not permitted", exc=frappe.PermissionError)` |
| `frappe.MandatoryError` | Required field is empty | Auto-raised on save if mandatory field missing |
| `frappe.LinkValidationError` | Link field points to non-existent doc | Auto-raised if linked doc does not exist |
| `frappe.DuplicateEntryError` | Unique constraint violation | Auto-raised on duplicate name/unique field |
| `frappe.TimestampMismatchError` | Concurrent edit conflict | Auto-raised when `modified` timestamp differs |
| `frappe.DoesNotExistError` | Document not found | `frappe.get_doc("Sales Order", "NONEXISTENT")` |
| `frappe.AuthenticationError` | Invalid login credentials | Login failure |
| `frappe.OutgoingEmailError` | Email sending fails | SMTP errors |
| `frappe.InvalidStatusError` | Invalid status transition | Workflow violations |
| `frappe.DataError` | Data integrity issue | Invalid data types |
| `frappe.UniqueValidationError` | Unique field constraint | Duplicate value in unique field |

### ERPNext-Specific Exceptions

```python
# Stock exceptions
from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import NegativeStockError
# Raised when stock goes negative and negative stock is not allowed

# Workflow exceptions (Frappe)
from frappe.model.workflow import WorkflowTransitionError
# Raised when an invalid workflow transition is attempted
# NOTE: frappe.exceptions.InvalidTransitionError does NOT exist

# Over-limit exceptions
from erpnext.controllers.selling_controller import CreditLimitExceeded
# Raised when customer credit limit is exceeded (subclass of ValidationError)
```

---

## Using frappe.throw()

### Basic Usage

```python
import frappe
from frappe import _

# Simple error
frappe.throw(_("Item {0} is not available").format(item_code))

# With specific exception type
frappe.throw(_("Insufficient stock for {0}").format(item_code), exc=frappe.ValidationError)

# With title
frappe.throw(
    msg=_("Cannot submit this order"),
    title=_("Validation Error"),
    exc=frappe.ValidationError
)

# Non-blocking message (does NOT stop execution)
frappe.msgprint(_("Warning: Low stock for {0}").format(item_code))
frappe.msgprint(_("Check stock levels"), indicator="orange", alert=True)

# Raise without message to user (silent, logged only)
raise frappe.ValidationError("internal error detail")
```

### Conditional Throw Patterns

```python
# Throw if condition fails
if flt(doc.qty) <= 0:
    frappe.throw(_("Quantity must be greater than zero"))

# Collect multiple errors then throw
errors = []
for item in doc.items:
    if not item.warehouse:
        errors.append(_("Row {0}: Warehouse is required for {1}").format(item.idx, item.item_code))
    if flt(item.qty) <= 0:
        errors.append(_("Row {0}: Qty must be > 0 for {1}").format(item.idx, item.item_code))

if errors:
    frappe.throw("<br>".join(errors), title=_("Validation Errors"))
```

---

## Permission System Overview

### Permission Layers (evaluated top to bottom)

```
Layer 1: Role Permission (DocPerm)
    "Can this role READ/WRITE/CREATE/DELETE/SUBMIT this DocType?"

Layer 2: User Permission
    "Can this user access documents where field X = value Y?"
    (e.g., user can only see Sales Orders where company = "My Company")

Layer 3: Role Permission for Page and Report
    "Can this role access this specific Page or Report?"

Layer 4: has_permission hook (custom code)
    "Custom logic to allow/deny access"

Layer 5: permission_query_conditions (list filtering)
    "Additional WHERE clause for list queries"
```

### Layer 1: Role Permission (DocPerm)

Defined in DocType JSON or via Setup > Role Permission Manager.

| Permission | Level | Description |
|------------|-------|-------------|
| `read` | 0 | View document |
| `write` | 0 | Edit document |
| `create` | 0 | Create new document |
| `delete` | 0 | Delete document |
| `submit` | 0 | Submit document (docstatus 0->1) |
| `cancel` | 0 | Cancel document (docstatus 1->2) |
| `amend` | 0 | Amend cancelled document |
| `report` | 0 | Access in Report Builder |
| `import` | 0 | Data Import |
| `export` | 0 | Data Export |
| `print` | 0 | Print |
| `email` | 0 | Email |
| `share` | 0 | Share with other users |

```python
# Check role permission programmatically
frappe.has_permission("Sales Order", "write")          # Current user
frappe.has_permission("Sales Order", "write", doc=doc) # Specific document
frappe.has_permission("Sales Order", "write", user="user@example.com")

# Throw if no permission
frappe.has_permission("Sales Order", "write", throw=True)

# Check specific role
frappe.get_roles()  # Current user's roles
"Sales Manager" in frappe.get_roles()
```

### Layer 2: User Permission

Restricts access based on Link field values. Configured via Setup > User Permission.

```python
# Create User Permission
frappe.get_doc({
    "doctype": "User Permission",
    "user": "salesperson@example.com",
    "allow": "Company",             # DocType to restrict
    "for_value": "My Company",      # Allowed value
    "applicable_for": "Sales Order" # Only apply to this DocType (optional)
}).insert()

# Check user permissions programmatically
from frappe.permissions import get_user_permissions
perms = get_user_permissions("salesperson@example.com")
# Returns: {"Company": [{"doc": "My Company", ...}], ...}
```

### Layer 3: Role Permission for Page and Report

```python
# Grant access to a Page
frappe.get_doc({
    "doctype": "Role Permission for Page and Report",
    "page": "my-custom-page",
    "role": "Sales Manager"
}).insert()

# Grant access to a Report
frappe.get_doc({
    "doctype": "Role Permission for Page and Report",
    "report": "My Custom Report",
    "role": "Sales Manager"
}).insert()
```

---

## has_permission Hook

Custom permission logic via `hooks.py`. Runs after standard permission checks.

### In hooks.py

```python
# hooks.py
has_permission = {
    "Sales Order": "myapp.permissions.sales_order_permission",
    "My Custom DocType": "myapp.permissions.custom_permission"
}
```

### Permission Function

```python
# myapp/permissions.py
import frappe

def sales_order_permission(doc, ptype, user):
    """
    Custom permission check for Sales Order.

    Args:
        doc: The document being checked (None for list view)
        ptype: Permission type ("read", "write", "create", etc.)
        user: User being checked

    Returns:
        True  -> Allow (overrides deny)
        False -> Deny (blocks access)
        None  -> Don't interfere (let standard permissions decide)
    """
    # Example: Only Sales Manager can see orders > 1M
    if doc and ptype == "read":
        if flt(doc.grand_total) > 1000000:
            if "Sales Manager" not in frappe.get_roles(user):
                return False

    # Return None to not interfere with standard permissions
    return None
```

### CRITICAL Rules

| Return Value | Effect |
|-------------|--------|
| `True` | Allow access (careful: overrides standard denials) |
| `False` | Deny access (hard deny) |
| `None` | Do not interfere (standard permissions apply) |

```python
# WRONG: Returning True grants access even if user has no role permission
def bad_permission(doc, ptype, user):
    if some_condition:
        return True   # Dangerous! Bypasses role permissions

# CORRECT: Only deny, never grant
def good_permission(doc, ptype, user):
    if should_deny:
        return False
    return None   # Let standard permissions handle the rest
```

---

## permission_query_conditions

Adds WHERE clauses to list queries for filtering documents in list view.

### In hooks.py

```python
# hooks.py
permission_query_conditions = {
    "Sales Order": "myapp.permissions.so_query_conditions",
}
```

### Query Conditions Function

```python
def so_query_conditions(user):
    """
    Return additional WHERE clause for Sales Order list view.

    Args:
        user: The user viewing the list

    Returns:
        SQL condition string (without WHERE keyword) or empty string
    """
    if user == "Administrator":
        return ""  # No restriction for admin

    # Restrict to user's territory
    territories = frappe.get_all("User Permission",
        filters={"user": user, "allow": "Territory"},
        pluck="for_value"
    )

    if territories:
        territory_list = ", ".join(f"'{t}'" for t in territories)
        return f"`tabSales Order`.territory IN ({territory_list})"

    return ""  # No restriction if no territory assigned
```

### Combined with has_permission

```python
# hooks.py -- both work together
has_permission = {
    "Sales Order": "myapp.permissions.so_has_permission"       # Per-document check
}
permission_query_conditions = {
    "Sales Order": "myapp.permissions.so_query_conditions"     # List filtering
}

# has_permission runs when: opening a specific document, checking API access
# permission_query_conditions runs when: loading list view, report queries
```

---

## Client-Side Error Handling

### JavaScript Error Handling

```javascript
// Standard call with error handling
frappe.call({
    method: 'myapp.api.risky_operation',
    args: { name: 'DOC-001' },
    callback: function(r) {
        if (r.message) {
            frappe.show_alert({message: __('Success!'), indicator: 'green'});
        }
    },
    error: function(r) {
        // Called on HTTP error (500, 403, etc.)
        frappe.show_alert({message: __('Operation failed'), indicator: 'red'});
    }
});

// Try/catch with async
try {
    let r = await frappe.xcall('myapp.api.risky_operation', { name: 'DOC-001' });
    frappe.show_alert({message: __('Done'), indicator: 'green'});
} catch (e) {
    console.error(e);
    frappe.show_alert({message: __('Failed'), indicator: 'red'});
}

// Handle specific server-side exceptions
frappe.call({
    method: 'myapp.api.check_stock',
    args: { item: 'ITEM-001' },
    callback: function(r) {
        // r.exc_type contains the exception class name if error occurred
    },
    error: function(r) {
        if (r.exc_type === 'ValidationError') {
            // Handle validation error
        } else if (r.exc_type === 'PermissionError') {
            // Handle permission error
        }
    }
});
```

### Form-Level Error Display

```javascript
// In form script
frappe.ui.form.on('My DocType', {
    validate: function(frm) {
        if (!frm.doc.some_field) {
            frappe.throw(__('Some Field is required'));
            // Stops save
        }

        // Non-blocking warning
        frappe.msgprint({
            title: __('Warning'),
            indicator: 'orange',
            message: __('Consider filling in optional field')
        });
    }
});
```

---

## Permission Debugging

### Useful Commands

```python
# Check all permissions for a user on a doctype
from frappe.permissions import get_doc_permissions
perms = get_doc_permissions(frappe.get_doc("Sales Order", "SO-00001"), user="user@example.com")
# Returns: {"read": 1, "write": 1, "create": 0, "delete": 0, ...}

# Check user permissions (link-level restrictions)
from frappe.permissions import get_user_permissions
user_perms = get_user_permissions("user@example.com")

# Get all roles for a user
roles = frappe.get_roles("user@example.com")

# Check if user has specific role
has_role = frappe.db.exists("Has Role", {"parent": "user@example.com", "role": "Sales Manager"})

# Debug: print permission check result
print(frappe.has_permission("Sales Order", "write", doc="SO-00001", user="user@example.com"))
```

### Common Permission Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| 403 on form open | Missing read permission for role | Add Role Permission |
| Can see list but not document | User Permission restricting specific docs | Check User Permission for Link fields |
| Can read but not save | Missing write permission | Add write to Role Permission |
| Submit button missing | Missing submit permission or wrong docstatus | Check submit permission and docstatus |
| Report shows no data | permission_query_conditions filtering | Check conditions function |
| API returns 403 | Missing `@frappe.whitelist()` or no role permission | Add decorator and check roles |
| Can save but validation error | has_permission returning False | Check has_permission hook |
