# How To: Close Assignment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test close assignment

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.projects.doctype.task.task`
- `erpnext.tests.utils`
- `erpnext.projects.doctype.project.test_project`
- `erpnext.projects.doctype.timesheet.test_timesheet`
- `erpnext.setup.doctype.employee.test_employee`
- `erpnext.projects.doctype.task.task`
- `frappe.desk.form`


## Step-by-Step Guide

### Step 1: Call assign()

```python
assign()
```

### Step 2: Assign todo = get_owner_and_status(...)

```python
todo = get_owner_and_status()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(todo.allocated_to, 'test@example.com')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(todo.status, 'Open')
```

### Step 5: Call task.load_from_db()

```python
task.load_from_db()
```

### Step 6: Assign task.status = 'Completed'

```python
task.status = 'Completed'
```

### Step 7: Call task.save()

```python
task.save()
```

### Step 8: Assign todo = get_owner_and_status(...)

```python
todo = get_owner_and_status()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(todo.allocated_to, 'test@example.com')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(todo.status, 'Closed')
```

### Step 11: Assign task = frappe.new_doc(...)

```python
task = frappe.new_doc('Task')
```

### Step 12: Assign task.subject = 'Test Close Assignment'

```python
task.subject = 'Test Close Assignment'
```

### Step 13: Call task.insert()

```python
task.insert()
```

### Step 14: Call assign_to.add()

```python
assign_to.add({'assign_to': ['test@example.com'], 'doctype': task.doctype, 'name': task.name, 'description': 'Close this task'})
```


## Complete Example

```python
# Workflow
if not frappe.db.exists('Task', 'Test Close Assignment'):
    task = frappe.new_doc('Task')
    task.subject = 'Test Close Assignment'
    task.insert()

def assign():
    from frappe.desk.form import assign_to
    assign_to.add({'assign_to': ['test@example.com'], 'doctype': task.doctype, 'name': task.name, 'description': 'Close this task'})

def get_owner_and_status():
    return frappe.db.get_value('ToDo', filters={'reference_type': task.doctype, 'reference_name': task.name, 'description': 'Close this task'}, fieldname=('allocated_to', 'status'), as_dict=True)
assign()
todo = get_owner_and_status()
self.assertEqual(todo.allocated_to, 'test@example.com')
self.assertEqual(todo.status, 'Open')
task.load_from_db()
task.status = 'Completed'
task.save()
todo = get_owner_and_status()
self.assertEqual(todo.allocated_to, 'test@example.com')
self.assertEqual(todo.status, 'Closed')
```

## Next Steps


---

*Source: test_task.py:94 | Complexity: Advanced | Last updated: 2026-02-04*