# How To: Sales Invoice From Timesheet

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales invoice from timesheet

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

### Step 2: Assign timesheet = make_timesheet(...)

```python
timesheet = make_timesheet(emp, simulate=True, is_billable=1)
```

### Step 3: Assign sales_invoice = make_sales_invoice(...)

```python
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
```

### Step 4: Assign sales_invoice.due_date = nowdate(...)

```python
sales_invoice.due_date = nowdate()
```

### Step 5: Call sales_invoice.submit()

```python
sales_invoice.submit()
```

### Step 6: Assign timesheet = frappe.get_doc(...)

```python
timesheet = frappe.get_doc('Timesheet', timesheet.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(sales_invoice.total_billing_amount, 100)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(timesheet.status, 'Billed')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(sales_invoice.customer, '_Test Customer')
```

### Step 10: Assign item = value

```python
item = sales_invoice.items[0]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(item.item_code, '_Test Item')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(item.qty, 2.0)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(item.rate, 50.0)
```


## Complete Example

```python
# Workflow
emp = make_employee('test_employee_6@salary.com')
timesheet = make_timesheet(emp, simulate=True, is_billable=1)
sales_invoice = make_sales_invoice(timesheet.name, '_Test Item', '_Test Customer', currency='INR')
sales_invoice.due_date = nowdate()
sales_invoice.submit()
timesheet = frappe.get_doc('Timesheet', timesheet.name)
self.assertEqual(sales_invoice.total_billing_amount, 100)
self.assertEqual(timesheet.status, 'Billed')
self.assertEqual(sales_invoice.customer, '_Test Customer')
item = sales_invoice.items[0]
self.assertEqual(item.item_code, '_Test Item')
self.assertEqual(item.qty, 2.0)
self.assertEqual(item.rate, 50.0)
```

## Next Steps


---

*Source: test_timesheet.py:104 | Complexity: Advanced | Last updated: 2026-02-04*