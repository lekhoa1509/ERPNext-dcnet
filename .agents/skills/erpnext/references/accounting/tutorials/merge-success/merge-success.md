# How To: Merge Success

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test merge success

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.ledger_merge.ledger_merge`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Test Expenses - _TC', 'root_type'), 'account': 'Indirect Expenses - _TC', 'merge_accounts': [{'account': 'Indirect Test Expenses - _TC', 'account_name': 'Indirect Expenses'}]}).insert(ignore_permissions=True)
```

### Step 2: Assign parent = frappe.db.get_value(...)

```python
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(parent, 'Indirect Test Expenses - _TC')
```

### Step 4: Call start_merge()

```python
start_merge(doc.name)
```

### Step 5: Assign parent = frappe.db.get_value(...)

```python
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(parent, 'Indirect Expenses - _TC')
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))
```

### Step 8: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 9: Assign acc.account_name = 'Indirect Expenses'

```python
acc.account_name = 'Indirect Expenses'
```

### Step 10: Assign acc.is_group = 1

```python
acc.is_group = 1
```

### Step 11: Assign acc.parent_account = 'Expenses - _TC'

```python
acc.parent_account = 'Expenses - _TC'
```

### Step 12: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 13: Call acc.insert()

```python
acc.insert()
```

### Step 14: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 15: Assign acc.account_name = 'Indirect Test Expenses'

```python
acc.account_name = 'Indirect Test Expenses'
```

### Step 16: Assign acc.is_group = 1

```python
acc.is_group = 1
```

### Step 17: Assign acc.parent_account = 'Expenses - _TC'

```python
acc.parent_account = 'Expenses - _TC'
```

### Step 18: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 19: Call acc.insert()

```python
acc.insert()
```

### Step 20: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 21: Assign acc.account_name = 'Administrative Test Expenses'

```python
acc.account_name = 'Administrative Test Expenses'
```

### Step 22: Assign acc.parent_account = 'Indirect Test Expenses - _TC'

```python
acc.parent_account = 'Indirect Test Expenses - _TC'
```

### Step 23: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 24: Call acc.insert()

```python
acc.insert()
```


## Complete Example

```python
# Workflow
if not frappe.db.exists('Account', 'Indirect Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Expenses'
    acc.is_group = 1
    acc.parent_account = 'Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Indirect Test Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Test Expenses'
    acc.is_group = 1
    acc.parent_account = 'Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Administrative Test Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Administrative Test Expenses'
    acc.parent_account = 'Indirect Test Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Test Expenses - _TC', 'root_type'), 'account': 'Indirect Expenses - _TC', 'merge_accounts': [{'account': 'Indirect Test Expenses - _TC', 'account_name': 'Indirect Expenses'}]}).insert(ignore_permissions=True)
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Test Expenses - _TC')
start_merge(doc.name)
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Expenses - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))
```

## Next Steps


---

*Source: test_ledger_merge.py:11 | Complexity: Advanced | Last updated: 2026-02-03*