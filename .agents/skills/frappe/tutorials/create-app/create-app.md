# How To: Create App

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test create app

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

### Step 1: Assign app_name = 'test_app'

```python
app_name = 'test_app'
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
self.create_app(hooks)
```

### Step 5: Assign new_app_dir = os.path.join(...)

```python
new_app_dir = os.path.join(self.bench_path, self.apps_dir, app_name)
```

### Step 6: Assign paths = self.get_paths(...)

```python
paths = self.get_paths(new_app_dir, app_name)
```

### Step 7: Call self.check_parsable_python_files()

```python
self.check_parsable_python_files(new_app_dir)
```

### Step 8: Assign app_repo = git.Repo(...)

```python
app_repo = git.Repo(new_app_dir)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(app_repo.active_branch.name, 'develop')
```

### Step 10: Assign patches_file = os.path.join(...)

```python
patches_file = os.path.join(new_app_dir, app_name, 'patches.txt')
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(patches_file), msg=f'{patches_file} not found')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(parse_as_configfile(patches_file), [])
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(os.path.exists(path), msg=f'{path} should exist in {app_name} app')
```


## Complete Example

```python
# Workflow
app_name = 'test_app'
hooks = self.default_hooks.copy()
hooks.app_name = app_name
del hooks['create_github_workflow']
self.create_app(hooks)
new_app_dir = os.path.join(self.bench_path, self.apps_dir, app_name)
paths = self.get_paths(new_app_dir, app_name)
for path in paths:
    self.assertTrue(os.path.exists(path), msg=f'{path} should exist in {app_name} app')
self.check_parsable_python_files(new_app_dir)
app_repo = git.Repo(new_app_dir)
self.assertEqual(app_repo.active_branch.name, 'develop')
patches_file = os.path.join(new_app_dir, app_name, 'patches.txt')
self.assertTrue(os.path.exists(patches_file), msg=f'{patches_file} not found')
self.assertEqual(parse_as_configfile(patches_file), [])
```

## Next Steps


---

*Source: test_boilerplate.py:116 | Complexity: Advanced | Last updated: 2026-02-04*