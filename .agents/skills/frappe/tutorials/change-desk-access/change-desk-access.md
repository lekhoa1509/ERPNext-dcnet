# How To: Change Desk Access

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: if we change desk acecss from role, remove from user

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.role.role`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: 'if we change desk acecss from role, remove from user'

```python
'if we change desk acecss from role, remove from user'
```

### Step 2: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('User', 'test-user-for-desk-access@example.com')
```

### Step 3: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Role', 'desk-access-test')
```

### Step 4: Assign user = frappe.get_doc.insert(...)

```python
user = frappe.get_doc(doctype='User', email='test-user-for-desk-access@example.com', first_name='test').insert()
```

### Step 5: Assign role = frappe.get_doc.insert(...)

```python
role = frappe.get_doc(doctype='Role', role_name='desk-access-test', desk_access=0).insert()
```

### Step 6: Call user.add_roles()

```python
user.add_roles(role.name)
```

### Step 7: Call user.save()

```python
user.save()
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(user.user_type == 'Website User')
```

### Step 9: Assign role.desk_access = 1

```python
role.desk_access = 1
```

### Step 10: Call role.save()

```python
role.save()
```

### Step 11: Call user.reload()

```python
user.reload()
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(user.user_type == 'System User')
```

### Step 13: Assign role.desk_access = 0

```python
role.desk_access = 0
```

### Step 14: Call role.save()

```python
role.save()
```

### Step 15: Call user.reload()

```python
user.reload()
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(user.user_type == 'Website User')
```


## Complete Example

```python
# Workflow
'if we change desk acecss from role, remove from user'
frappe.delete_doc_if_exists('User', 'test-user-for-desk-access@example.com')
frappe.delete_doc_if_exists('Role', 'desk-access-test')
user = frappe.get_doc(doctype='User', email='test-user-for-desk-access@example.com', first_name='test').insert()
role = frappe.get_doc(doctype='Role', role_name='desk-access-test', desk_access=0).insert()
user.add_roles(role.name)
user.save()
self.assertTrue(user.user_type == 'Website User')
role.desk_access = 1
role.save()
user.reload()
self.assertTrue(user.user_type == 'System User')
role.desk_access = 0
role.save()
user.reload()
self.assertTrue(user.user_type == 'Website User')
```

## Next Steps


---

*Source: test_role.py:26 | Complexity: Advanced | Last updated: 2026-02-04*