# How To: Add Attachments By File Content

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add attachments by file content

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

### Step 3: Assign file_name = 'test_add_attachments_by_file_content.txt'

```python
file_name = 'test_add_attachments_by_file_content.txt'
```

### Step 4: Assign file_content = 'test_add_attachments_by_file_content'

```python
file_content = 'test_add_attachments_by_file_content'
```

### Step 5: Call add_attachments()

```python
add_attachments(comm.name, [{'fcontent': file_content, 'fname': file_name}])
```

### Step 6: Assign attached_file_name = frappe.db.get_value(...)

```python
attached_file_name = frappe.db.get_value('File', {'attached_to_name': comm.name, 'attached_to_doctype': comm.doctype})
```

### Step 7: Assign attached_file = frappe.get_doc(...)

```python
attached_file = frappe.get_doc('File', attached_file_name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(attached_file.file_name, file_name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(attached_file.get_content(), file_content)
```


## Complete Example

```python
# Workflow
to_list = ['to <to@test.com>']
comm = self.new_communication(recipients=to_list)
file_name = 'test_add_attachments_by_file_content.txt'
file_content = 'test_add_attachments_by_file_content'
add_attachments(comm.name, [{'fcontent': file_content, 'fname': file_name}])
attached_file_name = frappe.db.get_value('File', {'attached_to_name': comm.name, 'attached_to_doctype': comm.doctype})
attached_file = frappe.get_doc('File', attached_file_name)
self.assertEqual(attached_file.file_name, file_name)
self.assertEqual(attached_file.get_content(), file_content)
```

## Next Steps


---

*Source: test_communication.py:427 | Complexity: Advanced | Last updated: 2026-02-04*