# How To: Log Touched Tables

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test log touched tables

## Prerequisites

**Required Modules:**
- `datetime`
- `math`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.core.utils`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.database`
- `frappe.database.database`
- `frappe.database.utils`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.data`
- `frappe.utils.testutils`
- `frappe.database.database`
- `frappe.database.postgres.database`
- `frappe.database.postgres.database`
- `psycopg2.errors`
- `frappe.core.doctype.doctype.test_doctype`
- `contextlib`
- `os`
- `re`
- `frappe.database.postgres.database`


## Step-by-Step Guide

### Step 1: Assign frappe.flags.in_migrate = True

```python
frappe.flags.in_migrate = True
```

### Step 2: Assign frappe.flags.touched_tables = set(...)

```python
frappe.flags.touched_tables = set()
```

### Step 3: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('System Settings', 'backup_limit', 5)
```

### Step 4: Call self.assertIn()

```python
self.assertIn('tabSingles', frappe.flags.touched_tables)
```

### Step 5: Assign frappe.flags.touched_tables = set(...)

```python
frappe.flags.touched_tables = set()
```

### Step 6: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'Random Description'})
```

### Step 7: Call todo.save()

```python
todo.save()
```

### Step 8: Call self.assertIn()

```python
self.assertIn('tabToDo', frappe.flags.touched_tables)
```

### Step 9: Assign frappe.flags.touched_tables = set(...)

```python
frappe.flags.touched_tables = set()
```

### Step 10: Assign todo.description = 'Another Description'

```python
todo.description = 'Another Description'
```

### Step 11: Call todo.save()

```python
todo.save()
```

### Step 12: Call self.assertIn()

```python
self.assertIn('tabToDo', frappe.flags.touched_tables)
```

### Step 13: Assign frappe.flags.touched_tables = set(...)

```python
frappe.flags.touched_tables = set()
```

### Step 14: Call todo.delete()

```python
todo.delete()
```

### Step 15: Call self.assertIn()

```python
self.assertIn('tabToDo', frappe.flags.touched_tables)
```

### Step 16: Assign frappe.flags.touched_tables = set(...)

```python
frappe.flags.touched_tables = set()
```

### Step 17: Assign cf = create_custom_field(...)

```python
cf = create_custom_field('ToDo', {'label': 'ToDo Custom Field'})
```

### Step 18: Call self.assertIn()

```python
self.assertIn('tabToDo', frappe.flags.touched_tables)
```

### Step 19: Call self.assertIn()

```python
self.assertIn('tabCustom Field', frappe.flags.touched_tables)
```

### Step 20: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 21: Assign frappe.flags.in_migrate = False

```python
frappe.flags.in_migrate = False
```

### Step 22: Call frappe.flags.touched_tables.clear()

```python
frappe.flags.touched_tables.clear()
```

### Step 23: Assign frappe.flags.touched_tables = set(...)

```python
frappe.flags.touched_tables = set()
```

### Step 24: Call frappe.db.sql()

```python
frappe.db.sql("UPDATE tabToDo SET description = 'Updated Description'")
```

### Step 25: Call self.assertNotIn()

```python
self.assertNotIn('tabToDo SET', frappe.flags.touched_tables)
```

### Step 26: Call self.assertIn()

```python
self.assertIn('tabToDo', frappe.flags.touched_tables)
```

### Step 27: Call cf.delete()

```python
cf.delete()
```


## Complete Example

```python
# Workflow
frappe.flags.in_migrate = True
frappe.flags.touched_tables = set()
frappe.db.set_single_value('System Settings', 'backup_limit', 5)
self.assertIn('tabSingles', frappe.flags.touched_tables)
frappe.flags.touched_tables = set()
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'Random Description'})
todo.save()
self.assertIn('tabToDo', frappe.flags.touched_tables)
frappe.flags.touched_tables = set()
todo.description = 'Another Description'
todo.save()
self.assertIn('tabToDo', frappe.flags.touched_tables)
if frappe.db.db_type != 'postgres':
    frappe.flags.touched_tables = set()
    frappe.db.sql("UPDATE tabToDo SET description = 'Updated Description'")
    self.assertNotIn('tabToDo SET', frappe.flags.touched_tables)
    self.assertIn('tabToDo', frappe.flags.touched_tables)
frappe.flags.touched_tables = set()
todo.delete()
self.assertIn('tabToDo', frappe.flags.touched_tables)
frappe.flags.touched_tables = set()
cf = create_custom_field('ToDo', {'label': 'ToDo Custom Field'})
self.assertIn('tabToDo', frappe.flags.touched_tables)
self.assertIn('tabCustom Field', frappe.flags.touched_tables)
if cf:
    cf.delete()
frappe.db.commit()
frappe.flags.in_migrate = False
frappe.flags.touched_tables.clear()
```

## Next Steps


---

*Source: test_db.py:217 | Complexity: Advanced | Last updated: 2026-02-04*