# How To: Summary With Return And Payment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test summary with return and payment

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

### Step 7: Assign cr_note = self.create_credit_note(...)

```python
cr_note = self.create_credit_note(si.name, True)
```

### Step 8: Assign unknown.qty = value

```python
cr_note.items[0].qty = -2
```

### Step 9: Call cr_note.save.submit()

```python
cr_note.save().submit()
```

### Step 10: Assign expected_after_cr_note = value

```python
expected_after_cr_note = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 200.0, 'closing_balance': 800.0, 'currency': 'INR'}
```

### Step 11: Assign report = value

```python
report = execute(filters)[1]
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(report), 1)
```

### Step 13: Assign pe = self.create_payment_entry(...)

```python
pe = self.create_payment_entry(si.name, True)
```

### Step 14: Assign pe.paid_amount = 500

```python
pe.paid_amount = 500
```

### Step 15: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 16: Assign expected_after_cr_and_payment = value

```python
expected_after_cr_and_payment = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 500.0, 'return_amount': 200.0, 'closing_balance': 300.0, 'currency': 'INR'}
```

### Step 17: Assign report = value

```python
report = execute(filters)[1]
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(len(report), 1)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(report[0].get(field), expected.get(field))
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(report[0].get(field), expected_after_cr_note.get(field))
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(report[0].get(field), expected_after_cr_and_payment.get(field))
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
cr_note = self.create_credit_note(si.name, True)
cr_note.items[0].qty = -2
cr_note.save().submit()
expected_after_cr_note = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 200.0, 'closing_balance': 800.0, 'currency': 'INR'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected_after_cr_note:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected_after_cr_note.get(field))
pe = self.create_payment_entry(si.name, True)
pe.paid_amount = 500
pe.save().submit()
expected_after_cr_and_payment = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 500.0, 'return_amount': 200.0, 'closing_balance': 300.0, 'currency': 'INR'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected_after_cr_and_payment:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected_after_cr_and_payment.get(field))
```

## Next Steps


---

*Source: test_customer_ledger_summary.py:89 | Complexity: Advanced | Last updated: 2026-02-03*