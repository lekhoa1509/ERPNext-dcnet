# How To: Sendmail

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sendmail

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

### Step 2: Assign cc_list = value

```python
cc_list = ['cc <cc+1@test.com>', 'cc <cc+2@test.com>']
```

### Step 3: Assign comm = self.new_communication(...)

```python
comm = self.new_communication(recipients=to_list, cc=cc_list)
```

### Step 4: Call comm.send_email()

```python
comm.send_email()
```

### Step 5: Assign doc = EmailQueue.find_one_by_filters(...)

```python
doc = EmailQueue.find_one_by_filters(communication=comm.name)
```

### Step 6: Assign mail_receivers = value

```python
mail_receivers = [each.recipient for each in doc.recipients]
```

### Step 7: Call self.assertIsNotNone()

```python
self.assertIsNotNone(doc)
```

### Step 8: Call self.assertCountEqual()

```python
self.assertCountEqual(to_list + cc_list, mail_receivers)
```

### Step 9: Call doc.delete()

```python
doc.delete()
```

### Step 10: Call comm.delete()

```python
comm.delete()
```


## Complete Example

```python
# Workflow
to_list = ['to <to@test.com>']
cc_list = ['cc <cc+1@test.com>', 'cc <cc+2@test.com>']
comm = self.new_communication(recipients=to_list, cc=cc_list)
comm.send_email()
doc = EmailQueue.find_one_by_filters(communication=comm.name)
mail_receivers = [each.recipient for each in doc.recipients]
self.assertIsNotNone(doc)
self.assertCountEqual(to_list + cc_list, mail_receivers)
doc.delete()
comm.delete()
```

## Next Steps


---

*Source: test_communication.py:395 | Complexity: Advanced | Last updated: 2026-02-04*