# How To: Toggle Debit Credit If Negative

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test toggle debit credit if negative

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

### Step 2: Assign jv = frappe.new_doc(...)

```python
jv = frappe.new_doc('Journal Entry')
```

### Step 3: Assign jv.posting_date = nowdate(...)

```python
jv.posting_date = nowdate()
```

### Step 4: Assign jv.company = '_Test Company'

```python
jv.company = '_Test Company'
```

### Step 5: Assign jv.user_remark = 'test'

```python
jv.user_remark = 'test'
```

### Step 6: Call jv.extend()

```python
jv.extend('accounts', [{'account': '_Test Cash - _TC', 'debit': 100 * -1, 'debit_in_account_currency': 100 * -1, 'exchange_rate': 1}, {'account': '_Test Bank - _TC', 'credit': 100 * -1, 'credit_in_account_currency': 100 * -1, 'exchange_rate': 1}])
```

### Step 7: Assign jv.flags.ignore_validate = True

```python
jv.flags.ignore_validate = True
```

### Step 8: Call jv.save()

```python
jv.save()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(jv.accounts), 2)
```

### Step 10: Assign gl_map = jv.build_gl_map(...)

```python
gl_map = jv.build_gl_map()
```

### Step 11: Assign gl_map = process_gl_map(...)

```python
gl_map = process_gl_map(gl_map, False)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(row.debit, 100 * -1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(row.debit_in_account_currency, 100 * -1)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(row.debit_in_transaction_currency, 100 * -1)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(row.credit, 100)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(row.credit_in_account_currency, 100)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(row.credit_in_transaction_currency, 100)
```


## Complete Example

```python
# Workflow
from erpnext.accounts.general_ledger import process_gl_map
frappe.db.set_single_value('Accounts Settings', 'merge_similar_account_heads', 0)
jv = frappe.new_doc('Journal Entry')
jv.posting_date = nowdate()
jv.company = '_Test Company'
jv.user_remark = 'test'
jv.extend('accounts', [{'account': '_Test Cash - _TC', 'debit': 100 * -1, 'debit_in_account_currency': 100 * -1, 'exchange_rate': 1}, {'account': '_Test Bank - _TC', 'credit': 100 * -1, 'credit_in_account_currency': 100 * -1, 'exchange_rate': 1}])
jv.flags.ignore_validate = True
jv.save()
self.assertEqual(len(jv.accounts), 2)
gl_map = jv.build_gl_map()
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.debit, 100 * -1)
        self.assertEqual(row.debit_in_account_currency, 100 * -1)
        self.assertEqual(row.debit_in_transaction_currency, 100 * -1)
gl_map = process_gl_map(gl_map, False)
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.credit, 100)
        self.assertEqual(row.credit_in_account_currency, 100)
        self.assertEqual(row.credit_in_transaction_currency, 100)
```

## Next Steps


---

*Source: test_journal_entry.py:517 | Complexity: Advanced | Last updated: 2026-02-03*