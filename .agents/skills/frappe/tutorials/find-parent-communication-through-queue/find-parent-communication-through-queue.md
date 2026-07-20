# How To: Find Parent Communication Through Queue

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Find parent communication of an inbound mail.
Cases where parent communication does exist:
1. No parent communication is the mail is not a reply.

Cases where parent communication does not exist:
2. If mail is not a reply to system sent mail, then there can exist co

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

### Step 1: 'Find parent communication of an inbound mail.\n\t\tCases where parent communication does exist:\n\t\t1. No parent communication is the mail is not a reply.\n\n\t\tCases where parent communication does not exist:\n\t\t2. If mail is not a reply to system sent mail, then there can exist co\n\t\t'

```python
'Find parent communication of an inbound mail.\n\t\tCases where parent communication does exist:\n\t\t1. No parent communication is the mail is not a reply.\n\n\t\tCases where parent communication does not exist:\n\t\t2. If mail is not a reply to system sent mail, then there can exist co\n\t\t'
```

### Step 2: Assign communication = self.new_communication(...)

```python
communication = self.new_communication()
```

### Step 3: Assign queue_record = self.new_email_queue(...)

```python
queue_record = self.new_email_queue(communication=communication.name)
```

### Step 4: Assign mail_content = self.get_test_mail.replace(...)

```python
mail_content = self.get_test_mail(fname='reply-4.raw').replace('{{ message_id }}', queue_record.message_id)
```

### Step 5: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 6: Assign inbound_mail = InboundMail(...)

```python
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
```

### Step 7: Assign parent_communication = inbound_mail.parent_communication(...)

```python
parent_communication = inbound_mail.parent_communication()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(parent_communication.name, communication.name)
```


## Complete Example

```python
# Setup
cleanup()
frappe.db.delete('Email Queue')
frappe.db.delete('ToDo')

# Workflow
'Find parent communication of an inbound mail.\n\t\tCases where parent communication does exist:\n\t\t1. No parent communication is the mail is not a reply.\n\n\t\tCases where parent communication does not exist:\n\t\t2. If mail is not a reply to system sent mail, then there can exist co\n\t\t'
communication = self.new_communication()
queue_record = self.new_email_queue(communication=communication.name)
mail_content = self.get_test_mail(fname='reply-4.raw').replace('{{ message_id }}', queue_record.message_id)
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
parent_communication = inbound_mail.parent_communication()
self.assertEqual(parent_communication.name, communication.name)
```

## Next Steps


---

*Source: test_email_account.py:551 | Complexity: Advanced | Last updated: 2026-02-04*