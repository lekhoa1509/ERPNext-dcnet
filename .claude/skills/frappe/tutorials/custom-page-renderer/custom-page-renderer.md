# How To: Custom Page Renderer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test custom page renderer

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

### Step 1: Assign return_value = get_hooks(...)

```python
return_value = get_hooks(*args, **kwargs)
```

### Step 2: Call set_request()

```python
set_request(method='GET', path='/custom')
```

### Step 3: Assign response = get_response(...)

```python
response = get_response()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 3984)
```

### Step 5: Call set_request()

```python
set_request(method='GET', path='/new')
```

### Step 6: Assign content = get_response_content(...)

```python
content = get_response_content()
```

### Step 7: Call self.assertIn()

```python
self.assertIn('<div>Custom Page Response</div>', content)
```

### Step 8: Call set_request()

```python
set_request(method='GET', path='/random')
```

### Step 9: Assign response = get_response(...)

```python
response = get_response()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 404)
```

### Step 11: Assign return_value = value

```python
return_value = ['frappe.tests.test_website.CustomPageRenderer']
```


## Complete Example

```python
# Workflow
from frappe import get_hooks

def patched_get_hooks(*args, **kwargs):
    return_value = get_hooks(*args, **kwargs)
    if args and args[0] == 'page_renderer':
        return_value = ['frappe.tests.test_website.CustomPageRenderer']
    return return_value
with patch.object(frappe, 'get_hooks', patched_get_hooks):
    set_request(method='GET', path='/custom')
    response = get_response()
    self.assertEqual(response.status_code, 3984)
    set_request(method='GET', path='/new')
    content = get_response_content()
    self.assertIn('<div>Custom Page Response</div>', content)
    set_request(method='GET', path='/random')
    response = get_response()
    self.assertEqual(response.status_code, 404)
```

## Next Steps


---

*Source: test_website.py:241 | Complexity: Advanced | Last updated: 2026-02-04*