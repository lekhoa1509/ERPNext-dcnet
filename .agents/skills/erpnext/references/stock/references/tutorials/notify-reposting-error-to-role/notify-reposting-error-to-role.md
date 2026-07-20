# How To: Notify Reposting Error To Role

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test notify reposting error to role

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`


## Step-by-Step Guide

### Step 1: Assign role = 'Notify Reposting Role'

```python
role = 'Notify Reposting Role'
```

### Step 2: Assign user = 'notify_reposting_error@test.com'

```python
user = 'notify_reposting_error@test.com'
```

### Step 3: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', '')
```

### Step 4: Assign users = get_recipients(...)

```python
users = get_recipients()
```

### Step 5: Call self.assertFalse()

```python
self.assertFalse(user in users)
```

### Step 6: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', role)
```

### Step 7: Assign users = get_recipients(...)

```python
users = get_recipients()
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(user in users)
```

### Step 9: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Role', 'role_name': role}).insert(ignore_permissions=True)
```

### Step 10: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'User', 'email': user, 'first_name': 'Test', 'language': 'en', 'time_zone': 'Asia/Kolkata', 'send_welcome_email': 0, 'roles': [{'role': role}]}).insert(ignore_permissions=True)
```


## Complete Example

```python
# Workflow
role = 'Notify Reposting Role'
if not frappe.db.exists('Role', role):
    frappe.get_doc({'doctype': 'Role', 'role_name': role}).insert(ignore_permissions=True)
user = 'notify_reposting_error@test.com'
if not frappe.db.exists('User', user):
    frappe.get_doc({'doctype': 'User', 'email': user, 'first_name': 'Test', 'language': 'en', 'time_zone': 'Asia/Kolkata', 'send_welcome_email': 0, 'roles': [{'role': role}]}).insert(ignore_permissions=True)
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', '')
users = get_recipients()
self.assertFalse(user in users)
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', role)
users = get_recipients()
self.assertTrue(user in users)
```

## Next Steps


---

*Source: test_stock_reposting_settings.py:11 | Complexity: Advanced | Last updated: 2026-02-04*