# How To: Account Sync

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test account sync

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

### Step 3: Assign acc.account_name = 'Test Sync Account'

```python
acc.account_name = 'Test Sync Account'
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

### Step 7: Assign acc_tc_4 = frappe.db.get_value(...)

```python
acc_tc_4 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 4'})
```

### Step 8: Assign acc_tc_5 = frappe.db.get_value(...)

```python
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 5'})
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(acc_tc_4, 'Test Sync Account - _TC4')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(acc_tc_5, 'Test Sync Account - _TC5')
```


## Complete Example

```python
# Workflow
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Sync Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.company = '_Test Company 3'
acc.insert()
acc_tc_4 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 4'})
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 5'})
self.assertEqual(acc_tc_4, 'Test Sync Account - _TC4')
self.assertEqual(acc_tc_5, 'Test Sync Account - _TC5')
```

## Next Steps


---

*Source: test_account.py:131 | Complexity: Advanced | Last updated: 2026-02-03*