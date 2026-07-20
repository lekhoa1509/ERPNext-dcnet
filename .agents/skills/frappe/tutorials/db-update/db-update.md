# How To: Db Update

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test db update

## Prerequisites

**Required Modules:**
- `random`
- `unittest.case`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.utils`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.database.schema`


## Step-by-Step Guide

### Step 1: Assign doctype = 'User'

```python
doctype = 'User'
```

### Step 2: Call frappe.reload_doctype()

```python
frappe.reload_doctype('User', force=True)
```

### Step 3: Call frappe.model.meta.trim_tables()

```python
frappe.model.meta.trim_tables('User')
```

### Step 4: Call make_property_setter()

```python
make_property_setter(doctype, 'bio', 'fieldtype', 'Text', 'Data')
```

### Step 5: Call make_property_setter()

```python
make_property_setter(doctype, 'middle_name', 'fieldtype', 'Data', 'Text')
```

### Step 6: Call make_property_setter()

```python
make_property_setter(doctype, 'enabled', 'default', '1', 'Int')
```

### Step 7: Call frappe.db.updatedb()

```python
frappe.db.updatedb(doctype)
```

### Step 8: Assign field_defs = get_field_defs(...)

```python
field_defs = get_field_defs(doctype)
```

### Step 9: Assign table_columns = frappe.db.get_table_columns_description(...)

```python
table_columns = frappe.db.get_table_columns_description(f'tab{doctype}')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(field_defs), len(table_columns))
```

### Step 11: Assign fieldname = field_def.get(...)

```python
fieldname = field_def.get('fieldname')
```

### Step 12: Assign table_column = find(...)

```python
table_column = find(table_columns, lambda d: d.get('name') == fieldname)
```

### Step 13: Assign fieldtype = get_fieldtype_from_def(...)

```python
fieldtype = get_fieldtype_from_def(field_def)
```

### Step 14: Assign fallback_default = value

```python
fallback_default = '0' if field_def.get('fieldtype') in frappe.model.numeric_fieldtypes else 'NULL'
```

### Step 15: Assign default = value

```python
default = field_def.default if field_def.default is not None else fallback_default
```

### Step 16: Call self.assertIn()

```python
self.assertIn(fieldtype, table_column.type, msg=f'Types not matching for {fieldname}')
```

### Step 17: Call self.assertIn()

```python
self.assertIn(cstr(table_column.default) or 'NULL', [cstr(default), f"'{default}'"])
```


## Complete Example

```python
# Workflow
doctype = 'User'
frappe.reload_doctype('User', force=True)
frappe.model.meta.trim_tables('User')
make_property_setter(doctype, 'bio', 'fieldtype', 'Text', 'Data')
make_property_setter(doctype, 'middle_name', 'fieldtype', 'Data', 'Text')
make_property_setter(doctype, 'enabled', 'default', '1', 'Int')
frappe.db.updatedb(doctype)
field_defs = get_field_defs(doctype)
table_columns = frappe.db.get_table_columns_description(f'tab{doctype}')
self.assertEqual(len(field_defs), len(table_columns))
for field_def in field_defs:
    fieldname = field_def.get('fieldname')
    table_column = find(table_columns, lambda d: d.get('name') == fieldname)
    fieldtype = get_fieldtype_from_def(field_def)
    fallback_default = '0' if field_def.get('fieldtype') in frappe.model.numeric_fieldtypes else 'NULL'
    default = field_def.default if field_def.default is not None else fallback_default
    self.assertIn(fieldtype, table_column.type, msg=f'Types not matching for {fieldname}')
    self.assertIn(cstr(table_column.default) or 'NULL', [cstr(default), f"'{default}'"])
```

## Next Steps


---

*Source: test_db_update.py:15 | Complexity: Advanced | Last updated: 2026-02-04*