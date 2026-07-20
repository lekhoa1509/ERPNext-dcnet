# How To: Get Permitted Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get permitted fields

## Prerequisites

**Required Modules:**
- `contextlib`
- `random`
- `frappe`
- `frappe.model`
- `frappe.model.utils`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign todo_all_fields = get_permitted_fields(...)

```python
todo_all_fields = get_permitted_fields('ToDo', user='Administrator')
```

### Step 2: Assign todo_all_columns = frappe.get_meta.get_valid_columns(...)

```python
todo_all_columns = frappe.get_meta('ToDo').get_valid_columns()
```

### Step 3: Call self.assertListEqual()

```python
self.assertListEqual(todo_all_fields, todo_all_columns)
```

### Step 4: Assign guest_permitted_fields = get_permitted_fields(...)

```python
guest_permitted_fields = get_permitted_fields('ToDo')
```

### Step 5: Call self.assertNotIn()

```python
self.assertNotIn('description', guest_permitted_fields)
```

### Step 6: Assign picked_doctype = choice(...)

```python
picked_doctype = choice(core_doctypes_list)
```

### Step 7: Assign core_permitted_fields = get_permitted_fields(...)

```python
core_permitted_fields = get_permitted_fields(picked_doctype)
```

### Step 8: Assign picked_doctype_all_columns = frappe.get_meta.get_valid_columns(...)

```python
picked_doctype_all_columns = frappe.get_meta(picked_doctype).get_valid_columns()
```

### Step 9: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(core_permitted_fields, picked_doctype_all_columns)
```

### Step 10: Assign without_parent_fields = get_permitted_fields(...)

```python
without_parent_fields = get_permitted_fields('Installed Application')
```

### Step 11: Assign with_parent_fields = get_permitted_fields(...)

```python
with_parent_fields = get_permitted_fields('Installed Application', parenttype='Installed Applications')
```

### Step 12: Assign child_all_fields = frappe.get_meta.get_valid_columns(...)

```python
child_all_fields = frappe.get_meta('Installed Application').get_valid_columns()
```

### Step 13: Call self.assertLess()

```python
self.assertLess(len(without_parent_fields), len(with_parent_fields))
```

### Step 14: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(set(with_parent_fields), set(child_all_fields))
```

### Step 15: Call self.assertNotIn()

```python
self.assertNotIn('app_name', get_permitted_fields('Installed Application'))
```

### Step 16: Call self.assertNotIn()

```python
self.assertNotIn('app_name', get_permitted_fields('Installed Application', parenttype='Installed Applications'))
```


## Complete Example

```python
# Workflow
todo_all_fields = get_permitted_fields('ToDo', user='Administrator')
todo_all_columns = frappe.get_meta('ToDo').get_valid_columns()
self.assertListEqual(todo_all_fields, todo_all_columns)
with set_user('Guest'):
    guest_permitted_fields = get_permitted_fields('ToDo')
    self.assertNotIn('description', guest_permitted_fields)
with set_user('Guest'):
    picked_doctype = choice(core_doctypes_list)
    core_permitted_fields = get_permitted_fields(picked_doctype)
    picked_doctype_all_columns = frappe.get_meta(picked_doctype).get_valid_columns()
    self.assertSequenceEqual(core_permitted_fields, picked_doctype_all_columns)
with set_user('Administrator'):
    without_parent_fields = get_permitted_fields('Installed Application')
    with_parent_fields = get_permitted_fields('Installed Application', parenttype='Installed Applications')
    child_all_fields = frappe.get_meta('Installed Application').get_valid_columns()
    self.assertLess(len(without_parent_fields), len(with_parent_fields))
    self.assertSequenceEqual(set(with_parent_fields), set(child_all_fields))
with set_user('Guest'):
    self.assertNotIn('app_name', get_permitted_fields('Installed Application'))
    self.assertNotIn('app_name', get_permitted_fields('Installed Application', parenttype='Installed Applications'))
```

## Next Steps


---

*Source: test_model_utils.py:31 | Complexity: Advanced | Last updated: 2026-02-04*