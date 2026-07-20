# How To: Exchange Revaluation For Party

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Exchange Revaluation for party on Receivable/Payable should be included

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

### Step 1: '\n\t\tExchange Revaluation for party on Receivable/Payable should be included\n\t\t'

```python
'\n\t\tExchange Revaluation for party on Receivable/Payable should be included\n\t\t'
```

### Step 2: Assign company_doc = frappe.get_doc(...)

```python
company_doc = frappe.get_doc('Company', self.company)
```

### Step 3: Assign company_doc.unrealized_exchange_gain_loss_account = value

```python
company_doc.unrealized_exchange_gain_loss_account = company_doc.exchange_gain_loss_account
```

### Step 4: Call company_doc.save()

```python
company_doc.save()
```

### Step 5: Assign si = self.create_sales_invoice(...)

```python
si = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
```

### Step 6: Assign si.currency = 'USD'

```python
si.currency = 'USD'
```

### Step 7: Assign si.conversion_rate = 80

```python
si.conversion_rate = 80
```

### Step 8: Assign si.debit_to = value

```python
si.debit_to = self.debtors_usd
```

### Step 9: Assign si = si.save.submit(...)

```python
si = si.save().submit()
```

### Step 10: Assign err = frappe.new_doc(...)

```python
err = frappe.new_doc('Exchange Rate Revaluation')
```

### Step 11: Assign err.company = value

```python
err.company = self.company
```

### Step 12: Assign err.posting_date = today(...)

```python
err.posting_date = today()
```

### Step 13: Assign accounts = err.get_accounts_data(...)

```python
accounts = err.get_accounts_data()
```

### Step 14: Call err.extend()

```python
err.extend('accounts', accounts)
```

### Step 15: Assign unknown.new_exchange_rate = 85

```python
err.accounts[0].new_exchange_rate = 85
```

### Step 16: Assign row = value

```python
row = err.accounts[0]
```

### Step 17: Assign row.new_balance_in_base_currency = flt(...)

```python
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
```

### Step 18: Assign row.gain_loss = value

```python
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
```

### Step 19: Call err.set_total_gain_loss()

```python
err.set_total_gain_loss()
```

### Step 20: Assign err = err.save.submit(...)

```python
err = err.save().submit()
```

### Step 21: Assign err_journals = err.make_jv_entries(...)

```python
err_journals = err.make_jv_entries()
```

### Step 22: Assign je = frappe.get_doc(...)

```python
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
```

### Step 23: Assign je = je.submit(...)

```python
je = je.submit()
```

### Step 24: Assign filters = value

```python
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120'}
```

### Step 25: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 26: Assign expected_data_for_err = value

```python
expected_data_for_err = [0, -500, 0, 500]
```

### Step 27: Assign row = next(...)

```python
row = next((x for x in report[1] if x.voucher_type == je.doctype and x.voucher_no == je.name))
```

### Step 28: Call self.assertEqual()

```python
self.assertEqual(expected_data_for_err, [row.invoiced, row.paid, row.credit_note, row.outstanding])
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
'\n\t\tExchange Revaluation for party on Receivable/Payable should be included\n\t\t'
company_doc = frappe.get_doc('Company', self.company)
company_doc.unrealized_exchange_gain_loss_account = company_doc.exchange_gain_loss_account
company_doc.save()
si = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
si.currency = 'USD'
si.conversion_rate = 80
si.debit_to = self.debtors_usd
si = si.save().submit()
err = frappe.new_doc('Exchange Rate Revaluation')
err.company = self.company
err.posting_date = today()
accounts = err.get_accounts_data()
err.extend('accounts', accounts)
err.accounts[0].new_exchange_rate = 85
row = err.accounts[0]
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
err.set_total_gain_loss()
err = err.save().submit()
err_journals = err.make_jv_entries()
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
je = je.submit()
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120'}
report = execute(filters)
expected_data_for_err = [0, -500, 0, 500]
row = next((x for x in report[1] if x.voucher_type == je.doctype and x.voucher_no == je.name))
self.assertEqual(expected_data_for_err, [row.invoiced, row.paid, row.credit_note, row.outstanding])
```

## Next Steps


---

*Source: test_accounts_receivable.py:455 | Complexity: Advanced | Last updated: 2026-02-03*