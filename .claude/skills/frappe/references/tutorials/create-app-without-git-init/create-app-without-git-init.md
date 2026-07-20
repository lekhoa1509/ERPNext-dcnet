# How To: Create App Without Git Init

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test create app without git init

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

### Step 1: Assign app_name = 'test_app_no_git'

```python
app_name = 'test_app_no_git'
```

### Step 2: Assign hooks = self.default_hooks.copy(...)

```python
hooks = self.default_hooks.copy()
```

### Step 3: Assign hooks.app_name = app_name

```python
hooks.app_name = app_name
```

### Step 4: Call self.create_app()

```python
self.create_app(hooks, no_git=True)
```

### Step 5: Assign new_app_dir = os.path.join(...)

```python
new_app_dir = os.path.join(self.apps_dir, app_name)
```

### Step 6: Assign paths = self.get_paths(...)

```python
paths = self.get_paths(new_app_dir, app_name)
```

### Step 7: Call self.check_parsable_python_files()

```python
self.check_parsable_python_files(new_app_dir)
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(os.path.exists(path), msg=f"{path} shouldn't exist in {app_name} app")
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(path), msg=f'{path} should exist in {app_name} app')
```


## Complete Example

```python
# Workflow
app_name = 'test_app_no_git'
hooks = self.default_hooks.copy()
hooks.app_name = app_name
del hooks['create_github_workflow']
self.create_app(hooks, no_git=True)
new_app_dir = os.path.join(self.apps_dir, app_name)
paths = self.get_paths(new_app_dir, app_name)
for path in paths:
    if os.path.basename(path) in (self.git_folder, self.gitignore_file):
        self.assertFalse(os.path.exists(path), msg=f"{path} shouldn't exist in {app_name} app")
    else:
        self.assertTrue(os.path.exists(path), msg=f'{path} should exist in {app_name} app')
self.check_parsable_python_files(new_app_dir)
```

## Next Steps


---

*Source: test_boilerplate.py:142 | Complexity: Advanced | Last updated: 2026-02-04*