# How To: Saved Content Private

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test saved content private

## Prerequisites

**Required Modules:**
- `base64`
- `os`
- `shutil`
- `tempfile`
- `contextlib`
- `typing`
- `frappe`
- `frappe`
- `frappe.core.api.file`
- `frappe.core.doctype.file.exceptions`
- `frappe.core.doctype.file.utils`
- `frappe.desk.form.utils`
- `frappe.exceptions`
- `frappe.tests`
- `frappe.utils`
- `frappe.core.doctype.file.file`
- `frappe.custom.doctype.property_setter.property_setter`
- `shutil`


## Step-by-Step Guide

### Step 1: Assign _file1 = frappe.get_doc.insert(...)

```python
_file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing-private.txt', 'content': test_content1, 'is_private': 1}).insert()
```

### Step 2: Assign _file2 = frappe.get_doc.insert(...)

```python
_file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing-private.txt', 'content': test_content2, 'is_private': 1}).insert()
```

### Step 3: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc('File', {'file_url': _file1.file_url})
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(_file.get_content(), test_content1)
```

### Step 5: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc('File', {'file_url': _file2.file_url})
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(_file.get_content(), test_content2)
```


## Complete Example

```python
# Workflow
_file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing-private.txt', 'content': test_content1, 'is_private': 1}).insert()
_file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing-private.txt', 'content': test_content2, 'is_private': 1}).insert()
_file = frappe.get_doc('File', {'file_url': _file1.file_url})
self.assertEqual(_file.get_content(), test_content1)
_file = frappe.get_doc('File', {'file_url': _file2.file_url})
self.assertEqual(_file.get_content(), test_content2)
```

## Next Steps


---

*Source: test_file.py:167 | Complexity: Intermediate | Last updated: 2026-02-04*