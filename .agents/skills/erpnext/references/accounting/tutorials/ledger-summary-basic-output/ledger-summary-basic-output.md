# How To: Ledger Summary Basic Output

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test ledger summary basic output

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.customer_ledger_summary.customer_ledger_summary`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.controllers.sales_and_purchase_return`


## Step-by-Step Guide

### Step 1: Assign filters = value

```python
filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
```

### Step 2: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(do_not_submit=True)
```

### Step 3: Call si.save.submit()

```python
si.save().submit()
```

### Step 4: Assign expected = value

```python
expected = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 1000.0, 'currency': 'INR', 'customer_name': '_Test Customer'}
```

### Step 5: Assign report = value

```python
report = execute(filters)[1]
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(report), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(report[0].get(field), expected.get(field))
```


## Complete Example

```python
# Workflow
filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
si = self.create_sales_invoice(do_not_submit=True)
si.save().submit()
expected = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 1000.0, 'currency': 'INR', 'customer_name': '_Test Customer'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected.get(field))
```

## Next Steps


---

*Source: test_customer_ledger_summary.py:65 | Complexity: Intermediate | Last updated: 2026-02-03*