# How To: Utf8 Bom Content Decoding

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test utf8 bom content decoding

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

### Step 1: Assign utf8_bom_content = test_content1.encode(...)

```python
utf8_bom_content = test_content1.encode('utf-8-sig')
```

### Step 2: Call _file.save()

```python
_file.save()
```

### Step 3: Assign saved_file = frappe.get_doc(...)

```python
saved_file = frappe.get_doc('File', _file.name)
```

### Step 4: Assign file_content_decoded = saved_file.get_content(...)

```python
file_content_decoded = saved_file.get_content(encodings=['utf-8'])
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(file_content_decoded[0], '\ufeff')
```

### Step 6: Assign file_content_properly_decoded = saved_file.get_content(...)

```python
file_content_properly_decoded = saved_file.get_content(encodings=['utf-8-sig', 'utf-8'])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(file_content_properly_decoded, test_content1)
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
utf8_bom_content = test_content1.encode('utf-8-sig')
_file: frappe.Document = frappe.get_doc({'doctype': 'File', 'file_name': 'utf8bom.txt', 'attached_to_doctype': self.attached_to_doctype1, 'attached_to_name': self.attached_to_docname1, 'content': utf8_bom_content, 'decode': False})
_file.save()
saved_file = frappe.get_doc('File', _file.name)
file_content_decoded = saved_file.get_content(encodings=['utf-8'])
self.assertEqual(file_content_decoded[0], '\ufeff')
file_content_properly_decoded = saved_file.get_content(encodings=['utf-8-sig', 'utf-8'])
self.assertEqual(file_content_properly_decoded, test_content1)
```

## Next Steps


---

*Source: test_file.py:257 | Complexity: Intermediate | Last updated: 2026-02-04*