# How To: Validate Account Currency

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test validate account currency

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

### Step 1: Call self.assertEqual()

```python
self.assertEqual(acc.account_currency, 'INR')
```

### Step 2: Call make_journal_entry()

```python
make_journal_entry('Test Currency Account - _TC', 'Miscellaneous Expenses - _TC', 100, submit=True)
```

### Step 3: Assign acc.account_currency = 'USD'

```python
acc.account_currency = 'USD'
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, acc.save)
```

### Step 5: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 6: Assign acc.account_name = 'Test Currency Account'

```python
acc.account_name = 'Test Currency Account'
```

### Step 7: Assign acc.parent_account = 'Tax Assets - _TC'

```python
acc.parent_account = 'Tax Assets - _TC'
```

### Step 8: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 9: Call acc.insert()

```python
acc.insert()
```

### Step 10: Assign acc = frappe.get_doc(...)

```python
acc = frappe.get_doc('Account', 'Test Currency Account - _TC')
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.journal_entry.test_journal_entry import make_journal_entry
if not frappe.db.get_value('Account', 'Test Currency Account - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Test Currency Account'
    acc.parent_account = 'Tax Assets - _TC'
    acc.company = '_Test Company'
    acc.insert()
else:
    acc = frappe.get_doc('Account', 'Test Currency Account - _TC')
self.assertEqual(acc.account_currency, 'INR')
make_journal_entry('Test Currency Account - _TC', 'Miscellaneous Expenses - _TC', 100, submit=True)
acc.account_currency = 'USD'
self.assertRaises(frappe.ValidationError, acc.save)
```

## Next Steps


---

*Source: test_account.py:291 | Complexity: Advanced | Last updated: 2026-02-03*