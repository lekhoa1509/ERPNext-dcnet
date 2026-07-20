# How To: Operations On Locked Documents

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test operations on locked documents

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='testing operations').insert()
```

### Step 2: Call todo.lock()

```python
todo.lock()
```

### Step 3: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('ToDo', todo.name)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(doc.is_locked, True)
```

### Step 5: Call doc.unlock()

```python
doc.unlock()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(doc.is_locked, False)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(todo.is_locked, False)
```

### Step 8: Assign todo.description = 'Random'

```python
todo.description = 'Random'
```

### Step 9: Call todo.save()

```python
todo.save()
```

### Step 10: Assign doc.description = 'Random'

```python
doc.description = 'Random'
```

### Step 11: Call doc.save()

```python
doc.save()
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc(doctype='ToDo', description='testing operations').insert()
todo.lock()
with self.assertRaises(frappe.DocumentLockedError):
    todo.description = 'Random'
    todo.save()
doc = frappe.get_doc('ToDo', todo.name)
self.assertEqual(doc.is_locked, True)
with self.assertRaises(frappe.DocumentLockedError):
    doc.description = 'Random'
    doc.save()
doc.unlock()
self.assertEqual(doc.is_locked, False)
self.assertEqual(todo.is_locked, False)
```

## Next Steps


---

*Source: test_document_locks.py:21 | Complexity: Advanced | Last updated: 2026-02-04*