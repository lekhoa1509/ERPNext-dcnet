# How To: Basic Local

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test basic local

## Prerequisites

**Required Modules:**
- `time`
- `threading`
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign ns = value

```python
ns = frappe.local
```

**Verification:**
```python
assert sorted(values) == [1, 2, 3]
```

### Step 2: Assign ns.foo = 0

```python
ns.foo = 0
```

### Step 3: Assign values = value

```python
values = []
```

### Step 4: Assign threads = value

```python
threads = [Thread(target=value_setter, args=(x,)) for x in [1, 2, 3]]
```

**Verification:**
```python
assert sorted(values) == [1, 2, 3]
```

### Step 5: Call delfoo()

```python
delfoo()
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(AttributeError, lambda: ns.foo)
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(AttributeError, delfoo)
```

### Step 8: Call time.sleep()

```python
time.sleep(0.01 * idx)
```

### Step 9: Assign ns.foo = idx

```python
ns.foo = idx
```

### Step 10: Call time.sleep()

```python
time.sleep(0.02)
```

### Step 11: Call values.append()

```python
values.append(ns.foo)
```

### Step 12: Call thread.start()

```python
thread.start()
```

### Step 13: Call thread.join()

```python
thread.join()
```


## Complete Example

```python
# Workflow
ns = frappe.local
ns.foo = 0
values = []

def value_setter(idx):
    time.sleep(0.01 * idx)
    ns.foo = idx
    time.sleep(0.02)
    values.append(ns.foo)
threads = [Thread(target=value_setter, args=(x,)) for x in [1, 2, 3]]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
assert sorted(values) == [1, 2, 3]

def delfoo():
    del ns.foo
delfoo()
self.assertRaises(AttributeError, lambda: ns.foo)
self.assertRaises(AttributeError, delfoo)
```

## Next Steps


---

*Source: test_local_proxy.py:13 | Complexity: Advanced | Last updated: 2026-02-04*