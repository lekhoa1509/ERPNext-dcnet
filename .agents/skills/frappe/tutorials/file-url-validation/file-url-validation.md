# How To: File Url Validation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test file url validation

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

### Step 1: Call test_file.update()

```python
test_file.update({'file_name': 'logo', 'file_url': 'https://frappe.io/files/frappe.png'})
```

### Step 2: Call self.assertIsNone()

```python
self.assertIsNone(test_file.validate())
```

### Step 3: Assign test_file.file_url = '/usr/bin/man'

```python
test_file.file_url = '/usr/bin/man'
```

### Step 4: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(ValidationError, f'Cannot access file path {test_file.file_url}', test_file.validate)
```

### Step 5: Assign test_file.file_url = None

```python
test_file.file_url = None
```

### Step 6: Assign test_file.file_name = '/usr/bin/man'

```python
test_file.file_name = '/usr/bin/man'
```

### Step 7: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(ValidationError, 'There is some problem with the file url', test_file.validate)
```

### Step 8: Assign test_file.file_url = None

```python
test_file.file_url = None
```

### Step 9: Assign test_file.file_name = '_file'

```python
test_file.file_name = '_file'
```

### Step 10: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(IOError, 'does not exist', test_file.validate)
```

### Step 11: Assign test_file.file_url = None

```python
test_file.file_url = None
```

### Step 12: Assign test_file.file_name = '/private/files/_file'

```python
test_file.file_name = '/private/files/_file'
```

### Step 13: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(ValidationError, 'File name cannot have', test_file.validate)
```


## Complete Example

```python
# Setup
frappe.set_user('Administrator')
self.delete_test_data()
self.upload_file()

# Workflow
test_file: File = frappe.new_doc('File')
test_file.update({'file_name': 'logo', 'file_url': 'https://frappe.io/files/frappe.png'})
self.assertIsNone(test_file.validate())
test_file.file_url = '/usr/bin/man'
self.assertRaisesRegex(ValidationError, f'Cannot access file path {test_file.file_url}', test_file.validate)
test_file.file_url = None
test_file.file_name = '/usr/bin/man'
self.assertRaisesRegex(ValidationError, 'There is some problem with the file url', test_file.validate)
test_file.file_url = None
test_file.file_name = '_file'
self.assertRaisesRegex(IOError, 'does not exist', test_file.validate)
test_file.file_url = None
test_file.file_name = '/private/files/_file'
self.assertRaisesRegex(ValidationError, 'File name cannot have', test_file.validate)
```

## Next Steps


---

*Source: test_file.py:462 | Complexity: Advanced | Last updated: 2026-02-04*