# How To: Round Off Entry

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test round off entry

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.model.naming`
- `frappe.tests`
- `erpnext.accounts.doctype.gl_entry.gl_entry`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'round_off_account', '_Test Write Off - _TC')
```

### Step 2: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'round_off_cost_center', '_Test Cost Center - _TC')
```

### Step 3: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', submit=False)
```

### Step 4: Assign unknown.debit = 100.01

```python
jv.get('accounts')[0].debit = 100.01
```

### Step 5: Assign jv.flags.ignore_validate = True

```python
jv.flags.ignore_validate = True
```

### Step 6: Call jv.submit()

```python
jv.submit()
```

### Step 7: Assign round_off_entry = frappe.db.sql(...)

```python
round_off_entry = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\tand account='_Test Write Off - _TC' and cost_center='_Test Cost Center - _TC'\n\t\t\tand debit = 0 and credit = '.01'", jv.name)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(round_off_entry)
```


## Complete Example

```python
# Workflow
frappe.db.set_value('Company', '_Test Company', 'round_off_account', '_Test Write Off - _TC')
frappe.db.set_value('Company', '_Test Company', 'round_off_cost_center', '_Test Cost Center - _TC')
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', submit=False)
jv.get('accounts')[0].debit = 100.01
jv.flags.ignore_validate = True
jv.submit()
round_off_entry = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\tand account='_Test Write Off - _TC' and cost_center='_Test Cost Center - _TC'\n\t\t\tand debit = 0 and credit = '.01'", jv.name)
self.assertTrue(round_off_entry)
```

## Next Steps


---

*Source: test_gl_entry.py:13 | Complexity: Advanced | Last updated: 2026-02-03*