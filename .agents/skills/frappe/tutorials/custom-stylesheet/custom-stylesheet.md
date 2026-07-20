# How To: Custom Stylesheet

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test custom stylesheet

## Prerequisites

**Required Modules:**
- `bs4`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`


## Step-by-Step Guide

### Step 1: Call self.create_web_page()

```python
self.create_web_page()
```

### Step 2: Assign theme = self.create_website_theme(...)

```python
theme = self.create_website_theme()
```

### Step 3: Call theme.set_as_default()

```python
theme.set_as_default()
```

### Step 4: Assign frappe.conf.developer_mode = 1

```python
frappe.conf.developer_mode = 1
```

### Step 5: Call set_request()

```python
set_request(method='GET', path='test-web-template')
```

### Step 6: Assign response = get_response(...)

```python
response = get_response()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 8: Assign html = frappe.safe_decode(...)

```python
html = frappe.safe_decode(response.get_data())
```

### Step 9: Assign soup = BeautifulSoup(...)

```python
soup = BeautifulSoup(html, 'html.parser')
```

### Step 10: Assign stylesheet = soup.select_one(...)

```python
stylesheet = soup.select_one('link[rel="stylesheet"]')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(stylesheet.attrs['href'], theme.theme_url)
```

### Step 12: Call frappe.get_doc.set_as_default()

```python
frappe.get_doc('Website Theme', 'Standard').set_as_default()
```


## Complete Example

```python
# Workflow
self.create_web_page()
theme = self.create_website_theme()
theme.set_as_default()
frappe.conf.developer_mode = 1
set_request(method='GET', path='test-web-template')
response = get_response()
self.assertEqual(response.status_code, 200)
html = frappe.safe_decode(response.get_data())
soup = BeautifulSoup(html, 'html.parser')
stylesheet = soup.select_one('link[rel="stylesheet"]')
self.assertEqual(stylesheet.attrs['href'], theme.theme_url)
frappe.get_doc('Website Theme', 'Standard').set_as_default()
```

## Next Steps


---

*Source: test_web_template.py:51 | Complexity: Advanced | Last updated: 2026-02-04*