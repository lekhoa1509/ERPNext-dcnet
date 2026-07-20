# How To: Document Indexing Operations

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test individual document indexing and removal operations.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `os`
- `sqlite3`
- `time`
- `typing`
- `unittest.mock`
- `frappe`
- `frappe.search.sqlite_search`
- `frappe.tests`
- `frappe.search.sqlite_search`

**Setup Required:**
```python
'Set up test data for each test.'
super().setUp()
self.test_notes = []
self.test_todos = []
note_data = [{'title': 'Python Programming Guide', 'content': 'Learn Python basics and advanced concepts'}, {'title': 'Project Management Tips', 'content': 'How to manage software projects effectively'}, {'title': 'Cooking Recipe Collection', 'content': 'Delicious recipes for home cooking'}, {'title': 'Machine Learning Tutorial', 'content': 'Introduction to ML algorithms and Python implementation'}]
for data in note_data:
    note = frappe.get_doc({'doctype': 'Note', 'title': data['title'], 'content': data['content']})
    note.insert()
    self.test_notes.append(note)
todo_data = [{'description': 'Review Python code for search functionality'}, {'description': 'Update project documentation'}, {'description': 'Plan team meeting agenda'}]
for data in todo_data:
    todo = frappe.get_doc({'doctype': 'ToDo', 'description': data['description'], 'status': 'Open'})
    todo.insert()
    self.test_todos.append(todo)
```

## Step-by-Step Guide

### Step 1: 'Test individual document indexing and removal operations.'

```python
'Test individual document indexing and removal operations.'
```

### Step 2: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 3: Assign new_note = frappe.get_doc(...)

```python
new_note = frappe.get_doc({'doctype': 'Note', 'title': 'Newly Added Document', 'content': 'This document was added after initial indexing'})
```

### Step 4: Call new_note.insert()

```python
new_note.insert()
```

### Step 5: Assign results = self.search.search(...)

```python
results = self.search.search('Newly Added Document')
```

### Step 6: Assign initial_count = len(...)

```python
initial_count = len(results['results'])
```

### Step 7: Call self.search.index_doc()

```python
self.search.index_doc('Note', new_note.name)
```

### Step 8: Assign results = self.search.search(...)

```python
results = self.search.search('Newly Added Document')
```

### Step 9: Call self.assertGreater()

```python
self.assertGreater(len(results['results']), initial_count)
```

### Step 10: Assign found = False

```python
found = False
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(found, 'Newly indexed document not found in search results')
```

### Step 12: Call self.search.remove_doc()

```python
self.search.remove_doc('Note', new_note.name)
```

### Step 13: Assign results = self.search.search(...)

```python
results = self.search.search('Newly Added Document')
```

### Step 14: Assign found = False

```python
found = False
```

### Step 15: Call self.assertFalse()

```python
self.assertFalse(found, 'Removed document still found in search results')
```

### Step 16: Call new_note.delete()

```python
new_note.delete()
```

### Step 17: Assign found = True

```python
found = True
```

### Step 18: Assign found = True

```python
found = True
```


## Complete Example

```python
# Setup
'Set up test data for each test.'
super().setUp()
self.test_notes = []
self.test_todos = []
note_data = [{'title': 'Python Programming Guide', 'content': 'Learn Python basics and advanced concepts'}, {'title': 'Project Management Tips', 'content': 'How to manage software projects effectively'}, {'title': 'Cooking Recipe Collection', 'content': 'Delicious recipes for home cooking'}, {'title': 'Machine Learning Tutorial', 'content': 'Introduction to ML algorithms and Python implementation'}]
for data in note_data:
    note = frappe.get_doc({'doctype': 'Note', 'title': data['title'], 'content': data['content']})
    note.insert()
    self.test_notes.append(note)
todo_data = [{'description': 'Review Python code for search functionality'}, {'description': 'Update project documentation'}, {'description': 'Plan team meeting agenda'}]
for data in todo_data:
    todo = frappe.get_doc({'doctype': 'ToDo', 'description': data['description'], 'status': 'Open'})
    todo.insert()
    self.test_todos.append(todo)

# Workflow
'Test individual document indexing and removal operations.'
self.search.build_index()
new_note = frappe.get_doc({'doctype': 'Note', 'title': 'Newly Added Document', 'content': 'This document was added after initial indexing'})
new_note.insert()
try:
    results = self.search.search('Newly Added Document')
    initial_count = len(results['results'])
    self.search.index_doc('Note', new_note.name)
    results = self.search.search('Newly Added Document')
    self.assertGreater(len(results['results']), initial_count)
    found = False
    for result in results['results']:
        if result['name'] == new_note.name:
            found = True
            break
    self.assertTrue(found, 'Newly indexed document not found in search results')
    self.search.remove_doc('Note', new_note.name)
    results = self.search.search('Newly Added Document')
    found = False
    for result in results['results']:
        if result['name'] == new_note.name:
            found = True
            break
    self.assertFalse(found, 'Removed document still found in search results')
finally:
    new_note.delete()
```

## Next Steps


---

*Source: test_sqlite_search.py:311 | Complexity: Advanced | Last updated: 2026-02-04*