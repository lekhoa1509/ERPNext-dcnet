# How To: Account Rename Sync

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test account rename sync

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

### Step 1: Call frappe.local.flags.pop()

```python
frappe.local.flags.pop('ignore_root_company_validation', None)
```

### Step 2: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 3: Assign acc.account_name = 'Test Rename Account'

```python
acc.account_name = 'Test Rename Account'
```

### Step 4: Assign acc.parent_account = 'Temporary Accounts - _TC3'

```python
acc.parent_account = 'Temporary Accounts - _TC3'
```

### Step 5: Assign acc.company = '_Test Company 3'

```python
acc.company = '_Test Company 3'
```

### Step 6: Call acc.insert()

```python
acc.insert()
```

### Step 7: Call update_account_number()

```python
update_account_number(acc.name, 'Test Rename Sync Account', '1234')
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 4', 'account_number': '1234'}))
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 5', 'account_number': '1234'}))
```

### Step 10: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC3')
```

### Step 11: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC4')
```

### Step 12: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC5')
```


## Complete Example

```python
# Workflow
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Rename Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.company = '_Test Company 3'
acc.insert()
update_account_number(acc.name, 'Test Rename Sync Account', '1234')
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 4', 'account_number': '1234'}))
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 5', 'account_number': '1234'}))
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC3')
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC4')
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC5')
```

## Next Steps


---

*Source: test_account.py:160 | Complexity: Advanced | Last updated: 2026-02-03*