# How To: Clear Block Modules

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Clearing block_modules in profile should also clear them for users

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'Clearing block_modules in profile should also clear them for users'

```python
'Clearing block_modules in profile should also clear them for users'
```

### Step 2: Assign module_profile = frappe.get_doc.insert(...)

```python
module_profile = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile', 'block_modules': [{'module': 'Accounts'}]}).insert()
```

### Step 3: Assign user = frappe.get_doc.insert(...)

```python
user = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user1@example.com', 'first_name': 'Test User'}).insert()
```

### Step 4: Assign user.module_profile = value

```python
user.module_profile = module_profile.name
```

### Step 5: Call user.save()

```python
user.save()
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(user.block_modules)
```

### Step 7: Assign module_profile.block_modules = value

```python
module_profile.block_modules = []
```

### Step 8: Call module_profile.save()

```python
module_profile.save()
```

### Step 9: Call user.reload()

```python
user.reload()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(user.block_modules, [])
```


## Complete Example

```python
# Workflow
'Clearing block_modules in profile should also clear them for users'
module_profile = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile', 'block_modules': [{'module': 'Accounts'}]}).insert()
user = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user1@example.com', 'first_name': 'Test User'}).insert()
user.module_profile = module_profile.name
user.save()
self.assertTrue(user.block_modules)
module_profile.block_modules = []
module_profile.save()
user.reload()
self.assertEqual(user.block_modules, [])
```

## Next Steps


---

*Source: test_module_profile.py:76 | Complexity: Advanced | Last updated: 2026-02-04*