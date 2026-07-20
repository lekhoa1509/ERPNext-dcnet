# How To: Dunning Resolution From Credit Note

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that dunning is resolved when a credit note is issued against the original invoice.

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

### Step 1: '\n\t\tTest that dunning is resolved when a credit note is issued against the original invoice.\n\t\t'

```python
'\n\t\tTest that dunning is resolved when a credit note is issued against the original invoice.\n\t\t'
```

### Step 2: Assign sales_invoice = create_sales_invoice_against_cost_center(...)

```python
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -10), qty=1, rate=100)
```

### Step 3: Assign dunning = create_dunning_from_sales_invoice(...)

```python
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
```

### Step 4: Call dunning.submit()

```python
dunning.submit()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(dunning.status, 'Unresolved')
```

### Step 6: Assign credit_note = frappe.copy_doc(...)

```python
credit_note = frappe.copy_doc(sales_invoice)
```

### Step 7: Assign credit_note.is_return = 1

```python
credit_note.is_return = 1
```

### Step 8: Assign credit_note.return_against = value

```python
credit_note.return_against = sales_invoice.name
```

### Step 9: Assign credit_note.update_outstanding_for_self = 0

```python
credit_note.update_outstanding_for_self = 0
```

### Step 10: Call credit_note.save()

```python
credit_note.save()
```

### Step 11: Call credit_note.submit()

```python
credit_note.submit()
```

### Step 12: Call dunning.reload()

```python
dunning.reload()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(dunning.status, 'Resolved')
```

### Step 14: Call credit_note.cancel()

```python
credit_note.cancel()
```

### Step 15: Call dunning.reload()

```python
dunning.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(dunning.status, 'Unresolved')
```

### Step 17: Assign item.qty = value

```python
item.qty = -item.qty
```


## Complete Example

```python
# Workflow
'\n\t\tTest that dunning is resolved when a credit note is issued against the original invoice.\n\t\t'
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -10), qty=1, rate=100)
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
dunning.submit()
self.assertEqual(dunning.status, 'Unresolved')
credit_note = frappe.copy_doc(sales_invoice)
credit_note.is_return = 1
credit_note.return_against = sales_invoice.name
credit_note.update_outstanding_for_self = 0
for item in credit_note.items:
    item.qty = -item.qty
credit_note.save()
credit_note.submit()
dunning.reload()
self.assertEqual(dunning.status, 'Resolved')
credit_note.cancel()
dunning.reload()
self.assertEqual(dunning.status, 'Unresolved')
```

## Next Steps


---

*Source: test_dunning.py:142 | Complexity: Advanced | Last updated: 2026-02-03*