# How To: Delayed Tasks Summary

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test delayed tasks summary

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.projects.doctype.task.test_task`
- `erpnext.projects.report.delayed_tasks_summary.delayed_tasks_summary`


## Step-by-Step Guide

### Step 1: Assign filters = frappe._dict(...)

```python
filters = frappe._dict({'from_date': add_months(nowdate(), -1), 'to_date': nowdate(), 'priority': 'Low', 'status': 'Open'})
```

### Step 2: Assign expected_data = value

```python
expected_data = [{'subject': '_Test Task 99', 'status': 'Open', 'priority': 'Low', 'delay': 1}, {'subject': '_Test Task 98', 'status': 'Completed', 'priority': 'Low', 'delay': -1}]
```

### Step 3: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 4: Assign data = next(...)

```python
data = next(filter(lambda x: x.subject == '_Test Task 99', report[1]))
```

### Step 5: Assign filters.status = 'Completed'

```python
filters.status = 'Completed'
```

### Step 6: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 7: Assign data = next(...)

```python
data = next(filter(lambda x: x.subject == '_Test Task 98', report[1]))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(expected_data[0].get(key), data.get(key))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(expected_data[1].get(key), data.get(key))
```


## Complete Example

```python
# Workflow
filters = frappe._dict({'from_date': add_months(nowdate(), -1), 'to_date': nowdate(), 'priority': 'Low', 'status': 'Open'})
expected_data = [{'subject': '_Test Task 99', 'status': 'Open', 'priority': 'Low', 'delay': 1}, {'subject': '_Test Task 98', 'status': 'Completed', 'priority': 'Low', 'delay': -1}]
report = execute(filters)
data = next(filter(lambda x: x.subject == '_Test Task 99', report[1]))
for key in ['subject', 'status', 'priority', 'delay']:
    self.assertEqual(expected_data[0].get(key), data.get(key))
filters.status = 'Completed'
report = execute(filters)
data = next(filter(lambda x: x.subject == '_Test Task 98', report[1]))
for key in ['subject', 'status', 'priority', 'delay']:
    self.assertEqual(expected_data[1].get(key), data.get(key))
```

## Next Steps


---

*Source: test_delayed_tasks_summary.py:19 | Complexity: Advanced | Last updated: 2026-02-04*