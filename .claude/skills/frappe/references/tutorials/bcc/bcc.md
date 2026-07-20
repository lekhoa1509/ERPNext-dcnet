# How To: Bcc

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bcc

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

### Step 1: Assign bcc_list = value

```python
bcc_list = ['bcc+1@test.com', 'cc <bcc+2@test.com>']
```

### Step 2: Assign user = self.new_user(...)

```python
user = self.new_user(email='bcc+2@test.com', enabled=0)
```

### Step 3: Assign comm = self.new_communication(...)

```python
comm = self.new_communication(bcc=bcc_list)
```

### Step 4: Assign res = comm.get_mail_bcc_with_displayname(...)

```python
res = comm.get_mail_bcc_with_displayname()
```

### Step 5: Call self.assertCountEqual()

```python
self.assertCountEqual(res, bcc_list[:1])
```

### Step 6: Call user.delete()

```python
user.delete()
```

### Step 7: Call comm.delete()

```python
comm.delete()
```


## Complete Example

```python
# Workflow
bcc_list = ['bcc+1@test.com', 'cc <bcc+2@test.com>']
user = self.new_user(email='bcc+2@test.com', enabled=0)
comm = self.new_communication(bcc=bcc_list)
res = comm.get_mail_bcc_with_displayname()
self.assertCountEqual(res, bcc_list[:1])
user.delete()
comm.delete()
```

## Next Steps


---

*Source: test_communication.py:382 | Complexity: Intermediate | Last updated: 2026-02-04*