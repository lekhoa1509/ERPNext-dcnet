# How To: Multi Currency

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multi currency

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
jv = make_journal_entry('_Test Bank USD - _TC', '_Test Bank - _TC', 100, exchange_rate=50, save=False)
```

### Step 2: Assign unknown.credit_in_account_currency = 5000

```python
jv.get('accounts')[1].credit_in_account_currency = 5000
```

### Step 3: Call jv.submit()

```python
jv.submit()
```

### Step 4: Assign self.voucher_no = value

```python
self.voucher_no = jv.name
```

### Step 5: Assign self.fields = value

```python
self.fields = ['account', 'account_currency', 'debit', 'debit_in_account_currency', 'credit', 'credit_in_account_currency']
```

### Step 6: Assign self.expected_gle = value

```python
self.expected_gle = [{'account': '_Test Bank - _TC', 'account_currency': 'INR', 'debit': 0, 'debit_in_account_currency': 0, 'credit': 5000, 'credit_in_account_currency': 5000}, {'account': '_Test Bank USD - _TC', 'account_currency': 'USD', 'debit': 5000, 'debit_in_account_currency': 100, 'credit': 0, 'credit_in_account_currency': 0}]
```

### Step 7: Call self.check_gl_entries()

```python
self.check_gl_entries()
```

### Step 8: Call jv.cancel()

```python
jv.cancel()
```

### Step 9: Assign gle = frappe.db.sql(...)

```python
gle = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Sales Invoice' and voucher_no=%s", jv.name)
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(gle)
```


## Complete Example

```python
# Workflow
jv = make_journal_entry('_Test Bank USD - _TC', '_Test Bank - _TC', 100, exchange_rate=50, save=False)
jv.get('accounts')[1].credit_in_account_currency = 5000
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'account_currency', 'debit', 'debit_in_account_currency', 'credit', 'credit_in_account_currency']
self.expected_gle = [{'account': '_Test Bank - _TC', 'account_currency': 'INR', 'debit': 0, 'debit_in_account_currency': 0, 'credit': 5000, 'credit_in_account_currency': 5000}, {'account': '_Test Bank USD - _TC', 'account_currency': 'USD', 'debit': 5000, 'debit_in_account_currency': 100, 'credit': 0, 'credit_in_account_currency': 0}]
self.check_gl_entries()
jv.cancel()
gle = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Sales Invoice' and voucher_no=%s", jv.name)
self.assertFalse(gle)
```

## Next Steps


---

*Source: test_journal_entry.py:157 | Complexity: Advanced | Last updated: 2026-02-03*