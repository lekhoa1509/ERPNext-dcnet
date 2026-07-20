# How To: User Data Creation

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test user data creation

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.contacts.doctype.contact.contact`
- `frappe.core.doctype.user.user`
- `frappe.tests`
- `frappe.website.doctype.personal_data_download_request.personal_data_download_request`


## Step-by-Step Guide

### Step 1: Assign user_data = json.loads(...)

```python
user_data = json.loads(get_user_data('test_privacy@example.com'))
```

### Step 2: Assign contact_name = get_contact_name(...)

```python
contact_name = get_contact_name('test_privacy@example.com')
```

### Step 3: Assign expected_data = value

```python
expected_data = {'Contact': frappe.get_all('Contact', {'name': contact_name}, ['*'])}
```

### Step 4: Assign expected_data = json.loads(...)

```python
expected_data = json.loads(json.dumps(expected_data, default=str))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual({'Contact': user_data['Contact']}, expected_data)
```


## Complete Example

```python
# Workflow
user_data = json.loads(get_user_data('test_privacy@example.com'))
contact_name = get_contact_name('test_privacy@example.com')
expected_data = {'Contact': frappe.get_all('Contact', {'name': contact_name}, ['*'])}
expected_data = json.loads(json.dumps(expected_data, default=str))
self.assertEqual({'Contact': user_data['Contact']}, expected_data)
```

## Next Steps


---

*Source: test_personal_data_download_request.py:21 | Complexity: Intermediate | Last updated: 2026-02-04*