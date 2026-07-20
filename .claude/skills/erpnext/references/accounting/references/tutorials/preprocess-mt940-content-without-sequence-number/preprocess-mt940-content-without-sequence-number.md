# How To: Preprocess Mt940 Content Without Sequence Number

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test statement number truncation without sequence number

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test statement number truncation without sequence number'

```python
'Test statement number truncation without sequence number'
```

### Step 2: Assign mt940_content = ':28C:987654321'

```python
mt940_content = ':28C:987654321'
```

### Step 3: Assign expected_content = ':28C:54321'

```python
expected_content = ':28C:54321'
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
'Test statement number truncation without sequence number'
mt940_content = ':28C:987654321'
expected_content = ':28C:54321'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:35 | Complexity: Intermediate | Last updated: 2026-02-03*