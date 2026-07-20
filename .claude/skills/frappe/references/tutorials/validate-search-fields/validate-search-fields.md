# How To: Validate Search Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test validate search fields

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
doc = new_doctype('Test Search Fields')
```

### Step 2: Assign doc.search_fields = 'some_fieldname'

```python
doc.search_fields = 'some_fieldname'
```

### Step 3: Call doc.insert()

```python
doc.insert()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(doc.name, 'Test Search Fields')
```

### Step 5: Assign doc.search_fields = 'some_fieldname_1'

```python
doc.search_fields = 'some_fieldname_1'
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, doc.save)
```

### Step 7: Assign field = doc.append(...)

```python
field = doc.append('fields', {})
```

### Step 8: Assign field.fieldname = 'some_html_field'

```python
field.fieldname = 'some_html_field'
```

### Step 9: Assign field.fieldtype = 'HTML'

```python
field.fieldtype = 'HTML'
```

### Step 10: Assign field.label = 'Some HTML Field'

```python
field.label = 'Some HTML Field'
```

### Step 11: Assign doc.search_fields = 'some_fieldname,some_html_field'

```python
doc.search_fields = 'some_fieldname,some_html_field'
```

### Step 12: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, doc.save)
```


## Complete Example

```python
# Workflow
doc = new_doctype('Test Search Fields')
doc.search_fields = 'some_fieldname'
doc.insert()
self.assertEqual(doc.name, 'Test Search Fields')
doc.search_fields = 'some_fieldname_1'
self.assertRaises(frappe.ValidationError, doc.save)
field = doc.append('fields', {})
field.fieldname = 'some_html_field'
field.fieldtype = 'HTML'
field.label = 'Some HTML Field'
doc.search_fields = 'some_fieldname,some_html_field'
self.assertRaises(frappe.ValidationError, doc.save)
```

## Next Steps


---

*Source: test_doctype.py:126 | Complexity: Advanced | Last updated: 2026-02-04*