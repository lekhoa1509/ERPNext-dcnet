# How To: To Time

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test to time

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.projects.doctype.task.test_task`
- `erpnext.projects.doctype.timesheet.timesheet`
- `erpnext.setup.doctype.employee.test_employee`
- `erpnext.tests.utils`

**Setup Required:**
```python
frappe.db.delete('Timesheet')
```

## Step-by-Step Guide

### Step 1: Assign emp = make_employee(...)

```python
emp = make_employee('test_employee_6@salary.com')
```

### Step 2: Assign from_time = now_datetime(...)

```python
from_time = now_datetime()
```

### Step 3: Assign timesheet = frappe.new_doc(...)

```python
timesheet = frappe.new_doc('Timesheet')
```

### Step 4: Assign timesheet.employee = emp

```python
timesheet.employee = emp
```

### Step 5: Call timesheet.append()

```python
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': from_time, 'hours': 2, 'company': '_Test Company'})
```

### Step 6: Call timesheet.save()

```python
timesheet.save()
```

### Step 7: Assign to_time = value

```python
to_time = timesheet.time_logs[0].to_time
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(to_time, add_to_date(from_time, hours=2, as_datetime=True))
```


## Complete Example

```python
# Setup
frappe.db.delete('Timesheet')

# Workflow
emp = make_employee('test_employee_6@salary.com')
from_time = now_datetime()
timesheet = frappe.new_doc('Timesheet')
timesheet.employee = emp
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': from_time, 'hours': 2, 'company': '_Test Company'})
timesheet.save()
to_time = timesheet.time_logs[0].to_time
self.assertEqual(to_time, add_to_date(from_time, hours=2, as_datetime=True))
```

## Next Steps


---

*Source: test_timesheet.py:223 | Complexity: Advanced | Last updated: 2026-02-04*