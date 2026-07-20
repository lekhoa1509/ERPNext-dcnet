# How To: Find Parent Communication For Self Reply

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: If the inbound email is a reply but not reply to system sent mail.

Ex: User replied to his/her mail.

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

### Step 1: 'If the inbound email is a reply but not reply to system sent mail.\n\n\t\tEx: User replied to his/her mail.\n\t\t'

```python
'If the inbound email is a reply but not reply to system sent mail.\n\n\t\tEx: User replied to his/her mail.\n\t\t'
```

### Step 2: Assign message_id = 'new-message-id'

```python
message_id = 'new-message-id'
```

### Step 3: Assign mail_content = self.get_test_mail.replace(...)

```python
mail_content = self.get_test_mail(fname='reply-4.raw').replace('{{ message_id }}', message_id)
```

### Step 4: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 5: Assign inbound_mail = InboundMail(...)

```python
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
```

### Step 6: Assign parent_communication = inbound_mail.parent_communication(...)

```python
parent_communication = inbound_mail.parent_communication()
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(parent_communication)
```

### Step 8: Assign communication = self.new_communication(...)

```python
communication = self.new_communication(message_id=message_id)
```

### Step 9: Assign inbound_mail = InboundMail(...)

```python
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
```

### Step 10: Assign parent_communication = inbound_mail.parent_communication(...)

```python
parent_communication = inbound_mail.parent_communication()
```

### Step 11: Call self.assertEqual()

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
'If the inbound email is a reply but not reply to system sent mail.\n\n\t\tEx: User replied to his/her mail.\n\t\t'
message_id = 'new-message-id'
mail_content = self.get_test_mail(fname='reply-4.raw').replace('{{ message_id }}', message_id)
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
parent_communication = inbound_mail.parent_communication()
self.assertFalse(parent_communication)
communication = self.new_communication(message_id=message_id)
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
parent_communication = inbound_mail.parent_communication()
self.assertEqual(parent_communication.name, communication.name)
```

## Next Steps


---

*Source: test_email_account.py:571 | Complexity: Advanced | Last updated: 2026-02-04*