# How To: Render Web Template With Values

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test render web template with values

## Prerequisites

**Required Modules:**
- `bs4`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('Web Template', 'Hero with Right Image')
```

### Step 2: Assign values = value

```python
values = {'title': 'Test Hero', 'subtitle': 'Test subtitle content', 'primary_action': '/test', 'primary_action_label': 'Test Button'}
```

### Step 3: Assign html = doc.render(...)

```python
html = doc.render(values)
```

### Step 4: Assign soup = BeautifulSoup(...)

```python
soup = BeautifulSoup(html, 'html.parser')
```

### Step 5: Assign heading = soup.find(...)

```python
heading = soup.find('h1')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue('Test Hero' in heading.text)
```

### Step 7: Assign subtitle = soup.find(...)

```python
subtitle = soup.find('p')
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue('Test subtitle content' in subtitle.text)
```

### Step 9: Assign button = soup.find(...)

```python
button = soup.find('a')
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue('Test Button' in button.text)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue('/test' == button.attrs['href'])
```


## Complete Example

```python
# Workflow
doc = frappe.get_doc('Web Template', 'Hero with Right Image')
values = {'title': 'Test Hero', 'subtitle': 'Test subtitle content', 'primary_action': '/test', 'primary_action_label': 'Test Button'}
html = doc.render(values)
soup = BeautifulSoup(html, 'html.parser')
heading = soup.find('h1')
self.assertTrue('Test Hero' in heading.text)
subtitle = soup.find('p')
self.assertTrue('Test subtitle content' in subtitle.text)
button = soup.find('a')
self.assertTrue('Test Button' in button.text)
self.assertTrue('/test' == button.attrs['href'])
```

## Next Steps


---

*Source: test_web_template.py:12 | Complexity: Advanced | Last updated: 2026-02-04*