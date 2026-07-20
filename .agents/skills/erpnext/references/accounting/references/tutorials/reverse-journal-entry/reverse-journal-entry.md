# How To: Reverse Journal Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reverse journal entry

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

### Step 1: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Bank USD - _TC', 'Sales - _TC', 100, exchange_rate=50, save=False)
```

### Step 2: Assign unknown.credit_in_account_currency = 5000

```python
jv.get('accounts')[1].credit_in_account_currency = 5000
```

### Step 3: Assign unknown.exchange_rate = 1

```python
jv.get('accounts')[1].exchange_rate = 1
```

### Step 4: Call jv.submit()

```python
jv.submit()
```

### Step 5: Assign rjv = make_reverse_journal_entry(...)

```python
rjv = make_reverse_journal_entry(jv.name)
```

### Step 6: Assign rjv.posting_date = nowdate(...)

```python
rjv.posting_date = nowdate()
```

### Step 7: Call rjv.submit()

```python
rjv.submit()
```

### Step 8: Assign self.voucher_no = value

```python
self.voucher_no = rjv.name
```

### Step 9: Assign self.fields = value

```python
self.fields = ['account', 'account_currency', 'debit', 'credit', 'debit_in_account_currency', 'credit_in_account_currency']
```

### Step 10: Assign self.expected_gle = value

```python
self.expected_gle = [{'account': '_Test Bank USD - _TC', 'account_currency': 'USD', 'debit': 0, 'debit_in_account_currency': 0, 'credit': 5000, 'credit_in_account_currency': 100}, {'account': 'Sales - _TC', 'account_currency': 'INR', 'debit': 5000, 'debit_in_account_currency': 5000, 'credit': 0, 'credit_in_account_currency': 0}]
```

### Step 11: Call self.check_gl_entries()

```python
self.check_gl_entries()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.journal_entry.journal_entry import make_reverse_journal_entry
jv = make_journal_entry('_Test Bank USD - _TC', 'Sales - _TC', 100, exchange_rate=50, save=False)
jv.get('accounts')[1].credit_in_account_currency = 5000
jv.get('accounts')[1].exchange_rate = 1
jv.submit()
rjv = make_reverse_journal_entry(jv.name)
rjv.posting_date = nowdate()
rjv.submit()
self.voucher_no = rjv.name
self.fields = ['account', 'account_currency', 'debit', 'credit', 'debit_in_account_currency', 'credit_in_account_currency']
self.expected_gle = [{'account': '_Test Bank USD - _TC', 'account_currency': 'USD', 'debit': 0, 'debit_in_account_currency': 0, 'credit': 5000, 'credit_in_account_currency': 100}, {'account': 'Sales - _TC', 'account_currency': 'INR', 'debit': 5000, 'debit_in_account_currency': 5000, 'credit': 0, 'credit_in_account_currency': 0}]
self.check_gl_entries()
```

## Next Steps


---

*Source: test_journal_entry.py:206 | Complexity: Advanced | Last updated: 2026-02-03*