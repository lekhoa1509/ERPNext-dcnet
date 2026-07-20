# How To: New And Save

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Check creating a new communication triggers a notification.

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

### Step 1: 'Check creating a new communication triggers a notification.'

```python
'Check creating a new communication triggers a notification.'
```

### Step 2: Assign communication = frappe.new_doc(...)

```python
communication = frappe.new_doc('Communication')
```

### Step 3: Assign communication.communication_type = 'Communication'

```python
communication.communication_type = 'Communication'
```

### Step 4: Assign communication.sender_full_name = '__test_notification_sender__'

```python
communication.sender_full_name = '__test_notification_sender__'
```

### Step 5: Assign communication.subject = 'test'

```python
communication.subject = 'test'
```

### Step 6: Assign communication.content = 'test'

```python
communication.content = 'test'
```

### Step 7: Call communication.insert()

```python
communication.insert(ignore_permissions=True)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Communication', 'reference_name': communication.name, 'status': 'Not Sent'}))
```

### Step 9: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue')
```

### Step 10: Call communication.reload()

```python
communication.reload()
```

### Step 11: Assign communication.content = 'test 2'

```python
communication.content = 'test 2'
```

### Step 12: Call communication.save()

```python
communication.save()
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Communication', 'reference_name': communication.name, 'status': 'Not Sent'}))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value('Communication', communication.name, 'subject'), '__testing__')
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
'Check creating a new communication triggers a notification.'
communication = frappe.new_doc('Communication')
communication.communication_type = 'Communication'
communication.sender_full_name = '__test_notification_sender__'
communication.subject = 'test'
communication.content = 'test'
communication.insert(ignore_permissions=True)
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Communication', 'reference_name': communication.name, 'status': 'Not Sent'}))
frappe.db.delete('Email Queue')
communication.reload()
communication.content = 'test 2'
communication.save()
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Communication', 'reference_name': communication.name, 'status': 'Not Sent'}))
self.assertEqual(frappe.db.get_value('Communication', communication.name, 'subject'), '__testing__')
```

## Next Steps


---

*Source: test_notification.py:104 | Complexity: Advanced | Last updated: 2026-02-04*