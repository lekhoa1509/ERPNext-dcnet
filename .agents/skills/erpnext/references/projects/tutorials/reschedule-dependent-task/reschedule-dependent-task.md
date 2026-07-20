# How To: Reschedule Dependent Task

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reschedule dependent task

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

### Step 1: Assign project = frappe.get_value(...)

```python
project = frappe.get_value('Project', {'project_name': '_Test Project'})
```

### Step 2: Assign task1 = create_task(...)

```python
task1 = create_task('_Test Task 1', nowdate(), add_days(nowdate(), 10))
```

### Step 3: Assign task2 = create_task(...)

```python
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
```

### Step 4: Assign unknown.project = project

```python
task2.get('depends_on')[0].project = project
```

### Step 5: Call task2.save()

```python
task2.save()
```

### Step 6: Assign task3 = create_task(...)

```python
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
```

### Step 7: Assign unknown.project = project

```python
task3.get('depends_on')[0].project = project
```

### Step 8: Call task3.save()

```python
task3.save()
```

### Step 9: Call task1.update()

```python
task1.update({'exp_end_date': add_days(nowdate(), 20)})
```

### Step 10: Call task1.save()

```python
task1.save()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_start_date')), getdate(add_days(nowdate(), 21)))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_end_date')), getdate(add_days(nowdate(), 25)))
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_start_date')), getdate(add_days(nowdate(), 26)))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_end_date')), getdate(add_days(nowdate(), 30)))
```


## Complete Example

```python
# Workflow
project = frappe.get_value('Project', {'project_name': '_Test Project'})
task1 = create_task('_Test Task 1', nowdate(), add_days(nowdate(), 10))
task2 = create_task('_Test Task 2', add_days(nowdate(), 11), add_days(nowdate(), 15), task1.name)
task2.get('depends_on')[0].project = project
task2.save()
task3 = create_task('_Test Task 3', add_days(nowdate(), 11), add_days(nowdate(), 15), task2.name)
task3.get('depends_on')[0].project = project
task3.save()
task1.update({'exp_end_date': add_days(nowdate(), 20)})
task1.save()
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_start_date')), getdate(add_days(nowdate(), 21)))
self.assertEqual(getdate(frappe.db.get_value('Task', task2.name, 'exp_end_date')), getdate(add_days(nowdate(), 25)))
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_start_date')), getdate(add_days(nowdate(), 26)))
self.assertEqual(getdate(frappe.db.get_value('Task', task3.name, 'exp_end_date')), getdate(add_days(nowdate(), 30)))
```

## Next Steps


---

*Source: test_task.py:60 | Complexity: Advanced | Last updated: 2026-02-04*