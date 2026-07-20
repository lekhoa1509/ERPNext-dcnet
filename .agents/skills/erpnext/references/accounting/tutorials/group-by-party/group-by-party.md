# How To: Group By Party

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test group by party

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

### Step 1: Assign si1 = self.create_sales_invoice(...)

```python
si1 = self.create_sales_invoice(do_not_submit=True)
```

### Step 2: Assign si1.posting_date = add_days(...)

```python
si1.posting_date = add_days(today(), -1)
```

### Step 3: Call si1.save.submit()

```python
si1.save().submit()
```

### Step 4: Assign si2 = self.create_sales_invoice(...)

```python
si2 = self.create_sales_invoice(do_not_submit=True)
```

### Step 5: Assign unknown.rate = 85

```python
si2.items[0].rate = 85
```

### Step 6: Call si2.save.submit()

```python
si2.save().submit()
```

### Step 7: Assign filters = value

```python
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120', 'group_by_party': True}
```

### Step 8: Assign report = value

```python
report = execute(filters)[1]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(report), 5)
```

### Step 10: Assign expected_voucher_rows = value

```python
expected_voucher_rows = [[100.0, 100.0, 100.0, 100.0], [85.0, 85.0, 85.0, 85.0]]
```

### Step 11: Assign voucher_rows = value

```python
voucher_rows = []
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(expected_voucher_rows, voucher_rows)
```

### Step 13: Assign expected_total_rows = value

```python
expected_total_rows = [[self.customer, 185.0, 185.0], {}, ['Total', 185.0, 185.0]]
```

### Step 14: Assign party_total_row = value

```python
party_total_row = report[2]
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(expected_total_rows[0], [party_total_row.get('party'), party_total_row.get('invoiced'), party_total_row.get('outstanding')])
```

### Step 16: Assign empty_row = value

```python
empty_row = report[3]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(expected_total_rows[1], empty_row)
```

### Step 18: Assign grand_total_row = value

```python
grand_total_row = report[4]
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(expected_total_rows[2], [grand_total_row.get('party'), grand_total_row.get('invoiced'), grand_total_row.get('outstanding')])
```

### Step 20: Call voucher_rows.append()

```python
voucher_rows.append([x.invoiced, x.outstanding, x.invoiced_in_account_currency, x.outstanding_in_account_currency])
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
si1 = self.create_sales_invoice(do_not_submit=True)
si1.posting_date = add_days(today(), -1)
si1.save().submit()
si2 = self.create_sales_invoice(do_not_submit=True)
si2.items[0].rate = 85
si2.save().submit()
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120', 'group_by_party': True}
report = execute(filters)[1]
self.assertEqual(len(report), 5)
expected_voucher_rows = [[100.0, 100.0, 100.0, 100.0], [85.0, 85.0, 85.0, 85.0]]
voucher_rows = []
for x in report[0:2]:
    voucher_rows.append([x.invoiced, x.outstanding, x.invoiced_in_account_currency, x.outstanding_in_account_currency])
self.assertEqual(expected_voucher_rows, voucher_rows)
expected_total_rows = [[self.customer, 185.0, 185.0], {}, ['Total', 185.0, 185.0]]
party_total_row = report[2]
self.assertEqual(expected_total_rows[0], [party_total_row.get('party'), party_total_row.get('invoiced'), party_total_row.get('outstanding')])
empty_row = report[3]
self.assertEqual(expected_total_rows[1], empty_row)
grand_total_row = report[4]
self.assertEqual(expected_total_rows[2], [grand_total_row.get('party'), grand_total_row.get('invoiced'), grand_total_row.get('outstanding')])
```

## Next Steps


---

*Source: test_accounts_receivable.py:563 | Complexity: Advanced | Last updated: 2026-02-03*