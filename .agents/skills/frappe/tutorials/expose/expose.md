# How To: Expose

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test expose

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

### Step 1: Call frappe.sendmail()

```python
frappe.sendmail(recipients=['test@example.com'], cc=['test1@example.com'], sender='admin@example.com', reference_doctype='User', reference_name='Administrator', subject='Testing Email Queue', message='This is mail is queued!', unsubscribe_message='Unsubscribe', now=True)
```

### Step 2: Call frappe.db.commit()

```python
frappe.db.commit()
```

### Step 3: Assign email_queue = frappe.db.sql(...)

```python
email_queue = frappe.db.sql("select name from `tabEmail Queue` where status='Sent'", as_dict=1)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(len(email_queue), 1)
```

### Step 5: Assign queue_recipients = value

```python
queue_recipients = [r.recipient for r in frappe.db.sql("select recipient from `tabEmail Queue Recipient`\n\t\t\twhere status='Sent'", as_dict=1)]
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue('test@example.com' in queue_recipients)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue('test1@example.com' in queue_recipients)
```

### Step 8: Assign message = value

```python
message = frappe.db.sql("select message from `tabEmail Queue`\n\t\t\twhere status='Sent'", as_dict=1)[0].message
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue('<!--recipient-->' in message)
```

### Step 10: Assign email_obj = email.message_from_string(...)

```python
email_obj = email.message_from_string(frappe.safe_decode(frappe.flags.sent_mail))
```

### Step 11: Assign content = part.get_payload(...)

```python
content = part.get_payload(decode=True)
```

### Step 12: Assign eol = '\r\n'

```python
eol = '\r\n'
```

### Step 13: Assign query_string = re.search.group(...)

```python
query_string = re.search('(?<=/api/method/frappe.email.queue.unsubscribe\\?).*(?=' + eol + ')', content.decode()).group(0)
```

### Step 14: Call set_request()

```python
set_request(method='GET', query_string=query_string)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(verify_request())
```


## Complete Example

```python
# Workflow
from frappe.utils import set_request
from frappe.utils.verified_command import verify_request
frappe.sendmail(recipients=['test@example.com'], cc=['test1@example.com'], sender='admin@example.com', reference_doctype='User', reference_name='Administrator', subject='Testing Email Queue', message='This is mail is queued!', unsubscribe_message='Unsubscribe', now=True)
frappe.db.commit()
email_queue = frappe.db.sql("select name from `tabEmail Queue` where status='Sent'", as_dict=1)
self.assertEqual(len(email_queue), 1)
queue_recipients = [r.recipient for r in frappe.db.sql("select recipient from `tabEmail Queue Recipient`\n\t\t\twhere status='Sent'", as_dict=1)]
self.assertTrue('test@example.com' in queue_recipients)
self.assertTrue('test1@example.com' in queue_recipients)
message = frappe.db.sql("select message from `tabEmail Queue`\n\t\t\twhere status='Sent'", as_dict=1)[0].message
self.assertTrue('<!--recipient-->' in message)
email_obj = email.message_from_string(frappe.safe_decode(frappe.flags.sent_mail))
for part in email_obj.walk():
    content = part.get_payload(decode=True)
    if content:
        eol = '\r\n'
        query_string = re.search('(?<=/api/method/frappe.email.queue.unsubscribe\\?).*(?=' + eol + ')', content.decode()).group(0)
        set_request(method='GET', query_string=query_string)
        self.assertTrue(verify_request())
        break
```

## Next Steps


---

*Source: test_email.py:154 | Complexity: Advanced | Last updated: 2026-02-04*