<!-- Source: frappe skill (original) -->

# Frappe Framework Codebase Analysis

## Description

This skill provides comprehensive knowledge of the **Frappe Framework** extracted from deep codebase analysis. It covers the core Document ORM, Database API, Authentication system, Workflow engine, and Web Framework patterns.

**Source:** Codebase analysis of Frappe Framework
**Path:** `/Users/vovanduc/Code/dcnet/flow_next/development/frappe-bench/apps/frappe/frappe`
**Files Analyzed:** 1248
**Languages:** Python (82.9%), JavaScript (17.1%)
**Analysis Depth:** Full (API Reference, Design Patterns, Test Examples, Architecture)

---

## When to Use This Skill

### Primary Use Cases

Use this skill when you need to:

1. **Document Operations (CRUD)**
   - Create, read, update, delete documents
   - Work with child tables and linked documents
   - Handle document lifecycle hooks (`validate`, `on_update`, `on_submit`, etc.)
   - Understand `docstatus` transitions (Draft → Submitted → Cancelled)

2. **Database Operations**
   - Execute raw SQL queries with `frappe.db.sql()`
   - Use ORM methods like `get_value()`, `get_list()`, `set_value()`
   - Handle transactions, commits, and rollbacks
   - Work with MariaDB/MySQL or SQLite backends

3. **Authentication & Authorization**
   - Implement login/logout flows
   - Validate API keys, OAuth tokens
   - Check permissions with `has_permission()`
   - Handle session management

4. **Automation & Workflows**
   - Create workflow state machines
   - Set up Auto Repeat for recurring documents
   - Configure Assignment Rules
   - Use Notification triggers

5. **Web Framework**
   - Build REST APIs with `@frappe.whitelist()`
   - Create web pages with Jinja templates
   - Handle WSGI request/response cycle
   - Implement rate limiting

### Trigger Keywords

- `frappe.get_doc`, `frappe.new_doc`, `frappe.db`
- `docstatus`, `validate`, `on_update`, `on_submit`
- `frappe.whitelist`, `frappe.call`
- `LoginManager`, `HTTPRequest`, `CookieManager`
- Workflow, Auto Repeat, Assignment Rule

---

## Quick Reference

### Codebase Statistics

| Metric | Value |
|--------|-------|
| **Python Files** | 1,035 (82.9%) |
| **JavaScript Files** | 213 (17.1%) |
| **Total Test Examples** | 1,478 |
| **API Functions Documented** | 1,100+ |
| **Tutorials Generated** | 369 |

### Design Patterns Detected

*From C3.1 codebase analysis (confidence > 0.7)*

| Pattern | Instances | Primary Usage |
|---------|-----------|---------------|
| **Factory** | 198 | Document creation, Controller loading |
| **Strategy** | 85 | Report generation, Export formats |
| **Observer** | 54 | Document hooks, Notifications |
| **Builder** | 23 | Query building, Form construction |
| **Template Method** | 7 | Document lifecycle methods |

### Architectural Patterns

- **MVC (Model-View-Controller)** - confidence: 0.90
  - Model: DocType definitions, Document class
  - View: Jinja templates, Desk UI
  - Controller: Python controllers, Client Scripts

- **Layered Architecture (2-tier)** - confidence: 0.85
  - Presentation Layer: Web UI, REST API
  - Data Layer: Database abstraction, ORM

---

## Key Concepts

### 1. Document Class

The `Document` class is the heart of Frappe's ORM. All DocType controllers inherit from it.

**Core Methods:**

| Method | Description |
|--------|-------------|
| `insert()` | Create new document in database |
| `save()` | Update existing document |
| `submit()` | Set `docstatus=1`, trigger `on_submit` |
| `cancel()` | Set `docstatus=2`, trigger `on_cancel` |
| `delete()` | Remove document from database |
| `reload()` | Refresh from database |
| `db_set()` | Direct database update (bypasses hooks) |

**Lifecycle Hooks:**

```
Before Insert: before_insert → validate → before_save
After Insert:  on_update → after_insert

Before Update: validate → before_save
After Update:  on_update

Before Submit: validate → before_submit
After Submit:  on_update → on_submit

Before Cancel: before_cancel
After Cancel:  on_cancel
```

