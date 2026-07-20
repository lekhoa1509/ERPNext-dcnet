# How To: Set Only Once Child Table Rows

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test set only once child table rows

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

### Step 1: Assign doctype_meta = frappe.get_meta(...)

```python
doctype_meta = frappe.get_meta('DocType')
```

### Step 2: Assign doctype_meta.get_field.set_only_once = 1

```python
doctype_meta.get_field('fields').set_only_once = 1
```

### Step 3: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('DocType', 'Test Blog Post')
```

### Step 4: Assign doc.fields = value

```python
doc.fields = doc.fields[:-1]
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(frappe.CannotChangeConstantError, doc.save)
```

### Step 6: Call frappe.clear_cache()

```python
frappe.clear_cache(doctype='DocType')
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
doctype_meta = frappe.get_meta('DocType')
doctype_meta.get_field('fields').set_only_once = 1
doc = frappe.get_doc('DocType', 'Test Blog Post')
doc.fields = doc.fields[:-1]
self.assertRaises(frappe.CannotChangeConstantError, doc.save)
frappe.clear_cache(doctype='DocType')
```

## Next Steps


---

*Source: test_permissions.py:277 | Complexity: Intermediate | Last updated: 2026-02-04*