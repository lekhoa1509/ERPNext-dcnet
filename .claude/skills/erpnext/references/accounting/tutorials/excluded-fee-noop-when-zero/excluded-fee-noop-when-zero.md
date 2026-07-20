# How To: Excluded Fee Noop When Zero

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: When there is no excluded fee to apply, the amounts should remain
unchanged.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'When there is no excluded fee to apply, the amounts should remain\n\t\tunchanged.'

```python
'When there is no excluded fee to apply, the amounts should remain\n\t\tunchanged.'
```

### Step 2: Assign bt = frappe.new_doc(...)

```python
bt = frappe.new_doc('Bank Transaction')
```

### Step 3: Assign bt.deposit = 100

```python
bt.deposit = 100
```

### Step 4: Assign bt.withdrawal = 0

```python
bt.withdrawal = 0
```

### Step 5: Assign bt.included_fee = 5

```python
bt.included_fee = 5
```

### Step 6: Assign bt.excluded_fee = 0

```python
bt.excluded_fee = 0
```

### Step 7: Call bt.handle_excluded_fee()

```python
bt.handle_excluded_fee()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(bt.deposit, 100)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(bt.withdrawal, 0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(bt.included_fee, 5)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(bt.excluded_fee, 0)
```


## Complete Example

```python
# Workflow
'When there is no excluded fee to apply, the amounts should remain\n\t\tunchanged.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 100
bt.withdrawal = 0
bt.included_fee = 5
bt.excluded_fee = 0
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 100)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

## Next Steps


---

*Source: test_bank_transaction_fees.py:36 | Complexity: Advanced | Last updated: 2026-02-03*