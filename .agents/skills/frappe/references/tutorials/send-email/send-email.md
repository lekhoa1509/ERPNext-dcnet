# How To: Send Email

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test send email

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

### Step 1: Assign sender = 'a@example.io'

```python
sender = 'a@example.io'
```

### Step 2: Assign recipients = 'b@example.io,c@example.io'

```python
recipients = 'b@example.io,c@example.io'
```

### Step 3: Assign subject = 'checking if email works'

```python
subject = 'checking if email works'
```

### Step 4: Assign content = 'is email working?'

```python
content = 'is email working?'
```

### Step 5: Assign email = frappe.sendmail(...)

```python
email = frappe.sendmail(sender=sender, recipients=recipients, subject=subject, content=content, now=True)
```

### Step 6: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 7: Call email.reload()

```python
email.reload()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(email.sender, sender)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(email.recipients), 2)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(email.status, 'Sent')
```

### Step 11: Assign sent_mails = self.get_last_sent_emails(...)

```python
sent_mails = self.get_last_sent_emails()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(sent_mails), 2)
```

### Step 13: Call self.assertSetEqual()

```python
self.assertSetEqual(set(recipients.split(',')), {m['to'][0] for m in sent_mails})
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(sent_mail['from'], sender)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sent_mail['subject'], subject)
```


## Complete Example

```python
# Workflow
sender = 'a@example.io'
recipients = 'b@example.io,c@example.io'
subject = 'checking if email works'
content = 'is email working?'
email = frappe.sendmail(sender=sender, recipients=recipients, subject=subject, content=content, now=True)
frappe.db.commit()
email.reload()
self.assertEqual(email.sender, sender)
self.assertEqual(len(email.recipients), 2)
self.assertEqual(email.status, 'Sent')
sent_mails = self.get_last_sent_emails()
self.assertEqual(len(sent_mails), 2)
for sent_mail in sent_mails:
    self.assertEqual(sent_mail['from'], sender)
    self.assertEqual(sent_mail['subject'], subject)
self.assertSetEqual(set(recipients.split(',')), {m['to'][0] for m in sent_mails})
```

## Next Steps


---

*Source: test_email.py:355 | Complexity: Advanced | Last updated: 2026-02-04*