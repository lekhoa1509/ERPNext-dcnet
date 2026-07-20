# How To: Webform Publish Functionality

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test webform publish functionality

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.www.list`
- `frappe`


## Step-by-Step Guide

### Step 1: Assign request_data = frappe.get_doc(...)

```python
request_data = frappe.get_doc('Web Form', 'request-data')
```

### Step 2: Assign request_data.published = True

```python
request_data.published = True
```

### Step 3: Call request_data.save()

```python
request_data.save()
```

### Step 4: Call set_request()

```python
set_request(method='GET', path='request-data/new')
```

### Step 5: Assign response = get_response(...)

```python
response = get_response()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 7: Assign request_data.published = False

```python
request_data.published = False
```

### Step 8: Call request_data.save()

```python
request_data.save()
```

### Step 9: Assign response = get_response(...)

```python
response = get_response()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 404)
```


## Complete Example

```python
# Workflow
request_data = frappe.get_doc('Web Form', 'request-data')
request_data.published = True
request_data.save()
set_request(method='GET', path='request-data/new')
response = get_response()
self.assertEqual(response.status_code, 200)
request_data.published = False
request_data.save()
response = get_response()
self.assertEqual(response.status_code, 404)
```

## Next Steps


---

*Source: test_webform.py:9 | Complexity: Advanced | Last updated: 2026-02-04*