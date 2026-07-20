# How To: Insert Update And Load From Desk

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Insert, update, reload and assert changes

## Prerequisites

**Required Modules:**
- `json`
- `os`
- `unittest.mock`
- `frappe`
- `frappe.modules.utils`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.form.save`
- `frappe.model.document`
- `frappe.model.virtual_doctype`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'Insert, update, reload and assert changes'

```python
'Insert, update, reload and assert changes'
```

### Step 2: Assign frappe.response.docs = value

```python
frappe.response.docs = []
```

### Step 3: Assign doc = json.dumps(...)

```python
doc = json.dumps({'docstatus': 0, 'doctype': TEST_DOCTYPE_NAME, 'name': 'new-doctype-1', '__islocal': 1, '__unsaved': 1, 'owner': 'Administrator', TEST_DOCTYPE_NAME: 'Original Data'})
```

### Step 4: Call savedocs()

```python
savedocs(doc, 'Save')
```

### Step 5: Assign docname = value

```python
docname = frappe.response.docs[0]['name']
```

### Step 6: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc(TEST_DOCTYPE_NAME, docname)
```

### Step 7: Call doc.update()

```python
doc.update({'child_table': [{'name': 'child-1', 'some_fieldname': 'child1-field-value'}]})
```

### Step 8: Call savedocs()

```python
savedocs(doc.as_json(), 'Save')
```

### Step 9: Call doc.reload()

```python
doc.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(doc.child_table[0].some_fieldname, 'child1-field-value')
```


## Complete Example

```python
# Workflow
'Insert, update, reload and assert changes'
frappe.response.docs = []
doc = json.dumps({'docstatus': 0, 'doctype': TEST_DOCTYPE_NAME, 'name': 'new-doctype-1', '__islocal': 1, '__unsaved': 1, 'owner': 'Administrator', TEST_DOCTYPE_NAME: 'Original Data'})
savedocs(doc, 'Save')
docname = frappe.response.docs[0]['name']
doc = frappe.get_doc(TEST_DOCTYPE_NAME, docname)
doc.update({'child_table': [{'name': 'child-1', 'some_fieldname': 'child1-field-value'}]})
savedocs(doc.as_json(), 'Save')
doc.reload()
self.assertEqual(doc.child_table[0].some_fieldname, 'child1-field-value')
```

## Next Steps


---

*Source: test_virtual_doctype.py:118 | Complexity: Advanced | Last updated: 2026-02-04*