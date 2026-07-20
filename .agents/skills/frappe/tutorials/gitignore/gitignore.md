# How To: Gitignore

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gitignore

## Prerequisites

**Required Modules:**
- `frappe.gettext.translate`
- `frappe.tests`
- `os`
- `frappe`


## Step-by-Step Guide

### Step 1: Assign is_gitignored = get_is_gitignored_function_for_app(...)

```python
is_gitignored = get_is_gitignored_function_for_app('frappe')
```

### Step 2: Assign file_name = 'frappe/public/dist/test_translate_test_gitignore.js'

```python
file_name = 'frappe/public/dist/test_translate_test_gitignore.js'
```

### Step 3: Assign file_path = frappe.get_app_source_path(...)

```python
file_path = frappe.get_app_source_path('frappe', file_name)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(is_gitignored('frappe/public/node_modules'))
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(is_gitignored('frappe/public/dist'))
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(is_gitignored('frappe/public/dist/sub'))
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(is_gitignored(file_name))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(is_gitignored(file_path))
```

### Step 9: Call self.assertFalse()

```python
self.assertFalse(is_gitignored('frappe/public/dist2'))
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(is_gitignored('frappe/public/dist2/sub'))
```

### Step 11: Call os.makedirs()

```python
os.makedirs(os.path.dirname(file_path), exist_ok=True)
```

### Step 12: Assign pot_path = get_pot_path(...)

```python
pot_path = get_pot_path('frappe')
```

### Step 13: Call pot_path.unlink()

```python
pot_path.unlink(missing_ok=True)
```

### Step 14: Call generate_pot()

```python
generate_pot('frappe')
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(pot_path.exists())
```

### Step 16: Call self.assertNotIn()

```python
self.assertNotIn('test_translate_test_gitignore', pot_path.read_text())
```

### Step 17: Call os.remove()

```python
os.remove(file_path)
```

### Step 18: Call self.assertTrue()

```python
self.assertTrue(get_is_gitignored_function_for_app(None)('frappe/public/dist'))
```

### Step 19: Call f.write()

```python
f.write('__("test_translate_test_gitignore")')
```


## Complete Example

```python
# Workflow
import os
import frappe
is_gitignored = get_is_gitignored_function_for_app('frappe')
file_name = 'frappe/public/dist/test_translate_test_gitignore.js'
file_path = frappe.get_app_source_path('frappe', file_name)
self.assertTrue(is_gitignored('frappe/public/node_modules'))
self.assertTrue(is_gitignored('frappe/public/dist'))
self.assertTrue(is_gitignored('frappe/public/dist/sub'))
self.assertTrue(is_gitignored(file_name))
self.assertTrue(is_gitignored(file_path))
self.assertFalse(is_gitignored('frappe/public/dist2'))
self.assertFalse(is_gitignored('frappe/public/dist2/sub'))
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, 'w') as f:
    f.write('__("test_translate_test_gitignore")')
pot_path = get_pot_path('frappe')
pot_path.unlink(missing_ok=True)
generate_pot('frappe')
self.assertTrue(pot_path.exists())
self.assertNotIn('test_translate_test_gitignore', pot_path.read_text())
os.remove(file_path)
self.assertTrue(get_is_gitignored_function_for_app(None)('frappe/public/dist'))
```

## Next Steps


---

*Source: test_translate.py:67 | Complexity: Advanced | Last updated: 2026-02-04*