### 2. DocStatus Transitions

```
Draft (0) ──save──→ Draft (0)
Draft (0) ──submit─→ Submitted (1)
Submitted (1) ──save──→ Submitted (1) [update_after_submit]
Submitted (1) ──cancel─→ Cancelled (2)
```

### 3. Permission Levels

| Level | Meaning |
|-------|---------|
| 0 | Basic fields (default) |
| 1+ | Restricted fields |
| `permlevel` | Field-level access control |

---

## Code Examples

### Document CRUD Operations

**Creating a Document** *(From codebase analysis)*

```python
# Method 1: Using new_doc (recommended)
doc = frappe.new_doc("ToDo")
doc.description = "Complete task"
doc.assigned_by = "Administrator"
doc.insert()

# Method 2: Using get_doc with dict
doc = frappe.get_doc({
    "doctype": "ToDo",
    "description": "Complete task",
    "assigned_by": "Administrator"
}).insert()

# Method 3: With child tables
sales_order = frappe.new_doc("Sales Order")
sales_order.customer = "CUST-001"
sales_order.append("items", {
    "item_code": "ITEM-001",
    "qty": 10
})
sales_order.insert()
```

**Reading Documents** *(From codebase analysis)*

```python
# Get single document
doc = frappe.get_doc("Customer", "CUST-001")

# Get with permission check
doc = frappe.get_doc("Customer", "CUST-001", check_permission=True)

# Get cached (for frequently accessed docs)
doc = frappe.get_cached_doc("Customer", "CUST-001")

# Get single value
email = frappe.db.get_value("User", "john@example.com", "email")

# Get multiple values
user = frappe.db.get_value("User", "john@example.com",
    ["email", "full_name"], as_dict=True)

# Get list with filters
customers = frappe.get_all("Customer",
    filters={"territory": "United States"},
    fields=["name", "customer_name", "email_id"],
    limit=10
)
```

**Updating Documents** *(From codebase analysis)*

```python
# Standard update (triggers hooks)
doc = frappe.get_doc("Customer", "CUST-001")
doc.customer_name = "Updated Name"
doc.save()

# Direct database update (bypasses hooks)
doc.db_set("customer_name", "Updated Name")

# Bulk update
frappe.db.set_value("Customer", "CUST-001", {
    "customer_name": "New Name",
    "territory": "Asia"
})
```

**Submitting and Cancelling** *(From test examples)*

```python
# Submit a document
doc = frappe.get_doc("Sales Order", "SO-001")
doc.submit()  # Sets docstatus=1, runs on_submit

# Cancel a submitted document
doc.cancel()  # Sets docstatus=2, runs on_cancel

# Amend cancelled document (creates new with -1 suffix)
amended = frappe.copy_doc(doc)
amended.amended_from = doc.name
amended.insert()
```

### Database API Examples

**Raw SQL Queries** *(From codebase analysis)*

```python
# Simple query
result = frappe.db.sql("""
    SELECT name, customer_name
    FROM tabCustomer
    WHERE territory = %s
""", ("United States",), as_dict=True)

# Query with named parameters
result = frappe.db.sql("""
    SELECT name, amount
    FROM `tabSales Invoice`
    WHERE customer = %(customer)s
    AND posting_date BETWEEN %(from_date)s AND %(to_date)s
""", {
    "customer": "CUST-001",
    "from_date": "2024-01-01",
    "to_date": "2024-12-31"
}, as_dict=True)

# Check if exists
exists = frappe.db.exists("Customer", "CUST-001")
exists = frappe.db.exists("Customer", {"email_id": "john@example.com"})
```

**Transaction Control** *(From codebase analysis)*

```python
try:
    frappe.db.begin()

    # Multiple operations
    doc1 = frappe.new_doc("Customer")
    doc1.customer_name = "Customer 1"
    doc1.insert()

    doc2 = frappe.new_doc("Customer")
    doc2.customer_name = "Customer 2"
    doc2.insert()

    frappe.db.commit()
except Exception:
    frappe.db.rollback()
    raise
```

