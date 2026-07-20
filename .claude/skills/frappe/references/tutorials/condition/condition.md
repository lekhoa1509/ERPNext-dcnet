# How To: Condition

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Check notification is triggered based on a condition.

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

### Step 1: 'Check notification is triggered based on a condition.'

```python
'Check notification is triggered based on a condition.'
```

### Step 2: Assign event = frappe.new_doc(...)

```python
event = frappe.new_doc('Event')
```

### Step 3: Assign event.subject = 'test'

```python
event.subject = 'test'
```

### Step 4: Assign event.event_type = 'Private'

```python
event.event_type = 'Private'
```

### Step 5: Assign event.starts_on = '2014-06-06 12:00:00'

```python
event.starts_on = '2014-06-06 12:00:00'
```

### Step 6: Call event.insert()

```python
event.insert()
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 8: Assign event.event_type = 'Public'

```python
event.event_type = 'Public'
```

### Step 9: Call event.save()

```python
event.save()
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Communication', {'reference_doctype': 'Event', 'reference_name': event.name, 'communication_type': 'Automated Message'}))
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
'Check notification is triggered based on a condition.'
event = frappe.new_doc('Event')
event.subject = 'test'
event.event_type = 'Private'
event.starts_on = '2014-06-06 12:00:00'
event.insert()
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
event.event_type = 'Public'
event.save()
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
self.assertTrue(frappe.db.get_value('Communication', {'reference_doctype': 'Event', 'reference_name': event.name, 'communication_type': 'Automated Message'}))
```

## Next Steps


---

*Source: test_notification.py:142 | Complexity: Advanced | Last updated: 2026-02-04*