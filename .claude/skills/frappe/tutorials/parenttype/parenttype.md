# How To: Parenttype

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test parenttype

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

### Step 1: Assign child = new_doctype.insert(...)

```python
child = new_doctype(istable=1).insert()
```

### Step 2: Assign table_field = value

```python
table_field = {'label': 'Test Table', 'fieldname': 'test_table', 'fieldtype': 'Table', 'options': child.name}
```

### Step 3: Assign parent_a = new_doctype.insert(...)

```python
parent_a = new_doctype(fields=[table_field], allow_rename=1, autoname='Prompt').insert()
```

### Step 4: Assign parent_b = new_doctype.insert(...)

```python
parent_b = new_doctype(fields=[table_field], allow_rename=1, autoname='Prompt').insert()
```

### Step 5: Assign parent_a_instance = frappe.get_doc.insert(...)

```python
parent_a_instance = frappe.get_doc(doctype=parent_a.name, test_table=[{'some_fieldname': 'x'}], name='XYZ').insert()
```

### Step 6: Assign parent_b_instance = frappe.get_doc.insert(...)

```python
parent_b_instance = frappe.get_doc(doctype=parent_b.name, test_table=[{'some_fieldname': 'x'}], name='XYZ').insert()
```

### Step 7: Call parent_b_instance.rename()

```python
parent_b_instance.rename('ABC')
```

### Step 8: Call parent_a_instance.reload()

```python
parent_a_instance.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(parent_a_instance.test_table), 1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(parent_b_instance.test_table), 1)
```


## Complete Example

```python
# Workflow
child = new_doctype(istable=1).insert()
table_field = {'label': 'Test Table', 'fieldname': 'test_table', 'fieldtype': 'Table', 'options': child.name}
parent_a = new_doctype(fields=[table_field], allow_rename=1, autoname='Prompt').insert()
parent_b = new_doctype(fields=[table_field], allow_rename=1, autoname='Prompt').insert()
parent_a_instance = frappe.get_doc(doctype=parent_a.name, test_table=[{'some_fieldname': 'x'}], name='XYZ').insert()
parent_b_instance = frappe.get_doc(doctype=parent_b.name, test_table=[{'some_fieldname': 'x'}], name='XYZ').insert()
parent_b_instance.rename('ABC')
parent_a_instance.reload()
self.assertEqual(len(parent_a_instance.test_table), 1)
self.assertEqual(len(parent_b_instance.test_table), 1)
```

## Next Steps


---

*Source: test_rename_doc.py:257 | Complexity: Advanced | Last updated: 2026-02-04*