# How To: Doctype Unique Constraint Dropped

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test doctype unique constraint dropped

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

### Step 1: Assign dt = new_doctype(...)

```python
dt = new_doctype('With_Unique', unique=1)
```

### Step 2: Call dt.insert()

```python
dt.insert()
```

### Step 3: Assign doc1 = frappe.new_doc(...)

```python
doc1 = frappe.new_doc('With_Unique')
```

### Step 4: Assign doc2 = frappe.new_doc(...)

```python
doc2 = frappe.new_doc('With_Unique')
```

### Step 5: Assign doc1.some_fieldname = 'Something'

```python
doc1.some_fieldname = 'Something'
```

### Step 6: Assign doc1.name = 'one'

```python
doc1.name = 'one'
```

### Step 7: Assign doc2.some_fieldname = 'Something'

```python
doc2.some_fieldname = 'Something'
```

### Step 8: Assign doc2.name = 'two'

```python
doc2.name = 'two'
```

### Step 9: Call doc1.insert()

```python
doc1.insert()
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.UniqueValidationError, doc2.insert)
```

### Step 11: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 12: Assign unknown.unique = 0

```python
dt.fields[0].unique = 0
```

### Step 13: Call dt.save()

```python
dt.save()
```

### Step 14: Call doc2.insert()

```python
doc2.insert()
```

### Step 15: Call doc1.delete()

```python
doc1.delete()
```

### Step 16: Call doc2.delete()

```python
doc2.delete()
```

### Step 17: Call frappe.delete_doc()

```python
frappe.delete_doc('DocType', 'With_Unique')
```


## Complete Example

```python
# Workflow
if frappe.db.exists('DocType', 'With_Unique'):
    frappe.delete_doc('DocType', 'With_Unique')
dt = new_doctype('With_Unique', unique=1)
dt.insert()
doc1 = frappe.new_doc('With_Unique')
doc2 = frappe.new_doc('With_Unique')
doc1.some_fieldname = 'Something'
doc1.name = 'one'
doc2.some_fieldname = 'Something'
doc2.name = 'two'
doc1.insert()
self.assertRaises(frappe.UniqueValidationError, doc2.insert)
frappe.db.rollback()
dt.fields[0].unique = 0
dt.save()
doc2.insert()
doc1.delete()
doc2.delete()
```

## Next Steps


---

*Source: test_doctype.py:101 | Complexity: Advanced | Last updated: 2026-02-04*