# How To: Assignment Count

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test assignment count

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.desk.form.assign_to`
- `frappe.automation.doctype.assignment_rule.test_assignment_rule`
- `frappe.desk.form.load`
- `frappe.desk.listview`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call frappe.db.delete()

```python
frappe.db.delete('ToDo')
```

### Step 2: Assign note = _make_test_record(...)

```python
note = _make_test_record()
```

### Step 3: Call assign()

```python
assign(note, 'test_assign1@example.com')
```

### Step 4: Assign note = _make_test_record(...)

```python
note = _make_test_record(public=1)
```

### Step 5: Call assign()

```python
assign(note, 'test_assign2@example.com')
```

### Step 6: Assign note = _make_test_record(...)

```python
note = _make_test_record(public=1)
```

### Step 7: Call assign()

```python
assign(note, 'test_assign2@example.com')
```

### Step 8: Assign note = _make_test_record(...)

```python
note = _make_test_record()
```

### Step 9: Call assign()

```python
assign(note, 'test_assign2@example.com')
```

### Step 10: Assign data = value

```python
data = {d.name: d.count for d in get_group_by_count(TEST_DOCTYPE, '[]', 'assigned_to')}
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue('test_assign1@example.com' in data)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(data['test_assign1@example.com'], 1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(data['test_assign2@example.com'], 3)
```

### Step 14: Assign data = value

```python
data = {d.name: d.count for d in get_group_by_count(TEST_DOCTYPE, '[{"public": 1}]', 'assigned_to')}
```

### Step 15: Call self.assertFalse()

```python
self.assertFalse('test_assign1@example.com' in data)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(data['test_assign2@example.com'], 2)
```

### Step 17: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 18: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'User', 'email': 'test_assign1@example.com', 'first_name': 'Test', 'roles': [{'role': 'System Manager'}]}).insert()
```

### Step 19: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'User', 'email': 'test_assign2@example.com', 'first_name': 'Test', 'roles': [{'role': 'System Manager'}]}).insert()
```


## Complete Example

```python
# Workflow
frappe.db.delete('ToDo')
if not frappe.db.exists('User', 'test_assign1@example.com'):
    frappe.get_doc({'doctype': 'User', 'email': 'test_assign1@example.com', 'first_name': 'Test', 'roles': [{'role': 'System Manager'}]}).insert()
if not frappe.db.exists('User', 'test_assign2@example.com'):
    frappe.get_doc({'doctype': 'User', 'email': 'test_assign2@example.com', 'first_name': 'Test', 'roles': [{'role': 'System Manager'}]}).insert()
note = _make_test_record()
assign(note, 'test_assign1@example.com')
note = _make_test_record(public=1)
assign(note, 'test_assign2@example.com')
note = _make_test_record(public=1)
assign(note, 'test_assign2@example.com')
note = _make_test_record()
assign(note, 'test_assign2@example.com')
data = {d.name: d.count for d in get_group_by_count(TEST_DOCTYPE, '[]', 'assigned_to')}
self.assertTrue('test_assign1@example.com' in data)
self.assertEqual(data['test_assign1@example.com'], 1)
self.assertEqual(data['test_assign2@example.com'], 3)
data = {d.name: d.count for d in get_group_by_count(TEST_DOCTYPE, '[{"public": 1}]', 'assigned_to')}
self.assertFalse('test_assign1@example.com' in data)
self.assertEqual(data['test_assign2@example.com'], 2)
frappe.db.rollback()
```

## Next Steps


---

*Source: test_assign.py:43 | Complexity: Advanced | Last updated: 2026-02-04*