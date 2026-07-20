# How To: Store Attachments

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: "attach print" feature just tells email queue which document to attach, this is not
actually stored unless system setting says so.

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

### Step 1: ' "attach print" feature just tells email queue which document to attach, this is not\n\t\tactually stored unless system setting says so.'

```python
' "attach print" feature just tells email queue which document to attach, this is not\n\t\tactually stored unless system setting says so.'
```

### Step 2: Assign name = make.get(...)

```python
name = make(sender='test_sender@example.com', recipients='test_recipient@example.com,test_recipient2@example.com', content='test mail 001', subject='test-mail-002', doctype='Email Account', name='_Test Email Account 1', print_format='Standard', send_email=True, now=True).get('name')
```

### Step 3: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 4: Assign communication = frappe.get_doc(...)

```python
communication = frappe.get_doc('Communication', name)
```

### Step 5: Assign attachments = get_attachments(...)

```python
attachments = get_attachments(communication.doctype, communication.name)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(attachments), 1)
```

### Step 7: Assign file = frappe.get_doc(...)

```python
file = frappe.get_doc('File', attachments[0].name)
```

### Step 8: Call self.assertGreater()

```python
self.assertGreater(file.file_size, 1000)
```

### Step 9: Call self.assertIn()

```python
self.assertIn('pdf', file.file_name.lower())
```

### Step 10: Assign sent_mails = self.get_last_sent_emails(...)

```python
sent_mails = self.get_last_sent_emails()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(sent_mails), 2)
```

### Step 12: Assign email_content = self.get_message(...)

```python
email_content = self.get_message(mail['id'])
```

### Step 13: Assign attachment_found = False

```python
attachment_found = False
```

### Step 14: Call self.fail()

```python
self.fail('Attachment not found', email_content)
```

### Step 15: Assign attachment_found = True

```python
attachment_found = True
```

### Step 16: Call self.assertIn()

```python
self.assertIn('pdf', child_part['name'])
```


## Complete Example

```python
# Workflow
' "attach print" feature just tells email queue which document to attach, this is not\n\t\tactually stored unless system setting says so.'
name = make(sender='test_sender@example.com', recipients='test_recipient@example.com,test_recipient2@example.com', content='test mail 001', subject='test-mail-002', doctype='Email Account', name='_Test Email Account 1', print_format='Standard', send_email=True, now=True).get('name')
frappe.db.commit()
communication = frappe.get_doc('Communication', name)
attachments = get_attachments(communication.doctype, communication.name)
self.assertEqual(len(attachments), 1)
file = frappe.get_doc('File', attachments[0].name)
self.assertGreater(file.file_size, 1000)
self.assertIn('pdf', file.file_name.lower())
sent_mails = self.get_last_sent_emails()
self.assertEqual(len(sent_mails), 2)
for mail in sent_mails:
    email_content = self.get_message(mail['id'])
    attachment_found = False
    for part in email_content['parts']:
        for child_part in part['childParts']:
            if child_part['isAttachment']:
                attachment_found = True
                self.assertIn('pdf', child_part['name'])
                break
    if not attachment_found:
        self.fail('Attachment not found', email_content)
```

## Next Steps


---

*Source: test_email.py:379 | Complexity: Advanced | Last updated: 2026-02-04*