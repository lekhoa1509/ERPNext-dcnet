# How To: Milestone

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test milestone

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.cache_manager`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call frappe.db.delete()

```python
frappe.db.delete('Milestone Tracker')
```

### Step 2: Call frappe.cache_manager.clear_doctype_map()

```python
frappe.cache_manager.clear_doctype_map('Milestone Tracker')
```

### Step 3: Assign milestone_tracker = frappe.get_doc.insert(...)

```python
milestone_tracker = frappe.get_doc(doctype='Milestone Tracker', document_type='ToDo', track_field='status').insert()
```

### Step 4: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', description='test milestone', status='Open').insert()
```

### Step 5: Assign milestones = frappe.get_all(...)

```python
milestones = frappe.get_all('Milestone', fields=['track_field', 'value', 'milestone_tracker'], filters=dict(reference_type=todo.doctype, reference_name=todo.name))
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(milestones), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(milestones[0].track_field, 'status')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(milestones[0].value, 'Open')
```

### Step 9: Assign todo.status = 'Closed'

```python
todo.status = 'Closed'
```

### Step 10: Call todo.save()

```python
todo.save()
```

### Step 11: Assign milestones = frappe.get_all(...)

```python
milestones = frappe.get_all('Milestone', fields=['track_field', 'value', 'milestone_tracker'], filters=dict(reference_type=todo.doctype, reference_name=todo.name), order_by='creation desc')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(milestones), 2)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(milestones[0].track_field, 'status')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(milestones[0].value, 'Closed')
```

### Step 15: Call frappe.db.delete()

```python
frappe.db.delete('Milestone')
```

### Step 16: Call milestone_tracker.delete()

```python
milestone_tracker.delete()
```


## Complete Example

```python
# Workflow
frappe.db.delete('Milestone Tracker')
frappe.cache_manager.clear_doctype_map('Milestone Tracker')
milestone_tracker = frappe.get_doc(doctype='Milestone Tracker', document_type='ToDo', track_field='status').insert()
todo = frappe.get_doc(doctype='ToDo', description='test milestone', status='Open').insert()
milestones = frappe.get_all('Milestone', fields=['track_field', 'value', 'milestone_tracker'], filters=dict(reference_type=todo.doctype, reference_name=todo.name))
self.assertEqual(len(milestones), 1)
self.assertEqual(milestones[0].track_field, 'status')
self.assertEqual(milestones[0].value, 'Open')
todo.status = 'Closed'
todo.save()
milestones = frappe.get_all('Milestone', fields=['track_field', 'value', 'milestone_tracker'], filters=dict(reference_type=todo.doctype, reference_name=todo.name), order_by='creation desc')
self.assertEqual(len(milestones), 2)
self.assertEqual(milestones[0].track_field, 'status')
self.assertEqual(milestones[0].value, 'Closed')
frappe.db.delete('Milestone')
milestone_tracker.delete()
```

## Next Steps


---

*Source: test_milestone_tracker.py:9 | Complexity: Advanced | Last updated: 2026-02-04*