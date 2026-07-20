# How To: Preprocess Mt940 Content Whitespace Variants

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test handling of whitespace and different line endings

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test handling of whitespace and different line endings'

```python
'Test handling of whitespace and different line endings'
```

### Step 2: Assign mt940_content = ':28C:167619/1   \n'

```python
mt940_content = ':28C:167619/1   \n'
```

### Step 3: Assign expected_content = ':28C:67619/1   \n'

```python
expected_content = ':28C:67619/1   \n'
```

### Step 4: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result, expected_content)
```

### Step 6: Assign mt940_content = ':28C:167619/1\r\n'

```python
mt940_content = ':28C:167619/1\r\n'
```

### Step 7: Assign expected_content = ':28C:67619/1\r\n'

```python
expected_content = ':28C:67619/1\r\n'
```

### Step 8: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(result, expected_content)
```

### Step 10: Assign mt940_content = '   :28C:167619/1\n'

```python
mt940_content = '   :28C:167619/1\n'
```

### Step 11: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(result, mt940_content)
```


## Complete Example

```python
# Workflow
'Test handling of whitespace and different line endings'
mt940_content = ':28C:167619/1   \n'
expected_content = ':28C:67619/1   \n'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
mt940_content = ':28C:167619/1\r\n'
expected_content = ':28C:67619/1\r\n'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
mt940_content = '   :28C:167619/1\n'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:192 | Complexity: Advanced | Last updated: 2026-02-03*