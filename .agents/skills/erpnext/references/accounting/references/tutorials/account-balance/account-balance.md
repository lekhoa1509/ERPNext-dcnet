# How To: Account Balance

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test account balance

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.account`
- `erpnext.stock`
- `frappe.tests.utils`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.accounts.utils`


## Step-by-Step Guide

### Step 1: Assign balance = get_balance_on(...)

```python
balance = get_balance_on(account='Test Percent Account %5 - _TC', date=nowdate())
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(balance, 0)
```

### Step 3: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 4: Assign acc.account_name = 'Test Percent Account %5'

```python
acc.account_name = 'Test Percent Account %5'
```

### Step 5: Assign acc.parent_account = 'Tax Assets - _TC'

```python
acc.parent_account = 'Tax Assets - _TC'
```

### Step 6: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 7: Call acc.insert()

```python
acc.insert()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.utils import get_balance_on
if not frappe.db.exists('Account', 'Test Percent Account %5 - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Test Percent Account %5'
    acc.parent_account = 'Tax Assets - _TC'
    acc.company = '_Test Company'
    acc.insert()
balance = get_balance_on(account='Test Percent Account %5 - _TC', date=nowdate())
self.assertEqual(balance, 0)
```

## Next Steps


---

*Source: test_account.py:311 | Complexity: Intermediate | Last updated: 2026-02-03*