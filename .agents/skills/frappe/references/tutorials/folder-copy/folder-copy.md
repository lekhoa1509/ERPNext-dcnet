# How To: Folder Copy

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test folder copy

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

### Step 1: Assign folder = self.get_folder(...)

```python
folder = self.get_folder('Test Folder 2', 'Home')
```

### Step 2: Assign folder = self.get_folder(...)

```python
folder = self.get_folder('Test Folder 3', 'Home/Test Folder 2')
```

### Step 3: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc({'doctype': 'File', 'file_name': 'folder_copy.txt', 'attached_to_name': '', 'attached_to_doctype': '', 'folder': folder.name, 'content': 'Testing folder copy example'})
```

### Step 4: Call _file.save()

```python
_file.save()
```

### Step 5: Call move_file()

```python
move_file([{'name': folder.name}], 'Home/Test Folder 1', folder.folder)
```

### Step 6: Assign file = frappe.get_doc(...)

```python
file = frappe.get_doc('File', {'file_name': 'folder_copy.txt'})
```

### Step 7: Assign file_copy_txt = frappe.get_value(...)

```python
file_copy_txt = frappe.get_value('File', {'file_name': 'file_copy.txt'})
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(_('Home/Test Folder 1/Test Folder 3'), file.folder)
```

### Step 9: Call frappe.get_doc.delete()

```python
frappe.get_doc('File', file_copy_txt).delete()
```


## Complete Example

```python
# Setup
frappe.set_user('Administrator')
self.delete_test_data()
self.upload_file()

# Workflow
folder = self.get_folder('Test Folder 2', 'Home')
folder = self.get_folder('Test Folder 3', 'Home/Test Folder 2')
_file = frappe.get_doc({'doctype': 'File', 'file_name': 'folder_copy.txt', 'attached_to_name': '', 'attached_to_doctype': '', 'folder': folder.name, 'content': 'Testing folder copy example'})
_file.save()
move_file([{'name': folder.name}], 'Home/Test Folder 1', folder.folder)
file = frappe.get_doc('File', {'file_name': 'folder_copy.txt'})
file_copy_txt = frappe.get_value('File', {'file_name': 'file_copy.txt'})
if file_copy_txt:
    frappe.get_doc('File', file_copy_txt).delete()
self.assertEqual(_('Home/Test Folder 1/Test Folder 3'), file.folder)
```

## Next Steps


---

*Source: test_file.py:354 | Complexity: Advanced | Last updated: 2026-02-04*