# How To: Value Changed

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test value changed

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

### Step 4: Assign event.starts_on = '2014-06-06 12:00:00'

```python
event.starts_on = '2014-06-06 12:00:00'
```

### Step 5: Call event.insert()

```python
event.insert()
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 7: Assign event.subject = 'test 1'

```python
event.subject = 'test 1'
```

### Step 8: Call event.save()

```python
event.save()
```

### Step 9: Call self.assertFalse()

```python
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

### Step 10: Assign event.description = 'test'

```python
event.description = 'test'
```

### Step 11: Call event.save()

```python
event.save()
```

### Step 12: Call self.assertTrue()

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
event.starts_on = '2014-06-06 12:00:00'
event.insert()
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
event.subject = 'test 1'
event.save()
self.assertFalse(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
event.description = 'test'
event.save()
self.assertTrue(frappe.db.get_value('Email Queue', {'reference_doctype': 'Event', 'reference_name': event.name, 'status': 'Not Sent'}))
```

## Next Steps


---

*Source: test_notification.py:196 | Complexity: Advanced | Last updated: 2026-02-04*