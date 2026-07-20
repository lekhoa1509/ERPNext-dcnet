# How To: Invite By Email Api

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test invite by email api

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

### Step 1: Assign accepted_invite_email = value

```python
accepted_invite_email = emails[1]
```

### Step 2: Assign invitation = frappe.get_doc.insert(...)

```python
invitation = frappe.get_doc(doctype='User Invitation', email=accepted_invite_email, roles=[dict(role='System Manager')], redirect_to_path='/abc', app_name='frappe').insert()
```

### Step 3: Call invitation.accept()

```python
invitation.accept()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(len(self.get_email_names(False)), 1)
```

### Step 5: Assign pending_invite_email = value

```python
pending_invite_email = emails[2]
```

### Step 6: Call frappe.get_doc.insert()

```python
frappe.get_doc(doctype='User Invitation', email=pending_invite_email, roles=[dict(role='System Manager')], redirect_to_path='/abc', app_name='frappe').insert()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(self.get_email_names(False)), 2)
```

### Step 8: Assign email_to_invite = value

```python
email_to_invite = emails[3]
```

### Step 9: Assign res = invite_by_email(...)

```python
res = invite_by_email(emails=', '.join([accepted_invite_email, pending_invite_email, email_to_invite]), roles=['System Manager'], redirect_to_path='/xyz')
```

### Step 10: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['disabled_user_emails'], [])
```

### Step 11: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['accepted_invite_emails'], [accepted_invite_email])
```

### Step 12: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['pending_invite_emails'], [pending_invite_email])
```

### Step 13: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(res['invited_emails'], [email_to_invite])
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(self.get_email_names(False)), 3)
```

### Step 15: Assign user = frappe.get_doc(...)

```python
user = frappe.get_doc('User', invitation.email)
```

### Step 16: Call IntegrationTestUserInvitation.delete_invitation()

```python
IntegrationTestUserInvitation.delete_invitation(invitation.name)
```

### Step 17: Call frappe.delete_doc()

```python
frappe.delete_doc('User', user.name)
```


## Complete Example

```python
# Workflow
accepted_invite_email = emails[1]
invitation = frappe.get_doc(doctype='User Invitation', email=accepted_invite_email, roles=[dict(role='System Manager')], redirect_to_path='/abc', app_name='frappe').insert()
invitation.accept()
self.assertEqual(len(self.get_email_names(False)), 1)
pending_invite_email = emails[2]
frappe.get_doc(doctype='User Invitation', email=pending_invite_email, roles=[dict(role='System Manager')], redirect_to_path='/abc', app_name='frappe').insert()
self.assertEqual(len(self.get_email_names(False)), 2)
email_to_invite = emails[3]
res = invite_by_email(emails=', '.join([accepted_invite_email, pending_invite_email, email_to_invite]), roles=['System Manager'], redirect_to_path='/xyz')
self.assertSequenceEqual(res['disabled_user_emails'], [])
self.assertSequenceEqual(res['accepted_invite_emails'], [accepted_invite_email])
self.assertSequenceEqual(res['pending_invite_emails'], [pending_invite_email])
self.assertSequenceEqual(res['invited_emails'], [email_to_invite])
self.assertEqual(len(self.get_email_names(False)), 3)
user = frappe.get_doc('User', invitation.email)
IntegrationTestUserInvitation.delete_invitation(invitation.name)
frappe.delete_doc('User', user.name)
```

## Next Steps


---

*Source: test_user_invitation.py:139 | Complexity: Advanced | Last updated: 2026-02-04*