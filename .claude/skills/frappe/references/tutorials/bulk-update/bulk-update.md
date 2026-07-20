# How To: Bulk Update

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk update

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

### Step 1: Assign test_body = value

```python
test_body = f'test_bulk_update - {random_string(10)}'
```

### Step 2: Call frappe.db.bulk_insert()

```python
frappe.db.bulk_insert('ToDo', ['name', 'description'], [[f'ToDo Test Bulk Update {i}', test_body] for i in range(20)], ignore_duplicates=True)
```

### Step 3: Assign record_names = frappe.get_all(...)

```python
record_names = frappe.get_all('ToDo', filters={'description': test_body}, pluck='name')
```

### Step 4: Assign new_descriptions = value

```python
new_descriptions = {name: f'{test_body} - updated - {random_string(10)}' for name in record_names}
```

### Step 5: Call frappe.db.bulk_update()

```python
frappe.db.bulk_update('ToDo', {name: {'description': new_descriptions[name]} for name in record_names})
```

### Step 6: Assign updated_records = dict(...)

```python
updated_records = dict(frappe.get_all('ToDo', filters={'name': ('in', record_names)}, fields=['name', 'description'], as_list=True))
```

### Step 7: Call self.assertDictEqual()

```python
self.assertDictEqual(new_descriptions, updated_records)
```

### Step 8: Assign updates = value

```python
updates = {record_names[0]: {'priority': 'High', 'status': 'Closed'}, record_names[1]: {'status': 'Closed'}}
```

### Step 9: Call frappe.db.bulk_update()

```python
frappe.db.bulk_update('ToDo', updates)
```

### Step 10: Assign unknown = frappe.db.get_value(...)

```python
priority, status = frappe.db.get_value('ToDo', record_names[0], ['priority', 'status'])
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(priority, 'High')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(status, 'Closed')
```

### Step 13: Assign updates = value

```python
updates = {record_names[0]: {'status': 'Open'}, record_names[1]: {'priority': 'Low'}}
```

### Step 14: Call frappe.db.bulk_update()

```python
frappe.db.bulk_update('ToDo', updates)
```

### Step 15: Assign unknown = frappe.db.get_value(...)

```python
priority, status = frappe.db.get_value('ToDo', record_names[0], ['priority', 'status'])
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(priority, 'High')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(status, 'Open')
```

### Step 18: Assign unknown = frappe.db.get_value(...)

```python
priority, status = frappe.db.get_value('ToDo', record_names[1], ['priority', 'status'])
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(priority, 'Low')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(status, 'Closed')
```

### Step 21: Call frappe.db.delete()

```python
frappe.db.delete('ToDo', {'name': ('in', record_names)})
```


## Complete Example

```python
# Workflow
test_body = f'test_bulk_update - {random_string(10)}'
frappe.db.bulk_insert('ToDo', ['name', 'description'], [[f'ToDo Test Bulk Update {i}', test_body] for i in range(20)], ignore_duplicates=True)
record_names = frappe.get_all('ToDo', filters={'description': test_body}, pluck='name')
new_descriptions = {name: f'{test_body} - updated - {random_string(10)}' for name in record_names}
frappe.db.bulk_update('ToDo', {name: {'description': new_descriptions[name]} for name in record_names})
updated_records = dict(frappe.get_all('ToDo', filters={'name': ('in', record_names)}, fields=['name', 'description'], as_list=True))
self.assertDictEqual(new_descriptions, updated_records)
updates = {record_names[0]: {'priority': 'High', 'status': 'Closed'}, record_names[1]: {'status': 'Closed'}}
frappe.db.bulk_update('ToDo', updates)
priority, status = frappe.db.get_value('ToDo', record_names[0], ['priority', 'status'])
self.assertEqual(priority, 'High')
self.assertEqual(status, 'Closed')
updates = {record_names[0]: {'status': 'Open'}, record_names[1]: {'priority': 'Low'}}
frappe.db.bulk_update('ToDo', updates)
priority, status = frappe.db.get_value('ToDo', record_names[0], ['priority', 'status'])
self.assertEqual(priority, 'High')
self.assertEqual(status, 'Open')
priority, status = frappe.db.get_value('ToDo', record_names[1], ['priority', 'status'])
self.assertEqual(priority, 'Low')
self.assertEqual(status, 'Closed')
frappe.db.delete('ToDo', {'name': ('in', record_names)})
```

## Next Steps


---

*Source: test_db.py:585 | Complexity: Advanced | Last updated: 2026-02-04*