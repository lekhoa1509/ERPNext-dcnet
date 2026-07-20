# How To: Traced Field Context Custom Validation

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test traced field context custom validation

## Prerequisites

**Required Modules:**
- `unittest`
- `unittest.mock`
- `frappe`
- `frappe.model.document`
- `frappe.model.trace`
- `frappe.tests`
- `frappe.tests.utils`


## Step-by-Step Guide

### Step 1: Assign doc = TestDocument(...)

```python
doc = TestDocument()
```

### Step 2: Assign doc.number_field = 3

```python
doc.number_field = 3
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(doc.number_field, 3)
```

### Step 4: Assign doc.number_field = 2

```python
doc.number_field = 2
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(doc.number_field, 2)
```

### Step 6: Assign doc.number_field = 3

```python
doc.number_field = 3
```


## Complete Example

```python
# Workflow
doc = TestDocument()

def validate_even(obj, value):
    if value % 2 != 0:
        raise ValueError('Value must be even')
with self.trace_fields(TestDocument, 'number_field', custom_validation=validate_even):
    doc.number_field = 2
    self.assertEqual(doc.number_field, 2)
    with self.assertRaises(AssertionError):
        doc.number_field = 3
doc.number_field = 3
self.assertEqual(doc.number_field, 3)
```

## Next Steps


---

*Source: test_trace.py:90 | Complexity: Intermediate | Last updated: 2026-02-04*