# How To: Add Select Perm Doctypes

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add select perm doctypes

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.installer`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign user_type = create_user_type(...)

```python
user_type = create_user_type('Test User Type')
```

### Step 2: Assign doc = frappe.get_meta(...)

```python
doc = frappe.get_meta('Contact')
```

### Step 3: Assign link_fields = doc.get_link_fields(...)

```python
link_fields = doc.get_link_fields()
```

### Step 4: Assign select_doctypes = frappe.get_all(...)

```python
select_doctypes = frappe.get_all('User Select Document Type', {'parent': user_type.name}, pluck='document_type')
```

### Step 5: Assign link_fields = value

```python
link_fields = []
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(entry.options in select_doctypes)
```

### Step 7: Assign child_doc = frappe.get_meta(...)

```python
child_doc = frappe.get_meta(child_table.options)
```

### Step 8: Call link_fields.extend()

```python
link_fields.extend(child_doc.get_link_fields())
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(entry.options in select_doctypes)
```


## Complete Example

```python
# Workflow
user_type = create_user_type('Test User Type')
doc = frappe.get_meta('Contact')
link_fields = doc.get_link_fields()
select_doctypes = frappe.get_all('User Select Document Type', {'parent': user_type.name}, pluck='document_type')
for entry in link_fields:
    self.assertTrue(entry.options in select_doctypes)
link_fields = []
for child_table in doc.get_table_fields():
    child_doc = frappe.get_meta(child_table.options)
    link_fields.extend(child_doc.get_link_fields())
for entry in link_fields:
    self.assertTrue(entry.options in select_doctypes)
```

## Next Steps


---

*Source: test_user_type.py:12 | Complexity: Advanced | Last updated: 2026-02-04*