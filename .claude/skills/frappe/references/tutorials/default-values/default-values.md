# How To: Default Values

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test default values

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

### Step 1: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Test Blog Post')
```

### Step 2: Call self.assertFalse()

```python
self.assertFalse(doc.get('blog_category'))
```

### Step 3: Call add_user_permission()

```python
add_user_permission('Test Blog Category', '_Test Blog Category 1', 'test2@example.com')
```

### Step 4: Call frappe.set_user()

```python
frappe.set_user('test2@example.com')
```

### Step 5: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Test Blog Post')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(doc.get('blog_category'), '_Test Blog Category 1')
```

### Step 7: Call add_user_permission()

```python
add_user_permission('Test Blog Category', '_Test Blog Category', 'test2@example.com', ignore_permissions=True)
```

### Step 8: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 9: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Test Blog Post')
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(doc.get('blog_category'))
```

### Step 11: Call add_user_permission()

```python
add_user_permission('Test Blog Category', '_Test Blog Category 2', 'test2@example.com', ignore_permissions=True, is_default=1)
```

### Step 12: Call frappe.clear_cache()

```python
frappe.clear_cache()
```

### Step 13: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Test Blog Post')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(doc.get('blog_category'), '_Test Blog Category 2')
```


## Complete Example

```python
# Workflow
doc = frappe.new_doc('Test Blog Post')
self.assertFalse(doc.get('blog_category'))
add_user_permission('Test Blog Category', '_Test Blog Category 1', 'test2@example.com')
frappe.set_user('test2@example.com')
doc = frappe.new_doc('Test Blog Post')
self.assertEqual(doc.get('blog_category'), '_Test Blog Category 1')
add_user_permission('Test Blog Category', '_Test Blog Category', 'test2@example.com', ignore_permissions=True)
frappe.clear_cache()
doc = frappe.new_doc('Test Blog Post')
self.assertFalse(doc.get('blog_category'))
add_user_permission('Test Blog Category', '_Test Blog Category 2', 'test2@example.com', ignore_permissions=True, is_default=1)
frappe.clear_cache()
doc = frappe.new_doc('Test Blog Post')
self.assertEqual(doc.get('blog_category'), '_Test Blog Category 2')
```

## Next Steps


---

*Source: test_permissions.py:128 | Complexity: Advanced | Last updated: 2026-02-04*