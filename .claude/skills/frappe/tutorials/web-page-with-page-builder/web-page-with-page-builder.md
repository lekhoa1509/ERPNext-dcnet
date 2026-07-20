# How To: Web Page With Page Builder

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test web page with page builder

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

### Step 2: Call set_request()

```python
set_request(method='GET', path='test-web-template')
```

### Step 3: Assign response = get_response(...)

```python
response = get_response()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 5: Assign html = frappe.safe_decode(...)

```python
html = frappe.safe_decode(response.get_data())
```

### Step 6: Assign soup = BeautifulSoup(...)

```python
soup = BeautifulSoup(html, 'html.parser')
```

### Step 7: Assign sections = soup.find.find_all(...)

```python
sections = soup.find('main').find_all('section')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(sections), 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(sections[0].find('h2').text, 'Test Title')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(sections[0].find('p').text, 'test lorem ipsum')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(sections[1].find_all('a')), 3)
```


## Complete Example

```python
# Workflow
self.create_web_page()
set_request(method='GET', path='test-web-template')
response = get_response()
self.assertEqual(response.status_code, 200)
html = frappe.safe_decode(response.get_data())
soup = BeautifulSoup(html, 'html.parser')
sections = soup.find('main').find_all('section')
self.assertEqual(len(sections), 2)
self.assertEqual(sections[0].find('h2').text, 'Test Title')
self.assertEqual(sections[0].find('p').text, 'test lorem ipsum')
self.assertEqual(len(sections[1].find_all('a')), 3)
```

## Next Steps


---

*Source: test_web_template.py:33 | Complexity: Advanced | Last updated: 2026-02-04*