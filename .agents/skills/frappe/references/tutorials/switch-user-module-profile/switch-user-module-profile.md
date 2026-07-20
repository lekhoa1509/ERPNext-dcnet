# How To: Switch User Module Profile

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Switching user to a different profile updates their block_modules

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'Switching user to a different profile updates their block_modules'

```python
'Switching user to a different profile updates their block_modules'
```

### Step 2: Assign profile1 = frappe.get_doc.insert(...)

```python
profile1 = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile', 'block_modules': [{'module': 'Accounts'}]}).insert()
```

### Step 3: Assign profile2 = frappe.get_doc.insert(...)

```python
profile2 = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile 2', 'block_modules': [{'module': 'HR'}]}).insert()
```

### Step 4: Assign user = frappe.get_doc.insert(...)

```python
user = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user1@example.com', 'first_name': 'Test User'}).insert()
```

### Step 5: Assign user.module_profile = value

```python
user.module_profile = profile1.name
```

### Step 6: Call user.save()

```python
user.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual([bm.module for bm in user.block_modules], ['Accounts'])
```

### Step 8: Assign user.module_profile = value

```python
user.module_profile = profile2.name
```

### Step 9: Call user.save()

```python
user.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual([bm.module for bm in user.block_modules], ['HR'])
```


## Complete Example

```python
# Workflow
'Switching user to a different profile updates their block_modules'
profile1 = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile', 'block_modules': [{'module': 'Accounts'}]}).insert()
profile2 = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile 2', 'block_modules': [{'module': 'HR'}]}).insert()
user = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user1@example.com', 'first_name': 'Test User'}).insert()
user.module_profile = profile1.name
user.save()
self.assertEqual([bm.module for bm in user.block_modules], ['Accounts'])
user.module_profile = profile2.name
user.save()
self.assertEqual([bm.module for bm in user.block_modules], ['HR'])
```

## Next Steps


---

*Source: test_module_profile.py:129 | Complexity: Advanced | Last updated: 2026-02-04*