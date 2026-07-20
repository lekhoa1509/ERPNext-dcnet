# How To: Fetch Overdue Payments

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Create SI with overdue payment. Check if overdue payment is fetched in Dunning.

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

### Step 1: '\n\t\tCreate SI with overdue payment. Check if overdue payment is fetched in Dunning.\n\t\t'

```python
'\n\t\tCreate SI with overdue payment. Check if overdue payment is fetched in Dunning.\n\t\t'
```

### Step 2: Assign si1 = create_sales_invoice_against_cost_center(...)

```python
si1 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100)
```

### Step 3: Assign si2 = create_sales_invoice_against_cost_center(...)

```python
si2 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=300)
```

### Step 4: Assign dunning = create_dunning_from_sales_invoice(...)

```python
dunning = create_dunning_from_sales_invoice(si1.name)
```

### Step 5: Assign dunning.overdue_payments = value

```python
dunning.overdue_payments = []
```

### Step 6: Assign method = 'erpnext.accounts.doctype.sales_invoice.sales_invoice.create_dunning'

```python
method = 'erpnext.accounts.doctype.sales_invoice.sales_invoice.create_dunning'
```

### Step 7: Assign updated_dunning = mapper.map_docs(...)

```python
updated_dunning = mapper.map_docs(method, json.dumps([si1.name, si2.name]), dunning)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(updated_dunning.overdue_payments), 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(updated_dunning.overdue_payments[0].sales_invoice, si1.name)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(updated_dunning.overdue_payments[0].outstanding, si1.outstanding_amount)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(updated_dunning.overdue_payments[1].sales_invoice, si2.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(updated_dunning.overdue_payments[1].outstanding, si2.outstanding_amount)
```


## Complete Example

```python
# Workflow
'\n\t\tCreate SI with overdue payment. Check if overdue payment is fetched in Dunning.\n\t\t'
si1 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100)
si2 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=300)
dunning = create_dunning_from_sales_invoice(si1.name)
dunning.overdue_payments = []
method = 'erpnext.accounts.doctype.sales_invoice.sales_invoice.create_dunning'
updated_dunning = mapper.map_docs(method, json.dumps([si1.name, si2.name]), dunning)
self.assertEqual(len(updated_dunning.overdue_payments), 2)
self.assertEqual(updated_dunning.overdue_payments[0].sales_invoice, si1.name)
self.assertEqual(updated_dunning.overdue_payments[0].outstanding, si1.outstanding_amount)
self.assertEqual(updated_dunning.overdue_payments[1].sales_invoice, si2.name)
self.assertEqual(updated_dunning.overdue_payments[1].outstanding, si2.outstanding_amount)
```

## Next Steps


---

*Source: test_dunning.py:74 | Complexity: Advanced | Last updated: 2026-02-03*