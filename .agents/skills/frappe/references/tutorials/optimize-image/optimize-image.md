# How To: Optimize Image

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test optimize image

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

### Step 1: Assign image_file_path = frappe.get_app_path(...)

```python
image_file_path = frappe.get_app_path('frappe', 'tests', 'data', 'sample_image_for_optimization.jpg')
```

### Step 2: Assign content_type = value

```python
content_type = guess_type(image_file_path)[0]
```

### Step 3: Assign original_content = open.read(...)

```python
original_content = open(image_file_path, mode='rb').read()
```

### Step 4: Assign optimized_content = optimize_image(...)

```python
optimized_content = optimize_image(original_content, content_type, max_width=500, max_height=500)
```

### Step 5: Assign optimized_image = Image.open(...)

```python
optimized_image = Image.open(io.BytesIO(optimized_content))
```

### Step 6: Assign unknown = value

```python
width, height = optimized_image.size
```

### Step 7: Call self.assertLessEqual()

```python
self.assertLessEqual(width, 500)
```

### Step 8: Call self.assertLessEqual()

```python
self.assertLessEqual(height, 500)
```

### Step 9: Call self.assertLess()

```python
self.assertLess(len(optimized_content), len(original_content))
```


## Complete Example

```python
# Workflow
image_file_path = frappe.get_app_path('frappe', 'tests', 'data', 'sample_image_for_optimization.jpg')
content_type = guess_type(image_file_path)[0]
original_content = open(image_file_path, mode='rb').read()
optimized_content = optimize_image(original_content, content_type, max_width=500, max_height=500)
optimized_image = Image.open(io.BytesIO(optimized_content))
width, height = optimized_image.size
self.assertLessEqual(width, 500)
self.assertLessEqual(height, 500)
self.assertLess(len(optimized_content), len(original_content))
```

## Next Steps


---

*Source: test_utils.py:669 | Complexity: Advanced | Last updated: 2026-02-04*