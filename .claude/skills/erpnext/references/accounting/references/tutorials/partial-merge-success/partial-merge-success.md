# How To: Partial Merge Success

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test partial merge success

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.ledger_merge.ledger_merge`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Income - _TC', 'root_type'), 'account': 'Indirect Income - _TC', 'merge_accounts': [{'account': 'Indirect Test Income - _TC', 'account_name': 'Indirect Test Income'}, {'account': 'Administrative Test Income - _TC', 'account_name': 'Administrative Test Income'}]}).insert(ignore_permissions=True)
```

### Step 2: Assign parent = frappe.db.get_value(...)

```python
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(parent, 'Indirect Test Income - _TC')
```

### Step 4: Call start_merge()

```python
start_merge(doc.name)
```

### Step 5: Assign parent = frappe.db.get_value(...)

```python
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(parent, 'Indirect Income - _TC')
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))
```

### Step 9: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 10: Assign acc.account_name = 'Indirect Income'

```python
acc.account_name = 'Indirect Income'
```

### Step 11: Assign acc.is_group = 1

```python
acc.is_group = 1
```

### Step 12: Assign acc.parent_account = 'Income - _TC'

```python
acc.parent_account = 'Income - _TC'
```

### Step 13: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 14: Call acc.insert()

```python
acc.insert()
```

### Step 15: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 16: Assign acc.account_name = 'Indirect Test Income'

```python
acc.account_name = 'Indirect Test Income'
```

### Step 17: Assign acc.is_group = 1

```python
acc.is_group = 1
```

### Step 18: Assign acc.parent_account = 'Income - _TC'

```python
acc.parent_account = 'Income - _TC'
```

### Step 19: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 20: Call acc.insert()

```python
acc.insert()
```

### Step 21: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 22: Assign acc.account_name = 'Administrative Test Income'

```python
acc.account_name = 'Administrative Test Income'
```

### Step 23: Assign acc.parent_account = 'Indirect Test Income - _TC'

```python
acc.parent_account = 'Indirect Test Income - _TC'
```

### Step 24: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 25: Call acc.insert()

```python
acc.insert()
```


## Complete Example

```python
# Workflow
if not frappe.db.exists('Account', 'Indirect Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Income'
    acc.is_group = 1
    acc.parent_account = 'Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Indirect Test Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Test Income'
    acc.is_group = 1
    acc.parent_account = 'Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Administrative Test Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Administrative Test Income'
    acc.parent_account = 'Indirect Test Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Income - _TC', 'root_type'), 'account': 'Indirect Income - _TC', 'merge_accounts': [{'account': 'Indirect Test Income - _TC', 'account_name': 'Indirect Test Income'}, {'account': 'Administrative Test Income - _TC', 'account_name': 'Administrative Test Income'}]}).insert(ignore_permissions=True)
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Test Income - _TC')
start_merge(doc.name)
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Income - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))
```

## Next Steps


---

*Source: test_ledger_merge.py:55 | Complexity: Advanced | Last updated: 2026-02-03*