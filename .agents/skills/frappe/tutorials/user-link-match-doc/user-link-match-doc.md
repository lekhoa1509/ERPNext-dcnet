# How To: User Link Match Doc

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test user link match doc

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign blogger = frappe.get_doc(...)

```python
blogger = frappe.get_doc('Test Blogger', '_Test Blogger 1')
```

### Step 2: Assign blogger.user = 'test2@example.com'

```python
blogger.user = 'test2@example.com'
```

### Step 3: Call blogger.save()

```python
blogger.save()
```

### Step 4: Call frappe.permissions.add_user_permission()

```python
frappe.permissions.add_user_permission('Test Blogger', blogger.name, blogger.user)
```

### Step 5: Call frappe.set_user()

```python
frappe.set_user('test2@example.com')
```

### Step 6: Assign post = frappe.get_doc(...)

```python
post = frappe.get_doc('Test Blog Post', '_Test Blog Post 2')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(post.has_permission('read'))
```

### Step 8: Assign post1 = frappe.get_doc(...)

```python
post1 = frappe.get_doc('Test Blog Post', '_Test Blog Post 1')
```

### Step 9: Call self.assertFalse()

```python
self.assertFalse(post1.has_permission('read'))
```


## Complete Example

```python
# Workflow
blogger = frappe.get_doc('Test Blogger', '_Test Blogger 1')
blogger.user = 'test2@example.com'
blogger.save()
frappe.permissions.add_user_permission('Test Blogger', blogger.name, blogger.user)
frappe.set_user('test2@example.com')
post = frappe.get_doc('Test Blog Post', '_Test Blog Post 2')
self.assertTrue(post.has_permission('read'))
post1 = frappe.get_doc('Test Blog Post', '_Test Blog Post 1')
self.assertFalse(post1.has_permission('read'))
```

## Next Steps


---

*Source: test_permissions.py:159 | Complexity: Advanced | Last updated: 2026-02-04*