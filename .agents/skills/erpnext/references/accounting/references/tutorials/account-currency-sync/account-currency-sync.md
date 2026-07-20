# How To: Account Currency Sync

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: In a parent->child company setup, child should inherit parent account currency if explicitly specified.

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

### Step 1: '\n\t\tIn a parent->child company setup, child should inherit parent account currency if explicitly specified.\n\t\t'

```python
'\n\t\tIn a parent->child company setup, child should inherit parent account currency if explicitly specified.\n\t\t'
```

### Step 2: Call frappe.local.flags.pop()

```python
frappe.local.flags.pop('ignore_root_company_validation', None)
```

### Step 3: Assign acc = create_bank_account(...)

```python
acc = create_bank_account()
```

### Step 4: Assign acc.account_currency = 'JPY'

```python
acc.account_currency = 'JPY'
```

### Step 5: Call acc.insert()

```python
acc.insert()
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'JPY', 'company': '_Test Company 7'}))
```

### Step 7: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '_Test Bank JPY - _TC6')
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '_Test Bank JPY - _TC7')
```

### Step 9: Assign acc = create_bank_account(...)

```python
acc = create_bank_account()
```

### Step 10: Call acc.insert()

```python
acc.insert()
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'USD', 'company': '_Test Company 7'}))
```

### Step 12: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '_Test Bank JPY - _TC6')
```

### Step 13: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '_Test Bank JPY - _TC7')
```

### Step 14: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 15: Assign acc.account_name = '_Test Bank JPY'

```python
acc.account_name = '_Test Bank JPY'
```

### Step 16: Assign acc.parent_account = 'Temporary Accounts - _TC6'

```python
acc.parent_account = 'Temporary Accounts - _TC6'
```

### Step 17: Assign acc.company = '_Test Company 6'

```python
acc.company = '_Test Company 6'
```


## Complete Example

```python
# Workflow
'\n\t\tIn a parent->child company setup, child should inherit parent account currency if explicitly specified.\n\t\t'
frappe.local.flags.pop('ignore_root_company_validation', None)

def create_bank_account():
    acc = frappe.new_doc('Account')
    acc.account_name = '_Test Bank JPY'
    acc.parent_account = 'Temporary Accounts - _TC6'
    acc.company = '_Test Company 6'
    return acc
acc = create_bank_account()
acc.account_currency = 'JPY'
acc.insert()
self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'JPY', 'company': '_Test Company 7'}))
frappe.delete_doc('Account', '_Test Bank JPY - _TC6')
frappe.delete_doc('Account', '_Test Bank JPY - _TC7')
acc = create_bank_account()
acc.insert()
self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'USD', 'company': '_Test Company 7'}))
frappe.delete_doc('Account', '_Test Bank JPY - _TC6')
frappe.delete_doc('Account', '_Test Bank JPY - _TC7')
```

## Next Steps


---

*Source: test_account.py:198 | Complexity: Advanced | Last updated: 2026-02-03*