# How To: All Depends On Fields Conditions

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test all depends on fields conditions

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

### Step 1: Assign DocField = frappe.qb.DocType(...)

```python
DocField = frappe.qb.DocType('DocField')
```

### Step 2: Assign docfields_query = frappe.qb.from_.select.where(...)

```python
docfields_query = frappe.qb.from_(DocField).select(DocField.parent, DocField.depends_on, DocField.collapsible_depends_on, DocField.mandatory_depends_on, DocField.read_only_depends_on, DocField.fieldname).where((DocField.depends_on != '') | (DocField.collapsible_depends_on != '') | (DocField.mandatory_depends_on != '') | (DocField.read_only_depends_on != ''))
```

### Step 3: Assign docfields = docfields_query.run(...)

```python
docfields = docfields_query.run(as_dict=True)
```

### Step 4: Assign pattern = '[\\w\\.:_]+\\s*={1}\\s*[\\w\\.@\\\'"]+'

```python
pattern = '[\\w\\.:_]+\\s*={1}\\s*[\\w\\.@\\\'"]+'
```

### Step 5: Assign condition = field.get(...)

```python
condition = field.get(depends_on)
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(re.match(pattern, condition))
```


## Complete Example

```python
# Workflow
import re
DocField = frappe.qb.DocType('DocField')
docfields_query = frappe.qb.from_(DocField).select(DocField.parent, DocField.depends_on, DocField.collapsible_depends_on, DocField.mandatory_depends_on, DocField.read_only_depends_on, DocField.fieldname).where((DocField.depends_on != '') | (DocField.collapsible_depends_on != '') | (DocField.mandatory_depends_on != '') | (DocField.read_only_depends_on != ''))
docfields = docfields_query.run(as_dict=True)
pattern = '[\\w\\.:_]+\\s*={1}\\s*[\\w\\.@\\\'"]+'
for field in docfields:
    for depends_on in ['depends_on', 'collapsible_depends_on', 'mandatory_depends_on', 'read_only_depends_on']:
        condition = field.get(depends_on)
        if condition:
            self.assertFalse(re.match(pattern, condition))
```

## Next Steps


---

*Source: test_doctype.py:153 | Complexity: Intermediate | Last updated: 2026-02-04*