# How To: 01 Revaluation Of Forex Balance

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Forex account balance and Journal creation post Revaluation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.query_builder`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.test.accounts_mixin`
- `erpnext.accounts.doctype.exchange_rate_revaluation.exchange_rate_revaluation`


## Step-by-Step Guide

### Step 1: '\n\t\tTest Forex account balance and Journal creation post Revaluation\n\t\t'

```python
'\n\t\tTest Forex account balance and Journal creation post Revaluation\n\t\t'
```

### Step 2: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
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

### Step 6: Assign err = frappe.new_doc(...)

```python
err = frappe.new_doc('Exchange Rate Revaluation')
```

### Step 7: Assign err.company = value

```python
err.company = self.company
```

### Step 8: Assign err.posting_date = today(...)

```python
err.posting_date = today()
```

### Step 9: Assign accounts = err.get_accounts_data(...)

```python
accounts = err.get_accounts_data()
```

### Step 10: Call err.extend()

```python
err.extend('accounts', accounts)
```

### Step 11: Assign row = value

```python
row = err.accounts[0]
```

### Step 12: Assign row.new_exchange_rate = 85

```python
row.new_exchange_rate = 85
```

### Step 13: Assign row.new_balance_in_base_currency = flt(...)

```python
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
```

### Step 14: Assign row.gain_loss = value

```python
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
```

### Step 15: Call err.set_total_gain_loss()

```python
err.set_total_gain_loss()
```

### Step 16: Assign err = err.save.submit(...)

```python
err = err.save().submit()
```

### Step 17: Assign err_journals = err.make_jv_entries(...)

```python
err_journals = err.make_jv_entries()
```

### Step 18: Assign je = frappe.get_doc(...)

```python
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
```

### Step 19: Assign je = je.submit(...)

```python
je = je.submit()
```

### Step 20: Call je.reload()

```python
je.reload()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(je.total_debit, 8500.0)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(je.total_credit, 8500.0)
```

### Step 24: Assign gl = DocType(...)

```python
gl = DocType('GL Entry')
```

### Step 25: Assign acc_balance = value

```python
acc_balance = frappe.db.get_all('GL Entry', filters={'account': self.debtors_usd, 'is_cancelled': 0}, fields=[(functions.Sum(gl.debit) - functions.Sum(gl.credit)).as_('balance')])[0]
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(acc_balance.balance, 8500.0)
```


## Complete Example

```python
# Workflow
'\n\t\tTest Forex account balance and Journal creation post Revaluation\n\t\t'
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
err = frappe.new_doc('Exchange Rate Revaluation')
err.company = self.company
err.posting_date = today()
accounts = err.get_accounts_data()
err.extend('accounts', accounts)
row = err.accounts[0]
row.new_exchange_rate = 85
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
err.set_total_gain_loss()
err = err.save().submit()
err_journals = err.make_jv_entries()
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
je = je.submit()
je.reload()
self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')
self.assertEqual(je.total_debit, 8500.0)
self.assertEqual(je.total_credit, 8500.0)
gl = DocType('GL Entry')
acc_balance = frappe.db.get_all('GL Entry', filters={'account': self.debtors_usd, 'is_cancelled': 0}, fields=[(functions.Sum(gl.debit) - functions.Sum(gl.credit)).as_('balance')])[0]
self.assertEqual(acc_balance.balance, 8500.0)
```

## Next Steps


---

*Source: test_exchange_rate_revaluation.py:44 | Complexity: Advanced | Last updated: 2026-02-03*