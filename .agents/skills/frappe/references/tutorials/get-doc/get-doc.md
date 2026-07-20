# How To: Get Doc

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get doc

## Prerequisites

**Required Modules:**
- `base64`
- `requests`
- `frappe`
- `frappe.core.doctype.user.user`
- `frappe.frappeclient`
- `frappe.model`
- `frappe.tests`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Assign USER = 'Administrator'

```python
USER = 'Administrator'
```

### Step 2: Assign TITLE = 'get_this'

```python
TITLE = 'get_this'
```

### Step 3: Assign DOCTYPE = 'Note'

```python
DOCTYPE = 'Note'
```

### Step 4: Assign server = FrappeClient(...)

```python
server = FrappeClient(get_url(), 'Administrator', self.PASSWORD, verify=False)
```

### Step 5: Assign NAME = server.insert.get(...)

```python
NAME = server.insert({'doctype': DOCTYPE, 'title': TITLE}).get('name')
```

### Step 6: Assign doc = server.get_doc(...)

```python
doc = server.get_doc(DOCTYPE, NAME)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.get('doctype'), DOCTYPE)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doc.get('name'), NAME)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(doc.get('title'), TITLE)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(doc.get('owner'), USER)
```

### Step 11: Call self.assertIn()

```python
self.assertIn(field, doc)
```


## Complete Example

```python
# Workflow
USER = 'Administrator'
TITLE = 'get_this'
DOCTYPE = 'Note'
server = FrappeClient(get_url(), 'Administrator', self.PASSWORD, verify=False)
NAME = server.insert({'doctype': DOCTYPE, 'title': TITLE}).get('name')
doc = server.get_doc(DOCTYPE, NAME)
for field in default_fields:
    self.assertIn(field, doc)
self.assertEqual(doc.get('doctype'), DOCTYPE)
self.assertEqual(doc.get('name'), NAME)
self.assertEqual(doc.get('title'), TITLE)
self.assertEqual(doc.get('owner'), USER)
```

## Next Steps


---

*Source: test_frappe_client.py:85 | Complexity: Advanced | Last updated: 2026-02-04*