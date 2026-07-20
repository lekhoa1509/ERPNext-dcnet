# How To: Strip Exif Data

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test strip exif data

## Prerequisites

**Required Modules:**
- `io`
- `json`
- `os`
- `sys`
- `datetime`
- `decimal`
- `enum`
- `io`
- `mimetypes`
- `unittest.mock`
- `hypothesis`
- `hypothesis`
- `PIL`
- `frappe`
- `frappe.installer`
- `frappe.model.document`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.utils.change_log`
- `frappe.utils.data`
- `frappe.utils.dateutils`
- `frappe.utils.diff`
- `frappe.utils.identicon`
- `frappe.utils.image`
- `frappe.utils.make_random`
- `frappe.utils.response`
- `frappe.utils.synchronization`
- `frappe.utils.typing_validations`
- `decimal`
- `decimal`
- `frappe.utils.html_utils`
- `frappe.utils.html_utils`
- `frappe`
- `frappe.utils.xlsxutils`
- `frappe.boot`
- `frappe.desk.form.load`
- `frappe.utils.lazy_loader`
- `unittest.mock`
- `frappe.core.doctype.doctype.doctype`


## Step-by-Step Guide

### Step 1: Assign original_image = Image.open(...)

```python
original_image = Image.open(frappe.get_app_path('frappe', 'tests', 'data', 'exif_sample_image.jpg'))
```

### Step 2: Assign original_image_content = open.read(...)

```python
original_image_content = open(frappe.get_app_path('frappe', 'tests', 'data', 'exif_sample_image.jpg'), mode='rb').read()
```

### Step 3: Assign new_image_content = strip_exif_data(...)

```python
new_image_content = strip_exif_data(original_image_content, 'image/jpeg')
```

### Step 4: Assign new_image = Image.open(...)

```python
new_image = Image.open(io.BytesIO(new_image_content))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(new_image._getexif(), None)
```

### Step 6: Call self.assertNotEqual()

```python
self.assertNotEqual(original_image._getexif(), new_image._getexif())
```


## Complete Example

```python
# Workflow
original_image = Image.open(frappe.get_app_path('frappe', 'tests', 'data', 'exif_sample_image.jpg'))
original_image_content = open(frappe.get_app_path('frappe', 'tests', 'data', 'exif_sample_image.jpg'), mode='rb').read()
new_image_content = strip_exif_data(original_image_content, 'image/jpeg')
new_image = Image.open(io.BytesIO(new_image_content))
self.assertEqual(new_image._getexif(), None)
self.assertNotEqual(original_image._getexif(), new_image._getexif())
```

## Next Steps


---

*Source: test_utils.py:656 | Complexity: Intermediate | Last updated: 2026-02-04*