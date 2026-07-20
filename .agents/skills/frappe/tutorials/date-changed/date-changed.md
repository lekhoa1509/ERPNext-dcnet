# How To: Date Changed

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test date changed

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

### Step 2: Assign event.subject = 'test'

```python
event.subject = 'test'
```

### Step 3: Assign event.event_type = 'Private'

```python
event.event_type = 'Private'
```

### Step 4: Assign event.starts_on = '2014-01-01 12:00:00'

```python
event.starts_on = '2014-01-01 12:00:00'
```

### Step 5: Call event.insert()

```python
event.insert()
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 7: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 8: Call frappe.get_doc.execute()

```python
frappe.get_doc('Scheduled Job Type', dict(method='frappe.email.doctype.notification.notification.trigger_daily_alerts')).execute()
```

### Step 9: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 10: Assign event.starts_on = value

```python
event.starts_on = frappe.utils.add_days(frappe.utils.nowdate(), 2) + ' 12:00:00'
```

### Step 11: Call event.save()

```python
event.save()
```

### Step 12: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 13: Call frappe.get_doc.execute()

```python
frappe.get_doc('Scheduled Job Type', dict(method='frappe.email.doctype.notification.notification.trigger_daily_alerts')).execute()
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
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
event = frappe.new_doc('Event')
event.subject = 'test'
event.event_type = 'Private'
event.starts_on = '2014-01-01 12:00:00'
event.insert()
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
frappe.set_user('Administrator')
frappe.get_doc('Scheduled Job Type', dict(method='frappe.email.doctype.notification.notification.trigger_daily_alerts')).execute()
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
event.starts_on = frappe.utils.add_days(frappe.utils.nowdate(), 2) + ' 12:00:00'
event.save()
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
frappe.get_doc('Scheduled Job Type', dict(method='frappe.email.doctype.notification.notification.trigger_daily_alerts')).execute()
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

## Next Steps


---

*Source: test_notification.py:346 | Complexity: Advanced | Last updated: 2026-02-04*