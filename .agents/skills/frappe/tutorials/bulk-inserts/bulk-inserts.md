# How To: Bulk Inserts

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk inserts

## Prerequisites

**Required Modules:**
- `inspect`
- `contextlib`
- `copy`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.app`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.core.doctype.user.user`
- `frappe.desk.doctype.note.note`
- `frappe.model.document`
- `frappe.model.naming`
- `frappe.tests`
- `frappe.utils`
- `frappe.website.serve`
- `frappe.desk.doctype.event.event`
- `pathlib`
- `frappe.modules.utils`
- `frappe.model.document`


## Step-by-Step Guide

### Step 1: Assign doctype = 'Role Profile'

```python
doctype = 'Role Profile'
```

### Step 2: Assign child_field = 'roles'

```python
child_field = 'roles'
```

### Step 3: Assign child_doctype = value

```python
child_doctype = frappe.get_meta(doctype).get_field(child_field).options
```

### Step 4: Assign sent_docs = set(...)

```python
sent_docs = set()
```

### Step 5: Assign sent_child_docs = set(...)

```python
sent_child_docs = set()
```

### Step 6: Call bulk_insert()

```python
bulk_insert(doctype, doc_generator(), chunk_size=5)
```

### Step 7: Assign all_docs = set(...)

```python
all_docs = set(frappe.get_all(doctype, pluck='name'))
```

### Step 8: Assign all_child_docs = set(...)

```python
all_child_docs = set(frappe.get_all(child_doctype, filters={'parenttype': doctype, 'parentfield': child_field}, pluck='name'))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(sent_docs - all_docs, set(), 'All docs should be inserted')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(sent_child_docs - all_child_docs, set(), 'All child docs should be inserted')
```

### Step 11: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc(doctype)
```

### Step 12: Assign doc.role_profile = frappe.generate_hash(...)

```python
doc.role_profile = frappe.generate_hash()
```

### Step 13: Call doc.append()

```python
doc.append('roles', {'role': 'System Manager'})
```

### Step 14: Call doc.set_new_name()

```python
doc.set_new_name()
```

### Step 15: Call doc.set_parent_in_children()

```python
doc.set_parent_in_children()
```

### Step 16: Call sent_docs.add()

```python
sent_docs.add(doc.name)
```

### Step 17: Call sent_child_docs.add()

```python
sent_child_docs.add(doc.roles[0].name)
```

### Step 18: yield doc

```python
yield doc
```


## Complete Example

```python
# Workflow
from frappe.model.document import bulk_insert
doctype = 'Role Profile'
child_field = 'roles'
child_doctype = frappe.get_meta(doctype).get_field(child_field).options
sent_docs = set()
sent_child_docs = set()

def doc_generator():
    for _ in range(21):
        doc = frappe.new_doc(doctype)
        doc.role_profile = frappe.generate_hash()
        doc.append('roles', {'role': 'System Manager'})
        doc.set_new_name()
        doc.set_parent_in_children()
        sent_docs.add(doc.name)
        sent_child_docs.add(doc.roles[0].name)
        yield doc
bulk_insert(doctype, doc_generator(), chunk_size=5)
all_docs = set(frappe.get_all(doctype, pluck='name'))
all_child_docs = set(frappe.get_all(child_doctype, filters={'parenttype': doctype, 'parentfield': child_field}, pluck='name'))
self.assertEqual(sent_docs - all_docs, set(), 'All docs should be inserted')
self.assertEqual(sent_child_docs - all_child_docs, set(), 'All child docs should be inserted')
```

## Next Steps


---

*Source: test_document.py:640 | Complexity: Advanced | Last updated: 2026-02-04*