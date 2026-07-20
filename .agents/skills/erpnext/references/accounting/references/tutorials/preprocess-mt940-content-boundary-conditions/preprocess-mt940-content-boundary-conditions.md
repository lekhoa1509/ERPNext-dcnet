# How To: Preprocess Mt940 Content Boundary Conditions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test boundary conditions for statement number length

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test boundary conditions for statement number length'

```python
'Test boundary conditions for statement number length'
```

### Step 2: Assign mt940_content = ':28C:123456/1'

```python
mt940_content = ':28C:123456/1'
```

### Step 3: Assign expected_content = ':28C:23456/1'

```python
expected_content = ':28C:23456/1'
```

### Step 4: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result, expected_content)
```

### Step 6: Assign mt940_content = ':28C:12345/1'

```python
mt940_content = ':28C:12345/1'
```

### Step 7: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(result, mt940_content)
```

### Step 9: Assign mt940_content = ':28C:123456789012345/1'

```python
mt940_content = ':28C:123456789012345/1'
```

### Step 10: Assign expected_content = ':28C:12345/1'

```python
expected_content = ':28C:12345/1'
```

### Step 11: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(result, expected_content)
```


## Complete Example

```python
# Workflow
'Test boundary conditions for statement number length'
mt940_content = ':28C:123456/1'
expected_content = ':28C:23456/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
mt940_content = ':28C:12345/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
mt940_content = ':28C:123456789012345/1'
expected_content = ':28C:12345/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:110 | Complexity: Advanced | Last updated: 2026-02-03*