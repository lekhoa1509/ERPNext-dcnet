# How To: Meta Tag Generation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test meta tag generation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`


## Step-by-Step Guide

### Step 1: Assign blogs = frappe.get_all(...)

```python
blogs = frappe.get_all('Web Page', fields=['name', 'route'], filters={'published': 1, 'route': ('!=', '')}, limit=1)
```

### Step 2: Assign blog = value

```python
blog = blogs[0]
```

### Step 3: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Website Route Meta')
```

### Step 4: Call doc.append()

```python
doc.append('meta_tags', {'key': 'type', 'value': 'web_page'})
```

### Step 5: Call doc.append()

```python
doc.append('meta_tags', {'key': 'og:title', 'value': 'My Web Page'})
```

### Step 6: Assign doc.name = value

```python
doc.name = blog.route
```

### Step 7: Call doc.insert()

```python
doc.insert()
```

### Step 8: Call set_request()

```python
set_request(path=blog.route)
```

### Step 9: Assign response = get_response(...)

```python
response = get_response()
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(response.status_code, 200)
```

### Step 11: Assign html = self.normalize_html(...)

```python
html = self.normalize_html(response.get_data().decode())
```

### Step 12: Call self.assertIn()

```python
self.assertIn(self.normalize_html('<meta name="type" content="web_page">'), html)
```

### Step 13: Call self.assertIn()

```python
self.assertIn(self.normalize_html('<meta property="og:title" content="My Web Page">'), html)
```


## Complete Example

```python
# Workflow
blogs = frappe.get_all('Web Page', fields=['name', 'route'], filters={'published': 1, 'route': ('!=', '')}, limit=1)
blog = blogs[0]
doc = frappe.new_doc('Website Route Meta')
doc.append('meta_tags', {'key': 'type', 'value': 'web_page'})
doc.append('meta_tags', {'key': 'og:title', 'value': 'My Web Page'})
doc.name = blog.route
doc.insert()
set_request(path=blog.route)
response = get_response()
self.assertTrue(response.status_code, 200)
html = self.normalize_html(response.get_data().decode())
self.assertIn(self.normalize_html('<meta name="type" content="web_page">'), html)
self.assertIn(self.normalize_html('<meta property="og:title" content="My Web Page">'), html)
```

## Next Steps


---

*Source: test_website_route_meta.py:12 | Complexity: Advanced | Last updated: 2026-02-04*