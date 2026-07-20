# How To: Binary And Csv Response

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test binary and csv response

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

### Step 1: Assign response = download_template(...)

```python
response = download_template('Excel')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(response.headers['content-type'], 'application/octet-stream')
```

### Step 4: Call self.assertGreater()

```python
self.assertGreater(cint(response.headers['content-length']), 0)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(guess_mime(response.data), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
```

### Step 6: Assign response = download_template(...)

```python
response = download_template('CSV')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('text/csv', response.headers['content-type'])
```

### Step 9: Call self.assertGreater()

```python
self.assertGreater(cint(response.headers['content-length']), 0)
```

### Step 10: Assign filename = 'دفتر الأستاذ العام'

```python
filename = 'دفتر الأستاذ العام'
```

### Step 11: Assign encoded_filename = value

```python
encoded_filename = filename.encode('utf-8').decode('unicode-escape', 'ignore') + '.xlsx'
```

### Step 12: Call provide_binary_file()

```python
provide_binary_file(filename, 'xlsx', 'content')
```

### Step 13: Assign response = build_response(...)

```python
response = build_response('binary')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(response.headers['content-type'], 'application/octet-stream')
```

### Step 16: Call self.assertGreater()

```python
self.assertGreater(cint(response.headers['content-length']), 0)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(response.headers['content-disposition'], f'filename="{encoded_filename}"')
```

### Step 18: Assign filters = json.dumps(...)

```python
filters = json.dumps({})
```

### Step 19: Assign fields = json.dumps(...)

```python
fields = json.dumps({'User': ['name']})
```


## Complete Example

```python
# Workflow
def download_template(file_type):
    filters = json.dumps({})
    fields = json.dumps({'User': ['name']})
    return self.post('/api/method/frappe.core.doctype.data_import.data_import.download_template', {'sid': self.sid, 'doctype': 'User', 'export_fields': fields, 'export_filters': filters, 'file_type': file_type})
response = download_template('Excel')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.headers['content-type'], 'application/octet-stream')
self.assertGreater(cint(response.headers['content-length']), 0)
self.assertEqual(guess_mime(response.data), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
response = download_template('CSV')
self.assertEqual(response.status_code, 200)
self.assertIn('text/csv', response.headers['content-type'])
self.assertGreater(cint(response.headers['content-length']), 0)
from frappe.desk.utils import provide_binary_file
from frappe.utils.response import build_response
filename = 'دفتر الأستاذ العام'
encoded_filename = filename.encode('utf-8').decode('unicode-escape', 'ignore') + '.xlsx'
provide_binary_file(filename, 'xlsx', 'content')
response = build_response('binary')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.headers['content-type'], 'application/octet-stream')
self.assertGreater(cint(response.headers['content-length']), 0)
self.assertEqual(response.headers['content-disposition'], f'filename="{encoded_filename}"')
```

## Next Steps


---

*Source: test_api.py:447 | Complexity: Advanced | Last updated: 2026-02-04*