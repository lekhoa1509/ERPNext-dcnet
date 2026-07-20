# How To: Search Filtering And Permissions

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test search filtering and permission-based result filtering.

## Prerequisites

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


## Step-by-Step Guide

### Step 1: 'Test search filtering and permission-based result filtering.'

```python
'Test search filtering and permission-based result filtering.'
```

### Step 2: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 3: Assign results = self.search.search(...)

```python
results = self.search.search('', filters={'doctype': 'Note'})
```

### Step 4: Assign results = self.search.search(...)

```python
results = self.search.search('', filters={'doctype': ['Note', 'ToDo']})
```

### Step 5: Assign results = self.search.search(...)

```python
results = self.search.search('', filters={'doctype': []})
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(results['results']), 0)
```

### Step 7: Assign original_user = value

```python
original_user = frappe.session.user
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(result['doctype'], 'Note')
```

### Step 9: Call self.assertIn()

```python
self.assertIn(result['doctype'], ['Note', 'ToDo'])
```

### Step 10: Assign test_user_email = 'test_search_user@example.com'

```python
test_user_email = 'test_search_user@example.com'
```

### Step 11: Call frappe.set_user()

```python
frappe.set_user(test_user_email)
```

### Step 12: Assign results = self.search.search(...)

```python
results = self.search.search('Python')
```

### Step 13: Call self.assertIsInstance()

```python
self.assertIsInstance(results['results'], list)
```

### Step 14: Call frappe.set_user()

```python
frappe.set_user(original_user)
```

### Step 15: Assign test_user = frappe.get_doc(...)

```python
test_user = frappe.get_doc({'doctype': 'User', 'email': test_user_email, 'first_name': 'Test', 'last_name': 'User', 'enabled': 1})
```

### Step 16: Call test_user.insert()

```python
test_user.insert()
```


## Complete Example

```python
# Workflow
'Test search filtering and permission-based result filtering.'
self.search.build_index()
results = self.search.search('', filters={'doctype': 'Note'})
for result in results['results']:
    self.assertEqual(result['doctype'], 'Note')
results = self.search.search('', filters={'doctype': ['Note', 'ToDo']})
for result in results['results']:
    self.assertIn(result['doctype'], ['Note', 'ToDo'])
results = self.search.search('', filters={'doctype': []})
self.assertEqual(len(results['results']), 0)
original_user = frappe.session.user
try:
    test_user_email = 'test_search_user@example.com'
    if not frappe.db.exists('User', test_user_email):
        test_user = frappe.get_doc({'doctype': 'User', 'email': test_user_email, 'first_name': 'Test', 'last_name': 'User', 'enabled': 1})
        test_user.insert()
    frappe.set_user(test_user_email)
    results = self.search.search('Python')
    self.assertIsInstance(results['results'], list)
finally:
    frappe.set_user(original_user)
```

## Next Steps


---

*Source: test_sqlite_search.py:211 | Complexity: Advanced | Last updated: 2026-02-04*