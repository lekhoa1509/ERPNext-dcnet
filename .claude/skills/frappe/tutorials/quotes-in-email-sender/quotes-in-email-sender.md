# How To: Quotes In Email Sender

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test quotes in email sender

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

### Step 1: Assign content_bytes = b'MIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Disposition: inline\nContent-Transfer-Encoding: 8bit\nTo: "\\"fail@example.com\\" via ABC"  <success@example.com>\nFrom: "\\"fail@example.com\\" via DEF"  <success@example.com>\nReply-To: "\\"fail@example.com\\" via GHI"  <success@example.com>\nCC: "\\"fail@example.com\\" via JKL"  <success@example.com>\n'

```python
content_bytes = b'MIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Disposition: inline\nContent-Transfer-Encoding: 8bit\nTo: "\\"fail@example.com\\" via ABC"  <success@example.com>\nFrom: "\\"fail@example.com\\" via DEF"  <success@example.com>\nReply-To: "\\"fail@example.com\\" via GHI"  <success@example.com>\nCC: "\\"fail@example.com\\" via JKL"  <success@example.com>\n'
```

### Step 2: Assign mail = Email(...)

```python
mail = Email(content_bytes)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(mail.from_email, 'success@example.com')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(mail.from_real_name, 'failexamplecom via DEF')
```

### Step 5: Assign email_account = frappe._dict(...)

```python
email_account = frappe._dict({'email_id': 'receive@example.com'})
```

### Step 6: Assign mail = InboundMail(...)

```python
mail = InboundMail(content_bytes, email_account)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(communication.sender_full_name, 'failexamplecom via DEF')
```


## Complete Example

```python
# Workflow
content_bytes = b'MIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Disposition: inline\nContent-Transfer-Encoding: 8bit\nTo: "\\"fail@example.com\\" via ABC"  <success@example.com>\nFrom: "\\"fail@example.com\\" via DEF"  <success@example.com>\nReply-To: "\\"fail@example.com\\" via GHI"  <success@example.com>\nCC: "\\"fail@example.com\\" via JKL"  <success@example.com>\n'
mail = Email(content_bytes)
self.assertEqual(mail.from_email, 'success@example.com')
self.assertEqual(mail.from_real_name, 'failexamplecom via DEF')
email_account = frappe._dict({'email_id': 'receive@example.com'})
mail = InboundMail(content_bytes, email_account)
communication: Communication = mail.process()
self.assertEqual(communication.sender_full_name, 'failexamplecom via DEF')
```

## Next Steps


---

*Source: test_email_body.py:209 | Complexity: Intermediate | Last updated: 2026-02-04*