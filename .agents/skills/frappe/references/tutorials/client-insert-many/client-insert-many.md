# How To: Client Insert Many

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test client insert many

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `frappe.client`
- `frappe.desk.doctype.note.note`
- `frappe.client`
- `frappe.handler`
- `frappe.handler`
- `frappe.handler`
- `requests`
- `frappe.auth`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`
- `frappe.client`


## Step-by-Step Guide

### Step 1: Assign note1 = value

```python
note1 = {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}
```

### Step 2: Assign note1 = insert(...)

```python
note1 = insert(note1)
```

### Step 3: Assign doc_list = value

```python
doc_list = [{'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}, {'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}, {'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}, {'doctype': 'Note', 'title': 'not-a-random-title', 'content': 'test'}, {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}, {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}, {'doctype': 'Note', 'title': 'another-note-title', 'content': 'test'}]
```

### Step 4: Assign docs = insert_many(...)

```python
docs = insert_many(doc_list)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(docs), 7)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Note', docs[3], 'title'), 'not-a-random-title')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Note', docs[6], 'title'), 'another-note-title')
```

### Step 8: Call self.assertIn()

```python
self.assertIn(note1.name, docs)
```

### Step 9: Call frappe.delete_doc()

```python
frappe.delete_doc('Note', doc)
```


## Complete Example

```python
# Workflow
from frappe.client import insert, insert_many

def get_random_title():
    return f'test-{frappe.generate_hash(length=5)}'
note1 = {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}
note1 = insert(note1)
doc_list = [{'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}, {'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}, {'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}, {'doctype': 'Note', 'title': 'not-a-random-title', 'content': 'test'}, {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}, {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}, {'doctype': 'Note', 'title': 'another-note-title', 'content': 'test'}]
docs = insert_many(doc_list)
self.assertEqual(len(docs), 7)
self.assertEqual(frappe.db.get_value('Note', docs[3], 'title'), 'not-a-random-title')
self.assertEqual(frappe.db.get_value('Note', docs[6], 'title'), 'another-note-title')
self.assertIn(note1.name, docs)
for doc in docs:
    frappe.delete_doc('Note', doc)
```

## Next Steps


---

*Source: test_client.py:245 | Complexity: Advanced | Last updated: 2026-02-04*