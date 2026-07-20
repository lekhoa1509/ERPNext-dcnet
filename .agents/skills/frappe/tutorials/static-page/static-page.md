# How To: Static Page

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test static page

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.page_renderers.static_page`
- `frappe.website.serve`
- `frappe.website.utils`
- `frappe.hooks`
- `frappe`
- `pathlib`
- `random`
- `frappe.utils.jinja_globals`
- `frappe`


## Step-by-Step Guide

### Step 1: Call set_request()

```python
set_request(method='GET', path='/_test/static-file-test.png')
```

### Step 2: Assign response = get_response(...)

```python
response = get_response()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 4: Call set_request()

```python
set_request(method='GET', path='/_test/assets/image.jpg')
```

### Step 5: Assign response = get_response(...)

```python
response = get_response()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 7: Call set_request()

```python
set_request(method='GET', path='/_test/assets/image')
```

### Step 8: Assign response = get_response(...)

```python
response = get_response()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 10: Call set_request()

```python
set_request(method='GET', path='/_test/assets/image')
```

### Step 11: Assign response = get_response(...)

```python
response = get_response()
```

### Step 12: Call static_render.assert_called()

```python
static_render.assert_called()
```


## Complete Example

```python
# Workflow
set_request(method='GET', path='/_test/static-file-test.png')
response = get_response()
self.assertEqual(response.status_code, 200)
set_request(method='GET', path='/_test/assets/image.jpg')
response = get_response()
self.assertEqual(response.status_code, 200)
set_request(method='GET', path='/_test/assets/image')
response = get_response()
self.assertEqual(response.status_code, 200)
with patch.object(StaticPage, 'render') as static_render:
    set_request(method='GET', path='/_test/assets/image')
    response = get_response()
    static_render.assert_called()
```

## Next Steps


---

*Source: test_website.py:109 | Complexity: Advanced | Last updated: 2026-02-04*