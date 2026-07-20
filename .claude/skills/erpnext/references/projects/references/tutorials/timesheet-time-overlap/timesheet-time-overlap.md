# How To: Timesheet Time Overlap

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test timesheet time overlap

## Prerequisites

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


## Step-by-Step Guide

### Step 1: Assign emp = make_employee(...)

```python
emp = make_employee('test_employee_6@salary.com')
```

### Step 2: Assign settings = frappe.get_single(...)

```python
settings = frappe.get_single('Projects Settings')
```

### Step 3: Assign initial_setting = value

```python
initial_setting = settings.ignore_employee_time_overlap
```

### Step 4: Assign settings.ignore_employee_time_overlap = 0

```python
settings.ignore_employee_time_overlap = 0
```

### Step 5: Call settings.save()

```python
settings.save()
```

### Step 6: Call update_activity_type()

```python
update_activity_type('_Test Activity Type')
```

### Step 7: Assign timesheet = frappe.new_doc(...)

```python
timesheet = frappe.new_doc('Timesheet')
```

### Step 8: Assign timesheet.employee = emp

```python
timesheet.employee = emp
```

### Step 9: Call timesheet.append()

```python
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
```

### Step 10: Call timesheet.append()

```python
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, timesheet.save)
```

### Step 12: Assign settings.ignore_employee_time_overlap = 1

```python
settings.ignore_employee_time_overlap = 1
```

### Step 13: Call settings.save()

```python
settings.save()
```

### Step 14: Call timesheet.save()

```python
timesheet.save()
```

### Step 15: Call timesheet.submit()

```python
timesheet.submit()
```

### Step 16: Assign settings.ignore_employee_time_overlap = 0

```python
settings.ignore_employee_time_overlap = 0
```

### Step 17: Call settings.save()

```python
settings.save()
```

### Step 18: Call timesheet.append()

```python
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
```

### Step 19: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, timesheet.submit)
```

### Step 20: Assign settings.ignore_employee_time_overlap = initial_setting

```python
settings.ignore_employee_time_overlap = initial_setting
```

### Step 21: Call settings.save()

```python
settings.save()
```


## Complete Example

```python
# Workflow
emp = make_employee('test_employee_6@salary.com')
settings = frappe.get_single('Projects Settings')
initial_setting = settings.ignore_employee_time_overlap
settings.ignore_employee_time_overlap = 0
settings.save()
update_activity_type('_Test Activity Type')
timesheet = frappe.new_doc('Timesheet')
timesheet.employee = emp
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
self.assertRaises(frappe.ValidationError, timesheet.save)
settings.ignore_employee_time_overlap = 1
settings.save()
timesheet.save()
timesheet.submit()
settings.ignore_employee_time_overlap = 0
settings.save()
timesheet.append('time_logs', {'billable': 1, 'activity_type': '_Test Activity Type', 'from_time': now_datetime(), 'to_time': now_datetime() + datetime.timedelta(hours=3), 'company': '_Test Company'})
self.assertRaises(frappe.ValidationError, timesheet.submit)
settings.ignore_employee_time_overlap = initial_setting
settings.save()
```

## Next Steps


---

*Source: test_timesheet.py:138 | Complexity: Advanced | Last updated: 2026-02-04*