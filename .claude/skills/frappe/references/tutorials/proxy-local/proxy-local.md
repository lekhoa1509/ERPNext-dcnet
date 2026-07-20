# How To: Proxy Local

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test proxy local

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
assert p == [42, 1, 2, 3]
```

### Step 2: Assign ns.foo = value

```python
ns.foo = []
```

**Verification:**
```python
assert p == ns.foo
```

### Step 3: Assign p = ns(...)

```python
p = ns('foo')
```

**Verification:**
```python
assert list(p) == [42, 1, 2, 3, 1]
```

### Step 4: Call p.append()

```python
p.append(42)
```

**Verification:**
```python
assert p == p_from_local
```

### Step 5: Call p.append()

```python
p.append(23)
```

**Verification:**
```python
assert p._get_current_object() is ns.foo
```

### Step 6: Assign unknown = value

```python
p[1:] = [1, 2, 3]
```

**Verification:**
```python
assert p == [42, 1, 2, 3]
```

### Step 7: Assign p_from_local = ns(...)

```python
p_from_local = ns('foo')
```

### Step 8: Call p_from_local.append()

```python
p_from_local.append(2)
```

**Verification:**
```python
assert p == p_from_local
```


## Complete Example

```python
# Workflow
ns = frappe.local
ns.foo = []
p = ns('foo')
p.append(42)
p.append(23)
p[1:] = [1, 2, 3]
assert p == [42, 1, 2, 3]
assert p == ns.foo
ns.foo += [1]
assert list(p) == [42, 1, 2, 3, 1]
p_from_local = ns('foo')
p_from_local.append(2)
assert p == p_from_local
assert p._get_current_object() is ns.foo
```

## Next Steps


---

*Source: test_local_proxy.py:38 | Complexity: Advanced | Last updated: 2026-02-04*