### Authentication Examples

**Login Manager** *(From api_reference/auth.md)*

```python
from frappe.auth import LoginManager

# Standard login
login_manager = LoginManager()
login_manager.authenticate(user="john@example.com", pwd="password")
login_manager.post_login()

# Check if user is allowed (rate limiting)
from frappe.auth import get_login_attempt_tracker
tracker = get_login_attempt_tracker("john@example.com")
if not tracker.is_user_allowed():
    frappe.throw("Account locked due to too many failed attempts")

# API Key validation
from frappe.auth import validate_api_key_secret
validate_api_key_secret(api_key, api_secret)
```

### Assignment and Workflow

**Assigning Documents** *(From tutorials/assign/assign.md)*

```python
from frappe.desk.form.assign_to import add

# Assign document to user
add({
    'assign_to': ['test@example.com'],
    'doctype': 'Event',
    'name': 'EV-001',
    'description': 'Please review this event'
})

# Assign to multiple users
add({
    'assign_to': ['user1@example.com', 'user2@example.com'],
    'doctype': 'Task',
    'name': 'TASK-001',
    'description': 'Collaborative task'
})

# Check assigned users
doc = frappe.get_doc('Event', 'EV-001')
assigned_users = doc.get_assigned_users()
```

**Auto Repeat** *(From test_examples)*

```python
from frappe.automation.doctype.auto_repeat.auto_repeat import (
    make_auto_repeat,
    get_auto_repeat_entries,
    create_repeated_entries
)

# Create daily recurring ToDo
todo = frappe.get_doc(doctype='ToDo',
    description='Daily standup',
    assigned_by='Administrator'
).insert()

auto_repeat = make_auto_repeat(
    reference_doctype='ToDo',
    reference_document=todo.name,
    frequency='Daily',
    start_date=today()
)

# Weekly with specific days
auto_repeat = make_auto_repeat(
    reference_doctype='ToDo',
    frequency='Weekly',
    reference_document=todo.name,
    start_date=add_days(today(), -7),
    days=[{'day': 'Monday'}, {'day': 'Wednesday'}]
)

# Process auto repeat entries
data = get_auto_repeat_entries(getdate(today()))
create_repeated_entries(data)
frappe.db.commit()
```

### REST API Examples

**Whitelist Decorator** *(From codebase analysis)*

```python
@frappe.whitelist()
def get_customer_details(customer):
    """Public API endpoint"""
    return frappe.get_doc("Customer", customer)

@frappe.whitelist(allow_guest=True)
def public_endpoint():
    """Accessible without login"""
    return {"status": "ok"}

@frappe.whitelist(methods=["POST"])
def create_order(customer, items):
    """POST-only endpoint"""
    order = frappe.new_doc("Sales Order")
    order.customer = customer
    for item in items:
        order.append("items", item)
    order.insert()
    return order
```

**Client-side API Call**

```javascript
frappe.call({
    method: 'myapp.api.get_customer_details',
    args: {
        customer: 'CUST-001'
    },
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Rate Limiting

**Rate Limiter Usage** *(From test_examples)*

```python
from frappe.rate_limiter import RateLimiter

# Configure rate limit
limiter = RateLimiter(limit=100, window=86400)  # 100 requests per day
limiter.update()

# In site_config.json
# "rate_limit": {"window": 86400, "limit": 1000}

