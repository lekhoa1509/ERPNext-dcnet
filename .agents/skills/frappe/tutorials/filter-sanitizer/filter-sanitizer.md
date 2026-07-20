# How To: Filter Sanitizer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test filter sanitizer

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

### Step 1: Call self.assertRaises()

```python
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'istable,': 1}, limit_start=0, limit_page_length=1)
```

### Step 2: Call self.assertRaises()

```python
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'editable_grid,': 1}, or_filters={'istable,': 1}, limit_start=0, limit_page_length=1)
```

### Step 3: Call self.assertRaises()

```python
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'editable_grid,': 1}, or_filters=[['DocType', 'istable,', '=', 1]], limit_start=0, limit_page_length=1)
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'editable_grid,': 1}, or_filters=[['DocType', 'istable', '=', 1], ['DocType', 'beta and 1=1', '=', 0]], limit_start=0, limit_page_length=1)
```

### Step 5: Assign out = DatabaseQuery.execute(...)

```python
out = DatabaseQuery('DocType').execute(fields=['name'], filters={'editable_grid': 1, 'module': 'Core'}, or_filters=[['DocType', 'istable', '=', 1]], order_by='creation')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue('DocField' in [d['name'] for d in out])
```

### Step 7: Assign out = DatabaseQuery.execute(...)

```python
out = DatabaseQuery('DocType').execute(fields=['name'], filters={'issingle': 1}, or_filters=[['DocType', 'module', '=', 'Core']], order_by='creation')
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue('Role Permission for Page and Report' in [d['name'] for d in out])
```

### Step 9: Assign out = DatabaseQuery.execute(...)

```python
out = DatabaseQuery('DocType').execute(fields=['name'], filters={'track_changes': 1, 'module': 'Core'}, order_by='creation')
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue('File' in [d['name'] for d in out])
```

### Step 11: Assign out = DatabaseQuery.execute(...)

```python
out = DatabaseQuery('DocType').execute(fields=['name'], filters=[['DocType', 'ifnull(track_changes, 0)', '=', 0], ['DocType', 'module', '=', 'Core']], order_by='creation')
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue('DefaultValue' in [d['name'] for d in out])
```


## Complete Example

```python
# Setup
setup_for_tests()
frappe.set_user('Administrator')

# Workflow
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'istable,': 1}, limit_start=0, limit_page_length=1)
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'editable_grid,': 1}, or_filters={'istable,': 1}, limit_start=0, limit_page_length=1)
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'editable_grid,': 1}, or_filters=[['DocType', 'istable,', '=', 1]], limit_start=0, limit_page_length=1)
self.assertRaises(frappe.DataError, DatabaseQuery('DocType').execute, fields=['name'], filters={'editable_grid,': 1}, or_filters=[['DocType', 'istable', '=', 1], ['DocType', 'beta and 1=1', '=', 0]], limit_start=0, limit_page_length=1)
out = DatabaseQuery('DocType').execute(fields=['name'], filters={'editable_grid': 1, 'module': 'Core'}, or_filters=[['DocType', 'istable', '=', 1]], order_by='creation')
self.assertTrue('DocField' in [d['name'] for d in out])
out = DatabaseQuery('DocType').execute(fields=['name'], filters={'issingle': 1}, or_filters=[['DocType', 'module', '=', 'Core']], order_by='creation')
self.assertTrue('Role Permission for Page and Report' in [d['name'] for d in out])
out = DatabaseQuery('DocType').execute(fields=['name'], filters={'track_changes': 1, 'module': 'Core'}, order_by='creation')
self.assertTrue('File' in [d['name'] for d in out])
out = DatabaseQuery('DocType').execute(fields=['name'], filters=[['DocType', 'ifnull(track_changes, 0)', '=', 0], ['DocType', 'module', '=', 'Core']], order_by='creation')
self.assertTrue('DefaultValue' in [d['name'] for d in out])
```

## Next Steps


---

*Source: test_db_query.py:608 | Complexity: Advanced | Last updated: 2026-02-04*