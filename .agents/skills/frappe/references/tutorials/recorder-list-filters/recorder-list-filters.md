# How To: Recorder List Filters

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test recorder list filters

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

### Step 1: Assign user = frappe.qb.DocType(...)

```python
user = frappe.qb.DocType('User')
```

### Step 2: Call frappe.qb.from_.select.run()

```python
frappe.qb.from_(user).select('name').run()
```

### Step 3: Call self.stop_recorder()

```python
self.stop_recorder()
```

### Step 4: Call set_request()

```python
set_request(path='/api/method/abc')
```

### Step 5: Call frappe.recorder.start()

```python
frappe.recorder.start()
```

### Step 6: Call frappe.recorder.record()

```python
frappe.recorder.record()
```

### Step 7: Call frappe.get_all()

```python
frappe.get_all('User')
```

### Step 8: Call self.stop_recorder()

```python
self.stop_recorder()
```

### Step 9: Assign requests = frappe.get_list(...)

```python
requests = frappe.get_list('Recorder', filters={'path': ('like', '/api/method/ping'), 'number_of_queries': 1})
```

### Step 10: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(requests), 1)
```

### Step 11: Assign requests = frappe.get_list(...)

```python
requests = frappe.get_list('Recorder', filters={'path': ('like', '/api/method/test')})
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(requests), 0)
```

### Step 13: Assign requests = frappe.get_list(...)

```python
requests = frappe.get_list('Recorder', filters={'method': 'GET'})
```

### Step 14: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(requests), 1)
```

### Step 15: Assign requests = frappe.get_list(...)

```python
requests = frappe.get_list('Recorder', filters={'method': 'POST'})
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(requests), 0)
```

### Step 17: Assign requests = frappe.get_list(...)

```python
requests = frappe.get_list('Recorder', order_by='path desc')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(requests[0].path, '/api/method/ping')
```


## Complete Example

```python
# Workflow
user = frappe.qb.DocType('User')
frappe.qb.from_(user).select('name').run()
self.stop_recorder()
set_request(path='/api/method/abc')
frappe.recorder.start()
frappe.recorder.record()
frappe.get_all('User')
self.stop_recorder()
requests = frappe.get_list('Recorder', filters={'path': ('like', '/api/method/ping'), 'number_of_queries': 1})
self.assertGreaterEqual(len(requests), 1)
requests = frappe.get_list('Recorder', filters={'path': ('like', '/api/method/test')})
self.assertEqual(len(requests), 0)
requests = frappe.get_list('Recorder', filters={'method': 'GET'})
self.assertGreaterEqual(len(requests), 1)
requests = frappe.get_list('Recorder', filters={'method': 'POST'})
self.assertEqual(len(requests), 0)
requests = frappe.get_list('Recorder', order_by='path desc')
self.assertEqual(requests[0].path, '/api/method/ping')
```

## Next Steps


---

*Source: test_recorder.py:48 | Complexity: Advanced | Last updated: 2026-02-04*