# How To: Get List Dict

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get list dict

## Prerequisites

**Required Modules:**
- `json`
- `sys`
- `typing`
- `contextlib`
- `functools`
- `random`
- `threading`
- `time`
- `unittest.mock`
- `urllib.parse`
- `requests`
- `filetype`
- `werkzeug.test`
- `frappe`
- `frappe.installer`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.core.doctype.user.user`
- `frappe.auth`
- `frappe.utils`
- `frappe.desk.utils`
- `frappe.utils.response`


## Step-by-Step Guide

### Step 1: Assign response = self.get(...)

```python
response = self.get(self.resource(self.DOCTYPE), {'sid': self.sid, 'as_dict': True})
```

### Step 2: Assign json = frappe._dict(...)

```python
json = frappe._dict(response.json)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 4: Call self.assertIsInstance()

```python
self.assertIsInstance(json.data, list)
```

### Step 5: Call self.assertIsInstance()

```python
self.assertIsInstance(json.data[0], dict)
```

### Step 6: Assign response = self.get(...)

```python
response = self.get(self.resource(self.DOCTYPE), {'sid': self.sid, 'as_dict': False})
```

### Step 7: Assign json = frappe._dict(...)

```python
json = frappe._dict(response.json)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 9: Call self.assertIsInstance()

```python
self.assertIsInstance(json.data, list)
```

### Step 10: Call self.assertIsInstance()

```python
self.assertIsInstance(json.data[0], list)
```


## Complete Example

```python
# Workflow
response = self.get(self.resource(self.DOCTYPE), {'sid': self.sid, 'as_dict': True})
json = frappe._dict(response.json)
self.assertEqual(response.status_code, 200)
self.assertIsInstance(json.data, list)
self.assertIsInstance(json.data[0], dict)
response = self.get(self.resource(self.DOCTYPE), {'sid': self.sid, 'as_dict': False})
json = frappe._dict(response.json)
self.assertEqual(response.status_code, 200)
self.assertIsInstance(json.data, list)
self.assertIsInstance(json.data[0], list)
```

## Next Steps


---

*Source: test_api.py:218 | Complexity: Advanced | Last updated: 2026-02-04*