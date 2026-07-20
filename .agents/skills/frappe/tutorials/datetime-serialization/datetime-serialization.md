# How To: Datetime Serialization

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test datetime serialization

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

### Step 1: Assign dt = now_datetime(...)

```python
dt = now_datetime()
```

### Step 2: Assign dt = dt.replace(...)

```python
dt = dt.replace(microsecond=0)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(str(dt), str(frappe.db.sql('select %s', dt)[0][0]))
```

### Step 4: Call frappe.db.exists()

```python
frappe.db.exists('User', {'creation': ('>', dt)})
```

### Step 5: Call self.assertIn()

```python
self.assertIn(str(dt), str(frappe.db.last_query))
```

### Step 6: Assign before = now_datetime(...)

```python
before = now_datetime()
```

### Step 7: Assign note = frappe.get_doc.insert(...)

```python
note = frappe.get_doc(doctype='Note', title=frappe.generate_hash(), content='something').insert()
```

### Step 8: Assign after = now_datetime(...)

```python
after = now_datetime()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(note.name, frappe.db.exists('Note', {'creation': ('between', (before, after))}))
```


## Complete Example

```python
# Workflow
dt = now_datetime()
dt = dt.replace(microsecond=0)
self.assertEqual(str(dt), str(frappe.db.sql('select %s', dt)[0][0]))
frappe.db.exists('User', {'creation': ('>', dt)})
self.assertIn(str(dt), str(frappe.db.last_query))
before = now_datetime()
note = frappe.get_doc(doctype='Note', title=frappe.generate_hash(), content='something').insert()
after = now_datetime()
self.assertEqual(note.name, frappe.db.exists('Note', {'creation': ('between', (before, after))}))
```

## Next Steps


---

*Source: test_db.py:545 | Complexity: Advanced | Last updated: 2026-02-04*