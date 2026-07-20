# How To: Fetch If Empty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fetch if empty

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.doctype`
- `frappe.model.db_query`
- `frappe.permissions`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call frappe.db.delete()

```python
frappe.db.delete('ToDo')
```

### Step 2: Assign todo_meta = frappe.get_meta(...)

```python
todo_meta = frappe.get_meta('ToDo')
```

### Step 3: Assign field = value

```python
field = todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0]
```

### Step 4: Assign field.fetch_from = 'assigned_by.full_name'

```python
field.fetch_from = 'assigned_by.full_name'
```

### Step 5: Assign field.fetch_if_empty = 1

```python
field.fetch_if_empty = 1
```

### Step 6: Call todo_meta.save()

```python
todo_meta.save()
```

### Step 7: Call frappe.clear_cache()

```python
frappe.clear_cache(doctype='ToDo')
```

### Step 8: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator', assigned_by_full_name='Admin').insert()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(todo.assigned_by_full_name, 'Admin')
```

### Step 10: Assign unknown.fetch_if_empty = 0

```python
todo.meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_if_empty = 0
```

### Step 11: Call todo.meta.save()

```python
todo.meta.save()
```

### Step 12: Call todo.reload()

```python
todo.reload()
```

### Step 13: Call todo.save()

```python
todo.save()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```


## Complete Example

```python
# Workflow
frappe.db.delete('ToDo')
todo_meta = frappe.get_meta('ToDo')
field = todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0]
field.fetch_from = 'assigned_by.full_name'
field.fetch_if_empty = 1
todo_meta.save()
frappe.clear_cache(doctype='ToDo')
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator', assigned_by_full_name='Admin').insert()
self.assertEqual(todo.assigned_by_full_name, 'Admin')
todo.meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_if_empty = 0
todo.meta.save()
todo.reload()
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

## Next Steps


---

*Source: test_todo.py:111 | Complexity: Advanced | Last updated: 2026-02-04*