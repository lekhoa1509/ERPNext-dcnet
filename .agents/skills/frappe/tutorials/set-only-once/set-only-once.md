# How To: Set Only Once

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test set only once

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

### Step 1: Assign blog_post = frappe.get_meta(...)

```python
blog_post = frappe.get_meta('Test Blog Post')
```

### Step 2: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Test Blog Post', '_Test Blog Post 1')
```

### Step 3: Call doc.db_set()

```python
doc.db_set('title', 'Old')
```

### Step 4: Assign blog_post.get_field.set_only_once = 1

```python
blog_post.get_field('title').set_only_once = 1
```

### Step 5: Assign doc.title = 'New'

```python
doc.title = 'New'
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.CannotChangeConstantError, doc.save)
```

### Step 7: Assign blog_post.get_field.set_only_once = 0

```python
blog_post.get_field('title').set_only_once = 0
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
blog_post = frappe.get_meta('Test Blog Post')
doc = frappe.get_doc('Test Blog Post', '_Test Blog Post 1')
doc.db_set('title', 'Old')
blog_post.get_field('title').set_only_once = 1
doc.title = 'New'
self.assertRaises(frappe.CannotChangeConstantError, doc.save)
blog_post.get_field('title').set_only_once = 0
```

## Next Steps


---

*Source: test_permissions.py:268 | Complexity: Intermediate | Last updated: 2026-02-04*