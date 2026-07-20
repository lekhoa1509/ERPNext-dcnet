# How To: Website Route Default

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test website route default

## Prerequisites

**Required Modules:**
- `inspect`
- `contextlib`
- `copy`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.app`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user.user`
- `frappe.desk.doctype.note.note`
- `frappe.model.document`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.desk.doctype.event.event`
- `pathlib`
- `frappe.modules.utils`
- `frappe.model.document`


## Step-by-Step Guide

### Step 1: Assign default = frappe.generate_hash(...)

```python
default = frappe.generate_hash()
```

### Step 2: Assign child_table = value

```python
child_table = new_doctype(default=default, istable=1).insert().name
```

### Step 3: Assign parent = value

```python
parent = new_doctype(fields=[{'fieldtype': 'Table', 'options': child_table, 'fieldname': 'child_table'}]).insert().name
```

### Step 4: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc({'doctype': parent, 'child_table': [{'some_fieldname': 'xasd'}]}).insert()
```

### Step 5: Call doc.append()

```python
doc.append('child_table', {})
```

### Step 6: Call doc.save()

```python
doc.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.child_table[-1].some_fieldname, default)
```


## Complete Example

```python
# Workflow
default = frappe.generate_hash()
child_table = new_doctype(default=default, istable=1).insert().name
parent = new_doctype(fields=[{'fieldtype': 'Table', 'options': child_table, 'fieldname': 'child_table'}]).insert().name
doc = frappe.get_doc({'doctype': parent, 'child_table': [{'some_fieldname': 'xasd'}]}).insert()
doc.append('child_table', {})
doc.save()
self.assertEqual(doc.child_table[-1].some_fieldname, default)
```

## Next Steps


---

*Source: test_document.py:69 | Complexity: Intermediate | Last updated: 2026-02-04*