# How To: Project Total Costing And Billing Amount

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test project total costing and billing amount

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.projects.doctype.project_template.test_project_template`
- `erpnext.projects.doctype.task.test_task`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.tests.utils`
- `erpnext.projects.doctype.timesheet.test_timesheet`
- `erpnext.setup.doctype.employee.test_employee`


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

### Step 4: Assign timesheet = make_timesheet(...)

```python
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80)
```

### Step 5: Call timesheet.reload()

```python
timesheet.reload()
```

### Step 6: Call project.reload()

```python
project.reload()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(project.total_costing_amount, 3200)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(project.total_billable_amount, 8000)
```


## Complete Example

```python
# Workflow
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.setup.doctype.employee.test_employee import make_employee
project_name = 'Test Project Costing'
employee = make_employee('employee@frappe.io')
project = make_project({'project_name': project_name})
timesheet = make_timesheet(employee=employee, is_billable=1, currency='USD', project=project.name, simulate=True, exchange_rate=80)
timesheet.reload()
project.reload()
self.assertEqual(project.total_costing_amount, 3200)
self.assertEqual(project.total_billable_amount, 8000)
```

## Next Steps


---

*Source: test_project.py:22 | Complexity: Advanced | Last updated: 2026-02-04*