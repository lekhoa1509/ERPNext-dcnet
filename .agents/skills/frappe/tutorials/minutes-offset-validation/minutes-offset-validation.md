# How To: Minutes Offset Validation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test minutes offset validation

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

### Step 1: Assign notification = frappe.new_doc(...)

```python
notification = frappe.new_doc('Notification')
```

### Step 2: Assign notification.name = 'Test Minutes Offset Validation'

```python
notification.name = 'Test Minutes Offset Validation'
```

### Step 3: Assign notification.subject = 'Test Minutes Offset Validation'

```python
notification.subject = 'Test Minutes Offset Validation'
```

### Step 4: Assign notification.document_type = 'Event'

```python
notification.document_type = 'Event'
```

### Step 5: Assign notification.event = 'Minutes Before'

```python
notification.event = 'Minutes Before'
```

### Step 6: Assign notification.datetime_changed = 'starts_on'

```python
notification.datetime_changed = 'starts_on'
```

### Step 7: Assign notification.message = 'Test message'

```python
notification.message = 'Test message'
```

### Step 8: Assign notification.minutes_offset = value

```python
notification.minutes_offset = -5
```

### Step 9: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, notification.insert)
```

### Step 10: Assign notification.minutes_offset = 0

```python
notification.minutes_offset = 0
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, notification.insert)
```

### Step 12: Assign notification.minutes_offset = 5

```python
notification.minutes_offset = 5
```

### Step 13: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, notification.insert)
```

### Step 14: Assign notification.minutes_offset = 15

```python
notification.minutes_offset = 15
```

### Step 15: Call notification.insert()

```python
notification.insert()
```

### Step 16: Call notification.delete()

```python
notification.delete()
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
notification = frappe.new_doc('Notification')
notification.name = 'Test Minutes Offset Validation'
notification.subject = 'Test Minutes Offset Validation'
notification.document_type = 'Event'
notification.event = 'Minutes Before'
notification.datetime_changed = 'starts_on'
notification.message = 'Test message'
notification.minutes_offset = -5
self.assertRaises(frappe.ValidationError, notification.insert)
notification.minutes_offset = 0
self.assertRaises(frappe.ValidationError, notification.insert)
notification.minutes_offset = 5
self.assertRaises(frappe.ValidationError, notification.insert)
notification.minutes_offset = 15
notification.insert()
notification.delete()
```

## Next Steps


---

*Source: test_notification.py:290 | Complexity: Advanced | Last updated: 2026-02-04*