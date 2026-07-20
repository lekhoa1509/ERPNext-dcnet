# How To: Search Result Summary And Metadata

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test search result summary and metadata information.

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

### Step 1: 'Test search result summary and metadata information.'

```python
'Test search result summary and metadata information.'
```

### Step 2: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 3: Assign results = self.search.search(...)

```python
results = self.search.search('Python')
```

### Step 4: Assign summary = value

```python
summary = results['summary']
```

### Step 5: Assign required_summary_fields = value

```python
required_summary_fields = ['total_matches', 'filtered_matches', 'returned_matches', 'duration', 'title_only', 'applied_filters']
```

### Step 6: Call self.assertIsInstance()

```python
self.assertIsInstance(summary['duration'], (int, float))
```

### Step 7: Call self.assertGreater()

```python
self.assertGreater(summary['duration'], 0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(summary['total_matches'], summary['filtered_matches'])
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(summary['filtered_matches'], len(results['results']))
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(summary['title_only'])
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(summary['applied_filters'], {})
```

### Step 12: Assign results = self.search.search(...)

```python
results = self.search.search('Python', filters={'doctype': 'Note'})
```

### Step 13: Assign summary = value

```python
summary = results['summary']
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(summary['applied_filters'], {'doctype': 'Note'})
```

### Step 15: Assign results = self.search.search(...)

```python
results = self.search.search('Python', title_only=True)
```

### Step 16: Assign summary = value

```python
summary = results['summary']
```

### Step 17: Call self.assertTrue()

```python
self.assertTrue(summary['title_only'])
```

### Step 18: Call self.assertIn()

```python
self.assertIn(field, summary)
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
'Test search result summary and metadata information.'
self.search.build_index()
results = self.search.search('Python')
summary = results['summary']
required_summary_fields = ['total_matches', 'filtered_matches', 'returned_matches', 'duration', 'title_only', 'applied_filters']
for field in required_summary_fields:
    self.assertIn(field, summary)
self.assertIsInstance(summary['duration'], (int, float))
self.assertGreater(summary['duration'], 0)
self.assertEqual(summary['total_matches'], summary['filtered_matches'])
self.assertEqual(summary['filtered_matches'], len(results['results']))
self.assertFalse(summary['title_only'])
self.assertEqual(summary['applied_filters'], {})
results = self.search.search('Python', filters={'doctype': 'Note'})
summary = results['summary']
self.assertEqual(summary['applied_filters'], {'doctype': 'Note'})
results = self.search.search('Python', title_only=True)
summary = results['summary']
self.assertTrue(summary['title_only'])
```

## Next Steps


---

*Source: test_sqlite_search.py:360 | Complexity: Advanced | Last updated: 2026-02-04*