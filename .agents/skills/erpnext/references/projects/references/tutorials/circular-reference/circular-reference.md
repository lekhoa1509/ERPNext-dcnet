# How To: Circular Reference

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test circular reference

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

### Step 1: Assign task1 = create_task(...)

```python
task1 = create_task('_Test Task 1', add_days(nowdate(), -15), add_days(nowdate(), -10))
```

### Step 2: Assign task2 = create_task(...)

```python
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
```

### Step 3: Assign task3 = create_task(...)

```python
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
```

### Step 4: Call task1.reload()

```python
task1.reload()
```

### Step 5: Call task1.append()

```python
task1.append('depends_on', {'task': task3.name})
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(CircularReferenceError, task1.save)
```

### Step 7: Call task1.set()

```python
task1.set('depends_on', [])
```

### Step 8: Call task1.save()

```python
task1.save()
```

### Step 9: Assign task4 = create_task(...)

```python
task4 = create_task('_Test Task 4', nowdate(), add_days(nowdate(), 15), task1.name)
```

### Step 10: Call task3.append()

```python
task3.append('depends_on', {'task': task4.name})
```


## Complete Example

```python
# Workflow
task1 = create_task('_Test Task 1', add_days(nowdate(), -15), add_days(nowdate(), -10))
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
task1.reload()
task1.append('depends_on', {'task': task3.name})
self.assertRaises(CircularReferenceError, task1.save)
task1.set('depends_on', [])
task1.save()
task4 = create_task('_Test Task 4', nowdate(), add_days(nowdate(), 15), task1.name)
task3.append('depends_on', {'task': task4.name})
```

## Next Steps


---

*Source: test_task.py:43 | Complexity: Advanced | Last updated: 2026-02-04*