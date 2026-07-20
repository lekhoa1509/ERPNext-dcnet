# How To: Jv Account And Party Balance With Cost Centre

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test jv account and party balance with cost centre

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.exceptions`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.journal_entry.journal_entry`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.projects.doctype.project.test_project`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.general_ledger`
- `erpnext.accounts.general_ledger`


## Step-by-Step Guide

### Step 1: Assign cost_center = '_Test Cost Center for BS Account - _TC'

```python
cost_center = '_Test Cost Center for BS Account - _TC'
```

### Step 2: Call create_cost_center()

```python
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
```

### Step 3: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, cost_center=cost_center, save=False)
```

### Step 4: Assign account_balance = get_balance_on(...)

```python
account_balance = get_balance_on(account='_Test Bank - _TC', cost_center=cost_center)
```

### Step 5: Assign jv.voucher_type = 'Bank Entry'

```python
jv.voucher_type = 'Bank Entry'
```

### Step 6: Assign jv.multi_currency = 0

```python
jv.multi_currency = 0
```

### Step 7: Assign jv.cheque_no = '112233'

```python
jv.cheque_no = '112233'
```

### Step 8: Assign jv.cheque_date = nowdate(...)

```python
jv.cheque_date = nowdate()
```

### Step 9: Call jv.insert()

```python
jv.insert()
```

### Step 10: Call jv.submit()

```python
jv.submit()
```

### Step 11: Assign expected_account_balance = value

```python
expected_account_balance = account_balance - 100
```

### Step 12: Assign account_balance = get_balance_on(...)

```python
account_balance = get_balance_on(account='_Test Bank - _TC', cost_center=cost_center)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(expected_account_balance, account_balance)
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_balance_on
cost_center = '_Test Cost Center for BS Account - _TC'
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, cost_center=cost_center, save=False)
account_balance = get_balance_on(account='_Test Bank - _TC', cost_center=cost_center)
jv.voucher_type = 'Bank Entry'
jv.multi_currency = 0
jv.cheque_no = '112233'
jv.cheque_date = nowdate()
jv.insert()
jv.submit()
expected_account_balance = account_balance - 100
account_balance = get_balance_on(account='_Test Bank - _TC', cost_center=cost_center)
self.assertEqual(expected_account_balance, account_balance)
```

## Next Steps


---

*Source: test_journal_entry.py:391 | Complexity: Advanced | Last updated: 2026-02-03*