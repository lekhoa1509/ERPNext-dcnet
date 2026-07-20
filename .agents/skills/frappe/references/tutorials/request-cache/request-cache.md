# How To: Request Cache

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test request cache

## Prerequisites

**Required Modules:**
- `time`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe.tests.utils`
- `frappe.utils.caching`
- `frappe.cache_manager`
- `frappe.cache_manager`


## Step-by-Step Guide

### Step 1: Assign retval = value

```python
retval = []
```

### Step 2: Assign hashable_values = value

```python
hashable_values = [range(10), frappe.get_last_doc('DocType'), True, None]
```

### Step 3: Assign unhashable_values = value

```python
unhashable_values = [[1, 2, 3, 4], {'abc': 'test-key'}, frappe._dict()]
```

### Step 4: Call retval.extend()

```python
retval.extend((request_specific_api(120, 23) for _ in range(5)))
```

### Step 5: Call external_service.assert_called_once()

```python
external_service.assert_called_once()
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(same_output_received())
```

### Step 7: Call retval.append()

```python
retval.append(request_specific_api(120.0, 23))
```

### Step 8: Call external_service.assert_called_once()

```python
external_service.assert_called_once()
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(same_output_received())
```

### Step 10: Call retval.clear()

```python
retval.clear()
```

### Step 11: Call retval.extend()

```python
retval.extend((request_specific_api(120, 13) for _ in range(10)))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(external_service.call_count, 2)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(same_output_received())
```

### Step 14: Assign external_service.call_count = 0

```python
external_service.call_count = 0
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(external_service.call_count, 1)
```

### Step 16: Assign external_service.call_count = 0

```python
external_service.call_count = 0
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(external_service.call_count, 2)
```

### Step 18: Call request_specific_api()

```python
request_specific_api(arg, 13)
```

### Step 19: Call request_specific_api()

```python
request_specific_api(arg, 13)
```


## Complete Example

```python
# Workflow
retval = []
hashable_values = [range(10), frappe.get_last_doc('DocType'), True, None]
unhashable_values = [[1, 2, 3, 4], {'abc': 'test-key'}, frappe._dict()]

def same_output_received():
    return len(set(retval)) == 1
retval.extend((request_specific_api(120, 23) for _ in range(5)))
external_service.assert_called_once()
self.assertTrue(same_output_received())
retval.append(request_specific_api(120.0, 23))
external_service.assert_called_once()
self.assertTrue(same_output_received())
retval.clear()
retval.extend((request_specific_api(120, 13) for _ in range(10)))
self.assertEqual(external_service.call_count, 2)
self.assertTrue(same_output_received())
for arg in hashable_values:
    external_service.call_count = 0
    for _ in range(2):
        request_specific_api(arg, 13)
    self.assertEqual(external_service.call_count, 1)
for arg in unhashable_values:
    external_service.call_count = 0
    for _ in range(2):
        request_specific_api(arg, 13)
    self.assertEqual(external_service.call_count, 2)
```

## Next Steps


---

*Source: test_caching.py:40 | Complexity: Advanced | Last updated: 2026-02-04*