# How To: Invalid Condition

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test invalid condition

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

### Step 2: Assign notification = frappe.new_doc(...)

```python
notification = frappe.new_doc('Notification')
```

### Step 3: Assign notification.subject = 'test'

```python
notification.subject = 'test'
```

### Step 4: Assign notification.document_type = 'ToDo'

```python
notification.document_type = 'ToDo'
```

### Step 5: Assign notification.send_alert_on = 'New'

```python
notification.send_alert_on = 'New'
```

### Step 6: Assign notification.message = 'test'

```python
notification.message = 'test'
```

### Step 7: Assign recipent = frappe.new_doc(...)

```python
recipent = frappe.new_doc('Notification Recipient')
```

### Step 8: Assign recipent.receiver_by_document_field = 'owner'

```python
recipent.receiver_by_document_field = 'owner'
```

### Step 9: Assign notification.recipents = recipent

```python
notification.recipents = recipent
```

### Step 10: Assign notification.condition = 'test'

```python
notification.condition = 'test'
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, notification.save)
```

### Step 12: Call notification.delete()

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
frappe.set_user('Administrator')
notification = frappe.new_doc('Notification')
notification.subject = 'test'
notification.document_type = 'ToDo'
notification.send_alert_on = 'New'
notification.message = 'test'
recipent = frappe.new_doc('Notification Recipient')
recipent.receiver_by_document_field = 'owner'
notification.recipents = recipent
notification.condition = 'test'
self.assertRaises(frappe.ValidationError, notification.save)
notification.delete()
```

## Next Steps


---

*Source: test_notification.py:179 | Complexity: Advanced | Last updated: 2026-02-04*