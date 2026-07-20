# How To: Index Lifecycle And Status Methods

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test index building, existence checking, and status validation.

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

### Step 1: 'Test index building, existence checking, and status validation.'

```python
'Test index building, existence checking, and status validation.'
```

### Step 2: Call self.search.drop_index()

```python
self.search.drop_index()
```

### Step 3: Call self.assertFalse()

```python
self.assertFalse(self.search.index_exists())
```

### Step 4: Call self.search.build_index()

```python
self.search.build_index()
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(self.search.index_exists())
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(self.search.db_path))
```

### Step 7: Assign conn = sqlite3.connect(...)

```python
conn = sqlite3.connect(self.search.db_path)
```

### Step 8: Assign cursor = conn.cursor(...)

```python
cursor = conn.cursor()
```

### Step 9: Call cursor.execute()

```python
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_fts'")
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(cursor.fetchone())
```

### Step 11: Call cursor.execute()

```python
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_vocabulary'")
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(cursor.fetchone())
```

### Step 13: Call cursor.execute()

```python
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_trigrams'")
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(cursor.fetchone())
```

### Step 15: Call conn.close()

```python
conn.close()
```

### Step 16: Call self.search.drop_index()

```python
self.search.drop_index()
```

### Step 17: Call self.assertFalse()

```python
self.assertFalse(self.search.index_exists())
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(os.path.exists(self.search.db_path))
```

### Step 19: Call self.search.drop_index()

```python
self.search.drop_index()
```

### Step 20: Call self.search.raise_if_not_indexed()

```python
self.search.raise_if_not_indexed()
```

### Step 21: Call self.search.raise_if_not_indexed()

```python
self.search.raise_if_not_indexed()
```

### Step 22: Call self.fail()

```python
self.fail('raise_if_not_indexed() raised exception when index exists')
```


## Complete Example

```python
# Workflow
'Test index building, existence checking, and status validation.'
self.search.drop_index()
self.assertFalse(self.search.index_exists())
with self.assertRaises(SQLiteSearchIndexMissingError):
    self.search.raise_if_not_indexed()
self.search.build_index()
self.assertTrue(self.search.index_exists())
try:
    self.search.raise_if_not_indexed()
except SQLiteSearchIndexMissingError:
    self.fail('raise_if_not_indexed() raised exception when index exists')
self.assertTrue(os.path.exists(self.search.db_path))
conn = sqlite3.connect(self.search.db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_fts'")
self.assertTrue(cursor.fetchone())
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_vocabulary'")
self.assertTrue(cursor.fetchone())
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_trigrams'")
self.assertTrue(cursor.fetchone())
conn.close()
self.search.drop_index()
self.assertFalse(self.search.index_exists())
self.assertFalse(os.path.exists(self.search.db_path))
self.search.drop_index()
```

## Next Steps


---

*Source: test_sqlite_search.py:114 | Complexity: Advanced | Last updated: 2026-02-04*