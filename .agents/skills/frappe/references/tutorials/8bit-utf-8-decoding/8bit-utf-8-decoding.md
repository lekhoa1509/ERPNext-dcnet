# How To: 8Bit Utf 8 Decoding

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 8bit utf 8 decoding

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

### Step 1: Assign text_content_bytes = b'\xed\x95\x9c\xea\xb8\x80\xe1\xa5\xa1\xe2\x95\xa5\xe0\xba\xaa\xe0\xa4\x8f'

```python
text_content_bytes = b'\xed\x95\x9c\xea\xb8\x80\xe1\xa5\xa1\xe2\x95\xa5\xe0\xba\xaa\xe0\xa4\x8f'
```

### Step 2: Assign text_content = text_content_bytes.decode(...)

```python
text_content = text_content_bytes.decode('utf-8')
```

### Step 3: Assign content_bytes = value

```python
content_bytes = b'MIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Disposition: inline\nContent-Transfer-Encoding: 8bit\nFrom: test1_@erpnext.com\nReply-To: test2_@erpnext.com\n' + text_content_bytes
```

### Step 4: Assign mail = Email(...)

```python
mail = Email(content_bytes)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(mail.text_content, text_content)
```


## Complete Example

```python
# Workflow
text_content_bytes = b'\xed\x95\x9c\xea\xb8\x80\xe1\xa5\xa1\xe2\x95\xa5\xe0\xba\xaa\xe0\xa4\x8f'
text_content = text_content_bytes.decode('utf-8')
content_bytes = b'MIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Disposition: inline\nContent-Transfer-Encoding: 8bit\nFrom: test1_@erpnext.com\nReply-To: test2_@erpnext.com\n' + text_content_bytes
mail = Email(content_bytes)
self.assertEqual(mail.text_content, text_content)
```

## Next Steps


---

*Source: test_email_body.py:181 | Complexity: Intermediate | Last updated: 2026-02-04*