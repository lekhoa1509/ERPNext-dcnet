# How To: Preprocess Mt940 Content With Long Statement Number

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test that statement numbers longer than 5 digits are truncated to last 5 digits

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test that statement numbers longer than 5 digits are truncated to last 5 digits'

```python
'Test that statement numbers longer than 5 digits are truncated to last 5 digits'
```

### Step 2: Assign mt940_content = ':28C:167619/1'

```python
mt940_content = ':28C:167619/1'
```

### Step 3: Assign expected_content = ':28C:67619/1'

```python
expected_content = ':28C:67619/1'
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
'Test that statement numbers longer than 5 digits are truncated to last 5 digits'
mt940_content = ':28C:167619/1'
expected_content = ':28C:67619/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:15 | Complexity: Intermediate | Last updated: 2026-02-03*