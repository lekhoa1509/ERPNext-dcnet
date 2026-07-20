# How To: Set Standard Fields Manually

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test set standard fields manually

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.defaults`
- `frappe.model.meta`
- `frappe.permissions`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user_permission.user_permission`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.desk.form.load`
- `frappe.installer`
- `frappe.permissions`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.tests.utils`
- `frappe.utils.data`
- `datetime`

**Setup Required:**
```python
frappe.clear_cache(doctype='Test Blog Post')
reset('Test Blogger')
reset('Test Blog Post')
frappe.db.delete('User Permission')
frappe.set_user('test1@example.com')
```

## Step-by-Step Guide

### Step 1: Assign fake_creation = value

```python
fake_creation = now_datetime() + timedelta(days=-7)
```

### Step 2: Assign fake_owner = frappe.db.get_value(...)

```python
fake_owner = frappe.db.get_value('User', {'name': ('!=', frappe.session.user)})
```

### Step 3: Assign d = frappe.new_doc(...)

```python
d = frappe.new_doc('ToDo')
```

### Step 4: Assign d.description = 'ToDo created via test_set_standard_fields_manually'

```python
d.description = 'ToDo created via test_set_standard_fields_manually'
```

### Step 5: Assign d.creation = fake_creation

```python
d.creation = fake_creation
```

### Step 6: Assign d.owner = fake_owner

```python
d.owner = fake_owner
```

### Step 7: Call d.save()

```python
d.save()
```

### Step 8: Call self.assertNotEqual()

```python
self.assertNotEqual(d.creation, fake_creation)
```

### Step 9: Call self.assertNotEqual()

```python
self.assertNotEqual(d.owner, fake_owner)
```


## Complete Example

```python
# Setup
frappe.clear_cache(doctype='Test Blog Post')
reset('Test Blogger')
reset('Test Blog Post')
frappe.db.delete('User Permission')
frappe.set_user('test1@example.com')

# Workflow
from datetime import timedelta
fake_creation = now_datetime() + timedelta(days=-7)
fake_owner = frappe.db.get_value('User', {'name': ('!=', frappe.session.user)})
d = frappe.new_doc('ToDo')
d.description = 'ToDo created via test_set_standard_fields_manually'
d.creation = fake_creation
d.owner = fake_owner
d.save()
self.assertNotEqual(d.creation, fake_creation)
self.assertNotEqual(d.owner, fake_owner)
```

## Next Steps


---

*Source: test_permissions.py:242 | Complexity: Advanced | Last updated: 2026-02-04*