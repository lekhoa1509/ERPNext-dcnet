# How To: Default User Permission Validation

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test default user permission validation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user_permission.user_permission`
- `frappe.permissions`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.session_default_settings.session_default_settings`


## Step-by-Step Guide

### Step 1: Assign user = create_user(...)

```python
user = create_user('test_default_permission@example.com')
```

### Step 2: Assign param = get_params(...)

```python
param = get_params(user, 'User', user.name, is_default=1)
```

### Step 3: Call add_user_permissions()

```python
add_user_permissions(param)
```

### Step 4: Assign perm_user = create_user(...)

```python
perm_user = create_user('test_user_perm@example.com')
```

### Step 5: Assign param = get_params(...)

```python
param = get_params(user, 'User', perm_user.name, is_default=1)
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, add_user_permissions, param)
```


## Complete Example

```python
# Workflow
user = create_user('test_default_permission@example.com')
param = get_params(user, 'User', user.name, is_default=1)
add_user_permissions(param)
perm_user = create_user('test_user_perm@example.com')
param = get_params(user, 'User', perm_user.name, is_default=1)
self.assertRaises(frappe.ValidationError, add_user_permissions, param)
```

## Next Steps


---

*Source: test_user_permission.py:28 | Complexity: Intermediate | Last updated: 2026-02-04*