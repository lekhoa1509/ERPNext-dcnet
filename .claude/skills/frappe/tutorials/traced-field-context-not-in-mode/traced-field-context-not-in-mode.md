# How To: Traced Field Context Not In Mode

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test traced field context not in test mode

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

### Step 2: Assign original_in_test = value

```python
original_in_test = frappe.in_test
```

### Step 3: Call toggle_test_mode()

```python
toggle_test_mode(False)
```

### Step 4: Assign doc.test_field = 'forbidden'

```python
doc.test_field = 'forbidden'
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(doc.test_field, 'forbidden')
```

### Step 6: Call toggle_test_mode()

```python
toggle_test_mode(original_in_test)
```

### Step 7: Assign doc.test_field = 'allowed'

```python
doc.test_field = 'allowed'
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doc.test_field, 'allowed')
```

### Step 9: Assign doc.test_field = 'forbidden'

```python
doc.test_field = 'forbidden'
```


## Complete Example

```python
# Workflow
doc = TestDocument()
original_in_test = frappe.in_test
toggle_test_mode(False)
try:
    with self.trace_fields(TestDocument, test_field={'forbidden_values': ['forbidden']}):
        with self.assertRaises(frappe.exceptions.ValidationError):
            doc.test_field = 'forbidden'
        doc.test_field = 'allowed'
        self.assertEqual(doc.test_field, 'allowed')
finally:
    toggle_test_mode(original_in_test)
doc.test_field = 'forbidden'
self.assertEqual(doc.test_field, 'forbidden')
```

## Next Steps


---

*Source: test_trace.py:108 | Complexity: Advanced | Last updated: 2026-02-04*