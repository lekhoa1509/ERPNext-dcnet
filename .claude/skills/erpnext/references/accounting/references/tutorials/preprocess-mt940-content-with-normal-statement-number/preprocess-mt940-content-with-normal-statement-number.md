# How To: Preprocess Mt940 Content With Normal Statement Number

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test that statement numbers with 5 or fewer digits are unchanged

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test that statement numbers with 5 or fewer digits are unchanged'

```python
'Test that statement numbers with 5 or fewer digits are unchanged'
```

### Step 2: Assign mt940_content = ':28C:12345/1'

```python
mt940_content = ':28C:12345/1'
```

### Step 3: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(result, mt940_content)
```

### Step 5: Assign mt940_content = ':28C:1234/1'

```python
mt940_content = ':28C:1234/1'
```

### Step 6: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result, mt940_content)
```


## Complete Example

```python
# Workflow
'Test that statement numbers with 5 or fewer digits are unchanged'
mt940_content = ':28C:12345/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
mt940_content = ':28C:1234/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:23 | Complexity: Intermediate | Last updated: 2026-02-03*