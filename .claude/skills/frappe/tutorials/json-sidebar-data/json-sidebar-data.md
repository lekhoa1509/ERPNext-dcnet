# How To: Json Sidebar Data

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test json sidebar data

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

### Step 1: Assign frappe.flags.look_for_sidebar = False

```python
frappe.flags.look_for_sidebar = False
```

### Step 2: Assign content = get_response_content(...)

```python
content = get_response_content('/_test/_test_folder/_test_page')
```

### Step 3: Call self.assertNotIn()

```python
self.assertNotIn('Test Sidebar', content)
```

### Step 4: Call clear_website_cache()

```python
clear_website_cache()
```

### Step 5: Assign frappe.flags.look_for_sidebar = True

```python
frappe.flags.look_for_sidebar = True
```

### Step 6: Assign content = get_response_content(...)

```python
content = get_response_content('/_test/_test_folder/_test_page')
```

### Step 7: Call self.assertIn()

```python
self.assertIn('Test Sidebar', content)
```

### Step 8: Assign frappe.flags.look_for_sidebar = False

```python
frappe.flags.look_for_sidebar = False
```


## Complete Example

```python
# Workflow
frappe.flags.look_for_sidebar = False
content = get_response_content('/_test/_test_folder/_test_page')
self.assertNotIn('Test Sidebar', content)
clear_website_cache()
frappe.flags.look_for_sidebar = True
content = get_response_content('/_test/_test_folder/_test_page')
self.assertIn('Test Sidebar', content)
frappe.flags.look_for_sidebar = False
```

## Next Steps


---

*Source: test_website.py:277 | Complexity: Advanced | Last updated: 2026-02-04*