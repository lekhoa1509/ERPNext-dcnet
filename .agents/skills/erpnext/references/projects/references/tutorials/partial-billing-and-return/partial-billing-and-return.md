# How To: Partial Billing And Return

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Timesheet status transitions during partial billing, full billing,
sales return, and return cancellation.

Scenario:
1. Create a Timesheet with two billable time logs.
2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.
3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.
4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.
5. Cancel the Sales Return → Timesheet returns to Billed status.

This test ensures Timesheet status is recalculated correctly
across billing and return lifecycle events.

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

### Step 1: '\n\t\tTest Timesheet status transitions during partial billing, full billing,\n\t\tsales return, and return cancellation.\n\n\t\tScenario:\n\t\t1. Create a Timesheet with two billable time logs.\n\t\t2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.\n\t\t3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.\n\t\t4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.\n\t\t5. Cancel the Sales Return → Timesheet returns to Billed status.\n\n\t\tThis test ensures Timesheet status is recalculated correctly\n\t\tacross billing and return lifecycle events.\n\t\t'

```python
'\n\t\tTest Timesheet status transitions during partial billing, full billing,\n\t\tsales return, and return cancellation.\n\n\t\tScenario:\n\t\t1. Create a Timesheet with two billable time logs.\n\t\t2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.\n\t\t3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.\n\t\t4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.\n\t\t5. Cancel the Sales Return → Timesheet returns to Billed status.\n\n\t\tThis test ensures Timesheet status is recalculated correctly\n\t\tacross billing and return lifecycle events.\n\t\t'
```

### Step 2: Assign emp = make_employee(...)

```python
emp = make_employee('test_employee_6@salary.com')
```

### Step 3: Assign timesheet = make_timesheet(...)

```python
timesheet = make_timesheet(emp, simulate=True, is_billable=1, do_not_submit=True)
```

### Step 4: Assign timesheet_detail = timesheet.append(...)

```python
timesheet_detail = timesheet.append('time_logs', {})
```

### Step 5: Assign timesheet_detail.is_billable = 1

```python
timesheet_detail.is_billable = 1
```

### Step 6: Assign timesheet_detail.activity_type = '_Test Activity Type'

```python
timesheet_detail.activity_type = '_Test Activity Type'
```

### Step 7: Assign timesheet_detail.from_time = value

```python
timesheet_detail.from_time = timesheet.time_logs[0].to_time + datetime.timedelta(minutes=1)
```

### Step 8: Assign timesheet_detail.hours = 2

```python
timesheet_detail.hours = 2
```

### Step 9: Assign timesheet_detail.to_time = value

```python
timesheet_detail.to_time = timesheet_detail.from_time + datetime.timedelta(hours=timesheet_detail.hours)
```

### Step 10: Call timesheet.save.submit()

```python
timesheet.save().submit()
```

### Step 11: Assign sales_invoice = make_sales_invoice(...)

```python
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
```

### Step 12: Assign sales_invoice.due_date = nowdate(...)

```python
sales_invoice.due_date = nowdate()
```

### Step 13: Call sales_invoice.timesheets.pop()

```python
sales_invoice.timesheets.pop()
```

### Step 14: Call sales_invoice.submit()

```python
sales_invoice.submit()
```

### Step 15: Assign timesheet_status = frappe.get_value(...)

```python
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(timesheet_status, 'Partially Billed')
```

### Step 17: Assign sales_invoice2 = make_sales_invoice(...)

```python
sales_invoice2 = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
```

### Step 18: Assign sales_invoice2.due_date = nowdate(...)

```python
sales_invoice2.due_date = nowdate()
```

### Step 19: Call sales_invoice2.submit()

```python
sales_invoice2.submit()
```

### Step 20: Assign timesheet_status = frappe.get_value(...)

```python
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(timesheet_status, 'Billed')
```

### Step 22: Assign sales_return = make_sales_return.submit(...)

```python
sales_return = make_sales_return(sales_invoice2.name).submit()
```

### Step 23: Assign timesheet_status = frappe.get_value(...)

```python
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(timesheet_status, 'Partially Billed')
```

### Step 25: Call sales_return.load_from_db()

```python
sales_return.load_from_db()
```

### Step 26: Call sales_return.cancel()

```python
sales_return.cancel()
```

### Step 27: Call timesheet.load_from_db()

```python
timesheet.load_from_db()
```

### Step 28: Call self.assertEqual()

```python
self.assertEqual(timesheet.time_logs[1].sales_invoice, sales_invoice2.name)
```

### Step 29: Call self.assertEqual()

```python
self.assertEqual(timesheet.status, 'Billed')
```


## Complete Example

```python
# Setup
frappe.db.delete('Timesheet')

# Workflow
'\n\t\tTest Timesheet status transitions during partial billing, full billing,\n\t\tsales return, and return cancellation.\n\n\t\tScenario:\n\t\t1. Create a Timesheet with two billable time logs.\n\t\t2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.\n\t\t3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.\n\t\t4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.\n\t\t5. Cancel the Sales Return → Timesheet returns to Billed status.\n\n\t\tThis test ensures Timesheet status is recalculated correctly\n\t\tacross billing and return lifecycle events.\n\t\t'
emp = make_employee('test_employee_6@salary.com')
timesheet = make_timesheet(emp, simulate=True, is_billable=1, do_not_submit=True)
timesheet_detail = timesheet.append('time_logs', {})
timesheet_detail.is_billable = 1
timesheet_detail.activity_type = '_Test Activity Type'
timesheet_detail.from_time = timesheet.time_logs[0].to_time + datetime.timedelta(minutes=1)
timesheet_detail.hours = 2
timesheet_detail.to_time = timesheet_detail.from_time + datetime.timedelta(hours=timesheet_detail.hours)
timesheet.save().submit()
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice.due_date = nowdate()
sales_invoice.timesheets.pop()
sales_invoice.submit()
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
self.assertEqual(timesheet_status, 'Partially Billed')
sales_invoice2 = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice2.due_date = nowdate()
sales_invoice2.submit()
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
self.assertEqual(timesheet_status, 'Billed')
sales_return = make_sales_return(sales_invoice2.name).submit()
timesheet_status = frappe.get_value('Timesheet', timesheet.name, 'status')
self.assertEqual(timesheet_status, 'Partially Billed')
sales_return.load_from_db()
sales_return.cancel()
timesheet.load_from_db()
self.assertEqual(timesheet.time_logs[1].sales_invoice, sales_invoice2.name)
self.assertEqual(timesheet.status, 'Billed')
```

## Next Steps


---

*Source: test_timesheet.py:275 | Complexity: Advanced | Last updated: 2026-02-04*