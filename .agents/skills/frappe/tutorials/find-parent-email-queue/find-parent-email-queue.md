# How To: Find Parent Email Queue

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: If the mail is reply to the already sent mail, there will be a email queue record.

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

### Step 1: 'If the mail is reply to the already sent mail, there will be a email queue record.'

```python
'If the mail is reply to the already sent mail, there will be a email queue record.'
```

### Step 2: Assign queue_record = self.new_email_queue(...)

```python
queue_record = self.new_email_queue()
```

### Step 3: Assign mail_content = self.get_test_mail.replace(...)

```python
mail_content = self.get_test_mail(fname='reply-4.raw').replace('{{ message_id }}', queue_record.message_id)
```

### Step 4: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 5: Assign inbound_mail = InboundMail(...)

```python
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
```

### Step 6: Assign parent_queue = inbound_mail.parent_email_queue(...)

```python
parent_queue = inbound_mail.parent_email_queue()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(queue_record.name, parent_queue.name)
```


## Complete Example

```python
# Setup
cleanup()
frappe.db.delete('Email Queue')
frappe.db.delete('ToDo')

# Workflow
'If the mail is reply to the already sent mail, there will be a email queue record.'
queue_record = self.new_email_queue()
mail_content = self.get_test_mail(fname='reply-4.raw').replace('{{ message_id }}', queue_record.message_id)
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
inbound_mail = InboundMail(mail_content, email_account, 12345, 1)
parent_queue = inbound_mail.parent_email_queue()
self.assertEqual(queue_record.name, parent_queue.name)
```

## Next Steps


---

*Source: test_email_account.py:537 | Complexity: Intermediate | Last updated: 2026-02-04*