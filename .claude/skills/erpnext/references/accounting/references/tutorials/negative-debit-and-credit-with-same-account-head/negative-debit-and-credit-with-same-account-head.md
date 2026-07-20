# How To: Negative Debit And Credit With Same Account Head

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test negative debit and credit with same account head

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

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Accounts Settings', 'merge_similar_account_heads', 0)
```

### Step 2: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Bank - _TC', '_Test Bank - _TC', 100 * -1, save=True)
```

### Step 3: Call jv.append()

```python
jv.append('accounts', {'account': '_Test Cash - _TC', 'debit': 100 * -1, 'credit': 100 * -1, 'debit_in_account_currency': 100 * -1, 'credit_in_account_currency': 100 * -1, 'exchange_rate': 1})
```

### Step 4: Assign jv.flags.ignore_validate = True

```python
jv.flags.ignore_validate = True
```

### Step 5: Call jv.save()

```python
jv.save()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(jv.accounts), 3)
```

### Step 7: Assign gl_map = jv.build_gl_map(...)

```python
gl_map = jv.build_gl_map()
```

### Step 8: Assign gl_map = process_gl_map(...)

```python
gl_map = process_gl_map(gl_map, False)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(row.debit_in_account_currency, 100 * -1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(row.credit_in_account_currency, 100 * -1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(row.debit_in_account_currency, 100)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(row.credit_in_account_currency, 100)
```


## Complete Example

```python
# Workflow
from erpnext.accounts.general_ledger import process_gl_map
frappe.db.set_single_value('Accounts Settings', 'merge_similar_account_heads', 0)
jv = make_journal_entry('_Test Bank - _TC', '_Test Bank - _TC', 100 * -1, save=True)
jv.append('accounts', {'account': '_Test Cash - _TC', 'debit': 100 * -1, 'credit': 100 * -1, 'debit_in_account_currency': 100 * -1, 'credit_in_account_currency': 100 * -1, 'exchange_rate': 1})
jv.flags.ignore_validate = True
jv.save()
self.assertEqual(len(jv.accounts), 3)
gl_map = jv.build_gl_map()
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.debit_in_account_currency, 100 * -1)
        self.assertEqual(row.credit_in_account_currency, 100 * -1)
gl_map = process_gl_map(gl_map, False)
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.debit_in_account_currency, 100)
        self.assertEqual(row.credit_in_account_currency, 100)
```

## Next Steps


---

*Source: test_journal_entry.py:480 | Complexity: Advanced | Last updated: 2026-02-03*