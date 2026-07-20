# How To: Timesheet Billing Based On Project

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test timesheet billing based on project

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

### Step 2: Assign project = frappe.get_value(...)

```python
project = frappe.get_value('Project', {'project_name': '_Test Project'})
```

### Step 3: Assign timesheet = make_timesheet(...)

```python
timesheet = make_timesheet(emp, simulate=True, is_billable=1, project=project, company='_Test Company')
```

### Step 4: Assign sales_invoice = create_sales_invoice(...)

```python
sales_invoice = create_sales_invoice(do_not_save=True)
```

### Step 5: Assign sales_invoice.project = project

```python
sales_invoice.project = project
```

### Step 6: Call sales_invoice.add_timesheet_data()

```python
sales_invoice.add_timesheet_data()
```

### Step 7: Call sales_invoice.submit()

```python
sales_invoice.submit()
```

### Step 8: Assign ts = frappe.get_doc(...)

```python
ts = frappe.get_doc('Timesheet', timesheet.name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(ts.per_billed, 100)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(ts.time_logs[0].sales_invoice, sales_invoice.name)
```


## Complete Example

```python
# Workflow
emp = make_employee('test_employee_6@salary.com')
project = frappe.get_value('Project', {'project_name': '_Test Project'})
timesheet = make_timesheet(emp, simulate=True, is_billable=1, project=project, company='_Test Company')
sales_invoice = create_sales_invoice(do_not_save=True)
sales_invoice.project = project
sales_invoice.add_timesheet_data()
sales_invoice.submit()
ts = frappe.get_doc('Timesheet', timesheet.name)
self.assertEqual(ts.per_billed, 100)
self.assertEqual(ts.time_logs[0].sales_invoice, sales_invoice.name)
```

## Next Steps


---

*Source: test_timesheet.py:122 | Complexity: Advanced | Last updated: 2026-02-04*