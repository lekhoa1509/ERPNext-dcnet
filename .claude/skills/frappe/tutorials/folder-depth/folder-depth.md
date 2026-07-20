# How To: Folder Depth

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test folder depth

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

### Step 1: Assign result1 = self.get_folder(...)

```python
result1 = self.get_folder('d1', 'Home')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(result1.name, 'Home/d1')
```

### Step 3: Assign result2 = self.get_folder(...)

```python
result2 = self.get_folder('d2', 'Home/d1')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(result2.name, 'Home/d1/d2')
```

### Step 5: Assign result3 = self.get_folder(...)

```python
result3 = self.get_folder('d3', 'Home/d1/d2')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result3.name, 'Home/d1/d2/d3')
```

### Step 7: Assign result4 = self.get_folder(...)

```python
result4 = self.get_folder('d4', 'Home/d1/d2/d3')
```

### Step 8: Assign _file = frappe.get_doc(...)

```python
_file = frappe.get_doc({'doctype': 'File', 'file_name': 'folder_copy.txt', 'attached_to_name': '', 'attached_to_doctype': '', 'folder': result4.name, 'content': 'Testing folder copy example'})
```

### Step 9: Call _file.save()

```python
_file.save()
```


## Complete Example

```python
# Setup
frappe.set_user('Administrator')
self.delete_test_data()
self.upload_file()

# Workflow
result1 = self.get_folder('d1', 'Home')
self.assertEqual(result1.name, 'Home/d1')
result2 = self.get_folder('d2', 'Home/d1')
self.assertEqual(result2.name, 'Home/d1/d2')
result3 = self.get_folder('d3', 'Home/d1/d2')
self.assertEqual(result3.name, 'Home/d1/d2/d3')
result4 = self.get_folder('d4', 'Home/d1/d2/d3')
_file = frappe.get_doc({'doctype': 'File', 'file_name': 'folder_copy.txt', 'attached_to_name': '', 'attached_to_doctype': '', 'folder': result4.name, 'content': 'Testing folder copy example'})
_file.save()
```

## Next Steps


---

*Source: test_file.py:334 | Complexity: Advanced | Last updated: 2026-02-04*