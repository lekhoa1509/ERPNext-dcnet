# How To: Prepare Message Returns Already Encoded String

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test prepare message returns already encoded string

## Prerequisites

**Required Modules:**
- `base64`
- `os`
- `frappe`
- `frappe`
- `frappe.core.doctype.communication.communication`
- `frappe.email.doctype.email_queue.email_queue`
- `frappe.email.email_body`
- `frappe.email.receive`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign uni_chr1 = chr(...)

```python
uni_chr1 = chr(40960)
```

### Step 2: Assign uni_chr2 = chr(...)

```python
uni_chr2 = chr(1972)
```

### Step 3: Call QueueBuilder.process()

```python
QueueBuilder(recipients=['test@example.com'], sender='me@example.com', subject='Test Subject', message=f'<h1>{uni_chr1}abcd{uni_chr2}</h1>', text_content='whatever').process()
```

### Step 4: Assign queue_doc = frappe.get_last_doc(...)

```python
queue_doc = frappe.get_last_doc('Email Queue')
```

### Step 5: Assign mail_ctx = SendMailContext(...)

```python
mail_ctx = SendMailContext(queue_doc=queue_doc)
```

### Step 6: Assign result = mail_ctx.build_message(...)

```python
result = mail_ctx.build_message(recipient_email='test@test.com')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(b'<h1>=EA=80=80abcd=DE=B4</h1>' in result)
```


## Complete Example

```python
# Workflow
uni_chr1 = chr(40960)
uni_chr2 = chr(1972)
QueueBuilder(recipients=['test@example.com'], sender='me@example.com', subject='Test Subject', message=f'<h1>{uni_chr1}abcd{uni_chr2}</h1>', text_content='whatever').process()
queue_doc = frappe.get_last_doc('Email Queue')
mail_ctx = SendMailContext(queue_doc=queue_doc)
result = mail_ctx.build_message(recipient_email='test@test.com')
self.assertTrue(b'<h1>=EA=80=80abcd=DE=B4</h1>' in result)
```

## Next Steps


---

*Source: test_email_body.py:55 | Complexity: Intermediate | Last updated: 2026-02-04*