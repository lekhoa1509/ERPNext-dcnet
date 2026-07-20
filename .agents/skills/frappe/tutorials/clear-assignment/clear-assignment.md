# How To: Clear Assignment

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test clear assignment

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.tests.utils`


## Step-by-Step Guide

### Step 1: Assign note = _make_test_record(...)

```python
note = _make_test_record(public=1)
```

### Step 2: Assign todo = value

```python
todo = frappe.get_list('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status='Open'), limit=1)[0]
```

### Step 3: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc('ToDo', todo['name'])
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(todo.allocated_to, 'test@example.com')
```

### Step 5: Assign note.public = 0

```python
note.public = 0
```

### Step 6: Call note.save()

```python
note.save()
```

### Step 7: Call todo.load_from_db()

```python
todo.load_from_db()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(todo.status, 'Cancelled')
```


## Complete Example

```python
# Workflow
note = _make_test_record(public=1)
todo = frappe.get_list('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status='Open'), limit=1)[0]
todo = frappe.get_doc('ToDo', todo['name'])
self.assertEqual(todo.allocated_to, 'test@example.com')
note.public = 0
note.save()
todo.load_from_db()
self.assertEqual(todo.status, 'Cancelled')
```

## Next Steps


---

*Source: test_assignment_rule.py:161 | Complexity: Advanced | Last updated: 2026-02-04*