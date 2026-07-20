# How To: Preprocess Mt940 Content Edge Cases

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test edge cases like empty content and content without :28C: tags

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test edge cases like empty content and content without :28C: tags'

```python
'Test edge cases like empty content and content without :28C: tags'
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(preprocess_mt940_content(''), '')
```

### Step 3: Assign content_without_28c = ':20:STARTUMSE\n:25:12345678901234567890\n:60F:C031002EUR0,00'

```python
content_without_28c = ':20:STARTUMSE\n:25:12345678901234567890\n:60F:C031002EUR0,00'
```

### Step 4: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(content_without_28c)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result, content_without_28c)
```


## Complete Example

```python
# Workflow
'Test edge cases like empty content and content without :28C: tags'
self.assertEqual(preprocess_mt940_content(''), '')
content_without_28c = ':20:STARTUMSE\n:25:12345678901234567890\n:60F:C031002EUR0,00'
result = preprocess_mt940_content(content_without_28c)
self.assertEqual(result, content_without_28c)
```

## Next Steps


---

*Source: test_bank_statement_import.py:52 | Complexity: Intermediate | Last updated: 2026-02-03*