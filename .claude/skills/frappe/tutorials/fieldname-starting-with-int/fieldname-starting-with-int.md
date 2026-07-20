# How To: Fieldname Starting With Int

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test fieldname starting with int

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `contextlib`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.database.utils`
- `frappe.desk.reportview`
- `frappe.handler`
- `frappe.model.db_query`
- `frappe.permissions`
- `frappe.query_builder`
- `frappe.tests`
- `frappe.tests.test_helpers`
- `frappe.tests.test_query_builder`
- `frappe.utils.testutils`
- `frappe.utils`
- `frappe.desk.search`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.dashboard_settings.dashboard_settings`
- `frappe.desk.reportview`
- `frappe.desk`
- `frappe.types.filter`

**Setup Required:**
```python
setup_for_tests()
frappe.set_user('Administrator')
```

## Step-by-Step Guide

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('DocType', 'dt_with_int_named_fieldname')
```

### Step 2: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('DocType', 'table_dt')
```

### Step 3: Assign table_dt = new_doctype.insert(...)

```python
table_dt = new_doctype('table_dt', istable=1, fields=[{'label': '1field', 'fieldname': '2field', 'fieldtype': 'Data'}]).insert()
```

### Step 4: Assign dt = new_doctype.insert(...)

```python
dt = new_doctype('dt_with_int_named_fieldname', fields=[{'label': '1field', 'fieldname': '1field', 'fieldtype': 'Data'}, {'label': '2table_field', 'fieldname': '2table_field', 'fieldtype': 'Table', 'options': table_dt.name}]).insert(ignore_permissions=True)
```

### Step 5: Assign dt_data = frappe.get_doc.insert(...)

```python
dt_data = frappe.get_doc({'doctype': 'dt_with_int_named_fieldname', '1field': '10'}).insert(ignore_permissions=True)
```

### Step 6: Assign query = DatabaseQuery(...)

```python
query = DatabaseQuery('dt_with_int_named_fieldname')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(query.execute(filters={'1field': '10'}))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(query.execute(filters={'1field': ['like', '1%']}))
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(query.execute(filters={'1field': ['in', '1,2,10']}))
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(query.execute(filters={'1field': ['is', 'set']}))
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(query.execute(filters={'1field': ['not like', '1%']}))
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(query.execute(filters=[['table_dt', '2field', 'is', 'not set']]))
```

### Step 13: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': table_dt.name, '2field': '10', 'parent': dt_data.name, 'parenttype': dt_data.doctype, 'parentfield': '2table_field'}).insert(ignore_permissions=True)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(query.execute(filters=[['table_dt', '2field', 'is', 'set']]))
```

### Step 15: Call dt.delete()

```python
dt.delete()
```

### Step 16: Call table_dt.delete()

```python
table_dt.delete()
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
from frappe.core.doctype.doctype.test_doctype import new_doctype
frappe.delete_doc_if_exists('DocType', 'dt_with_int_named_fieldname')
frappe.delete_doc_if_exists('DocType', 'table_dt')
table_dt = new_doctype('table_dt', istable=1, fields=[{'label': '1field', 'fieldname': '2field', 'fieldtype': 'Data'}]).insert()
dt = new_doctype('dt_with_int_named_fieldname', fields=[{'label': '1field', 'fieldname': '1field', 'fieldtype': 'Data'}, {'label': '2table_field', 'fieldname': '2table_field', 'fieldtype': 'Table', 'options': table_dt.name}]).insert(ignore_permissions=True)
dt_data = frappe.get_doc({'doctype': 'dt_with_int_named_fieldname', '1field': '10'}).insert(ignore_permissions=True)
query = DatabaseQuery('dt_with_int_named_fieldname')
self.assertTrue(query.execute(filters={'1field': '10'}))
self.assertTrue(query.execute(filters={'1field': ['like', '1%']}))
self.assertTrue(query.execute(filters={'1field': ['in', '1,2,10']}))
self.assertTrue(query.execute(filters={'1field': ['is', 'set']}))
self.assertFalse(query.execute(filters={'1field': ['not like', '1%']}))
self.assertTrue(query.execute(filters=[['table_dt', '2field', 'is', 'not set']]))
frappe.get_doc({'doctype': table_dt.name, '2field': '10', 'parent': dt_data.name, 'parenttype': dt_data.doctype, 'parentfield': '2table_field'}).insert(ignore_permissions=True)
self.assertTrue(query.execute(filters=[['table_dt', '2field', 'is', 'set']]))
dt.delete()
table_dt.delete()
```

## Next Steps


---

*Source: test_db_query.py:936 | Complexity: Advanced | Last updated: 2026-02-04*