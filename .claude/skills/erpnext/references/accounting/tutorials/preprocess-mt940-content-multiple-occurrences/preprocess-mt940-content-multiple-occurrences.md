# How To: Preprocess Mt940 Content Multiple Occurrences

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test multiple statement numbers in the same content

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test multiple statement numbers in the same content'

```python
'Test multiple statement numbers in the same content'
```

### Step 2: Assign mt940_content = ':28C:167619/1\n:28C:987654/2'

```python
mt940_content = ':28C:167619/1\n:28C:987654/2'
```

### Step 3: Assign expected_content = ':28C:67619/1\n:28C:87654/2'

```python
expected_content = ':28C:67619/1\n:28C:87654/2'
```

### Step 4: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result, expected_content)
```


## Complete Example

```python
# Workflow
'Test multiple statement numbers in the same content'
mt940_content = ':28C:167619/1\n:28C:987654/2'
expected_content = ':28C:67619/1\n:28C:87654/2'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:43 | Complexity: Intermediate | Last updated: 2026-02-03*