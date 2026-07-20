# How To: Pos Receivable

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pos receivable

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
filters = {'company': self.company, 'party_type': 'Customer', 'party': [self.customer], 'report_date': add_days(today(), 2), 'based_on_payment_terms': 0, 'range': '30, 60, 90, 120', 'show_remarks': False}
```

### Step 2: Assign pos_inv = self.create_sales_invoice(...)

```python
pos_inv = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
```

### Step 3: Assign pos_inv.posting_date = add_days(...)

```python
pos_inv.posting_date = add_days(today(), 2)
```

### Step 4: Assign pos_inv.is_pos = 1

```python
pos_inv.is_pos = 1
```

### Step 5: Call pos_inv.append()

```python
pos_inv.append('payments', frappe._dict(mode_of_payment='Cash', amount=flt(pos_inv.grand_total / 2)))
```

### Step 6: Assign pos_inv.disable_rounded_total = 1

```python
pos_inv.disable_rounded_total = 1
```

### Step 7: Call pos_inv.save()

```python
pos_inv.save()
```

### Step 8: Call pos_inv.submit()

```python
pos_inv.submit()
```

### Step 9: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 10: Assign expected_data = value

```python
expected_data = [[pos_inv.grand_total, pos_inv.paid_amount, 0]]
```

### Step 11: Assign row = value

```python
row = report[1][-1]
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(expected_data[0], [row.invoiced, row.paid, row.credit_note])
```

### Step 13: Call pos_inv.cancel()

```python
pos_inv.cancel()
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
filters = {'company': self.company, 'party_type': 'Customer', 'party': [self.customer], 'report_date': add_days(today(), 2), 'based_on_payment_terms': 0, 'range': '30, 60, 90, 120', 'show_remarks': False}
pos_inv = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
pos_inv.posting_date = add_days(today(), 2)
pos_inv.is_pos = 1
pos_inv.append('payments', frappe._dict(mode_of_payment='Cash', amount=flt(pos_inv.grand_total / 2)))
pos_inv.disable_rounded_total = 1
pos_inv.save()
pos_inv.submit()
report = execute(filters)
expected_data = [[pos_inv.grand_total, pos_inv.paid_amount, 0]]
row = report[1][-1]
self.assertEqual(expected_data[0], [row.invoiced, row.paid, row.credit_note])
pos_inv.cancel()
```

## Next Steps


---

*Source: test_accounts_receivable.py:80 | Complexity: Advanced | Last updated: 2026-02-03*