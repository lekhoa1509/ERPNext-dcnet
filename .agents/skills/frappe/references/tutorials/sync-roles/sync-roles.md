# How To: Sync Roles

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test sync roles

## Prerequisites

**Required Modules:**
- `contextlib`
- `functools`
- `os`
- `ssl`
- `typing`
- `unittest`
- `ldap3`
- `ldap3`
- `frappe`
- `frappe.exceptions`
- `frappe.integrations.doctype.ldap_settings.ldap_settings`


## Step-by-Step Guide

### Step 1: Assign role_to_group_map = value

```python
role_to_group_map = {self.doc['ldap_groups'][0]['erpnext_role']: self.doc['ldap_groups'][0]['ldap_group'], self.doc['ldap_groups'][1]['erpnext_role']: self.doc['ldap_groups'][1]['ldap_group'], self.doc['ldap_groups'][2]['erpnext_role']: self.doc['ldap_groups'][2]['ldap_group'], 'Newsletter Manager': 'default_role', 'All': 'frappe_default_all', 'Guest': 'frappe_default_guest', 'Desk User': 'frappe_default_desk_user'}
```

### Step 2: Call frappe.get_doc.delete()

```python
frappe.get_doc('User', 'posix.user1@unit.testing').delete()
```

### Step 3: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc(self.user1doc)
```

### Step 4: Call user.insert()

```python
user.insert(ignore_permissions=True)
```

### Step 5: Assign test_user_data = value

```python
test_user_data = {'posix.user1': ['Users', 'Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user'], 'posix.user2': ['Users', 'Group3', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user']}
```

### Step 6: Assign test_user_doc = frappe.get_doc(...)

```python
test_user_doc = frappe.get_doc('User', f'{test_user}@unit.testing')
```

### Step 7: Assign test_user_roles = frappe.get_roles(...)

```python
test_user_roles = frappe.get_roles(f'{test_user}@unit.testing')
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(len(test_user_roles) == 2, 'User should only be a part of the All and Guest roles')
```

### Step 9: Call self.test_class.sync_roles()

```python
self.test_class.sync_roles(test_user_doc, test_user_data[test_user])
```

### Step 10: Call frappe.get_doc()

```python
frappe.get_doc('User', f'{test_user}@unit.testing')
```

### Step 11: Assign updated_user_roles = frappe.get_roles(...)

```python
updated_user_roles = frappe.get_roles(f'{test_user}@unit.testing')
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(len(updated_user_roles) == len(test_user_data[test_user]), f'syncing of the user roles failed. {len(updated_user_roles)} != {len(test_user_data[test_user])} for user {test_user}')
```

### Step 13: Assign test_user_data = value

```python
test_user_data = {'posix.user1': ['Domain Users', 'Domain Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user'], 'posix.user2': ['Domain Users', 'Enterprise Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user']}
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(role_to_group_map[user_role] in test_user_data[test_user], f'during sync_roles(), the user was given role {user_role} which should not have occurred')
```


## Complete Example

```python
# Workflow
if self.TEST_LDAP_SERVER.lower() == 'openldap':
    test_user_data = {'posix.user1': ['Users', 'Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user'], 'posix.user2': ['Users', 'Group3', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user']}
elif self.TEST_LDAP_SERVER.lower() == 'active directory':
    test_user_data = {'posix.user1': ['Domain Users', 'Domain Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user'], 'posix.user2': ['Domain Users', 'Enterprise Administrators', 'default_role', 'frappe_default_all', 'frappe_default_guest', 'frappe_default_desk_user']}
role_to_group_map = {self.doc['ldap_groups'][0]['erpnext_role']: self.doc['ldap_groups'][0]['ldap_group'], self.doc['ldap_groups'][1]['erpnext_role']: self.doc['ldap_groups'][1]['ldap_group'], self.doc['ldap_groups'][2]['erpnext_role']: self.doc['ldap_groups'][2]['ldap_group'], 'Newsletter Manager': 'default_role', 'All': 'frappe_default_all', 'Guest': 'frappe_default_guest', 'Desk User': 'frappe_default_desk_user'}
frappe.get_doc('User', 'posix.user1@unit.testing').delete()
user = frappe.get_doc(self.user1doc)
user.insert(ignore_permissions=True)
for test_user in test_user_data:
    test_user_doc = frappe.get_doc('User', f'{test_user}@unit.testing')
    test_user_roles = frappe.get_roles(f'{test_user}@unit.testing')
    self.assertTrue(len(test_user_roles) == 2, 'User should only be a part of the All and Guest roles')
    self.test_class.sync_roles(test_user_doc, test_user_data[test_user])
    frappe.get_doc('User', f'{test_user}@unit.testing')
    updated_user_roles = frappe.get_roles(f'{test_user}@unit.testing')
    self.assertTrue(len(updated_user_roles) == len(test_user_data[test_user]), f'syncing of the user roles failed. {len(updated_user_roles)} != {len(test_user_data[test_user])} for user {test_user}')
    for user_role in updated_user_roles:
        self.assertTrue(role_to_group_map[user_role] in test_user_data[test_user], f'during sync_roles(), the user was given role {user_role} which should not have occurred')
```

## Next Steps


---

*Source: test_ldap_settings.py:365 | Complexity: Advanced | Last updated: 2026-02-04*