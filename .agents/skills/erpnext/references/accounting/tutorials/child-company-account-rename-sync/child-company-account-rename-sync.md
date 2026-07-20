# How To: Child Company Account Rename Sync

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test child company account rename sync

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

### Step 3: Assign acc.account_name = 'Test Group Account'

```python
acc.account_name = 'Test Group Account'
```

### Step 4: Assign acc.parent_account = 'Temporary Accounts - _TC3'

```python
acc.parent_account = 'Temporary Accounts - _TC3'
```

### Step 5: Assign acc.is_group = 1

```python
acc.is_group = 1
```

### Step 6: Assign acc.company = '_Test Company 3'

```python
acc.company = '_Test Company 3'
```

### Step 7: Call acc.insert()

```python
acc.insert()
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 4'}))
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 5'}))
```

### Step 10: Assign acc_tc_5 = frappe.db.get_value(...)

```python
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 5'})
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, update_account_number, acc_tc_5, 'Test Modified Account')
```

### Step 12: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company 5', 'allow_account_creation_against_child_company', 1)
```

### Step 13: Call update_account_number()

```python
update_account_number(acc_tc_5, 'Test Modified Account')
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Account', {'name': 'Test Modified Account - _TC5', 'company': '_Test Company 5'}))
```

### Step 15: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company 5', 'allow_account_creation_against_child_company', 0)
```

### Step 16: Assign to_delete = value

```python
to_delete = ['Test Group Account - _TC3', 'Test Group Account - _TC4', 'Test Modified Account - _TC5']
```

### Step 17: Call frappe.delete_doc()

```python
frappe.delete_doc('Account', doc)
```


## Complete Example

```python
# Workflow
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Group Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.is_group = 1
acc.company = '_Test Company 3'
acc.insert()
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 4'}))
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 5'}))
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 5'})
self.assertRaises(frappe.ValidationError, update_account_number, acc_tc_5, 'Test Modified Account')
frappe.db.set_value('Company', '_Test Company 5', 'allow_account_creation_against_child_company', 1)
update_account_number(acc_tc_5, 'Test Modified Account')
self.assertTrue(frappe.db.exists('Account', {'name': 'Test Modified Account - _TC5', 'company': '_Test Company 5'}))
frappe.db.set_value('Company', '_Test Company 5', 'allow_account_creation_against_child_company', 0)
to_delete = ['Test Group Account - _TC3', 'Test Group Account - _TC4', 'Test Modified Account - _TC5']
for doc in to_delete:
    frappe.delete_doc('Account', doc)
```

## Next Steps


---

*Source: test_account.py:248 | Complexity: Advanced | Last updated: 2026-02-03*