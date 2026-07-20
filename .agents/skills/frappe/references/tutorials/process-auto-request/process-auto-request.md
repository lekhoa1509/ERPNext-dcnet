# How To: Process Auto Request

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test process auto request

## Prerequisites

**Required Modules:**
- `datetime`
- `frappe`
- `frappe.tests`
- `frappe.website.doctype.personal_data_deletion_request.personal_data_deletion_request`
- `frappe.website.doctype.personal_data_download_request.test_personal_data_download_request`


## Step-by-Step Guide

### Step 1: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Website Settings', 'auto_account_deletion', '1')
```

### Step 2: Assign date_time_obj = value

```python
date_time_obj = datetime.strptime(self.delete_request.creation, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-2)
```

### Step 3: Call self.delete_request.db_set()

```python
self.delete_request.db_set('creation', date_time_obj)
```

### Step 4: Call self.delete_request.db_set()

```python
self.delete_request.db_set('status', 'Pending Approval')
```

### Step 5: Call process_data_deletion_request()

```python
process_data_deletion_request()
```

### Step 6: Call self.delete_request.reload()

```python
self.delete_request.reload()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(self.delete_request.status, 'Deleted')
```


## Complete Example

```python
# Workflow
frappe.db.set_single_value('Website Settings', 'auto_account_deletion', '1')
date_time_obj = datetime.strptime(self.delete_request.creation, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-2)
self.delete_request.db_set('creation', date_time_obj)
self.delete_request.db_set('status', 'Pending Approval')
process_data_deletion_request()
self.delete_request.reload()
self.assertEqual(self.delete_request.status, 'Deleted')
```

## Next Steps


---

*Source: test_personal_data_deletion_request.py:61 | Complexity: Intermediate | Last updated: 2026-02-04*