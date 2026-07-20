# How To: Task Total Costing And Billing Amount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test task total costing and billing amount

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

### Step 1: Assign project_name = 'Test Project Costing'

```python
project_name = 'Test Project Costing'
```

### Step 2: Assign employee = make_employee(...)

```python
employee = make_employee('employee@frappe.io')
```

### Step 3: Assign project = make_project(...)

```python
project = make_project({'project_name': project_name})
```

### Step 4: Assign task = create_task(...)

```python
task = create_task('_Test Task 1')
```

### Step 5: Assign task.project = value

```python
task.project = project.name
```

### Step 6: Call task.save()

```python
task.save()
```

### Step 7: Assign timesheet = make_timesheet(...)

```python
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80, task=task.name)
```

### Step 8: Call timesheet.reload()

```python
timesheet.reload()
```

### Step 9: Call project.reload()

```python
project.reload()
```

### Step 10: Call task.reload()

```python
task.reload()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(task.total_costing_amount, 3200)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(task.total_billing_amount, 8000)
```


## Complete Example

```python
# Workflow
from erpnext.projects.doctype.project.test_project import make_project
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.setup.doctype.employee.test_employee import make_employee
project_name = 'Test Project Costing'
employee = make_employee('employee@frappe.io')
project = make_project({'project_name': project_name})
task = create_task('_Test Task 1')
task.project = project.name
task.save()
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80, task=task.name)
timesheet.reload()
project.reload()
task.reload()
self.assertEqual(task.total_costing_amount, 3200)
self.assertEqual(task.total_billing_amount, 8000)
```

## Next Steps


---

*Source: test_task.py:17 | Complexity: Advanced | Last updated: 2026-02-04*