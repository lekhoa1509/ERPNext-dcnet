# How To: Allow Multi Currency Invoices Against Single Party Account

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test allow multi currency invoices against single party account

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
filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True, 'in_party_currency': 1}
```

### Step 2: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(qty=1, no_payment_schedule=True, do_not_submit=True)
```

### Step 3: Assign si.currency = 'USD'

```python
si.currency = 'USD'
```

### Step 4: Assign si.conversion_rate = 80

```python
si.conversion_rate = 80
```

### Step 5: Call si.save.submit()

```python
si.save().submit()
```

### Step 6: Call filters.update()

```python
filters.update({'party_type': 'Customer', 'party': [self.customer]})
```

### Step 7: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 8: Assign row = value

```python
row = report[1][0]
```

### Step 9: Assign expected_data = value

```python
expected_data = [8000, 8000, 'No Remarks']
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
```

### Step 11: Call self.create_customer()

```python
self.create_customer('USD Customer', currency='USD', default_account=self.debtors_usd, company=self.company)
```

### Step 12: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, currency='USD', conversion_rate=80, price_list_rate=100, do_not_save=1)
```

### Step 13: Call si.save.submit()

```python
si.save().submit()
```

### Step 14: Call filters.update()

```python
filters.update({'party_type': 'Customer', 'party': [self.customer]})
```

### Step 15: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 16: Assign row = value

```python
row = report[1][0]
```

### Step 17: Assign expected_data = value

```python
expected_data = [100, 100, 'No Remarks']
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
```

### Step 19: Call filters.pop()

```python
filters.pop('in_party_currency')
```

### Step 20: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 21: Assign row = value

```python
row = report[1][0]
```

### Step 22: Assign expected_data = value

```python
expected_data = [8000, 8000, 'No Remarks']
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
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
filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True, 'in_party_currency': 1}
si = self.create_sales_invoice(qty=1, no_payment_schedule=True, do_not_submit=True)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
filters.update({'party_type': 'Customer', 'party': [self.customer]})
report = execute(filters)
row = report[1][0]
expected_data = [8000, 8000, 'No Remarks']
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_customer('USD Customer', currency='USD', default_account=self.debtors_usd, company=self.company)
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, currency='USD', conversion_rate=80, price_list_rate=100, do_not_save=1)
si.save().submit()
filters.update({'party_type': 'Customer', 'party': [self.customer]})
report = execute(filters)
row = report[1][0]
expected_data = [100, 100, 'No Remarks']
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
filters.pop('in_party_currency')
report = execute(filters)
row = report[1][0]
expected_data = [8000, 8000, 'No Remarks']
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
```

## Next Steps


---

*Source: test_accounts_receivable.py:206 | Complexity: Advanced | Last updated: 2026-02-03*