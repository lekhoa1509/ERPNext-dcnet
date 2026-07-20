# How To: Payment Againt Po In Receivable Report

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Payments made against Purchase Order will show up as outstanding amount

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

### Step 1: '\n\t\tPayments made against Purchase Order will show up as outstanding amount\n\t\t'

```python
'\n\t\tPayments made against Purchase Order will show up as outstanding amount\n\t\t'
```

### Step 2: Assign so = make_sales_order(...)

```python
so = make_sales_order(company=self.company, customer=self.customer, warehouse=self.warehouse, debit_to=self.debit_to, income_account=self.income_account, expense_account=self.expense_account, cost_center=self.cost_center)
```

### Step 3: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(so.doctype, so.name)
```

### Step 4: Assign pe = pe.save.submit(...)

```python
pe = pe.save().submit()
```

### Step 5: Assign filters = value

```python
filters = {'company': self.company, 'based_on_payment_terms': 0, 'report_date': today(), 'range': '30, 60, 90, 120'}
```

### Step 6: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 7: Assign expected_data_after_payment = value

```python
expected_data_after_payment = [0, 1000, 0, -1000]
```

### Step 8: Assign row = value

```python
row = report[1][0]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(expected_data_after_payment, [row.invoiced, row.paid, row.credit_note, row.outstanding])
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
'\n\t\tPayments made against Purchase Order will show up as outstanding amount\n\t\t'
so = make_sales_order(company=self.company, customer=self.customer, warehouse=self.warehouse, debit_to=self.debit_to, income_account=self.income_account, expense_account=self.expense_account, cost_center=self.cost_center)
pe = get_payment_entry(so.doctype, so.name)
pe = pe.save().submit()
filters = {'company': self.company, 'based_on_payment_terms': 0, 'report_date': today(), 'range': '30, 60, 90, 120'}
report = execute(filters)
expected_data_after_payment = [0, 1000, 0, -1000]
row = report[1][0]
self.assertEqual(expected_data_after_payment, [row.invoiced, row.paid, row.credit_note, row.outstanding])
```

## Next Steps


---

*Source: test_accounts_receivable.py:411 | Complexity: Advanced | Last updated: 2026-02-03*