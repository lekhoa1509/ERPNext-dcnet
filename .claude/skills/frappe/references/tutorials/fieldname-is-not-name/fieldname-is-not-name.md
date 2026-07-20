# How To: Fieldname Is Not Name

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test fieldname is not name

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
doc = new_doctype('Test Name Field')
```

### Step 2: Assign field_1 = doc.append(...)

```python
field_1 = doc.append('fields', {})
```

### Step 3: Assign field_1.label = 'Name'

```python
field_1.label = 'Name'
```

### Step 4: Assign field_1.fieldtype = 'Data'

```python
field_1.fieldtype = 'Data'
```

### Step 5: Call doc.insert()

```python
doc.insert()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(doc.fields[1].fieldname, 'name1')
```

### Step 7: Assign unknown.fieldname = 'name'

```python
doc.fields[1].fieldname = 'name'
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(InvalidFieldNameError, doc.save)
```


## Complete Example

```python
# Workflow
doc = new_doctype('Test Name Field')
field_1 = doc.append('fields', {})
field_1.label = 'Name'
field_1.fieldtype = 'Data'
doc.insert()
self.assertEqual(doc.fields[1].fieldname, 'name1')
doc.fields[1].fieldname = 'name'
self.assertRaises(InvalidFieldNameError, doc.save)
```

## Next Steps


---

*Source: test_doctype.py:320 | Complexity: Advanced | Last updated: 2026-02-04*