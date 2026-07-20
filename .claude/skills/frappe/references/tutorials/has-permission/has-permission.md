# How To: Has Permission

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test has permission

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.cache_manager`
- `frappe.desk.doctype.todo.todo`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe`
- `frappe`
- `os`
- `shutil`
- `frappe`
- `frappe.utils.fixtures`


## Step-by-Step Guide

### Step 1: Assign address_has_permission_hook = hooks.has_permission.get(...)

```python
address_has_permission_hook = hooks.has_permission.get('Address', [])
```

### Step 2: Call address_has_permission_hook.append()

```python
address_has_permission_hook.append('frappe.tests.test_hooks.custom_has_permission')
```

### Step 3: Assign unknown = address_has_permission_hook

```python
hooks.has_permission['Address'] = address_has_permission_hook
```

### Step 4: Assign wildcard_has_permission_hook = hooks.has_permission.get(...)

```python
wildcard_has_permission_hook = hooks.has_permission.get('*', [])
```

### Step 5: Call wildcard_has_permission_hook.append()

```python
wildcard_has_permission_hook.append('frappe.tests.test_hooks.custom_has_permission')
```

### Step 6: Assign unknown = wildcard_has_permission_hook

```python
hooks.has_permission['*'] = wildcard_has_permission_hook
```

### Step 7: Call frappe.client_cache.delete_value()

```python
frappe.client_cache.delete_value('app_hooks')
```

### Step 8: Assign username = 'test@example.com'

```python
username = 'test@example.com'
```

### Step 9: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', username)
```

### Step 10: Call user.add_roles()

```python
user.add_roles('System Manager')
```

### Step 11: Assign address = frappe.new_doc(...)

```python
address = frappe.new_doc('Address')
```

### Step 12: Assign note = frappe.new_doc(...)

```python
note = frappe.new_doc('Note')
```

### Step 13: Assign note.public = 1

```python
note.public = 1
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(frappe.has_permission('Address', doc=address, user=username))
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(frappe.has_permission('Note', doc=note, user=username))
```

### Step 16: Assign address.flags.dont_touch_me = True

```python
address.flags.dont_touch_me = True
```

### Step 17: Call self.assertFalse()

```python
self.assertFalse(frappe.has_permission('Address', doc=address, user=username))
```

### Step 18: Assign note.flags.dont_touch_me = True

```python
note.flags.dont_touch_me = True
```

### Step 19: Call self.assertFalse()

```python
self.assertFalse(frappe.has_permission('Note', doc=note, user=username))
```

### Step 20: Assign address_has_permission_hook = value

```python
address_has_permission_hook = [address_has_permission_hook]
```

### Step 21: Assign wildcard_has_permission_hook = value

```python
wildcard_has_permission_hook = [wildcard_has_permission_hook]
```


## Complete Example

```python
# Workflow
from frappe import hooks
address_has_permission_hook = hooks.has_permission.get('Address', [])
if isinstance(address_has_permission_hook, str):
    address_has_permission_hook = [address_has_permission_hook]
address_has_permission_hook.append('frappe.tests.test_hooks.custom_has_permission')
hooks.has_permission['Address'] = address_has_permission_hook
wildcard_has_permission_hook = hooks.has_permission.get('*', [])
if isinstance(wildcard_has_permission_hook, str):
    wildcard_has_permission_hook = [wildcard_has_permission_hook]
wildcard_has_permission_hook.append('frappe.tests.test_hooks.custom_has_permission')
hooks.has_permission['*'] = wildcard_has_permission_hook
frappe.client_cache.delete_value('app_hooks')
username = 'test@example.com'
user = frappe.get_doc('User', username)
user.add_roles('System Manager')
address = frappe.new_doc('Address')
note = frappe.new_doc('Note')
note.public = 1
self.assertTrue(frappe.has_permission('Address', doc=address, user=username))
self.assertTrue(frappe.has_permission('Note', doc=note, user=username))
address.flags.dont_touch_me = True
self.assertFalse(frappe.has_permission('Address', doc=address, user=username))
note.flags.dont_touch_me = True
self.assertFalse(frappe.has_permission('Note', doc=note, user=username))
```

## Next Steps


---

*Source: test_hooks.py:35 | Complexity: Advanced | Last updated: 2026-02-04*