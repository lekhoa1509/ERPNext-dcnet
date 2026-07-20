# How To: Content Processing And Html Handling

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test content processing including HTML tag removal and text normalization.

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

### Step 1: 'Test content processing including HTML tag removal and text normalization.'

```python
'Test content processing including HTML tag removal and text normalization.'
```

### Step 2: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 3: Assign html_note = frappe.get_doc(...)

```python
html_note = frappe.get_doc({'doctype': 'Note', 'title': 'HTML Content Test', 'content': "<p>This is <strong>bold</strong> text with <a href='http://example.com'>links</a> and <br> line breaks.</p>"})
```

### Step 4: Call html_note.insert()

```python
html_note.insert()
```

### Step 5: Call self.search.index_doc()

```python
self.search.index_doc('Note', html_note.name)
```

### Step 6: Assign results = self.search.search(...)

```python
results = self.search.search('bold text links')
```

### Step 7: Assign found = False

```python
found = False
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(found, 'HTML content document not found in search')
```

### Step 9: Call html_note.delete()

```python
html_note.delete()
```

### Step 10: Assign found = True

```python
found = True
```

### Step 11: Call self.assertNotIn()

```python
self.assertNotIn('<p>', result['content'])
```

### Step 12: Call self.assertNotIn()

```python
self.assertNotIn('<strong>', result['content'])
```

### Step 13: Call self.assertIn()

```python
self.assertIn('bold', result['content'])
```

### Step 14: Call self.assertNotIn()

```python
self.assertNotIn("<a href='http://example.com'>", result['content'])
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
'Test content processing including HTML tag removal and text normalization.'
self.search.build_index()
html_note = frappe.get_doc({'doctype': 'Note', 'title': 'HTML Content Test', 'content': "<p>This is <strong>bold</strong> text with <a href='http://example.com'>links</a> and <br> line breaks.</p>"})
html_note.insert()
try:
    self.search.index_doc('Note', html_note.name)
    results = self.search.search('bold text links')
    found = False
    for result in results['results']:
        if result['name'] == html_note.name:
            found = True
            self.assertNotIn('<p>', result['content'])
            self.assertNotIn('<strong>', result['content'])
            self.assertIn('bold', result['content'])
            self.assertNotIn("<a href='http://example.com'>", result['content'])
            break
    self.assertTrue(found, 'HTML content document not found in search')
finally:
    html_note.delete()
```

## Next Steps


---

*Source: test_sqlite_search.py:427 | Complexity: Advanced | Last updated: 2026-02-04*