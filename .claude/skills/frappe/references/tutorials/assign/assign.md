# How To: Assign

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test assign

## Prerequisites

**Required Modules:**
- `json`
- `datetime`
- `frappe`
- `frappe.core.utils`
- `frappe.desk.doctype.event.event`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.desk.form.assign_to`


## Step-by-Step Guide

### Step 1: Assign ev = frappe.get_doc.insert(...)

```python
ev = frappe.get_doc(self.globalTestRecords['Event'][0]).insert()
```

### Step 2: Call add()

```python
add({'assign_to': ['test@example.com'], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
```

### Step 3: Assign ev = frappe.get_doc(...)

```python
ev = frappe.get_doc('Event', ev.name)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
```

### Step 5: Call add()

```python
add({'assign_to': [self.test_user], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
```

### Step 6: Assign ev = frappe.get_doc(...)

```python
ev = frappe.get_doc('Event', ev.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(set(json.loads(ev._assign)), {'test@example.com', self.test_user})
```

### Step 8: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc('ToDo', {'reference_type': ev.doctype, 'reference_name': ev.name, 'allocated_to': self.test_user})
```

### Step 9: Assign todo.status = 'Cancelled'

```python
todo.status = 'Cancelled'
```

### Step 10: Call todo.save()

```python
todo.save()
```

### Step 11: Assign ev = frappe.get_doc(...)

```python
ev = frappe.get_doc('Event', ev.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
```

### Step 13: Call ev.delete()

```python
ev.delete()
```


## Complete Example

```python
# Workflow
from frappe.desk.form.assign_to import add
ev = frappe.get_doc(self.globalTestRecords['Event'][0]).insert()
add({'assign_to': ['test@example.com'], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
add({'assign_to': [self.test_user], 'doctype': 'Event', 'name': ev.name, 'description': 'Test Assignment'})
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(set(json.loads(ev._assign)), {'test@example.com', self.test_user})
todo = frappe.get_doc('ToDo', {'reference_type': ev.doctype, 'reference_name': ev.name, 'allocated_to': self.test_user})
todo.status = 'Cancelled'
todo.save()
ev = frappe.get_doc('Event', ev.name)
self.assertEqual(ev._assign, json.dumps(['test@example.com']))
ev.delete()
```

## Next Steps


---

*Source: test_event.py:65 | Complexity: Advanced | Last updated: 2026-02-04*