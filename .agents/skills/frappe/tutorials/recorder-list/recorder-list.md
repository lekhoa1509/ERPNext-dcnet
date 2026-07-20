# How To: Recorder List

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test recorder list

## Prerequisites

**Required Modules:**
- `re`
- `frappe`
- `frappe.recorder`
- `frappe.core.doctype.recorder.recorder`
- `frappe.query_builder.utils`
- `frappe.recorder`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Call frappe.get_all()

```python
frappe.get_all('User')
```

### Step 2: Call self.stop_recorder()

```python
self.stop_recorder()
```

### Step 3: Assign requests = frappe.get_all(...)

```python
requests = frappe.get_all('Recorder')
```

### Step 4: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(requests), 1)
```

### Step 5: Assign request = frappe.get_doc(...)

```python
request = frappe.get_doc('Recorder', requests[0].name)
```

### Step 6: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(request.sql_queries), 1)
```

### Step 7: Assign queries = value

```python
queries = [sql_query.query for sql_query in request.sql_queries]
```

### Step 8: Assign match_flag = 0

```python
match_flag = 0
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(match_flag, 1)
```

### Step 10: Assign match_flag = 1

```python
match_flag = 1
```


## Complete Example

```python
# Workflow
frappe.get_all('User')
self.stop_recorder()
requests = frappe.get_all('Recorder')
self.assertGreaterEqual(len(requests), 1)
request = frappe.get_doc('Recorder', requests[0].name)
self.assertGreaterEqual(len(request.sql_queries), 1)
queries = [sql_query.query for sql_query in request.sql_queries]
match_flag = 0
for query in queries:
    if bool(re.match('^[select.*from `tabUser`]', query, flags=re.IGNORECASE)):
        match_flag = 1
        break
self.assertEqual(match_flag, 1)
```

## Next Steps


---

*Source: test_recorder.py:33 | Complexity: Advanced | Last updated: 2026-02-04*