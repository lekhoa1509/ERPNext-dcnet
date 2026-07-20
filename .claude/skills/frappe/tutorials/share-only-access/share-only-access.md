# How To: Share Only Access

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that shared docs grant access when user has no role permissions.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `itertools`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.classes.context_managers`
- `frappe.tests.test_db_query`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.nestedset`
- `frappe.permissions`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.share`
- `frappe.share`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.share`
- `frappe.permissions`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.permissions`
- `frappe.database.query`

**Setup Required:**
```python
setup_for_tests()
```

## Step-by-Step Guide

### Step 1: 'Test that shared docs grant access when user has no role permissions.'

```python
'Test that shared docs grant access when user has no role permissions.'
```

### Step 2: Assign test_user = 'test2@example.com'

```python
test_user = 'test2@example.com'
```

### Step 3: Assign event = frappe.get_doc.insert(...)

```python
event = frappe.get_doc(doctype='Event', subject='Share Only Test Event', starts_on='2025-01-01 10:00:00', event_type='Private').insert()
```

### Step 4: Call self.addCleanup()

```python
self.addCleanup(event.delete)
```

### Step 5: Call self.addCleanup()

```python
self.addCleanup(lambda: frappe.set_user('Administrator'))
```

### Step 6: Call frappe.set_user()

```python
frappe.set_user(test_user)
```

### Step 7: Assign result = frappe.qb.get_query.run(...)

```python
result = frappe.qb.get_query('Event', filters={'name': event.name}, ignore_permissions=False).run()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(result), 0, 'User should not see event without share')
```

### Step 9: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 10: Call frappe.share.add()

```python
frappe.share.add('Event', event.name, test_user)
```

### Step 11: Call frappe.set_user()

```python
frappe.set_user(test_user)
```

### Step 12: Assign result = frappe.qb.get_query.run(...)

```python
result = frappe.qb.get_query('Event', filters={'name': event.name}, ignore_permissions=False).run()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(result), 1, 'User should see event via share')
```


## Complete Example

```python
# Setup
setup_for_tests()

# Workflow
'Test that shared docs grant access when user has no role permissions.'
import frappe.share
test_user = 'test2@example.com'
event = frappe.get_doc(doctype='Event', subject='Share Only Test Event', starts_on='2025-01-01 10:00:00', event_type='Private').insert()
self.addCleanup(event.delete)
self.addCleanup(lambda: frappe.set_user('Administrator'))
frappe.set_user(test_user)
result = frappe.qb.get_query('Event', filters={'name': event.name}, ignore_permissions=False).run()
self.assertEqual(len(result), 0, 'User should not see event without share')
frappe.set_user('Administrator')
frappe.share.add('Event', event.name, test_user)
frappe.set_user(test_user)
result = frappe.qb.get_query('Event', filters={'name': event.name}, ignore_permissions=False).run()
self.assertEqual(len(result), 1, 'User should see event via share')
```

## Next Steps


---

*Source: test_query.py:1951 | Complexity: Advanced | Last updated: 2026-02-04*