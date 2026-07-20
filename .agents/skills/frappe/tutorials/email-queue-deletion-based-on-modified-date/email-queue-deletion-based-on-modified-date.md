# How To: Email Queue Deletion Based On Modified Date

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test email queue deletion based on modified date

## Prerequisites

**Required Modules:**
- `textwrap`
- `frappe`
- `frappe.email.doctype.email_queue.email_queue`
- `frappe.tests`
- `frappe.email.doctype.email_queue.email_queue`


## Step-by-Step Guide

### Step 1: Assign old_record = frappe.get_doc.insert(...)

```python
old_record = frappe.get_doc({'doctype': 'Email Queue', 'sender': 'Test <test@example.com>', 'show_as_cc': '', 'message': 'Test message', 'status': 'Sent', 'priority': 1, 'recipients': [{'recipient': 'test_auth@test.com'}]}).insert()
```

### Step 2: Assign old_record.creation = '2010-01-01 00:00:01'

```python
old_record.creation = '2010-01-01 00:00:01'
```

### Step 3: Assign unknown.creation = value

```python
old_record.recipients[0].creation = old_record.creation
```

### Step 4: Call old_record.db_update_all()

```python
old_record.db_update_all()
```

### Step 5: Assign new_record = frappe.copy_doc(...)

```python
new_record = frappe.copy_doc(old_record)
```

### Step 6: Call new_record.insert()

```python
new_record.insert()
```

### Step 7: Call EmailQueue.clear_old_logs()

```python
EmailQueue.clear_old_logs()
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Email Queue', old_record.name))
```

### Step 9: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Email Queue Recipient', {'parent': old_record.name}))
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Email Queue', new_record.name))
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Email Queue Recipient', {'parent': new_record.name}))
```


## Complete Example

```python
# Workflow
from frappe.email.doctype.email_queue.email_queue import EmailQueue
old_record = frappe.get_doc({'doctype': 'Email Queue', 'sender': 'Test <test@example.com>', 'show_as_cc': '', 'message': 'Test message', 'status': 'Sent', 'priority': 1, 'recipients': [{'recipient': 'test_auth@test.com'}]}).insert()
old_record.creation = '2010-01-01 00:00:01'
old_record.recipients[0].creation = old_record.creation
old_record.db_update_all()
new_record = frappe.copy_doc(old_record)
new_record.insert()
EmailQueue.clear_old_logs()
self.assertFalse(frappe.db.exists('Email Queue', old_record.name))
self.assertFalse(frappe.db.exists('Email Queue Recipient', {'parent': old_record.name}))
self.assertTrue(frappe.db.exists('Email Queue', new_record.name))
self.assertTrue(frappe.db.exists('Email Queue Recipient', {'parent': new_record.name}))
```

## Next Steps


---

*Source: test_email_queue.py:11 | Complexity: Advanced | Last updated: 2026-02-04*