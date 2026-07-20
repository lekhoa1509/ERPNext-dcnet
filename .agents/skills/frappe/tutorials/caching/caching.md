# How To: Caching

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test caching

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

### Step 1: Assign frappe.flags.force_website_cache = True

```python
frappe.flags.force_website_cache = True
```

### Step 2: Call clear_website_cache()

```python
clear_website_cache()
```

### Step 3: Assign response = get_response(...)

```python
response = get_response('/_test/_test_folder/_test_page')
```

### Step 4: Call self.assertIn()

```python
self.assertIn(('X-From-Cache', 'False'), list(response.headers))
```

### Step 5: Assign response = get_response(...)

```python
response = get_response('/_test/_test_folder/_test_page')
```

### Step 6: Call self.assertIn()

```python
self.assertIn(('X-From-Cache', 'True'), list(response.headers))
```

### Step 7: Assign frappe.flags.force_website_cache = False

```python
frappe.flags.force_website_cache = False
```


## Complete Example

```python
# Workflow
frappe.flags.force_website_cache = True
clear_website_cache()
response = get_response('/_test/_test_folder/_test_page')
self.assertIn(('X-From-Cache', 'False'), list(response.headers))
response = get_response('/_test/_test_folder/_test_page')
self.assertIn(('X-From-Cache', 'True'), list(response.headers))
frappe.flags.force_website_cache = False
```

## Next Steps


---

*Source: test_website.py:333 | Complexity: Intermediate | Last updated: 2026-02-04*