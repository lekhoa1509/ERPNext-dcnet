# How To: Hash

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test hash

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

### Step 1: Assign key = 'test_hash'

```python
key = 'test_hash'
```

### Step 2: Assign exists = frappe.cache.exists(...)

```python
exists = frappe.cache.exists(key)
```

### Step 3: Call self.assertFalse()

```python
self.assertFalse(exists)
```

### Step 4: Assign values = frappe.cache.hgetall(...)

```python
values = frappe.cache.hgetall(key)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(values), 5)
```

### Step 6: Assign keys = frappe.cache.hkeys(...)

```python
keys = frappe.cache.hkeys(key)
```

### Step 7: Call frappe.cache.hdel()

```python
frappe.cache.hdel(key, 'key_1')
```

### Step 8: Assign values = frappe.cache.hgetall(...)

```python
values = frappe.cache.hgetall(key)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(values), 4)
```

### Step 10: Call frappe.cache.hdel()

```python
frappe.cache.hdel(key, ['key_2', 'key_3'])
```

### Step 11: Assign values = frappe.cache.hgetall(...)

```python
values = frappe.cache.hgetall(key)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(values), 2)
```

### Step 13: Call frappe.cache.delete_value()

```python
frappe.cache.delete_value(key)
```

### Step 14: Assign exists = frappe.cache.exists(...)

```python
exists = frappe.cache.exists(key)
```

### Step 15: Call self.assertFalse()

```python
self.assertFalse(exists)
```

### Step 16: Call frappe.cache.hset()

```python
frappe.cache.hset(key, f'key_{i}', f'value_{i}')
```

### Step 17: Assign value = frappe.cache.hget(...)

```python
value = frappe.cache.hget(key, f'key_{i}')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(value, f'value_{i}')
```

### Step 19: Call self.assertIn()

```python
self.assertIn(f'key_{i}'.encode(), keys)
```


## Complete Example

```python
# Workflow
key = 'test_hash'
exists = frappe.cache.exists(key)
self.assertFalse(exists)
for i in range(5):
    frappe.cache.hset(key, f'key_{i}', f'value_{i}')
values = frappe.cache.hgetall(key)
self.assertEqual(len(values), 5)
for i in range(5):
    value = frappe.cache.hget(key, f'key_{i}')
    self.assertEqual(value, f'value_{i}')
keys = frappe.cache.hkeys(key)
for i in range(5):
    self.assertIn(f'key_{i}'.encode(), keys)
frappe.cache.hdel(key, 'key_1')
values = frappe.cache.hgetall(key)
self.assertEqual(len(values), 4)
frappe.cache.hdel(key, ['key_2', 'key_3'])
values = frappe.cache.hgetall(key)
self.assertEqual(len(values), 2)
frappe.cache.delete_value(key)
exists = frappe.cache.exists(key)
self.assertFalse(exists)
```

## Next Steps


---

*Source: test_caching.py:288 | Complexity: Advanced | Last updated: 2026-02-04*