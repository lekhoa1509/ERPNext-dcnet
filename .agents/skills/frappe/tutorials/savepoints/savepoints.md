# How To: Savepoints

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test savepoints

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

### Step 1: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 2: Assign save_point = 'todonope'

```python
save_point = 'todonope'
```

### Step 3: Assign created_docs = value

```python
created_docs = []
```

### Step 4: Assign failed_docs = value

```python
failed_docs = []
```

### Step 5: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 6: Call frappe.db.savepoint()

```python
frappe.db.savepoint(save_point)
```

### Step 7: Assign doc_gone = frappe.get_doc.save(...)

```python
doc_gone = frappe.get_doc(doctype='ToDo', description='nope').save()
```

### Step 8: Call failed_docs.append()

```python
failed_docs.append(doc_gone.name)
```

### Step 9: Call frappe.db.rollback()

```python
frappe.db.rollback(save_point=save_point)
```

### Step 10: Assign doc_kept = frappe.get_doc.save(...)

```python
doc_kept = frappe.get_doc(doctype='ToDo', description='nope').save()
```

### Step 11: Call created_docs.append()

```python
created_docs.append(doc_kept.name)
```

### Step 12: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('ToDo', d))
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('ToDo', d))
```


## Complete Example

```python
# Workflow
frappe.db.rollback()
save_point = 'todonope'
created_docs = []
failed_docs = []
for _ in range(5):
    frappe.db.savepoint(save_point)
    doc_gone = frappe.get_doc(doctype='ToDo', description='nope').save()
    failed_docs.append(doc_gone.name)
    frappe.db.rollback(save_point=save_point)
    doc_kept = frappe.get_doc(doctype='ToDo', description='nope').save()
    created_docs.append(doc_kept.name)
frappe.db.commit()
for d in failed_docs:
    self.assertFalse(frappe.db.exists('ToDo', d))
for d in created_docs:
    self.assertTrue(frappe.db.exists('ToDo', d))
```

## Next Steps


---

*Source: test_db.py:419 | Complexity: Advanced | Last updated: 2026-02-04*