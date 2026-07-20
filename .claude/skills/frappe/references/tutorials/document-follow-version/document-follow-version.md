# How To: Document Follow Version

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test document follow version

## Prerequisites

**Required Modules:**
- `dataclasses`
- `frappe`
- `frappe.desk.form.document_follow`
- `frappe.desk.form.assign_to`
- `frappe.desk.form.document_follow`
- `frappe.desk.form.utils`
- `frappe.desk.like`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.share`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign user = get_user(...)

```python
user = get_user()
```

### Step 2: Assign event_doc = get_event(...)

```python
event_doc = get_event()
```

### Step 3: Assign event_doc.description = 'This is a test description for sending mail'

```python
event_doc.description = 'This is a test description for sending mail'
```

### Step 4: Call event_doc.save()

```python
event_doc.save(ignore_version=False)
```

### Step 5: Call document_follow.unfollow_document()

```python
document_follow.unfollow_document('Event', event_doc.name, user.name)
```

### Step 6: Assign doc = document_follow.follow_document(...)

```python
doc = document_follow.follow_document('Event', event_doc.name, user.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(doc.user, user.name)
```

### Step 8: Call document_follow.send_hourly_updates()

```python
document_follow.send_hourly_updates()
```

### Step 9: Assign emails = get_emails(...)

```python
emails = get_emails(event_doc, '%This is a test description for sending mail%')
```

### Step 10: Call self.assertIsNotNone()

```python
self.assertIsNotNone(emails)
```


## Complete Example

```python
# Workflow
user = get_user()
event_doc = get_event()
event_doc.description = 'This is a test description for sending mail'
event_doc.save(ignore_version=False)
document_follow.unfollow_document('Event', event_doc.name, user.name)
doc = document_follow.follow_document('Event', event_doc.name, user.name)
self.assertEqual(doc.user, user.name)
document_follow.send_hourly_updates()
emails = get_emails(event_doc, '%This is a test description for sending mail%')
self.assertIsNotNone(emails)
```

## Next Steps


---

*Source: test_document_follow.py:18 | Complexity: Advanced | Last updated: 2026-02-04*