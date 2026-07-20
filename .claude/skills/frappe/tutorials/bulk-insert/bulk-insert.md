# How To: Bulk Insert

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk insert

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

### Step 1: Assign current_count = frappe.db.count(...)

```python
current_count = frappe.db.count('ToDo')
```

### Step 2: Assign test_body = value

```python
test_body = f'test_bulk_insert - {random_string(10)}'
```

### Step 3: Assign chunk_size = 10

```python
chunk_size = 10
```

### Step 4: Call frappe.db.delete()

```python
frappe.db.delete('ToDo', {'description': test_body})
```

### Step 5: Assign current_transaction_writes = value

```python
current_transaction_writes = frappe.db.transaction_writes
```

### Step 6: Call frappe.db.bulk_insert()

```python
frappe.db.bulk_insert('ToDo', ['name', 'description'], [[f'ToDo Test Bulk Insert {i}', test_body] for i in range(number_of_values)], ignore_duplicates=True, chunk_size=chunk_size)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(number_of_values, frappe.db.count('ToDo') - current_count)
```

### Step 8: Assign expected_number_of_writes = ceil(...)

```python
expected_number_of_writes = ceil(number_of_values / chunk_size)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(expected_number_of_writes, frappe.db.transaction_writes - current_transaction_writes)
```


## Complete Example

```python
# Workflow
current_count = frappe.db.count('ToDo')
test_body = f'test_bulk_insert - {random_string(10)}'
chunk_size = 10
for number_of_values in (1, 2, 5, 27):
    current_transaction_writes = frappe.db.transaction_writes
    frappe.db.bulk_insert('ToDo', ['name', 'description'], [[f'ToDo Test Bulk Insert {i}', test_body] for i in range(number_of_values)], ignore_duplicates=True, chunk_size=chunk_size)
    self.assertEqual(number_of_values, frappe.db.count('ToDo') - current_count)
    expected_number_of_writes = ceil(number_of_values / chunk_size)
    self.assertEqual(expected_number_of_writes, frappe.db.transaction_writes - current_transaction_writes)
frappe.db.delete('ToDo', {'description': test_body})
```

## Next Steps


---

*Source: test_db.py:558 | Complexity: Advanced | Last updated: 2026-02-04*