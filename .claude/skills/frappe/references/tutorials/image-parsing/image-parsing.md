# How To: Image Parsing

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test image parsing

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

### Step 1: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 2: Call frappe.db.delete()

```python
frappe.db.delete('Communication', {'sender': 'sukh@yyy.com'})
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(re.search('<img[^>]*src=["\']/private/files/rtco1.png[^>]*>', communication.content))
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(re.search('<img[^>]*src=["\']/private/files/rtco2.png[^>]*>', communication.content))
```

### Step 5: Assign messages = value

```python
messages = {'"INBOX"': {'latest_messages': [raw.read()], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
```

### Step 6: Assign email_account = frappe.get_doc(...)

```python
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
```

### Step 7: Assign changed_flag = False

```python
changed_flag = False
```

### Step 8: Assign mails = TestEmailAccount.mocked_get_inbound_mails(...)

```python
mails = TestEmailAccount.mocked_get_inbound_mails(email_account, messages)
```

### Step 9: Assign communication = unknown.process(...)

```python
communication = mails[0].process()
```

### Step 10: Assign email_account.enable_incoming = False

```python
email_account.enable_incoming = False
```

### Step 11: Assign email_account.enable_incoming = True

```python
email_account.enable_incoming = True
```

### Step 12: Assign changed_flag = True

```python
changed_flag = True
```


## Complete Example

```python
# Workflow
import re
email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
frappe.db.delete('Communication', {'sender': 'sukh@yyy.com'})
with open(frappe.get_app_path('frappe', 'tests', 'data', 'email_with_image.txt')) as raw:
    messages = {'"INBOX"': {'latest_messages': [raw.read()], 'seen_status': {2: 'UNSEEN'}, 'uid_list': [2]}}
    email_account = frappe.get_doc('Email Account', '_Test Email Account 1')
    changed_flag = False
    if not email_account.enable_incoming:
        email_account.enable_incoming = True
        changed_flag = True
    mails = TestEmailAccount.mocked_get_inbound_mails(email_account, messages)
    if not mails:
        raise self.skipTest("No inbound mails found / Email Account wasn't patched properly")
    communication = mails[0].process()
self.assertTrue(re.search('<img[^>]*src=["\']/private/files/rtco1.png[^>]*>', communication.content))
self.assertTrue(re.search('<img[^>]*src=["\']/private/files/rtco2.png[^>]*>', communication.content))
if changed_flag:
    email_account.enable_incoming = False
```

## Next Steps


---

*Source: test_email.py:276 | Complexity: Advanced | Last updated: 2026-02-04*