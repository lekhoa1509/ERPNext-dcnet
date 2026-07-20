# How To: On Delete

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test on delete

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
frappe.set_user('Administrator')
self.delete_test_data()
self.upload_file()
```

## Step-by-Step Guide

### Step 1: Assign file = frappe.get_doc(...)

```python
file = frappe.get_doc('File', {'file_name': 'file_copy.txt'})
```

### Step 2: Call file.delete()

```python
file.delete()
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('File', _('Home/Test Folder 1'), 'file_size'), 0)
```

### Step 4: Assign folder = self.get_folder(...)

```python
folder = self.get_folder('Test Folder 3', 'Home/Test Folder 1')
```

### Step 5: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc({'doctype': 'File', 'file_name': 'folder_copy.txt', 'attached_to_name': '', 'attached_to_doctype': '', 'folder': folder.name, 'content': 'Testing folder copy example'})
```

### Step 6: Call _file.save()

```python
_file.save()
```

### Step 7: Assign folder = frappe.get_doc(...)

```python
folder = frappe.get_doc('File', 'Home/Test Folder 1/Test Folder 3')
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(ValidationError, folder.delete)
```


## Complete Example

```python
# Setup
frappe.set_user('Administrator')
self.delete_test_data()
self.upload_file()

# Workflow
file = frappe.get_doc('File', {'file_name': 'file_copy.txt'})
file.delete()
self.assertEqual(frappe.db.get_value('File', _('Home/Test Folder 1'), 'file_size'), 0)
folder = self.get_folder('Test Folder 3', 'Home/Test Folder 1')
_file = frappe.get_doc({'doctype': 'File', 'file_name': 'folder_copy.txt', 'attached_to_name': '', 'attached_to_doctype': '', 'folder': folder.name, 'content': 'Testing folder copy example'})
_file.save()
folder = frappe.get_doc('File', 'Home/Test Folder 1/Test Folder 3')
self.assertRaises(ValidationError, folder.delete)
```

## Next Steps


---

*Source: test_file.py:383 | Complexity: Advanced | Last updated: 2026-02-04*