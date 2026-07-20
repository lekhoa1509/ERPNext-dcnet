# How To: Approve Ptype On Blog Post

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that custom permission types are applied correctly.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.permissions`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'Test that custom permission types are applied correctly.'

```python
'Test that custom permission types are applied correctly.'
```

### Step 2: Assign user_role = 'Website Manager'

```python
user_role = 'Website Manager'
```

### Step 3: Assign doc_type = 'Web Page'

```python
doc_type = 'Web Page'
```

### Step 4: Assign ptype_name = 'approve'

```python
ptype_name = 'approve'
```

### Step 5: Assign user = self._create_test_user(...)

```python
user = self._create_test_user('test_approve_permission@example.com', user_role)
```

### Step 6: Assign ptype_doc = self._create_permission_type(...)

```python
ptype_doc = self._create_permission_type(ptype_name, doc_type)
```

### Step 7: Call self._verify_custom_fields_created()

```python
self._verify_custom_fields_created(ptype_doc, doc_type)
```

### Step 8: Call self._verify_user_lacks_permission()

```python
self._verify_user_lacks_permission(doc_type, ptype_name, user.name)
```

### Step 9: Call update_permission_property()

```python
update_permission_property(doctype=doc_type, role=user_role, permlevel=0, ptype=ptype_name, value=1)
```

### Step 10: Call self._verify_user_has_permission()

```python
self._verify_user_has_permission(doc_type, ptype_name, user.name)
```

### Step 11: Call update_permission_property()

```python
update_permission_property(doctype=doc_type, role=user_role, permlevel=0, ptype=ptype_name, value=0)
```

### Step 12: Call frappe.delete_doc()

```python
frappe.delete_doc('User', user.name, force=True)
```

### Step 13: Call frappe.delete_doc()

```python
frappe.delete_doc('Permission Type', ptype_doc.name, force=True)
```


## Complete Example

```python
# Workflow
'Test that custom permission types are applied correctly.'
user_role = 'Website Manager'
doc_type = 'Web Page'
ptype_name = 'approve'
user = self._create_test_user('test_approve_permission@example.com', user_role)
ptype_doc = self._create_permission_type(ptype_name, doc_type)
try:
    self._verify_custom_fields_created(ptype_doc, doc_type)
    self._verify_user_lacks_permission(doc_type, ptype_name, user.name)
    update_permission_property(doctype=doc_type, role=user_role, permlevel=0, ptype=ptype_name, value=1)
    self._verify_user_has_permission(doc_type, ptype_name, user.name)
    update_permission_property(doctype=doc_type, role=user_role, permlevel=0, ptype=ptype_name, value=0)
finally:
    frappe.delete_doc('User', user.name, force=True)
    frappe.delete_doc('Permission Type', ptype_doc.name, force=True)
```

## Next Steps


---

*Source: test_permission_type.py:21 | Complexity: Advanced | Last updated: 2026-02-04*