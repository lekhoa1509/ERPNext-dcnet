# How To: Per Billed Hours

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: If amounts are 0, per_billed should be calculated based on hours.

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

### Step 1: 'If amounts are 0, per_billed should be calculated based on hours.'

```python
'If amounts are 0, per_billed should be calculated based on hours.'
```

### Step 2: Assign ts = frappe.new_doc(...)

```python
ts = frappe.new_doc('Timesheet')
```

### Step 3: Assign ts.total_billable_amount = 0

```python
ts.total_billable_amount = 0
```

### Step 4: Assign ts.total_billed_amount = 0

```python
ts.total_billed_amount = 0
```

### Step 5: Assign ts.total_billable_hours = 2

```python
ts.total_billable_hours = 2
```

### Step 6: Assign ts.total_billed_hours = 0.5

```python
ts.total_billed_hours = 0.5
```

### Step 7: Call ts.calculate_percentage_billed()

```python
ts.calculate_percentage_billed()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(ts.per_billed, 25)
```

### Step 9: Assign ts.total_billed_hours = 2

```python
ts.total_billed_hours = 2
```

### Step 10: Call ts.calculate_percentage_billed()

```python
ts.calculate_percentage_billed()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(ts.per_billed, 100)
```


## Complete Example

```python
# Setup
frappe.db.delete('Timesheet')

# Workflow
'If amounts are 0, per_billed should be calculated based on hours.'
ts = frappe.new_doc('Timesheet')
ts.total_billable_amount = 0
ts.total_billed_amount = 0
ts.total_billable_hours = 2
ts.total_billed_hours = 0.5
ts.calculate_percentage_billed()
self.assertEqual(ts.per_billed, 25)
ts.total_billed_hours = 2
ts.calculate_percentage_billed()
self.assertEqual(ts.per_billed, 100)
```

## Next Steps


---

*Source: test_timesheet.py:244 | Complexity: Advanced | Last updated: 2026-02-04*