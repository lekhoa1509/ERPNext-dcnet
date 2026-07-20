# How To: Multiple Doc Insert And Get List

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple doc insert and get list

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

### Step 1: Assign doc1 = frappe.new_doc(...)

```python
doc1 = frappe.new_doc(doctype=TEST_DOCTYPE_NAME)
```

### Step 2: Call doc1.append()

```python
doc1.append('child_table', {'name': 'first', 'some_fieldname': 'first-value'})
```

### Step 3: Call doc1.insert()

```python
doc1.insert()
```

### Step 4: Assign doc2 = frappe.new_doc(...)

```python
doc2 = frappe.new_doc(doctype=TEST_DOCTYPE_NAME)
```

### Step 5: Call doc2.append()

```python
doc2.append('child_table', {'name': 'second', 'some_fieldname': 'second-value'})
```

### Step 6: Call doc2.insert()

```python
doc2.insert()
```

### Step 7: Assign docs = value

```python
docs = {doc1.name, doc2.name}
```

### Step 8: Call doc2.reload()

```python
doc2.reload()
```

### Step 9: Call doc1.reload()

```python
doc1.reload()
```

### Step 10: Assign updated_docs = value

```python
updated_docs = {doc1.name, doc2.name}
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(docs, updated_docs)
```

### Step 12: Assign listed_docs = value

```python
listed_docs = {d.name for d in VirtualDoctypeTest.get_list()}
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(docs, listed_docs)
```


## Complete Example

```python
# Workflow
doc1 = frappe.new_doc(doctype=TEST_DOCTYPE_NAME)
doc1.append('child_table', {'name': 'first', 'some_fieldname': 'first-value'})
doc1.insert()
doc2 = frappe.new_doc(doctype=TEST_DOCTYPE_NAME)
doc2.append('child_table', {'name': 'second', 'some_fieldname': 'second-value'})
doc2.insert()
docs = {doc1.name, doc2.name}
doc2.reload()
doc1.reload()
updated_docs = {doc1.name, doc2.name}
self.assertEqual(docs, updated_docs)
listed_docs = {d.name for d in VirtualDoctypeTest.get_list()}
self.assertEqual(docs, listed_docs)
```

## Next Steps


---

*Source: test_virtual_doctype.py:145 | Complexity: Advanced | Last updated: 2026-02-04*