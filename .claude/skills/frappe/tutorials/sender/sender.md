# How To: Sender

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test sender

## Prerequisites

**Required Modules:**
- `email`
- `re`
- `unittest.mock`
- `requests`
- `frappe`
- `frappe.core.doctype.communication.email`
- `frappe.desk.form.load`
- `frappe.email.doctype.email_account.test_email_account`
- `frappe.email.doctype.email_queue.email_queue`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.email.queue`
- `frappe.email.queue`
- `frappe.utils`
- `frappe.utils.verified_command`
- `frappe.email.queue`
- `re`
- `frappe.utils`
- `frappe.utils.verified_command`


## Step-by-Step Guide

### Step 1: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 2: Assign email_account.default_outgoing = 1

```python
email_account.default_outgoing = 1
```

### Step 3: Assign email_account.always_use_account_name_as_sender_name = 0

```python
email_account.always_use_account_name_as_sender_name = 0
```

### Step 4: Assign email_account.always_use_account_email_id_as_sender = 0

```python
email_account.always_use_account_email_id_as_sender = 0
```

### Step 5: Call _patched_assertion()

```python
_patched_assertion(email_account, 'admin@example.com')
```

### Step 6: Assign email_account.always_use_account_name_as_sender_name = 1

```python
email_account.always_use_account_name_as_sender_name = 1
```

### Step 7: Call _patched_assertion()

```python
_patched_assertion(email_account, '_Test Email Account 1 <admin@example.com>')
```

### Step 8: Assign email_account.always_use_account_name_as_sender_name = 0

```python
email_account.always_use_account_name_as_sender_name = 0
```

### Step 9: Assign email_account.always_use_account_email_id_as_sender = 1

```python
email_account.always_use_account_email_id_as_sender = 1
```

### Step 10: Call _patched_assertion()

```python
_patched_assertion(email_account, '"admin@example.com" <test@example.com>')
```

### Step 11: Assign email_account.always_use_account_name_as_sender_name = 1

```python
email_account.always_use_account_name_as_sender_name = 1
```

### Step 12: Call _patched_assertion()

```python
_patched_assertion(email_account, '_Test Email Account 1 <test@example.com>')
```

### Step 13: Call frappe.sendmail()

```python
frappe.sendmail(recipients=['test1@example.com'], sender='admin@example.com', subject='Test Email Queue', message='This mail is queued!', now=True)
```

### Step 14: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 15: Assign email_queue_sender = frappe.db.get_value(...)

```python
email_queue_sender = frappe.db.get_value('Email Queue', {'status': 'Sent'}, 'sender')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(email_queue_sender, assertion)
```


## Complete Example

```python
# Workflow
def _patched_assertion(email_account, assertion):
    with patch.object(QueueBuilder, 'get_outgoing_email_account', return_value=email_account):
        frappe.sendmail(recipients=['test1@example.com'], sender='admin@example.com', subject='Test Email Queue', message='This mail is queued!', now=True)
        frappe.db.commit()
        email_queue_sender = frappe.db.get_value('Email Queue', {'status': 'Sent'}, 'sender')
        self.assertEqual(email_queue_sender, assertion)
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
email_account.default_outgoing = 1
email_account.always_use_account_name_as_sender_name = 0
email_account.always_use_account_email_id_as_sender = 0
_patched_assertion(email_account, 'admin@example.com')
email_account.always_use_account_name_as_sender_name = 1
_patched_assertion(email_account, '_Test Email Account 1 <admin@example.com>')
email_account.always_use_account_name_as_sender_name = 0
email_account.always_use_account_email_id_as_sender = 1
_patched_assertion(email_account, '"admin@example.com" <test@example.com>')
email_account.always_use_account_name_as_sender_name = 1
_patched_assertion(email_account, '_Test Email Account 1 <test@example.com>')
```

## Next Steps


---

*Source: test_email.py:205 | Complexity: Advanced | Last updated: 2026-02-04*