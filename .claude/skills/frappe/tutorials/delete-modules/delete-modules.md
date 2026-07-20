# How To: Delete Modules

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test delete modules

## Prerequisites

**Required Modules:**
- `gzip`
- `importlib`
- `json`
- `os`
- `secrets`
- `shlex`
- `signal`
- `string`
- `subprocess`
- `sys`
- `time`
- `types`
- `unittest`
- `contextlib`
- `functools`
- `glob`
- `pathlib`
- `unittest.case`
- `unittest.mock`
- `click`
- `psutil`
- `requests`
- `click`
- `click.testing`
- `tenacity`
- `frappe`
- `frappe.commands.scheduler`
- `frappe.commands.site`
- `frappe.commands.utils`
- `frappe.recorder`
- `frappe.installer`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.backups`
- `frappe.utils.jinja_globals`
- `frappe.utils.scheduler`
- `frappe.utils.password`
- `frappe.installer`
- `frappe.utils.bench_helper`
- `frappe.database.mariadb.setup_db`
- `frappe.database.postgres.setup_db`


## Step-by-Step Guide

### Step 1: Assign test_module = frappe.new_doc(...)

```python
test_module = frappe.new_doc('Module Def')
```

### Step 2: Call test_module.update()

```python
test_module.update({'module_name': 'RemoveThis', 'app_name': 'frappe'})
```

### Step 3: Call test_module.save()

```python
test_module.save()
```

### Step 4: Assign module_def_linked_doctype = frappe.get_doc.insert(...)

```python
module_def_linked_doctype = frappe.get_doc({'doctype': 'DocType', 'name': 'Doctype linked with module def', 'module': 'RemoveThis', 'custom': 1, 'fields': [{'label': "Modulen't", 'fieldname': 'notmodule', 'fieldtype': 'Link', 'options': 'Module Def'}]}).insert()
```

### Step 5: Assign doctype_to_link_field_map = _get_module_linked_doctype_field_map(...)

```python
doctype_to_link_field_map = _get_module_linked_doctype_field_map()
```

### Step 6: Call self.assertIn()

```python
self.assertIn('Report', doctype_to_link_field_map)
```

### Step 7: Call self.assertIn()

```python
self.assertIn(module_def_linked_doctype.name, doctype_to_link_field_map)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(doctype_to_link_field_map[module_def_linked_doctype.name], 'notmodule')
```

### Step 9: Call self.assertNotIn()

```python
self.assertNotIn('DocType', doctype_to_link_field_map)
```

### Step 10: Assign doctypes_to_delete = _delete_modules(...)

```python
doctypes_to_delete = _delete_modules([test_module.module_name], dry_run=False)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(doctypes_to_delete), 1)
```

### Step 12: Call _delete_doctypes()

```python
_delete_doctypes(doctypes_to_delete, dry_run=False)
```

### Step 13: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Module Def', test_module.module_name))
```

### Step 14: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('DocType', module_def_linked_doctype.name))
```


## Complete Example

```python
# Workflow
from frappe.installer import _delete_doctypes, _delete_modules, _get_module_linked_doctype_field_map
test_module = frappe.new_doc('Module Def')
test_module.update({'module_name': 'RemoveThis', 'app_name': 'frappe'})
test_module.save()
module_def_linked_doctype = frappe.get_doc({'doctype': 'DocType', 'name': 'Doctype linked with module def', 'module': 'RemoveThis', 'custom': 1, 'fields': [{'label': "Modulen't", 'fieldname': 'notmodule', 'fieldtype': 'Link', 'options': 'Module Def'}]}).insert()
doctype_to_link_field_map = _get_module_linked_doctype_field_map()
self.assertIn('Report', doctype_to_link_field_map)
self.assertIn(module_def_linked_doctype.name, doctype_to_link_field_map)
self.assertEqual(doctype_to_link_field_map[module_def_linked_doctype.name], 'notmodule')
self.assertNotIn('DocType', doctype_to_link_field_map)
doctypes_to_delete = _delete_modules([test_module.module_name], dry_run=False)
self.assertEqual(len(doctypes_to_delete), 1)
_delete_doctypes(doctypes_to_delete, dry_run=False)
self.assertFalse(frappe.db.exists('Module Def', test_module.module_name))
self.assertFalse(frappe.db.exists('DocType', module_def_linked_doctype.name))
```

## Next Steps


---

*Source: test_commands.py:872 | Complexity: Advanced | Last updated: 2026-02-04*