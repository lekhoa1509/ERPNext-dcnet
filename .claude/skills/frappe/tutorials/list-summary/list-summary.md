# How To: List Summary

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test list summary

## Prerequisites

**Required Modules:**
- `base64`
- `requests`
- `frappe`
- `frappe.core.doctype.user.user`
- `frappe.frappeclient`
- `frappe.model`
- `frappe.tests`
- `frappe.utils.data`


## Step-by-Step Guide

### Step 1: Assign server = FrappeClient(...)

```python
server = FrappeClient(get_url(), 'Administrator', self.PASSWORD, verify=False)
```

### Step 2: Call server.insert_many()

```python
server.insert_many([{'doctype': 'Note', 'title': 'Sing'}, {'doctype': 'Note', 'title': 'a'}, {'doctype': 'Note', 'title': 'song'}, {'doctype': 'Note', 'title': 'of'}, {'doctype': 'Note', 'title': 'sixpence'}])
```

### Step 3: Assign notes = server.get_list(...)

```python
notes = server.get_list('Note', fields=['title'], order_by='creation desc')
```

### Step 4: Assign notes = value

```python
notes = [d.get('title') for d in notes]
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(notes[0], 'sixpence')
```

### Step 6: Assign getlist_users = server.get_list(...)

```python
getlist_users = server.get_list('User', fields=[{'COUNT': 'name', 'as': 'user_count'}], filters={'user_type': 'System User'}, group_by='user_type')
```

### Step 7: Assign getall_users = frappe.db.get_all(...)

```python
getall_users = frappe.db.get_all('User', fields=[{'COUNT': 'name', 'as': 'system_user_count'}], filters={'user_type': 'System User'}, group_by='user_type')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(getlist_users[0]['user_count'], getall_users[0]['system_user_count'])
```


## Complete Example

```python
# Workflow
server = FrappeClient(get_url(), 'Administrator', self.PASSWORD, verify=False)
server.insert_many([{'doctype': 'Note', 'title': 'Sing'}, {'doctype': 'Note', 'title': 'a'}, {'doctype': 'Note', 'title': 'song'}, {'doctype': 'Note', 'title': 'of'}, {'doctype': 'Note', 'title': 'sixpence'}])
notes = server.get_list('Note', fields=['title'], order_by='creation desc')
notes = [d.get('title') for d in notes]
self.assertEqual(notes[0], 'sixpence')
getlist_users = server.get_list('User', fields=[{'COUNT': 'name', 'as': 'user_count'}], filters={'user_type': 'System User'}, group_by='user_type')
getall_users = frappe.db.get_all('User', fields=[{'COUNT': 'name', 'as': 'system_user_count'}], filters={'user_type': 'System User'}, group_by='user_type')
self.assertEqual(getlist_users[0]['user_count'], getall_users[0]['system_user_count'])
```

## Next Steps


---

*Source: test_frappe_client.py:55 | Complexity: Advanced | Last updated: 2026-02-04*