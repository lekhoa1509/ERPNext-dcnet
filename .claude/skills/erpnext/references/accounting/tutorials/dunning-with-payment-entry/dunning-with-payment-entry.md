# How To: Dunning With Payment Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test dunning with payment entry

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.model`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`


## Step-by-Step Guide

### Step 1: Assign dunning = create_dunning(...)

```python
dunning = create_dunning(overdue_days=15, dunning_type_name='Second Notice - _TC')
```

### Step 2: Call dunning.submit()

```python
dunning.submit()
```

### Step 3: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Dunning', dunning.name)
```

### Step 4: Assign pe.reference_no = '1'

```python
pe.reference_no = '1'
```

### Step 5: Assign pe.reference_date = nowdate(...)

```python
pe.reference_date = nowdate()
```

### Step 6: Call pe.insert()

```python
pe.insert()
```

### Step 7: Call pe.submit()

```python
pe.submit()
```

### Step 8: Call dunning.reload()

```python
dunning.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(dunning.status, 'Resolved')
```

### Step 10: Assign outstanding_amount = frappe.get_value(...)

```python
outstanding_amount = frappe.get_value('Sales Invoice', overdue_payment.sales_invoice, 'outstanding_amount')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(outstanding_amount, 0)
```


## Complete Example

```python
# Workflow
dunning = create_dunning(overdue_days=15, dunning_type_name='Second Notice - _TC')
dunning.submit()
pe = get_payment_entry('Dunning', dunning.name)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.insert()
pe.submit()
for overdue_payment in dunning.overdue_payments:
    outstanding_amount = frappe.get_value('Sales Invoice', overdue_payment.sales_invoice, 'outstanding_amount')
    self.assertEqual(outstanding_amount, 0)
dunning.reload()
self.assertEqual(dunning.status, 'Resolved')
```

## Next Steps


---

*Source: test_dunning.py:56 | Complexity: Advanced | Last updated: 2026-02-03*