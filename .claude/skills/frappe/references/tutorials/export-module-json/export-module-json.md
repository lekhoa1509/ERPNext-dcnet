# How To: Export Module Json

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test export module json

## Prerequisites

**Required Modules:**
- `os`
- `shutil`
- `unittest`
- `contextlib`
- `pathlib`
- `frappe`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.model.meta`
- `frappe.modules`
- `frappe.modules.utils`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.get_last_doc(...)

```python
doc = frappe.get_last_doc('DocType', {'issingle': 0, 'custom': 0})
```

### Step 2: Assign export_doc_path = os.path.join(...)

```python
export_doc_path = os.path.join(get_module_path(doc.module), scrub(doc.doctype), scrub(doc.name), f'{scrub(doc.name)}.json')
```

### Step 3: Assign last_modified_before = os.path.getmtime(...)

```python
last_modified_before = os.path.getmtime(export_doc_path)
```

### Step 4: Call self.addCleanup()

```python
self.addCleanup(write_file, path=export_doc_path, content=frappe.as_json(export_doc_before))
```

### Step 5: Assign frappe.flags.in_import = False

```python
frappe.flags.in_import = False
```

### Step 6: Assign frappe.conf.developer_mode = True

```python
frappe.conf.developer_mode = True
```

### Step 7: Assign export_path = export_module_json(...)

```python
export_path = export_module_json(doc=doc, is_standard=True, module=doc.module)
```

### Step 8: Assign last_modified_after = os.path.getmtime(...)

```python
last_modified_after = os.path.getmtime(export_doc_path)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(last_modified_after > last_modified_before)
```

### Step 10: Assign export_doc_before = frappe.parse_json(...)

```python
export_doc_before = frappe.parse_json(f.read())
```

### Step 11: Call frappe.parse_json()

```python
frappe.parse_json(f.read())
```


## Complete Example

```python
# Workflow
doc = frappe.get_last_doc('DocType', {'issingle': 0, 'custom': 0})
export_doc_path = os.path.join(get_module_path(doc.module), scrub(doc.doctype), scrub(doc.name), f'{scrub(doc.name)}.json')
with open(export_doc_path) as f:
    export_doc_before = frappe.parse_json(f.read())
last_modified_before = os.path.getmtime(export_doc_path)
self.addCleanup(write_file, path=export_doc_path, content=frappe.as_json(export_doc_before))
frappe.flags.in_import = False
frappe.conf.developer_mode = True
export_path = export_module_json(doc=doc, is_standard=True, module=doc.module)
last_modified_after = os.path.getmtime(export_doc_path)
with open(f'{export_path}.json') as f:
    frappe.parse_json(f.read())
self.assertTrue(last_modified_after > last_modified_before)
```

## Next Steps


---

*Source: test_modules.py:52 | Complexity: Advanced | Last updated: 2026-02-04*