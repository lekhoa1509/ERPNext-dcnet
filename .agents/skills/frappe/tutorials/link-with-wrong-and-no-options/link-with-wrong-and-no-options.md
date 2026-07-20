# How To: Link With Wrong And No Options

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test link with wrong and no options

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
doc = new_doctype('Test link')
```

### Step 2: Assign field_1 = doc.append(...)

```python
field_1 = doc.append('fields', {})
```

### Step 3: Assign field_1.fieldname = 'some_fieldname_1'

```python
field_1.fieldname = 'some_fieldname_1'
```

### Step 4: Assign field_1.fieldtype = 'Link'

```python
field_1.fieldtype = 'Link'
```

### Step 5: Call self.assertRaises()

```python
self.assertRaises(DoctypeLinkError, doc.insert)
```

### Step 6: Assign field_1.options = 'wrongdoctype'

```python
field_1.options = 'wrongdoctype'
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(WrongOptionsDoctypeLinkError, doc.insert)
```


## Complete Example

```python
# Workflow
doc = new_doctype('Test link')
field_1 = doc.append('fields', {})
field_1.fieldname = 'some_fieldname_1'
field_1.fieldtype = 'Link'
self.assertRaises(DoctypeLinkError, doc.insert)
field_1.options = 'wrongdoctype'
self.assertRaises(WrongOptionsDoctypeLinkError, doc.insert)
```

## Next Steps


---

*Source: test_doctype.py:339 | Complexity: Intermediate | Last updated: 2026-02-04*