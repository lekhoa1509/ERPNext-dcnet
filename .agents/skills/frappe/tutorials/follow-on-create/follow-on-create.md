# How To: Follow On Create

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test follow on create

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
user = get_user(DocumentFollowConditions(1))
```

### Step 2: Call frappe.set_user()

```python
frappe.set_user(user.name)
```

### Step 3: Assign event = get_event(...)

```python
event = get_event()
```

### Step 4: Assign event.description = 'This is a test description for sending mail'

```python
event.description = 'This is a test description for sending mail'
```

### Step 5: Call event.save()

```python
event.save(ignore_version=False)
```

### Step 6: Assign documents_followed = get_events_followed_by_user(...)

```python
documents_followed = get_events_followed_by_user(event.name, user.name)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(documents_followed)
```


## Complete Example

```python
# Workflow
user = get_user(DocumentFollowConditions(1))
frappe.set_user(user.name)
event = get_event()
event.description = 'This is a test description for sending mail'
event.save(ignore_version=False)
documents_followed = get_events_followed_by_user(event.name, user.name)
self.assertTrue(documents_followed)
```

## Next Steps


---

*Source: test_document_follow.py:58 | Complexity: Intermediate | Last updated: 2026-02-04*