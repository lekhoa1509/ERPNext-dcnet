# How To: Share

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test share

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.user.user`
- `frappe.desk.form.assign_to`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign todo = get_todo(...)

```python
todo = get_todo()
```

### Step 2: Assign user = get_user(...)

```python
user = get_user()
```

### Step 3: Call frappe.share.add()

```python
frappe.share.add('ToDo', todo.name, user, notify=1)
```

### Step 4: Assign log_type = frappe.db.get_value(...)

```python
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(log_type, 'Share')
```

### Step 6: Assign email = get_last_email_queue(...)

```python
email = get_last_email_queue()
```

### Step 7: Assign content = value

```python
content = f'Subject: {frappe.utils.get_fullname(frappe.session.user)} shared a document ToDo'
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(content in email.message)
```


## Complete Example

```python
# Workflow
todo = get_todo()
user = get_user()
frappe.share.add('ToDo', todo.name, user, notify=1)
log_type = frappe.db.get_value('Notification Log', {'document_type': 'ToDo', 'document_name': todo.name}, 'type')
self.assertEqual(log_type, 'Share')
email = get_last_email_queue()
content = f'Subject: {frappe.utils.get_fullname(frappe.session.user)} shared a document ToDo'
self.assertTrue(content in email.message)
```

## Next Steps


---

*Source: test_notification_log.py:22 | Complexity: Advanced | Last updated: 2026-02-04*