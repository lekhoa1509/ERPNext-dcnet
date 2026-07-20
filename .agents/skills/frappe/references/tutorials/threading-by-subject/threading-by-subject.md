# How To: Threading By Subject

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test threading by subject

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

### Step 2: Assign messages = value

```python
messages = {'"INBOX"': {'latest_messages': test_mails, 'seen_status': {2: 'UNSEEN', 3: 'UNSEEN'}, 'uid_list': [2, 3]}}
```

### Step 3: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 4: Call TestEmailAccount.mocked_email_receive()

```python
TestEmailAccount.mocked_email_receive(email_account, messages)
```

### Step 5: Assign comm_list = frappe.get_all(...)

```python
comm_list = frappe.get_all('Communication', filters={'sender': 'test_sender@example.com'}, fields=['name', 'reference_doctype', 'reference_name'])
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(comm_list[0].reference_doctype, comm_list[1].reference_doctype)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(comm_list[0].reference_name, comm_list[1].reference_name)
```

### Step 8: Assign test_mails = value

```python
test_mails = [f.read()]
```

### Step 9: Call test_mails.append()

```python
test_mails.append(f.read())
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
with open(os.path.join(os.path.dirname(__file__), 'test_mails', 'reply-2.raw')) as f:
    test_mails = [f.read()]
with open(os.path.join(os.path.dirname(__file__), 'test_mails', 'reply-3.raw')) as f:
    test_mails.append(f.read())
messages = {'"INBOX"': {'latest_messages': test_mails, 'seen_status': {2: 'UNSEEN', 3: 'UNSEEN'}, 'uid_list': [2, 3]}}
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
TestEmailAccount.mocked_email_receive(email_account, messages)
comm_list = frappe.get_all('Communication', filters={'sender': 'test_sender@example.com'}, fields=['name', 'reference_doctype', 'reference_name'])
self.assertEqual(comm_list[0].reference_doctype, comm_list[1].reference_doctype)
self.assertEqual(comm_list[0].reference_name, comm_list[1].reference_name)
```

## Next Steps


---

*Source: test_email_account.py:249 | Complexity: Advanced | Last updated: 2026-02-04*