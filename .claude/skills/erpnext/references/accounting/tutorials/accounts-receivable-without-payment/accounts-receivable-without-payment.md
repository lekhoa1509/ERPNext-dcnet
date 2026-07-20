# How To: Accounts Receivable Without Payment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test accounts receivable without payment

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
si = self.create_sales_invoice()
```

### Step 3: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 4: Assign expected_data = value

```python
expected_data = [[100, 30, 'No Remarks'], [100, 50, 'No Remarks'], [100, 20, 'No Remarks']]
```

### Step 5: Assign cr_note = self.create_credit_note(...)

```python
cr_note = self.create_credit_note(si.name, do_not_submit=True)
```

### Step 6: Assign cr_note.update_outstanding_for_self = False

```python
cr_note.update_outstanding_for_self = False
```

### Step 7: Call cr_note.save.submit()

```python
cr_note.save().submit()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(cr_note.update_outstanding_for_self, False)
```

### Step 9: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 10: Assign row = value

```python
row = report[1]
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(len(row) == 0)
```

### Step 12: Assign row = value

```python
row = report[1][i - 1]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
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
si = self.create_sales_invoice()
report = execute(filters)
expected_data = [[100, 30, 'No Remarks'], [100, 50, 'No Remarks'], [100, 20, 'No Remarks']]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = False
cr_note.save().submit()
self.assertEqual(cr_note.update_outstanding_for_self, False)
report = execute(filters)
row = report[1]
self.assertTrue(len(row) == 0)
```

## Next Steps


---

*Source: test_accounts_receivable.py:170 | Complexity: Advanced | Last updated: 2026-02-03*