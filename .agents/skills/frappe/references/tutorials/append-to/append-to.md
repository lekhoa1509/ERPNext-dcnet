# How To: Append To

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test append to

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

### Step 1: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 2: Assign mail_content = self.get_test_mail(...)

```python
mail_content = self.get_test_mail(fname='incoming-2.raw')
```

### Step 3: Assign inbound_mail = InboundMail(...)

```python
inbound_mail = InboundMail(mail_content, email_account, 12345, 1, 'ToDo')
```

### Step 4: Assign communication = inbound_mail.process(...)

```python
communication = inbound_mail.process()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(communication.reference_doctype, 'ToDo')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(communication.reference_name)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists(communication.reference_doctype, communication.reference_name))
```


## Complete Example

```python
# Setup
frappe.flags.mute_emails = False
frappe.flags.sent_mail = None
frappe.db.delete('Email Queue')
frappe.db.delete('Unhandled Email')

# Workflow
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
mail_content = self.get_test_mail(fname='incoming-2.raw')
inbound_mail = InboundMail(mail_content, email_account, 12345, 1, 'ToDo')
communication = inbound_mail.process()
self.assertEqual(communication.reference_doctype, 'ToDo')
self.assertTrue(communication.reference_name)
self.assertTrue(frappe.db.exists(communication.reference_doctype, communication.reference_name))
```

## Next Steps


---

*Source: test_email_account.py:381 | Complexity: Intermediate | Last updated: 2026-02-04*