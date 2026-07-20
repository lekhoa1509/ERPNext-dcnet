# How To: Signature In Email Content

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test signature in email content

## Prerequisites

**Required Modules:**
- `typing`
- `frappe`
- `frappe.core.doctype.communication.communication`
- `frappe.core.doctype.communication.email`
- `frappe.email.doctype.email_queue.email_queue`
- `frappe.tests`
- `frappe.contacts.doctype.contact.contact`
- `frappe.email.doctype.email_account.email_account`
- `frappe.desk.form.load`


## Step-by-Step Guide

### Step 1: Assign email_account = create_email_account(...)

```python
email_account = create_email_account()
```

### Step 2: Assign signature = value

```python
signature = email_account.signature
```

### Step 3: Assign base_communication = value

```python
base_communication = {'doctype': 'Communication', 'communication_medium': 'Email', 'subject': 'Document Link in Email', 'sender': 'comm_sender@example.com'}
```

### Step 4: Assign comm_with_signature = frappe.get_doc.insert(...)

```python
comm_with_signature = frappe.get_doc(base_communication | {'content': f'<div class="ql-editor read-mode">\n\t\t\t\tHi,\n\t\t\t\tHow are you?\n\t\t\t\t</div><p></p><br><p class="signature">{signature}</p>'}).insert(ignore_permissions=True)
```

### Step 5: Assign comm_without_signature = frappe.get_doc.insert(...)

```python
comm_without_signature = frappe.get_doc(base_communication | {'content': '<div class="ql-editor read-mode">\n\t\t\t\tHi,\n\t\t\t\tHow are you?\n\t\t\t\t</div>'}).insert(ignore_permissions=True)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(comm_with_signature.content, comm_without_signature.content)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(comm_with_signature.content.count(signature), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(comm_without_signature.content.count(signature), 1)
```


## Complete Example

```python
# Workflow
email_account = create_email_account()
signature = email_account.signature
base_communication = {'doctype': 'Communication', 'communication_medium': 'Email', 'subject': 'Document Link in Email', 'sender': 'comm_sender@example.com'}
comm_with_signature = frappe.get_doc(base_communication | {'content': f'<div class="ql-editor read-mode">\n\t\t\t\tHi,\n\t\t\t\tHow are you?\n\t\t\t\t</div><p></p><br><p class="signature">{signature}</p>'}).insert(ignore_permissions=True)
comm_without_signature = frappe.get_doc(base_communication | {'content': '<div class="ql-editor read-mode">\n\t\t\t\tHi,\n\t\t\t\tHow are you?\n\t\t\t\t</div>'}).insert(ignore_permissions=True)
self.assertEqual(comm_with_signature.content, comm_without_signature.content)
self.assertEqual(comm_with_signature.content.count(signature), 1)
self.assertEqual(comm_without_signature.content.count(signature), 1)
```

## Next Steps


---

*Source: test_communication.py:259 | Complexity: Advanced | Last updated: 2026-02-04*