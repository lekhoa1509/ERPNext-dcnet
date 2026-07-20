# How To: Clear User Permissions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test clear user permissions

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

### Step 1: Assign current_user = value

```python
current_user = frappe.session.user
```

### Step 2: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 3: Call clear_user_permissions_for_doctype()

```python
clear_user_permissions_for_doctype('Test Blog Category', 'test2@example.com')
```

### Step 4: Call clear_user_permissions_for_doctype()

```python
clear_user_permissions_for_doctype('Test Blog Post', 'test2@example.com')
```

### Step 5: Call add_user_permission()

```python
add_user_permission('Test Blog Post', '_Test Blog Post 1', 'test2@example.com')
```

### Step 6: Call add_user_permission()

```python
add_user_permission('Test Blog Post', '_Test Blog Post 2', 'test2@example.com')
```

### Step 7: Call add_user_permission()

```python
add_user_permission('Test Blog Category', '_Test Blog Category 1', 'test2@example.com')
```

### Step 8: Assign deleted_user_permission_count = clear_user_permissions(...)

```python
deleted_user_permission_count = clear_user_permissions('test2@example.com', 'Test Blog Post')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(deleted_user_permission_count, 2)
```

### Step 10: Assign blog_post_user_permission_count = frappe.db.count(...)

```python
blog_post_user_permission_count = frappe.db.count('User Permission', filters={'user': 'test2@example.com', 'allow': 'Test Blog Post'})
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(blog_post_user_permission_count, 0)
```

### Step 12: Assign blog_category_user_permission_count = frappe.db.count(...)

```python
blog_category_user_permission_count = frappe.db.count('User Permission', filters={'user': 'test2@example.com', 'allow': 'Test Blog Category'})
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(blog_category_user_permission_count, 1)
```

### Step 14: Call frappe.set_user()

```python
frappe.set_user(current_user)
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
current_user = frappe.session.user
frappe.set_user('Administrator')
clear_user_permissions_for_doctype('Test Blog Category', 'test2@example.com')
clear_user_permissions_for_doctype('Test Blog Post', 'test2@example.com')
add_user_permission('Test Blog Post', '_Test Blog Post 1', 'test2@example.com')
add_user_permission('Test Blog Post', '_Test Blog Post 2', 'test2@example.com')
add_user_permission('Test Blog Category', '_Test Blog Category 1', 'test2@example.com')
deleted_user_permission_count = clear_user_permissions('test2@example.com', 'Test Blog Post')
self.assertEqual(deleted_user_permission_count, 2)
blog_post_user_permission_count = frappe.db.count('User Permission', filters={'user': 'test2@example.com', 'allow': 'Test Blog Post'})
self.assertEqual(blog_post_user_permission_count, 0)
blog_category_user_permission_count = frappe.db.count('User Permission', filters={'user': 'test2@example.com', 'allow': 'Test Blog Category'})
self.assertEqual(blog_category_user_permission_count, 1)
frappe.set_user(current_user)
```

## Next Steps


---

*Source: test_permissions.py:639 | Complexity: Advanced | Last updated: 2026-02-04*