# How To: Transaction Writes Error

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test transaction writes error

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

### Step 2: Assign frappe.db.MAX_WRITES_PER_TRANSACTION = 1

```python
frappe.db.MAX_WRITES_PER_TRANSACTION = 1
```

### Step 3: Assign note = frappe.get_last_doc(...)

```python
note = frappe.get_last_doc('ToDo')
```

### Step 4: Assign note.description = 'changed'

```python
note.description = 'changed'
```

### Step 5: Assign frappe.db.MAX_WRITES_PER_TRANSACTION = value

```python
frappe.db.MAX_WRITES_PER_TRANSACTION = Database.MAX_WRITES_PER_TRANSACTION
```

### Step 6: Call note.save()

```python
note.save()
```


## Complete Example

```python
# Workflow
from frappe.database.database import Database
frappe.db.rollback()
frappe.db.MAX_WRITES_PER_TRANSACTION = 1
note = frappe.get_last_doc('ToDo')
note.description = 'changed'
with self.assertRaises(frappe.TooManyWritesError):
    note.save()
frappe.db.MAX_WRITES_PER_TRANSACTION = Database.MAX_WRITES_PER_TRANSACTION
```

## Next Steps


---

*Source: test_db.py:466 | Complexity: Intermediate | Last updated: 2026-02-04*