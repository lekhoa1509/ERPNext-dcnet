# How To: Add Account To A Group

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add account to a group

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

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Account', 'Office Rent - _TC3', 'is_group', 1)
```

### Step 2: Assign acc = frappe.new_doc(...)

```python
acc = frappe.new_doc('Account')
```

### Step 3: Assign acc.account_name = 'Test Group Account'

```python
acc.account_name = 'Test Group Account'
```

### Step 4: Assign acc.parent_account = 'Office Rent - _TC3'

```python
acc.parent_account = 'Office Rent - _TC3'
```

### Step 5: Assign acc.company = '_Test Company 3'

```python
acc.company = '_Test Company 3'
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, acc.insert)
```

### Step 7: Call frappe.db.set_value()

```python
frappe.db.set_value('Account', 'Office Rent - _TC3', 'is_group', 0)
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Account', 'Office Rent - _TC3', 'is_group', 1)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Group Account'
acc.parent_account = 'Office Rent - _TC3'
acc.company = '_Test Company 3'
self.assertRaises(frappe.ValidationError, acc.insert)
frappe.db.set_value('Account', 'Office Rent - _TC3', 'is_group', 0)
```

## Next Steps


---

*Source: test_account.py:149 | Complexity: Intermediate | Last updated: 2026-02-03*