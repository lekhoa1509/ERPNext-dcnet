# How To: File Attachment On Update

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test file attachment on update

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

### Step 1: Assign doc = frappe.get_doc.insert(...)

```python
doc = frappe.get_doc(doctype=self.test_doctype, title='test for attachment on update').insert()
```

### Step 2: Assign file = frappe.get_doc.save(...)

```python
file = frappe.get_doc({'doctype': 'File', 'file_name': 'test_attach.txt', 'content': 'Test Content'}).save()
```

### Step 3: Assign doc.attachment = value

```python
doc.attachment = file.file_url
```

### Step 4: Call doc.save()

```python
doc.save()
```

### Step 5: Assign exists = frappe.db.exists(...)

```python
exists = frappe.db.exists('File', {'file_name': 'test_attach.txt', 'file_url': file.file_url, 'attached_to_doctype': self.test_doctype, 'attached_to_name': doc.name, 'attached_to_field': 'attachment'})
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(exists)
```


## Complete Example

```python
# Workflow
doc = frappe.get_doc(doctype=self.test_doctype, title='test for attachment on update').insert()
file = frappe.get_doc({'doctype': 'File', 'file_name': 'test_attach.txt', 'content': 'Test Content'}).save()
doc.attachment = file.file_url
doc.save()
exists = frappe.db.exists('File', {'file_name': 'test_attach.txt', 'file_url': file.file_url, 'attached_to_doctype': self.test_doctype, 'attached_to_name': doc.name, 'attached_to_field': 'attachment'})
self.assertTrue(exists)
```

## Next Steps


---

*Source: test_file.py:620 | Complexity: Intermediate | Last updated: 2026-02-04*