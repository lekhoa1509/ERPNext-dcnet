# How To: Update Document

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test update document

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

### Step 1: Assign generated_desc = frappe.mock(...)

```python
generated_desc = frappe.mock('paragraph')
```

### Step 2: Assign data = value

```python
data = {'description': generated_desc, 'sid': self.sid}
```

### Step 3: Assign random_doc = choice(...)

```python
random_doc = choice(self.GENERATED_DOCUMENTS)
```

### Step 4: Assign response = self.put(...)

```python
response = self.put(self.resource(self.DOCTYPE, random_doc), data=data)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.json['data']['description'], generated_desc)
```

### Step 7: Assign response = self.get(...)

```python
response = self.get(self.resource(self.DOCTYPE, random_doc))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(response.json['data']['description'], generated_desc)
```


## Complete Example

```python
# Workflow
generated_desc = frappe.mock('paragraph')
data = {'description': generated_desc, 'sid': self.sid}
random_doc = choice(self.GENERATED_DOCUMENTS)
response = self.put(self.resource(self.DOCTYPE, random_doc), data=data)
self.assertEqual(response.status_code, 200)
self.assertEqual(response.json['data']['description'], generated_desc)
response = self.get(self.resource(self.DOCTYPE, random_doc))
self.assertEqual(response.json['data']['description'], generated_desc)
```

## Next Steps


---

*Source: test_api.py:255 | Complexity: Advanced | Last updated: 2026-02-04*