# How To: Unique Field Name For Two Fields

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test unique field name for two fields

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

### Step 1: Assign doc = new_doctype(...)

```python
doc = new_doctype('Test Unique Field')
```

### Step 2: Assign field_1 = doc.append(...)

```python
field_1 = doc.append('fields', {})
```

### Step 3: Assign field_1.fieldname = 'some_fieldname_1'

```python
field_1.fieldname = 'some_fieldname_1'
```

### Step 4: Assign field_1.fieldtype = 'Data'

```python
field_1.fieldtype = 'Data'
```

### Step 5: Assign field_2 = doc.append(...)

```python
field_2 = doc.append('fields', {})
```

### Step 6: Assign field_2.fieldname = 'some_fieldname_1'

```python
field_2.fieldname = 'some_fieldname_1'
```

### Step 7: Assign field_2.fieldtype = 'Data'

```python
field_2.fieldtype = 'Data'
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(UniqueFieldnameError, doc.insert)
```


## Complete Example

```python
# Workflow
doc = new_doctype('Test Unique Field')
field_1 = doc.append('fields', {})
field_1.fieldname = 'some_fieldname_1'
field_1.fieldtype = 'Data'
field_2 = doc.append('fields', {})
field_2.fieldname = 'some_fieldname_1'
field_2.fieldtype = 'Data'
self.assertRaises(UniqueFieldnameError, doc.insert)
```

## Next Steps


---

*Source: test_doctype.py:308 | Complexity: Advanced | Last updated: 2026-02-04*