# How To: Web View Link Authentication

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test web view link authentication

## Prerequisites

**Required Modules:**
- `inspect`
- `contextlib`
- `copy`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.app`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user.user`
- `frappe.desk.doctype.note.note`
- `frappe.model.document`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.desk.doctype.event.event`
- `pathlib`
- `frappe.modules.utils`
- `frappe.model.document`


## Step-by-Step Guide

### Step 1: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'Test'}).insert()
```

### Step 2: Assign document_key = todo.get_document_share_key(...)

```python
document_key = todo.get_document_share_key()
```

### Step 3: Assign old_document_key = todo.get_signature(...)

```python
old_document_key = todo.get_signature()
```

### Step 4: Assign url = value

```python
url = f'/ToDo/{todo.name}?key={old_document_key}'
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(self.get(url).status, '403 FORBIDDEN')
```

### Step 6: Assign url = value

```python
url = f'/ToDo/{todo.name}?key={document_key}'
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(self.get(url).status, '200 OK')
```

### Step 8: Assign invalid_key_url = value

```python
invalid_key_url = f'/ToDo/{todo.name}?key=INVALID_KEY'
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(self.get(invalid_key_url).status, '403 FORBIDDEN')
```

### Step 10: Assign document_key_doc = frappe.get_doc(...)

```python
document_key_doc = frappe.get_doc('Document Share Key', {'key': document_key})
```

### Step 11: Assign document_key_doc.expires_on = '2020-01-01'

```python
document_key_doc.expires_on = '2020-01-01'
```

### Step 12: Call document_key_doc.save()

```python
document_key_doc.save(ignore_permissions=True)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(self.get(url).status, '410 GONE')
```

### Step 14: Assign url_without_key = value

```python
url_without_key = f'/ToDo/{todo.name}'
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(self.get(url_without_key).status, '403 FORBIDDEN')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(self.get(url_without_key, 'Administrator').status, '200 OK')
```


## Complete Example

```python
# Workflow
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'Test'}).insert()
document_key = todo.get_document_share_key()
old_document_key = todo.get_signature()
url = f'/ToDo/{todo.name}?key={old_document_key}'
self.assertEqual(self.get(url).status, '403 FORBIDDEN')
url = f'/ToDo/{todo.name}?key={document_key}'
self.assertEqual(self.get(url).status, '200 OK')
invalid_key_url = f'/ToDo/{todo.name}?key=INVALID_KEY'
self.assertEqual(self.get(invalid_key_url).status, '403 FORBIDDEN')
document_key_doc = frappe.get_doc('Document Share Key', {'key': document_key})
document_key_doc.expires_on = '2020-01-01'
document_key_doc.save(ignore_permissions=True)
self.assertEqual(self.get(url).status, '410 GONE')
url_without_key = f'/ToDo/{todo.name}'
self.assertEqual(self.get(url_without_key).status, '403 FORBIDDEN')
self.assertEqual(self.get(url_without_key, 'Administrator').status, '200 OK')
```

## Next Steps


---

*Source: test_document.py:551 | Complexity: Advanced | Last updated: 2026-02-04*