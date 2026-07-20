# How To: Get Communication Data

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get communication data

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

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Note', 'get communication data')
```

### Step 2: Assign note = frappe.get_doc.insert(...)

```python
note = frappe.get_doc({'doctype': 'Note', 'title': 'get communication data', 'content': 'get communication data'}).insert(ignore_permissions=True)
```

### Step 3: Assign comm_note_1 = frappe.get_doc.insert(...)

```python
comm_note_1 = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'Test Get Communication Data 1', 'communication_medium': 'Email'}).insert(ignore_permissions=True)
```

### Step 4: Call comm_note_1.add_link()

```python
comm_note_1.add_link(link_doctype='Note', link_name=note.name, autosave=True)
```

### Step 5: Assign comm_note_2 = frappe.get_doc.insert(...)

```python
comm_note_2 = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'Test Get Communication Data 2', 'communication_medium': 'Email'}).insert(ignore_permissions=True)
```

### Step 6: Call comm_note_2.add_link()

```python
comm_note_2.add_link(link_doctype='Note', link_name=note.name, autosave=True)
```

### Step 7: Assign comms = get_communication_data(...)

```python
comms = get_communication_data('Note', note.name, as_dict=True)
```

### Step 8: Assign data = value

```python
data = [comm.name for comm in comms]
```

### Step 9: Call self.assertIn()

```python
self.assertIn(comm_note_1.name, data)
```

### Step 10: Call self.assertIn()

```python
self.assertIn(comm_note_2.name, data)
```


## Complete Example

```python
# Workflow
from frappe.desk.form.load import get_communication_data
frappe.delete_doc_if_exists('Note', 'get communication data')
note = frappe.get_doc({'doctype': 'Note', 'title': 'get communication data', 'content': 'get communication data'}).insert(ignore_permissions=True)
comm_note_1 = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'Test Get Communication Data 1', 'communication_medium': 'Email'}).insert(ignore_permissions=True)
comm_note_1.add_link(link_doctype='Note', link_name=note.name, autosave=True)
comm_note_2 = frappe.get_doc({'doctype': 'Communication', 'communication_type': 'Communication', 'content': 'Test Get Communication Data 2', 'communication_medium': 'Email'}).insert(ignore_permissions=True)
comm_note_2.add_link(link_doctype='Note', link_name=note.name, autosave=True)
comms = get_communication_data('Note', note.name, as_dict=True)
data = [comm.name for comm in comms]
self.assertIn(comm_note_1.name, data)
self.assertIn(comm_note_2.name, data)
```

## Next Steps


---

*Source: test_communication.py:182 | Complexity: Advanced | Last updated: 2026-02-04*