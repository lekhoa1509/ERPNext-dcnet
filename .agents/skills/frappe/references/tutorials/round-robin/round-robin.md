# How To: Round Robin

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test round robin

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.tests.utils`


## Step-by-Step Guide

### Step 1: Assign record = _make_test_record(...)

```python
record = _make_test_record(public=1)
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test@example.com')
```

### Step 3: Assign record = _make_test_record(...)

```python
record = _make_test_record(public=1)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test1@example.com')
```

### Step 5: Call clear_assignments()

```python
clear_assignments()
```

### Step 6: Assign record = _make_test_record(...)

```python
record = _make_test_record(public=1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test2@example.com')
```

### Step 8: Assign record = _make_test_record(...)

```python
record = _make_test_record(public=1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test@example.com')
```


## Complete Example

```python
# Workflow
record = _make_test_record(public=1)
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test@example.com')
record = _make_test_record(public=1)
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test1@example.com')
clear_assignments()
record = _make_test_record(public=1)
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test2@example.com')
record = _make_test_record(public=1)
self.assertEqual(frappe.db.get_value('ToDo', dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status='Open'), 'allocated_to'), 'test@example.com')
```

## Next Steps


---

*Source: test_assignment_rule.py:38 | Complexity: Advanced | Last updated: 2026-02-04*