# How To: Rename Doctype

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Rename DocType via frappe.rename_doc

## Prerequisites

**Required Modules:**
- `os`
- `contextlib`
- `io`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.exceptions`
- `frappe.model.base_document`
- `frappe.model.rename_doc`
- `frappe.modules.utils`
- `frappe.tests`
- `frappe.utils`
- `frappe.core.doctype.doctype.test_doctype`


## Step-by-Step Guide

### Step 1: 'Rename DocType via frappe.rename_doc'

```python
'Rename DocType via frappe.rename_doc'
```

### Step 2: Assign to_rename_record = frappe.get_doc.insert(...)

```python
to_rename_record = frappe.get_doc({'doctype': 'Rename This', 'linked_to_doctype': 'Rename This'}).insert()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual('Renamed Doc', frappe.rename_doc('DocType', 'Rename This', 'Renamed Doc', force=True))
```

### Step 4: Assign linked_to_doctype = frappe.db.get_value(...)

```python
linked_to_doctype = frappe.db.get_value('Renamed Doc', to_rename_record.name, 'linked_to_doctype')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(linked_to_doctype, 'Renamed Doc')
```

### Step 6: Assign old_name = value

```python
old_name = to_rename_record.name
```

### Step 7: Assign new_name = 'ToDo'

```python
new_name = 'ToDo'
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(new_name, frappe.rename_doc('Renamed Doc', old_name, new_name, force=True))
```

### Step 9: Call new_doctype.insert()

```python
new_doctype('Rename This', fields=[{'label': 'Linked To', 'fieldname': 'linked_to_doctype', 'fieldtype': 'Link', 'options': 'DocType', 'unique': 0}]).insert()
```


## Complete Example

```python
# Workflow
'Rename DocType via frappe.rename_doc'
from frappe.core.doctype.doctype.test_doctype import new_doctype
if not frappe.db.exists('DocType', 'Rename This'):
    new_doctype('Rename This', fields=[{'label': 'Linked To', 'fieldname': 'linked_to_doctype', 'fieldtype': 'Link', 'options': 'DocType', 'unique': 0}]).insert()
to_rename_record = frappe.get_doc({'doctype': 'Rename This', 'linked_to_doctype': 'Rename This'}).insert()
self.assertEqual('Renamed Doc', frappe.rename_doc('DocType', 'Rename This', 'Renamed Doc', force=True))
linked_to_doctype = frappe.db.get_value('Renamed Doc', to_rename_record.name, 'linked_to_doctype')
self.assertEqual(linked_to_doctype, 'Renamed Doc')
old_name = to_rename_record.name
new_name = 'ToDo'
self.assertEqual(new_name, frappe.rename_doc('Renamed Doc', old_name, new_name, force=True))
```

## Next Steps


---

*Source: test_rename_doc.py:165 | Complexity: Advanced | Last updated: 2026-02-04*