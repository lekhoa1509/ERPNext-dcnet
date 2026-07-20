# How To: Add Attachments By Filename

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add attachments by filename

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

### Step 1: Assign to_list = value

```python
to_list = ['to <to@test.com>']
```

### Step 2: Assign comm = self.new_communication(...)

```python
comm = self.new_communication(recipients=to_list)
```

### Step 3: Assign file = frappe.new_doc(...)

```python
file = frappe.new_doc('File')
```

### Step 4: Assign file.file_name = 'test_add_attachments_by_filename.txt'

```python
file.file_name = 'test_add_attachments_by_filename.txt'
```

### Step 5: Assign file.content = 'test_add_attachments_by_filename'

```python
file.content = 'test_add_attachments_by_filename'
```

### Step 6: Call file.insert()

```python
file.insert(ignore_permissions=True)
```

### Step 7: Call add_attachments()

```python
add_attachments(comm.name, [file.name])
```

### Step 8: Assign unknown = frappe.db.get_value(...)

```python
attached_file_name, attached_content_hash = frappe.db.get_value('File', {'attached_to_name': comm.name, 'attached_to_doctype': comm.doctype}, ['file_name', 'content_hash'])
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(attached_content_hash, file.content_hash)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(attached_file_name, file.file_name)
```


## Complete Example

```python
# Workflow
to_list = ['to <to@test.com>']
comm = self.new_communication(recipients=to_list)
file = frappe.new_doc('File')
file.file_name = 'test_add_attachments_by_filename.txt'
file.content = 'test_add_attachments_by_filename'
file.insert(ignore_permissions=True)
add_attachments(comm.name, [file.name])
attached_file_name, attached_content_hash = frappe.db.get_value('File', {'attached_to_name': comm.name, 'attached_to_doctype': comm.doctype}, ['file_name', 'content_hash'])
self.assertEqual(attached_content_hash, file.content_hash)
self.assertEqual(attached_file_name, file.file_name)
```

## Next Steps


---

*Source: test_communication.py:408 | Complexity: Advanced | Last updated: 2026-02-04*