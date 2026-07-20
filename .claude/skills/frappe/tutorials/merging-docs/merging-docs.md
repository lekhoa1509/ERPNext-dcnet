# How To: Merging Docs

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Merge two documents via frappe.rename_doc

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

### Step 1: 'Merge two documents via frappe.rename_doc'

```python
'Merge two documents via frappe.rename_doc'
```

### Step 2: Assign unknown = sample(...)

```python
first_todo, second_todo = sample(self.available_documents, 2)
```

### Step 3: Assign second_todo_doc = frappe.get_doc(...)

```python
second_todo_doc = frappe.get_doc(self.test_doctype, second_todo)
```

### Step 4: Assign second_todo_doc.priority = 'High'

```python
second_todo_doc.priority = 'High'
```

### Step 5: Call second_todo_doc.save()

```python
second_todo_doc.save()
```

### Step 6: Assign merged_todo = frappe.rename_doc(...)

```python
merged_todo = frappe.rename_doc(self.test_doctype, first_todo, second_todo, merge=True, force=True)
```

### Step 7: Assign merged_todo_doc = frappe.get_doc(...)

```python
merged_todo_doc = frappe.get_doc(self.test_doctype, merged_todo)
```

### Step 8: Call self.available_documents.remove()

```python
self.available_documents.remove(first_todo)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(merged_todo_doc.priority, second_todo_doc.priority)
```

### Step 10: Call frappe.get_doc()

```python
frappe.get_doc(self.test_doctype, first_todo)
```


## Complete Example

```python
# Workflow
'Merge two documents via frappe.rename_doc'
first_todo, second_todo = sample(self.available_documents, 2)
second_todo_doc = frappe.get_doc(self.test_doctype, second_todo)
second_todo_doc.priority = 'High'
second_todo_doc.save()
merged_todo = frappe.rename_doc(self.test_doctype, first_todo, second_todo, merge=True, force=True)
merged_todo_doc = frappe.get_doc(self.test_doctype, merged_todo)
self.available_documents.remove(first_todo)
with self.assertRaises(DoesNotExistError):
    frappe.get_doc(self.test_doctype, first_todo)
self.assertEqual(merged_todo_doc.priority, second_todo_doc.priority)
```

## Next Steps


---

*Source: test_rename_doc.py:131 | Complexity: Advanced | Last updated: 2026-02-04*