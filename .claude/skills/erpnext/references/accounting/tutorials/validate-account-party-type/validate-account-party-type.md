# How To: Validate Account Party Type

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test validate account party type

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.model.naming`
- `frappe.tests`
- `erpnext.accounts.doctype.gl_entry.gl_entry`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`


## Step-by-Step Guide

### Step 1: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
```

### Step 2: Call jv.save()

```python
jv.save()
```

### Step 3: Assign jv1 = make_journal_entry(...)

```python
jv1 = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
```

### Step 4: Call jv1.save()

```python
jv1.save()
```

### Step 5: Assign row.party_type = 'Supplier'

```python
row.party_type = 'Supplier'
```

### Step 6: Call jv.submit()

```python
jv.submit()
```

### Step 7: Assign row.party_type = 'Customer'

```python
row.party_type = 'Customer'
```

### Step 8: Call jv1.submit()

```python
jv1.submit()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
```


## Complete Example

```python
# Workflow
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
for row in jv.accounts:
    row.party_type = 'Supplier'
    break
jv.save()
try:
    jv.submit()
except Exception as e:
    self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
jv1 = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
for row in jv.accounts:
    row.party_type = 'Customer'
    break
jv1.save()
try:
    jv1.submit()
except Exception as e:
    self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
```

## Next Steps


---

*Source: test_gl_entry.py:81 | Complexity: Advanced | Last updated: 2026-02-03*