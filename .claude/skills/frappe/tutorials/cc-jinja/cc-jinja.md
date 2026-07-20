# How To: Cc Jinja

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cc jinja

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `contextlib`
- `frappe`
- `frappe.utils`
- `frappe.utils.scheduler`
- `frappe.desk.form`
- `frappe.tests`
- `notification`
- `frappe.utils`
- `frappe.utils`

**Setup Required:**
```python
frappe.db.delete('Email Queue')
frappe.set_user('test@example.com')
if not frappe.db.exists('Notification', {'name': 'ToDo Status Update'}, 'name'):
    notification = frappe.new_doc('Notification')
    notification.name = 'ToDo Status Update'
    notification.subject = 'ToDo Status Update'
    notification.document_type = 'ToDo'
    notification.event = 'Value Change'
    notification.value_changed = 'status'
    notification.send_to_all_assignees = 1
    notification.set_property_after_alert = 'description'
    notification.property_value = 'Changed by Notification'
    notification.save()
if not frappe.db.exists('Notification', {'name': 'Contact Status Update'}, 'name'):
    notification = frappe.new_doc('Notification')
    notification.name = 'Contact Status Update'
    notification.subject = 'Contact Status Update'
    notification.document_type = 'Contact'
    notification.event = 'Value Change'
    notification.value_changed = 'status'
    notification.message = 'Test Contact Update'
    notification.append('recipients', {'receiver_by_document_field': 'email_id,email_ids'})
    notification.save()
```

## Step-by-Step Guide

### Step 1: Call frappe.db.delete()

```python
frappe.db.delete('User', {'email': 'test_jinja@example.com'})
```

### Step 2: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue')
```

### Step 3: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue Recipient')
```

### Step 4: Assign test_user = frappe.new_doc(...)

```python
test_user = frappe.new_doc('User')
```

### Step 5: Assign test_user.name = 'test_jinja'

```python
test_user.name = 'test_jinja'
```

### Step 6: Assign test_user.first_name = 'test_jinja'

```python
test_user.first_name = 'test_jinja'
```

### Step 7: Assign test_user.email = 'test_jinja@example.com'

```python
test_user.email = 'test_jinja@example.com'
```

### Step 8: Call test_user.insert()

```python
test_user.insert(ignore_permissions=True)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'User', 'reference_name': test_user.name, 'status': 'Not Sent'}))
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Email Queue Recipient', {'recipient': 'test_jinja@example.com'}))
```

### Step 11: Call frappe.db.delete()

```python
frappe.db.delete('User', {'email': 'test_jinja@example.com'})
```

### Step 12: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue')
```

### Step 13: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue Recipient')
```


## Complete Example

```python
# Setup
frappe.db.delete('Email Queue')
frappe.set_user('test@example.com')
if not frappe.db.exists('Notification', {'name': 'ToDo Status Update'}, 'name'):
    notification = frappe.new_doc('Notification')
    notification.name = 'ToDo Status Update'
    notification.subject = 'ToDo Status Update'
    notification.document_type = 'ToDo'
    notification.event = 'Value Change'
    notification.value_changed = 'status'
    notification.send_to_all_assignees = 1
    notification.set_property_after_alert = 'description'
    notification.property_value = 'Changed by Notification'
    notification.save()
if not frappe.db.exists('Notification', {'name': 'Contact Status Update'}, 'name'):
    notification = frappe.new_doc('Notification')
    notification.name = 'Contact Status Update'
    notification.subject = 'Contact Status Update'
    notification.document_type = 'Contact'
    notification.event = 'Value Change'
    notification.value_changed = 'status'
    notification.message = 'Test Contact Update'
    notification.append('recipients', {'receiver_by_document_field': 'email_id,email_ids'})
    notification.save()

# Workflow
frappe.db.delete('User', {'email': 'test_jinja@example.com'})
frappe.db.delete('Email Queue')
frappe.db.delete('Email Queue Recipient')
test_user = frappe.new_doc('User')
test_user.name = 'test_jinja'
test_user.first_name = 'test_jinja'
test_user.email = 'test_jinja@example.com'
test_user.insert(ignore_permissions=True)
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'User', 'reference_name': test_user.name, 'status': 'Not Sent'}))
self.assertTrue(frappe.db.get_value('Email Queue Recipient', {'recipient': 'test_jinja@example.com'}))
frappe.db.delete('User', {'email': 'test_jinja@example.com'})
frappe.db.delete('Email Queue')
frappe.db.delete('Email Queue Recipient')
```

## Next Steps


---

*Source: test_notification.py:399 | Complexity: Advanced | Last updated: 2026-02-04*