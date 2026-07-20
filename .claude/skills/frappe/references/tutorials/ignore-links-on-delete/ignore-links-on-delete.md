# How To: Ignore Links On Delete

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test ignore links on delete

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.cache_manager`
- `frappe.desk.doctype.todo.todo`
- `frappe.tests`
- `frappe.tests.test_api`
- `frappe`
- `frappe`
- `os`
- `shutil`
- `frappe`
- `frappe.utils.fixtures`


## Step-by-Step Guide

### Step 1: Assign email_unsubscribe = frappe.get_doc.insert(...)

```python
email_unsubscribe = frappe.get_doc({'doctype': 'Email Unsubscribe', 'email': 'test@example.com', 'global_unsubscribe': 1}).insert()
```

### Step 2: Assign event = frappe.get_doc.insert(...)

```python
event = frappe.get_doc({'doctype': 'Event', 'subject': 'Test Event', 'starts_on': '2022-12-21', 'event_type': 'Public', 'event_participants': [{'reference_doctype': 'Email Unsubscribe', 'reference_docname': email_unsubscribe.name}]}).insert()
```

### Step 3: Call self.assertRaises()

```python
self.assertRaises(frappe.LinkExistsError, email_unsubscribe.delete)
```

### Step 4: Assign event.event_participants = value

```python
event.event_participants = []
```

### Step 5: Call event.save()

```python
event.save()
```

### Step 6: Assign todo = frappe.get_doc(...)

```python
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'Test ToDo', 'reference_type': 'Event', 'reference_name': event.name})
```

### Step 7: Call todo.insert()

```python
todo.insert()
```

### Step 8: Call event.delete()

```python
event.delete()
```


## Complete Example

```python
# Workflow
email_unsubscribe = frappe.get_doc({'doctype': 'Email Unsubscribe', 'email': 'test@example.com', 'global_unsubscribe': 1}).insert()
event = frappe.get_doc({'doctype': 'Event', 'subject': 'Test Event', 'starts_on': '2022-12-21', 'event_type': 'Public', 'event_participants': [{'reference_doctype': 'Email Unsubscribe', 'reference_docname': email_unsubscribe.name}]}).insert()
self.assertRaises(frappe.LinkExistsError, email_unsubscribe.delete)
event.event_participants = []
event.save()
todo = frappe.get_doc({'doctype': 'ToDo', 'description': 'Test ToDo', 'reference_type': 'Event', 'reference_name': event.name})
todo.insert()
event.delete()
```

## Next Steps


---

*Source: test_hooks.py:78 | Complexity: Advanced | Last updated: 2026-02-04*