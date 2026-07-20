# How To: Threading By Message Id

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test threading by message id

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
cleanup()
```

### Step 2: Call frappe.db.delete()

```python
frappe.db.delete('Email Queue')
```

### Step 3: Assign event = frappe.get_doc.insert(...)

```python
event = frappe.get_doc(doctype='Event', subject='test-message').insert()
```

### Step 4: Call frappe.sendmail()

```python
frappe.sendmail(recipients='test@example.com', subject='test message for threading', message='testing', reference_doctype=event.doctype, reference_name=event.name)
```

### Step 5: Assign last_mail = frappe.get_doc(...)

```python
last_mail = frappe.get_doc('Email Queue', dict(reference_name=event.name))
```

### Step 6: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 7: Call TestEmailAccount.mocked_email_receive()

```python
TestEmailAccount.mocked_email_receive(email_account, messages)
```

### Step 8: Assign comm_list = frappe.get_all(...)

```python
comm_list = frappe.get_all('Communication', filters={'sender': 'test_sender@example.com'}, fields=['name', 'reference_doctype', 'reference_name'])
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(comm_list[0].reference_doctype, event.doctype)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(comm_list[0].reference_name, event.name)
```

### Step 11: Assign messages = value

```python
messages = {'"INBOX"': {'latest_messages': [f.read().replace('{{ message_id }}', '<' + last_mail.message_id + '>')], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
```


## Complete Example

```python
# Setup
frappe.flags.mute_emails = False
frappe.flags.sent_mail = None
frappe.db.delete('Email Queue')
frappe.db.delete('Unhandled Email')

# Workflow
cleanup()
frappe.db.delete('Email Queue')
event = frappe.get_doc(doctype='Event', subject='test-message').insert()
frappe.sendmail(recipients='test@example.com', subject='test message for threading', message='testing', reference_doctype=event.doctype, reference_name=event.name)
last_mail = frappe.get_doc('Email Queue', dict(reference_name=event.name))
with open(os.path.join(os.path.dirname(__file__), 'test_mails', 'reply-4.raw')) as f:
    messages = {'"INBOX"': {'latest_messages': [f.read().replace('{{ message_id }}', '<' + last_mail.message_id + '>')], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
TestEmailAccount.mocked_email_receive(email_account, messages)
comm_list = frappe.get_all('Communication', filters={'sender': 'test_sender@example.com'}, fields=['name', 'reference_doctype', 'reference_name'])
self.assertEqual(comm_list[0].reference_doctype, event.doctype)
self.assertEqual(comm_list[0].reference_name, event.name)
```

## Next Steps


---

*Source: test_email_account.py:280 | Complexity: Advanced | Last updated: 2026-02-04*