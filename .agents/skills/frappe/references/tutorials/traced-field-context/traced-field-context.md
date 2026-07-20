# How To: Traced Field Context

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test traced field context

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

### Step 2: Assign doc.test_field = 'forbidden'

```python
doc.test_field = 'forbidden'
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(doc.test_field, 'forbidden')
```

### Step 4: Assign doc.test_field = 'forbidden'

```python
doc.test_field = 'forbidden'
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(doc.test_field, 'forbidden')
```

### Step 6: Assign doc.test_field = 'allowed'

```python
doc.test_field = 'allowed'
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.test_field, 'allowed')
```

### Step 8: Assign doc.test_field = 'forbidden'

```python
doc.test_field = 'forbidden'
```


## Complete Example

```python
# Workflow
doc = TestDocument()
doc.test_field = 'forbidden'
self.assertEqual(doc.test_field, 'forbidden')
with self.trace_fields(TestDocument, 'test_field', forbidden_values=['forbidden']):
    with self.assertRaises(AssertionError):
        doc.test_field = 'forbidden'
    doc.test_field = 'allowed'
    self.assertEqual(doc.test_field, 'allowed')
doc.test_field = 'forbidden'
self.assertEqual(doc.test_field, 'forbidden')
```

## Next Steps


---

*Source: test_trace.py:71 | Complexity: Advanced | Last updated: 2026-02-04*