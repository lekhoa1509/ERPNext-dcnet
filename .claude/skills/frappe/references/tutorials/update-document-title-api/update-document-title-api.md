# How To: Update Document Title Api

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update document title api

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

**Required Fixtures:**
- `api_client` fixture


## Step-by-Step Guide

### Step 1: Assign test_doctype = 'Module Def'

```python
test_doctype = 'Module Def'
```

### Step 2: Assign test_doc = frappe.get_doc(...)

```python
test_doc = frappe.get_doc({'doctype': test_doctype, 'module_name': f'Test-test_update_document_title_api-{frappe.generate_hash()}', 'custom': True})
```

### Step 3: Call test_doc.insert()

```python
test_doc.insert(ignore_mandatory=True)
```

### Step 4: Assign dt = value

```python
dt = test_doc.doctype
```

### Step 5: Assign dn = value

```python
dn = test_doc.name
```

### Step 6: Assign new_name = value

```python
new_name = f'{dn}-new'
```

### Step 7: Assign doc_before = frappe.get_doc(...)

```python
doc_before = frappe.get_doc(test_doctype, dn)
```

### Step 8: Assign return_value = update_document_title(...)

```python
return_value = update_document_title(doctype=dt, docname=dn, new_name=new_name)
```

### Step 9: Assign doc_after = frappe.get_doc(...)

```python
doc_after = frappe.get_doc(test_doctype, return_value)
```

### Step 10: Assign doc_before_dict = doc_before.as_dict(...)

```python
doc_before_dict = doc_before.as_dict(no_nulls=True, no_default_fields=True)
```

### Step 11: Assign doc_after_dict = doc_after.as_dict(...)

```python
doc_after_dict = doc_after.as_dict(no_nulls=True, no_default_fields=True)
```

### Step 12: Call doc_before_dict.pop()

```python
doc_before_dict.pop('module_name')
```

### Step 13: Call doc_after_dict.pop()

```python
doc_after_dict.pop('module_name')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(new_name, return_value)
```

### Step 15: Call self.assertDictEqual()

```python
self.assertDictEqual(doc_before_dict, doc_after_dict)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(doc_after.module_name, return_value)
```

### Step 17: Call test_doc.delete()

```python
test_doc.delete()
```

### Step 18: Call update_document_title()

```python
update_document_title(doctype=dt, docname=dn, title={}, name={'hack': 'this'})
```


## Complete Example

```python
# Workflow
test_doctype = 'Module Def'
test_doc = frappe.get_doc({'doctype': test_doctype, 'module_name': f'Test-test_update_document_title_api-{frappe.generate_hash()}', 'custom': True})
test_doc.insert(ignore_mandatory=True)
dt = test_doc.doctype
dn = test_doc.name
new_name = f'{dn}-new'
with self.assertRaises(TypeError):
    update_document_title(doctype=dt, docname=dn, title={}, name={'hack': 'this'})
doc_before = frappe.get_doc(test_doctype, dn)
return_value = update_document_title(doctype=dt, docname=dn, new_name=new_name)
doc_after = frappe.get_doc(test_doctype, return_value)
doc_before_dict = doc_before.as_dict(no_nulls=True, no_default_fields=True)
doc_after_dict = doc_after.as_dict(no_nulls=True, no_default_fields=True)
doc_before_dict.pop('module_name')
doc_after_dict.pop('module_name')
self.assertEqual(new_name, return_value)
self.assertDictEqual(doc_before_dict, doc_after_dict)
self.assertEqual(doc_after.module_name, return_value)
test_doc.delete()
```

## Next Steps


---

*Source: test_rename_doc.py:202 | Complexity: Advanced | Last updated: 2026-02-04*