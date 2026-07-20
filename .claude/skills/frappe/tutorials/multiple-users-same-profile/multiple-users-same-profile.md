# How To: Multiple Users Same Profile

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Updates should propagate to all users linked to the same profile

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'Updates should propagate to all users linked to the same profile'

```python
'Updates should propagate to all users linked to the same profile'
```

### Step 2: Assign module_profile = frappe.get_doc.insert(...)

```python
module_profile = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile', 'block_modules': [{'module': 'Accounts'}]}).insert()
```

### Step 3: Assign user1 = frappe.get_doc.insert(...)

```python
user1 = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user1@example.com', 'first_name': 'User One'}).insert()
```

### Step 4: Assign user2 = frappe.get_doc.insert(...)

```python
user2 = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user2@example.com', 'first_name': 'User Two'}).insert()
```

### Step 5: Call module_profile.append()

```python
module_profile.append('block_modules', {'module': 'Projects'})
```

### Step 6: Call module_profile.save()

```python
module_profile.save()
```

### Step 7: Call user1.reload()

```python
user1.reload()
```

### Step 8: Call user2.reload()

```python
user2.reload()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual([bm.module for bm in user1.block_modules], ['Accounts', 'Projects'])
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual([bm.module for bm in user2.block_modules], ['Accounts', 'Projects'])
```

### Step 11: Assign u.module_profile = value

```python
u.module_profile = module_profile.name
```

### Step 12: Call u.save()

```python
u.save()
```


## Complete Example

```python
# Workflow
'Updates should propagate to all users linked to the same profile'
module_profile = frappe.get_doc({'doctype': 'Module Profile', 'module_profile_name': '_Test Module Profile', 'block_modules': [{'module': 'Accounts'}]}).insert()
user1 = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user1@example.com', 'first_name': 'User One'}).insert()
user2 = frappe.get_doc({'doctype': 'User', 'email': 'test-module-user2@example.com', 'first_name': 'User Two'}).insert()
for u in (user1, user2):
    u.module_profile = module_profile.name
    u.save()
module_profile.append('block_modules', {'module': 'Projects'})
module_profile.save()
user1.reload()
user2.reload()
self.assertEqual([bm.module for bm in user1.block_modules], ['Accounts', 'Projects'])
self.assertEqual([bm.module for bm in user2.block_modules], ['Accounts', 'Projects'])
```

## Next Steps


---

*Source: test_module_profile.py:100 | Complexity: Advanced | Last updated: 2026-02-04*