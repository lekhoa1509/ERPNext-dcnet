# How To: Fetch Setup

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fetch setup

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

### Step 3: Assign unknown.fetch_from = ''

```python
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = ''
```

### Step 4: Call todo_meta.save()

```python
todo_meta.save()
```

### Step 5: Call frappe.clear_cache()

```python
frappe.clear_cache(doctype='ToDo')
```

### Step 6: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator').insert()
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(todo.assigned_by_full_name)
```

### Step 8: Assign todo_meta = frappe.get_meta(...)

```python
todo_meta = frappe.get_meta('ToDo')
```

### Step 9: Assign unknown.fetch_from = 'assigned_by.full_name'

```python
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = 'assigned_by.full_name'
```

### Step 10: Call todo_meta.save()

```python
todo_meta.save()
```

### Step 11: Call todo.reload()

```python
todo.reload()
```

### Step 12: Call todo.save()

```python
todo.save()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```


## Complete Example

```python
# Workflow
frappe.db.delete('ToDo')
todo_meta = frappe.get_meta('ToDo')
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = ''
todo_meta.save()
frappe.clear_cache(doctype='ToDo')
todo = frappe.get_doc(doctype='ToDo', description='test todo', assigned_by='Administrator').insert()
self.assertFalse(todo.assigned_by_full_name)
todo_meta = frappe.get_meta('ToDo')
todo_meta.get('fields', dict(fieldname='assigned_by_full_name'))[0].fetch_from = 'assigned_by.full_name'
todo_meta.save()
todo.reload()
todo.save()
self.assertEqual(todo.assigned_by_full_name, frappe.db.get_value('User', todo.assigned_by, 'full_name'))
```

## Next Steps


---

*Source: test_todo.py:30 | Complexity: Advanced | Last updated: 2026-02-04*