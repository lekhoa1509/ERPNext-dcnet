# How To: Alert Disabled On Wrong Field

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test alert disabled on wrong field

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

### Step 1: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 2: Assign notification = frappe.get_doc.insert(...)

```python
notification = frappe.get_doc({'doctype': 'Notification', 'subject': '_Test Notification for wrong field', 'document_type': 'Event', 'event': 'Value Change', 'attach_print': 0, 'value_changed': 'description1', 'message': 'Description changed', 'recipients': [{'receiver_by_document_field': 'owner'}]}).insert()
```

### Step 3: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 4: Assign event = frappe.new_doc(...)

```python
event = frappe.new_doc('Event')
```

### Step 5: Assign event.subject = 'test-2'

```python
event.subject = 'test-2'
```

### Step 6: Assign event.event_type = 'Private'

```python
event.event_type = 'Private'
```

### Step 7: Assign event.starts_on = '2014-06-06 12:00:00'

```python
event.starts_on = '2014-06-06 12:00:00'
```

### Step 8: Call event.insert()

```python
event.insert()
```

### Step 9: Assign event.subject = 'test 1'

```python
event.subject = 'test 1'
```

### Step 10: Call event.save()

```python
event.save()
```

### Step 11: Call notification.reload()

```python
notification.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(notification.enabled, 0)
```

### Step 13: Call notification.delete()

```python
notification.delete()
```

### Step 14: Call event.delete()

```python
event.delete()
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
frappe.set_user('Administrator')
notification = frappe.get_doc({'doctype': 'Notification', 'subject': '_Test Notification for wrong field', 'document_type': 'Event', 'event': 'Value Change', 'attach_print': 0, 'value_changed': 'description1', 'message': 'Description changed', 'recipients': [{'receiver_by_document_field': 'owner'}]}).insert()
frappe.db.commit()
event = frappe.new_doc('Event')
event.subject = 'test-2'
event.event_type = 'Private'
event.starts_on = '2014-06-06 12:00:00'
event.insert()
event.subject = 'test 1'
event.save()
notification.reload()
self.assertEqual(notification.enabled, 0)
notification.delete()
event.delete()
```

## Next Steps


---

*Source: test_notification.py:316 | Complexity: Advanced | Last updated: 2026-02-04*