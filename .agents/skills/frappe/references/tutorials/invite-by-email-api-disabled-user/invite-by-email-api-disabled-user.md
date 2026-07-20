# How To: Invite By Email Api Disabled User

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test invite by email api disabled user

## Prerequisites

**Required Modules:**
- `re`
- `frappe`
- `frappe.utils`
- `frappe.core.api.user_invitation`
- `frappe.core.doctype.user_invitation.user_invitation`
- `frappe.tests`

**Required Fixtures:**
- `api_client` fixture


## Step-by-Step Guide

### Step 1: Assign user = frappe.new_doc(...)

```python
user = frappe.new_doc('User')
```

### Step 2: Assign user.first_name = 'Random'

```python
user.first_name = 'Random'
```

### Step 3: Assign user.last_name = 'User'

```python
user.last_name = 'User'
```

### Step 4: Assign user.email = value

```python
user.email = emails[5]
```

### Step 5: Call user.append_roles()

```python
user.append_roles('System Manager')
```

### Step 6: Call user.insert()

```python
user.insert()
```

### Step 7: Call user.reload()

```python
user.reload()
```

### Step 8: Assign user.enabled = 0

```python
user.enabled = 0
```

### Step 9: Call user.save()

```python
user.save()
```

### Step 10: Assign res = invite_by_email(...)

```python
res = invite_by_email(emails=user.email, roles=['System Manager'], redirect_to_path='/xyz')
```

### Step 11: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['disabled_user_emails'], [user.email])
```

### Step 12: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['accepted_invite_emails'], [])
```

### Step 13: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['pending_invite_emails'], [])
```

### Step 14: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['invited_emails'], [])
```

### Step 15: Call frappe.delete_doc()

```python
frappe.delete_doc('User', user.email)
```


## Complete Example

```python
# Workflow
user = frappe.new_doc('User')
user.first_name = 'Random'
user.last_name = 'User'
user.email = emails[5]
user.append_roles('System Manager')
user.insert()
user.reload()
user.enabled = 0
user.save()
res = invite_by_email(emails=user.email, roles=['System Manager'], redirect_to_path='/xyz')
self.assertSequenceEqual(res['disabled_user_emails'], [user.email])
self.assertSequenceEqual(res['accepted_invite_emails'], [])
self.assertSequenceEqual(res['pending_invite_emails'], [])
self.assertSequenceEqual(res['invited_emails'], [])
frappe.delete_doc('User', user.email)
```

## Next Steps


---

*Source: test_user_invitation.py:174 | Complexity: Advanced | Last updated: 2026-02-04*