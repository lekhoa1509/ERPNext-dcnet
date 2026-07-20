# How To: Child Permissions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test child permissions

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

### Step 1: Call frappe.set_user()

```python
frappe.set_user('test3@example.com')
```

### Step 2: Call self.assertIsInstance()

```python
self.assertIsInstance(frappe.get_list('DefaultValue', parent_doctype='User', limit=1), list)
```

### Step 3: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, frappe.get_list, 'DefaultValue')
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, frappe.get_list, 'DefaultValue', parent_doctype='ToDo')
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, frappe.get_list, 'DefaultValue', parent_doctype='DefaultValue')
```

### Step 6: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', frappe.session.user)
```

### Step 7: Assign doc = user.append(...)

```python
doc = user.append('defaults')
```

### Step 8: Call doc.check_permission()

```python
doc.check_permission()
```

### Step 9: Assign doc = user.append(...)

```python
doc = user.append('roles')
```

### Step 10: Assign doc.parentfield = None

```python
doc.parentfield = None
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, doc.check_permission)
```

### Step 12: Assign doc = user.append(...)

```python
doc = user.append('roles')
```

### Step 13: Assign doc.parentfield = 'first_name'

```python
doc.parentfield = 'first_name'
```

### Step 14: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, doc.check_permission)
```

### Step 15: Assign doc = user.append(...)

```python
doc = user.append('roles')
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, doc.check_permission)
```

### Step 17: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', 'Administrator')
```

### Step 18: Assign doc = user.append(...)

```python
doc = user.append('defaults')
```

### Step 19: Call self.assertRaises()

```python
self.assertRaises(frappe.PermissionError, doc.check_permission)
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
frappe.set_user('test3@example.com')
self.assertIsInstance(frappe.get_list('DefaultValue', parent_doctype='User', limit=1), list)
self.assertRaises(frappe.PermissionError, frappe.get_list, 'DefaultValue')
self.assertRaises(frappe.PermissionError, frappe.get_list, 'DefaultValue', parent_doctype='ToDo')
self.assertRaises(frappe.PermissionError, frappe.get_list, 'DefaultValue', parent_doctype='DefaultValue')
user = frappe.get_doc('User', frappe.session.user)
doc = user.append('defaults')
doc.check_permission()
doc = user.append('roles')
doc.parentfield = None
self.assertRaises(frappe.PermissionError, doc.check_permission)
doc = user.append('roles')
doc.parentfield = 'first_name'
self.assertRaises(frappe.PermissionError, doc.check_permission)
doc = user.append('roles')
self.assertRaises(frappe.PermissionError, doc.check_permission)
user = frappe.get_doc('User', 'Administrator')
doc = user.append('defaults')
self.assertRaises(frappe.PermissionError, doc.check_permission)
```

## Next Steps


---

*Source: test_permissions.py:668 | Complexity: Advanced | Last updated: 2026-02-04*