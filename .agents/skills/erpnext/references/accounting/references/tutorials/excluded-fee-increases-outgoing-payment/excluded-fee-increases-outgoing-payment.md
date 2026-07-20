# How To: Excluded Fee Increases Outgoing Payment

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: When a separately-deducted fee is provided for an outgoing payment,
the total money leaving increases and the fee is tracked.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'When a separately-deducted fee is provided for an outgoing payment,\n\t\tthe total money leaving increases and the fee is tracked.'

```python
'When a separately-deducted fee is provided for an outgoing payment,\n\t\tthe total money leaving increases and the fee is tracked.'
```

### Step 2: Assign bt = frappe.new_doc(...)

```python
bt = frappe.new_doc('Bank Transaction')
```

### Step 3: Assign bt.deposit = 0

```python
bt.deposit = 0
```

### Step 4: Assign bt.withdrawal = 100

```python
bt.withdrawal = 100
```

### Step 5: Assign bt.included_fee = 2

```python
bt.included_fee = 2
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
self.assertEqual(bt.withdrawal, 105)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(bt.included_fee, 7)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(bt.excluded_fee, 0)
```


## Complete Example

```python
# Workflow
'When a separately-deducted fee is provided for an outgoing payment,\n\t\tthe total money leaving increases and the fee is tracked.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 0
bt.withdrawal = 100
bt.included_fee = 2
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 105)
self.assertEqual(bt.included_fee, 7)
self.assertEqual(bt.excluded_fee, 0)
```

## Next Steps


---

*Source: test_bank_transaction_fees.py:103 | Complexity: Advanced | Last updated: 2026-02-03*