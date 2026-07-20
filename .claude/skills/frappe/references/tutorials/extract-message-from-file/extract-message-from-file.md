# How To: Extract Message From File

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test extract message from file

## Prerequisites

**Required Modules:**
- `os`
- `textwrap`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.translate`
- `frappe`
- `frappe.gettext.extractors.javascript`
- `frappe.tests`
- `frappe.translate`
- `frappe.utils`
- `pathlib`


## Step-by-Step Guide

### Step 1: Assign data = frappe.translate.get_messages_from_file(...)

```python
data = frappe.translate.get_messages_from_file(translation_string_file)
```

### Step 2: Assign bench_path = get_bench_path(...)

```python
bench_path = get_bench_path()
```

### Step 3: Assign file_path = frappe.get_app_path(...)

```python
file_path = frappe.get_app_path('frappe', 'tests', 'translation_test_file.txt')
```

### Step 4: Assign exp_filename = os.path.relpath(...)

```python
exp_filename = os.path.relpath(file_path, bench_path)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(data), len(expected_output), msg=f'Mismatched output:\nExpected: {expected_output}\nFound: {data}')
```

### Step 6: Assign unknown = extracted

```python
ext_filename, ext_message, ext_context, ext_line = extracted
```

### Step 7: Assign unknown = expected

```python
exp_message, exp_context, exp_line = expected
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(ext_filename, exp_filename)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(ext_message, exp_message)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(ext_context, exp_context)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(ext_line, exp_line)
```


## Complete Example

```python
# Workflow
data = frappe.translate.get_messages_from_file(translation_string_file)
bench_path = get_bench_path()
file_path = frappe.get_app_path('frappe', 'tests', 'translation_test_file.txt')
exp_filename = os.path.relpath(file_path, bench_path)
self.assertEqual(len(data), len(expected_output), msg=f'Mismatched output:\nExpected: {expected_output}\nFound: {data}')
for extracted, expected in zip(data, expected_output, strict=False):
    ext_filename, ext_message, ext_context, ext_line = extracted
    exp_message, exp_context, exp_line = expected
    self.assertEqual(ext_filename, exp_filename)
    self.assertEqual(ext_message, exp_message)
    self.assertEqual(ext_context, exp_context)
    self.assertEqual(ext_line, exp_line)
```

## Next Steps


---

*Source: test_translate.py:65 | Complexity: Advanced | Last updated: 2026-02-04*