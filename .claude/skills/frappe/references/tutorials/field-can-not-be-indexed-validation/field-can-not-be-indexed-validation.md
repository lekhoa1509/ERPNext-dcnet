# How To: Field Can Not Be Indexed Validation

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test field can not be indexed validation

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
doc = new_doctype('Test index')
```

### Step 2: Assign field_1 = doc.append(...)

```python
field_1 = doc.append('fields', {})
```

### Step 3: Assign field_1.fieldname = 'some_fieldname_1'

```python
field_1.fieldname = 'some_fieldname_1'
```

### Step 4: Assign field_1.fieldtype = 'Long Text'

```python
field_1.fieldtype = 'Long Text'
```

### Step 5: Assign field_1.search_index = 1

```python
field_1.search_index = 1
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(CannotIndexedError, doc.insert)
```


## Complete Example

```python
# Workflow
doc = new_doctype('Test index')
field_1 = doc.append('fields', {})
field_1.fieldname = 'some_fieldname_1'
field_1.fieldtype = 'Long Text'
field_1.search_index = 1
self.assertRaises(CannotIndexedError, doc.insert)
```

## Next Steps


---

*Source: test_doctype.py:361 | Complexity: Intermediate | Last updated: 2026-02-04*