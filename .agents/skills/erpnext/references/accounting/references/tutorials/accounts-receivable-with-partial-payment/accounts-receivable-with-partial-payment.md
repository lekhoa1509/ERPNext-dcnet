# How To: Accounts Receivable With Partial Payment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test accounts receivable with partial payment

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.accounts_receivable.accounts_receivable`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.selling.doctype.sales_order.test_sales_order`

**Setup Required:**
```python
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: Assign filters = value

```python
filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
```

### Step 2: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(qty=2)
```

### Step 3: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 4: Assign expected_data = value

```python
expected_data = [[200, 60, 'No Remarks'], [200, 100, 'No Remarks'], [200, 40, 'No Remarks']]
```

### Step 5: Call self.create_payment_entry()

```python
self.create_payment_entry(si.name)
```

### Step 6: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 7: Assign expected_data_after_payment = value

```python
expected_data_after_payment = [[200, 60, 40, 20], [200, 100, 0, 100], [200, 40, 0, 40]]
```

### Step 8: Assign cr_note = self.create_credit_note(...)

```python
cr_note = self.create_credit_note(si.name, do_not_submit=True)
```

### Step 9: Assign cr_note.update_outstanding_for_self = False

```python
cr_note.update_outstanding_for_self = False
```

### Step 10: Call cr_note.save.submit()

```python
cr_note.save().submit()
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(cr_note.update_outstanding_for_self)
```

### Step 12: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 13: Assign expected_data_after_credit_note = value

```python
expected_data_after_credit_note = [[200, 100, 0, 80, 20, self.debit_to], [200, 40, 0, 0, 40, self.debit_to]]
```

### Step 14: Assign row = value

```python
row = report[1][i - 1]
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
```

### Step 16: Assign row = value

```python
row = report[1][i - 1]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(expected_data_after_payment[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
```

### Step 18: Assign row = value

```python
row = report[1][i - 1]
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(expected_data_after_credit_note[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.party_account])
```


## Complete Example

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

# Workflow
filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
si = self.create_sales_invoice(qty=2)
report = execute(filters)
expected_data = [[200, 60, 'No Remarks'], [200, 100, 'No Remarks'], [200, 40, 'No Remarks']]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_payment_entry(si.name)
report = execute(filters)
expected_data_after_payment = [[200, 60, 40, 20], [200, 100, 0, 100], [200, 40, 0, 40]]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data_after_payment[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = False
cr_note.save().submit()
self.assertFalse(cr_note.update_outstanding_for_self)
report = execute(filters)
expected_data_after_credit_note = [[200, 100, 0, 80, 20, self.debit_to], [200, 40, 0, 0, 40, self.debit_to]]
for i in range(2):
    row = report[1][i - 1]
    self.assertEqual(expected_data_after_credit_note[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.party_account])
```

## Next Steps


---

*Source: test_accounts_receivable.py:277 | Complexity: Advanced | Last updated: 2026-02-03*