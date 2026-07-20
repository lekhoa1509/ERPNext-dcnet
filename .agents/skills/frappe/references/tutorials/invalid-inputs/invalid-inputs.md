# How To: Invalid Inputs

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test invalid inputs

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

### Step 1: Assign invalid_inputs = copy.copy(...)

```python
invalid_inputs = copy.copy(self.default_user_input)
```

### Step 2: Assign unknown = value

```python
invalid_inputs[0] = ['1nvalid Title', 'valid title']
```

### Step 3: Assign unknown = value

```python
invalid_inputs[3] = ['notavalidemail', 'what@is@this.email', 'example@example.org']
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(hooks.app_title, 'valid title')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(hooks.app_email, 'example@example.org')
```

### Step 6: Assign hooks = _get_user_inputs(...)

```python
hooks = _get_user_inputs(self.default_hooks.app_name)
```


## Complete Example

```python
# Workflow
invalid_inputs = copy.copy(self.default_user_input)
invalid_inputs[0] = ['1nvalid Title', 'valid title']
invalid_inputs[3] = ['notavalidemail', 'what@is@this.email', 'example@example.org']
with patch('sys.stdin', self.get_user_input_stream(invalid_inputs)):
    hooks = _get_user_inputs(self.default_hooks.app_name)
self.assertEqual(hooks.app_title, 'valid title')
self.assertEqual(hooks.app_email, 'example@example.org')
```

## Next Steps


---

*Source: test_boilerplate.py:99 | Complexity: Intermediate | Last updated: 2026-02-04*