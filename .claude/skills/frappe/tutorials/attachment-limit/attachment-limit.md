# How To: Attachment Limit

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test attachment limit

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
self.attached_to_doctype1, self.attached_to_docname1 = make_test_doc()
self.attached_to_doctype2, self.attached_to_docname2 = make_test_doc()
self.test_content1 = test_content1
self.test_content2 = test_content1
self.orig_filename = 'hello.txt'
self.dup_filename = 'hello2.txt'
_file1 = frappe.get_doc({'doctype': 'File', 'file_name': self.orig_filename, 'attached_to_doctype': self.attached_to_doctype1, 'attached_to_name': self.attached_to_docname1, 'content': self.test_content1})
_file1.save()
_file2 = frappe.get_doc({'doctype': 'File', 'file_name': self.dup_filename, 'attached_to_doctype': self.attached_to_doctype2, 'attached_to_name': self.attached_to_docname2, 'content': self.test_content2})
_file2.save()
```

## Step-by-Step Guide

### Step 1: Assign unknown = make_test_doc(...)

```python
doctype, docname = make_test_doc()
```

### Step 2: Assign limit_property = make_property_setter(...)

```python
limit_property = make_property_setter('ToDo', None, 'max_attachments', 1, 'int', for_doctype=True)
```

### Step 3: Assign file1 = frappe.get_doc(...)

```python
file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'test-attachment', 'attached_to_doctype': doctype, 'attached_to_name': docname, 'content': 'test'})
```

### Step 4: Call file1.insert()

```python
file1.insert()
```

### Step 5: Assign file2 = frappe.get_doc(...)

```python
file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'test-attachment', 'attached_to_doctype': doctype, 'attached_to_name': docname, 'content': 'test2'})
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(frappe.exceptions.AttachmentLimitReached, file2.insert)
```

### Step 7: Call limit_property.delete()

```python
limit_property.delete()
```

### Step 8: Call frappe.clear_cache()

```python
frappe.clear_cache(doctype='ToDo')
```


## Complete Example

```python
# Setup
self.attached_to_doctype1, self.attached_to_docname1 = make_test_doc()
self.attached_to_doctype2, self.attached_to_docname2 = make_test_doc()
self.test_content1 = test_content1
self.test_content2 = test_content1
self.orig_filename = 'hello.txt'
self.dup_filename = 'hello2.txt'
_file1 = frappe.get_doc({'doctype': 'File', 'file_name': self.orig_filename, 'attached_to_doctype': self.attached_to_doctype1, 'attached_to_name': self.attached_to_docname1, 'content': self.test_content1})
_file1.save()
_file2 = frappe.get_doc({'doctype': 'File', 'file_name': self.dup_filename, 'attached_to_doctype': self.attached_to_doctype2, 'attached_to_name': self.attached_to_docname2, 'content': self.test_content2})
_file2.save()

# Workflow
doctype, docname = make_test_doc()
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
limit_property = make_property_setter('ToDo', None, 'max_attachments', 1, 'int', for_doctype=True)
file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'test-attachment', 'attached_to_doctype': doctype, 'attached_to_name': docname, 'content': 'test'})
file1.insert()
file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'test-attachment', 'attached_to_doctype': doctype, 'attached_to_name': docname, 'content': 'test2'})
self.assertRaises(frappe.exceptions.AttachmentLimitReached, file2.insert)
limit_property.delete()
frappe.clear_cache(doctype='ToDo')
```

## Next Steps


---

*Source: test_file.py:226 | Complexity: Advanced | Last updated: 2026-02-04*