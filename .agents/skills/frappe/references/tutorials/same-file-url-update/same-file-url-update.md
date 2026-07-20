# How To: Same File Url Update

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test same file url update

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

### Step 1: Assign unknown = make_test_doc(...)

```python
attached_to_doctype1, attached_to_docname1 = make_test_doc()
```

### Step 2: Assign unknown = make_test_doc(...)

```python
attached_to_doctype2, attached_to_docname2 = make_test_doc()
```

### Step 3: Assign file1 = frappe.get_doc.insert(...)

```python
file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'file1.txt', 'attached_to_doctype': attached_to_doctype1, 'attached_to_name': attached_to_docname1, 'is_private': 1, 'content': test_content1}).insert()
```

### Step 4: Assign file2 = frappe.get_doc.insert(...)

```python
file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'file2.txt', 'attached_to_doctype': attached_to_doctype2, 'attached_to_name': attached_to_docname2, 'is_private': 1, 'content': test_content1}).insert()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(file1.is_private, file2.is_private, 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(file1.file_url, file2.file_url)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(file1.get_full_path()))
```

### Step 8: Assign file1.is_private = 0

```python
file1.is_private = 0
```

### Step 9: Call file1.save()

```python
file1.save()
```

### Step 10: Assign file2 = frappe.get_doc(...)

```python
file2 = frappe.get_doc('File', file2.name)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(file1.is_private, file2.is_private, 0)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(file1.file_url, file2.file_url)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(file2.get_full_path()))
```


## Complete Example

```python
# Setup
frappe.set_user('Administrator')
self.delete_test_data()
self.upload_file()

# Workflow
attached_to_doctype1, attached_to_docname1 = make_test_doc()
attached_to_doctype2, attached_to_docname2 = make_test_doc()
file1 = frappe.get_doc({'doctype': 'File', 'file_name': 'file1.txt', 'attached_to_doctype': attached_to_doctype1, 'attached_to_name': attached_to_docname1, 'is_private': 1, 'content': test_content1}).insert()
file2 = frappe.get_doc({'doctype': 'File', 'file_name': 'file2.txt', 'attached_to_doctype': attached_to_doctype2, 'attached_to_name': attached_to_docname2, 'is_private': 1, 'content': test_content1}).insert()
self.assertEqual(file1.is_private, file2.is_private, 1)
self.assertEqual(file1.file_url, file2.file_url)
self.assertTrue(os.path.exists(file1.get_full_path()))
file1.is_private = 0
file1.save()
file2 = frappe.get_doc('File', file2.name)
self.assertEqual(file1.is_private, file2.is_private, 0)
self.assertEqual(file1.file_url, file2.file_url)
self.assertTrue(os.path.exists(file2.get_full_path()))
```

## Next Steps


---

*Source: test_file.py:405 | Complexity: Advanced | Last updated: 2026-02-04*