# How To: Client Insert

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test client insert

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

### Step 1: Assign doc = value

```python
doc = {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}
```

### Step 2: Assign note1 = insert(...)

```python
note1 = insert(doc)
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(note1)
```

### Step 4: Assign unknown = get_random_title(...)

```python
doc['title'] = get_random_title()
```

### Step 5: Assign json_doc = frappe.as_json(...)

```python
json_doc = frappe.as_json(doc)
```

### Step 6: Assign note2 = insert(...)

```python
note2 = insert(json_doc)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(note2)
```

### Step 8: Assign child_doc = value

```python
child_doc = {'doctype': 'Note Seen By', 'user': 'Administrator'}
```

### Step 9: Assign child_doc = value

```python
child_doc = {'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}
```

### Step 10: Assign note3 = insert(...)

```python
note3 = insert(child_doc)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(note3)
```

### Step 12: Call frappe.delete_doc()

```python
frappe.delete_doc('Note', note1.name)
```

### Step 13: Call frappe.delete_doc()

```python
frappe.delete_doc('Note', note2.name)
```

### Step 14: Call insert()

```python
insert(child_doc)
```


## Complete Example

```python
# Workflow
from frappe.client import insert

def get_random_title():
    return f'test-{frappe.generate_hash()}'
doc = {'doctype': 'Note', 'title': get_random_title(), 'content': 'test'}
note1 = insert(doc)
self.assertTrue(note1)
doc['title'] = get_random_title()
json_doc = frappe.as_json(doc)
note2 = insert(json_doc)
self.assertTrue(note2)
child_doc = {'doctype': 'Note Seen By', 'user': 'Administrator'}
with self.assertRaises(frappe.ValidationError):
    insert(child_doc)
child_doc = {'doctype': 'Note Seen By', 'user': 'Administrator', 'parenttype': 'Note', 'parent': note1.name, 'parentfield': 'seen_by'}
note3 = insert(child_doc)
self.assertTrue(note3)
frappe.delete_doc('Note', note1.name)
frappe.delete_doc('Note', note2.name)
```

## Next Steps


---

*Source: test_client.py:208 | Complexity: Advanced | Last updated: 2026-02-04*