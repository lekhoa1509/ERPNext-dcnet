# How To: Get Pending Invitations Api

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get pending invitations api

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

### Step 1: Assign invitation = self.get_dummy_invitation(...)

```python
invitation = self.get_dummy_invitation()
```

### Step 2: Call invitation.insert()

```python
invitation.insert()
```

### Step 3: Call invitation.reload()

```python
invitation.reload()
```

### Step 4: Assign pending_invitations = get_pending_invitations(...)

```python
pending_invitations = get_pending_invitations('frappe')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(pending_invitations), 1)
```

### Step 6: Assign pending_invitation = value

```python
pending_invitation = pending_invitations[0]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pending_invitation['name'], invitation.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pending_invitation['email'], invitation.email)
```

### Step 9: Assign roles = value

```python
roles = pending_invitation['roles']
```

### Step 10: Call self.assertIsInstance()

```python
self.assertIsInstance(roles, list)
```

### Step 11: Call self.assertSequenceEqual()

```python
self.assertSequenceEqual(roles, [r.role for r in invitation.roles])
```


## Complete Example

```python
# Workflow
invitation = self.get_dummy_invitation()
invitation.insert()
invitation.reload()
pending_invitations = get_pending_invitations('frappe')
self.assertEqual(len(pending_invitations), 1)
pending_invitation = pending_invitations[0]
self.assertEqual(pending_invitation['name'], invitation.name)
self.assertEqual(pending_invitation['email'], invitation.email)
roles = pending_invitation['roles']
self.assertIsInstance(roles, list)
self.assertSequenceEqual(roles, [r.role for r in invitation.roles])
```

## Next Steps


---

*Source: test_user_invitation.py:242 | Complexity: Advanced | Last updated: 2026-02-04*