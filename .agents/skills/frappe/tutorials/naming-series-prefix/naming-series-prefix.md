# How To: Naming Series Prefix

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming series prefix

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `time`
- `uuid`
- `uuid_utils`
- `tenacity`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.model.naming`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `datetime`
- `datetime`
- `frappe.core.doctype.doctype.test_doctype`

**Setup Required:**
```python
frappe.db.delete('Note')
```

## Step-by-Step Guide

### Step 1: Assign today = now_datetime(...)

```python
today = now_datetime()
```

### Step 2: Assign year = today.strftime(...)

```python
year = today.strftime('%y')
```

### Step 3: Assign month = today.strftime(...)

```python
month = today.strftime('%m')
```

### Step 4: Assign prefix_test_cases = value

```python
prefix_test_cases = {'SINV-.YY.-.####': f'SINV-{year}-', 'SINV-.YY.-.MM.-.####': f'SINV-{year}-{month}-', 'SINV': 'SINV', 'SINV-.': 'SINV-'}
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(prefix, NamingSeries(series).get_prefix())
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
today = now_datetime()
year = today.strftime('%y')
month = today.strftime('%m')
prefix_test_cases = {'SINV-.YY.-.####': f'SINV-{year}-', 'SINV-.YY.-.MM.-.####': f'SINV-{year}-{month}-', 'SINV': 'SINV', 'SINV-.': 'SINV-'}
for series, prefix in prefix_test_cases.items():
    self.assertEqual(prefix, NamingSeries(series).get_prefix())
```

## Next Steps


---

*Source: test_naming.py:312 | Complexity: Intermediate | Last updated: 2026-02-04*