# How To: Rename Account

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test rename account

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

### Step 1: Assign unknown = frappe.db.get_value(...)

```python
account_number, account_name = frappe.db.get_value('Account', '1210 - Debtors - _TC', ['account_number', 'account_name'])
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(account_number, '1210')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(account_name, 'Debtors')
```

### Step 4: Assign new_account_number = '1211-11-4 - 6 - '

```python
new_account_number = '1211-11-4 - 6 - '
```

### Step 5: Assign new_account_name = 'Debtors 1 - Test - '

```python
new_account_name = 'Debtors 1 - Test - '
```

### Step 6: Call update_account_number()

```python
update_account_number('1210 - Debtors - _TC', new_account_name, new_account_number)
```

### Step 7: Assign new_acc = frappe.db.get_value(...)

```python
new_acc = frappe.db.get_value('Account', '1211-11-4 - 6 - - Debtors 1 - Test - - _TC', ['account_name', 'account_number'], as_dict=1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(new_acc.account_name, 'Debtors 1 - Test -')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(new_acc.account_number, '1211-11-4 - 6 -')
```

### Step 10: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '1211-11-4 - 6 - Debtors 1 - Test - - _TC')
```

### Step 11: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 12: Assign acc.account_name = 'Debtors'

```python
acc.account_name = 'Debtors'
```

### Step 13: Assign acc.parent_account = 'Accounts Receivable - _TC'

```python
acc.parent_account = 'Accounts Receivable - _TC'
```

### Step 14: Assign acc.account_number = '1210'

```python
acc.account_number = '1210'
```

### Step 15: Assign acc.company = '_Test Company'

```python
acc.company = '_Test Company'
```

### Step 16: Call acc.insert()

```python
acc.insert()
```


## Complete Example

```python
# Workflow
if not frappe.db.exists('Account', '1210 - Debtors - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Debtors'
    acc.parent_account = 'Accounts Receivable - _TC'
    acc.account_number = '1210'
    acc.company = '_Test Company'
    acc.insert()
account_number, account_name = frappe.db.get_value('Account', '1210 - Debtors - _TC', ['account_number', 'account_name'])
self.assertEqual(account_number, '1210')
self.assertEqual(account_name, 'Debtors')
new_account_number = '1211-11-4 - 6 - '
new_account_name = 'Debtors 1 - Test - '
update_account_number('1210 - Debtors - _TC', new_account_name, new_account_number)
new_acc = frappe.db.get_value('Account', '1211-11-4 - 6 - - Debtors 1 - Test - - _TC', ['account_name', 'account_number'], as_dict=1)
self.assertEqual(new_acc.account_name, 'Debtors 1 - Test -')
self.assertEqual(new_acc.account_number, '1211-11-4 - 6 -')
frappe.delete_doc('Account', '1211-11-4 - 6 - Debtors 1 - Test - - _TC')
```

## Next Steps


---

*Source: test_account.py:19 | Complexity: Advanced | Last updated: 2026-02-03*