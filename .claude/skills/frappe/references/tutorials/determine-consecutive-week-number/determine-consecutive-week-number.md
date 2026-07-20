# How To: Determine Consecutive Week Number

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test determine consecutive week number

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

### Step 1: Assign dt = datetime.fromisoformat(...)

```python
dt = datetime.fromisoformat('2019-12-31')
```

### Step 2: Assign w = determine_consecutive_week_number(...)

```python
w = determine_consecutive_week_number(dt)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(w, '53')
```

### Step 4: Assign dt = datetime.fromisoformat(...)

```python
dt = datetime.fromisoformat('2020-01-01')
```

### Step 5: Assign w = determine_consecutive_week_number(...)

```python
w = determine_consecutive_week_number(dt)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(w, '01')
```

### Step 7: Assign dt = datetime.fromisoformat(...)

```python
dt = datetime.fromisoformat('2020-01-15')
```

### Step 8: Assign w = determine_consecutive_week_number(...)

```python
w = determine_consecutive_week_number(dt)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(w, '03')
```

### Step 10: Assign dt = datetime.fromisoformat(...)

```python
dt = datetime.fromisoformat('2021-01-01')
```

### Step 11: Assign w = determine_consecutive_week_number(...)

```python
w = determine_consecutive_week_number(dt)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(w, '00')
```

### Step 13: Assign dt = datetime.fromisoformat(...)

```python
dt = datetime.fromisoformat('2021-12-31')
```

### Step 14: Assign w = determine_consecutive_week_number(...)

```python
w = determine_consecutive_week_number(dt)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(w, '52')
```


## Complete Example

```python
# Setup
frappe.db.delete('Note')

# Workflow
from datetime import datetime
dt = datetime.fromisoformat('2019-12-31')
w = determine_consecutive_week_number(dt)
self.assertEqual(w, '53')
dt = datetime.fromisoformat('2020-01-01')
w = determine_consecutive_week_number(dt)
self.assertEqual(w, '01')
dt = datetime.fromisoformat('2020-01-15')
w = determine_consecutive_week_number(dt)
self.assertEqual(w, '03')
dt = datetime.fromisoformat('2021-01-01')
w = determine_consecutive_week_number(dt)
self.assertEqual(w, '00')
dt = datetime.fromisoformat('2021-12-31')
w = determine_consecutive_week_number(dt)
self.assertEqual(w, '52')
```

## Next Steps


---

*Source: test_naming.py:253 | Complexity: Advanced | Last updated: 2026-02-04*