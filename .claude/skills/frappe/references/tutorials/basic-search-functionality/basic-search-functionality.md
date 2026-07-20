# How To: Basic Search Functionality

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test core search functionality with various query types.

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

### Step 1: 'Test core search functionality with various query types.'

```python
'Test core search functionality with various query types.'
```

### Step 2: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 3: Assign results = self.search.search(...)

```python
results = self.search.search('Python')
```

### Step 4: Call self.assertGreater()

```python
self.assertGreater(len(results['results']), 0)
```

### Step 5: Call self.assertIn()

```python
self.assertIn('Python', results['results'][0]['title'] + results['results'][0]['content'])
```

### Step 6: Assign result = value

```python
result = results['results'][0]
```

### Step 7: Assign required_fields = value

```python
required_fields = ['id', 'title', 'content', 'doctype', 'name', 'score', 'original_rank', 'modified_rank']
```

### Step 8: Assign results_lower = self.search.search(...)

```python
results_lower = self.search.search('python')
```

### Step 9: Assign results_upper = self.search.search(...)

```python
results_upper = self.search.search('PYTHON')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(results_lower['results']), len(results_upper['results']))
```

### Step 11: Assign results = self.search.search(...)

```python
results = self.search.search('prog')
```

### Step 12: Call self.assertGreater()

```python
self.assertGreater(len(results['results']), 0)
```

### Step 13: Assign results = self.search.search(...)

```python
results = self.search.search('Python programming')
```

### Step 14: Call self.assertGreater()

```python
self.assertGreater(len(results['results']), 0)
```

### Step 15: Assign results = self.search.search(...)

```python
results = self.search.search('')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(results['results']), 0)
```

### Step 17: Assign results = self.search.search(...)

```python
results = self.search.search('Python', title_only=True)
```

### Step 18: Call self.assertGreater()

```python
self.assertGreater(len(results['results']), 0)
```

### Step 19: Call self.assertIn()

```python
self.assertIn(field, result)
```

### Step 20: Call self.assertIn()

```python
self.assertIn('Python', result['title'])
```


## Complete Example

```python
# Workflow
'Test core search functionality with various query types.'
self.search.build_index()
results = self.search.search('Python')
self.assertGreater(len(results['results']), 0)
self.assertIn('Python', results['results'][0]['title'] + results['results'][0]['content'])
result = results['results'][0]
required_fields = ['id', 'title', 'content', 'doctype', 'name', 'score', 'original_rank', 'modified_rank']
for field in required_fields:
    self.assertIn(field, result)
results_lower = self.search.search('python')
results_upper = self.search.search('PYTHON')
self.assertEqual(len(results_lower['results']), len(results_upper['results']))
results = self.search.search('prog')
self.assertGreater(len(results['results']), 0)
results = self.search.search('Python programming')
self.assertGreater(len(results['results']), 0)
results = self.search.search('')
self.assertEqual(len(results['results']), 0)
results = self.search.search('Python', title_only=True)
self.assertGreater(len(results['results']), 0)
for result in results['results']:
    self.assertIn('Python', result['title'])
```

## Next Steps


---

*Source: test_sqlite_search.py:163 | Complexity: Advanced | Last updated: 2026-02-04*