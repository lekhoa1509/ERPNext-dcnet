# How To: Http Valid Method Access

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test http valid method access

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.client`
- `frappe.desk.doctype.note.note`
- `frappe.client`
- `frappe.handler`
- `frappe.handler`
- `frappe.handler`
- `requests`
- `frappe.auth`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`


## Step-by-Step Guide

### Step 1: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 2: Assign frappe.local.request = frappe._dict(...)

```python
frappe.local.request = frappe._dict()
```

### Step 3: Assign frappe.local.request.method = 'POST'

```python
frappe.local.request.method = 'POST'
```

### Step 4: Assign frappe.local.form_dict = frappe._dict(...)

```python
frappe.local.form_dict = frappe._dict({'doc': dict(doctype='ToDo', description='Valid http method'), 'cmd': 'frappe.client.save'})
```

### Step 5: Assign todo = execute_cmd(...)

```python
todo = execute_cmd('frappe.client.save')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(todo.get('description'), 'Valid http method')
```

### Step 7: Call delete()

```python
delete('ToDo', todo.name)
```


## Complete Example

```python
# Workflow
from frappe.client import delete
from frappe.handler import execute_cmd
frappe.set_user('Administrator')
frappe.local.request = frappe._dict()
frappe.local.request.method = 'POST'
frappe.local.form_dict = frappe._dict({'doc': dict(doctype='ToDo', description='Valid http method'), 'cmd': 'frappe.client.save'})
todo = execute_cmd('frappe.client.save')
self.assertEqual(todo.get('description'), 'Valid http method')
delete('ToDo', todo.name)
```

## Next Steps


---

*Source: test_client.py:42 | Complexity: Intermediate | Last updated: 2026-02-04*