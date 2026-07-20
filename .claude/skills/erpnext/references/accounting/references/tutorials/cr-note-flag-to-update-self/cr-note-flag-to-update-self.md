# How To: Cr Note Flag To Update Self

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cr note flag to update self

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
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
```

### Step 2: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
```

### Step 3: Assign si.set_posting_time = True

```python
si.set_posting_time = True
```

### Step 4: Assign si.posting_date = add_days(...)

```python
si.posting_date = add_days(today(), -1)
```

### Step 5: Call si.save.submit()

```python
si.save().submit()
```

### Step 6: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 7: Assign expected_data = value

```python
expected_data = [100, 100, 'No Remarks']
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(report[1]), 1)
```

### Step 9: Assign row = value

```python
row = report[1][0]
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
```

### Step 11: Call self.create_payment_entry()

```python
self.create_payment_entry(si.name)
```

### Step 12: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 13: Assign expected_data_after_payment = value

```python
expected_data_after_payment = [100, 100, 40, 60]
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(report[1]), 1)
```

### Step 15: Assign row = value

```python
row = report[1][0]
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(expected_data_after_payment, [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
```

### Step 17: Assign cr_note = self.create_credit_note(...)

```python
cr_note = self.create_credit_note(si.name, do_not_submit=True)
```

### Step 18: Assign cr_note.update_outstanding_for_self = True

```python
cr_note.update_outstanding_for_self = True
```

### Step 19: Call cr_note.save.submit()

```python
cr_note.save().submit()
```

### Step 20: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 21: Assign expected_data_after_credit_note = value

```python
expected_data_after_credit_note = [[100.0, 100.0, 40.0, 0.0, 60.0, si.name], [0, 0, 100.0, 0.0, -100.0, cr_note.name]]
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(report[1]), 2)
```

### Step 23: Assign si_row = next(...)

```python
si_row = next(([row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.voucher_no] for row in report[1] if row.voucher_no == si.name))
```

### Step 24: Assign cr_note_row = next(...)

```python
cr_note_row = next(([row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.voucher_no] for row in report[1] if row.voucher_no == cr_note.name))
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(expected_data_after_credit_note[0], si_row)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(expected_data_after_credit_note[1], cr_note_row)
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
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
si = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
si.set_posting_time = True
si.posting_date = add_days(today(), -1)
si.save().submit()
report = execute(filters)
expected_data = [100, 100, 'No Remarks']
self.assertEqual(len(report[1]), 1)
row = report[1][0]
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_payment_entry(si.name)
report = execute(filters)
expected_data_after_payment = [100, 100, 40, 60]
self.assertEqual(len(report[1]), 1)
row = report[1][0]
self.assertEqual(expected_data_after_payment, [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = True
cr_note.save().submit()
report = execute(filters)
expected_data_after_credit_note = [[100.0, 100.0, 40.0, 0.0, 60.0, si.name], [0, 0, 100.0, 0.0, -100.0, cr_note.name]]
self.assertEqual(len(report[1]), 2)
si_row = next(([row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.voucher_no] for row in report[1] if row.voucher_no == si.name))
cr_note_row = next(([row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.voucher_no] for row in report[1] if row.voucher_no == cr_note.name))
self.assertEqual(expected_data_after_credit_note[0], si_row)
self.assertEqual(expected_data_after_credit_note[1], cr_note_row)
```

## Next Steps


---

*Source: test_accounts_receivable.py:338 | Complexity: Advanced | Last updated: 2026-02-03*