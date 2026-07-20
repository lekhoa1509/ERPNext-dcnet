# How To: Append To With Imap Folders

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, mock, workflow, integration

## Overview

Workflow: test append to with imap folders

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

### Step 1: Assign mail_content_1 = self.get_test_mail(...)

```python
mail_content_1 = self.get_test_mail(fname='incoming-1.raw')
```

### Step 2: Assign mail_content_2 = self.get_test_mail(...)

```python
mail_content_2 = self.get_test_mail(fname='incoming-2.raw')
```

### Step 3: Assign mail_content_3 = self.get_test_mail(...)

```python
mail_content_3 = self.get_test_mail(fname='incoming-3.raw')
```

### Step 4: Assign messages = value

```python
messages = {'"INBOX"': {'latest_messages': [mail_content_1, mail_content_2], 'seen_status': {0: 'UNSEEN', 1: 'UNSEEN'}, 'uid_list': [0, 1]}, '"Test Folder"': {'latest_messages': [mail_content_3], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
```

### Step 5: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 6: Assign mails = TestEmailAccount.mocked_get_inbound_mails(...)

```python
mails = TestEmailAccount.mocked_get_inbound_mails(email_account, messages)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(mails), 3)
```

### Step 8: Assign inbox_mails = 0

```python
inbox_mails = 0
```

### Step 9: Assign test_folder_mails = 0

```python
test_folder_mails = 0
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(inbox_mails, 2)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(test_folder_mails, 1)
```

### Step 12: Assign communication = mail.process(...)

```python
communication = mail.process()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(communication.reference_doctype, 'ToDo')
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(communication.reference_name)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists(communication.reference_doctype, communication.reference_name))
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(communication.reference_doctype, None)
```


## Complete Example

```python
# Setup
frappe.flags.mute_emails = False
frappe.flags.sent_mail = None
frappe.db.delete('Email Queue')
frappe.db.delete('Unhandled Email')

# Workflow
mail_content_1 = self.get_test_mail(fname='incoming-1.raw')
mail_content_2 = self.get_test_mail(fname='incoming-2.raw')
mail_content_3 = self.get_test_mail(fname='incoming-3.raw')
messages = {'"INBOX"': {'latest_messages': [mail_content_1, mail_content_2], 'seen_status': {0: 'UNSEEN', 1: 'UNSEEN'}, 'uid_list': [0, 1]}, '"Test Folder"': {'latest_messages': [mail_content_3], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
mails = TestEmailAccount.mocked_get_inbound_mails(email_account, messages)
self.assertEqual(len(mails), 3)
inbox_mails = 0
test_folder_mails = 0
for mail in mails:
    communication = mail.process()
    if mail.append_to == 'ToDo':
        inbox_mails += 1
        self.assertEqual(communication.reference_doctype, 'ToDo')
        self.assertTrue(communication.reference_name)
        self.assertTrue(frappe.db.exists(communication.reference_doctype, communication.reference_name))
    else:
        test_folder_mails += 1
        self.assertEqual(communication.reference_doctype, None)
self.assertEqual(inbox_mails, 2)
self.assertEqual(test_folder_mails, 1)
```

## Next Steps


---

*Source: test_email_account.py:393 | Complexity: Advanced | Last updated: 2026-02-04*