# Check rate limit status
headers = frappe.local.rate_limiter.headers()
# Returns: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
```

---

## Working with This Skill

### For Beginners

1. Start with **Document CRUD operations** - understand `frappe.get_doc()`, `insert()`, `save()`
2. Learn the **lifecycle hooks** - `validate`, `on_update`, `on_submit`
3. Practice **database queries** with `frappe.db.get_value()` and `frappe.db.get_list()`

### For Intermediate Users

1. Master **child table operations** with `append()` and `get_all_children()`
2. Understand **permission checking** with `has_permission()` and permission levels
3. Implement **custom workflows** using the Workflow DocType

### For Advanced Users

1. Deep dive into **authentication internals** - `LoginManager`, `LoginAttemptTracker`
2. Optimize with **lazy loading** using `get_lazy_doc()`
3. Implement **custom automation** with Assignment Rules and Auto Repeat
4. Use **background jobs** with `doc.queue_action()`

### Navigation Tips

| Need | Reference Location |
|------|-------------------|
| Document API | `references/api_reference/document.md` |
| Database API | `references/api_reference/database.md` |
| Authentication | `references/api_reference/auth.md` |
| Workflow | `references/documentation/workflows/` |
| Test Examples | `references/test_examples/test_examples.md` |
| Tutorials | `tutorials/` (369 step-by-step guides) |

---

## Available References

### API Reference (`references/api_reference/`)

Complete API documentation for 1,100+ files:

| Category | Files | Key APIs |
|----------|-------|----------|
| **Core** | document.py, base_document.py | Document, BaseDocument |
| **Database** | database.py | SQLiteDatabase, Database |
| **Authentication** | auth.py | LoginManager, HTTPRequest, CookieManager |
| **Automation** | auto_repeat.py, assignment_rule.py | AutoRepeat, AssignmentRule |
| **Web** | app.py, api.py | application(), whitelist() |
| **UI** | form.js, desk.js | FormBuilder, DeskPage |

### Tutorials (`tutorials/`)

369 step-by-step tutorials extracted from test files:

- `assign/` - Document assignment workflow
- `auto-email/` - Auto Email Report configuration
- `auto-repeat-*` - Recurring document patterns
- `workflow/` - State machine implementation
- `permission/` - Access control patterns

### Design Patterns (`references/patterns/`)

Detected patterns with code locations:

- Factory Pattern - Document/Controller creation
- Strategy Pattern - Report format handlers
- Observer Pattern - Hook system implementation

### Test Examples (`references/test_examples/`)

1,478 high-quality examples by category:

| Category | Count | Description |
|----------|-------|-------------|
| workflow | 592 | End-to-end business flows |
| method_call | 633 | API usage patterns |
| instantiation | 239 | Object creation patterns |
| config | 14 | Configuration examples |

### Architecture (`references/architecture/`)

- MVC implementation details
- Layered architecture analysis
- Module dependency graph

### Documentation (`references/documentation/`)

101 markdown files from the project:

- **workflows/** - Workflow State, Workflow Action, Workflow Transition
- **architecture/** - SQLite Search Framework
- **other/** - Release notes (v10-v13+), changelog

---

## Source Confidence

| Source Type | Confidence | Description |
|-------------|------------|-------------|
| **API Reference** | High | Extracted directly from source code |
| **Test Examples** | High | Real usage from test suite |
| **Design Patterns** | Medium-High | Detected with confidence > 0.7 |
| **Architecture** | Medium-High | Inferred from code structure |
| **Documentation** | Medium | From project markdown files |

---

## Common Patterns & Best Practices

### 1. Always Use Context Managers for Transactions

```python
import frappe

with frappe.db.transaction():
    doc1.insert()
    doc2.insert()
    # Auto-commits or rolls back
```

### 2. Prefer `db_set` for Simple Updates

```python
# Instead of:
doc = frappe.get_doc("Customer", "CUST-001")
doc.status = "Active"
doc.save()  # Triggers all hooks

# Use for simple updates:
doc.db_set("status", "Active")  # Direct DB update
```

### 3. Use `get_cached_doc` for Frequently Accessed Documents

```python
# For settings, configurations
settings = frappe.get_cached_doc("Selling Settings")

# For master data
customer = frappe.get_cached_doc("Customer", customer_name)
```

### 4. Handle Permissions Explicitly

```python
@frappe.whitelist()
def sensitive_operation(docname):
    doc = frappe.get_doc("Sensitive DocType", docname)
    if not doc.has_permission("write"):
        frappe.throw("No permission to modify this document")
    # Proceed with operation
```

### 5. Use Flags to Control Hook Execution

```python
doc = frappe.get_doc("Sales Order", "SO-001")
doc.flags.ignore_permissions = True
doc.flags.ignore_validate = True
doc.save()
```

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis
**Analysis Date:** 2026-02-04
**Frappe Version:** v16 (development branch)
