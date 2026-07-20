# How To: Making Sequence On Change

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test making sequence on change

## Prerequisites

**Required Modules:**
- `os`
- `random`
- `string`
- `unittest`
- `unittest.case`
- `unittest.mock`
- `frappe`
- `frappe.cache_manager`
- `frappe.core.doctype.doctype.doctype`
- `frappe.core.doctype.rq_job.test_rq_job`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.desk.form.load`
- `frappe.model.delete_doc`
- `frappe.model.sync`
- `frappe.tests`
- `frappe.utils`
- `re`
- `os`
- `frappe.modules.import_file`
- `json`
- `frappe.desk.form.linked_with`
- `json`
- `frappe.desk.form.linked_with`
- `json`
- `ast`
- `frappe.types.exporter`
- `frappe.custom.doctype.property_setter.property_setter`


## Step-by-Step Guide

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('DocType', self._testMethodName)
```

### Step 2: Assign dt = new_doctype.insert(...)

```python
dt = new_doctype(self._testMethodName).insert(ignore_permissions=True)
```

### Step 3: Assign autoname = value

```python
autoname = dt.autoname
```

### Step 4: Assign dt.autoname = 'autoincrement'

```python
dt.autoname = 'autoincrement'
```

### Step 5: Call dt.save()

```python
dt.save()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(frappe.db.sql(f"select data_type FROM information_schema.columns\n\t\t\t\twhere column_name = 'name' and table_name = 'tab{self._testMethodName}'")[0][0], 'bigint')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(frappe.db.sql(f'select * from {table_name}\n\t\t\t\twhere {conditions}'))
```

### Step 8: Assign dt.autoname = autoname

```python
dt.autoname = autoname
```

### Step 9: Call dt.save()

```python
dt.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(frappe.db.sql(f"select data_type FROM information_schema.columns\n\t\t\t\twhere column_name = 'name' and table_name = 'tab{self._testMethodName}'")[0][0], 'varchar' if frappe.db.db_type == 'mariadb' else 'character varying')
```

### Step 11: Assign table_name = 'information_schema.tables'

```python
table_name = 'information_schema.tables'
```

### Step 12: Assign conditions = value

```python
conditions = f"table_type = 'sequence' and table_name = '{self._testMethodName}_id_seq'"
```

### Step 13: Assign table_name = 'information_schema.sequences'

```python
table_name = 'information_schema.sequences'
```

### Step 14: Assign conditions = value

```python
conditions = f"sequence_name = '{self._testMethodName}_id_seq'"
```


## Complete Example

```python
# Workflow
frappe.delete_doc_if_exists('DocType', self._testMethodName)
dt = new_doctype(self._testMethodName).insert(ignore_permissions=True)
autoname = dt.autoname
dt.autoname = 'autoincrement'
dt.save()
self.assertEqual(frappe.db.sql(f"select data_type FROM information_schema.columns\n\t\t\t\twhere column_name = 'name' and table_name = 'tab{self._testMethodName}'")[0][0], 'bigint')
if frappe.db.db_type == 'mariadb':
    table_name = 'information_schema.tables'
    conditions = f"table_type = 'sequence' and table_name = '{self._testMethodName}_id_seq'"
else:
    table_name = 'information_schema.sequences'
    conditions = f"sequence_name = '{self._testMethodName}_id_seq'"
self.assertTrue(frappe.db.sql(f'select * from {table_name}\n\t\t\t\twhere {conditions}'))
dt.autoname = autoname
dt.save()
self.assertEqual(frappe.db.sql(f"select data_type FROM information_schema.columns\n\t\t\t\twhere column_name = 'name' and table_name = 'tab{self._testMethodName}'")[0][0], 'varchar' if frappe.db.db_type == 'mariadb' else 'character varying')
```

## Next Steps


---

*Source: test_doctype.py:55 | Complexity: Advanced | Last updated: 2026-02-04*