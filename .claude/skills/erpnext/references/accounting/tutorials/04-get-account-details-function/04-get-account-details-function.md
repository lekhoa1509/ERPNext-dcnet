# How To: 04 Get Account Details Function

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 04 get account details function

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

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
```

### Step 2: Assign si.currency = 'USD'

```python
si.currency = 'USD'
```

### Step 3: Assign si.conversion_rate = 80

```python
si.conversion_rate = 80
```

### Step 4: Call si.save.submit()

```python
si.save().submit()
```

### Step 5: Assign account_details = get_account_details(...)

```python
account_details = get_account_details(self.company, si.posting_date, self.debtors_usd, 'Customer', self.customer, 0.05)
```

### Step 6: Assign expected_data = value

```python
expected_data = {'account_currency': 'USD', 'balance_in_base_currency': 8000.0, 'balance_in_account_currency': 100.0, 'current_exchange_rate': 80.0, 'zero_balance': False, 'new_balance_in_account_currency': 100.0}
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(expected_data.get(key), account_details.get(key))
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
from erpnext.accounts.doctype.exchange_rate_revaluation.exchange_rate_revaluation import get_account_details
account_details = get_account_details(self.company, si.posting_date, self.debtors_usd, 'Customer', self.customer, 0.05)
expected_data = {'account_currency': 'USD', 'balance_in_base_currency': 8000.0, 'balance_in_account_currency': 100.0, 'current_exchange_rate': 80.0, 'zero_balance': False, 'new_balance_in_account_currency': 100.0}
for key, _val in expected_data.items():
    self.assertEqual(expected_data.get(key), account_details.get(key))
```

## Next Steps


---

*Source: test_exchange_rate_revaluation.py:266 | Complexity: Intermediate | Last updated: 2026-02-03*