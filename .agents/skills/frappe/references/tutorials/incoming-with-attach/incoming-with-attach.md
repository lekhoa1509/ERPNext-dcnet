# How To: Incoming With Attach

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test incoming with attach

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
cleanup('test_sender@example.com')
```

### Step 2: Assign existing_file = frappe.get_doc(...)

```python
existing_file = frappe.get_doc({'doctype': 'File', 'file_name': 'erpnext-conf-14.png'})
```

### Step 3: Call frappe.delete_doc()

```python
frappe.delete_doc('File', existing_file.name)
```

### Step 4: Assign messages = value

```python
messages = {'"INBOX"': {'latest_messages': [self.get_test_mail('incoming-2.raw')], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
```

### Step 5: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 6: Call TestEmailAccount.mocked_email_receive()

```python
TestEmailAccount.mocked_email_receive(email_account, messages)
```

### Step 7: Assign comm = frappe.get_doc(...)

```python
comm = frappe.get_doc('Communication', {'sender': 'test_sender@example.com'})
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue('test_receiver@example.com' in comm.recipients)
```

### Step 9: Assign attachments = get_attachments(...)

```python
attachments = get_attachments(comm.doctype, comm.name)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue('erpnext-conf-14.png' in [f.file_name for f in attachments])
```

### Step 11: Assign existing_file = frappe.get_doc(...)

```python
existing_file = frappe.get_doc({'doctype': 'File', 'file_name': 'erpnext-conf-14.png'})
```

### Step 12: Call frappe.delete_doc()

```python
frappe.delete_doc('File', existing_file.name)
```


## Complete Example

```python
# Setup
frappe.flags.mute_emails = False
frappe.flags.sent_mail = None
frappe.db.delete('Email Queue')
frappe.db.delete('Unhandled Email')

# Workflow
cleanup('test_sender@example.com')
existing_file = frappe.get_doc({'doctype': 'File', 'file_name': 'erpnext-conf-14.png'})
frappe.delete_doc('File', existing_file.name)
messages = {'"INBOX"': {'latest_messages': [self.get_test_mail('incoming-2.raw')], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
TestEmailAccount.mocked_email_receive(email_account, messages)
comm = frappe.get_doc('Communication', {'sender': 'test_sender@example.com'})
self.assertTrue('test_receiver@example.com' in comm.recipients)
attachments = get_attachments(comm.doctype, comm.name)
self.assertTrue('erpnext-conf-14.png' in [f.file_name for f in attachments])
existing_file = frappe.get_doc({'doctype': 'File', 'file_name': 'erpnext-conf-14.png'})
frappe.delete_doc('File', existing_file.name)
```

## Next Steps


---

*Source: test_email_account.py:90 | Complexity: Advanced | Last updated: 2026-02-04*