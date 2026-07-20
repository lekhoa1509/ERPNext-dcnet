# How To: Repost Accounting Entries

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test repost accounting entries

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

### Step 1: Assign settings = frappe.get_doc(...)

```python
settings = frappe.get_doc('Repost Accounting Ledger Settings')
```

### Step 2: Call settings.save()

```python
settings.save()
```

### Step 3: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, save=False)
```

### Step 4: Assign jv.multi_currency = 0

```python
jv.multi_currency = 0
```

### Step 5: Call jv.submit()

```python
jv.submit()
```

### Step 6: Assign self.voucher_no = value

```python
self.voucher_no = jv.name
```

### Step 7: Assign self.fields = value

```python
self.fields = ['account', 'debit_in_account_currency', 'credit_in_account_currency', 'cost_center']
```

### Step 8: Assign self.expected_gle = value

```python
self.expected_gle = [{'account': '_Test Bank - _TC', 'debit_in_account_currency': 0, 'credit_in_account_currency': 100, 'cost_center': '_Test Cost Center - _TC'}, {'account': '_Test Cash - _TC', 'debit_in_account_currency': 100, 'credit_in_account_currency': 0, 'cost_center': '_Test Cost Center - _TC'}]
```

### Step 9: Call self.check_gl_entries()

```python
self.check_gl_entries()
```

### Step 10: Call create_cost_center()

```python
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
```

### Step 11: Assign unknown.cost_center = '_Test Cost Center for BS Account - _TC'

```python
jv.accounts[1].cost_center = '_Test Cost Center for BS Account - _TC'
```

### Step 12: Call jv.save()

```python
jv.save()
```

### Step 13: Call jv.load_from_db()

```python
jv.load_from_db()
```

### Step 14: Assign unknown = '_Test Cost Center for BS Account - _TC'

```python
self.expected_gle[0]['cost_center'] = '_Test Cost Center for BS Account - _TC'
```

### Step 15: Call self.check_gl_entries()

```python
self.check_gl_entries()
```

### Step 16: Call settings.append()

```python
settings.append('allowed_types', {'document_type': 'Journal Entry', 'allowed': True})
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
settings = frappe.get_doc('Repost Accounting Ledger Settings')
if not [x for x in settings.allowed_types if x.document_type == 'Journal Entry']:
    settings.append('allowed_types', {'document_type': 'Journal Entry', 'allowed': True})
settings.save()
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, save=False)
jv.multi_currency = 0
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'debit_in_account_currency', 'credit_in_account_currency', 'cost_center']
self.expected_gle = [{'account': '_Test Bank - _TC', 'debit_in_account_currency': 0, 'credit_in_account_currency': 100, 'cost_center': '_Test Cost Center - _TC'}, {'account': '_Test Cash - _TC', 'debit_in_account_currency': 100, 'credit_in_account_currency': 0, 'cost_center': '_Test Cost Center - _TC'}]
self.check_gl_entries()
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
jv.accounts[1].cost_center = '_Test Cost Center for BS Account - _TC'
jv.save()
jv.load_from_db()
self.expected_gle[0]['cost_center'] = '_Test Cost Center for BS Account - _TC'
self.check_gl_entries()
```

## Next Steps


---

*Source: test_journal_entry.py:412 | Complexity: Advanced | Last updated: 2026-02-03*