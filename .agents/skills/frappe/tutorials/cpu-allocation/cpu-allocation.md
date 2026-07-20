# How To: Cpu Allocation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cpu allocation

## Prerequisites

**Required Modules:**
- `gc`
- `itertools`
- `sys`
- `time`
- `unittest.mock`
- `psutil`
- `tenacity`
- `frappe`
- `frappe.frappeclient`
- `frappe.model.base_document`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.caching`
- `frappe.website.path_resolver`
- `frappe.utils`
- `frappe._optimizations`


## Step-by-Step Guide

### Step 1: Call self.assertEqual()

```python
self.assertEqual(assign_core(0, 4, 8, [0], []), 0)
```

### Step 2: Assign siblings = value

```python
siblings = [(i,) for i in range(8)]
```

### Step 3: Assign cores = list(...)

```python
cores = list(range(8))
```

### Step 4: Assign default_affinity_16 = list(...)

```python
default_affinity_16 = list(range(16))
```

### Step 5: Assign linear_siblings_16 = list(...)

```python
linear_siblings_16 = list(itertools.batched(range(16), 2, strict=True))
```

### Step 6: Assign logical_cores = list(...)

```python
logical_cores = list(range(16))
```

### Step 7: Assign expected_assignments = value

```python
expected_assignments = [*(l[0] for l in linear_siblings_16), *(l[1] for l in linear_siblings_16)]
```

### Step 8: Assign block_siblings_16 = list(...)

```python
block_siblings_16 = list(zip(range(8), range(8, 16), strict=True))
```

### Step 9: Assign enabled_cores = value

```python
enabled_cores = [0, 2, 4, 6]
```

### Step 10: Assign affinity = value

```python
affinity = [(i,) for i in enabled_cores]
```

### Step 11: Assign core = assign_core(...)

```python
core = assign_core(0, 4, 4, enabled_cores, affinity)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(core, 0)
```

### Step 13: Assign core = assign_core(...)

```python
core = assign_core(1, 4, 4, enabled_cores, affinity)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(core, 2)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(assign_core(pid, len(cores), len(cores), cores, siblings), pid)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(assign_core(pid, len(cores), len(cores), cores, siblings), pid % len(cores))
```

### Step 17: Assign core = assign_core(...)

```python
core = assign_core(pid, len(logical_cores) // 2, len(logical_cores), default_affinity_16, linear_siblings_16)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(core, expected_core)
```

### Step 19: Assign core = assign_core(...)

```python
core = assign_core(pid, len(logical_cores) // 2, len(logical_cores), logical_cores, block_siblings_16)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(core, pid)
```


## Complete Example

```python
# Workflow
from frappe._optimizations import assign_core
self.assertEqual(assign_core(0, 4, 8, [0], []), 0)
siblings = [(i,) for i in range(8)]
cores = list(range(8))
for pid in cores:
    self.assertEqual(assign_core(pid, len(cores), len(cores), cores, siblings), pid)
for pid in range(8, 16):
    self.assertEqual(assign_core(pid, len(cores), len(cores), cores, siblings), pid % len(cores))
default_affinity_16 = list(range(16))
linear_siblings_16 = list(itertools.batched(range(16), 2, strict=True))
logical_cores = list(range(16))
expected_assignments = [*(l[0] for l in linear_siblings_16), *(l[1] for l in linear_siblings_16)]
for pid, expected_core in zip(logical_cores, expected_assignments, strict=True):
    core = assign_core(pid, len(logical_cores) // 2, len(logical_cores), default_affinity_16, linear_siblings_16)
    self.assertEqual(core, expected_core)
block_siblings_16 = list(zip(range(8), range(8, 16), strict=True))
for pid in logical_cores:
    core = assign_core(pid, len(logical_cores) // 2, len(logical_cores), logical_cores, block_siblings_16)
    self.assertEqual(core, pid)
enabled_cores = [0, 2, 4, 6]
affinity = [(i,) for i in enabled_cores]
core = assign_core(0, 4, 4, enabled_cores, affinity)
self.assertEqual(core, 0)
core = assign_core(1, 4, 4, enabled_cores, affinity)
self.assertEqual(core, 2)
```

## Next Steps


---

*Source: test_perf.py:234 | Complexity: Advanced | Last updated: 2026-02-04*