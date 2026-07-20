# How To: New Patch Util

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test new patch util

## Prerequisites

**Required Modules:**
- `ast`
- `copy`
- `glob`
- `os`
- `pathlib`
- `shutil`
- `unittest`
- `io`
- `unittest.mock`
- `git`
- `yaml`
- `frappe`
- `frappe.modules.patch_handler`
- `frappe.utils.boilerplate`


## Step-by-Step Guide

### Step 1: Assign user_inputs = value

```python
user_inputs = ['frappe', 'User', 'Delete all users', '', 'Y']
```

### Step 2: Assign patches_txt = pathlib.Path(...)

```python
patches_txt = pathlib.Path(pathlib.Path(frappe.get_app_path('frappe', 'patches.txt')))
```

### Step 3: Assign original_patches = patches_txt.read_text(...)

```python
original_patches = patches_txt.read_text()
```

### Step 4: Assign patches = get_all_patches(...)

```python
patches = get_all_patches()
```

### Step 5: Assign expected_patch = 'frappe.core.doctype.user.patches.delete_all_users'

```python
expected_patch = 'frappe.core.doctype.user.patches.delete_all_users'
```

### Step 6: Call self.assertIn()

```python
self.assertIn(expected_patch, patches)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(patch_creator.patch_file.exists())
```

### Step 8: Call shutil.rmtree()

```python
shutil.rmtree(patch_creator.patch_file.parents[0])
```

### Step 9: Call patches_txt.write_text()

```python
patches_txt.write_text(original_patches)
```

### Step 10: Assign patch_creator = PatchCreator(...)

```python
patch_creator = PatchCreator()
```

### Step 11: Call patch_creator.fetch_user_inputs()

```python
patch_creator.fetch_user_inputs()
```

### Step 12: Call patch_creator.create_patch_file()

```python
patch_creator.create_patch_file()
```


## Complete Example

```python
# Workflow
user_inputs = ['frappe', 'User', 'Delete all users', '', 'Y']
patches_txt = pathlib.Path(pathlib.Path(frappe.get_app_path('frappe', 'patches.txt')))
original_patches = patches_txt.read_text()
with patch('sys.stdin', self.get_user_input_stream(user_inputs)):
    patch_creator = PatchCreator()
    patch_creator.fetch_user_inputs()
    patch_creator.create_patch_file()
patches = get_all_patches()
expected_patch = 'frappe.core.doctype.user.patches.delete_all_users'
self.assertIn(expected_patch, patches)
self.assertTrue(patch_creator.patch_file.exists())
shutil.rmtree(patch_creator.patch_file.parents[0])
patches_txt.write_text(original_patches)
```

## Next Steps


---

*Source: test_boilerplate.py:182 | Complexity: Advanced | Last updated: 2026-02-04*