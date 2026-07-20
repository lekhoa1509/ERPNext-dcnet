# How To: Jv Against Stock Account

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test jv against stock account

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

### Step 1: Assign company = '_Test Company with perpetual inventory'

```python
company = '_Test Company with perpetual inventory'
```

### Step 2: Assign stock_account = get_inventory_account(...)

```python
stock_account = get_inventory_account(company)
```

### Step 3: Assign unknown = get_stock_and_account_balance(...)

```python
account_bal, stock_bal, warehouse_list = get_stock_and_account_balance(stock_account, nowdate(), company)
```

### Step 4: Assign diff = value

```python
diff = flt(account_bal) - flt(stock_bal)
```

### Step 5: Assign jv = frappe.new_doc(...)

```python
jv = frappe.new_doc('Journal Entry')
```

### Step 6: Assign jv.company = company

```python
jv.company = company
```

### Step 7: Assign jv.posting_date = nowdate(...)

```python
jv.posting_date = nowdate()
```

### Step 8: Call jv.append()

```python
jv.append('accounts', {'account': stock_account, 'cost_center': 'Main - TCP1', 'debit_in_account_currency': 0 if diff > 0 else abs(diff), 'credit_in_account_currency': diff if diff > 0 else 0})
```

### Step 9: Call jv.append()

```python
jv.append('accounts', {'account': 'Stock Adjustment - TCP1', 'cost_center': 'Main - TCP1', 'debit_in_account_currency': diff if diff > 0 else 0, 'credit_in_account_currency': 0 if diff > 0 else abs(diff)})
```

### Step 10: Assign diff = 100

```python
diff = 100
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(StockAccountInvalidTransaction, jv.save)
```

### Step 12: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 13: Call jv.submit()

```python
jv.submit()
```

### Step 14: Call jv.cancel()

```python
jv.cancel()
```


## Complete Example

```python
# Workflow
company = '_Test Company with perpetual inventory'
stock_account = get_inventory_account(company)
from erpnext.accounts.utils import get_stock_and_account_balance
account_bal, stock_bal, warehouse_list = get_stock_and_account_balance(stock_account, nowdate(), company)
diff = flt(account_bal) - flt(stock_bal)
if not diff:
    diff = 100
jv = frappe.new_doc('Journal Entry')
jv.company = company
jv.posting_date = nowdate()
jv.append('accounts', {'account': stock_account, 'cost_center': 'Main - TCP1', 'debit_in_account_currency': 0 if diff > 0 else abs(diff), 'credit_in_account_currency': diff if diff > 0 else 0})
jv.append('accounts', {'account': 'Stock Adjustment - TCP1', 'cost_center': 'Main - TCP1', 'debit_in_account_currency': diff if diff > 0 else 0, 'credit_in_account_currency': 0 if diff > 0 else abs(diff)})
if account_bal == stock_bal:
    self.assertRaises(StockAccountInvalidTransaction, jv.save)
    frappe.db.rollback()
else:
    jv.submit()
    jv.cancel()
```

## Next Steps


---

*Source: test_journal_entry.py:113 | Complexity: Advanced | Last updated: 2026-02-03*