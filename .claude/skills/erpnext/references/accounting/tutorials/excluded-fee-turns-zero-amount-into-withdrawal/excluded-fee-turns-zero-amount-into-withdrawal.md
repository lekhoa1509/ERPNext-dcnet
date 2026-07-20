# How To: Excluded Fee Turns Zero Amount Into Withdrawal

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: If only an excluded fee is provided, it should be treated as an
outgoing payment and the fee is then tracked as included.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'If only an excluded fee is provided, it should be treated as an\n\t\toutgoing payment and the fee is then tracked as included.'

```python
'If only an excluded fee is provided, it should be treated as an\n\t\toutgoing payment and the fee is then tracked as included.'
```

### Step 2: Assign bt = frappe.new_doc(...)

```python
bt = frappe.new_doc('Bank Transaction')
```

### Step 3: Assign bt.deposit = 0

```python
bt.deposit = 0
```

### Step 4: Assign bt.withdrawal = 0

```python
bt.withdrawal = 0
```

### Step 5: Assign bt.included_fee = 0

```python
bt.included_fee = 0
```

### Step 6: Assign bt.excluded_fee = 5

```python
bt.excluded_fee = 5
```

### Step 7: Call bt.handle_excluded_fee()

```python
bt.handle_excluded_fee()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(bt.deposit, 0)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(bt.withdrawal, 5)
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
'If only an excluded fee is provided, it should be treated as an\n\t\toutgoing payment and the fee is then tracked as included.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 0
bt.withdrawal = 0
bt.included_fee = 0
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 5)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

## Next Steps


---

*Source: test_bank_transaction_fees.py:119 | Complexity: Advanced | Last updated: 2026-02-03*