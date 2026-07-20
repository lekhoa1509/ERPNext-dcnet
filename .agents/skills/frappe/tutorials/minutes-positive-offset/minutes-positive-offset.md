# How To: Minutes Positive Offset

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test minutes positive offset

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

### Step 1: Assign event = frappe.new_doc(...)

```python
event = frappe.new_doc('Event')
```

### Step 2: Assign event.subject = 'Test Minutes Positive Offset Event'

```python
event.subject = 'Test Minutes Positive Offset Event'
```

### Step 3: Assign event.event_type = 'Private'

```python
event.event_type = 'Private'
```

### Step 4: Assign event.starts_on = add_to_date(...)

```python
event.starts_on = add_to_date(now_datetime(), minutes=14)
```

### Step 5: Call event.insert()

```python
event.insert()
```

### Step 6: Assign notification = value

```python
notification = {'name': 'Test Minutes Positive Offset', 'subject': 'Test Minutes Positive Offset', 'document_type': 'Event', 'event': 'Minutes Before', 'datetime_changed': 'starts_on', 'minutes_offset': 15, 'message': 'Test message', 'channel': 'System Notification', 'recipients': [{'receiver_by_document_field': 'owner'}]}
```

### Step 7: Call frappe.db.delete()

```python
frappe.db.delete('Notification Log', {'subject': n.subject})
```

### Step 8: Call trigger_notifications()

```python
trigger_notifications(None, 'offset')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(1, frappe.db.count('Notification Log', {'subject': n.subject}))
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
from frappe.utils import add_to_date, now_datetime
event = frappe.new_doc('Event')
event.subject = 'Test Minutes Positive Offset Event'
event.event_type = 'Private'
event.starts_on = add_to_date(now_datetime(), minutes=14)
event.insert()
notification = {'name': 'Test Minutes Positive Offset', 'subject': 'Test Minutes Positive Offset', 'document_type': 'Event', 'event': 'Minutes Before', 'datetime_changed': 'starts_on', 'minutes_offset': 15, 'message': 'Test message', 'channel': 'System Notification', 'recipients': [{'receiver_by_document_field': 'owner'}]}
with get_test_notification(notification) as n:
    frappe.db.delete('Notification Log', {'subject': n.subject})
    trigger_notifications(None, 'offset')
    self.assertEqual(1, frappe.db.count('Notification Log', {'subject': n.subject}))
```

## Next Steps


---

*Source: test_notification.py:230 | Complexity: Advanced | Last updated: 2026-02-04*