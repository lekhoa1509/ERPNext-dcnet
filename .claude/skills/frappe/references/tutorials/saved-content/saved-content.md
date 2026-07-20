# How To: Saved Content

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test saved content

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

### Step 1: Assign unknown = make_test_doc(...)

```python
self.attached_to_doctype, self.attached_to_docname = make_test_doc()
```

### Step 2: Assign self.test_content1 = test_content1

```python
self.test_content1 = test_content1
```

### Step 3: Assign self.test_content2 = test_content2

```python
self.test_content2 = test_content2
```

### Step 4: Assign _file1 = frappe.get_doc(...)

```python
_file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing.txt', 'attached_to_doctype': self.attached_to_doctype, 'attached_to_name': self.attached_to_docname, 'content': self.test_content1})
```

### Step 5: Call _file1.save()

```python
_file1.save()
```

### Step 6: Assign _file2 = frappe.get_doc(...)

```python
_file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing.txt', 'attached_to_doctype': self.attached_to_doctype, 'attached_to_name': self.attached_to_docname, 'content': self.test_content2})
```

### Step 7: Call _file2.save()

```python
_file2.save()
```

### Step 8: Assign self.saved_file_url1 = value

```python
self.saved_file_url1 = _file1.file_url
```

### Step 9: Assign self.saved_file_url2 = value

```python
self.saved_file_url2 = _file2.file_url
```

### Step 10: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc('File', {'file_url': self.saved_file_url1})
```

### Step 11: Assign content1 = _file.get_content(...)

```python
content1 = _file.get_content()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(content1, self.test_content1)
```

### Step 13: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc('File', {'file_url': self.saved_file_url2})
```

### Step 14: Assign content2 = _file.get_content(...)

```python
content2 = _file.get_content()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(content2, self.test_content2)
```


## Complete Example

```python
# Workflow
self.attached_to_doctype, self.attached_to_docname = make_test_doc()
self.test_content1 = test_content1
self.test_content2 = test_content2
_file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing.txt', 'attached_to_doctype': self.attached_to_doctype, 'attached_to_name': self.attached_to_docname, 'content': self.test_content1})
_file1.save()
_file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'testing.txt', 'attached_to_doctype': self.attached_to_doctype, 'attached_to_name': self.attached_to_docname, 'content': self.test_content2})
_file2.save()
self.saved_file_url1 = _file1.file_url
self.saved_file_url2 = _file2.file_url
_file = frappe.get_doc('File', {'file_url': self.saved_file_url1})
content1 = _file.get_content()
self.assertEqual(content1, self.test_content1)
_file = frappe.get_doc('File', {'file_url': self.saved_file_url2})
content2 = _file.get_content()
self.assertEqual(content2, self.test_content2)
```

## Next Steps


---

*Source: test_file.py:133 | Complexity: Advanced | Last updated: 2026-02-04*