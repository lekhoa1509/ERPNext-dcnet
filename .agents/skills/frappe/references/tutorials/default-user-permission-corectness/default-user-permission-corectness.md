# How To: Default User Permission Corectness

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test default user permission corectness

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
user = create_user('test_default_corectness_permission_1@example.com')
```

### Step 2: Assign param = get_params(...)

```python
param = get_params(user, 'User', user.name, is_default=1, hide_descendants=1)
```

### Step 3: Call add_user_permissions()

```python
add_user_permissions(param)
```

### Step 4: Assign perm_user = create_user(...)

```python
perm_user = create_user('test_default_corectness2@example.com')
```

### Step 5: Assign test_blog = frappe.get_doc(...)

```python
test_blog = frappe.get_doc('Test Blog Post', '_Test Blog Post 1')
```

### Step 6: Assign param = get_params(...)

```python
param = get_params(perm_user, 'Test Blog Post', test_blog.name, is_default=1, hide_descendants=1)
```

### Step 7: Call add_user_permissions()

```python
add_user_permissions(param)
```

### Step 8: Call frappe.db.delete()

```python
frappe.db.delete('User Permission', filters={'for_value': test_blog.name})
```

### Step 9: Call frappe.delete_doc()

```python
frappe.delete_doc('Test Blog Post', test_blog.name)
```


## Complete Example

```python
# Workflow
user = create_user('test_default_corectness_permission_1@example.com')
param = get_params(user, 'User', user.name, is_default=1, hide_descendants=1)
add_user_permissions(param)
perm_user = create_user('test_default_corectness2@example.com')
test_blog = frappe.get_doc('Test Blog Post', '_Test Blog Post 1')
param = get_params(perm_user, 'Test Blog Post', test_blog.name, is_default=1, hide_descendants=1)
add_user_permissions(param)
frappe.db.delete('User Permission', filters={'for_value': test_blog.name})
frappe.delete_doc('Test Blog Post', test_blog.name)
```

## Next Steps


---

*Source: test_user_permission.py:37 | Complexity: Advanced | Last updated: 2026-02-04*