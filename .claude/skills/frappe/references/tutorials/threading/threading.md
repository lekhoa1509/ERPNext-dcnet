# How To: Threading

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test threading

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `email`
- `os`
- `unittest`
- `datetime`
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.communication.email`
- `frappe.desk.form.load`
- `frappe.email.doctype.email_account.email_account`
- `frappe.email.email_body`
- `frappe.email.receive`
- `frappe.tests`
- `frappe.email.receive`
- `frappe.email.receive`

**Setup Required:**
```python
frappe.flags.mute_emails = False
frappe.flags.sent_mail = None
frappe.db.delete('Email Queue')
frappe.db.delete('Unhandled Email')
```

## Step-by-Step Guide

### Step 1: Call cleanup()

```python
cleanup(['in', ['test_sender@example.com', 'test@example.com']])
```

### Step 2: Assign sent_name = value

```python
sent_name = make(subject='Test', content='test content', recipients='test_receiver@example.com', sender='test@example.com', doctype='ToDo', name=frappe.get_last_doc('ToDo').name, send_email=True)['name']
```

### Step 3: Assign sent_mail = email.message_from_string(...)

```python
sent_mail = email.message_from_string(frappe.get_last_doc('Email Queue').message)
```

### Step 4: Assign messages = value

```python
messages = {'"INBOX"': {'latest_messages': [raw], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
```

### Step 5: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 6: Call TestEmailAccount.mocked_email_receive()

```python
TestEmailAccount.mocked_email_receive(email_account, messages)
```

### Step 7: Assign sent = frappe.get_doc(...)

```python
sent = frappe.get_doc('Communication', sent_name)
```

### Step 8: Assign comm = frappe.get_doc(...)

```python
comm = frappe.get_doc('Communication', {'sender': 'test_sender@example.com'})
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(comm.reference_doctype, sent.reference_doctype)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(comm.reference_name, sent.reference_name)
```

### Step 11: Assign raw = f.read(...)

```python
raw = f.read()
```

### Step 12: Assign raw = raw.replace(...)

```python
raw = raw.replace('<-- in-reply-to -->', sent_mail.get('Message-Id'))
```


## Complete Example

```python
# Setup
frappe.flags.mute_emails = False
frappe.flags.sent_mail = None
frappe.db.delete('Email Queue')
frappe.db.delete('Unhandled Email')

# Workflow
cleanup(['in', ['test_sender@example.com', 'test@example.com']])
sent_name = make(subject='Test', content='test content', recipients='test_receiver@example.com', sender='test@example.com', doctype='ToDo', name=frappe.get_last_doc('ToDo').name, send_email=True)['name']
sent_mail = email.message_from_string(frappe.get_last_doc('Email Queue').message)
with open(os.path.join(os.path.dirname(__file__), 'test_mails', 'reply-1.raw')) as f:
    raw = f.read()
    raw = raw.replace('<-- in-reply-to -->', sent_mail.get('Message-Id'))
messages = {'"INBOX"': {'latest_messages': [raw], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
TestEmailAccount.mocked_email_receive(email_account, messages)
sent = frappe.get_doc('Communication', sent_name)
comm = frappe.get_doc('Communication', {'sender': 'test_sender@example.com'})
self.assertEqual(comm.reference_doctype, sent.reference_doctype)
self.assertEqual(comm.reference_name, sent.reference_name)
```

## Next Steps


---

*Source: test_email_account.py:214 | Complexity: Advanced | Last updated: 2026-02-04*