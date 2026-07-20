# How To: Mail Exist Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Do not create communication record if the mail is already downloaded into the system.

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
cleanup()
frappe.db.delete('Email Queue')
frappe.db.delete('ToDo')
```

## Step-by-Step Guide

### Step 1: 'Do not create communication record if the mail is already downloaded into the system.'

```python
'Do not create communication record if the mail is already downloaded into the system.'
```

### Step 2: Assign mail_content = self.get_test_mail(...)

```python
mail_content = self.get_test_mail(fname='incoming-1.raw')
```

### Step 3: Assign message_id = value

```python
message_id = Email(mail_content).message_id
```

### Step 4: Assign communication = self.new_communication(...)

```python
communication = self.new_communication(message_id=message_id, sent_or_received='Received')
```

### Step 5: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 6: Assign inbound_mail = InboundMail(...)

```python
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
```

### Step 7: Assign new_communication = inbound_mail.process(...)

```python
new_communication = inbound_mail.process()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(new_communication.uid, 12345)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(communication.name, new_communication.name)
```


## Complete Example

```python
# Setup
cleanup()
frappe.db.delete('Email Queue')
frappe.db.delete('ToDo')

# Workflow
'Do not create communication record if the mail is already downloaded into the system.'
mail_content = self.get_test_mail(fname='incoming-1.raw')
message_id = Email(mail_content).message_id
communication = self.new_communication(message_id=message_id, sent_or_received='Received')
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
new_communication = inbound_mail.process()
self.assertEqual(new_communication.uid, 12345)
self.assertEqual(communication.name, new_communication.name)
```

## Next Steps


---

*Source: test_email_account.py:522 | Complexity: Advanced | Last updated: 2026-02-04*