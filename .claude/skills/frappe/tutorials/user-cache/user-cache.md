# How To: User Cache

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test user cache

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

### Step 1: Assign function_call_count = 0

```python
function_call_count = 0
```

### Step 2: Assign PI = 3.1415

```python
PI = 3.1415
```

### Step 3: Assign ENGINEERING_PI, _E = 3

```python
ENGINEERING_PI = _E = 3
```

### Step 4: Assign PI_APPROX = value

```python
PI_APPROX = ENGINEERING_PI if frappe.session.user == 'Engineer' else PI
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(calculate_area(1), ENGINEERING_PI)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(function_call_count, 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(calculate_area(1), PI)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(function_call_count, 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(calculate_area(1), ENGINEERING_PI)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(function_call_count, 2)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(calculate_area(1), PI)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(function_call_count, 2)
```


## Complete Example

```python
# Workflow
function_call_count = 0
PI = 3.1415
ENGINEERING_PI = _E = 3

@redis_cache(user=True)
def calculate_area(radius: float) -> float:
    nonlocal function_call_count
    PI_APPROX = ENGINEERING_PI if frappe.session.user == 'Engineer' else PI
    function_call_count += 1
    return PI_APPROX * radius ** 2
with self.set_user('Engineer'):
    self.assertEqual(calculate_area(1), ENGINEERING_PI)
    self.assertEqual(function_call_count, 1)
with self.set_user('Mathematician'):
    self.assertEqual(calculate_area(1), PI)
    self.assertEqual(function_call_count, 2)
with self.set_user('Engineer'):
    self.assertEqual(calculate_area(1), ENGINEERING_PI)
    self.assertEqual(function_call_count, 2)
with self.set_user('Mathematician'):
    self.assertEqual(calculate_area(1), PI)
    self.assertEqual(function_call_count, 2)
```

## Next Steps


---

*Source: test_caching.py:201 | Complexity: Advanced | Last updated: 2026-02-04*