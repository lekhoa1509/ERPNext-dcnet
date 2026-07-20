# How To: Advanced Scoring And Ranking

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test scoring pipeline, ranking, and result ordering.

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

### Step 1: 'Test scoring pipeline, ranking, and result ordering.'

```python
'Test scoring pipeline, ranking, and result ordering.'
```

### Step 2: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 3: Assign results = self.search.search(...)

```python
results = self.search.search('Python')
```

### Step 4: Assign scores = value

```python
scores = [result['score'] for result in results['results']]
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(scores, sorted(scores, reverse=True))
```

### Step 6: Assign results = self.search.search(...)

```python
results = self.search.search('Programming')
```

### Step 7: Assign title_match_found = False

```python
title_match_found = False
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(title_match_found, 'No title matches found for scoring test')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(result['modified_rank'], i + 1)
```

### Step 10: Call self.assertIsInstance()

```python
self.assertIsInstance(result['original_rank'], int)
```

### Step 11: Call self.assertGreater()

```python
self.assertGreater(result['original_rank'], 0)
```

### Step 12: Call self.assertIn()

```python
self.assertIn('bm25_score', result)
```

### Step 13: Call self.assertIsInstance()

```python
self.assertIsInstance(result['bm25_score'], (int, float))
```

### Step 14: Assign title_match_found = True

```python
title_match_found = True
```

### Step 15: Call self.assertGreater()

```python
self.assertGreater(result['score'], 1.0)
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
'Test scoring pipeline, ranking, and result ordering.'
self.search.build_index()
results = self.search.search('Python')
scores = [result['score'] for result in results['results']]
self.assertEqual(scores, sorted(scores, reverse=True))
for i, result in enumerate(results['results']):
    self.assertEqual(result['modified_rank'], i + 1)
    self.assertIsInstance(result['original_rank'], int)
    self.assertGreater(result['original_rank'], 0)
results = self.search.search('Programming')
title_match_found = False
for result in results['results']:
    if 'Programming' in result['title']:
        title_match_found = True
        self.assertGreater(result['score'], 1.0)
        break
self.assertTrue(title_match_found, 'No title matches found for scoring test')
for result in results['results']:
    self.assertIn('bm25_score', result)
    self.assertIsInstance(result['bm25_score'], (int, float))
```

## Next Steps


---

*Source: test_sqlite_search.py:256 | Complexity: Advanced | Last updated: 2026-02-04*